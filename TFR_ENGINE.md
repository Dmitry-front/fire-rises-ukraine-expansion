# TFR_ENGINE.md - как устроен движок TFR под капотом

Справочник по реальным определениям, которые раньше были видны только по их применению: scripted effects, scripted triggers, on_actions, defines, правила игры, система отношений и влияния. Составлен 10.10.2026 по полному референсу (`TFR v1.2025.0b`). Помечено **(код)** - прочитано в определении; **[ПРОВЕРИТЬ]** - вывод по аналогии. Раздел по партиям и выборам - `TFR_POLITICS.md`; про Украину в TFR - `TFR_UKRAINE_HOOKS.md`; локализация и интерфейс - `TFR_INTERFACE.md`; практические рецепты - `TFR_CHEATSHEET.md`.

---

## 0. Масштаб и устройство файлов TFR

| Папка | Файлов | Строк | Что внутри |
|---|---|---|---|
| `common/scripted_effects` | 38 | 83 тыс. | 854 эффекта; крупнейшие: `TFR_scripted_effects_SOV` (23 тыс.), `USA` (9,6 тыс.), `00_..._ZZZ_generic` (7,8 тыс., ядро), `USB`, `FRA`, `GER`, `PRC` |
| `common/scripted_triggers` | 37 | 9,3 тыс. | общие триггеры (`00_..._ZZZ_generic`, 97 штук), страновые (USA 104, SRBM 74, GER 31, USB 30...) |
| `common/on_actions` | 35 | - | см. раздел 7 |
| `common/scripted_guis` | 32 | 7 тыс. | окна и кнопки интерфейса (`TFR_INTERFACE.md`) |
| `common/scripted_localisation` | 54 | 28 тыс. | динамические тексты |
| `common/dynamic_modifiers` | 27 | 9,3 тыс. | динамические модификаторы стран |
| `common/national_focus` | 60 | - | 58 деревьев фокусов |
| `events` | 125 | - | события |
| `localisation` | 1077 | - | 5 языков |

Правила именования (код):
- `00_` в начале - файл должен читаться первым (ядро и общие функции); `ZZZ` в имени - «общее для всех стран» (generic); `NVX_` - подключённый ИИ-мод; `LaR_` - La Résistance; `SF_` - спецназ.
- Файлы стран - `TFR_<вид>_<ТЕГ>.txt` (`TFR_scripted_effects_SOV.txt`). Файл с таким же путём и именем в нашем моде **целиком заменяет** оригинал.
- Эффект с одним именем в двух файлах: загружаются оба, действует, судя по порядку чтения, последний [ПРОВЕРИТЬ в игре]; в TFR так определены `decrease_corona` и `ROOT_inherit_current_scope_wars_effect` (дубли внутри `00_..._ZZZ_generic`). Свои эффекты называем с `UKR_`, чтобы ничего не перекрыть.

**Соглашения о переменных (код).**
- Постоянные переменные страны: `<имя>_var` (`income_var`, `debt_var`, `inflation_var`, `gdp_var`, `industrial_development_var`, `legit_var`).
- Параметры эффектов - **временные переменные** `<имя>_var_temp` (`income_var_temp`, `debt_var_temp`, `inflation_var_temp`, `industrial_development_var_temp`, `legit_var_temp`). Эффект читает `_var_temp` и пишет в `_var`. Поэтому «эффект = пара: сначала `set_temp_variable`, потом вызов».
- Чтение модификатора в переменную: `set_variable = { var = X value = modifier@имя }` (так TFR превращает модификаторы идей в числа).
- Глобальные переменные - префикс `global.`; массивы - `global.plague_affected_states` и т. п.

---

## 1. Экономика: настоящая модель (код)

Подтверждает и уточняет `TFR_CHEATSHEET.md`, раздел 1. Все суммы в «миллиардах» условных единиц.

### 1.1. Эффекты (`00_TFR_scripted_effects_ZZZ_generic.txt`)

