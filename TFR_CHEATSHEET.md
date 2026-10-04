# TFR_CHEATSHEET.md - шпаргалка по коду TFR

Справочник для автора и Claude: что делают эффекты, триггеры и модификаторы именно TFR (не ванильные), с примерами и масштабами величин.
Составлен 03.10.2026 по `_reference/` и по оригинальным TFR-файлам в репозитории (`TFR_*_UKR*`, `common/scripted_triggers/*TFR*`, игровые тексты `ABT_MONEY_*` в локализации). **Дополнен 04.10.2026** по расширенному набору референсов: законы, идеологии, дерево каждой России, фокусы Германии и Франции, черты, категории решений. Таблицы «что вообще существует в TFR» (законы, подидеологии, черты, модификаторы, здания) вынесены в **`TFR_CATALOG.md`** (генерируется `python3 _tools/build_catalog.py`); здесь - правила, рецепты и выводы. Дополнять по ходу работы.

## 0. Как читать

**Источник каждого утверждения:**
- **(код)** — прочитано в оригинальном коде TFR, лежащем в репозитории. Самый надёжный источник.
- **(реф)** — выведено из того, как это использует SOV в `_reference/`. Надёжно по смыслу, но определения эффекта мы не видим.
- **(автор)** — сказано автором.
- **[ПРОВЕРИТЬ]** — гипотеза, нужна сверка с игрой или кодом TFR.

**Главное ограничение.** Определения TFR-эффектов (`add_income`, `add_society_development`, `change_economy_type_*` и т. д.) лежат в `common/scripted_effects/` самого TFR. В репозитории их **нет**, мы видим только их использование. В репозитории лежат лишь TFR-скриптовые **триггеры** (`common/scripted_triggers/`), и они раскрывают, как устроены переменные под эффектами.

**Шкалы:** `add_stability`, `add_war_support`, `add_popularity` — доли (0.05 = 5 %). `add_political_power` — очки (25–100). Деньги — **миллиарды** (см. раздел 1).

### Карта `_reference/` (на 04.10.2026)

Все файлы начинаются с `_reference` (папка в игру не грузится), всего около 200 тыс. строк. Имена ниже даны без префикса `_referenceTFR_` / `_reference00_TFR_`.

| Файл | Что внутри |
|---|---|
| `national_focus_SOV.txt` | дерево Путина/ЕР (80 фокусов, `SOV_declare_smo`) и 5 общих `shared_focus` |
| `national_focus_SOV_medvedev.txt` | дерево Медведева/ЕР (654 фокуса, `SOV_address_the_nation`) |
| `national_focus_SOV_communist_new.txt` | КПРФ, id `SOV_communist` (327) |
| `national_focus_SOV_fascist.txt` | ЛДПР, id `SOV_ldpr_gaming` (449) |
| `national_focus_SOV_dugin.txt`, `_wagner.txt`, `_navalny.txt` | Дугин (69), Вагнер (47), Навальный (9, плюс 71 в войне НАТО) |
| `national_focus_GER.txt`, `_FRA.txt` | Германия (163), Франция (205): образцы «полного» контента не-SOV страны |
| `decisions_SOV.txt`, `decision_categories_SOV.txt` | 1148 решений в 53 категориях; 58 описаний категорий |
| `ideas_SOV.txt` | 2095 идей (духи, министры, скрытые) |
| `characters_SOV.txt` | 255 персонажей (портреты, роли) |
| `ideologies.txt` | 11 идеологий и 180 подидеологий |
| `laws_{economic,manpower,social,development}.txt` (`_reference00_TFR_laws_*`) | законы, 24 слота |
| `traits_*` (9 файлов) | черты: глава государства, правительство, экономика, МИД, МВД, разведка, военные, компании, идеологии |
| `idea_tags.txt` | `idea_categories`: слоты министров, законов, развития, армейские слоты |
| `buildings.txt`, `01_landmark_buildings.txt` | типы зданий |
| `generic_leader_abilities.txt` | способности лидеров |

**Нет в рабочей копии, но лежит в истории git** (удалены в коммите «Ref_new», последний коммит с ними `bc699df`): `events_SOV` (49 тыс. строк, события `russia.*` и `russiaflavor.*`), `scripted_effects_SOV`, `bop_SOV`, `traits_april`. Достать: `git show bc699df:_reference/Reference_TFR_events_SOV.txt > /tmp/x.txt`. Пометка **(реф-события)** ниже означает, что вывод сделан по ним.

**Чего референсы не показывают вообще:** определения scripted effects (`add_income`, `add_society_development`, `focus_unlock` и т. д. - видно только применение); `on_actions` TFR (поэтому неизвестно, кто вызывает `russia.76` и `ukraine.13`); события других пространств имён (`ukraine.*` оригинала, `news.*`, `nato.*`, `germany.*`, `france.*`); локализацию TFR (тексты тултипов вроде `change_economic_law_tooltip` не видны, смысл по названию [ПРОВЕРИТЬ]).

**Как искать аналог перед тем, как писать механику:** `grep -rn "ключевое_слово" _reference/` (эффект, флаг, идея), затем смотреть окружение найденного блока. Для структуры «как TFR делает N» самые полезные деревья - `GER` (полная не-российская страна, кабинеты, партии, ЕС) и `SOV_medvedev` (самое большое).

---

## 1. Экономика: ликвидность, долг, инфляция

### 1.1. Модель (код + локализация `ABT_MONEY_2`, реф)

| Переменная страны | Смысл |
|---|---|
| `income_var` | **Ликвидность** (резервы, «Доходы» в UI), в **млрд**. Её читают триггеры и стоимость решений: `income_var >= 25` = «нужно не меньше 25 млрд». Мелкие суммы пишутся долями: `0.002` = 200 млн |
| `debt_var` | **Долг**, в млрд |
| `inflation_var` | Инфляция страны как **доля** (0.15 = 15 %) |

По описанию TFR: каждый месяц считаются доходы и расходы; если ликвидность падает ниже нуля, расходы переходят в долг. Рост долга относительно реального ВВП бьёт по стабильности и доверию инвесторов. Реальный ВВП = номинальный ВВП с поправкой на инфляцию. На ежемесячный долг влияет процентная ставка.

### 1.2. Эффекты (все работают парой «переменная + эффект»)

```
set_temp_variable = { var = income_var_temp value = -2 }
add_income = yes
```

| Эффект | Переменная | Действие |
|---|---|---|
| `add_income = yes` | `income_var_temp` | Меняет ликвидность на значение как есть. **Плюс** = получили, **минус** = потратили (автор, реф) |
| `add_income_with_inflation = yes` | `income_var_temp` | То же, но сумма пересчитывается с учётом инфляции (автор). Триггер-аналог в коде считает `сумма × (1 + inflation_var)` (код) |
| `add_debt = yes` | `debt_var_temp` | Меняет долг. **Плюс** = долг вырос, **минус** = долг погашен (реф: «Syria Repays Debt» даёт −150) |
| `add_debt_with_inflation = yes` | `debt_var_temp` | То же с пересчётом на инфляцию |
| `add_inflation = yes` | `inflation_var_temp` | Меняет инфляцию. Пример TFR: снизить на 15 % от текущей, т. е. `inflation_var_temp = inflation_var`, затем `multiply_temp_variable = { var = inflation_var_temp value = -0.15 }` |

**Правила:**
- **Переменная без эффекта ничего не делает.** Игра не ругается (так было в `UKR_t_digital_registry`, `UKR_t_cyber_troops`, исправлено).
- **Не использовать `debttotal_temp`.** В 5 событиях SOV `add_debt` идёт после `debttotal_temp`, а остальные ~100 случаев используют `debt_var_temp`. Скорее всего, это ошибка TFR [ПРОВЕРИТЬ]. Нам: только `debt_var_temp`.
- **Где какой вариант (реф, оригинал UKR):** в **фокусах** TFR обычно берёт `*_with_inflation` (фокусы UKR: `add_income_with_inflation` с минусом; фокусы SOV: чаще `add_debt_with_inflation`). В **решениях и событиях** обычно просто `add_income` / `add_debt`. Это тенденция, не закон. Единого правила автор не называл [ПРОВЕРИТЬ].
- «Расход» можно оформить двумя способами: минус к `income_var_temp` (платим из ликвидности) или плюс к `debt_var_temp` (берём в долг). SOV в фокусах чаще берёт в долг, оригинал UKR чаще платит из ликвидности.

### 1.3. Масштаб сумм

| Контекст | Типичные значения (млрд) |
|---|---|
| SOV, решения (расход) | −45, −30, −25, −20, −10 (крупная держава; для Украины в 5–10 раз завышено) |
| SOV, решения (долг) | +10, +15, +25, +100, +150, +200 |
| SOV, фокусы (долг с инфляцией) | +5 … +200 |
| **Оригинал UKR, фокусы** | −2, −2.8, −5.5, −8, −13 (`add_income_with_inflation`) |
| **Оригинал UKR, решения** | −0.05 … −1 (мелкие, военные), −3, −8, −10, −20 (крупные) |
| **Оригинал UKR, события** | −0.1 … −0.75 (ущерб), +9 … +45 (помощь Запада, `with_inflation`) |
| Наш код (`income_var_temp`) | от −20 до +9, чаще ±1–3 |

Правило прикидки: смотреть оригинальный UKR. Для сравнения, фокус «покупки/программы» Украины стоит 2–13 млрд, не десятки.

### 1.4. Триггеры экономики (код, `common/scripted_triggers/*TFR*`)

Каждый принимает значение через временную переменную **перед** вызовом:

```
set_temp_variable = { income_trigger_temp_var = 5 }
has_income_greater_than_or_equals = yes
```

| Триггер | Временная переменная |
|---|---|
| `has_income_greater_than_or_equals` | `income_trigger_temp_var` |
| `has_debt_greater_than_or_equals` | `debt_trigger_temp_var` |
| `has_income_with_inflation_greater_than_or_equals` | `income_trigger_temp_var` (сам умножает на `1 + inflation_var`) |
| `has_debt_with_inflation_greater_than_or_equals` | `debt_trigger_temp_var` |

Проще, как делает SOV: `check_variable = { var = income_var value = 25 }` прямо в `custom_cost_trigger` (см. раздел 7).

