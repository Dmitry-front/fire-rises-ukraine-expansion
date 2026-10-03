# TFR_CHEATSHEET.md — шпаргалка по коду TFR

Справочник для автора и Claude: что делают эффекты, триггеры и модификаторы именно TFR (не ванильные), с примерами и масштабами величин.
Составлен 03.10.2026 по `_reference/` (решения, события и фокусы SOV, способности лидеров), по оригинальным TFR-файлам в репозитории (`TFR_*_UKR*`, `common/scripted_triggers/*TFR*`, игровые тексты `ABT_MONEY_*` в локализации). Дополнять по ходу работы.

## 0. Как читать

**Источник каждого утверждения:**
- **(код)** — прочитано в оригинальном коде TFR, лежащем в репозитории. Самый надёжный источник.
- **(реф)** — выведено из того, как это использует SOV в `_reference/`. Надёжно по смыслу, но определения эффекта мы не видим.
- **(автор)** — сказано автором.
- **[ПРОВЕРИТЬ]** — гипотеза, нужна сверка с игрой или кодом TFR.

**Главное ограничение.** Определения TFR-эффектов (`add_income`, `add_society_development`, `change_economy_type_*` и т. д.) лежат в `common/scripted_effects/` самого TFR. В репозитории их **нет**, мы видим только их использование. В репозитории лежат лишь TFR-скриптовые **триггеры** (`common/scripted_triggers/`), и они раскрывают, как устроены переменные под эффектами.

**Шкалы:** `add_stability`, `add_war_support`, `add_popularity` — доли (0.05 = 5 %). `add_political_power` — очки (25–100). Деньги — **миллиарды** (см. раздел 1).

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

---

## 3. Законы-уровни (реф)

Эффекты, по контексту, сдвигают закон на **одну ступень** [ПРОВЕРИТЬ]. Закон хранится идеей со ступенчатым именем (`swap_ideas` меняет ступень вручную).

| Эффект | Идеи-ступени (примеры из реф) | Подсказка в событиях (TFR) |
|---|---|---|
| `increase_welfare` | `laws_welfare_post_soviet`, `high_welfare`, `higher_welfare` | |
| `increase_police` | `medium_police`, `high_police`, `highest_police` | |
| `increase_prison` | `medium_prison` | |
| `increase_safety` / `decrease_safety` | `high_safety`, `higher_safety` | |
| `increase_academic` | `medium_academic`, `high_academic`, `higher_academic`, `highest_academic` | |
| `decrease_poverty` / `decrease_society` | | `generic_poverty_level_decreased_tt`, `generic_society_level_decrease_tt` |
| `decrease_taxes` | | |
| `decrease_immigration` | `lower_immigration` | |
| (раса/нация) | `low_race` | |
| призыв | `low_`, `medium_`, `high_`, `higher_`, `highest_conscription` | |
| мобилизация | `early_mobilization`, `partial_mobilization`, `war_mobilization`, `total_mobilization`, `civilian_mobilization` | |

**Нюансы:** `increase_*` и `decrease_*` в реф встречаются по разу; направление `decrease_poverty` (меньше «уровень бедности» или хуже защита?) [ПРОВЕРИТЬ]. Для разовых событий безопаснее `swap_ideas` и `show_ideas_tooltip`, как делает SOV.

**Поддержка законов (код, триггеры `has_unsupported_*_law`):** закон «не поддержан», если военная поддержка ниже порога:

| Мобилизация | Порог `has_war_support <` | Призыв | Порог |
|---|---|---|---|
| `early_mobilization` | 0.15 | `low_conscription` | 0.1 |
| `partial_mobilization` | 0.25 | `medium_conscription` | 0.2 (не для тоталитарных) |
| `war_mobilization` | 0.5 | `high_conscription` | 0.6 (не для тоталитарных) |
| `total_mobilization` | 0.8 | `higher_conscription` | 0.7 (не для тоталитарных) |
| | | `highest_conscription` | 0.85 (не для тоталитарных) |

---

## 4. Политика

### 4.1. Идеологии

Партий **11**, они же допустимые значения `ideology =` в `add_popularity`, `set_party_name`, `ruling_party` (код: список в `is_in_coalition`):
`authoritarian_democrat`, `communist`, `conservative`, `fascist`, `libertarian_socialist`, `market_liberal`, `national_socialist`, `nationalist`, `social_democrat`, `social_liberal`, `totalitarian_socialist`.