| Эффект | Читает | Что делает |
|---|---|---|
| `add_income` | `income_var_temp` | `income_var += income_var_temp`, затем `check_gdp` |
| `add_debt` | `debt_var_temp` | `debt_var += debt_var_temp`, затем `check_gdp`, обновляет `debt_billion_var`, `debt_million_var`, `debt_trillion_var` |
| `add_inflation` | `inflation_var_temp` | `inflation_var += ...`, затем `update_economy` |
| `add_income_with_inflation` | `income_var_temp`, `inflation_var` | сумма умножается на `(1 + inflation_var)` (то есть растёт с инфляцией), потом как `add_income` |
| `add_debt_with_inflation` | `debt_var_temp`, `inflation_var` | то же для долга |
| `check_gdp` | - | защита от петель: отрицательный доход превращается в долг (`income_var < 0` → `debt_var_temp = -income_var`, `income_var = 0`), отрицательный долг - в доход; флаг `anti_loop_flag`; в конце `update_economy` |
| `update_economy` | `debt_var`, `gdp_total_var`, модификаторы `dtg_threshold`, `dtg_threshold_factor`, `inflation_var` | пересчитывает динамические переменные для `gdp_debt_dynamic` и `inflation_dynamic` (формулы ниже) |

**Знак `add_debt`.** `debt_var_temp > 0` - долг растёт (плохо), `< 0` - гасится. `add_income` - наоборот. Это согласуется с таблицей в шпаргалке, раздел 1.2.

### 1.2. Ежемесячный бюджет (`add_GDP`, 1075 строк, вызывается `on_monthly` из `00_TFR_on_actions_ZZZ_money.txt`)

Порядок расчёта (код):
1. Обнуляет `income_total_var`, `expenses_total_var`, `resourceincome/expenses`; запоминает `gdp_previous_var = gdp_var`, `gdp_var = 0`.
2. **Доходы.**
   - *Бизнес:* `business_value_var = (num_of_civilian_factories × modifier@business_value) × (1 + modifier@business_value_factor)`, плюс офисные парки (`building_level@office_park × business_value × 1.5` с тем же множителем); делится на 12 и добавляется к `gdp_var`; налог = `business_value_var × tax_business_rate_var`, где ставка = `modifier@tax_business_rate × (1 + modifier@tax_business_rate_factor)`.
   - *Население:* `personal_value_var = (max_manpower / 100000) × modifier@personal_value × (1 + modifier@personal_value_factor) / 12`; налог = `personal_value_var × tax_personal_rate_var`.
   - `total_tax_var = business_tax_var + personal_tax_var`.
   - *Ресурсы:* экспорт/импорт хрома, вольфрама, каучука, алюминия, нефти, стали (`resource_exported@X`, `resource_imported@X`) × 0.1.
3. **Расходы.** Содержание батальонов, самолётов, кораблей (`battalion_upkeep_factor`, `aircraft_upkeep_factor`, `ship_upkeep_factor`) → `military_spending_var` (+ заводы `military_factory_upkeep`, верфи `dockyard_upkeep`); социальные: `personal_expense_var = (max_manpower/100000) × modifier@personal_expense × (1+factor)/12`; импорт ресурсов; **обслуживание долга** `debt_payment_var = debt_var / 12 × interest_rate_var`, `interest_rate_var = modifier@interest_rate × (1 + modifier@interest_rate_factor)`; `modifier@misc_expense`; рост расходов `expense_growth_factor`.
4. **Итог.** `income_total_var = misc_income + налоги + ресурсы + рост(income_growth_factor)`, `money_change_var = income_total_var − expenses_total_var`. Если стоит флаг `auto_payment_flag` и `money_change_var > 0` и есть долг - прибыль идёт на погашение долга (`add_debt` с отрицательным значением); иначе `income_var += money_change_var`.
5. **Инфляция.** `inflation_monthly_var = modifier@inflation_monthly × (1 + modifier@inflation_monthly_factor)` → `add_inflation`.
6. **ВВП.** `gdp_var × 12` (за год); `gdp_total_var = gdp_var / (1 + inflation_var)` (реальный ВВП). Затем `check_gdp`.