---

## 2. Развитие (код + реф)

Шесть шкал, у каждой читаемая переменная `<имя>_development_var`:

| Шкала | Переменная под эффект | Эффект | Читаемая переменная |
|---|---|---|---|
| Промышленность | `industrial_development_var_temp` | `add_industrial_development = yes` | `industrial_development_var` |
| Военное | `military_development_var_temp` | `add_military_development = yes` | `military_development_var` |
| Общество | `society_development_var_temp` | `add_society_development = yes` | `society_development_var` |
| Бедность / социальная защита | `poverty_development_var_temp` | `add_poverty_development = yes` | `poverty_development_var` |
| Наука и образование | `academic_development_var_temp` | `add_academic_development = yes` | `academic_development_var` |
| Сельское хозяйство | `farming_development_var_temp` | `add_farming_development = yes` | `farming_development_var` |

**Знак «бедности»** (реф): плюс = лучше. Плюс стоит в «Государство для трудящегося», «Народная программа», «Технократическая администрация» и т. п. Событие «разгром/распад» ставит −0.5 на все шкалы сразу. То есть `poverty_development` = «развитие социальной защиты», а не «уровень бедности».

**Масштаб разовых изменений:** обычно `±0.025`, `±0.05`, `±0.1`, `±0.15`; катастрофа `−0.5`; разовый максимум `0.25`–`0.45`.
**Масштаб в месяц** (модификаторы идей и решений, ключ `<имя>_development_monthly`):

| Ключ | Типичные значения |
|---|---|
| `society_development_monthly` | 0.005, 0.01, 0.015, 0.02, 0.05 (мин. −0.015) |
| `industrial_development_monthly` | 0.01, 0.015, 0.02, 0.03 |
| `military_development_monthly` | 0.005, 0.01, 0.015, 0.02 |
| `poverty_development_monthly` | 0.005, 0.01, 0.015, 0.02, 0.03 |
| `academic_development_monthly` | 0.01, 0.015, 0.03 |
| `farming_development_monthly` | 0.01, 0.015, 0.02, 0.03 |

В наших идеях порядок `0.001`–`0.02`, это в пределах разумного (оригинальный UKR добавляет и `0.002`).

**Триггеры:** `has_<имя>_development_greater_than_or_equals`, значение берётся из `<имя>_development_trigger_temp` (**без** `_var`: `society_development_trigger_temp` и т. д.).

**Флаг `manual_development_change_allowed`** (код): триггер `development` проверяет страновой флаг; он включает ручное изменение развития в UI. Аналоги: `manual_law_change_allowed` (триггер `non_changable_law`), `manual_head_minister_change_allowed` (`head_minister_trigger`). Как и когда TFR выставляет эти флаги [ПРОВЕРИТЬ].

**Законы развития и шкалы** (реф, `laws_development`): шесть шкал соответствуют шести законам-ступеням (`academic_development`, `farming_development`, `poverty_development`, `industry_development`, `military_development`, `society_development`; ступени `lower_*` ... `highest_*`, пять-шесть штук). У них `allowed_to_remove = { development = yes }` и нет цены: руками их не меняют, ступень определяется значением `<имя>_development_var` (пороги ступеней в референсах не видны [ПРОВЕРИТЬ]). Чтобы поднять ступень, двигаем шкалу эффектом `add_<имя>_development`, а не закон. Эффекты ступеней: `highest_poverty` = `personal_value` 1.2 и нет штрафа к стабильности, `lower_poverty` = `stability_factor` -0.2; `society_development` задаёт цены смены министров и законов (`lower_society` +20%, `highest_society` без наценки) и `dtg_threshold` (0.3 ... 1.05). Подробная таблица - `TFR_CATALOG.md`, раздел 1.

---

## 3. Законы (реф: `laws_*`; полный список - `TFR_CATALOG.md`, раздел 1)

Закон = идея в слоте категории с `law = yes`. Слотов **24**, в четырёх группах (`idea_categories`, файл `idea_tags`):

| Группа | Слоты | Цена смены |
|---|---|---|
| `economic_laws` | `economy` (экономическая мобилизация), `trade_laws`, `tax_laws`, `interest_rate_laws`, `welfare_laws`, `safety_laws` | 100 политсилы |
| `manpower_laws` | `mobilization_laws` (призыв), `female_service_laws`, `supervision_laws`, `training_laws`, `military_racial_integration_laws`, `draft_exemption_laws` | 100 |
| `social_laws` | `immigration_laws`, `education_laws`, `race_laws`, `female_laws`, `prison_laws`, `police_laws` | 100 |
| `development` | шесть шкал развития (раздел 2) | 0, автоматически |

**Две «мобилизации», не путать.** Слот `economy` - экономика военного времени: `mass_consumerism` (по умолчанию, L7) -> `civilian_mobilization` -> `early_` -> `partial_` -> `war_` -> `total_mobilization` -> `permanent_mobilization` (только у некоторых стран). Слот `mobilization_laws` - призыв: `lowest_` ... `highest_conscription`. Наши решения `UKR_*_mobilization_wave` (`TFR_decisions_UKR.txt`) законов не меняют и их не заменяют.

**Устройство.** `level` 1-8 (1 - самая «верхняя» ступень), в слоте один `default = yes` (стартовый закон страны, пока не задан иной). Поля: `cost = 100`, `removal_cost = -1`, `cancel_if_invalid = no`, `visible` / `available` / `allowed_to_remove`, `modifier`. Страновые законы (`SOV_`, `GER_`, `PRC_`, `USB_`, `FAF_` ...) закрыты условием `tag` в `visible`; нам доступны только общие.

**Старт Украины** (`history/countries/UKR - Ukraine.txt`): заданы `low_conscription`, `low_poverty`, `low_welfare`; остальное - по `default = yes` (проверить в окне законов в игре): `mass_consumerism`, `high_trade`, `medium_taxes`, `low_interest_rates`, `medium_safety`, `high_female_service`, `medium_supervision`, `medium_training`, `high_racial_integration`, `no_draft_exemptions`, `medium_immigration`, `medium_education`, `medium_race`, `medium_female`, `medium_prison`, `medium_police`.

**Как TFR меняет закон из скрипта (реф):**
1. `add_ideas = <закон>` ставит закон в слот вместо прежнего. TFR делает это в `hidden_effect`, а игроку показывает пару `custom_effect_tooltip = change_economic_law_tooltip` и `show_ideas_tooltip = <закон>` (также `change_security_law_tooltip` для `police`/`prison`, `change_trade_law_tooltip`). Это самый частый приём (63 раза).
2. `swap_ideas = { remove_idea = A add_idea = B }`, когда нужно снять конкретный особый закон (например, `civilian_mobilization` -> `partial_mobilization`).
3. Эффекты-шаги `increase_<X> = yes` / `decrease_<X> = yes` сдвигают закон на ступень. Встречаются: `increase_safety` (17), `increase_welfare` (15), `increase_police` (8), `decrease_taxes` (7), `increase_military` (6), `decrease_immigration` (5), `increase_taxes` (4), `increase_education` (4), `increase_society`, `increase_female`, `decrease_female`, `increase_race`, `decrease_race`, `increase_racial_integration`, `increase_poverty`, `increase_interest_rates`, `decrease_trade`, `decrease_safety`, `decrease_education`. Направление [ПРОВЕРИТЬ]: `increase_welfare` ведёт к `higher_welfare`, `decrease_taxes` - к `lower_taxes`. Для развития (`increase_military`, `increase_society`) это, скорее всего, сдвиг шкалы.
4. Проверка: `has_idea = <закон>` (219 раз в референсах).

**Условия доступа (`available`), которые мы обязаны учитывать:**

| Закон | Условие |
|---|---|
| `early_mobilization` | `has_war_support >= 0.15` |
| `partial_mobilization` | `>= 0.25` |
| `war_mobilization` | `>= 0.5` |
| `total_mobilization` | идёт война, `>= 0.8`, у противника ic_ratio > 0.5 к нашему |
| призыв | поддержка войны не ниже: `low_conscription` 0.1, `medium` 0.2, `high` 0.6, `higher` 0.7, `highest` 0.85 (последние три и `medium` - не для тоталитарных) |

(пороги призыва - из `has_unsupported_*_law` в коде TFR; мобилизации - из `available` законов.) **Следствие для Украины:** законы военного времени открываются поддержкой войны (`war_support`), а наш настрой её двигает: усталость (духи `UKR_war_spirit_fatigue_*`) даёт `war_support_factor` от -0.01 до -0.12, ненависть (`UKR_hate_dynamic`, 100+) - до +0.08. Значит, мобилизационные законы и настрой связаны реальным игровым прогрессом; учитывать в `ai_will_do` и в балансе (для `war_mobilization` нужно 0.5, для `total_mobilization` - 0.8).

**Масштаб эффектов (для расчёта собственных духов; значения из референса):**

| Призыв | `conscription` (доля) | Цена для промышленности (`industrial_capacity_factory`) |
|---|---|---|
| `lowest_conscription` | 0.002 | +0.10 |
| `lower_conscription` (def) | 0.005 | +0.05 |
| `low_conscription` | 0.01 | 0 |
| `medium_conscription` | 0.02 | 0 (`training_time_factor` +0.1) |
| `high_conscription` | 0.04 | -0.10 |
| `higher_conscription` | 0.08 | -0.30 |
| `highest_conscription` | 0.16 | -0.40 |

Налоги: `medium_taxes` = `tax_business_rate` 0.2 / `tax_personal_rate` 0.15; `higher_taxes` 0.3 / 0.25. Ставка: `lowest_interest_rates` 0 ... `highest_interest_rates` 0.2 (+ `inflation_monthly` от +0.003 до -0.005). Социальные расходы: `personal_expense` от 0 (`lower_welfare`) до 0.75 (`highest_welfare`).

---

## 4. Политика

### 4.1. Идеологии

Партий **11**, они же допустимые значения `ideology =` в `add_popularity`, `set_party_name`, `ruling_party` (код: список в `is_in_coalition`):
`authoritarian_democrat`, `communist`, `conservative`, `fascist`, `libertarian_socialist`, `market_liberal`, `national_socialist`, `nationalist`, `social_democrat`, `social_liberal`, `totalitarian_socialist`.