**Классификация (код):**
- `has_totalitarian_government`: `totalitarian_socialist`, `communist`, `national_socialist`, `fascist`, `nationalist`.
- `has_democratic_form_of_government`: `social_democrat`, `social_liberal`, `market_liberal`, `conservative`, `authoritarian_democrat`.
- `libertarian_socialist` не входит ни туда, ни туда.

**Подидеологии лидера** (внутри `country_leader = { ideology = ... }`, `promote_character = { ideology = ... }`, реф): `marxism_leninism`, `market_socialism`, `left_nationalism`, `communist_populism`, `post_leftism`, `military_junta`, `hybrid_regime`, `oligarchist`, `ultra_conservatism`, `ethno_nationalism`, `right_populism`, `derzhavism`, `neo_stalinism`, `constitutionalist`, `absolute_monarchist`, `neonazism`, `centrist`, `progressivism`, `neoliberalism`, `social_patriotism`, `classical_fascism`, `social_democracy`, а также частные `sovereign_democracy*`, `putinism`. Полный перечень в TFR шире [ПРОВЕРИТЬ].

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

### 4.4. Тип государства и экономики (реф)

Встречаются в TFR (все `= yes`):
- **Государство:** `change_government_type_` + `provisional_government`, `socialist_republic`, `parliamentary_republic`, `semi_presidential_system`, `presidential_republic`, `presidential_dictatorship`, `military_dictatorship`, `communist_party_state`, `revolutionary_front`.
- **Экономика:** `change_economy_type_` + `socialist_market`, `state_capitalism`, `mixed_economy`, `left_corporatism`, `welfare_capitalism`, `planned_economy`, `oligopolistic_capitalism`, `military_controlled`.
- Запомнить/вернуть: `get_current_government_type = yes` + `restore_previous_government_type = yes`.

**Открыто:** `liberal_corporatism` и «кооперативная экономика» в референсах **нет** (TD-18, TD-21). Наша обёртка `UKR_set_liberal_corporatism_economy` с угаданным именем даст ошибку в `error.log`, если TFR называет иначе.

### 4.5. Баланс сил (BoP) (реф)

`add_power_balance_value = { id = X value = Y }`, `set_power_balance`, `remove_power_balance`, `is_power_balance_in_range`, `has_power_balance`, `power_balance_value`, `power_balance_weekly` (в модификаторах). Наш BoP: `common/bop/UKR_bop.txt`.

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
| `theorist_minister` | оборона | `army_chief_*` |
| `intelligence_minister` | разведка | `int_*` |

Идея-министр: `picture`, `allowed = { original_tag = UKR }`, `visible`, `traits = { ... }`. Замена: `swap_ideas = { remove_idea = A add_idea = B }` или `remove_ideas` + `add_ideas`.
**Пустой слот** (реф): идеи-заглушки `vacant_hog`, `vacant_eco`, `vacant_for`, `vacant_sec`, `vacant_int`, `vacant_theorist`; `add_ideas = vacant_X` после увольнения.
**Разблокировка министра** (реф): флаг + подсказки. Идея держится скрытой (`visible = { has_country_flag = ... }`), в опции события пишется `custom_effect_tooltip = unlock_hog_minister_tooltip` (также `unlock_eco_/sec_/for_/int_/theorist_minister_tooltip`, `appoint_head_minister_tooltip` и т. д.) + `show_ideas_tooltip = ИДЕЯ` + `set_country_flag`. Реальное `add_ideas` делают в `hidden_effect`.
**Увольнение** запрещено, если не разрешено: `set_can_be_fired_in_advisor_role = { character = X value = yes }`.
**Командиры:** `add_corps_commander_role`, `create_corps_commander`, `add_field_marshal_role`, `add_trait = { character = X slot = corps_commander trait = Y }`.