**Отсюда практические выводы для наших фокусов:**
- Стоимость фокусов и решений - это влияние на `income_var` и `debt_var`, а не на «казну»: денег как предметов нет.
- Модификаторы идей, которые двигают экономику, - только перечисленные выше (`modifier_definitions/00_TFR_economic_modifiers_definition.txt`): `tax_business_rate`, `tax_personal_rate`, `business_value`, `personal_value`, `interest_rate`, `inflation_monthly`, `misc_income`, `misc_expense`, `income_growth_factor`, `expense_growth_factor`, `military_factory_upkeep`, `dockyard_upkeep`, `personal_expense`, `battalion_upkeep_factor`, `aircraft_upkeep_factor`, `ship_upkeep_factor`, `dtg_threshold`, `dtg_threshold_factor`, `low_stability_weekly`, шесть `*_development_monthly`. Каждый - с суффиксом `_factor`-близнеца для процентной надбавки.
- Нехватка денег не блокирует эффект, а превращается в долг (`check_gdp`).

### 1.3. Долг и инфляция → динамические модификаторы (код, `TFR_dynamic_modifiers_ZZZ_economic.txt`)

Страна получает два динамических модификатора (при создании: `new_country = yes`): `gdp_debt_dynamic` и `inflation_dynamic`. Их значения пересчитывает `update_economy`:
- Порог долга: `dtg_threshold_var = modifier@dtg_threshold × (1 + modifier@dtg_threshold_factor)`.
- `debt_dynamic_var = debt_var / gdp_total_var − dtg_threshold_var`.
  - **Если долг ниже порога** (`debt_dynamic < 0`): бонусы - `stability_factor = debt_dynamic × −0.134`, `production_factory_efficiency_gain_factor`, `production_factory_max_efficiency_factor`, `line_change_production_efficiency_factor` и `income_growth_factor` = `debt_dynamic × −0.067`, `industrial_development_monthly` и `academic_development_monthly` = `debt_dynamic × −0.0067` (значения положительные, потому что `debt_dynamic` отрицательна); после этого `debt_dynamic_var` обнуляется.
  - **Если долг выше порога**: `debt_dynamic_var` умножается на `−0.1` и идёт в `production_speed_buildings_factor`, `industrial_capacity_factory`, `industrial_capacity_dockyard` (штраф: стройка и мощность заводов), а бонусы выше равны нулю.
  - Независимо от ветки считаются по исходной разности: `research_speed_factor` и `fuel_gain_factor` = `разность × −0.025`, `military_development_monthly` = `разность × −0.0034` (бонус ниже порога, штраф выше).
- Инфляция > 0: `consumer_goods_factor = +inflation` и `stability_factor = inflation × −0.5`. Дефляция (< 0): `production_factory_max_efficiency_factor = inflation`, `production_speed_buildings_factor = inflation × 2`. Нулевая: ×1 и ×0.5.
- Стартовая экономика Украины (`on_startup`): тип `oligopolistic_capitalism`, инфляция `0.078`, долг `77` (у остальных 0.068 и 110).

### 1.4. Развитие (6 шкал; код)
- Шесть переменных `academic/farming/poverty/industrial/military/society_development_var` в диапазоне `[-1; 1]`. Ежемесячно `update_development` (из `00_TFR_on_actions_ZZZ_development.txt`) прибавляет `modifier@<имя>_development_monthly` и вызывает `check_<имя>_development`.
- Когда значение `>= 1`: показывается попап (`events/TFR_events_ZZZ_political.txt`: `generic.1-3` академическое, `4-6` сельское, `7-9` бедность, `10-12` промышленность, `13-15` армия, `16-18` общество; в каждой тройке «растёт», «падает», «максимум»), делается шаг вверх по лестнице идей (`increase_industry = yes`), переменная уменьшается на 1. Когда `<= -1` - шаг вниз и попап «падает».
- Лестница идей: `lower_<X>` → `low_<X>` → `medium_<X>` → `high_<X>` → `higher_<X>` → `highest_<X>` (для промышленности `lower_industry ... highest_industry`; аналогично `academic`, `farming`, `poverty`, `military`, `society`). `add_<X>_development` меняет переменную (параметр `<X>_development_var_temp`), сам шаг делает `check_*`.
- «Максимум» (`highest_*`): попап с выбором одноразового бонуса (идея вида `generic_construction_boost_idea`).
- Ручное изменение через законы возможно только с флагом `manual_development_change_allowed` (триггер `development`).