**Классификация (код):**
- `has_totalitarian_government`: `totalitarian_socialist`, `communist`, `national_socialist`, `fascist`, `nationalist`.
- `has_democratic_form_of_government`: `social_democrat`, `social_liberal`, `market_liberal`, `conservative`, `authoritarian_democrat`.
- `libertarian_socialist` не входит ни туда, ни туда.

**Подидеологии лидера.** Всего **180** в TFR (полный перечень по идеологиям - `TFR_CATALOG.md`, раздел 2). Подидеология задаётся в `country_leader = { ideology = ... }`, `promote_character = { ideology = ... }`; знак `*` в каталоге - `can_be_randomly_selected = no` (назначается только скриптом, это не запрет). Полезное для Украины:
- `social_liberal`: `neoliberalism` (Зеленский у нас), `centrist*`, `christian_democracy*`, `ultra_liberalism*`;
- `market_liberal`: `classical_liberalism`, `right_libertarianism`, `right_anarchism`;
- `conservative`: `neoconservative` (Порошенко, Тимошенко), `classical_conservatism`, `constitutionalist*` (Бойко), `right_populism*`, `national_conservativism_con`;
- `authoritarian_democrat`: `hybrid_regime` (Медведчук), `oligarchist*`, `auth_populism`, `corporatocracy`, `national_conservativism_auth`, `military_democracy*`, `ultra_conservatism*`;
- `nationalist`: `autocrat`, `military_junta` (Залужный после «переворота»), `radical_nationalism*`;
- `fascist`: `ethno_nationalism`, `classical_fascism`, `fascist_populism`, `national_syndicalism`; `national_socialist`: `neonazism`, `esoteric_fascism` (для нашего контента лучше не использовать);
- левые: `social_democrat` (`social_democracy`, `green_politics*`, `left_populism*`), `libertarian_socialist` (`left_anarchist`, `post_leftism`, `eco_socialism`, `communist_populism*`), `communist` (`marxism_leninism`, `trotskyism`, `anti_revisionist_communism`, `left_nationalism*`), `totalitarian_socialist` (`totalism`, `maoism`, `left_wing_junta`).
Все `ideology =` / `ruling_party =` в нашем коде существуют в TFR (проверено 04.10.2026: 32 значения).

### 4.2. Партии и выборы

| Что | Как (реф) |
|---|---|
| Популярность | `add_popularity = { ideology = X popularity = 0.05 }` (доля) |
| Название партии | `set_party_name = { ideology = X long_name = KEY name = KEY_short }` |
| Выборы | `set_politics = { ruling_party = X elections_allowed = yes/no election_frequency = 48 last_election = "2013.5.12" }` (частота в месяцах, дата строкой `"Г.М.Д"`) |
| Смена лидера | `add_country_leader_role = { character = X promote_leader = yes country_leader = { ideology = Y expire = "1.1.1.1" traits = { ... } } }`, затем при необходимости `retire_character`, `retire_country_leader`, `kill_country_leader` |
| Продвинуть персонажа | `promote_character = { character = X ideology = Y }` |
| Черты главы государства | `add_country_leader_trait`, `remove_country_leader_trait`, `swap_ruler_traits = { remove = hos_A add = hos_B }` |
| Косметический тег | `set_cosmetic_tag`, `drop_cosmetic_tag`, `has_cosmetic_tag` |
| Дрейф идеологий | ключ модификатора `<идеология>_drift = 0.01` (+ вправо). Встречаются: `fascist`, `authoritarian_democrat`, `social_democrat`, `conservative`, `communist`, `social_liberal`, `libertarian_socialist`, `market_liberal`, `totalitarian_socialist`, `nationalist`, у нас также `national_socialist_drift` |

### 4.3. Коалиции и крылья правящей партии (реф + код)

Идеология задаётся токеном: `token:conservative`.

```
set_temp_variable = { coalition_partner_var_temp = token:conservative }
add_to_coalition = yes            # добавить партнёра
remove_from_coalition = yes       # убрать (тоже читает coalition_partner_var_temp)
end_coalition = yes               # распустить всю коалицию

set_temp_variable = { ruling_party_wing_var_temp = token:libertarian_socialist }
add_ruling_party_wing = yes       # крыло внутри правящей партии
end_ruling_party_wings = yes      # убрать все крылья
```

**Триггеры коалиции (код):** `is_in_coalition_with_<идеология> = yes`, где идеология из списка 11 (каждый ставит `coalition_target` и проверяет страновую переменную `is_in_coalition_with_<идеология>`); `is_in_coalition = yes` — есть любая. Общий вариант: `set_temp_variable = { coalition_target = token:X }` + `has_coalition_with_target = yes`.

### 4.4. Тип государства и экономики (реф + реф-события; полный список по всем референсам, 04.10.2026)

Эффекты вида `change_government_type_<X> = yes` / `change_economy_type_<X> = yes`.

**Тип государства (18):** `provisional_government` (11 вхождений), `presidential_dictatorship` (8), `socialist_republic` (6), `semi_presidential_system` (5), `parliamentary_republic` (5), `communist_party_state` (5), `presidential_republic` (2), `military_dictatorship` (2), `revolutionary_front` (2), `ultranationalist_dictatorship` (2), `theocracy`, `semi_constitutional_monarchy`, `constitutional_monarchy`, `absolute_monarchy`, `peoples_democracy`, `fascist_dictatorship`, `eurasianist_system`, `counterintelligence_state`.

**Тип экономики (15):** `welfare_capitalism` (12; Германия и Франция), `capitalism` (8), `socialist_market` (7), `mixed_economy` (5), `planned_economy` (5), `state_capitalism` (5), `left_corporatism` (4), `command_economy` (4), `oligopolistic_capitalism` (3), `military_controlled` (3), `worker_controlled` (2), `corporatism` (2), `liberal_corporatism` (1), `minarchism` (1), `developed_socialism` (1).

- Запомнить/вернуть: `get_current_government_type = yes` + `restore_previous_government_type = yes`.
- Контексты в TFR: `liberal_corporatism` - дерево Медведева, фокус `SOV_state_corporations_liberalization` (линия Надеждина, «либерализация госкорпораций»; подмена идеи `SOV_nadezhdin_economy_*`, динамический модификатор); `worker_controlled` - «экономическая демократия» (`SOV_a_new_economy`, `SOV_adl_model_economy`, идея `SOV_new_socialist_economy_idea`); `minarchism` - ветка Навального; `capitalism` - либеральная линия ЕР; `corporatism` - ЛДПР и ЕР; `command_economy` - Дугин и «статистская модель»; `developed_socialism` - «брежневская» линия КПРФ.
- **Закрыто: TD-21.** `change_economy_type_liberal_corporatism` существует в TFR, наша обёртка `UKR_set_liberal_corporatism_economy` названа правильно.
- **TD-18 (закрыт 04.10.2026).** «Кооперативной экономики» под таким названием в референсах нет. По смыслу (рабочий контроль, экономическая демократия, кооперативы) ближе всего `worker_controlled`; сейчас `UKR_set_cooperative_economy` ставит `socialist_market`. Решение автора: ставим `worker_controlled`, исходная гипотеза записана комментарием в обёртке.
- `parliamentary_republic` существует (5 раз в событиях SOV), наш `ukraine_politics.508` корректен (TD-19, пункт про этот эффект закрыт).

### 4.5. Баланс сил (BoP) (реф)

`add_power_balance_value = { id = X value = Y }`, `set_power_balance`, `remove_power_balance`, `is_power_balance_in_range`, `has_power_balance`, `power_balance_value`, `power_balance_weekly` (в модификаторах). Наш BoP: `common/bop/UKR_bop.txt`.

Устройство баланса сил в TFR (реф-`bop_SOV`, `SOV_communist_party_balance`, `SOV_LDPR_balance`): корневые поля `initial_value`, `left_side`, `right_side`, `decision_category` (окно решений, где живёт шкала), центральный `range = { id min max modifier }` (рабочий компромисс, например `-0.15 ... 0.15`), две секции `side = { id icon range ... }` с диапазонами по убыванию силы (`-1 ... -0.9`, `-0.9 ... -0.65`, `-0.65 ... -0.35`, `-0.35 ... -0.15`) и `on_activate` / `on_deactivate` у каждого диапазона. В модификаторах диапазонов TFR чаще всего: `war_support_factor`, `political_power_gain`, `stability_factor`. Наш `UKR_bop.txt` построен тем же образом (проверено 04.10.2026: поля и порядок совпадают; пока без `on_deactivate`, они необязательны). Сами эффекты и триггеры управления (`add_power_balance_value`, `set_power_balance`, `power_balance_value`) в референсах используются 74 и 16 раз. Категории решений, привязанные к шкалам TFR (`SOV_LDPR_balance_category`, `SOV_communist_party_balance_category`, `SOV_medvedev_elections_balance_category`, `SOV_alikhanov_bop_category`), показывают, как оформлять окно решений вокруг шкалы.

### 4.6. Страновые «контент-теги» (код)

`has_content_tag` = страны с полным контентом (SOV, USA, JAP, PRC, FRA, GER, FPR и **UKR**, добавлена подмодом, пометка `#SubMod`); `has_skeleton_tag` = «скелетные» страны (ENG, ITA, BLR, TUR, ROM, NOV и др.); `is_relavent_tag` = любое из двух. Общие механики TFR могут проверять эти теги. Если на UKR что-то из TFR не срабатывает, смотреть сюда [ПРОВЕРИТЬ].

---

## 5. Министры и персонажи

Министр в TFR — **идея** в слоте страны (свой слот на роль). Слоты UKR (`common/ideas/TFR_ideas_UKR.txt`):

| Слот | Роль | Префикс черт |
|---|---|---|
| `head_minister` | премьер | `hog_*` |
| `economic_minister` | экономика | `eco_*` |
| `foreign_minister` | МИД | `for_*` |
| `interior_minister` | МВД | `sec_*` |
| `theorist_minister` | оборона | `theorist_*`, у нас также `army_chief_*` |
| `intelligence_minister` | разведка | `int_*` |

