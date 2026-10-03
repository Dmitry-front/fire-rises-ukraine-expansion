# TFR_CHEATSHEET.md — шпаргалка по коду TFR

Короткий справочник для автора и Claude: как работают эффекты именно TFR (не ванильные). Дополнять по ходу работы.
Метки: **[ПОДТВЕРЖДЕНО]** — автор или референс `_reference/`; **[ПРОВЕРИТЬ]** — не сверено с кодом TFR.

---

## 1. Экономика: сумма + инфляция

Эффекты TFR работают парой: сначала временная переменная с суммой, потом эффект, который её применяет.

```
set_temp_variable = {
	var = income_var_temp
	value = -1.8
}
add_income_with_inflation = yes
```

- **`add_income_with_inflation = yes`** — сумма из `income_var_temp` **пересчитывается с учётом инфляции страны** [ПОДТВЕРЖДЕНО, автор]. Расход `-1.8` на деле будет больше, чем 1.8, а доход `+3.5` — тоже масштабируется инфляцией.
- **Переменная без эффекта ничего не делает.** `set_temp_variable` с `income_var_temp`, после которой нет `add_income_with_inflation = yes`, — тихая ошибка: игра не ругается, эффекта нет. Так было в `UKR_t_digital_registry` и `UKR_t_cyber_troops` (исправлено).
- **Знак:** `income_var_temp` положительный — доход, отрицательный — расход [ПОДТВЕРЖДЕНО, автор].
- Долг — та же схема: `debt_var_temp` + `add_debt_with_inflation = yes` (пример в референсе: `value = 20`) [ПОДТВЕРЖДЕНО, референс]. Знак долга: плюс = долг растёт [ПРОВЕРИТЬ].
- Варианты без инфляции: `add_income`, `add_debt` [ПРОВЕРИТЬ, когда использовать].

## 2. Развитие (пары «переменная + эффект»)

| Переменная | Эффект | Что меняет |
|---|---|---|
| `industrial_development_var_temp` | `add_industrial_development = yes` | промышленное развитие |
| `military_development_var_temp` | `add_military_development = yes` | военное развитие |
| `society_development_var_temp` | `add_society_development = yes` | общество (свободы, гражданские институты) |
| `poverty_development_var_temp` | `add_poverty_development = yes` | бедность (минус = беднее, [ПРОВЕРИТЬ] знак) |
| `academic_development_var_temp` | `add_academic_development = yes` | наука и образование |

Правило то же: без эффекта переменная пропадает.

Постоянные добавки в идеях (раз в месяц): `industrial_development_monthly`, `military_development_monthly`, `society_development_monthly`, `poverty_development_monthly`, `academic_development_monthly`. Порядок величин в наших идеях: `0.001`–`0.01` в месяц.

## 3. Динамические модификаторы

После изменения переменной динамического модификатора — `force_update_dynamic_modifier = yes` (правило `CLAUDE.md`).

## 4. Министры (советники-идеи)

Министр в TFR — это **идея** в слоте страны. Слоты UKR (файл `common/ideas/TFR_ideas_UKR.txt`):

| Слот | Роль | Черты в нашем коде (префикс) |
|---|---|---|
| `head_minister` | премьер | `hog_*` |
| `economic_minister` | экономика | `eco_*` |
| `foreign_minister` | МИД | `for_*` |
| `interior_minister` | МВД | `sec_*` (и `eco_corrupt` у Авакова) |
| `theorist_minister` | оборона | `army_chief_*` |
| `intelligence_minister` | разведка | `int_*` |

Идея-министр: `picture`, `allowed = { original_tag = UKR }`, `visible`, `traits = { ... }`. Заменить министра: `swap_ideas = { remove_idea = ... add_idea = ... }` или `remove_ideas` + `add_ideas`.

**Черты, которые встречаются в нашем коде** (определения лежат в TFR, не в репозитории — новых имён не придумывать, сверять): `hog_silent_workhorse`, `hog_uncontested_prime_minister`, `hog_liberal_socialist`, `hog_backroom_backstabber`, `eco_economic_organizer`, `eco_keynesian_economy`, `eco_balanced_budget_economy`, `eco_industrialiser`, `eco_corrupt`, `for_free_trader`, `for_biased_intellectual`, `sec_populist_propagandist`, `sec_efficent_organizer` (в TFR именно так, с опечаткой), `int_encryptor`, `int_balanced_cryptographer`, `army_chief_reform_2`.

## 5. Прочее

- Первый фокус кризисной ветки не дороже 3; 1 cost = 7 дней.
- Тире `—`, `–` и `…` в локализации запрещены (шрифт показывает «?»).
- Скриптовые `.txt` — UTF-8 **без BOM** (с BOM не грузились идеи); `.yml` — **с BOM**.