### 1.5. Законы - шаговые эффекты (код)
В `00_..._ZZZ_generic.txt` каждый закон имеет пару `increase_<имя>` / `decrease_<имя>`: `taxes`, `trade`, `welfare`, `safety`, `immigration`, `conscription`, `police`, `training`, `exemptions`, `supervision`, `education`, `prison`, `race`, `female`, `female_service`, `racial_integration`, `interest_rates` (плюс `enable/disable_interest_rates`, `increase_safety_max`), `economy_law` (`upgrade/decrease_economy_law`). Каждый - цепочка `if has_idea = X { swap_ideas X → следующая ступень }`, то есть закон - это идея-ступенька, а шаг - обмен идеи. Изменение без флага `manual_law_change_allowed` (триггер `non_changable_law`) в интерфейсе недоступно, но эффектом из скрипта работает всегда.

### 1.6. Тип экономики и тип государства - это идеи `ZZZ_*` (код)
- `change_economy_type_<имя>` = `remove_economy_types` (снимает все 26 идей `ZZZ_capitalist_economy`, `ZZZ_collective_capitalism`, `ZZZ_oligopolistic_capitalism`, `ZZZ_mixed_economy`, `ZZZ_worker_controlled_economy`... ) + `add_ideas = ZZZ_<тип>`. Тот же приём для государства: `change_government_type_<имя>` = `remove_gov_types` (34 идеи `ZZZ_presidential_republic`, `ZZZ_semi_presidential_system`, `ZZZ_military_dictatorship`, `ZZZ_provisional_government`...) + `add_ideas = ZZZ_<тип>`.
- Полный список имён: 25 типов экономики и 31 тип государства, которые TFR реально использует (`_tools/tfr_index/econ_types.txt`, `gov_types.txt`; аудит сверяет по ним).
- Проверка текущего типа: `has_idea = ZZZ_mixed_economy`, `has_idea = ZZZ_presidential_republic`.
- **Не путать с парой `get_current_government_type` / `restore_previous_government_type`:** она сохраняет и восстанавливает не тип государства, а **политическое состояние**: правящую идеологическую группу (`current_party_ideology_group`), популярности всех 11 идеологий (`get_current_popularities` / `set_popularities`), коалицию (`coalition_partners`), признак выборов и статус подчинения (колониальное правительство, интегрированная, оккупированная, автономная, номинальная марионетка и т. д.). Применяется в капитуляциях (`TFR_UKRAINE_HOOKS.md`, 6): победитель сохраняет своё правительство, пока на время держит страну в марионетках.

---

## 2. Утилиты общего назначения (код)

| Эффект | Что делает | Примечание |
|---|---|---|
| `new_country = yes` | для вновь созданной страны (марионетка, республика): добавляет `gdp_debt_dynamic` и `inflation_dynamic`, обнуляет `debt_var`, `gdp_var`, `inflation_var`, считает `add_GDP`, `update_development`, ставит `auto_payment_flag`, `auto_payment_var = 2`, `bank_var` (2 для игрока и банка, 1 для ИИ), снимает демилитаризованные зоны | нужен, если мы создаём страну сами |
| `focus_unlock = yes` | лишь `mark_focus_tree_layout_dirty = yes` под красивым тултипом `focus_unlock_tooltip` | «открыть фокус» в тексте награды |
| `add_legit = yes` | `legit_var += legit_var_temp`, зажим [-1; 1] (+ динамика США) | легитимность - переменная, не идея |
| `recruit_character_effect` | `set_nationality = ROOT`, снимает «генерала» при вербовке | использовать в области персонажа |
| `add_coring_cost`, `add_coring_time`, `add_coring_cost_reduction`, `use_coring_cost_reduction` | стоимость и время «окоренения» | |
| `annex_faction`, `annex_core_faction` | аннексия всей фракции | |
| `get_current_ideology_popularities` / `restore_ideology_popularities`, `get_current_ruling_party` / `restore_ruling_party` | сохранить/восстановить партии | для временной смены режима |
| `find_biggest_<идеология>` (11 штук), `find_best_democratic_ally_leader` | находят страну-лидера идеологии и кладут её в `event_target` | можно использовать в реакциях ЕС |
| `instantiate_collaboration_government` | коллаборационистское правительство | |
| `disband_units_fraction` | расформировать долю дивизий | |
| `add_campaign_slot`, `remove_campaign_slot`, `add_total_campaign_slot` | слоты кампаний влияния (SOV) | `has_campaign_slot` |
| `remove_all_national_spirits` | снять **все** идеи с чертой `ZZZ_blank_idea_trait` + десятки динамических модификаторов + флаги (345 строк) | вызывается при перерождении страны; Украину не затрагивает (`TFR_SYNC.md`, раздел 3) |
| `enable_wargoal_justification`, `enable_guarantee` и обратные | включают/отключают дипломатические действия по игровым правилам | |
| `increase_state_category` / `decrease_state_category` | шаг категории области (117 строк) | |
| `replace_civ_with_arms_factories` | конверсия фабрик | |
| `gain_random_agency_upgrade` | случайное улучшение разведки (602 строки) | |