Идея-министр: `picture`, `allowed = { original_tag = UKR }`, `visible`, `traits = { ... }`. Замена: `swap_ideas = { remove_idea = A add_idea = B }` или `remove_ideas` + `add_ideas`.
**Пустой слот** (реф): идеи-заглушки `vacant_hog`, `vacant_eco`, `vacant_for`, `vacant_sec`, `vacant_int`, `vacant_theorist`; `add_ideas = vacant_X` после увольнения.
**Разблокировка министра** (реф): флаг + подсказки. Идея держится скрытой (`visible = { has_country_flag = ... }`), в опции события пишется `custom_effect_tooltip = unlock_hog_minister_tooltip` (также `unlock_eco_/sec_/for_/int_/theorist_minister_tooltip`, `appoint_head_minister_tooltip` и т. д.) + `show_ideas_tooltip = ИДЕЯ` + `set_country_flag`. Реальное `add_ideas` делают в `hidden_effect`.
**Увольнение** запрещено, если не разрешено: `set_can_be_fired_in_advisor_role = { character = X value = yes }`.
**Командиры:** `add_corps_commander_role`, `create_corps_commander`, `add_field_marshal_role`, `add_trait = { character = X slot = corps_commander trait = Y }`.

**Черты, встречающиеся в нашем коде** (определения лежат в TFR; новых имён не придумывать): `hog_silent_workhorse`, `hog_uncontested_prime_minister`, `hog_liberal_socialist`, `hog_backroom_backstabber`, `eco_economic_organizer`, `eco_keynesian_economy`, `eco_balanced_budget_economy`, `eco_industrialiser`, `eco_corrupt`, `for_free_trader`, `for_biased_intellectual`, `sec_populist_propagandist`, `sec_efficent_organizer` (в TFR с опечаткой), `int_encryptor`, `int_balanced_cryptographer`, `army_chief_reform_2`.
**Черты главы государства в реф** (префикс `hos_`): `hos_powerless_president`, `hos_peoples_president`, `hos_red_president`, `hos_initiative_apparatchik`, `hos_scandalous_reformer`, `hos_wounded_lion`, `hos_cowed_by_oligarchs`, `hos_aspiring_autocrat`. Флаг `head_of_gov_ui_enabled` включает интерфейс главы правительства [ПРОВЕРИТЬ].

**Каталог черт.** Полный список лежит в `TFR_CATALOG.md`, раздел 3 (глава правительства `hog_*` - 53 и `party_*` - 16, экономика `eco_*` - 51, МИД `for_*` - 28, МВД `sec_*` - 38, разведка `int_*` - 12, глава государства `hos_*` - 279 общих, военные - 172, компании - 36). **Правило: брать черты только из каталога, новых не придумывать.** Все 23 черты, использованные в нашем коде (`hog_`, `eco_`, `for_`, `sec_`, `int_`, `hos_`, `army_chief_reform_2`, `theorist_special_forces_expert`), в TFR существуют (проверено 04.10.2026). Слот `theorist_minister` (оборона) использует черты `theorist_*` (8 штук: `military_theorist`, `theorist_assymetrical_warfare_expert`, `theorist_cost_cutter`, `theorist_special_forces_expert`, `theorist_guerilla_warfare_expert`, `air_warfare_theorist`, `naval_theorist`, `blitzkrieg_theorist`). Черты `party_*` (16) сделаны под КПРФ (`#for CPRF`), `ide_*` - пустые заглушки идеологий.

**Типичный масштаб черты** (медианы по `hog_`/`eco_`/`sec_`): `political_power_gain` 0.05-0.15, `stability_factor` 0.02-0.05, `war_support_factor` 0.025-0.1; сильнейшие `hos_*` дают `stability_factor` до 0.25 и `political_power_gain` до 0.5. Черты главы государства часто несут `ai_focus_aggressive_factor` (в 37 случаях) - это влияет на поведение ИИ-страны.

**Персонажи (реф):** `characters_SOV` - 255 записей, из них только 25 имеют `advisor` (слоты `high_command` 12, `army_chief` 5, `air_chief` 4, `navy_chief` 3, `theorist` 1); министры правительства в TFR заданы **идеями** (раздел 5 выше), а персонаж часто содержит только `portraits`. Для `corps_commander` обязательны `skill`, `attack_skill`, `defense_skill`, `planning_skill`, `logistics_skill` и `traits`; `field_marshal` - те же поля; `navy_leader` - `maneuvering_skill`, `coordination_skill`. `can_be_captured` стоит у 72 персонажей. Для советника: `slot`, `idea_token`, `ledger`, `allowed`, `traits`, `cost = 100`, `ai_will_do`.

**Боевые портреты.** При начале войны TFR подменяет портреты: `set_portraits = { character = UKR_volodymyr_zelensky civilian = { large = "GFX_war_zelensky" } }` (аналогично `GFX_war_poroshenko`). Это делает дерево России (раздел 13), так что у Зеленского после старта войны будет «военный» портрет независимо от нашего файла персонажей.

---

## 6. Здания и регионы (реф)

| Что | Как |
|---|---|
| Здания TFR | вместо гражданских фабрик — `industrial_complex`; плюс `office_park`, `energy_farm`, `power_plant`, `nuclear_reactor`; также `arms_factory`, `infrastructure`, `bunker`, `synthetic_refinery`, `dockyard`, `air_base`, `anti_air_building`, `fuel_silo`, `supply_node`, `naval_base` |
| Стройка | `add_building_construction = { type = X level = N instant_build = yes }` |
| «Внестейтовая» стройка | `add_offsite_building = { type = X level = N }` |
| Слоты | `add_extra_state_shared_building_slots = N` |
| Категория региона | `increase_state_category = yes`, `set_state_category = megalopolis`; триггер `has_state_category` (`rural`, `village`) |
| Скорости строек (модификаторы) | `production_speed_buildings_factor`, `_industrial_complex_factor`, `_office_park_factor`, `_arms_factory_factor`, `_nuclear_reactor_factor`, `_energy_farm_factor`, `_infrastructure_factor`, `_rail_way_factor`, `_bunker_factor`, `_anti_air_building_factor` |
| Проверки (триггеры TFR) | `is_able_to_build_power_plant_in_state`, `is_able_to_build_energy_farm_in_state`, `is_able_to_build_nuclear_reactor_in_state` (они взаимоисключающие). В репозитории лежат **две копии** файла триггеров с одинаковыми именами (`00_TFR_scripted_triggers_ZZZ_generic.txt` и `TFR_scripted_triggers_ZZZ_generic.txt`, отличаются мелочами); не даёт ли это дублей в `error.log` [ПРОВЕРИТЬ] |

Полный список типов зданий (22 + 9 достопримечательностей) с базовой стоимостью - `TFR_CATALOG.md`, раздел 7; рецепт стройки - раздел 15.

---

## 7. Решения TFR

Каркас решения (реф):

```
SOV_xxx = {
	icon = GFX_...
	allowed = { ... }                # или visible
	visible = { ... }
	available = { ... }
	cost = 50                        # политсила
	custom_cost_trigger = { check_variable = { var = income_var value = 25 } }
	custom_cost_text = dx_more_than_25B
	days_remove = 60                 # длительность
	fire_only_once = yes
	cancel_if_not_visible = yes
	modifier = { ... }               # действует, пока идёт решение
	complete_effect = { ... }        # при запуске (здесь обычно платят)
	remove_effect = { ... }          # по завершении (здесь обычно награда)
	ai_will_do = { base = 5 }        # у решений всегда base (842 из 842); у фокусов по-разному, см. 8.4
}
```

- **Деньги в решении:** условие через `custom_cost_trigger` с `income_var` и текст `dx_more_than_<N>B` / `dx_more_than_<N>M`; сама оплата в `complete_effect` (`income_var_temp` −N + `add_income = yes`). Ключи `dx_more_than_*` в TFR есть для **своих** сумм (25B, 45B, 60B, 10B, 5B, 1B+25pp, 200M, 80M и т. д.). Для украинских сумм (0.5, 1.5, 3 млрд) нужно **свои** ключи `custom_cost_text` в нашей локализации [ПРОВЕРИТЬ, что чужие ключи не подойдут].
- Другие TFR-стоимости: `15cp_cost`, `30cp_cost` (командная сила), `15party_resource_cost` (SOV-ресурс), `5_stability_cost`, `5_war_support_cost`, `500inf_cost`. Ключи в TFR есть, у нас нужно проверять по месту.
- `ai_hint_pp_cost`, `priority`, `is_good = no`, `selectable_mission = no`, `days_mission_timeout`, `activate_mission`, `timeout_effect` — ванильные поля, но TFR использует их плотно (миссии-таймеры).
- `days_re_enable` при `fire_only_once = no` — повторный запуск.
- `highlight_states` + `on_map_mode = map_only` — подсветка регионов.
- **Кампании SOV:** `has_campaign_slot`, `add_campaign_slot`, `remove_campaign_slot` (слоты работают через `campaign_slot_var >= 1`, код); `*_international_campaign_slot`. Это общий механизм, но все примеры из SOV/НАТО-войны [ПРОВЕРИТЬ, нужен ли UKR].
- Отладка: `is_debug = yes` в `visible` прячет решение вне отладки.