**Черты, встречающиеся в нашем коде** (определения лежат в TFR; новых имён не придумывать): `hog_silent_workhorse`, `hog_uncontested_prime_minister`, `hog_liberal_socialist`, `hog_backroom_backstabber`, `eco_economic_organizer`, `eco_keynesian_economy`, `eco_balanced_budget_economy`, `eco_industrialiser`, `eco_corrupt`, `for_free_trader`, `for_biased_intellectual`, `sec_populist_propagandist`, `sec_efficent_organizer` (в TFR с опечаткой), `int_encryptor`, `int_balanced_cryptographer`, `army_chief_reform_2`.
**Черты главы государства в реф** (префикс `hos_`): `hos_powerless_president`, `hos_peoples_president`, `hos_red_president`, `hos_initiative_apparatchik`, `hos_scandalous_reformer`, `hos_wounded_lion`, `hos_cowed_by_oligarchs`, `hos_aspiring_autocrat`. Флаг `head_of_gov_ui_enabled` включает интерфейс главы правительства [ПРОВЕРИТЬ].

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
	ai_will_do = { base = 5 }        # у решений base, у фокусов factor
}
```

- **Деньги в решении:** условие через `custom_cost_trigger` с `income_var` и текст `dx_more_than_<N>B` / `dx_more_than_<N>M`; сама оплата в `complete_effect` (`income_var_temp` −N + `add_income = yes`). Ключи `dx_more_than_*` в TFR есть для **своих** сумм (25B, 45B, 60B, 10B, 5B, 1B+25pp, 200M, 80M и т. д.). Для украинских сумм (0.5, 1.5, 3 млрд) нужно **свои** ключи `custom_cost_text` в нашей локализации [ПРОВЕРИТЬ, что чужие ключи не подойдут].
- Другие TFR-стоимости: `15cp_cost`, `30cp_cost` (командная сила), `15party_resource_cost` (SOV-ресурс), `5_stability_cost`, `5_war_support_cost`, `500inf_cost`. Ключи в TFR есть, у нас нужно проверять по месту.
- `ai_hint_pp_cost`, `priority`, `is_good = no`, `selectable_mission = no`, `days_mission_timeout`, `activate_mission`, `timeout_effect` — ванильные поля, но TFR использует их плотно (миссии-таймеры).
- `days_re_enable` при `fire_only_once = no` — повторный запуск.
- `highlight_states` + `on_map_mode = map_only` — подсветка регионов.
- **Кампании SOV:** `has_campaign_slot`, `add_campaign_slot`, `remove_campaign_slot` (слоты работают через `campaign_slot_var >= 1`, код); `*_international_campaign_slot`. Это общий механизм, но все примеры из SOV/НАТО-войны [ПРОВЕРИТЬ, нужен ли UKR].
- Отладка: `is_debug = yes` в `visible` прячет решение вне отладки.

---

## 8. Фокусы TFR (реф)

- `cost` 4–5 у SOV (1 cost = 7 дней). Наши правила — в `CLAUDE.md`.
- **`is_completed_by_event = yes`** в `available`: фокус нельзя взять руками, его завершает событие через `complete_national_focus = ID` (триггер в коде = `always = no` с подсказкой). Нужно для «фокусов-приманок» и скриптовых развязок.
- `allow_branch`, `relative_position_id`, `shared_focus`, `cancelable = no`.
- События-перестройки: `mark_focus_tree_layout_dirty = yes` (после смены флага, влияющего на видимость), `load_focus_tree = ID`, `unlock_national_focus`, `focus_unlock = yes` (TFR-эффект открытия контента фокусов у других стран; точная семантика [ПРОВЕРИТЬ]).
- Награда: `completion_reward`. Денежные: `add_debt_with_inflation` / `add_income_with_inflation`.

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

---

## 11. Способности лидеров (`_reference/Reference_TFR_generic_leader_abilities.txt`)

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

## 13. Как SOV затрагивает Украину (для реакций и блока 4)

Решения SOV с участием UKR (`_reference/Reference_TFR_decisions_SOV.txt`), только названия, чтобы знать, что уже есть у России:
- Аннексия и подчинение: `SOV_subdue_ukraine`, `SOV_chain_ukraine_to_russia`, `SOV_integrate_ukraine_into_slavic_union`, `SOV_uss_integrate_ukr`, `SOV_core_ukr_states`, `SOV_ukraine_we_are_your_liberators`.
- Давление: `SOV_sabotage_ukr_industry`, `SOV_infiltrate_ukranian_territories`, `SOV_organize_partisans_in_ukraine`, `SOV_raid_ukraine`, `SOV_step_up_patrolling_ukraine`, `SOV_tatical_nuke_kiev`.
- Донбасс/Новороссия: `SOV_donbass_economic_reforms`, `SOV_donbass_new_red_army`, `SOV_rebuild_novorossiya`, `SOV_push_for_novorossiyan_unification`, `SOV_develop_ukrainian_army` (UKR как марионетка SOV).
- Контроль после аннексии: категория `SOV_ukrainian_insurgencies_category` (три ступени `SOV_resistance_spread1-3`, флаги `SOV_UKR_resistance_flag`, `SOV_UKR_resistance_spread22/33`, `SOV_pacified_ukraine`, `SOV_pacified_ukraine_ldpr`).
- Аннексия идёт через `annex_country = { target = UKR transfer_troops = yes }` (+ NOV, TRA, MOL). Эти механизмы — основа для блока 4 (оккупация и подполье); править их нельзя, но можно подстроиться флагами.

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