**Коронавирус.** Пять ступеней идей `lower_covid_cases ... higher_covid_cases` (`available: date < 2023.1.1`), эффекты `increase_corona` / `decrease_corona`; ступени дают `consumer_goods_factor +0.1...+0.5`, `production_factory_max_efficiency_factor -0.025...-0.125`, `production_speed_buildings_factor -0.05...-0.25`, `industrial_capacity_factory/dockyard -0.05...-0.25`, `local_resources_factor -0.05...-0.25`, `MONTHLY_POPULATION -0.1...-0.5`. Триггеры `generic_has_corona` / `generic_not_has_corona`. Маски: `add_mask_supply`, `has_mask_supply_greater_than_or_equals`. **Украине TFR эту лестницу не выдаёт** (в `history/countries/UKR` и в событиях нет), так что наша COVID-цепочка (`ukraine.400-409`) сама по себе; если нужно, её можно привязать к стандартной лестнице (`increase_corona = yes`) и получить готовые экономические штрафы.

---

## 3. Отношения между странами (код)

- Механика - обычная HOI4. Проверка: `has_opinion = { target = X value > 30 }` (127 вхождений в TFR); сила изменения - `add_opinion_modifier = { target = X modifier = <имя> }` (для обеих сторон отдельно). Для `ai_chance` согласий и отказов по `DESIGN.md`, 9.3, лучше всего подходит `modifier = { factor = N  has_opinion = { target = UKR value > 40 } }`.
- Ряд модификаторов уже есть в TFR и годится как есть (значение / распад в день):
  - общие: `declaration_of_friendship` (+25), `military_aid` (+20, распад 0.25), `military_aid_denied` (-10), `military_cooperation` (+20), `peace_talks` (+10), `note_of_protest` (-10, 0.7), `harshly_worded_letter` (-20, 0.5), `diplomatic_support` (+20), `eased_border_tensions` (+20), `economic_mission` (+20), `recent_actions_very_positive/positive/negative` (+50/+25/-25, распад 1), `ideological_alliance` (+50), `ideological_enemy` (-40), `rival` (-100), `joint_infrastructure_projects` (+10), `loan_granted` (+15), `loan_denied` (-15), `rebel_support` (-75), `threat_to_our_independence` (-75);
  - НАТО: `NATO_commitment` (+40), `NATO_expansion` (+10), `reaffirmed_NATO` (+25), `took_part_in_NATO_drills` (+10), `didnt_take_part_in_NATO_drills` (-10);
  - ЕС: `european_commitment` (+25), `european_union_member` (+30), `european_economic_partner` (+20), `european_traitor` (-40), `visegrad_group` (+20);
  - Россия и Украина: `annexed_ukraine` (-30/-40, торговый вариант -75), `donbas_conflict` (-50), `ukranian_neo_nazism` (-30), `friendship_of_peoples` (+75), `recognition` (+75), `our_motherland` (+100), `donbas_republic` (+100), `economic_ties` (+50), `opinion_neo_nazism` (-75);
  - дипломатия: `guarantee` (+5/+25), `betrayed_guarantee` (-150), `at_war` (-150), `in_faction` (+50), `military_access` (+30), `protest_action(_light/_strong)` (-25/-10/-50), `condemn_aggression` (-50), `sanctions_relations` (-40), `took_stand_for_us` (+50), `our_liberators` (+50).
  Каталоги: `common/opinion_modifiers/*.txt` (21 файл: generic, nato, european_union, russia, germany, france, britain, israel...). Свои модификаторы создаём в нашем файле `common/opinion_modifiers/UKR_opinion_modifiers.txt` (наша `ukr_flight752_*` уже так сделана).