**Статистика по референсу (1148 решений в 53 категориях)** - для калибровки новых решений:
- `ai_will_do = { base = N }` стоит у всех решений с ИИ (842 из 842 `base`); `factor` у решений не встречается (у фокусов бывает и то, и другое, см. раздел 8).
- `cost` (политсила): 50 (207), 100 (204), 15 (99), 75 (98), 35 (69), 25 (64), 30 (38), 20, 40, 10; есть 24 решения с `cost = 0`. Стоимость бывает переменной (`cost = SOV_propaganda_decision_cost_var`, 19 раз).
- `days_remove`: 100 (108), 20 (88), 30 (87), 50 (82), 31 (79), 5 (74), 15 (62), 35, 10, 60, 25, 180 - длительность «процесса», в конце срабатывает `remove_effect` (1033 из 1148 решений его имеют). `complete_effect` есть у 743.
- `fire_only_once = yes` у 953 (83%); повторяемые решения - `days_re_enable` (365 решений).
- `cancel_if_not_visible = yes` у 313; `visible` у 1100, `allowed` только у 261.
- Прочее: `custom_cost_trigger` + `custom_cost_text` (119 и 120), `priority` (102), `highlight_states` (78) + `on_map_mode` (49), `targets` (75) / `state_target` (53), миссии (`days_mission_timeout` 54, `timeout_effect` 53, `activation` 57, `is_good = no` 56), `targeted_modifier` (23), `ai_hint_pp_cost` (31), `cancel_trigger` (13), `selectable_mission` (18).
- Категории решений (`decision_categories`, 58 штук): ключи `icon` (всегда), `allowed`, `visible`, `visible_when_empty` (yes/no), `priority`, `picture` (21 категория), `scripted_gui` (9: окно с числами, как наше `UKR_war_mood_gui`). Приём TFR: категория видна, когда выполнен нужный фокус (`visible = { has_completed_focus = X }`), и пуста до этого (`visible_when_empty = no`, чтобы не светить пустую панель). Наши категории (`TFR_decision_categories_UKR.txt`) проще: в них часто нет `visible_when_empty`. Если пустая категория мешает - добавить `visible_when_empty = no`.
- Три категории SOV, полезные как образец: `SOV_ukrainian_insurgencies_category` (11 решений, три ступени распространения подполья - основа для блока 4), `SOV_LDPR_balance_category` и `SOV_communist_party_balance_category` (окна для `bop`).

---

## 8. Фокусы TFR (реф: 10 деревьев, 2074 фокуса; `GER`, `FRA`, `SOV_*`)

### 8.1. Стоимость
- **Стандарт - 5** (1177 из 2074, 57%), затем 4 (330), 3 (210), 2 (122), 6 (103), 1 (13), крупные 8-10 (11). 1 cost = 7 дней. В Германии 154 из 163 по 5, остальные по 4. Наши рамки (`CLAUDE.md`: 3-7, кризисные 1-3) совпадают с TFR; пятёрка - это «нормальный» фокус, не «средний».
- **Дробные cost - приём TFR: это число дней, делённое на 7.** `2.86` = 20 дней, `3.58` = 25 дней, `4.29` = 30 дней, `6.44` = 45 дней (встречаются также `3.5`, `4.5`, `4.3`, `2.9`, `2.2`, `7.1`, `7.2`); всего 67 фокусов в дереве КПРФ (ветки партийной политики и экономики), по одному-два в других деревьях. Значит, срок можно задавать в днях: `cost = дней / 7`, округляя до сотых. Для нас это разрешение на точную подгонку времени блока 1 к выборам 29.10.2023 (`DESIGN.md`, 4.2): целые cost не обязательны. Формулу «дни = cost × 7» подтверждает и автор (`defines`).
- Крупное: `SOV_declare_smo` = 30, «операции» войны = 10 (`SOV_operation_little_saturn`, `SOV_russian_revengeance`); один фокус с `cost = 0`.

### 8.2. Шапка дерева, выбор дерева, смена
```
focus_tree = {
	id = GER_tree_initial
	country = { factor = 0 modifier = { add = 20 original_tag = GER NOT = { has_country_flag = GER_communist_tree_flag } } }
	shared_focus = GER_united_and_undefeated
	focus = { ... }
}
```
- `country = { factor = 0 modifier = { add = N <условие> } }` - когда у страны подходят несколько деревьев, побеждает с большим итогом. У нас `add = 10 tag = UKR`; варианты внутри TFR управляются флагами (`GER_communist_tree_flag`).
- Смена дерева - `load_focus_tree = ID` (в TFR **всегда без** `keep_completed`: 0 вхождений; прогресс сохраняется тем, что общие фокусы повторяются под теми же id или заданы через `shared_focus`, а нужное «выполненное» ставят `complete_national_focus = ID`). Мы используем `keep_completed = yes` (ванильный синтаксис) - так и надо.
- `load_focus_tree = generic_focus` (12 раз) - страна теряет дерево и получает заглушку (распад, поражение).
- **`shared_focus`:** в шапке `shared_focus = ID`, а сам фокус описан отдельным блоком верхнего уровня `shared_focus = { id = ... }`. Он общий для нескольких деревьев и может иметь **иконку по условию**: `icon = { GFX_A = { условие } GFX_B = { условие } GFX_C = yes }`. В SOV так сделаны армейские фокусы, общие для Медведева, КПРФ и ЛДПР (`SOV_rollback_serdykovs_reforms`, `SOV_expand_ratnik_programme`). Для будущих «трёх Россий» и для общих военных фокусов опор блока 3 - готовый образец.

### 8.3. Поля фокуса (частота в 2074 фокусах)
`id`, `icon`, `x`, `y`, `cost`, `completion_reward` - у всех; `prerequisite` - 2382 (часто несколько), `relative_position_id` - **98%** (позиции почти везде относительные, а не абсолютные), `ai_will_do` - 54%, `available` - 32%, `mutually_exclusive` - 27%, `allow_branch` - 354, `available_if_capitulated` - 252, `cancel_if_invalid` - 95, `search_filters` - 68, `offset` - 42, `bypass_if_unavailable` - 36, `select_effect` - 27, `cancelable = no` - 21, `bypass` - 19, `will_lead_to_war_with` - 19, `continue_if_invalid` - 14.

- **`allow_branch = { условие }`** - ветка вообще не показывается, пока условие ложно (354 раза; флаги выборов, ковида, исходов). Именно так TFR делает «варианты дерева» внутри одного дерева (в Германии - ветки по итогам выборов 2021: `GER_die_linke_won_2021_flag`). Обычно в паре с `bypass_if_unavailable = yes`. **Это готовое решение для TD-15** (прятать фокусы блока 1 явно, а не скрытыми `available`).
- **`bypass = { условие }`** - фокус считается пройденным без награды, если условие верно (`has_country_flag = BLR_maidan`, `has_global_flag = second_nato_war_flag`).
- **`select_effect = { ... }`** - эффект в момент **выбора** фокуса (не завершения). В дереве КПРФ: `select_effect = { country_event = { id = russia.1501 days = 10 } }` - событие приходит посреди выполнения фокуса. Подходит нашим «кризисным» фокусам (событие во время фокуса).
- **`will_lead_to_war_with = TAG`** - предупреждение игроку; только у фокусов, объявляющих войну.
- `available_if_capitulated = yes` - 252; `cancelable = no` - для необратимых; `cancel_if_invalid = yes` - для зависящих от состояния.

### 8.4. `ai_will_do`
Единого стиля нет: Германия - `base = 50` (114 из 163), Франция - `base = 5`, деревья SOV - `factor` (10 / 25 / 35 / 100). **Большинство фокусов SOV вообще без `ai_will_do`** (дерево Медведева: 653 из 654), то есть TFR этого не требует. Внутри чаще всего: `has_idea`, `has_game_rule` (77), `has_completed_focus`, `date`. Наше правило «`ai_will_do` у каждого фокуса и `factor`, а не `base`» (`CLAUDE.md`) остаётся нашим стандартом; он безопасен, просто строже TFR.

### 8.5. Что кладут в награду (`completion_reward`)
Частота эффектов (по 10 деревьям): `unlock_decision_tooltip` 731, `add_ideas` 716, `add_popularity` 613, `country_event` 584, `swap_ideas` 523, `add_building_construction` 336, `add_political_power` 326, `add_timed_idea` 314, `add_stability` 273, `add_extra_state_shared_building_slots` 248, `add_war_support` 162, `set_party_name` 139, `random_owned_controlled_state` 142, `force_update_dynamic_modifier` 132, `add_to_coalition` 77, `add_power_balance_value` 74.

Приёмы TFR, которые стоит перенять:
- **Тултипы.** `custom_effect_tooltip = tooltip_white_line` (550 раз) - белая линия между группами эффектов; `unlock_decision_tooltip = ID` - фокус показывает, какие решения он откроет (само решение открывается условием `has_completed_focus`); `effect_tooltip = { ... }` + `hidden_effect = { ... }` - игроку показываем заголовок («смена идеи»), а техническую часть (динамические переменные, события) прячем. Список общих ключей-тултипов - раздел 10.
- **Временные идеи:** `add_timed_idea = { idea = X days = 350 }` (314) и продление `modify_timed_idea = { idea = X days = 50 }` (28); типичный срок 125-700 дней.
- **Стройки:** рецепт - в разделе 15.
- **Война и события:** `will_lead_to_war_with`, `declare_war_on = { target = X type = annex_everything }`, `add_named_threat = { threat = 20 name = KEY }`, `news_event`; события отложенные - `days`, `hours`, `random_days`.
- **Отладка:** `log = "[GetDateText]: [Root.GetName]: Focus ID"` (73 раза) - строка в `game.log` при завершении; удобно для проверки в игре.
- **Законы** (раздел 3), **тип государства/экономики** (4.4), **коалиции и партии** (4.2-4.3), **баланс сил** (4.5).
- `random_owned_controlled_state` / `every_controlled_state` / `random_list` / `random_select_amount` (90) - стандартный каркас случайных и массовых наград.

### 8.6. Калибровка величин (реф: медиана и частые значения в `completion_reward`)

| Эффект | Медиана | Частые значения | Диапазон |
|---|---|---|---|
| `add_stability` | 0.05 | 0.05 (77), 0.1 (55), -0.1 (31), 0.025, -0.05 | -0.25 ... 0.15 |
| `add_political_power` | 50 | 100 (88), 50 (63), 25, 75, -100 (27), 150 | -250 ... 250 |
| `add_war_support` | 0.05 | 0.05 (62), 0.1 (28), 0.025 | -0.25 ... 0.35 |
| `add_popularity` | 0.033 | 0.05 (157), 0.025, 0.02, 0.03, 0.1, -0.1 | -1 ... 0.5 |
| `society_development_var_temp` | 0.1 | 0.1 (25), 0.05, 0.15, 0.25 | -0.35 ... 0.25 |
| `industrial_development_var_temp` | 0.1 | 0.1 (27), 0.05, 0.15 | -0.45 ... 0.25 |
| `poverty_development_var_temp` | 0.1 | 0.1, 0.05, 0.15, 0.25 | -0.25 ... 0.25 |
| `military_development_var_temp` | 0.1 | 0.1 (17), 0.15, 0.05 | -0.15 ... 0.5 |
| `academic_development_var_temp` | 0.1 | 0.1 (13), 0.15 | -0.15 ... 0.3 |
| `farming_development_var_temp` | 0.15 | 0.15, 0.1, 0.05, 0.25 | 0.05 ... 0.3 |
| `add_manpower` | 10000 | 10000, 1000, -5000, 25000 | -20000 ... 200000 |
| `debt_var_temp` / `income_var_temp` (SOV) | 50 / 75 | 50, 100, 70 / 100 | для UKR делить на 5-10 |

Проверено 04.10.2026: наши `add_stability`, `add_war_support`, `add_political_power` в событиях, фокусах и решениях укладываются в эти диапазоны (выбросы - только в оригинальных событиях TFR). Шкалы развития у нас 0.001-0.35 - в рамках.

### 8.7. Прочие поля
`search_filters = { FOCUS_FILTER_POLITICAL }` - 68 раз из 2074 (то есть редкость; перечень фильтров в `TFR_CATALOG.md`, раздел 6). `offset`, `dynamic`, `mark_focus_tree_layout_dirty = yes` (10) - как в разделе 8.2. `focus_unlock = yes` (19) - TFR-эффект открытия контента фокусов; определение не видно [ПРОВЕРИТЬ].

---

## 9. Модификаторы идей и динамические модификаторы

**Экономические ключи TFR** (реф, типичные значения у SOV; для Украины брать пропорционально меньше):

| Ключ | Типичные значения | Смысл (по названию, [ПРОВЕРИТЬ] точная формула) |
|---|---|---|
| `consumer_goods_factor` | ±0.02 … ±0.1 | доля производства на потребление |
| `income_growth_factor` | ±0.02 … ±0.1 | рост доходов |
| `business_value_factor` | 0.05 … 0.25 | вклад бизнеса в ВВП |
| `personal_value_factor` | 0.05 … 0.25 | вклад личных расходов |
| `personal_expense_factor` | 0.025 … 0.25 | расходы населения |
| `expense_growth_factor` | 0.005 … 0.25 | рост расходов |
| `misc_expense` | 5 … 45 (SOV); 0.02 (UKR) | постоянный расход, млрд |
| `misc_income` | 15 | постоянный доход |
| `interest_rate_factor` | 0.05 / −0.2 | процентная ставка |
| `tax_business_rate_factor` | −0.25 | налог на бизнес |
| `inflation_monthly_factor` | −0.5 | месячная инфляция |
| `monthly_population` | −0.15 … 0.15 | рост населения |
| `civilian_factory_use` | 1 … 5 | занятость гражданских фабрик |
| `industrial_capacity_factory` | ±0.015 … 0.15 | мощность фабрик |
| `production_lack_of_resource_penalty_factor`, `local_resources_factor`, `min_export_factor` | | ресурсы и экспорт |
| `economic_minister_cost_factor`, `interior_minister_cost_factor`, `trade_laws_cost_factor`, `tax_laws_cost_factor`, `welfare_laws_cost_factor` | | цены смены министров и законов |
| `political_power_gain`, `political_power_cost`, `political_power_factor` | | политсила |
| `stability_weekly`, `war_support_weekly`, `stability_factor`, `war_stability_factor` | | стабильность и поддержка |
| `resistance_target_on_our_occupied_states`, `resistance_decay_..._`, `resistance_growth_..._`, `compliance_gain`, `compliance_growth` | | оккупация (понадобится в блоке 4) |

**Шаблон динамического модификатора (реф):** значения ключей берутся из **переменных страны с тем же именем, что и ключ + `_dynamic`**:

```
SOV_xxx_dynamic = { enable = {...} remove_trigger = {...}  consumer_goods_factor = SOV_xxx_consumer_goods_factor_dynamic ... }
```

Меняя переменную (`add_to_variable` / `set_variable`), нужно вызвать `force_update_dynamic_modifier = yes`. SOV создаёт десятки таких переменных на один модификатор (механика «ступеней»). Наш пример: `UKR_hate_dynamic` (там значения заданы константами по порогам `UKRhate`).

**Словарь ключей.** Полная таблица модификаторов (283 ключа с диапазонами) - `TFR_CATALOG.md`, раздел 4. Ориентиры масштаба (медиана; диапазон):

| Ключ | Медиана | Диапазон |
|---|---|---|
| `stability_factor` | 0.025 | -0.5 ... 0.25 |
| `political_power_gain` | 0.025 | -0.65 ... 0.75 |
| `political_power_factor` | -0.03 | -0.5 ... 0.5 |
| `war_support_factor` | 0.05 | -0.45 ... 0.25 |
| `society_development_monthly` | 0.01 | -0.1 ... 0.05 |
| `poverty_development_monthly` | 0.005 | -0.1 ... 0.15 |
| `industrial_development_monthly` | 0.005 | -0.1 ... 0.15 |
| `consumer_goods_factor` | 0 | -0.15 ... 0.7 |
| `personal_value_factor` / `business_value_factor` | 0.05 / 0.025 | -0.5 ... 0.5 |
| `income_growth_factor` | 0.02 | -0.5 ... 0.3 |
| `production_factory_efficiency_gain_factor` | 0.035 | -0.5 ... 0.2 |

TFR-специфичные семейства ключей, которых нет в ваниле:
- `<идеология>_drift` (дрейф популярности партии за месяц, медианы 0.01-0.03): `fascist`, `authoritarian_democrat`, `social_liberal`, `conservative`, `social_democrat`, `communist`, `libertarian_socialist`, `totalitarian_socialist`, `nationalist`, `market_liberal`, `national_socialist`;
- `<идеология>_acceptance` (принятие идеологии режимом; значения -50 ... 50, встречаются у идей SOV с `social_democrat_acceptance = 25/45`);
- `drift_defence_factor` (защита от дрейфа: 0.25-0.5 у «прочных» духов), `party_popularity_stability_factor` (стабильность от популярности правящей партии: до 0.55), `dtg_threshold` (порог, растёт с уровнем «Общество» от 0.3 до 1.05; смысл [ПРОВЕРИТЬ]);
- `*_laws_cost_factor` и `*_minister_cost_factor` (цена смены законов и министров; от -0.5 до +0.35);
- `usual_oligarch_influence_monthly`, `oligarch_influence_monthly`, `red_directors_influence_monthly`, `peoples_entrepreneurs_influence_monthly` - внутренние шкалы России, нам не нужны;
- `disabled_ideas = 1` (SOV: блокирует слот идей в кризисных духах).

**Вид идеи (реф, 2095 идей).** Типовой дух: `allowed`, `traits = { ZZZ_blank_idea_trait }` (1660 из 1702 «country»-идей SOV; в оригинальной `TFR_ideas_UKR.txt` только 2 из примерно 146 - то есть для работы не обязателен, смысл (вероятно, косметика окна) [ПРОВЕРИТЬ]), `picture`, `removal_cost = -1` (1593), `allowed_civil_war` (1094; у нас везде `always = yes`), `modifier`, иногда `targeted_modifier` (66), `on_add`/`on_remove` (5/62), `visible`/`available` (285/171), `equipment_bonus`, `research_bonus`. Категории: `country` 1702, `hidden_ideas` 108 (скрытые бонусы ИИ вроде `SOV_russia_can_win`), `head_minister` 84, `economic_minister` 59, `interior_minister` 52, `foreign_minister` 38, `intelligence_minister` 27, `theorist_minister` 23.

---

## 10. События и интерфейс

- **Событие:** `country_event = { id = ... days/hours = N random_days = M }`, `news_event`, `hidden_effect`, `is_triggered_only = yes`, `immediate = { log = "[GetDateText]: [Root.GetName]: event X" }`.
- **Подсказки:** `custom_effect_tooltip = tooltip_white_line` (белая разделительная линия между блоками эффектов; у SOV ~185 раз); `custom_effect_tooltip = tooltip_event_choice_option_1/2/3`; `show_ideas_tooltip`, `unlock_decision_tooltip`, `unlock_decision_category_tooltip`, `event_option_tooltip`. `effect_tooltip`, `hidden_effect` — ванильные.
- **Игровые правила:** `has_game_rule = { rule = X option = Y }` (правила SOV: `SOV_ai_behavior`, `The_First_Union_Presidential_Election`, `The_Kazakhstan_Riots`, `The_LDPR_Path` и др.). Для UKR правил нет; завести свои можно в `common/game_rules/` [ПРОВЕРИТЬ, нужно ли].
- DLC: `has_dlc = "By Blood Alone"` и др.
- Регион/сеть: `meta_effect`, `array`, `is_in_array`, `random_list`, `random_select_amount`, `clear_global_event_target`, `save_global_event_target_as` — ванильные.

**Глобальные флаги TFR, на которые можно ветвить контент UKR (реф):**
- `SOV_cprf_won`, `SOV_medvedev_won`, `SOV_ldpr_won`, `SOV_srzp_won`, `SOV_dugin_russia_flag`, `SOV_wagner_russia_flag`, `SOV_navalny_russia_flag`, `SOV_eurasia_won` — какая Россия победила на выборах/в смуте.
- `SOV_first_nato_war_victory`, `nato_nato_won_nato_war`, `SOV_nato_war_begins_global`, `SOV_LDPR_victory_NATO1` — первая европейская война.
- `SOV_kiev_nuked`, `SOV_moscow_nuked`, `SOV_berlin_nuked`, `SOV_warsaw_nuked`, … — ядерные удары. `SOV_nuked_deployed` — ядерное оружие применено.
- `NOV_red_ukraine_flag`, `NOV_red_novorossiya_flag` — красный вариант Украины/Новороссии.

**Общие ключи-тултипы TFR, годные и для нас** (частота в референсах; тексты в локализации TFR, смысл по названию [ПРОВЕРИТЬ]; префиксы `SOV_`, `GER_`, `FRA_` - чужая механика, не брать):