- Переопределение условий дипломатических действий: `scripted_triggers/diplomacy_scripted_triggers.txt` (`DIPLOMACY_GUARANTEE_ENABLE_TRIGGER`, `_LEND_LEASE_`, `_SEND_VOLUNTEERS_`, `_STAGE_COUP_`, `_BOOST_PARTY_POPULARITY_` и др.; ROOT - инициатор, FROM - получатель). Игровые правила `allow_*` включают или выключают соответствующие действия (раздел 5).

---

## 4. Влияние великих держав (код; большая часть - заготовка)

- На старте каждая страна получает шесть переменных в `history/countries/<ТЕГ>.txt`: `Russian_Influence`, `Chinese_Influence`, `American_Influence`, `European_Influence`, `PDO_Influence`, `Sovereign_Influence` (доли, в сумме 1). У UKR: 0.30 / 0.00 / 0.00 / 0.50 / 0.00 / 0.20 (наш файл; в оригинале TFR значения могут отличаться).
- В `modifier_definitions/00_TFR_influence_modifiers_definition.txt` объявлены модификаторы `russian_influence_modifier`, `chinese_...`, `american_...`, `european_...`, `pdo_...`, `sovereign_...`, а также `european_influence_cap`, `influence_drift_defence`. Читают их в основном идеи Франции и США; для остальных стран **механики-потребителя в скриптах нет**: никакой `on_action`, динамический модификатор или решение не использует `Russian_Influence`, кроме скриптовой локализации (`TFR_scripted_loc_influence`, подсказки «преобладает влияние...»).
- Эффекты `increase_<держава>_influence` / `decrease_<держава>_influence` читают временную переменную **`<Держава>_Influence_Temp`** (с заглавной буквы, например `European_Influence_Temp`), и в самом TFR **нигде не вызываются**. Нормализаторы суммы: `check_if_influence_sum_is_alright_if_too_high` и `..._too_low` (делят избыток/недостаток поровну между активными державами, сумма возвращается к 1).
- Для нас: влияние остаётся «декорацией» (переменные и тексты). Любой механический эффект нужно строить самим (динамический модификатор + наши события). Использовать ли `increase_*_influence` - решение автора; сейчас мы меняем переменную напрямую с `clamp_variable` (шпаргалка, раздел 12), что эквивалентно, но не нормализует сумму.

---

## 5. Правила игры (`common/game_rules/00_game_rules.txt`, 162 правила)

Доступны через `has_game_rule = { rule = X option = Y }`. Для нас важны:
- **Украина и соседи:** `UKR_election_24` (`UKR_election_UKR_24`, `UKR_election_RUS_24`), `BLR_20_election`, `The_MOL_2020_election`, `The_PLD_25_Election`, `SOV_ai_behavior`, `The_First_Union_Presidential_Election`, `The_CPRF_path`, `The_LDPR_Path`, `The_Dugin_or_Navalny`, `The_Dugin_Left_or_Right`, `The_Navalny_against_Navalny`, `The_Red_Navalny`, `The_Pre_Election_Congress_of_CPRF`, `The_Move_Against_the_Fifth_Column`.
- **Исход европейских войн:** `NATO_ai_behavior` (опция `NATO_VICTORY` даёт ЕС и НАТО бонус «20 дивизий» в `on_declare_war`), `Second_European_War_Outcome`, `The_NATO_Leader` (кто лидер блока), `GER_ai_behavior`, `FRA_ai_behavior`.
- **Дипломатические «замки»:** `allow_wargoals`, `allow_access`, `allow_release_nations`, `allow_licensing`, `allow_lend_lease`, `allow_volunteers`, `allow_guarantees`, `allow_revoke_guarantees`, `allow_leave_faction`, `allow_kick_faction`, `allow_take_over_faction`, `allow_coups`, `allow_party_boosting` - TFR ограничивает дипломатию правилами; их читают `diplomacy_scripted_triggers`.
- Остальное - выборы и пути других стран (Тайвань, Япония, Франция, Германия, Италия, Таиланд, Бразилия, Аргентина, Перу...).
- Для Украины своих правил добавлять не нужно; `required_dlc = "Waking the Tiger"` стоит у большинства правил TFR.

---

## 6. Defines (`common/defines/`)

- `TFR_defines_changes.lua`: **старт `2020.1.1.1`, конец `2050.1.1.1`**, `NPolitics.BASE_POLITICAL_POWER_INCREASE = 1.5`, `NFocus.MAX_SAVED_FOCUS_PROGRESS = 14`, `NMilitary.MAX_OUT_OF_SUPPLY_DAYS = 28`, `NDiplomacy.PEACE_SCORE_SCALE_FACTOR = 2.15`, `NDiplomacy.VOLUNTEERS_DIVISIONS_REQUIRED = 3`, `VOLUNTEERS_TRANSFER_SPEED = 7`, `NCountry.MIN_STABILITY = -1.0`, `MIN_WAR_SUPPORT = -1.0`, `BASE_STABILITY_PARTY_POPULARITY_FACTOR = 0.0` (стабильность напрямую от популярности партий отключена; она идёт через `party_popularity_stability_factor` идей). `NFocus.FOCUS_POINT_DAYS` не переопределён: 1 очко (cost) = 7 дней, как и ванильный `defines` (`CLAUDE.md`: cost 3-7).
- `TFR_00_optimization.lua`: оптимизация ИИ и мультиплеера (интервалы расчёта, лимиты шаблонов ИИ, графика); на наш код не влияет.
- Остальные два файла - камера и профиль карьеры.

---

## 7. `on_actions`: полный каталог (код)

Ключевые факты: **TFR не использует `on_daily`** (поэтому наш `on_daily` в `TFR_on_actions_UKR.txt` ни с чем не конфликтует), эффекты одноимённых on_actions из разных файлов выполняются все.

| Файл TFR | Ключи | Что делает |
|---|---|---|
| `00_TFR_on_actions_ZZZ_startup.txt` | `on_startup` | запускает все стартовые события и таймеры мира, типы экономики, инфляцию и долг, идеи типов государства (раздел 1) |
| `00_..._ZZZ_money.txt` | `on_startup`, `on_monthly` (`add_GDP`), `on_weekly` (подпитка стабильности при `has_stability < 0.5` через `low_stability_weekly`) | бюджет |
| `00_..._ZZZ_development.txt` | `on_startup` (`update_development`, `update_party_popularity`), `on_monthly` (`update_development`), `on_weekly` (`update_party_popularity`) | развитие и партии |
| `00_..._ZZZ_gamerules.txt` | `on_startup`, `on_declare_war`, `on_peace`, `on_annex` | применение игровых правил (бонусы ИИ-НАТО и пр.) |
| `00_..._ZZZ_coof.txt` | `on_weekly_ZZZ` | пандемия (глобальная) |
| `TFR_on_actions_ZZZ.txt` | `on_state_control_changed` (крупнейший: города войн), `on_army_leader_won_combat`, `on_army_leader_lost_combat`, `on_capitulation`, `on_leave_faction`, `on_declare_war` (суперсобытия 3EW Германия-Франция), `on_nuke_drop` | ход войн и ранения генералов |
| `TFR_on_actions_ZZZ_peace.txt` | `on_capitulation`, `on_declare_war`, `on_capitulation_immediate` | мирные договоры (27 тыс. строк) |
| `TFR_on_actions_ZZZ_civil_war.txt` | `on_state_control_changed` ×2, `on_annex` | гражданские войны (легитимность, замедление войны) |
| `TFR_on_actions_ZZZ_map_modes.txt` | `on_weekly`, `on_annex`, `on_subject_annexed`, `on_state_control_changed`, `on_peaceconference_ended`, `on_liberate`, `on_release_as_free`, `on_subject_free`, `on_release_as_puppet`, `on_war`, `on_peace`, `on_capitulation`, `on_uncapitulation` | обновляют особые режимы карты |
| `TFR_on_actions_ZZZ_elections.txt` | `on_new_term_election` (только `usa.90`) | выборы США; для остальных стран автоматических выборов в этом файле нет |
| `TFR_on_actions_{FRA,GER,JAP,PRC,USA,USB,USC,APA,ATW,CAC,KOR,LOS,NSM,PTF,SER,SOV,ITA,IRQ,BRS,AOF,CHI}.txt` | страновые `on_startup`, `on_state_control_changed`, `on_annex`, `on_new_term_election`, `on_government_change`, `on_declare_war` | `TFR_on_actions_SOV.txt` только `on_startup` (1,7 КБ) |
| `TFR_on_actions_ZZZ_{eu,nato}.txt`, `..._influence.txt`, `..._parliament_gui.txt` | `on_startup` (eu, nato) | инициализация ЕС и НАТО; influence и parliament_gui пусты |