| Ключ | Раз | Для чего |
|---|---|---|
| `tooltip_white_line` | 550 | белая разделительная линия между блоками эффектов |
| `tooltip_event_choice_option_1/2/3` | 21 / 21 / 13 | «на выбор: вариант 1/2/3» в награде фокуса, завершающегося событием с развилкой |
| `tooltip_event_allows_choice` | 4 | «событие позволит выбрать» |
| `which_has_the_following_effect` | - | связка с `event_option_tooltip = <событие>.<опция>`: показывает эффект опции события в тултипе |
| `change_economic_law_tooltip` / `change_security_law_tooltip` / `change_trade_law_tooltip` | 15 / 6 / 4 | «изменится закон» (в паре с `show_ideas_tooltip`) |
| `appoint_head_minister_tooltip`, `appoint_economic_minister_tooltip`, `appoint_interior_minister_tooltip`, `appoint_foreign_minister_tooltip`, `appoint_theorist_minister_tooltip`, `appoint_int_minister_tooltip` | 21 / 16 / 12 / 9 / 8 / 3 | «назначим министра» |
| `unlock_hog_minister_tooltip`, `unlock_eco_minister_tooltip`, `unlock_sec_minister_tooltip`, `unlock_for_minister_tooltip`, `unlock_int_minister_tooltip`, `unlock_theorist_minister_tooltip` | 12 / 16 / 11 / 11 / - / - | «открывается министр» |
| `focus_branch_unlock_tooltip` | 7 | «открывается ветка» |
| `after_idea_expires` | 10 | «после окончания действия духа» (к временной идее) |
| `needs_approval`, `if_they_accept` | 3 / 3 | события других стран |
| `unrestricted_diplomacy_tt` | 4 | снятие дипломатических ограничений |

У нас используются только `appoint_economic_minister_tooltip` (1 файл); остальные пока не применялись. Для сложных наград (много эффектов) стоит перенять `tooltip_white_line`.

**Внешние «крючки» на наши события** (реф: события и фокусы SOV, которые сами вызывают `ukraine.*`). Это точки, которые нельзя ломать и которые можно перехватывать:

| Событие | Кто вызывает | Когда |
|---|---|---|
| `ukraine.4` | `russia.43` | Украина выходит из Минского протокола (снимает идею `UKR_minsk_protocol`) |
| `ukraine.5` | миссия `NATO_intervention_timer` (решения SOV), `timeout_effect` вместе с `news.237` и `nato.22`; ту же связку повторяет наш таймер `UKR_special_military_operation_timer` | истёк срок до вмешательства НАТО (видна, пока не началась европейская война) |
| `ukraine.11` | дерево Медведева (`SOV_address_the_nation`), КПРФ (`SOV_prepare_to_march_west`), ЛДПР (`SOV_operation_southern_thunder`) | старт войны; наша копия активирует `UKR_special_military_operation_timer` и запускает `ukrainewar.1` |
| `ukraine.14` | решение SOV `SOV_raise_the_people` (`remove_effect`, при флаге `SOV_supported_ukrainian_communists`) | Россия подняла украинских коммунистов; параллельно `NOV` загружает отряды `NOV_soviet_uprising_1` |
| `ukraine.17` | дерево Дугина, фокус `SOV_the_eurasian_people_shall_bow_no_longer` | через 10-15 дней |
| `ukraine.8`, `ukraine.9`, `ukraine.15`, `ukraine.19` | дерево Дугина, фокус `SOV_march_on_the_west` | через 8, 10, 15, 12 дней |

`ukraine.13` (выборы 2024) в референсах **не вызывается нигде** - TD-17 остаётся открытым; значит вызов сидит в `on_actions` или в файлах других стран мода. `russia.76` («переворот Залужного») в референсе события определён, но не вызывается нигде: это `is_triggered_only`, условие в самом событии только `UKR = { NOT = { is_puppet_of = SOV } exists = yes }`, а шанс около 30% и сам вызов - в `on_actions`/скриптах вне референсов (TD-01).

---

## 11. Способности лидеров (`_reference/_referenceTFR_generic_leader_abilities.txt`)

Файл: `common/abilities/`; формат ванильный, TFR добавляет флаги и страновые варианты.

| Поле | Смысл |
|---|---|
| `type = army_leader` | для командиров |
| `allowed` | условия; `OWNER = { ... }` (владелец) и `FROM` (страна в `ai_will_do`) |
| `cost` | командная сила; `duration` — часы (168 = 7 дней); `cooldown` — часы; `cancelable` |
| `unit_modifiers` | эффекты, `tooltip = KEY` |
| `one_time_effect` | разовый эффект (`supply_units`) |
| `ai_will_do` | `factor = -1` + `modifier { add = 2 }` с проверками боёв (`num_units_offensive_combats`, `avg_offensive_combat_status`, `ai_random`) |

**TFR-ность:** способности привязаны к флагам стран: `super_force_attack_flag` (даёт дешёвую версию), `unlocked_gas_bombardment_tactic`, `GER_break_their_spirit_flag`, `PRC_tidal_wave_of_bodies`. Страновая копия `GER_force_attack` / `PRC_force_attack` включается так: `allowed = { GER = { has_country_flag = ... } }`. Строки с `#NVX#` закомментированы TFR. Для UKR можно сделать `UKR_*`-способность по тому же образцу (флаг или фокус как условие), иконка `GFX_ability_*`.

---

## 12. SOV-эффекты: не использовать для UKR

Эти эффекты и триггеры — внутренняя механика SOV или другой страны. Без наших копий для UKR их вызывать нельзя (ошибка в логе или молчаливый ноль):
- `SOV_add_election_approval_rating_*`, `SOV_add_party_*`, `SOV_add_*_influence`, `SOV_update_party_legitimacy`, `SOV_party_resource_var`, `SOV_change_*_power`, `SOV_increase_*` / `SOV_decrease_*` (партийно-политический блок).
- `SOV_has_*_opinion_less_than_or_equals`, `SOV_has_party_legitimacy_*`.
- `GER_add_eu_euroskepticism` / `GER_add_eu_visregard_sepratism` (+ `eu_euroskepticism_var_temp`, `eu_visregard_sepratism_var_temp`) — механика Германии/ЕС; для общих реакций ЕС лучше завести свой эффект.
- `PRC_add_BRM_influence`, `EU_membership_termination`, `upgrade_intelligence_agency = upgrade_collection`, `add_cic`, `enable_tech_cyber_units_warfare`, `terminator_ai_tech`, `add_to_tech_sharing_group = csto_research` — разовые эффекты TFR для отдельных стран; повторять их для UKR только после проверки.

Наши зависимости от TFR (влияние): переменные `Russian_Influence`, `European_Influence`, `American_Influence`, `Chinese_Influence`, `PDO_Influence`, `Sovereign_Influence` (доли 0..1; стартовые в `history/countries/UKR - Ukraine.txt`: 0.30 / 0.50 / 0 / 0 / 0 / 0.20). После `add_to_variable` на них мы ставим `clamp_variable ... min = 0 max = 1`.

---

## 13. Как SOV затрагивает Украину (для реакций, «трёх Россий» и блока 4)

### 13.1. Решения SOV с участием UKR (`decisions_SOV`)
Только названия, чтобы знать, что уже есть у России:
- Аннексия и подчинение: `SOV_subdue_ukraine`, `SOV_chain_ukraine_to_russia`, `SOV_integrate_ukraine_into_slavic_union`, `SOV_uss_integrate_ukr`, `SOV_core_ukr_states`, `SOV_ukraine_we_are_your_liberators`.
- Давление: `SOV_sabotage_ukr_industry`, `SOV_infiltrate_ukranian_territories`, `SOV_organize_partisans_in_ukraine`, `SOV_raid_ukraine`, `SOV_step_up_patrolling_ukraine`, `SOV_tatical_nuke_kiev`.
- Донбасс/Новороссия: `SOV_donbass_economic_reforms`, `SOV_donbass_new_red_army`, `SOV_rebuild_novorossiya`, `SOV_push_for_novorossiyan_unification`, `SOV_develop_ukrainian_army` (UKR как марионетка SOV).
- Контроль после аннексии: категория `SOV_ukrainian_insurgencies_category` (три ступени `SOV_resistance_spread1-3`, флаги `SOV_UKR_resistance_flag`, `SOV_UKR_resistance_spread22/33`, `SOV_pacified_ukraine`, `SOV_pacified_ukraine_ldpr`).
- Аннексия идёт через `annex_country = { target = UKR transfer_troops = yes }` (+ NOV, TRA, MOL). Эти механизмы - основа для блока 4; править их нельзя, но можно подстроиться флагами.

### 13.2. Как начинается война в каждой России (деревья фокусов, 04.10.2026)
Это ключ к «трём Россиям» (`DESIGN.md`, 9.1): у каждой России свой фокус-запуск, свой тип войны и свой набор побочных эффектов на Украину.

| Россия (id дерева) | Фокус-запуск (предшественник) | cost | Тип войны | Что делает с Украиной |
|---|---|---|---|---|
| **ЕР / Медведев** (`SOV_medvedev`) | `SOV_address_the_nation` (после `SOV_recognize_donbas`, а тот после `SOV_central_asian_military_operation` или `SOV_caucasus_military_operation`) | 5 | `topple_government` | идея `UKR_to_the_last`; снимает `UKR_mass_insurgency`; активирует миссию `UKR_special_military_operation_timer`; `ukraine.11`; боевые портреты Зеленского и Порошенко; `NOV` получает претензии и ядра на 8 областей и объявляет войну `take_core_state`; `news.190`; угроза +20 (`SOV_european_war_threat`); `will_lead_to_war_with` UKR, POL, LIT, LAT, EST |
| **КПРФ** (`SOV_communist`) | `SOV_operation_little_saturn` (после `SOV_prepare_to_march_west`, а тот после Тбилисской декларации, Ташкентского соглашения, советской Молдовы и защиты русских меньшинств) | 10 (подготовка 6.44) | `annex_everything` | то же; `ukraine.11` и снятие `UKR_mass_insurgency` стоят уже в `SOV_prepare_to_march_west` (до объявления войны); таймер и портреты - в `little_saturn` |
| **ЛДПР** (`SOV_ldpr_gaming`) | `SOV_operation_southern_thunder` (после `SOV_the_time_is_now`, а тот после `SOV_subdue_central_asia` и `SOV_bent_caucasus`) | 5 (подготовка 4) | `annex_everything` | то же, но **таймер СВО в самом фокусе не активируется** (его запустит `ukraine.11` из нашей копии); дальше `SOV_trample_over_kiev_LDPR` (Украине -0.15 поддержки войны, -0.1 стабильности, -5000 живой силы и дух на 125 дней, `load_oob "SOV_moa"`) |
| **Путин** (основное дерево `SOV`) | `SOV_declare_smo` | 30 | показан `annex_everything`, **но это ловушка** | тултип войны через `effect_tooltip`, а в `hidden_effect` вызывает `russia.484` - «anti cheat event»: -1000 политсилы, -0.9 стабильности и поддержки. Реальной войны не объявляет; образцом запуска войны не служит |
| **Дугин** (`SOV_dugin_tree`) | `SOV_march_on_the_west` (7.2) -> `SOV_grand_showdown` (2.2); предшественники - `SOV_march_on_caucasus`, `SOV_push_for_don_reunifaction` | 7.2 + 2.2 | `annex_everything` (UKR и FER) | `second_nato_war_flag`; события `ukraine.8/9/15/19` и `ukraine.17`; поздняя «вторая война НАТО» |
| **Вагнер** (`SOV_wagner_tree`) | `SOV_russian_revengeance` (после `SOV_prepare_for_the_march`) | 10 | `annex_everything` (UKR, FER, BLR) | `second_nato_war_flag` |
| **Навальный** (`SOV_navalny_*`) | `SOV_ultimatum_to_the_kuban` | 4 | - | наоборот: `UKR = { give_guarantee = FER }` |