**Предупреждение TFR из шапки `TFR_on_actions_ZZZ_peace.txt`:** файл «не трогать, часть аннексий работала и сломалась неизвестно почему». Наши крючки на капитуляцию делаем вне этого файла (`TFR_UKRAINE_HOOKS.md`, 6.4).

---

## 8. Скриптовые триггеры: самые полезные (код, `00_TFR_scripted_triggers_ZZZ_generic.txt`)

| Триггер | Смысл |
|---|---|
| `has_content_tag`, `has_skeleton_tag`, `is_relavent_tag` | уровень контента страны; «относится к существенным странам» |
| `has_totalitarian_government`, `has_democratic_form_of_government`, `has_ruling_party_popularity_less_than` | быстрые проверки режима |
| `head_minister_trigger` | допустимый премьер |
| `generic_has_corona`, `generic_not_has_corona` | лестница COVID |
| `has_<X>_development_greater_than_or_equals` (шесть) | проверки шкал развития |
| `has_income_greater_than_or_equals`, `has_debt_greater_than_or_equals` (+ `_with_inflation`) | условие стоимости в решениях (`custom_cost_trigger`) |
| `has_legit_greater_than_or_equals`, `has_mask_supply_greater_than_or_equals` | легитимность, маски |
| `has_campaign_slot`, `has_coalition_with_target`, `is_in_coalition`, `is_in_coalition_with_<идеология>` (11) | кампании и коалиции |
| `development`, `non_changable_law` | разрешено ли менять развитие/законы вручную (флаги) |
| `has_unsupported_economic_law`, `has_unsupported_manpower_law`, `has_disabled_ideas`, `is_completed_by_event`, `has_achievements_enabled` | служебные |
| `is_in_africa/asia/europe/the_americas/the_middle_east` (`continent_triggers.txt`), `is_EU_member`, `is_UNSC_member`, `is_neutral` | география и членство |
| `NATO_war_escalation_level_1`...`5` | ступень эскалации европейской войны (ЕС/НАТО) |
| `should_initiate_resistance` | включение сопротивления при оккупации |

Страновые наборы (`USA_*`, `GER_*`, `PRC_*`, `USB_*`, `APA_*`...) для UKR не нужны и не годятся (`TFR_CHEATSHEET.md`, 12).

---

## 9. Странности и ошибки TFR, о которых нужно знать

1. `ukraine.13` запланировано дважды (+1300 и +1551 дней); срабатывает ранний вызов (`TFR_UKRAINE_HOOKS.md`, 3).
2. Пустые условия `if = { limit = {...} }` без тела в `SOV_russian_victory`: следующие за ними аннексии выполняются безусловно (`TFR_UKRAINE_HOOKS.md`, 5.3).
3. В `add_debt` ряд событий SOV использует `debttotal_temp` вместо `debt_var_temp` (шпаргалка, раздел 1.2) - опечатка TFR; нам копировать нельзя.
4. Эффекты-дубли в `00_..._ZZZ_generic` (`decrease_corona` дважды, `ROOT_inherit_current_scope_wars_effect` дважды).
5. В `ukraine.13` тексты - заглушка `"Tupoe Govno"` (TFR), у нас заменена.
6. 213 файлов TFR пусты (`ai_strategy_plans`, `strategicregions`, `ai_equipment` и др.): это сознательные заглушки поверх ванильных файлов, не потеря.
7. `NATO_intervention_timer` доступна только `hidden_trigger = original_tag = NEP` в `available`, но реально работает по таймауту (миссия, `activation = always = no`), потому что активируется событием `nato.15`.
8. Условие `nato.12` в таймере войны с датами `(date <= 2024.09.01) И (date >= 2026.03.01)` невыполнимо (унаследовано).

---

## 10. Что дальше
- `TFR_POLITICS.md`: партии, коалиции, выборы, влияние на режим.
- `TFR_INTERFACE.md`: локализация, интерфейс, решения, события.
- Рецепты для новых механик - `TFR_CHEATSHEET.md`, раздел 15 (дополнен).