Выводы для дизайна:
1. **Точка входа - `ukraine.11`.** Его вызывают только деревья Медведева, КПРФ и ЛДПР; наша копия активирует по нему таймер СВО (`UKR_special_military_operation_timer`) и запускает `ukrainewar.1` (тот стреляет и сам по `has_war_with = SOV`, поэтому настрой стартует при любом запуске). У Дугина и Вагнера война объявляется иначе (флаг `second_nato_war_flag`, это уже «вторая война НАТО» [ПРОВЕРИТЬ]) и `ukraine.11` не приходит: таймер СВО там не стартует. Если в игре нет таймера, первым делом смотреть, какая Россия начала войну.
2. **Украина в каждой России - последняя.** Перед запуском все ветки заставляют Россию сначала пройти Среднюю Азию и Кавказ (Медведев и ЛДПР), Грузию, Ташкент и Молдову (КПРФ), Кавказ и Донбасс (Дугин). Это то же правило, что и в `CLAUDE.md` («Россия сначала нападает на соседей, Украина - последняя»), и оно уже реализовано самим TFR: в нашем моде ничего менять не нужно, достаточно знать, что к моменту `ukraine.11` соседи уже воюют или захвачены.
3. **Сезонность.** Фокус Медведева планирует `russia.157` («Распутица»): динамический модификатор местности `SOV_terrain_raputista` на областях 196 (60 дней) и 221 (100 дней), глобальный флаг `SOV_rasputista`. Событие приходит через 10 дней, если война началась в марте-мае любого года 2023-2027, и через 270 дней (к следующей весне), если в июне-августе; в остальные месяцы не планируется. Наша копия решений Украины тоже вызывает `russia.157` (три места в `TFR_decisions_UKR.txt`).
4. `UKR_to_the_last` (идея-дух «до последнего») выдаётся всеми тремя настоящими запусками (Медведев, КПРФ, ЛДПР); как общий признак «война началась» удобнее `has_war_with = SOV`, он работает и для Дугина с Вагнером.
5. Идеи и флаги России, которые читает Украина: `UKR_mass_insurgency` (снимается при войне), `UKR_brotherhood_treaty_idea` (1-3, договор о братстве), `UKR_legacy_of_kiev_junta_idea` (наследие «киевской хунты», пропагандистский ярлык TFR), `UKR_russian_speaking_majority_region`, `UKR_collapsing_military` (после «переворота»).
6. Фокусы SOV после войны переписывают Украину: `SOV_new_age_ukraine` (Медведев; **если у руля Украины Бойко** - Россия делает её марионеткой и участником ОДКБ, правящая партия `conservative` с популярностью 0.43, выборы разрешены; при любом лидере снимает `UKR_legacy_of_kiev_junta_idea` и даёт Украине +100 политсилы, +0.025 стабильности, +0.1 по шкале «Общество»), `SOV_proclaim_uss` (`UKR_uss`), `SOV_the_slavic_union`, `SOV_three_slavic_sisters`, `SOV_the_new_union_treaty`, `SOV_spark_anti_occupation_resistance`. Это отправные точки для блока 4 («Дарт Вейдер», оккупация) и причина, по которой нельзя трогать лидерство Бойко в TFR (`CLAUDE.md`).

---

## 14. Типичные ошибки (чек-лист)

1. `set_temp_variable` с `income_var_temp` / `debt_var_temp` / `*_development_var_temp`, но без эффекта после него. Тихая ошибка.
2. Вызов эффекта без `= yes` или триггера без значения (триггер экономики читает `*_trigger_temp_var` **до** вызова).
3. `debttotal_temp` вместо `debt_var_temp`.
4. Суммы масштаба SOV (десятки млрд) для Украины.
5. SOV-эффекты в UKR-коде (раздел 12).
6. `change_economy_type_*` / `change_government_type_*` с именем, которого нет в TFR (раздел 4.4).
7. Меняли переменную динамического модификатора и не вызвали `force_update_dynamic_modifier = yes`.
8. Знак «бедности» (раздел 2): плюс = лучше.
9. Тире `—`, `–` и `…` в локализации запрещены (шрифт показывает «?»).
10. Скриптовые `.txt` — UTF-8 **без BOM** (с BOM не грузились идеи); `.yml` — **с BOM**.
11. Первый фокус кризисной ветки не дороже 3; 1 cost = 7 дней.
12. **Черты, подидеологии, здания, типы государства/экономики - только из `TFR_CATALOG.md`.** Неизвестное имя даст ошибку в `error.log`, а не поведение «по смыслу».
13. **Закон меняется `add_ideas = <закон>` / `swap_ideas`, а не флагом.** Игроку покажите `custom_effect_tooltip = change_*_law_tooltip` и `show_ideas_tooltip` (раздел 3). Законы развития (`*_development`) руками не меняются, только через шкалу.
14. **`war_mobilization` и `total_mobilization` недоступны при низкой поддержке войны** (0.5 и 0.8). Не обещайте игроку закон, который `available` не пропустит.
15. **Путать слоты `economy` (экономическая мобилизация) и `mobilization_laws` (призыв).** Они разные.
16. **`load_focus_tree` без `keep_completed`** теряет пройденные фокусы, которых нет в новом дереве. У нас везде `keep_completed = yes`.
17. **`SOV_declare_smo` как образец запуска войны.** Это ловушка (раздел 13.2); образец - `SOV_address_the_nation`.
18. **`add_ideas` без `traits = { ZZZ_blank_idea_trait }`.** В оригинале UKR его нет почти ни у одной идеи, так что отсутствие не ошибка; не добавлять «для порядка».

---

## 15. Рецепты (копировать и подставлять)

**Стройка в области** (реф: `FRA`, `GER`, `SOV`; номер области - числом или `random_owned_controlled_state`):
```
29 = {
	add_extra_state_shared_building_slots = 1
	add_building_construction = { type = industrial_complex level = 1 instant_build = yes }
}
```
Или: `random_owned_controlled_state = { ... то же ... }`. Типы зданий - `TFR_CATALOG.md`, раздел 7. Слоты (`add_extra_state_shared_building_slots`) добавляем до строительства, иначе нет места.

**Смена закона с понятным тултипом** (реф: `SOV`, `GER`):
```
custom_effect_tooltip = change_economic_law_tooltip
show_ideas_tooltip = partial_mobilization
hidden_effect = { add_ideas = partial_mobilization }
```

**Временный дух и его продление:**
```
add_timed_idea = { idea = UKR_xxx days = 350 }
custom_effect_tooltip = after_idea_expires          # необязательная подпись «после окончания»
```
```
modify_timed_idea = { idea = UKR_xxx days = 50 }    # позже: продлить уже действующий дух
```

**Фокус с событием посреди и по завершении** (реф: `SOV_communist`):
```
select_effect = { country_event = { id = ukraine_politics.XXX days = 10 } }
completion_reward = { country_event = { id = ukraine_politics.YYY } custom_effect_tooltip = which_has_the_following_effect event_option_tooltip = ukraine_politics.YYY.a }
```

**Альтернатива скрытому `available` для вариантов дерева** (реф: `GER`):
```
focus = {
	id = UKR_xxx
	bypass_if_unavailable = yes
	allow_branch = { has_country_flag = UKR_some_flag }
	...
}
```

**Война и предупреждение игроку** (реф: `SOV_medvedev`):
```
will_lead_to_war_with = TAG
completion_reward = {
	add_named_threat = { threat = 20 name = KEY }
	declare_war_on = { target = TAG type = topple_government }  # или annex_everything, take_core_state
	news_event = { id = news.190 }
}
```

**Расчёт долей в тексте события** - как в `ukraine_politics.205`: `[?UKR_r1_zel|0]` (число без имени переменной; в игре ещё не проверено, `HANDOFF.md`, п. 8).

---

## 16. Где что смотреть (быстрый указатель)

| Нужно | Смотреть |
|---|---|
| Какие законы есть и что дают | `TFR_CATALOG.md`, раздел 1; здесь раздел 3 |
| Подидеология лидера или партии | `TFR_CATALOG.md`, раздел 2; здесь 4.1 |
| Черта министра | `TFR_CATALOG.md`, раздел 3 |
| Допустимый ключ модификатора и его масштаб | `TFR_CATALOG.md`, раздел 4; здесь 9 |
| Какое здание можно строить | `TFR_CATALOG.md`, раздел 7; здесь 15 |
| Сколько давать за фокус | здесь 8.6 |
| Как запускается война | здесь 13.2 |
| Как TFR строит полное дерево страны | `_reference/_referenceTFR_national_focus_GER.txt`, `..._FRA.txt` |
| Как строится многопартийная система (Бундестаг, ЕС) | `GER`: эффекты `GER_add_*` (определений нет, видно только применение) |
| Как сделать окно решений с числами | `decision_categories_SOV` (`scripted_gui`) и наш `common/scripted_guis/UKR_war_mood_gui.txt` |
