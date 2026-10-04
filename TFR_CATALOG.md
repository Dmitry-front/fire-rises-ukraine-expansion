# TFR_CATALOG.md - каталог кода TFR (генерируется)

Собрано `python3 _tools/build_catalog.py` из `_reference/*.txt`. **Не править руками** - при новых референсах перезапустить скрипт. Выводы, правила и ограничения - в `TFR_CHEATSHEET.md`; здесь только справочные таблицы: что именно существует в TFR.

Условные обозначения: **L** = уровень закона (1 - самый «высокий», больший номер - «ниже»); **def** = закон по умолчанию; **cost** = цена смены в политической силе (у законов развития цены нет, они зависят от шкалы развития); **[TAG]** = закон доступен только этой стране (по `visible`/`available`/`allowed`). Страновые законы других стран (SOV, GER, PRC, USB, FAF и т. д.) нам недоступны; смотрим на них как на образец.

## 1. Законы (идеи-законы)

### academic_development

Файл: `_reference00_TFR_laws_development.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_academic` | 1 |  |  |  |  |
| `highest_academic` | 1 |  |  |  | research_speed_factor=0.05 |
| `high_academic` | 2 |  |  |  | research_speed_factor=-0.05 |
| `medium_academic` (def) | 3 |  |  |  | research_speed_factor=-0.1 |
| `low_academic` | 4 |  |  |  | research_speed_factor=-0.15 |
| `lower_academic` | 5 |  |  |  | research_speed_factor=-0.2 |

### farming_development

Файл: `_reference00_TFR_laws_development.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_farming` | 1 |  |  |  |  |
| `highest_farming` | 1 |  |  |  | MONTHLY_POPULATION=0.2 local_resources_factor=0.1 |
| `high_farming` | 2 |  |  |  | MONTHLY_POPULATION=-0.2 local_resources_factor=-0.1 |
| `medium_farming` (def) | 3 |  |  |  | MONTHLY_POPULATION=-0.4 local_resources_factor=-0.2 |
| `low_farming` | 4 |  |  |  | MONTHLY_POPULATION=-0.6 local_resources_factor=-0.3 |
| `lower_farming` | 5 |  |  |  | MONTHLY_POPULATION=-0.8 local_resources_factor=-0.4 |

### poverty_development

Файл: `_reference00_TFR_laws_development.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_poverty` | 1 |  |  |  | personal_value=1 |
| `highest_poverty` | 1 |  |  |  | personal_value=1.2 |
| `high_poverty` | 2 |  |  |  | stability_factor=-0.05 personal_value=0.8 |
| `medium_poverty` (def) | 3 |  |  |  | stability_factor=-0.1 personal_value=0.6 |
| `low_poverty` | 4 |  |  |  | stability_factor=-0.15 personal_value=0.4 |
| `lower_poverty` | 5 |  |  |  | stability_factor=-0.2 personal_value=0.2 |

### industry_development

Файл: `_reference00_TFR_laws_development.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_industry` | 1 |  |  |  | production_speed_buildings_factor=0.05 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05 business_value=36 military_factory_upkeep=4.5 dockyard_upkeep=4.5 factory_energy_consumption=0.4 |
| `highest_industry` | 1 |  |  |  | production_speed_buildings_factor=0.15 industrial_capacity_factory=0.15 industrial_capacity_dockyard=0.15 business_value=42 military_factory_upkeep=5.25 dockyard_upkeep=5.25 factory_energy_consumption=0.5 |
| `high_industry` | 2 |  |  |  | business_value=30 military_factory_upkeep=3.75 dockyard_upkeep=3.75 factory_energy_consumption=0.3 |
| `medium_industry` (def) | 3 |  |  |  | production_speed_buildings_factor=-0.1 industrial_capacity_factory=-0.1 industrial_capacity_dockyard=-0.1 business_value=24 military_factory_upkeep=3 dockyard_upkeep=3 factory_energy_consumption=0.2 |
| `low_industry` | 4 |  |  |  | production_speed_buildings_factor=-0.2 industrial_capacity_factory=-0.2 industrial_capacity_dockyard=-0.2 business_value=18 military_factory_upkeep=2.25 dockyard_upkeep=2.25 factory_energy_consumption=0.1 |
| `lower_industry` | 5 |  |  |  | production_speed_buildings_factor=-0.25 industrial_capacity_factory=-0.25 industrial_capacity_dockyard=-0.25 business_value=12 military_factory_upkeep=1.5 dockyard_upkeep=1.5 |

### military_development

Файл: `_reference00_TFR_laws_development.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_military` | 1 |  |  |  | special_forces_cap=0.1 |
| `highest_military` | 1 |  |  |  | special_forces_cap=0.15 army_org_factor=0.05 army_defence_factor=0.05 army_attack_factor=0.05 battalion_upkeep_factor=0.05 aircraft_upkeep_factor=0.05 ship_upkeep_factor=0.05 |
| `high_military` | 2 |  |  |  | conscription_factor=0.05 training_time_army_factor=-0.05 army_org_factor=-0.05 army_defence_factor=-0.05 army_attack_factor=-0.05 battalion_upkeep_factor=-0.05 aircraft_upkeep_factor=-0.05 (+8) |
| `medium_military` (def) | 3 |  |  |  | conscription_factor=0.1 training_time_army_factor=-0.1 army_org_factor=-0.1 army_defence_factor=-0.1 army_attack_factor=-0.1 battalion_upkeep_factor=-0.1 aircraft_upkeep_factor=-0.1 (+7) |
| `low_military` | 4 |  |  |  | conscription_factor=0.15 training_time_army_factor=-0.15 army_org_factor=-0.15 army_defence_factor=-0.15 army_attack_factor=-0.15 battalion_upkeep_factor=-0.15 aircraft_upkeep_factor=-0.15 (+7) |
| `lower_military` | 5 |  |  |  | conscription_factor=0.2 training_time_army_factor=-0.2 army_org_factor=-0.2 army_defence_factor=-0.2 army_attack_factor=-0.2 battalion_upkeep_factor=-0.2 aircraft_upkeep_factor=-0.2 (+7) |

### society_development

Файл: `_reference00_TFR_laws_development.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_society` | 1 |  |  |  | dtg_threshold=0.9 |
| `highest_society` | 1 |  |  |  | dtg_threshold=1.05 |
| `high_society` (def) | 2 |  |  |  | head_minister_cost_factor=0.05 foreign_minister_cost_factor=0.05 economic_minister_cost_factor=0.05 interior_minister_cost_factor=0.05 intelligence_minister_cost_factor=0.05 theorist_minister_cost_factor=0.05 economy_cost_factor=0.05 (+4) |
| `medium_society` | 3 |  |  |  | head_minister_cost_factor=0.1 foreign_minister_cost_factor=0.1 economic_minister_cost_factor=0.1 interior_minister_cost_factor=0.1 intelligence_minister_cost_factor=0.1 theorist_minister_cost_factor=0.1 economy_cost_factor=0.1 (+4) |
| `low_society` | 4 |  |  |  | head_minister_cost_factor=0.15 foreign_minister_cost_factor=0.15 economic_minister_cost_factor=0.15 interior_minister_cost_factor=0.15 intelligence_minister_cost_factor=0.15 theorist_minister_cost_factor=0.15 economy_cost_factor=0.15 (+4) |
| `lower_society` | 5 |  |  |  | head_minister_cost_factor=0.2 foreign_minister_cost_factor=0.2 economic_minister_cost_factor=0.2 interior_minister_cost_factor=0.2 intelligence_minister_cost_factor=0.2 theorist_minister_cost_factor=0.2 economy_cost_factor=0.2 (+4) |
| `GER_gotterdammerung_society` | 6 |  | [GER] |  | economy_cost_factor=0.2 trade_laws_cost_factor=0.2 interest_rate_laws_cost_factor=0.2 tax_laws_cost_factor=0.2 dtg_threshold=0.3 army_core_defence_factor=0.25 war_support_factor=0.25 (+4) |
| `GER_gotterdammerung_society2` | 6 |  | [GER] |  | economy_cost_factor=0.2 trade_laws_cost_factor=0.2 interest_rate_laws_cost_factor=0.2 tax_laws_cost_factor=0.2 dtg_threshold=0.3 army_core_defence_factor=0.3 war_support_factor=0.25 (+4) |
| `GER_gotterdammerung_society3` | 6 |  | [GER] |  | economy_cost_factor=0.2 trade_laws_cost_factor=0.2 interest_rate_laws_cost_factor=0.2 tax_laws_cost_factor=0.2 dtg_threshold=0.3 army_core_defence_factor=0.35 war_support_factor=0.4 (+4) |

### economy

Файл: `_reference00_TFR_laws_economic.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `all_russian_consolidation` | 1 | 100 | [SOV] | has_war=yes; has_country_flag=SOV_med_consolidation_of_society; НЕ(has_global_flag=SOV_first_nato_war_victory) | business_value_factor=-0.15 stability_factor=-0.1 conscription_factor=0.05 consumer_goods_expected_value=-0.02 production_speed_arms_factory_factor=0.25 production_speed_industrial_complex_factor=0.15 production_speed_dockyard_factor=0.2 (+6) |
| `permanent_mobilization` | 1 | 100 | [ATW,GER,GMA,NSM,PLD,PRC,SOV] |  | business_value_factor=-0.15 conscription_factor=-0.2 consumer_goods_expected_value=0.1 production_speed_arms_factory_factor=0.3 production_speed_dockyard_factor=0.3 conversion_cost_civ_to_mil_factor=-0.3 max_fuel_factor=0.3 (+2) |
| `total_mobilization` | 2 | 100 |  | has_war=yes; НЕ(has_war_support<0.8) | business_value_factor=-0.1 conscription_factor=-0.1 consumer_goods_expected_value=0.15 production_speed_arms_factory_factor=0.2 production_speed_dockyard_factor=0.2 conversion_cost_civ_to_mil_factor=-0.2 max_fuel_factor=0.2 (+3) |
| `war_communism_of_21st_century` | 2 | 100 | [SOV] | has_war=yes; has_country_flag=SOV_war_communism_flag; НЕ(has_global_flag=SOV_first_nato_war_victory) | business_value_factor=-0.1 stability_factor=-0.25 conscription_factor=-0.15 production_speed_arms_factory_factor=0.25 conversion_cost_civ_to_mil_factor=-0.2 max_fuel_factor=0.3 mobilization_speed=0.4 (+1) |
| `all_russian_total_mobilization` | 2 | 100 | [SOV] | has_war=yes; has_country_flag=SOV_total_war_flag; НЕ(has_global_flag=SOV_first_nato_war_victory) | business_value_factor=-0.1 stability_factor=-0.25 conscription_factor=-0.15 consumer_goods_expected_value=0.02 production_speed_arms_factory_factor=0.25 conversion_cost_civ_to_mil_factor=-0.2 max_fuel_factor=0.3 (+3) |
| `war_mobilization` | 3 | 100 |  | НЕ(has_war_support<0.5) | business_value_factor=-0.05 consumer_goods_expected_value=0.2 production_speed_arms_factory_factor=0.1 production_speed_dockyard_factor=0.1 conversion_cost_civ_to_mil_factor=-0.1 max_fuel_factor=0.1 industrial_development_monthly=-0.005 (+1) |
| `partial_mobilization` | 4 | 100 |  | НЕ(has_war_support<0.25) | consumer_goods_expected_value=0.25 factory_energy_consumption=-0.05 |
| `early_mobilization` | 5 | 100 |  | НЕ(has_war_support<0.15) | business_value_factor=0.05 consumer_goods_expected_value=0.3 production_speed_arms_factory_factor=-0.1 production_speed_dockyard_factor=-0.1 conversion_cost_civ_to_mil_factor=0.1 max_fuel_factor=-0.1 industrial_development_monthly=0.002 (+2) |
| `business_as_usual_law` | 6 |  | [SOV] |  | business_value_factor=0.13 consumer_goods_expected_value=0.37 production_speed_arms_factory_factor=-0.17 production_speed_dockyard_factor=-0.16 conversion_cost_civ_to_mil_factor=0.15 max_fuel_factor=-0.14 low_stability_weekly=0.0025 (+1) |
| `common_prosperity_law_right_1` | 6 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.19 consumer_goods_expected_value=0.41 production_speed_arms_factory_factor=-0.45 production_speed_dockyard_factor=-0.45 conversion_cost_civ_to_mil_factor=0.5 production_speed_industrial_complex_factor=0.32 production_speed_infrastructure_factor=0.22 (+5) |
| `common_prosperity_law_right_2` | 6 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.2 consumer_goods_expected_value=0.42 production_speed_arms_factory_factor=-0.4 production_speed_dockyard_factor=-0.4 conversion_cost_civ_to_mil_factor=0.45 production_speed_industrial_complex_factor=0.34 production_speed_infrastructure_factor=0.24 (+5) |
| `common_prosperity_law_right_3` | 6 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.23 consumer_goods_expected_value=0.43 production_speed_arms_factory_factor=-0.35 production_speed_dockyard_factor=-0.35 conversion_cost_civ_to_mil_factor=0.35 production_speed_industrial_complex_factor=0.36 production_speed_infrastructure_factor=0.26 (+6) |
| `common_prosperity_law_right_4` | 6 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.25 consumer_goods_expected_value=0.44 production_speed_arms_factory_factor=-0.25 production_speed_dockyard_factor=-0.25 conversion_cost_civ_to_mil_factor=0.25 production_speed_industrial_complex_factor=0.38 production_speed_infrastructure_factor=0.28 (+6) |
| `common_prosperity_law_left_1` | 6 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.16 consumer_goods_expected_value=0.39 production_speed_arms_factory_factor=-0.5 production_speed_dockyard_factor=-0.5 conversion_cost_civ_to_mil_factor=0.55 production_speed_industrial_complex_factor=0.28 production_speed_infrastructure_factor=0.18 (+5) |
| `common_prosperity_law_left_2` | 6 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.14 consumer_goods_expected_value=0.38 production_speed_arms_factory_factor=-0.5 production_speed_dockyard_factor=-0.5 conversion_cost_civ_to_mil_factor=0.6 production_speed_industrial_complex_factor=0.26 production_speed_infrastructure_factor=0.16 (+5) |
| `common_prosperity_law_left_3` | 6 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.1 consumer_goods_expected_value=0.37 production_speed_arms_factory_factor=-0.65 production_speed_dockyard_factor=-0.65 conversion_cost_civ_to_mil_factor=0.65 production_speed_industrial_complex_factor=0.24 production_speed_infrastructure_factor=0.14 (+6) |
| `common_prosperity_law_left_4` | 6 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.05 consumer_goods_expected_value=0.36 production_speed_arms_factory_factor=-0.5 production_speed_dockyard_factor=-0.5 conversion_cost_civ_to_mil_factor=0.7 production_speed_industrial_complex_factor=0.22 production_speed_infrastructure_factor=0.12 (+6) |
| `common_prosperity_law_2` | 6 |  | [PRC] |  | business_value_factor=0.18 consumer_goods_expected_value=0.3 production_speed_arms_factory_factor=-0.4 production_speed_dockyard_factor=-0.4 conversion_cost_civ_to_mil_factor=0.25 production_speed_industrial_complex_factor=0.2 production_speed_infrastructure_factor=0.1 (+5) |
| `nationalist_consumerism_law` | 6 |  | [SOV] | has_completed_focus=SOV_improve_russian_made_products | business_value_factor=0.18 personal_expense_factor=-0.1 consumer_goods_expected_value=0.3 production_speed_arms_factory_factor=-0.4 conversion_cost_civ_to_mil_factor=0.25 production_speed_industrial_complex_factor=0.3 production_speed_infrastructure_factor=0.3 (+4) |
| `civilian_mobilization` | 6 | 100 |  |  | business_value_factor=0.1 consumer_goods_expected_value=0.35 production_speed_arms_factory_factor=-0.2 production_speed_dockyard_factor=-0.2 conversion_cost_civ_to_mil_factor=0.2 max_fuel_factor=-0.2 industrial_development_monthly=0.005 (+2) |
| `mass_consumerism` (def) | 7 |  |  |  | business_value_factor=0.15 consumer_goods_expected_value=0.4 production_speed_arms_factory_factor=-0.3 production_speed_dockyard_factor=-0.3 conversion_cost_civ_to_mil_factor=0.3 max_fuel_factor=-0.3 industrial_development_monthly=0.01 (+2) |
| `common_prosperity_law_1` | 7 |  | [PRC] |  | business_value_factor=0.18 consumer_goods_expected_value=0.35 production_speed_arms_factory_factor=-0.4 production_speed_dockyard_factor=-0.4 conversion_cost_civ_to_mil_factor=0.4 production_speed_industrial_complex_factor=0.2 production_speed_infrastructure_factor=0.1 (+5) |
| `common_prosperity_law` | 8 |  | [PRC] | tag=PRC; НЕ(has_idea=common_prosperity_law_1, has_idea=common_prosperity_law_2) | business_value_factor=0.18 consumer_goods_expected_value=0.4 production_speed_arms_factory_factor=-0.4 production_speed_dockyard_factor=-0.4 conversion_cost_civ_to_mil_factor=0.5 production_speed_industrial_complex_factor=0.3 production_speed_infrastructure_factor=0.2 (+5) |

### trade_laws

Файл: `_reference00_TFR_laws_economic.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_trade` | 1 | 100 |  |  | personal_value_factor=-0.2 min_export=0.8 industrial_capacity_factory=0.2 industrial_capacity_dockyard=0.2 production_speed_buildings_factor=0.2 research_speed_factor=0.1 civilian_intel_to_others=40 (+1) |
| `high_trade` (def) | 2 | 100 |  |  | personal_value_factor=-0.1 min_export=0.6 industrial_capacity_factory=0.15 industrial_capacity_dockyard=0.15 production_speed_buildings_factor=0.15 research_speed_factor=0.075 civilian_intel_to_others=30 (+1) |
| `medium_trade` | 3 | 100 |  |  | min_export=0.4 industrial_capacity_factory=0.1 industrial_capacity_dockyard=0.1 production_speed_buildings_factor=0.1 research_speed_factor=0.05 civilian_intel_to_others=20 navy_intel_to_others=10 |
| `ITA_made_in_italy` | 3 | 100 | [ITA] | tag=ITA | min_export=0.6 production_speed_buildings_factor=0.15 consumer_goods_expected_value=-0.05 personal_value_factor=-0.1 business_value_factor=0.2 research_speed_factor=0.125 civilian_intel_to_others=20 |
| `low_trade_autarky` | 4 | 100 | [ATW,SOV] |  | personal_value_factor=0.1 min_export=0.2 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05 production_speed_buildings_factor=-0.2 research_speed_factor=0.025 civilian_intel_to_others=10 (+2) |
| `low_trade` | 4 | 100 |  |  | personal_value_factor=0.1 min_export=0.2 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05 production_speed_buildings_factor=0.05 research_speed_factor=0.025 civilian_intel_to_others=10 (+1) |
| `lower_trade` | 5 | 100 |  | has_war=yes | personal_value_factor=0.2 min_export=0 |

### tax_laws

Файл: `_reference00_TFR_laws_economic.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_taxes` | 1 | 100 |  |  | tax_business_rate=0.3 tax_personal_rate=0.25 conversion_cost_mil_to_civ_factor=0.2 production_speed_industrial_complex_factor=-0.2 production_speed_office_park_factor=-0.2 fuel_gain_factor=-0.2 poverty_development_monthly=-0.01 |
| `high_taxes` | 2 | 100 |  |  | tax_business_rate=0.25 tax_personal_rate=0.2 conversion_cost_mil_to_civ_factor=0.1 production_speed_industrial_complex_factor=-0.1 production_speed_office_park_factor=-0.1 fuel_gain_factor=-0.1 poverty_development_monthly=-0.005 |
| `medium_taxes` (def) | 3 | 100 |  |  | tax_business_rate=0.2 tax_personal_rate=0.15 |
| `low_taxes` | 4 | 100 |  |  | tax_business_rate=0.15 tax_personal_rate=0.1 conversion_cost_mil_to_civ_factor=-0.1 production_speed_industrial_complex_factor=0.1 production_speed_office_park_factor=0.1 fuel_gain_factor=0.1 poverty_development_monthly=0.005 |
| `GER_gunther_taxes` | 4 | 100 | [GER] |  | tax_business_rate=0.05 tax_personal_rate=0.05 conversion_cost_mil_to_civ_factor=-0.3 production_speed_industrial_complex_factor=0.25 production_speed_office_park_factor=0.25 fuel_gain_factor=0.2 poverty_development_monthly=0.01 (+1) |
| `lower_taxes` | 5 | 100 |  |  | tax_business_rate=0.1 tax_personal_rate=0.05 conversion_cost_mil_to_civ_factor=-0.2 production_speed_industrial_complex_factor=0.2 production_speed_office_park_factor=0.2 fuel_gain_factor=0.2 poverty_development_monthly=0.01 |

### interest_rate_laws

Файл: `_reference00_TFR_laws_economic.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `highest_interest_rates` | 1 | 100 |  |  | interest_rate=0.2 inflation_monthly=-0.005 production_speed_buildings_factor=-0.2 poverty_development_monthly=-0.015 |
| `GER_interest_law` | 1 | 100 | [GER] |  | inflation_monthly=-0.004 production_speed_buildings_factor=0.05 business_value_factor=-0.05 |
| `higher_interest_rates` | 2 | 100 |  |  | interest_rate=0.125 inflation_monthly=-0.002 poverty_development_monthly=-0.01 production_speed_buildings_factor=-0.1 |
| `high_interest_rates` | 3 | 100 |  |  | interest_rate=0.1 inflation_monthly=-0.001 poverty_development_monthly=-0.005 production_speed_buildings_factor=-0.05 |
| `medium_interest_rates` | 4 | 100 |  |  | interest_rate=0.075 poverty_development_monthly=-0.0025 |
| `low_interest_rates` (def) | 5 | 100 |  |  | interest_rate=0.05 inflation_monthly=0.001 production_speed_buildings_factor=0.05 poverty_development_monthly=0.005 |
| `lower_interest_rates` | 6 | 100 |  |  | interest_rate=0.025 inflation_monthly=0.002 production_speed_buildings_factor=0.1 poverty_development_monthly=0.01 |
| `lowest_interest_rates` | 7 | 100 | [ATW,JAP,USC] |  | interest_rate=0 inflation_monthly=0.003 production_speed_buildings_factor=0.15 poverty_development_monthly=0.015 |

### welfare_laws

Файл: `_reference00_TFR_laws_economic.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `highest_welfare` | 1 | 100 | [GER] | has_completed_focus=GER_establish_minimum_pension | personal_expense=0.75 poverty_development_monthly=0.015 society_development_monthly=0.015 production_speed_infrastructure_factor=0.3 low_stability_weekly=0.003 |
| `higher_welfare` | 2 | 100 |  |  | personal_expense=0.6 production_speed_infrastructure_factor=0.2 society_development_monthly=0.01 poverty_development_monthly=0.01 low_stability_weekly=0.002 |
| `high_welfare` | 3 | 100 |  |  | personal_expense=0.45 production_speed_infrastructure_factor=0.1 society_development_monthly=0.005 poverty_development_monthly=0.005 low_stability_weekly=0.001 |
| `medium_welfare` (def) | 4 | 100 |  |  | stability_factor=0.015 poverty_development_monthly=0.001 society_development_monthly=0.001 personal_expense=0.3 |
| `low_welfare` | 5 | 100 |  |  | personal_expense=0.15 production_speed_infrastructure_factor=-0.1 society_development_monthly=-0.005 poverty_development_monthly=-0.005 |
| `GER_two_class_society_welfare` | 5 | 100 | [GER] |  | stability_factor=0.15 consumer_goods_factor=-0.1 personal_expense=-0.15 business_value_factor=0.25 low_stability_weekly=-0.005 production_speed_infrastructure_factor=-0.15 society_development_monthly=-0.015 (+2) |
| `laws_welfare_post_soviet` | 5 | 100 |  |  | stability_factor=0.025 consumer_goods_factor=0.05 personal_expense=0.2 income_growth_factor=-0.025 production_speed_infrastructure_factor=-0.05 |
| `welfare_nationalism_law` | 5 | 100 |  |  | stability_factor=0.025 consumer_goods_factor=0.025 personal_expense=0.2 personal_value_facotr=0.15 income_growth_factor=-0.05 production_factory_efficiency_gain_factor=0.03 mobilization_speed=0.025 (+1) |
| `lower_welfare` | 6 | 100 |  |  | personal_expense=0 production_speed_infrastructure_factor=-0.2 society_development_monthly=-0.01 poverty_development_monthly=-0.01 |

### safety_laws

Файл: `_reference00_TFR_laws_economic.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `GER_safety_law` | 1 | 100 | [GER] |  | production_factory_efficiency_gain_factor=0.05 production_speed_buildings_factor=0.025 industrial_capacity_factory=0.025 industrial_capacity_dockyard=0.025 industrial_development_monthly=-0.01 society_development_monthly=-0.01 personal_value_factor=-0.1 |
| `higher_safety` | 1 | 100 |  |  | stability_factor=0.075 production_factory_efficiency_gain_factor=0.1 production_speed_buildings_factor=-0.05 industrial_capacity_factory=-0.05 industrial_capacity_dockyard=-0.05 industrial_development_monthly=0.01 farming_development_monthly=0.01 |
| `PRC_revolutionary_rights` | 1 | 100 | [PRC] |  | personal_expense_factor=0.075 stability_factor=0.05 production_factory_efficiency_gain_factor=0.06 industrial_development_monthly=0.01 farming_development_monthly=0.01 |
| `high_safety` | 2 | 100 |  |  | stability_factor=0.05 production_factory_efficiency_gain_factor=0.05 production_speed_buildings_factor=-0.025 industrial_capacity_factory=-0.025 industrial_capacity_dockyard=-0.025 industrial_development_monthly=0.005 farming_development_monthly=0.005 |
| `medium_safety` (def) | 3 | 100 |  |  | stability_factor=0.025 industrial_development_monthly=0.005 farming_development_monthly=0.005 |
| `low_safety` | 4 | 100 |  |  | MONTHLY_POPULATION=-0.05 production_factory_efficiency_gain_factor=-0.05 production_speed_buildings_factor=0.025 industrial_capacity_factory=0.025 industrial_capacity_dockyard=0.025 industrial_development_monthly=-0.005 farming_development_monthly=-0.005 |
| `lower_safety` | 5 | 100 |  |  | MONTHLY_POPULATION=-0.1 production_factory_efficiency_gain_factor=-0.1 production_speed_buildings_factor=0.05 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05 industrial_development_monthly=-0.01 farming_development_monthly=-0.01 |

### mobilization_laws

Файл: `_reference00_TFR_laws_manpower.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `highest_conscription` | 1 | 100 |  | has_war=yes; enemies_strength_ratio>1 | conscription=0.16 industrial_capacity_factory=-0.4 industrial_capacity_dockyard=-0.4 production_speed_buildings_factor=-0.4 training_time_factor=0.5 |
| `PRC_entire_nation_in_arms` | 1 | 100 | [PRC] |  | army_attack_factor=-0.1 experience_loss_factor=0.1 conscription=0.15 industrial_capacity_factory=-0.3 industrial_capacity_dockyard=-0.3 production_speed_buildings_factor=-0.3 training_time_factor=-0.25 (+1) |
| `USB_duty_in_death_law` | 1 | 100 | [USB] | has_completed_focus=USB_duty_in_death | conscription=0.24 industrial_capacity_factory=-0.3 industrial_capacity_dockyard=-0.3 production_speed_buildings_factor=-0.3 training_time_factor=0.25 |
| `eurasia_conscription` | 2 | 100 | [SOV] | has_completed_focus=SOV_implement_a_conscription_program | conscription=0.08 industrial_capacity_factory=-0.15 industrial_capacity_dockyard=-0.15 production_speed_buildings_factor=-0.15 training_time_factor=-0.15 |
| `nibelungentreue_conscription` | 2 | 100 | [GER] | has_completed_focus=GER_national_service_tw | conscription=0.1 industrial_capacity_factory=-0.15 industrial_capacity_dockyard=-0.15 production_speed_buildings_factor=-0.15 training_time_factor=-0.15 |
| `higher_conscription` | 2 | 100 |  | has_war=yes; enemies_strength_ratio>0.75 | conscription=0.08 industrial_capacity_factory=-0.3 industrial_capacity_dockyard=-0.3 production_speed_buildings_factor=-0.3 training_time_factor=0.3 |
| `FAF_latin_conscription_law` | 2 | 100 | [FAF] | has_completed_focus=FAF_New_Imperial_Army | conscription=0.1 non_core_manpower=0.05 industrial_capacity_factory=-0.125 industrial_capacity_dockyard=-0.125 production_speed_buildings_factor=-0.125 |
| `lafayette_conscription` | 2 | 100 | [GER] | has_completed_focus=FAF_Control_the_Youth | conscription=0.12 industrial_capacity_factory=-0.2 industrial_capacity_dockyard=-0.2 production_speed_buildings_factor=-0.2 training_time_factor=-0.3 |
| `high_conscription` | 3 | 100 |  |  | conscription=0.04 industrial_capacity_factory=-0.1 industrial_capacity_dockyard=-0.1 production_speed_buildings_factor=-0.1 training_time_factor=0.2 |
| `volunteered_conscription` | 4 | 100 | [SOV] |  | conscription=0.0075 army_attack_factor=0.05 army_org_factor=0.05 army_defence_factor=0.05 |
| `medium_conscription` | 4 | 100 |  | НЕ(has_war_support<0.2) | conscription=0.02 training_time_factor=0.1 |
| `low_conscription` | 5 | 100 |  | НЕ(has_war_support<0.1) | conscription=0.01 |
| `GER_serve_the_republic` | 5 | 100 | [GER] | has_completed_focus=GER_militarize_reichsbanner_schwarz_rot_gold | conscription=0.035 offensive_war_stability_factor=0.1 defensive_war_stability_factor=0.15 |
| `PRC_militarized_society` | 5 | 100 | [PRC] | has_completed_focus=PRC_state_of_permanent_mobilization; tag=PRC | conscription=0.02 army_attack_factor=0.05 personal_value_factor=-0.2 war_stability_factor=0.1 military_factory_upkeep_factor=-0.2 battalion_upkeep_factor=-0.2 industrial_capacity_factory=-0.05 (+3) |
| `jihad_mobilization` | 5 | 100 |  |  | conscription=0.25 army_attack_factor=0.05 industrial_capacity_factory=-0.5 industrial_capacity_dockyard=-0.5 production_speed_buildings_factor=-0.5 training_time_factor=-0.15 stability_factor=-0.2 |
| `lower_conscription` (def) | 6 | 100 |  |  | conscription=0.005 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05 production_speed_buildings_factor=0.05 |
| `lowest_conscription` | 7 | 100 |  | НЕ(original_tag=SOV) | conscription=0.002 industrial_capacity_factory=0.1 industrial_capacity_dockyard=0.1 production_speed_buildings_factor=0.1 |

### female_service_laws

Файл: `_reference00_TFR_laws_manpower.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_female_service` | 1 | 100 |  |  | stability_factor=0.05 conscription_factor=0.1 army_org_factor=-0.05 female_random_army_leader_chance=0.5 |
| `USB_all_american_recruitment_female_service` | 1 | 100 | [USB] |  | stability_factor=0.075 conscription_factor=0.1 female_random_army_leader_chance=0.35 |
| `high_female_service` (def) | 2 | 100 |  |  | stability_factor=0.025 conscription_factor=0.05 female_random_army_leader_chance=0.3 |
| `medium_female_service` | 3 | 100 |  |  | army_org_factor=0.05 female_random_army_leader_chance=0.15 |
| `low_female_service` | 4 | 100 |  |  | conscription_factor=-0.05 army_org_factor=0.025 |
| `lower_female_service` | 5 | 100 |  |  | conscription_factor=-0.1 |

### supervision_laws

Файл: `_reference00_TFR_laws_manpower.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_supervision` | 1 | 100 |  |  | army_attack_factor=-0.1 war_support_factor=0.1 experience_gain_factor=0.2 battalion_upkeep_factor=0.1 military_development_monthly=0.01 |
| `USB_duty_in_death_supervision_law` | 1 | 100 | [USB] | has_completed_focus=USB_duty_in_death | army_attack_factor=-0.05 war_support_factor=0.1 experience_gain_factor=0.2 battalion_upkeep_factor=0.15 military_development_monthly=0.02 |
| `high_supervision` | 2 | 100 |  |  | army_attack_factor=-0.05 war_support_factor=0.05 experience_gain_factor=0.1 battalion_upkeep_factor=0.05 military_development_monthly=0.005 |
| `medium_supervision` (def) | 3 | 100 |  | НЕ(has_idea=higher_military, has_idea=highest_military) | army_attack_factor=-0.05 experience_gain_factor=0.05 |
| `PRC_systematic_dismantlement` | 4 | 100 | [PRC] |  | army_attack_factor=0.075 army_speed_factor=-0.125 experience_gain_factor=-0.2 military_development_monthly=-0.02 experience_loss_factor=0.1 ground_attack_factor=0.1 max_planning=0.25 |
| `PRC_systematic_dismantlement_mss` | 4 | 100 | [PRC] |  | war_support_factor=0.1 army_attack_factor=0.05 army_speed_factor=-0.125 experience_gain_factor=0.05 military_development_monthly=-0.02 experience_loss_factor=0.1 ground_attack_factor=0.1 (+2) |
| `low_supervision` | 4 | 100 |  | НЕ(has_idea=high_military, has_idea=higher_military, has_idea=highest_military) | army_attack_factor=0.05 war_support_factor=-0.05 experience_gain_factor=-0.1 military_development_monthly=-0.005 |
| `lower_supervision` | 5 | 100 |  | НЕ(has_idea=high_military, has_idea=higher_military, has_idea=highest_military) | army_attack_factor=0.1 war_support_factor=-0.1 experience_gain_factor=-0.2 military_development_monthly=-0.01 |
| `FAF_less_than_human_law` | 6 | 100 | [FAF] | tag=FAF | army_attack_factor=0.1 war_support_factor=0.1 military_development_monthly=-0.015 |

### training_laws

Файл: `_reference00_TFR_laws_manpower.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_training` | 1 | 100 |  |  | minimum_training_level=0.1 training_time_army_factor=0.2 army_org_factor=0.1 coordination_bonus=0.1 special_forces_cap=0.1 battalion_upkeep_factor=0.15 aircraft_upkeep_factor=0.15 (+2) |
| `highest_training` | 1 | 100 |  |  | minimum_training_level=0.15 training_time_army_factor=0.3 army_org_factor=0.15 coordination_bonus=0.15 special_forces_cap=0.2 battalion_upkeep_factor=0.3 aircraft_upkeep_factor=0.3 (+2) |
| `high_training` | 2 | 100 |  |  | minimum_training_level=0.05 training_time_army_factor=0.1 army_org_factor=0.05 coordination_bonus=0.05 special_forces_cap=0.05 battalion_upkeep_factor=0.1 aircraft_upkeep_factor=0.1 (+2) |
| `PRC_party_commands_the_guns` | 2 | 100 | [PRC] |  | conscription_factor=0.03 minimum_training_level=0.05 training_time_army_factor=0.1 army_org_factor=0.06 coordination_bonus=0.075 special_forces_cap=0.08 battalion_upkeep_factor=0.25 (+3) |
| `PRC_guns_command_the_party` | 2 | 100 | [PRC] |  | political_power_factor=-0.1 conscription_factor=0.03 minimum_training_level=0.15 training_time_army_factor=-0.1 army_org_factor=0.08 coordination_bonus=0.1 special_forces_cap=0.12 (+5) |
| `PRC_biologically_enhanced_warriors` | 2 | 100 | [PRC] |  | army_attack_factor=0.075 army_speed_factor=0.1 experience_gain_factor=0.1 military_development_monthly=-0.02 experience_loss_factor=0.1 ground_attack_factor=0.1 |
| `medium_training` (def) | 3 | 100 |  |  | conscription_factor=0.05 |
| `low_training` | 4 | 100 |  |  | conscription_factor=0.075 minimum_training_level=-0.05 training_time_army_factor=-0.1 army_org_factor=-0.05 coordination_bonus=-0.05 battalion_upkeep_factor=-0.05 aircraft_upkeep_factor=-0.05 (+2) |
| `well_regulated_militia` | 4 | 100 | [SOV] |  | conscription_factor=0.15 training_time_army_factor=-0.2 army_org_factor=-0.13 army_defence_factor=0.12 army_attack_factor=0.12 battalion_upkeep_factor=-0.05 aircraft_upkeep_factor=-0.05 (+5) |
| `lower_training` | 5 | 100 |  |  | conscription_factor=0.15 minimum_training_level=-0.1 training_time_army_factor=-0.2 army_org_factor=-0.1 coordination_bonus=-0.1 battalion_upkeep_factor=-0.1 aircraft_upkeep_factor=-0.1 (+2) |

### military_racial_integration_laws

Файл: `_reference00_TFR_laws_manpower.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_racial_integration` | 1 | 100 |  |  | conscription_factor=0.05 non_core_manpower=0.25 breakthrough_factor=0.025 field_officer_promotion_penalty=-0.2 military_leader_cost_factor=-0.2 promote_cost_factor=-0.2 |
| `USB_all_american_recruitment_racial_integration` | 1 | 100 | [USB] |  | conscription_factor=0.3 non_core_manpower=0.3 breakthrough_factor=0.025 field_officer_promotion_penalty=-0.2 military_leader_cost_factor=-0.2 promote_cost_factor=-0.2 |
| `high_racial_integration` (def) | 2 | 100 |  |  | conscription_factor=0.025 non_core_manpower=0.1 army_org_factor=0.025 breakthrough_factor=0.025 |
| `FAF_latin_military_integration_law` (def) | 2 | 100 | [FAF] |  | conscription_factor=0.05 non_core_manpower=0.15 weekly_manpower=300 army_org_factor=0.05 breakthrough_factor=0.05 war_support_factor=0.1 |
| `FRA_foreign_legion_integration` (def) | 2 | 100 | [FAF,FRA] |  | conscription_factor=0.05 non_core_manpower=0.2 weekly_manpower=250 army_org_factor=0.03 breakthrough_factor=0.03 war_support_factor=0.05 |
| `medium_racial_integration` | 3 | 100 |  |  | non_core_manpower=-0.05 army_org_factor=0.05 breakthrough_factor=0.05 |
| `low_racial_integration` | 4 | 100 |  |  | conscription_factor=-0.025 non_core_manpower=-0.075 army_org_factor=0.025 |
| `lower_racial_integration` | 5 | 100 |  |  | conscription_factor=-0.05 non_core_manpower=-0.1 |

### draft_exemption_laws

Файл: `_reference00_TFR_laws_manpower.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `general_exemptions` | 1 | 100 |  |  | conscription_factor=-0.25 war_support_factor=0.05 research_speed_factor=0.05 political_power_gain=0.1 farming_development_monthly=0.002 society_development_monthly=0.002 academic_development_monthly=0.002 |
| `education_exemptions` | 2 | 100 |  |  | conscription_factor=-0.1 research_speed_factor=0.05 academic_development_monthly=0.005 |
| `civil_service_exemptions` | 2 | 100 |  |  | conscription_factor=-0.1 political_power_gain=0.1 farming_development_monthly=0.005 |
| `religious_exemptions` | 2 | 100 |  |  | conscription_factor=-0.1 war_support_factor=0.05 society_development_monthly=0.005 |
| `no_draft_exemptions` (def) | 3 | 100 |  |  | war_support_factor=-0.05 farming_development_monthly=-0.002 society_development_monthly=-0.002 academic_development_monthly=-0.002 |

### immigration_laws

Файл: `_reference00_TFR_laws_social.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_immigration` | 1 | 100 |  |  | MONTHLY_POPULATION=1 political_power_gain=-0.15 min_export=0.05 |
| `USB_controlled_emigration` | 1 | 100 | [USB] |  | consumer_goods_factor=0.02 monthly_population=1.5 political_power_gain=-0.05 |
| `high_immigration` | 2 | 100 |  |  | MONTHLY_POPULATION=0.5 political_power_gain=-0.1 min_export=0.025 |
| `medium_immigration` (def) | 3 | 100 |  |  | MONTHLY_POPULATION=0.25 political_power_gain=-0.05 |
| `low_immigration` | 4 | 100 |  |  | MONTHLY_POPULATION=0.1 min_export=-0.025 |
| `lower_immigration` | 5 | 100 |  |  | political_power_gain=0.1 min_export=-0.05 |
| `FAF_involuntary_repatriation_law` | 6 | 100 | [FAF] |  | political_power_gain=0.15 MONTHLY_POPULATION=-0.1 industrial_capacity_factory=-0.075 industrial_capacity_dockyard=-0.075 |

### education_laws

Файл: `_reference00_TFR_laws_social.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_education` | 1 | 100 |  |  | personal_expense=0.2 stability_factor=0.1 research_speed_factor=0.1 academic_development_monthly=0.015 |
| `PRC_redirected_education_law` | 1 | 100 | [PRC] |  | experience_gain_factor=0.2 experience_gain_army_factor=0.2 political_power_factor=0.1 army_attack_factor=0.05 army_defence_factor=0.05 personal_expense_factor=-0.2 stability_factor=-0.075 (+2) |
| `high_education` | 2 | 100 |  |  | personal_expense=0.15 stability_factor=0.05 research_speed_factor=0.05 academic_development_monthly=0.01 |
| `medium_education` (def) | 3 | 100 |  |  | personal_expense=0.1 academic_development_monthly=0.005 |
| `low_education` | 4 | 100 |  |  | personal_expense=0.05 stability_factor=-0.05 research_speed_factor=-0.05 |
| `free_school_education` | 5 | 100 |  |  | stability_factor=-0.1 research_speed_factor=-0.2 libertarian_socialist_drift=0.02 academic_development_monthly=0.01 |
| `lower_education` | 5 | 100 |  |  | stability_factor=-0.1 research_speed_factor=-0.1 academic_development_monthly=-0.01 |
| `GER_consumerist_education_law` | 5 | 100 | [GER] |  | research_speed_factor=-0.15 political_power_gain=0.2 drift_defence_factor=0.25 business_value_factor=0.2 academic_development_monthly=-0.025 society_development_monthly=-0.025 |
| `GER_transhumanist_education_law` | 5 | 100 | [GER] |  | political_power_gain=-0.15 expense_growth_factor=0.25 monthly_population=-0.5 dtg_threshold_factor=0.25 research_speed_factor=0.1 academic_development_monthly=0.03 resistance_growth_on_our_occupied_states=-0.15 (+1) |
| `USB_department_of_information_education_law` | 5 | 100 | [USB] |  | research_speed_factor=0.1 academic_development_monthly=0.025 resistance_growth_on_our_occupied_states=-0.1 compliance_growth_on_our_occupied_states=0.1 nationalist_drift=0.03 fascist_drift=0.03 |
| `USB_NSS_education_law` | 5 | 100 | [USB] |  | political_power_gain=0.1 research_speed_factor=-0.05 academic_development_monthly=-0.02 resistance_growth_on_our_occupied_states=0.15 compliance_growth_on_our_occupied_states=-0.15 |
| `privatized_education` | 5 | 25 |  |  | research_speed_factor=0.05 academic_development_monthly=0.01 poverty_development_monthly=-0.005 |

### race_laws

Файл: `_reference00_TFR_laws_social.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_race` | 1 | 100 |  |  | political_power_gain=-0.15 stability_factor=-0.05 non_core_manpower=0.1 society_development_monthly=0.005 |
| `high_race` | 2 | 100 |  |  | political_power_gain=-0.1 stability_factor=-0.025 non_core_manpower=0.05 society_development_monthly=0.002 |
| `medium_race` (def) | 3 | 100 |  |  | non_core_manpower=0.02 |
| `low_race` | 4 | 100 |  |  | political_power_gain=0.1 non_core_manpower=-0.02 society_development_monthly=-0.002 |
| `PRC_chinese_nation_policy` | 4 | 100 | [PRC] |  | stability_factor=0.08 political_power_gain=0.05 non_core_manpower=-0.5 society_development_monthly=0.003 |
| `ultranational_liberalism` | 4 | 100 |  |  | political_power_gain=0.3 non_core_manpower=-0.05 conservative_drift=0.01 market_liberal_drift=0.01 authoritarian_democrat_drift=0.01 |
| `FAF_NMD_racial_law` | 5 | 100 | [FAF] |  | low_stability_weekly=0.005 political_power_gain=0.25 non_core_manpower=-0.1 |
| `lower_race` | 5 | 100 |  |  | political_power_gain=0.2 non_core_manpower=-0.04 society_development_monthly=-0.005 |

### female_laws

Файл: `_reference00_TFR_laws_social.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_female` | 1 | 100 |  |  | MONTHLY_POPULATION=-0.25 stability_factor=-0.075 industrial_capacity_factory=0.15 industrial_capacity_dockyard=0.15 society_development_monthly=-0.005 |
| `high_female` | 2 | 100 |  |  | MONTHLY_POPULATION=-0.15 stability_factor=-0.05 industrial_capacity_factory=0.1 industrial_capacity_dockyard=0.1 society_development_monthly=0.002 |
| `medium_female` (def) | 3 | 100 |  |  | MONTHLY_POPULATION=-0.05 stability_factor=-0.025 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05 society_development_monthly=0.005 |
| `low_female` | 4 | 100 |  |  | MONTHLY_POPULATION=0.05 society_development_monthly=0.002 |
| `lower_female` | 5 | 100 |  |  | MONTHLY_POPULATION=0.15 stability_factor=0.025 industrial_capacity_factory=-0.05 industrial_capacity_dockyard=-0.05 society_development_monthly=-0.005 |

### prison_laws

Файл: `_reference00_TFR_laws_social.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `higher_prison` | 1 | 100 |  |  | stability_factor=0.05 society_development_monthly=0.01 |
| `high_prison` | 2 | 100 |  |  | industry_free_repair_factor=0.1 society_development_monthly=0.005 stability_factor=0.025 |
| `medium_prison` (def) | 3 | 100 |  |  | industry_free_repair_factor=0.25 |
| `low_prison` | 4 | 100 |  |  | industry_free_repair_factor=0.5 production_speed_buildings_factor=0.05 stability_factor=-0.025 research_speed_factor=-0.025 |
| `USB_indiscriminate_violence_law` | 5 | 100 | [USB] |  | industry_free_repair_factor=0.75 production_speed_buildings_factor=0.1 stability_factor=-0.1 resistance_growth=-0.05 |
| `lower_prison` | 5 | 100 |  |  | industry_free_repair_factor=1 production_speed_buildings_factor=0.1 stability_factor=-0.05 research_speed_factor=-0.05 |

### police_laws

Файл: `_reference00_TFR_laws_social.txt`.

| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |
|---|---|---|---|---|---|
| `highest_police` | 1 | 100 |  |  | political_power_factor=-0.075 stability_factor=0.075 personal_expense=0.3 resistance_growth=-0.3 resistance_decay=0.3 compliance_growth=0.3 society_development_monthly=-0.015 |
| `GER_gunther_social_media_dominance` | 1 | 100 | [GER] |  | political_power_factor=0.05 stability_factor=0.05 personal_expense=0.05 resistance_growth=-0.1 resistance_decay=0.3 compliance_growth=0.3 society_development_monthly=0.02 (+1) |
| `SOV_rosgvardia_supervision_law` | 1 | 100 | [SOV] | has_country_flag=SOV_rosgvardia_law_enabled_flag | stability_factor=0.1 personal_expense=0.15 resistance_growth=-0.25 war_support_factor=0.05 compliance_growth=0.3 army_intel_to_others=-0.5 airforce_intel_to_others=-0.5 (+3) |
| `SOV_new_oprichnina_law` | 1 | 100 | [SOV] | has_country_flag=SOV_new_oprichnina_enabled_flag | stability_factor=-0.25 personal_expense=0.05 resistance_growth=-0.3 war_support_factor=0.1 business_value_factor=-0.1 compliance_growth=0.35 research_speed_factor=-0.07 (+7) |
| `SOV_sovereign_internet_law` | 1 | 100 | [SOV] | has_country_flag=SOV_sovereign_internet_enabled_flag | personal_expense=0.25 resistance_growth=-0.25 stability_factor=0.1 war_support_factor=0.05 compliance_growth=0.25 army_intel_to_others=-1.5 airforce_intel_to_others=-1.5 (+3) |
| `GER_totalitarian_party_state_law` | 1 | 100 | [GER] | has_country_flag=GER_neo_reich_flag | personal_expense=0.15 resistance_growth=-0.3 stability_factor=0.1 war_support_factor=0.1 compliance_growth=0.3 resistance_decay=0.1 conscription_factor=-0.1 (+6) |
| `GER_national_socialist_state_law` | 1 | 100 | [GER] | has_country_flag=GER_total_subjugation_of_state_flag | personal_expense=0.25 resistance_growth=-0.4 stability_factor=0.1 war_support_factor=0.15 compliance_growth=0.1 resistance_decay=0.1 conscription_factor=-0.1 (+6) |
| `PRC_chinese_surveillance_system` | 1 | 100 | [PRC] |  | personal_expense=0.2 resistance_growth=-0.25 stability_factor=0.1 war_support_factor=0.05 compliance_growth=0.25 army_intel_to_others=-35 airforce_intel_to_others=-35 (+4) |
| `USB_NSS_law` | 1 | 100 | [USB] |  | political_power_factor=0.05 stability_factor=0.1 personal_expense=0.4 resistance_growth=-0.35 resistance_decay=0.35 compliance_growth=0.35 society_development_monthly=-0.025 |
| `higher_police` | 2 | 100 |  |  | political_power_factor=-0.05 stability_factor=0.05 personal_expense=0.25 resistance_growth=-0.2 resistance_decay=0.2 compliance_growth=0.2 army_intel_to_others=7.5 (+4) |
| `high_police` | 3 | 100 |  |  | political_power_factor=-0.025 stability_factor=0.025 personal_expense=0.2 resistance_growth=-0.1 resistance_decay=0.1 compliance_growth=0.1 army_intel_to_others=15 (+4) |
| `medium_police` (def) | 4 | 100 |  |  | stability_factor=-0.025 personal_expense=0.15 army_intel_to_others=22.5 airforce_intel_to_others=22.5 navy_intel_to_others=22.5 civilian_intel_to_others=22.5 society_development_monthly=0.005 |
| `private_police` (def) | 4 | 100 |  |  | stability_factor=-0.05 personal_expense=0.2 resistance_growth=-0.1 resistance_decay=0.1 compliance_growth=0.1 army_intel_to_others=15 airforce_intel_to_others=15 (+3) |
| `private_police_upgrade` (def) | 4 | 100 |  |  | personal_expense=0.25 resistance_growth=-0.15 resistance_decay=0.15 compliance_growth=0.15 army_intel_to_others=15 airforce_intel_to_others=15 navy_intel_to_others=15 (+2) |
| `low_police` | 5 | 100 |  |  | political_power_factor=0.025 stability_factor=-0.05 personal_expense=0.1 resistance_growth=0.1 resistance_decay=-0.1 compliance_growth=-0.1 army_intel_to_others=30 (+4) |
| `lower_police` | 6 | 100 |  |  | political_power_factor=0.05 stability_factor=-0.075 personal_expense=0.05 resistance_growth=0.2 resistance_decay=-0.2 compliance_growth=-0.2 army_intel_to_others=37.5 (+4) |
| `lowest_police` | 7 | 100 |  |  | political_power_factor=0.075 stability_factor=-0.1 resistance_growth=0.3 resistance_decay=-0.3 compliance_growth=-0.3 army_intel_to_others=45 airforce_intel_to_others=45 (+3) |
| `anarchist_order` | 8 | 100 | [APA,FPR] |  | army_intel_to_others=30 airforce_intel_to_others=30 navy_intel_to_others=30 civilian_intel_to_others=30 society_development_monthly=0.01 |

## 2. Идеологии и подидеологии

11 идеологий (партий) - допустимые значения `ideology =` в `add_popularity`, `set_party_name`, `set_politics`. Подидеология (`types`) задаётся лидеру: `country_leader = { ideology = <подидеология> }`, `promote_character = { ideology = ... }`. Звёздочка `*` - `can_be_randomly_selected = no` (специальная подидеология: назначается скриптом, случайно не выпадает).

- **`totalitarian_socialist`** (12): `jucheism*`, `totalism`, `digital_leninism*`, `technocracy_totsoc*`, `maoism`, `jacobinism*`, `chekist_communism*`, `eurasianism_left*`, `left_wing_junta`, `social_fascism*`, `neo_stalinism*`, `transhumanism*`
  - ИИ: ai_communist; `war_impact_on_world_tension` = 1
- **`communist`** (12): `market_socialism*`, `putinism_neosoviet*`, `marxism_leninism`, `anti_revisionist_communism`, `populist_sovietism*`, `neo_socialism*`, `left_baathism*`, `left_nationalism*`, `red_derzhavism*`, `xi_jinping_thought*`, `li_zuocheng_thought*`, `trotskyism`
  - ИИ: ai_communist; `war_impact_on_world_tension` = 0.75
- **`libertarian_socialist`** (14): `left_anarchist`, `post_leftism`, `popular_front_socialism*`, `labour_syndicalism*`, `left_accelerationist*`, `reformist_socialism*`, `eco_socialism`, `eurocommunism*`, `communist_populism*`, `sovereign_democracy_left*`, `sovereign_democracy_lukashenko*`, `sovereign_democracy_prilepin*`, `sovereign_democracy_platoshkin*`, `confucian_socialism*`
  - ИИ: ai_communist; `war_impact_on_world_tension` = 2
- **`social_democrat`** (15): `left_centrist*`, `progressivism*`, `social_democracy`, `reformist_socialism_socdem*`, `left_populism*`, `green_politics*`, `technocracy*`, `social_patriotism*`, `neo_socialism_socdem*`, `sovereign_democracy_left_socdem*`, `sovereign_democracy_delyagin*`, `sovereign_democracy_konovalov*`, `sovereign_democracy_grudinin*`, `putinism_social_democrat*`, `lukashenkoism_socdem*`
  - ИИ: ai_democratic; `war_impact_on_world_tension` = 1
- **`social_liberal`** (11): `centrist*`, `neoliberalism`, `taiwanese_liberal_populism*`, `christian_democracy*`, `supervised_democracy_liberal*`, `russian_patriotic_liberalism*`, `liberal_socialism*`, `green_liberalism*`, `sovereign_democracy_liberal*`, `ultra_liberalism*`, `centrist_pluralism*`
  - ИИ: ai_democratic; `war_impact_on_world_tension` = 1
- **`market_liberal`** (6): `right_libertarianism`, `right_anarchism`, `classical_liberalism`, `civic_nationalism*`, `trumpism_market*`, `putinism_liberal*`
  - ИИ: ai_democratic; `war_impact_on_world_tension` = 1
- **`conservative`** (24): `right_centrist*`, `constitutionalist*`, `christian_conservatism*`, `right_populism*`, `neoconservative`, `classical_conservatism`, `national_conservativism_con`, `supervised_democracy*`, `islamic_democrat*`, `sovereign_democracy*`, `sovereign_democracy_patrushev*`, `sovereign_democracy_sobyanin*`, `sovereign_democracy_mishustin*`, `sovereign_democracy_belousov*`, `putinism_conservative*`, `russian_patriotic_populism*`, `generic_patriotic_populism*`, `belarus_patriotic_populism*`, `france_patriotic_populism*`, `transnistria_patriotic_populism*`, `conservative_socialism*`, `neo_sovereign_democracy*`, `trumpism_conservative*`, `fehlinger_doctrine*`
  - ИИ: ai_democratic; `war_impact_on_world_tension` = 1
- **`authoritarian_democrat`** (33): `oligarchist*`, `ultra_conservatism*`, `democratic_derzhavism*`, `leonid_slutsky_thought*`, `reformed_tridemism*`, `islamic_authoritarian*`, `hybrid_regime`, `auth_populism`, `national_conservativism_auth`, `military_democracy*`, `corporatocracy`, `ultraglobalism*`, `assadist_baathism*`, `sovereign_democracy_auth_dem*`, `sovereign_democracy_volodin*`, `sovereign_democracy_naryshkin*`, `sovereign_democracy_shoygu*`, `putinism*`, `kadyrovite_tendency*`, `populist_putinism*`, `patriotic_socialism*`, `novocommunism*`, `russian_patriotic_meritocracy*`, `russian_monarchist_conservative*`, `pragmatic_socialism*`, `trumpism_authdem*`, `state_liberalism*`, `left_pragmatism*`, `national_patriotism*`, `russian_nationalism_ideology*`, `russian_nationalism_lib*`, `russian_nationalism_soviet*`, `russian_nationalism_national*`
  - ИИ: ai_neutral; `war_impact_on_world_tension` = 1
- **`nationalist`** (18): `autocrat`, `theocracy*`, `mafia_state*`, `mafia_state_2*`, `absolute_monarchist*`, `salafi*`, `wahabi*`, `radical_nationalism*`, `putinism_imperial*`, `military_junta`, `neo_luddism*`, `purification_administration*`, `right_wing_accelerationist*`, `putinism_despot*`, `davos_system*`, `empty*`, `technocratic_utilitarism*`, `pax_americana_ultraglobalism*`
  - ИИ: ai_neutral; `war_impact_on_world_tension` = 1
- **`fascist`** (21): `falangist*`, `ethno_nationalism`, `national_spartanism`, `classical_fascism`, `clerical_fascism`, `fascist_populism`, `blackhundredism*`, `ultra_putinism*`, `naturalized_derzhavism*`, `derzhavism*`, `national_derzhavism*`, `revivalist_derzhavism*`, `ecofascism*`, `national_syndicalism`, `vladimir_zhirinovsky_thought*`, `vladimir_zhirinovsky_thought_post_war*`, `vladimir_zhirinovsky_thought_militarist*`, `russian_syncretism*`, `ultranationalism*`, `confucian_hyperconservativism*`, `chinese_exceptionalism*`
  - ИИ: ai_fascist; `war_impact_on_world_tension` = 1
- **`national_socialist`** (14): `esoteric_fascism`, `neonazism`, `american_neonazism*`, `eurasianism*`, `identitarianism*`, `accelerationist*`, `babylonian_nazism*`, `national_bolshevism*`, `strassarite*`, `death_cult*`, `greater_russia_system*`, `iraqi_baathism*`, `falun_dafa*`, `obliteration_of_the_self*`
  - ИИ: ai_fascist; `war_impact_on_world_tension` = 1

## 3. Черты (leader_traits)

Формат: `имя - главные эффекты`. Черты не привязаны к стране в самом определении (`random = no`); ограничения накладывает идея-министр (`allowed`) или персонаж. Новых имён не придумывать - брать из списка (ограничение «имя должно существовать в TFR», иначе будет ошибка в `error.log`).

### Глава правительства (`hog_*`, `party_*`)

- `hog_old_guard` - stability_factor=0.025
- `hog_ambitious_union_boss` - industrial_capacity_factory=0.08 political_power_gain=0.05
- `hog_chairman` - industrial_capacity_factory=0.025 war_support_factor=0.1 political_power_gain=0.15 army_morale_factor=0.05
- `hog_uncontested_prime_minister` - production_factory_max_efficiency_factor=0.075 war_support_factor=0.05 political_power_gain=0.15 army_morale_factor=0.075
- `hog_shadow_president` - production_speed_arms_factory_factor=0.1 war_support_factor=0.075 stability_factor=-0.1 political_power_cost=-0.15 army_attack_factor=0.065
- `hog_great_unifier` - stability_factor=0.1 political_power_gain=0.15 production_speed_buildings_factor=0.025 industrial_capacity_factory=0.025
- `hog_backroom_backstabber` - stability_factor=-0.07 political_power_gain=0.13
- `hog_corporate_suit` - trade_opinion_factor=0.05 political_power_gain=-0.12 production_speed_industrial_complex_factor=0.08 production_speed_office_park_factor=0.08 production_speed_arms_factory_factor=0.04
- `hog_technocratic_businessman` - political_power_gain=-0.1 production_factory_max_efficiency_factor=0.05 research_speed_factor=0.05
- `hog_flamboyant_tough_guy` - war_support_factor=0.05 stability_factor=0.05 political_power_gain=-0.1
- `hog_happy_amateur` - production_speed_buildings_factor=-0.04 political_power_gain=0.1
- `hog_local_tyrant` - political_power_gain=-0.09 local_resources_factor=0.13
- `hog_popular_tyrant` - political_power_gain=-0.09 local_resources_factor=0.08 stability_factor=0.04
- `hog_son_of_batyka` - political_power_gain=0.05 local_resources_factor=0.02 stability_factor=0.015
- `hog_naive_optimist` - political_power_gain=-0.05 production_speed_industrial_complex_factor=0.11 production_speed_arms_factory_factor=-0.09
- `hog_charming_hillbilly` - political_power_gain=-0.05 stability_factor=0.05 production_factory_max_efficiency_factor=0.015 production_speed_industrial_complex_factor=0.025 production_speed_infrastructure_factor=0.05
- `hog_old_admiral` - production_speed_naval_base_factor=0.09 production_speed_dockyard_factor=0.06 experience_gain_navy=0.12
- `hog_old_air_marshal` - production_speed_air_base_factor=0.13 experience_gain_air=0.05 equipment_bonus={..}
- `hog_old_general` - production_speed_bunker_factor=0.09 max_planning=0.1 experience_gain_army=0.07
- `hog_old_general_2` - name=hog_old_general production_speed_arms_factory_factor=0.05 max_planning=0.1 war_stability_factor=0.07
- `hog_political_protege` - political_power_gain=0.11
- `hog_pragmatic_statesman` - political_power_gain=0.14
- `hog_pragmatic_statesman_2` - stability_factor=0.05 political_power_gain=0.1 consumer_goods_factor=0.035
- `hog_reformist_soldier` - experience_gain_army_factor=0.08 army_morale_factor=0.1
- `hog_respected_war_hero` - political_power_gain=0.06 army_morale_factor=0.1 training_time_factor=-0.12
- `hog_silent_workhorse` - political_power_gain=0.07 local_resources_factor=0.14
- `hog_smiling_oilman` - production_factory_max_efficiency_factor=0.05 production_speed_synthetic_refinery_factor=0.12
- `hog_spiritual_leader` - stability_factor=0.1 consumer_goods_factor=0.05
- `hog_peaceful_revolutionary` - political_power_gain=0.11 war_support_factor=-0.02
- `hog_revolutionary` - political_power_gain=0.08 industrial_capacity_factory=0.04
- `hog_patriotic_ideolouge` - political_power_gain=0.08 production_speed_arms_factory_factor=0.04 stability_factor=-0.03
- `hog_firebrand_revolutionary` - political_power_gain=0.03 army_attack_factor=0.04 war_support_factor=0.04 stability_factor=-0.06 industrial_capacity_factory=-0.04
- `hog_committed_social_activist` - political_power_gain=0.03 income_growth_factor=0.03 stability_factor=-0.03 expense_growth_factor=-0.03
- `hog_militant_revolutionary` - political_power_gain=-0.11 industrial_capacity_factory=0.04 production_speed_arms_factory_factor=0.08
- `hog_old_figurehead` - political_power_gain=0.11 stability_factor=0.02
- `hog_military_statist` - political_power_gain=-0.14 production_speed_arms_factory_factor=0.08 production_speed_dockyard_factor=0.08 local_resources_factor=0.08
- `hog_radical_militarist` - political_power_gain=0.05 industrial_capacity_factory=0.05 war_support_factor=0.05
- `hog_experienced_journalist` - political_power_gain=0.11 production_factory_efficiency_gain_factor=0.06 stability_factor=-0.06
- `hog_smiling_serpent` - political_power_gain=-0.08 stability_factor=0.06
- `hog_controversial_politican` - political_power_gain=0.05 stability_factor=-0.06
- `hog_impudent_poseur` - political_power_gain=-0.1 stability_factor=-0.05 income_growth_factor=-0.01 war_support_factor=-0.025
- `hog_radical_financer` - political_power_gain=-0.08 production_speed_industrial_complex_factor=0.08 income_growth_factor=0.04 expense_growth_factor=-0.04
- `hog_fundementalist` - political_power_gain=0.11 stability_factor=-0.06 war_stability_factor=0.12
- `hog_distinguished_gentleman` - political_power_gain=0.08 stability_factor=0.02 war_support_factor=-0.02
- `hog_effective_manager` - political_power_gain=0.08 stability_factor=0.023 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05 income_growth_factor=0.04
- `hog_syncretic_politics` - political_power_gain=-0.05 war_support_factor=0.02 army_attack_factor=0.03 industrial_capacity_factory=0.023 army_morale_factor=0.015 stability_factor=-0.06
- `hog_his_serene_highness_knyaz` - political_power_gain=0.075 stability_factor=0.04 conservative_drift=0.02
- `hog_decentralized_governance` - political_power_gain=-0.05 stability_factor=0.1 war_support_factor=-0.05 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05 production_factory_efficiency_gain_factor=-0.025 production_factory_max_efficiency_factor=0.015
- `hog_pretty_boy` - political_power_gain=0.12 production_speed_buildings_factor=-0.04 industrial_capacity_factory=-0.04 industrial_capacity_dockyard=-0.04
- `hog_pretty_boy_good` - war_stability_factor=0.05 production_speed_buildings_factor=0.02 industrial_capacity_factory=0.01
- `hog_pretty_boy_koizumi` - war_stability_factor=0.05 production_speed_buildings_factor=0.02 industrial_capacity_factory=0.01
- `hog_military_government_cabinet` - stability_factor=-0.02 experience_gain_army=0.02 production_speed_industrial_complex_factor=-0.02 production_speed_arms_factory_factor=0.03
- `hog_liberal_socialist` - political_power_gain=0.04 income_growth_factor=0.04 industrial_capacity_factory=0.03
- `party_pragmatic_statesman` - stability_factor=0.01 political_power_gain=-0.05
- `party_party_veteran` - stability_factor=0.005
- `party_hardliner` - stability_factor=-0.015 war_support_factor=0.025 political_power_gain=0.1
- `party_public_intellectual` - stability_factor=0.025 political_power_gain=-0.1
- `party_regional_heavyweight` - stability_factor=-0.015 political_power_gain=0.05 production_speed_buildings_factor=0.01
- `party_guardian_of_marxism_leninism` - political_power_gain=0.1 communist_drift=0.01
- `party_guardian_of_marxism_leninism_2` - political_power_gain=0.15 drift_defence_factor=0.15 communist_drift=0.01
- `party_eurasian_leninist` - communist_drift=0.01 war_support_factor=0.03
- `party_historian` - communist_drift=0.01 drift_defence_factor=0.1 stability_factor=0.015
- `party_sentinel_of_party` - stability_factor=0.01
- `party_ideological_mediator` - stability_factor=0.005 war_support_factor=0.005
- `party_popular_compromise` - war_support_factor=0.015
- `party_effective_manager` - stability_factor=0.005 political_power_gain=0.05
- `party_youth_hero` - stability_factor=-0.015 war_support_factor=0.01 political_power_gain=0.1
- `party_president_of_rsfsr` - political_power_gain=0.1
- `party_decentralized_governance` - political_power_gain=-0.05

### Министр экономики (`eco_*`)

- `eco_experienced_capitalist` - stability_factor=0.03 production_speed_buildings_factor=0.08
- `eco_wise` - local_resources_factor=0.06
- `kor_apr_eco_manager_most_ingenious` - political_power_factor=-0.12 production_factory_efficiency_gain_factor=0.04 line_change_production_efficiency_factor=0.06 industrial_capacity_factory=0.08 local_resources_factor=0.06 fuel_gain_factor=10
- `eco_syndicate_proponent` - production_factory_efficiency_gain_factor=0.05 line_change_production_efficiency_factor=0.05
- `eco_economic_organizer` - stability_factor=0.02 consumer_goods_factor=-0.04
- `eco_economic_organizer_super` - stability_factor=0.05 consumer_goods_factor=-0.15
- `eco_war_industrialist` - industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05
- `SOV_viktor_bout_modifier` - custom_modifier_tooltip=SOV_viktor_bout_tt
- `eco_captain_of_industry` - production_speed_buildings_factor=0.05
- `eco_administrative_genius` - political_power_factor=0.03 production_speed_buildings_factor=0.02 research_speed_factor=0.03 industrial_capacity_factory=0.02
- `eco_computer_economic_managment` - production_speed_buildings_factor=0.03 research_speed_factor=0.015 industrial_capacity_factory=0.05 political_power_gain=0.05 production_factory_efficiency_gain_factor=0.05 production_factory_max_efficiency_factor=0.02 income_growth_factor=0.05
- `eco_balanced_budget_economy` - political_power_gain=0.03 production_speed_buildings_factor=0.02 production_factory_max_efficiency_factor=0.02
- `eco_balanced_budget_economy_less_buff` - production_speed_buildings_factor=0.02 production_factory_max_efficiency_factor=0.02
- `eco_bank_president` - production_speed_buildings_factor=0.04 political_power_gain=0.02
- `eco_syndicalist` - production_factory_efficiency_gain_factor=0.03 line_change_production_efficiency_factor=0.03 consumer_goods_factor=-0.03 stability_factor=0.01
- `eco_construction_magnate` - production_speed_infrastructure_factor=0.04 production_speed_air_base_factor=0.04 production_speed_naval_base_factor=0.04 production_speed_radar_station_factor=0.04 production_speed_rocket_site_factor=0.04
- `eco_corrupt_kleptocrat` - local_resources_factor=-0.05 consumer_goods_factor=0.06 political_power_gain=0.15
- `eco_organized_racketeer` - political_power_gain=-0.1 production_speed_buildings_factor=0.035 production_factory_efficiency_gain_factor=0.04
- `eco_industrial_chemist` - local_resources_factor=0.05 production_speed_industrial_complex_factor=0.02 production_speed_infrastructure_factor=0.03 production_speed_synthetic_refinery_factor=0.03
- `eco_corrupt` - misc_expense=5 political_power_gain=-0.025
- `eco_industrialiser` - industrial_capacity_factory=0.02 production_speed_buildings_factor=0.03 local_resources_factor=0.02 conscription_factor=-0.02 political_power_gain=-0.04
- `eco_keynesian_economy` - production_factory_max_efficiency_factor=-0.03 local_resources_factor=-0.02 consumer_goods_factor=-0.08 political_power_gain=0.04
- `eco_laissez_faire_capitalist` - production_speed_arms_factory_factor=-0.02 production_speed_buildings_factor=0.04 local_resources_factor=0.02 political_power_gain=-0.03
- `eco_military_entrepreneur` - production_speed_arms_factory_factor=0.04 production_factory_max_efficiency_factor=0.03 war_support_factor=0.02
- `eco_mixed_economy` - production_factory_max_efficiency_factor=0.02 local_resources_factor=0.03 production_speed_buildings_factor=0.03
- `eco_oil_baron` - local_resources_factor=0.04 production_factory_max_efficiency_factor=0.02 production_speed_synthetic_refinery_factor=0.04
- `eco_collectivist` - local_resources_factor=-0.03 production_factory_max_efficiency_factor=-0.025 consumer_goods_factor=-0.075 production_speed_buildings_factor=0.05
- `eco_labor_specialist` - production_speed_arms_factory_factor=-0.04 production_factory_max_efficiency_factor=0.04 consumer_goods_factor=-0.08
- `eco_economic_populist` - production_speed_infrastructure_factor=0.04 production_speed_industrial_complex_factor=0.03 local_resources_factor=0.02
- `eco_radical_redistrubutionist` - stability_factor=-0.05 production_factory_efficiency_gain_factor=0.1 production_speed_industrial_complex_factor=0.05 dtg_threshold_factor=-0.1
- `eco_reformer` - production_speed_infrastructure_factor=0.05 production_speed_industrial_complex_factor=0.02 interest_rate_factor=0.1
- `eco_economic_silent_workhorse` - consumer_goods_factor=0.06 production_speed_buildings_factor=0.05 stability_factor=0.03 production_factory_max_efficiency_factor=0.05
- `eco_proponent_of_stalin_model` - consumer_goods_factor=0.06 local_resources_factor=-0.02 production_speed_infrastructure_factor=0.05 production_factory_efficiency_gain_factor=0.05 production_speed_synthetic_refinery_factor=0.02 production_speed_industrial_complex_factor=0.05 totalitarian_socialist_drift=0.01
- `eco_socialist_market_economist` - consumer_goods_factor=-0.06 local_resources_factor=0.05 production_speed_infrastructure_factor=0.1 production_speed_industrial_complex_factor=0.05 production_factory_efficiency_gain_factor=-0.05 interest_rate_factor=0.1
- `eco_kosyginist_economics` - consumer_goods_factor=0.08 local_resources_factor=0.05 production_speed_infrastructure_factor=-0.05 production_factory_efficiency_gain_factor=0.1 industrial_capacity_factory=0.05
- `eco_america_first_economics` - consumer_goods_factor=0.05 local_resources_factor=0.1 business_value_factor=0.1 production_speed_infrastructure_factor=-0.05 production_factory_efficiency_gain_factor=0.1 industrial_capacity_factory=0.06
- `eco_resource_industrialist` - local_resources_factor=0.06
- `eco_steel_magnate` - local_resources_factor=0.04 production_factory_max_efficiency_factor=0.02
- `eco_railway_magnate` - production_speed_infrastructure_factor=0.1 production_speed_rail_way_factor=0.1
- `eco_regretful_taxman` - political_power_gain=0.05 business_value_factor=0.05
- `eco_shipping_baron` - production_speed_naval_base_factor=0.04 production_speed_dockyard_factor=0.04 production_factory_max_efficiency_factor=0.03 local_resources_factor=-0.02
- `eco_theoretical_scientist` - production_speed_rocket_site_factor=0.05 production_speed_nuclear_reactor_factor=0.05 research_speed_factor=0.01
- `eco_visionary_capitalist` - stability_factor=-0.1 research_speed_factor=0.025 production_factory_max_efficiency_factor=0.03 production_speed_infrastructure_factor=0.015 production_speed_rocket_site_factor=0.05 production_speed_nuclear_reactor_factor=0.05 production_speed_industrial_complex_factor=0.015
- `eco_radical_green_new_deal` - consumer_goods_factor=-0.05 local_resources_factor=0.1 production_speed_infrastructure_factor=-0.05 production_speed_industrial_complex_factor=-0.05 production_speed_energy_farm_factor=0.1 monthly_population=0.5
- `eco_air_superiority_proponent` - equipment_bonus={..}
- `eco_battlefield_support_proponent` - equipment_bonus={..}
- `eco_battle_fleet_proponent` - equipment_bonus={..}
- `eco_carrier_proponent` - equipment_bonus={..}
- `eco_infantry_proponent` - equipment_bonus={..}
- `eco_naval_aviation_proponent` - equipment_bonus={..}
- `eco_u_boat_proponent` - equipment_bonus={..}
- `eco_tank_proponent` - equipment_bonus={..}
- `eco_strategic_destruction_proponent` - equipment_bonus={..}

### Министр иностранных дел (`for_*`)

- `for_cool_japan` - opinion_gain_monthly_same_ideology_factor=0.3 trade_opinion_factor=0.05 dtg_threshold_factor=0.045 interest_rate_factor=0.025
- `for_fervent_nationalist` - war_support_factor=0.05 weekly_bombing_war_support=0.002 weekly_casualties_war_support=0.002 weekly_convoys_war_support=0.002
- `for_senbonzakura` - war_support_factor=0.05 weekly_bombing_war_support=0.002 weekly_casualties_war_support=0.002 weekly_convoys_war_support=0.002
- `for_perfect_diplomat` - war_support_factor=0.05 weekly_bombing_war_support=0.002 weekly_casualties_war_support=0.002 weekly_convoys_war_support=0.002 opinion_gain_monthly=5 trade_opinion_factor=1
- `for_expansionist` - war_support_factor=0.05 offensive_war_stability_factor=0.1
- `for_appeaser` - war_support_factor=-0.05 war_stability_factor=-0.15 stability_factor=0.1
- `for_loyal_nationalist` - stability_factor=0.06 war_support_factor=0.03
- `for_biased_intellectual` - opinion_gain_monthly_same_ideology_factor=0.15 opinion_gain_monthly_factor=-0.15 political_power_cost=-0.1
- `for_socialist_internationalist` - political_power_gain=0.05 libertarian_socialist_drift=0.01 opinion_gain_monthly_same_ideology_factor=0.15 social_democrat_acceptance=50 libertarian_socialist_acceptance=50 communist_acceptance=50 totalitarian_socialist_acceptance=50
- `for_ideological_crusader` - opinion_gain_monthly_same_ideology_factor=0.3 army_morale_factor=0.025 conscription_factor=0.01 army_core_attack_factor=0.01
- `for_firebrand_soldier` - stability_factor=-0.05 army_morale_factor=0.05 conscription_factor=0.01 war_support_factor=0.03
- `for_apologetic_clerk` - political_power_gain=0.15 stability_factor=0.01
- `for_iron_fisted_brute` - trade_opinion_factor=-0.1 justify_war_goal_time=-0.2 political_power_factor=0.015 army_attack_factor=0.02 war_stability_factor=-0.01
- `for_great_compromiser` - trade_opinion_factor=0.1 political_power_gain=0.1 business_value_factor=0.02 tax_business_rate_factor=-0.015
- `for_general_staffer` - justify_war_goal_time=-0.05 production_speed_bunker_factor=0.1 experience_gain_army_factor=0.05
- `for_the_cloak_n_dagger_schemer` - political_power_gain=-0.05 decryption=0.1
- `for_defensive_hawk` - mobilization_speed=0.1 defensive_war_stability_factor=0.1 offensive_war_stability_factor=-0.1 army_core_attack_factor=0.05 army_core_defence_factor=0.05
- `for_america_first_diplomacy` - army_core_defence_factor=0.025 political_power_factor=0.035 interest_rate_factor=-0.02 business_value_factor=0.05 income_growth_factor=0.04 misc_income=15
- `for_wolf_warrior` - political_power_gain=-0.1 mobilization_speed=0.1 offensive_war_stability_factor=0.1 army_attack_factor=0.05 army_defence_factor=-0.1
- `for_soviet_revanchist` - political_power_gain=-0.05 mobilization_speed=0.1 offensive_war_stability_factor=0.1 army_attack_factor=0.025 army_core_defence_factor=0.025
- `for_eurasianist_theorist` - political_power_factor=0.05 mobilization_speed=0.05 war_support_factor=0.1 army_core_attack_factor=0.05 breakthrough_factor=0.1 non_core_manpower=0.15 army_core_defence_factor=0.01
- `for_global_interventionist` - political_power_gain=-0.1 war_support_factor=0.05 send_volunteer_size=2 industrial_capacity_factory=0.05 industrial_capacity_dockyard=0.05
- `for_free_trader` - war_support_factor=-0.03 trade_opinion_factor=0.15 business_value_factor=0.05 income_growth_factor=0.03
- `for_connected_businessman` - improve_relations_maintain_cost_factor=-0.5 trade_opinion_factor=0.05 dtg_threshold_factor=0.045 interest_rate_factor=0.025
- `for_loyal_magnate` - political_power_cost=0.05 tax_business_rate_factor=-0.1 business_value_factor=0.1 interest_rate_factor=0.05 income_growth_factor=0.015
- `for_pragmatic_liberal` - trade_opinion_factor=0.15 war_stability_factor=0.1 war_support_factor=-0.05 stability_factor=0.05
- `for_progressive_diplomat` - political_power_gain=0.07 trade_opinion_factor=0.1 war_support_factor=-0.05 income_growth_factor=0.03
- `for_balanced_interventionist` - send_volunteer_size=1 industrial_capacity_factory=0.025 industrial_capacity_dockyard=0.05 army_core_defence_factor=0.025 political_power_factor=0.05 income_growth_factor=0.07

### Министр внутренних дел (`sec_*`)

- `sec_ace_attorney` - stability_factor=0.04 political_power_gain=0.04 industrial_capacity_factory=0.05
- `sec_sanest_japanese_man_in_korea` - stability_factor=0.04 political_power_gain=0.04 resistance_target=-0.5 required_garrison_factor=-0.5
- `sec_defensive_excavator` - political_power_gain=-0.03 local_resources_factor=0.08
- `sec_internal_compromiser` - political_power_gain=0.05 industrial_capacity_factory=0.05 line_change_production_efficiency_factor=0.05
- `sec_queen_of_france` - political_power_gain=0.05 stability_factor=0.05 compliance_gain=0.025
- `sec_efficent_attorney` - political_power_gain=0.05 stability_factor=0.05 compliance_gain=0.025
- `sec_compassionate_gentleman` - stability_factor=0.02 political_power_gain=0.04
- `sec_political_architect` - stability_factor=0.025 political_power_gain=0.1 fascist_drift=0.01 nationalist_drift=0.01 authoritarian_democrat_drift=0.01 non_core_manpower=0.025
- `SOV_surkov_modifier` - custom_modifier_tooltip=SOV_surkov_trait_tt
- `sec_long_lasting_state_ideologue` - stability_factor=0.1 political_power_gain=0.1 nationalist_drift=0.01 compliance_gain=0.05 starting_compliance=0.45
- `sec_populist_propagandist` - stability_factor=0.1 political_power_gain=0.065 authoritarian_democrat_drift=0.01 compliance_gain=0.05 starting_compliance=0.15
- `sec_efficent_organizer` - stability_factor=0.04 political_power_gain=0.04 industrial_capacity_factory=0.05
- `sec_religious_nationalist` - political_power_gain=0.1 nationalist_drift=0.01
- `sec_hardline_ideologue` - political_power_gain=0.1 stability_factor=-0.04 war_support_factor=0.025 nationalist_drift=0.01 resistance_damage_to_garrison=-0.1 conscription_factor=0.015
- `sec_crime_fighter` - political_power_gain=0.05 conscription_factor=-0.02 stability_factor=0.04
- `sec_anti_pope` - nationalist_drift=0.01 political_power_gain=0.05 conscription_factor=0.02 stability_factor=0.04
- `sec_reformer` - political_power_gain=0.03 stability_factor=0.02
- `sec_crooked_kleptocrat` - political_power_gain=0.04 production_speed_buildings_factor=-0.02
- `sec_efficient_sociopath` - local_resources_factor=0.05 conscription_factor=-0.02
- `sec_health_and_safety` - political_power_gain=0.05 conscription_factor=0.03 local_resources_factor=-0.04 production_speed_buildings_factor=0.04
- `sec_man_of_the_people` - stability_factor=0.05 resistance_target=-0.05
- `sec_media_magnate` - consumer_goods_factor=-0.05 political_power_gain=0.1
- `sec_prince_of_terror` - political_power_gain=0.05 local_resources_factor=0.05 global_building_slots_factor=0.05 resistance_target=0.1
- `sec_princess_of_terror` - political_power_gain=0.05 local_resources_factor=0.05 global_building_slots_factor=0.05 resistance_target=0.1
- `sec_secret_police_chief` - political_power_gain=-0.04 civilian_intel_to_others=-5 airforce_intel_to_others=-5 navy_intel_to_others=-5 resistance_growth=-0.05 resistance_decay=0.05
- `sec_tough_sheriff` - political_power_gain=0.05 war_stability_factor=0.06 compliance_gain=-0.1 resistance_damage_to_garrison=-0.1 resistance_growth=-0.1
- `sec_soldier_of_the_people` - war_support_factor=0.025 production_speed_buildings_factor=0.05 global_building_slots_factor=0.05 resistance_growth=-0.05 resistance_decay=0.05
- `sec_silent_lawyer` - political_power_gain=0.1
- `sec_loud_lawyer` - political_power_gain=0.1
- `sec_damned_liberal` - political_power_gain=-0.02 social_liberal_drift=0.05
- `sec_educator` - research_speed_factor=0.04
- `sec_crazy_scientist` - research_speed_factor=0.1
- `sec_rearmer` - political_power_gain=-0.03 industrial_capacity_factory=0.05
- `sec_architect_artist` - political_power_gain=0.02 industrial_capacity_factory=0.02 production_speed_buildings_factor=0.02
- `sec_propaganda_master` - political_power_gain=-0.03 compliance_growth=0.1 required_garrison_factor=-0.1 resistance_damage_to_garrison=-0.1
- `sec_mathematician` - political_power_gain=0.05 research_speed_factor=0.05
- `sec_ai_anti_corruption` - stability_factor=0.04 political_power_gain=-0.1 compliance_growth=0.1 misc_income=15 industrial_capacity_factory=0.05 conscription_factor=-0.015
- `sec_imperial_bootlicker` - political_power_gain=0.08 consumer_goods_factor=0.05
- `sec_peacemaker` - political_power_gain=-0.08 resistance_decay=0.05 non_core_manpower=0.15 industry_free_repair_factor=0.1

### Глава разведки (`int_*`)

- `int_featuring_dante` - root_out_resistance_effectiveness_factor=0.1 required_garrison_factor=-0.1 resistance_decay=0.05 resistance_growth=-0.05
- `int_son_sparda` - party_popularity_stability_factor=0.15 drift_defence_factor=-0.025
- `int_humble_librarian` - research_speed_factor=0.15 decryption_factor=0.5 encryption_factor=0.15
- `int_balanced_cryptographer` - operative_slot=1 intelligence_agency_defense=0.05 decryption_power_factor=0.05
- `int_decryptor` - operative_slot=1 decryption_power_factor=0.1
- `int_encryptor` - operative_slot=1 intelligence_agency_defense=0.1
- `int_resistance_crusher` - operative_slot=1 root_out_resistance_effectiveness_factor=0.1 required_garrison_factor=-0.1 resistance_decay=0.05 resistance_growth=-0.05
- `int_softie` - root_out_resistance_effectiveness_factor=-0.1 required_garrison_factor=-0.25 stability_factor=0.05
- `int_former_spy` - commando_trait_chance_factor=0.5 operation_cost=-0.25 intel_network_gain_factor=0.33
- `int_psychological_mastermind` - enemy_operative_forced_into_hiding_time_factor=0.5 enemy_operative_detection_chance_factor=0.25
- `int_ideological_enforcer` - operative_slot=1 low_stability_weekly=0.002
- `int_spy_staffer` - operative_slot=2 political_power_gain=-0.05

### Глава государства (`hos_*` и страновые)

Префикс показывает «хозяина» (`usb_` США-Б, `gma_`, `fra_`, `faf_` и т. д.); общие для любой страны - `hos_*`. Эффекты: `stab` = `stability_factor`, `pp` = `political_power_gain`, `ws` = `war_support_factor`.

**`hos_*`** (279):

- `hos_president_japan` - stab=0.05 army_core_defence_factor=0.05 defensive_war_stability_factor=0.1 offensive_war_stability_factor=0.1
- `hos_emerald_weapon` - production_factory_max_efficiency_factor=0.1 ws=0.1 pp=0.05 army_morale_factor=0.1
- `hos_ingenious_creature` - pp=0.15 army_morale_factor=0.1 army_strength_factor=0.1
- `hos_lvl_1_crook` - army_org=1 army_strength_factor=0.05
- `hos_lvl_100_boss` - army_org=3 army_strength_factor=0.1 army_morale=3 stab=0.15
- `hos_french_officer` - ws=0.05 party_popularity_stability_factor=0.05
- `hos_french_collaborator` - resistance_growth=0.08 stab=0.06 pp=-0.025
- `hos_catholic_figurehead` - nationalist_drift=0.06 pp=0.1
- `hos_emperor_of_austrians` - stab=0.1 ws=0.05
- `hos_principled_democrat` - army_morale_factor=0.025 defensive_war_stability_factor=0.05 drift_defence_factor=-0.15
- `hos_socialist_of_the_new_century` - army_attack_against_major_factor=0.025 offensive_war_stability_factor=0.035 consumer_goods_factor=0.025
- `hos_regent_of_poland` - stab=0.05 defensive_war_stability_factor=0.1 ai_focus_aggressive_factor=0.25
- `hos_architect_of_Day_X` - party_popularity_stability_factor=0.12 ws=0.08 nationalist_drift=0.04 fascist_drift=0.04
- `hos_french_noble` - stab=-0.1 consumer_goods_factor=0.1 nationalist_drift=0.05
- `hos_eurofash_demagogue` - fascist_drift=0.06 pp=0.15 fascist_acceptance=25
- `hos_herrenmeister` - pp=0.25 army_attack_factor=0.1
- `hos_national_symbol` - stab=0.05 ws=0.05
- `hos_architect_of_the_revolution` - party_popularity_stability_factor=0.1 ws=0.2 libertarian_socialist_drift=0.02
- `hos_savior_of_the_west` - stab=0.1 ws=0.025 army_morale_factor=0.05 drift_defence_factor=0.15
- `hos_son_of_the_century` - party_popularity_stability_factor=0.1 ws=0.1 army_morale_factor=0.05 drift_defence_factor=0.35
- `hos_red_marshal` - ws=0.1 army_morale_factor=0.1 army_attack_factor=0.1
- `hos_heavy_doctrinal_following` - stab=0.15 pp=0.15
- `hos_voice_of_reason` - social_liberal_acceptance=25 market_liberal_acceptance=25 foreign_minister_cost_factor=-0.5 economic_minister_cost_factor=-0.5 interior_minister_cost_factor=-0.5
- `hos_philosopher_king` - pp=0.1 research_speed_factor=0.05
- `hos_hindenburgian_figure` - authoritarian_democrat_acceptance=25 stab=-0.1 ws=0.1 army_morale_factor=0.05
- `hos_the_doctor` - stab=0.1 pp=0.2
- `hos_caesar` - stab=0.1 ws=0.1
- `hos_aspiring_autocrat` - pp=0.03 stab=-0.03 ai_focus_aggressive_factor=0.1
- `hos_enemy_of_the_united_left` - conservative_drift=-0.05 party_popularity_stability_factor=-0.05
- `hos_the_rightful_heir` - stab=0.05 offensive_war_stability_factor=0.1 ai_focus_aggressive_factor=0.1
- `hos_godfather_of_chongqing_model` - political_power_factor=0.02 production_speed_industrial_complex_factor=0.05 production_speed_infrastructure_factor=0.05 production_factory_start_efficiency_factor=0.035
- `hos_maoist_messiah` - ws=0.05 army_attack_factor=0.035 army_morale_factor=0.015
- `hos_supreme_leader_iran` - ws=0.015 army_attack_factor=0.025 army_morale_factor=0.015 stab=0.025
- `hos_anti_globalist` - ws=0.025 army_core_defence_factor=0.05 army_morale_factor=0.02
- `hos_custodian_of_world_order` - army_core_attack_factor=0.05 breakthrough_factor=0.02 offensive_war_stability_factor=0.1 ai_focus_aggressive_factor=0.1
- `hos_founder_of_the_french_state` - ws=0.05 army_core_attack_factor=0.05 army_core_defence_factor=0.05 offensive_war_stability_factor=0.1 ai_focus_aggressive_factor=0.2
- `hos_foster_son_of_vladimir_volfvich` - ws=0.05 army_core_attack_factor=0.05 army_core_defence_factor=0.05 offensive_war_stability_factor=0.1 ai_focus_aggressive_factor=0.2
- `hos_the_great_warlord` - ws=0.05 army_core_attack_factor=0.05 army_core_defence_factor=0.05 weekly_casualties_war_support=0.05 fascist_drift=0.02
- `hos_the_great_warlord_PRC` - ws=0.05 army_core_attack_factor=0.05 army_core_defence_factor=0.05 weekly_casualties_war_support=0.05 totalitarian_socialist_drift=0.02
- `hos_depressed` - political_power_factor=-0.1 stab=-0.05
- `hos_the_great_reformer` - stab=0.05 party_popularity_stability_factor=0.15 drift_defence_factor=0.025 academic_development_monthly=0.01 society_development_monthly=0.01
- `hos_national_president` - stab=0.025 ws=0.015 pp=0.05 production_speed_buildings_factor=0.05
- `hos_indistinguished_suit` - -
- `hos_articial_leadership` - production_factory_max_efficiency_factor=0.2 political_power_cost=0.15
- `hos_fit_as_a_fiddle` - stab=0.05 pp=0.15
- `hos_crisp_as_lettuce` - pp=0.05
- `hos_fuzzy_around_the_edges` - stab=-0.025 pp=-0.05
- `hos_foggy_as_a_mirror` - stab=-0.05 pp=-0.1
- `hos_lights_on_nobody_home` - stab=-0.075 pp=-0.15
- `hos_present_as_last_years_calendar` - stab=-0.1 pp=-0.2
- `hos_blank` - stab=-0.125 pp=-0.25
- `hos_fit_as_a_fiddle_nss` - stab=-0.05 pp=-0.15
- `hos_crisp_as_lettuce_nss` - pp=-0.05
- `hos_fuzzy_around_the_edges_nss` - stab=0.025 pp=0.05
- `hos_foggy_as_a_mirror_nss` - stab=0.05 pp=0.1
- `hos_lights_on_nobody_home_nss` - stab=0.075 pp=0.15
- `hos_present_as_last_years_calendar_nss` - stab=0.1 pp=0.2
- `hos_blank_nss` - stab=0.125 pp=0.25
- `hos_locked_in_nss` - stab=0.15 pp=0.3
- `hos_voice_of_the_free_world` - ai_focus_aggressive_factor=1 drift_defence_factor=0.25 ws=0.1
- `hos_the_architect` - political_power_factor=0.1 party_popularity_stability_factor=0.1
- `hos_brave` - ws=0.05
- `hos_craven` - ws=-0.05
- `hos_calm` - opinion_gain_monthly=2.5 ws=-0.05
- `hos_wrathful` - opinion_gain_monthly=-2.5 ws=0.05 drift_defence_factor=0.15
- `hos_content` - stab=0.1
- `hos_ambitious` - stab=0.025 ws=0.025 political_power_cost=0.05 production_speed_buildings_factor=0.05
- `hos_diligent` - production_speed_buildings_factor=-0.05 industrial_capacity_dockyard=-0.05 industrial_capacity_factory=-0.05 production_factory_max_efficiency_factor=0.15 production_factory_start_efficiency_factor=0.1
- `hos_lazy` - production_speed_buildings_factor=0.05 industrial_capacity_dockyard=0.05 industrial_capacity_factory=0.05 production_factory_max_efficiency_factor=-0.15
- `hos_forgiving` - compliance_growth_on_our_occupied_states=0.25 resistance_decay_on_our_occupied_states=0.15
- `hos_vengeful` - no_compliance_gain=1 required_garrison_factor=0.5 resistance_growth_on_our_occupied_states=-0.5
- `hos_gregarious` - pp=0.25
- `hos_shy` - pp=-0.25
- `hos_recluse` - pp=-0.125
- `hos_just` - stab=0.05
- `hos_paranoid` - stab=-0.05 drift_defence_factor=-0.15 resistance_decay_on_our_occupied_states=0.15
- `hos_nero` - stab=-0.15 drift_defence_factor=-0.3 resistance_decay_on_our_occupied_states=0.3 army_attack_against_minor_factor=0.1 opinion_gain_monthly_factor=-0.5
- `hos_compassionate` - compliance_growth_on_our_occupied_states=0.25 opinion_gain_monthly_factor=0.25 guarantee_cost=-0.5
- `hos_sadistic` - pp=-0.1 army_attack_against_minor_factor=0.1 opinion_gain_monthly_factor=-0.5
- `hos_stubborn` - opinion_gain_monthly_factor=-0.33
- `hos_lame_duck` - drift_defence_factor=-0.5 stab=-0.1
- `hos_avtoritet` - stab=0.1 consumer_goods_factor=0.1
- `hos_cultural_supremacist_trait` - stab=0.1 compliance_growth_on_our_occupied_states=-0.05 subjects_autonomy_gain=-0.1
- `hos_first_consul_trait` - stab=0.2 subjects_autonomy_gain=-1
- `hos_neo_federalist_trait` - head_minister_cost_factor=-0.25 foreign_minister_cost_factor=-0.25 economic_minister_cost_factor=-0.25 interior_minister_cost_factor=-0.25 intelligence_minister_cost_factor=-0.25
- `hos_russophile` - consumer_goods_factor=-0.05
- `hos_man_of_cobbled_stone` - ws=0.1 pp=-0.15
- `hos_Solid_Snake` - ws=0.125 army_attack_factor=0.1 attrition=-0.1 ai_focus_aggressive_factor=0.8
- `hos_First_of_Her_Name` - stab=0.2
- `hos_estranged_son` - pp=-0.15 ws=-0.05 stab=-0.05
- `hos_insane_regent` - pp=0.25 stab=-0.1 offensive_war_stability_factor=0.1
- `hos_political_jester` - stab=0.05 pp=-0.05
- `hos_Veteran_of_the_European_War` - ws=0.1 army_morale_factor=0.1 army_attack_factor=0.1
- `hos_Patriot_Front_Volunteer` - head_minister_cost_factor=-0.25 foreign_minister_cost_factor=-0.25 economic_minister_cost_factor=-0.25 interior_minister_cost_factor=-0.25 intelligence_minister_cost_factor=-0.25
- `hos_Disgraced_General` - ws=-0.05 mobilization_speed=-0.15
- `hos_crusader_king` - fascist_drift=0.1 fascist_acceptance=75 political_power_factor=0.1
- `hos_caliph` - ws=0.1 weekly_manpower=500 mobilization_speed=0.25
- `hos_puppet_imperator` - military_development_monthly=0.025 national_socialist_drift=0.01 stab=-0.2
- `hos_Marechal` - ws=0.05 army_attack_factor=0.1 attrition=-0.1 ai_focus_aggressive_factor=0.4
- `hos_marshal_of_poland` - ws=0.15 army_attack_factor=0.1 attrition=-0.1 army_core_attack_factor=0.15 army_core_defence_factor=0.15
- `hos_Establishment_Bulwark` - stab=0.05 pp=0.15
- `hos_Freedom_Fighter` - ws=0.1 army_morale_factor=0.1
- `hos_Royalist_Puppet` - stab=-0.1 ws=0.05
- `hos_Governor_Chief` - pp=0.15 resistance_target=-0.15
- `hos_Unbowed_Revolutionary` - social_democrat_drift=0.02 resistance_target=-0.05
- `hos_Unbowed_Revolutionary_libsoc` - libertarian_socialist_drift=0.02 resistance_target=-0.05
- `hos_The_Second_De_Gaulle` - stab=0.1 ws=0.15
- `hos_Middle_Ground_General` - stab=0.05 consumer_goods_factor=-0.1 market_liberal_drift=0.03
- `hos_6th_Republic_Loyalist` - ws=-0.1 social_democrat_drift=0.01
- `hos_6th_Republic_Militarist` - stab=-0.1 social_democrat_drift=-0.02 libertarian_socialist_drift=-0.02 communist_drift=-0.02 totalitarian_socialist_drift=-0.02
- `hos_Pluto` - consumer_goods_factor=-0.025 pp=-0.05
- `hos_King_to_be` - stab=0.05
- `hos_the_Desired` - stab=0.2
- `hos_French_Mussolini` - political_power_factor=0.1 max_command_power_mult=-0.1 custom_modifier_tooltip=Le_Duc_laws_cost_tt
- `hos_Duke_of_Brittany` - stab=0.05
- `hos_Oncle_Jean` - party_popularity_stability_factor=0.1 political_power_factor=0.1 libertarian_socialist_drift=0.02
- `hos_European_Federalist` - stab=0.05 business_value_factor=0.02 subjects_autonomy_gain=-0.15 social_liberal_drift=0.025
- `hos_European_Federalist` - stab=0.05 business_value_factor=0.02 subjects_autonomy_gain=-0.15 social_liberal_drift=0.025
- `hos_revolutionary_teacher` - pp=0.05 research_speed_factor=0.05 communist_drift=0.01
- `hos_king_of_luxembourg` - stab=0.05
- `hos_duke_of_calabria` - stab=0.05
- `hos_duke_of_castro` - stab=0.05
- `hos_duke_of_parma` - stab=0.05
- `hos_British_Ties` - pp=0.1
- `hos_lion_of_russia` - political_power_factor=0.05 weekly_casualties_war_support=0.005 party_popularity_stability_factor=0.05 army_core_attack_factor=0.035 army_core_defence_factor=0.035
- `hos_wounded_lion` - political_power_factor=-0.05 stab=-0.05 party_popularity_stability_factor=-0.05
- `hos_wounded_lion_1` - political_power_factor=-0.1 stab=-0.1 party_popularity_stability_factor=-0.1
- `hos_the_vozhd_of_russia` - weekly_casualties_war_support=0.005 party_popularity_stability_factor=0.1 ws=0.025 army_core_attack_factor=0.03 army_core_defence_factor=0.03
- `hos_the_great_president` - weekly_casualties_war_support=0.005 war_stability_factor=0.05 party_popularity_stability_factor=0.05 ws=0.025 army_core_attack_factor=0.03
- `hos_smiling_for_the_camera` - pp=0.24 stab=0.12 ws=-0.06 trade_opinion_factor=0.16
- `hos_grandfather_of_the_nation` - ws=0.12 army_morale_factor=0.08 industrial_capacity_factory=0.06
- `hos_peoples_fuhrer` - political_power_factor=0.1 weekly_casualties_war_support=0.01 party_popularity_stability_factor=0.2
- `hos_philosopher` - stab=0.05 political_power_cost=0.05 compliance_growth=0.05 production_factory_max_efficiency_factor=0.05
- `hos_Savior_of_the_Republic` - high_command_cost_factor=-0.25 air_chief_cost_factor=-0.25 army_chief_cost_factor=-0.25 navy_chief_cost_factor=-0.25 army_core_attack_factor=0.1
- `hos_protector_of_the_american_dream` - stab=0.15 ws=0.025 army_morale_factor=0.05 drift_defence_factor=0.15
- `hos_Prince_of_Wales` - stab=0.075
- `hos_Modern_Robespierre` - stab=-0.08 production_speed_buildings_factor=-0.125
- `hos_Germanophile` - send_volunteer_size=2 improve_relations_maintain_cost_factor=-1 fascist_acceptance=75
- `hos_Breton_Populist` - stab=0.15 army_morale_factor=0.1
- `hos_Emergency_Powers` - stab=-0.08 pp=0.5
- `hos_the_ghost` - attrition=-0.1 army_morale_factor=0.1
- `hos_covid_positive` - pp=-0.15
- `hos_cult_of_personality` - stab=0.5
- `hos_cult_of_personality_halved` - stab=0.25
- `hos_divisive_populist` - stability_weekly=-0.001 pp=0.2
- `hos_revolutioanry_spirit` - stability_weekly=-0.005 pp=0.25
- `hos_commander_of_chaos` - army_attack_factor=0.1 army_defence_factor=-0.1
- `hos_divisive_populist1` - stability_weekly=-0.001
- `hos_vanguard_of_america` - pp=0.2 war_stability_factor=0.2
- `hos_vanguard_of_america_2` - pp=0.1 war_stability_factor=0.2 army_attack_factor=0.025 army_defence_factor=0.025
- `hos_teflon_don` - pp=0.25 stab=0.1 army_morale_factor=0.1 production_speed_synthetic_refinery_factor=0.045
- `hos_american_cromwell` - pp=-0.05 ws=0.15 defensive_war_stability_factor=0.2 offensive_war_stability_factor=0.4
- `hos_commander_in_chief` - pp=0.05 army_attack_factor=0.025 army_defence_factor=0.025
- `hos_second_lenin` - ws=0.1 war_stability_factor=0.1
- `hos_provisional_president` - pp=-0.05 stab=0.03 drift_defence_factor=-0.15 disabled_ideas=1
- `hos_lady_of_steel` - ws=0.1 political_power_cost=-0.15 army_attack_factor=0.025 army_defence_factor=0.025
- `hos_beacon_of_hope` - stab=0.1 political_power_factor=0.05 libertarian_socialist_drift=0.02
- `hos_russian_ceasar` - army_morale_factor=0.1 army_org_factor=0.08 war_stability_factor=0.075 party_popularity_stability_factor=0.1
- `hos_faux_ceasar` - army_morale_factor=-0.1 war_stability_factor=-0.15
- `hos_political_deadlock` - pp=-0.5 stab=-0.15
- `hos_russian_brutus` - pp=-0.25 army_attack_factor=0.025 army_defence_factor=0.025 stab=-0.15
- `hos_collapsing_authority` - pp=-0.35 army_morale_factor=-0.1 army_attack_factor=-0.15 stab=-0.5 army_defence_factor=-0.15
- `hos_comrade_maxism` - pp=-0.05 army_attack_factor=0.025 army_defence_factor=0.025
- `hos_pariah_of_communism` - pp=-0.1 ws=-0.05 party_popularity_stability_factor=-0.05 communist_acceptance=-75 totalitarian_socialist_acceptance=-75
- `hos_pariah_of_communism_1` - name=hos_pariah_of_communism pp=-0.05 communist_acceptance=-100 totalitarian_socialist_acceptance=-100 libertarian_socialist_acceptance=-100
- `hos_anti_war_activist` - stab=0.1 ws=-0.1
- `hos_social_scholar` - pp=0.1 research_speed_factor=0.05
- `hos_flexible_ideologue` - pp=0.1 stab=-0.05 production_speed_arms_factory_factor=0.05
- `hos_red_dragon_rider` - pp=0.1 ws=0.1
- `hos_red_dragon_rider_1` - name=hos_red_dragon_rider pp=0.18 ws=0.1 production_factory_efficiency_gain_factor=0.05
- `hos_red_dragon_rider_3` - pp=0.25 ws=0.1 war_stability_factor=0.05 max_command_power_mult=0.25 production_factory_efficiency_gain_factor=0.1
- `hos_red_dragon_rider_2` - name=hos_red_dragon_rider pp=0.15 production_factory_start_efficiency_factor=0.035 production_speed_arms_factory_factor=0.05 stab=-0.05
- `hos_president_of_the_commoners` - name=hos_president_of_the_commoners pp=0.05 stab=-0.05 army_morale_factor=0.01
- `hos_american_caesar` - pp=0.1 stab=0.05 army_attack_factor=0.05
- `hos_middleman` - stab=0.1
- `hos_pied_piper` - political_power_factor=0.25
- `hos_insane_kleptocrat` - stab=-0.15 pp=0.25 weekly_manpower=-500 no_compliance_gain=1 resistance_damage_to_garrison=-0.5
- `hos_insane_kleptocrat_1` - stab=-0.1 pp=0.25 weekly_manpower=-500 no_compliance_gain=1 monthly_population=-1.5
- `hos_insane_kleptocrat_2` - stab=-0.05 pp=0.25 weekly_manpower=-500 no_compliance_gain=1 monthly_population=-1.75
- `hos_insane_kleptocrat_3` - pp=0.25 weekly_manpower=-100 resistance_damage_to_garrison=-1 monthly_population=-2 social_liberal_drift=-0.1
- `hos_insane_kleptocrat_eu` - consumer_goods_factor=0.15 political_power_factor=0.15 resistance_damage_to_garrison=-0.25
- `hos_expert_minuteman` - army_core_defence_factor=0.1 army_core_attack_factor=0.05
- `hos_puppet_master` - stab=0.1 political_power_factor=0.05 agency_upgrade_time=-0.15 enemy_operative_detection_chance_factor=0.1 enemy_operative_intel_extraction_rate=0.1
- `hos_puppet_master_2` - stab=0.15 political_power_factor=0.1 agency_upgrade_time=-0.15 enemy_operative_detection_chance_factor=0.15 enemy_operative_intel_extraction_rate=0.1
- `hos_anti_west_populist` - ws=0.02 army_morale_factor=0.05 pp=-0.1
- `hos_multipolar_populist` - ws=0.025 intel_network_gain_factor=0.1 opinion_gain_monthly_factor=0.1 send_volunteer_factor=0.2 lend_lease_tension=-0.3
- `hos_young_guard` - communist_drift=0.03 stab=0.025
- `hos_initiative_apparatchik` - stab=0.025 pp=0.1
- `hos_red_governor` - communist_drift=0.03 pp=0.05 production_speed_infrastructure_factor=0.01 production_speed_rail_way_factor=0.01 production_speed_industrial_complex_factor=0.01
- `hos_red_president` - pp=0.1 production_speed_buildings_factor=0.01
- `hos_peoples_candidate` - communist_drift=0.03 poverty_development_monthly=0.005 farming_development_monthly=0.005
- `hos_peoples_president` - communist_drift=0.01 poverty_development_monthly=0.005 farming_development_monthly=0.01
- `hos_successor` - stab=0.075 pp=0.1
- `hos_scandalous_reformer` - stab=-0.05 pp=0.25
- `hos_lenin_of_xxi_century` - pp=0.15 ws=0.025 army_morale_factor=0.05
- `hos_executor_of_the_partys_will` - pp=0.1
- `hos_political_showman` - stab=-0.01 pp=0.05 ws=0.01
- `hos_the_red_eagle` - stab=0.01 industrial_capacity_factory=0.025 production_factory_max_efficiency_factor=0.025
- `hos_populist_autocrat` - stab=-0.05 pp=0.15 ws=0.1 army_morale_factor=0.025 army_core_attack_factor=0.01
- `hos_populist_president` - pp=0.1 party_popularity_stability_factor=0.1
- `hos_economic_populist` - party_popularity_stability_factor=0.05 production_speed_infrastructure_factor=0.1 production_speed_rail_way_factor=0.1 production_speed_industrial_complex_factor=0.1
- `hos_like_father_like_son` - stab=0.02 pp=0.05
- `hos_grey_wolf` - stab=0.05 ws=0.05 party_popularity_stability_factor=0.1
- `hos_party_golden_boy` - stab=0.1 pp=0.05
- `hos_returned_from_taiga` - party_popularity_stability_factor=0.1 pp=0.05
- `hos_gunji_otaku` - industrial_capacity_factory=0.05 production_factory_start_efficiency_factor=0.025
- `hos_powerless_president` - pp=-0.1
- `hos_capital_p_president` - trade_opinion_factor=0.5 pp=0.1
- `hos_little_puppet_master` - party_popularity_stability_factor=0.1 ws=0.05
- `hos_great_successor` - stab=0.05 pp=0.05 army_core_defence_factor=0.05 army_core_attack_factor=0.05
- `hos_great_liberator` - stab=0.1 ws=0.05
- `hos_batyka` - ws=0.1 production_factory_max_efficiency_factor=0.05
- `hos_batyka_2` - ws=0.1 stab=0.05 industrial_capacity_factory=0.025 production_factory_max_efficiency_factor=0.05 political_power_cost=-0.1
- `hos_lion_of_damascus` - ws=0.1 political_power_factor=0.1 army_core_attack_factor=0.05 army_core_defence_factor=0.05
- `hos_cardinal_of_kremlin` - stab=0.1 pp=0.1 party_popularity_stability_factor=0.1
- `hos_notorious_gangster` - army_core_defence_factor=0.05 army_core_attack_factor=0.1
- `hos_reiwa` - stab=0.1
- `hos_iron_dimon` - ws=0.05 army_attack_factor=0.1 attrition=-0.1 ai_focus_aggressive_factor=0.2
- `hos_iron_russian` - ws=0.05 army_attack_factor=0.075 attrition=-0.1 ai_focus_aggressive_factor=0.2
- `hos_political_mastodon` - stab=0.05 war_stability_factor=0.15 production_speed_infrastructure_factor=0.1 political_power_factor=0.05
- `hos_supreme_commander_and_cheif` - ws=0.1 army_attack_factor=0.15 attrition=-0.12 army_morale_factor=0.05 army_core_defence_factor=0.025
- `hos_supreme_commander_and_cheif_zolotov` - political_power_factor=0.05 ws=0.1 army_attack_factor=0.075 attrition=-0.1 army_morale_factor=0.05
- `hos_great_leader_of_china` - political_power_factor=0.05 ws=0.1 army_attack_factor=0.05 attrition=-0.1 army_morale_factor=0.05
- `hos_the_great_enforcer` - ws=0.15 local_non_core_manpower=0.05 army_attack_factor=0.1 army_morale_factor=0.05 ai_focus_aggressive_factor=0.2
- `hos_father_of_eurasianism` - resistance_activity=-0.1 resistance_damage_to_garrison=-0.1 resistance_decay=0.1 stab=0.05
- `hos_the_great_revolutionary` - ws=0.15 local_non_core_manpower=0.05 army_attack_factor=0.1 army_morale_factor=0.05 ai_focus_aggressive_factor=0.2
- `hos_the_great_revolutionary_PRC` - ws=0.075 local_non_core_manpower=0.05 army_attack_factor=0.05 army_morale_factor=0.025 ai_focus_aggressive_factor=0.2
- `hos_solar_leader_of_eurasia` - stab=0.15 political_power_factor=0.1 agency_upgrade_time=-0.15 enemy_operative_detection_chance_factor=0.15 enemy_operative_intel_extraction_rate=0.1
- `hos_wolf_in_the_moonlight` - ws=0.1 pp=-0.15
- `hos_silver_tongue` - ws=0.1 stab=-0.02 authoritarian_democrat_drift=0.03 pp=-0.05
- `hos_cowed_by_oligarchs` - ws=-0.05 pp=-0.15
- `hos_puppet_of_the_partocrats` - ws=0.05 pp=-0.05 military_development_monthly=0.005 communist_drift=0.05
- `hos_cowed_by_nationalists` - stab=-0.05 ws=0.1 pp=-0.15 local_non_core_manpower=-0.1 ai_focus_aggressive_factor=0.1
- `hos_powerless_regent` - stab=0.1 ws=-0.05 pp=-0.15 army_morale_factor=0.05
- `hos_master_of_europe` - local_non_core_manpower=0.15 subjects_autonomy_gain=-0.05
- `hos_supreme_leader` - ws=0.05 offensive_war_stability_factor=0.15 ai_focus_aggressive_factor=0.4
- `hos_supreme_leader_2` - ws=0.1 stab=0.05 pp=0.02 offensive_war_stability_factor=0.15 ai_focus_aggressive_factor=0.4
- `hos_gospodin_president` - ws=0.01 stab=0.02 pp=0.035 ai_focus_aggressive_factor=0.01
- `hos_gospodin_president_1` - ws=0.02 stab=0.06 pp=0.05 offensive_war_stability_factor=0.1 ai_focus_aggressive_factor=0.01
- `hos_russian_unifier` - ws=0.1 stab=0.02 pp=0.02 offensive_war_stability_factor=0.15 ai_focus_aggressive_factor=0.05
- `hos_puppet_of_radicals` - pp=-0.025 stab=-0.05
- `hos_lord_of_war` - production_speed_arms_factory_factor=0.04 production_factory_max_efficiency_factor=0.03 ws=0.02
- `hos_imperial_majesty` - stab=0.15
- `hos_tsar_of_all_russia` - stab=0.15
- `hos_soldier_king` - ws=0.1
- `hos_hates_russians` - ai_focus_aggressive_factor=1
- `hos_shadow_dictator` - pp=-0.05 production_speed_industrial_complex_factor=0.1 production_speed_infrastructure_factor=0.1 production_speed_rail_way_factor=0.1 production_speed_synthetic_refinery_factor=0.1
- `hos_war_criminal` - stab=-0.1 war_stability_factor=0.15
- `hos_champion_democracy` - stab=0.1 industrial_capacity_factory=0.025 society_development_monthly=0.01
- `hos_Starhawk` - party_popularity_stability_factor=0.1 local_non_core_manpower=0.05
- `hos_Indecisive_Leader` - pp=-0.2 stab=-0.1
- `hos_decisive_politician` - production_speed_buildings_factor=0.05 personal_expense_factor=-0.1
- `hos_respected_general` - war_stability_factor=0.15 army_defence_factor=0.05
- `hos_soldier_of_the_revolution` - war_stability_factor=0.1 army_attack_factor=0.05 army_defence_factor=0.05
- `hos_grandmaster` - war_stability_factor=0.1 ws=0.1
- `hos_experienced_lawyer` - foreign_minister_cost_factor=-0.2 economic_minister_cost_factor=-0.2 interior_minister_cost_factor=-0.2 intelligence_minister_cost_factor=-0.2 theorist_minister_cost_factor=-0.2
- `hos_the_final_revolutionary` - war_stability_factor=0.1
- `hos_the_final_revolutionary1` - name=hos_the_final_revolutionary war_stability_factor=0.1 command_power_gain_mult=0.1
- `hos_Failed_Diplomat` - opinion_gain_monthly_factor=-0.25 guarantee_cost=0.5
- `hos_President_of_Congress` - conscription=0.02 max_command_power=25 consumer_goods_factor=-0.05
- `hos_godfather_of_accelerationism` - conscription_factor=0.05 consumer_goods_factor=-0.15 poverty_development_monthly=-0.01
- `hos_enlightened_gentleman` - political_power_factor=-0.05 drift_defence_factor=-0.1 consumer_goods_factor=-0.05 production_factory_efficiency_gain_factor=0.05 opinion_gain_monthly_factor=0.05
- `hos_desire_rise` - stab=-0.1 ws=0.1 army_attack_against_major_factor=0.05 army_attack_factor=0.05 command_power_gain_mult=0.25
- `hos_star_of_chinese_perestroika` - social_democrat_acceptance=15 drift_defence_factor=-0.2 head_minister_cost_factor=-0.25 foreign_minister_cost_factor=-0.25 economic_minister_cost_factor=-0.25
- `hos_the_new_deng_xiaoping` - communist_drift=0.03 ws=0.1 defensive_war_stability_factor=0.1 economy_cost_factor=-0.25
- `hos_hopeful_reformer` - pp=0.1 stab=0.05
- `hos_determined_reformer` - pp=0.25 stab=0.1
- `hos_harbringer_of_the_apocalypse` - conscription_factor=0.1 army_attack_factor=0.1 army_defence_factor=0.1
- `hos_heir_of_great_dynasties` - pp=0.15 stab=0.05 ws=0.05 war_stability_factor=0.075 society_development_monthly=0.01
- `hos_grand_preceptor` - political_power_factor=-0.1 stab=0.05 army_morale_factor=0.035 army_org_factor=0.05 society_development_monthly=0.01
- `hos_puppeteer_of_all_asia` - operation_cost=-0.25 personal_expense_factor=0.035 political_power_factor=0.05 society_development_monthly=0.01 academic_development_monthly=0.01
- `hos_harbringer_of_the_second_coming` - army_org_factor=0.1
- `hos_harbringer_of_the_apocalypse` - conscription_factor=0.1 army_attack_factor=0.1 army_defence_factor=0.1
- `hos_madam_president` - power_balance_weekly=-0.02 stab=-0.05 drift_defence_factor=0.5 pp=-0.1 army_attack_against_minor_factor=0.15
- `hos_hope_is_back` - army_attack_against_major_factor=0.2 stab=0.2 ws=0.2 pp=0.25 power_balance_weekly=0.05
- `hos_under_house_arrest` - stab=-0.15 ws=-0.15 political_power_factor=-0.5
- `hos_political_opportunist` - river_crossing_factor=-0.25 pp=0.15 ai_focus_defense_factor=0.25
- `hos_cowed_by_technocrats` - ws=-0.05 pp=-0.15
- `hos_imperial_president` - stab=0.05 ws=0.05 party_popularity_stability_factor=0.05 conservative_drift=0.05 political_power_factor=-0.05

**страновые и прочие** (130):

- `hog_god_machine` - stab=0.15 ws=0.15 stability_weekly=0.01 offensive_war_stability_factor=0.1 production_speed_industrial_complex_factor=0.1
- `hog_the_second_patriach` - stab=0.05 offensive_war_stability_factor=0.1 ai_focus_aggressive_factor=0.1 ws=0.015 army_attack_factor=0.025
- `hog_grey_demiurge` - political_power_factor=0.05 stab=0.05 ws=0.015 army_org_factor=0.05 nationalist_drift=0.015
- `hog_guardian_of_faith` - stab=0.05 army_core_defence_factor=0.05 defensive_war_stability_factor=0.1 offensive_war_stability_factor=0.1 ai_focus_aggressive_factor=0.1
- `USC_hog_president_of_the_people` - stab=0.015 ws=0.015 army_defence_factor=0.025 production_speed_infrastructure_factor=0.05 production_speed_industrial_complex_factor=0.05
- `USC_hog_macho_man` - stab=-0.1 ws=0.05 army_org_factor=0.05 conscription_factor=0.005 army_core_defence_factor=0.025
- `USC_hog_vizier_of_capitalism` - industrial_capacity_factory=0.025 business_value_factor=0.15 tax_business_rate_factor=-0.1 income_growth_factor=0.1 initiative_factor=0.025
- `bdn_juliet` - stab=0.8
- `bdn_whisky` - ws=0.8
- `bdn_yankee` - army_core_defence_factor=0.2 army_core_attack_factor=0.2
- `bdn_echo` - pp=0.5
- `openly_gay` - party_popularity_stability_factor=-0.05 national_socialist_drift=-0.02 social_liberal_acceptance=5
- `emergency_powers_trait` - political_power_factor=0.5 stab=-0.1
- `FAF_imperator` - military_development_monthly=0.05 war_stability_factor=0.25 national_socialist_drift=0.02
- `FRA_Appeaser` - ws=-0.05 industrial_capacity_factory=0.05
- `FAF_King_of_France_trait` - pp=-0.15 party_popularity_stability_factor=0.15 ws=0.05
- `FAF_Emperor_of_all_Latins_trait` - pp=-0.3 party_popularity_stability_factor=0.3 ws=0.1
- `FAF_Augustus` - ws=0.15 offensive_war_stability_factor=0.15 ai_focus_aggressive_factor=0.4
- `FAF_The_General_trait` - pp=-0.05 ws=0.15 defensive_war_stability_factor=0.2 offensive_war_stability_factor=0.4
- `FRA_Jvpiter` - consumer_goods_factor=-0.1 ws=0.05 pp=-0.1 head_minister_cost_factor=-0.5 foreign_minister_cost_factor=-0.5
- `FRA_Revolutionary_Father` - stab=0.1
- `FRA_Failed_Revolutionary` - stability_weekly=0.005 pp=-0.25
- `FRA_Hands_off_Revolutionary` - stab=0.1
- `FRA_Progressive_Icon` - party_popularity_stability_factor=0.05 pp=0.25
- `FRA_SocDem_Strongman` - party_popularity_stability_factor=0.05 social_democrat_drift=0.01
- `FRA_Chairman_of_the_revolution` - party_popularity_stability_factor=0.1 economic_minister_cost_factor=-0.15 foreign_minister_cost_factor=-0.15 pp=0.075 drift_defence_factor=0.25
- `FRA_The_Resolute` - pp=0.075 army_attack_factor=0.05 army_defence_factor=0.05
- `hog_the_great_revolutionary_leader` - party_popularity_stability_factor=0.1 army_morale_factor=0.065 research_speed_factor=-0.05
- `Africa_Disgruntled_Despot` - stab=-0.05 ws=0.025 army_morale_factor=0.05
- `Africa_Colonial_Marionette` - pp=-0.025 stab=-0.05
- `IVO_Colonial_Centerpiece` - pp=0.05 stab=0.1 consumer_goods_factor=-0.1
- `Africa_Ambitious_Dictator` - resistance_damage_to_garrison=-0.25 foreign_subversive_activites=-0.3 non_core_manpower=0.02
- `trait_supreme_chancellor` - political_power_factor=0.25 weekly_casualties_war_support=0.001 party_popularity_stability_factor=0.1 ws=0.05 stab=0.05
- `trait_dictator_less_buff` - political_power_factor=0.05 weekly_casualties_war_support=0.001 party_popularity_stability_factor=0.03
- `trait_dictator` - political_power_factor=0.2 weekly_casualties_war_support=0.001 party_popularity_stability_factor=0.1 ws=0.05 army_core_attack_factor=0.05
- `hog_the_great_leader` - political_power_factor=0.15 weekly_casualties_war_support=0.005 party_popularity_stability_factor=0.1 ws=0.055 army_core_attack_factor=0.03
- `hog_leader_of_the_free_europe` - political_power_factor=0.025 weekly_casualties_war_support=0.005 army_core_defence_factor=0.03
- `trait_imperial_sovereign` - political_power_factor=0.15 weekly_casualties_war_support=0.001 party_popularity_stability_factor=0.1 ws=0.05 army_core_attack_factor=0.025
- `trait_guardian_of_the_orthodoxy` - political_power_factor=0.15 war_stability_factor=0.1 weekly_casualties_war_support=0.005 army_core_attack_factor=0.05
- `trait_protector_of_of_all_faiths` - political_power_factor=0.05 stab=0.1 non_core_manpower=0.05 army_core_defence_factor=0.05
- `trait_GER_revolutionary_helmsman` - political_power_factor=0.15 weekly_casualties_war_support=0.005 party_popularity_stability_factor=0.1 army_attack_against_major_factor=0.05 army_core_defence_factor=0.05
- `trait_victorious_marshal` - political_power_factor=0.1 ws=0.1 army_core_attack_factor=0.05 army_core_defence_factor=0.05
- `MRT_Anti_Imperialist_Ideologue` - improve_relations_maintain_cost_factor=-0.5 trade_opinion_factor=0.1 opinion_gain_monthly_same_ideology_factor=1 party_popularity_stability_factor=0.1 non_core_manpower=0.05
- `BEL_French_Seperatist` - trade_laws_cost_factor=-0.25 economy_cost_factor=-0.25
- `Occupational_Governor` - ws=0.1 drift_defence_factor=0.15
- `FRA_Controversial_Conservative` - stab=-0.05 ws=0.025 army_morale_factor=0.05
- `FRA_Cutthroat_Conquerant` - consumer_goods_factor=-0.125 production_speed_buildings_factor=-0.125
- `FRA_Military_Prey` - production_speed_arms_factory_factor=-0.04 production_factory_max_efficiency_factor=-0.03 ws=-0.02
- `USC_supreme_commander_and_chief` - pp=0.05 army_attack_factor=0.05 army_defence_factor=0.05 war_stability_factor=0.1
- `hog_tsar_president` - army_morale_factor=0.035 army_org_factor=0.05 war_stability_factor=0.05
- `hog_lion_of_russia` - army_attack_factor=0.025 army_defence_factor=0.025
- `CHI_hos_madam_president` - pp=0.02 stab=0.02 ws=0.05
- `hog_lord_regent` - pp=0.1 stab=-0.06 max_command_power_mult=0.25 army_attack_factor=0.05
- `bdn_articial_leadership` - pp=0.33 stab=-0.5 weekly_manpower=-1000 resistance_damage_to_garrison=-0.99 monthly_population=-3
- `bdn_common_sense` - production_factory_max_efficiency_factor=0.5 resistance_activity=-0.35 resistance_damage_to_garrison=-0.35 resistance_growth=-0.35
- `bdn_honest_abe` - stab=0.8 ws=0.8
- `bdn_macarthur` - army_attack_factor=0.25 army_defence_factor=0.25
- `USG_the_son` - ws=0.1 party_popularity_stability_factor=0.1 war_stability_factor=0.1
- `Fidesz_Inner_Circle` - local_resources_factor=0.05 consumer_goods_factor=-0.03
- `FRA_French_Puppet` - party_popularity_stability_factor=-0.15 max_command_power=25 local_resources_factor=0.05
- `GMA_Beacon_of_Neo_Ludditism` - nationalist_drift=0.15 local_resources_factor=-0.15 consumer_goods_factor=-0.1 non_core_manpower=0.05 ai_focus_aggressive_factor=0.5
- `LDS_The_Prophet` - nationalist_drift=0.15 local_resources_factor=0.2 consumer_goods_factor=-0.1 non_core_manpower=0.1 monthly_population=0.8
- `GMA_Forged_in_Neo_Ludditism` - nationalist_drift=0.2 local_resources_factor=-0.25 consumer_goods_factor=-0.1 non_core_manpower=0.1 ai_focus_aggressive_factor=0.5
- `GMA_Anarcho_Primitivist_Ideologue` - party_popularity_stability_factor=0.3 consumer_goods_factor=-0.2 terrain_penalty_reduction=0.2 ai_focus_peaceful_factor=0.5
- `GMA_Military_Practitioner` - supply_consumption_factor=-0.2 recon_factor=0.1 special_forces_cap=0.5 ai_focus_war_production_factor=0.25
- `GMA_Environmental_Opportunist` - river_crossing_factor=-0.25 pp=0.15 ai_focus_defense_factor=0.25
- `GMA_Kaczynskis_Successor` - stab=0.05 ws=0.05
- `GMA_President_Field_Marshal_CEO` - pp=0.15 stab=0.1 ws=0.1 army_morale_factor=0.05 mobilization_speed=0.05
- `GMA_Illegitimate_Successor` - stab=-0.05 ws=-0.05
- `CAC_Caesar_of_the_New_World` - army_morale_factor=0.05 ws=0.05 mobilization_speed=0.05
- `CAC_Caesar_of_the_New_World2` - army_morale_factor=0.07 ws=0.07 mobilization_speed=0.07
- `GMA_Credible_Alternative` - research_speed_factor=0.1 stability_weekly_factor=0.005 max_planning_factor=0.25
- `GMA_Bazooka_Jew` - training_time_army_factor=-0.25 army_attack_factor=0.05 weekly_manpower=500 compliance_growth_on_our_occupied_states=0.1
- `GMA_Chaotic_but_Free` - send_volunteer_divisions_required=-0.3 encryption_factor=-0.1 production_speed_buildings_factor=0.05
- `GMA_Neo_Constitutionalist` - guarantee_cost=0.5 lend_lease_tension=-0.25 pp=0.1 authoritarian_democrat_drift=0.15
- `GMA_Hamiltonian_Federalist` - max_command_power=25 pp=0.15 social_liberal_drift=0.15
- `GMA_GMAC_Defector` - ws=-0.1 no_supply_grace=180 libertarian_socialist_drift=0.15
- `GMA_Founder_of_the_Collective` - guarantee_cost=-0.5 stab=0.15 party_popularity_stability_factor=0.15 defensive_war_stability_factor=0.4 ws=0.1
- `GMA_Free_State_Leader` - stab=0.15 ws=0.1 market_liberal_drift=0.05 weekly_manpower=500
- `GMA_Soldier_of_the_Free_Market` - ws=0.1 army_morale_factor=0.05 training_time_army_factor=-0.25 army_attack_factor=0.1 authoritarian_democrat_drift=0.1
- `KAZ_Great_Batyr` - ws=0.1 enemy_operative_detection_chance_factor=0.1 acclimatization_hot_climate_gain_factor=0.15 intel_network_gain_factor=0.05 army_morale_factor=0.05
- `GER_hos_government_agenda` - custom_modifier_tooltip=GER_government_agenda_tooltip
- `HEZ_secretary_general_of_the_jihad_council` - pp=0.02 stab=0.05
- `PRC_new_great_helmsman_trait` - stab=0.025 ws=0.025 party_popularity_stability_factor=0.05 political_power_factor=-0.05 conscription_factor=0.025
- `PRC_the_god_emperor_of_china_trait` - stab=0.15 ws=0.15 party_popularity_stability_factor=0.25 army_attack_factor=0.075 army_morale_factor=0.075
- `PTF_Imperial_Presidency_trait` - stab=0.1 party_popularity_stability_factor=0.5
- `NSM_Imperial_Presidency_Trait` - stab=0.05 pp=0.1 war_stability_factor=0.05
- `NSM_The_Founding_Father_Trait` - party_popularity_stability_factor=0.15 military_development_monthly=0.05 national_socialist_drift=0.02 conscription_factor=0.035
- `NSM_Imperator_Trait` - military_development_monthly=0.05 pp=0.05 stab=0.05
- `NSM_top_of_the_pyramid_Trait` - national_socialist_drift=0.01 stab=0.025
- `NSM_motivating_idol_Trait` - national_socialist_drift=0.01 stab=0.025 pp=0.05 military_development_monthly=0.035 society_development_monthly=0.035
- `ATW_speaker_of_the_heavens_hos` - required_garrison_factor=-0.1
- `ATW_the_overman_hos` - army_advisor_cost_factor=-0.15 air_advisor_cost_factor=-0.15 navy_chief_cost_factor=-0.15
- `ATW_apostle_of_god_hos` - party_popularity_stability_factor=0.1 society_development_monthly=0.01
- `ATW_saint_hos` - pp=-0.1 party_popularity_stability_factor=0.25 society_development_monthly=0.01
- `ATW_disciple_hos` - pp=0.1 stab=0.1 war_stability_factor=0.1 society_development_monthly=0.01
- `FPR_poet_of_the_revolution` - stability_weekly=0.005 war_support_weekly=-0.002
- `FPR_regent_of_liberty` - command_power_gain_mult=0.05 ws=0.1 pp=0.025
- `FPR_protector_of_the_republic` - pp=0.1 ws=0.15
- `CHI_Taiwan_Junta_Fanatic` - army_attack_against_major_factor=0.05 army_core_defence_factor=0.1
- `USB_biden_1_off` - -
- `USB_biden_1_on` - pp=0.05 social_liberal_drift=0.01
- `USB_biden_2_off` - -
- `USB_biden_2_on` - war_stability_factor=0.1 ws=0.1
- `USB_biden_3_off` - -
- `USB_biden_3_on` - production_factory_efficiency_gain_factor=0.05 production_speed_buildings_factor=0.05
- `USB_hillary_1_off` - power_balance_weekly=-0.01
- `USB_hillary_1_on` - pp=0.15 social_liberal_drift=0.05
- `USB_hillary_2_off` - power_balance_weekly=-0.01
- `USB_hillary_2_on` - ws=0.1 social_liberal_drift=0.05
- `USB_hillary_3_off` - power_balance_weekly=-0.01
- `USB_hillary_3_on` - army_morale_factor=0.1 army_org_factor=0.1
- `USB_sanders_1_off` - -
- `USB_sanders_1_on` - production_factory_max_efficiency_factor=0.05 social_democrat_drift=0.05
- `USB_sanders_2_off` - -
- `USB_sanders_2_on` - pp=0.1 personal_expense_factor=0.05
- `USB_sanders_3_off` - -
- `USB_sanders_3_on` - personal_value_factor=0.1 poverty_development_monthly=0.01
- `USB_romney_1_off` - -
- `USB_romney_1_on` - production_speed_arms_factory_factor=0.15
- `USB_romney_2_off` - -
- `USB_romney_2_on` - pp=0.1 conservative_drift=0.05
- `USB_romney_3_off` - -
- `USB_romney_3_on` - army_core_defence_factor=0.05 army_chief_cost_factor=-0.1
- `USB_bloomberg_1_off` - -
- `USB_bloomberg_1_on` - party_popularity_stability_factor=0.2
- `USB_bloomberg_2_off` - -
- `USB_bloomberg_2_on` - business_value_factor=0.25 income_growth_factor=0.25
- `USB_bloomberg_3_off` - -
- `USB_bloomberg_3_on` - ws=0.15

### Военные советники (армия, авиация, флот, теоретик)

- **другие** (100): `directed_by_hideo_kojima`, `starring_kazuhira_miller`, `tired_old_man`, `mobile_warfare_expert`, `superior_firepower_expert`, `grand_battle_plan_expert`, `mass_assault_expert`, `dive_bomber`, `victory_through_airpower`, `close_air_support_proponent`, `assault_avaition`, `naval_aviation_pioneer`, `grand_fleet_proponent`, `submarine_specialist`, `army_entrenchment_1`, `army_entrenchment_2`, `army_entrenchment_3`, `army_armored_1`, `army_armored_2`, `army_armored_3`, `army_artillery_1`, `army_artillery_2`, `army_artillery_3`, `army_infantry_1`, `army_infantry_2`, `army_infantry_3`, `army_commando_1`, `army_commando_2`, `army_commando_3`, `army_cavalry_1`, `army_cavalry_2`, `army_cavalry_3`, `army_CombinedArms_1`, `army_CombinedArms_2`, `army_CombinedArms_3`, `army_regrouping_1`, `army_regrouping_2`, `army_regrouping_3`, `army_concealment_1`, `army_concealment_2`, `army_concealment_3`, `army_logistics_1`, `army_logistics_2`, `army_logistics_3`, `army_adaptibility_1`, `army_adaptibility_2`, `army_adaptibility_3`, `air_air_combat_training_1`, `air_air_combat_training_2`, `air_air_combat_training_3`, `air_naval_strike_1`, `air_naval_strike_2`, `air_naval_strike_3`, `air_bomber_interception_1`, `air_bomber_interception_2`, `air_bomber_interception_3`, `air_air_superiority_1`, `air_air_superiority_2`, `air_air_superiority_3`, `air_close_air_support_1`, `air_close_air_support_2`, `air_close_air_support_3`, `air_strategic_bombing_1`, `air_strategic_bombing_2`, `air_strategic_bombing_3`, `air_tactical_bombing_1`, `air_tactical_bombing_2`, `air_tactical_bombing_3`, `air_airborne_1`, `air_airborne_2`, `air_airborne_3`, `air_pilot_training_1`, `air_pilot_training_2`, `air_pilot_training_3`, `navy_anti_submarine_1`, `navy_anti_submarine_2`, `navy_anti_submarine_3`, `navy_naval_air_defense_1`, `navy_naval_air_defense_2`, `navy_naval_air_defense_3`, `navy_fleet_logistics_1`, `navy_fleet_logistics_2`, `navy_fleet_logistics_3`, `navy_amphibious_assault_1`, `navy_amphibious_assault_2`, `navy_amphibious_assault_3`, `navy_submarine_1`, `navy_submarine_2`, `navy_submarine_3`, `navy_capital_ship_1`, `navy_capital_ship_2`, `navy_capital_ship_3`, `navy_screen_1`, `navy_screen_2`, `navy_screen_3`, `navy_carrier_1`, `navy_carrier_2`, `navy_carrier_3`, `navy_TFR_amphibious_fleet_commander`, `navy_TFR_iron_cpt`
- **theorist** (8): `military_theorist`, `theorist_assymetrical_warfare_expert`, `theorist_cost_cutter`, `theorist_special_forces_expert`, `theorist_guerilla_warfare_expert`, `air_warfare_theorist`, `naval_theorist`, `blitzkrieg_theorist`
- **army_chief** (32): `army_chief_defensive_1`, `army_chief_defensive_2`, `army_chief_defensive_3`, `army_chief_offensive_1`, `army_chief_offensive_2`, `army_chief_offensive_3`, `army_chief_old_guard`, `army_chief_political_protege`, `army_chief_unity_of_party_and_military`, `army_chief_militarist_merc_boss`, `army_chief_drill_1`, `army_chief_drill_2`, `army_chief_drill_3`, `army_chief_reform_1`, `army_chief_reform_2`, `army_chief_reform_3`, `army_chief_organizational_1`, `army_chief_organizational_2`, `army_chief_organizational_3`, `army_chief_planning_1`, `army_chief_planning_2`, `army_chief_planning_3`, `army_chief_morale_1`, `army_chief_morale_2`, `army_chief_morale_3`, `army_chief_maneuver_1`, `army_chief_maneuver_2`, `army_chief_maneuver_3`, `army_chief_entrenchment_1`, `army_chief_entrenchment_2`, `army_chief_entrenchment_3`, `army_chief_shellfire_determine_victory`
- **air_chief** (16): `air_chief_reform_1`, `air_chief_reform_2`, `air_chief_reform_3`, `air_chief_safety_1`, `air_chief_safety_2`, `air_chief_safety_3`, `air_chief_old_guard`, `air_chief_night_operations_1`, `air_chief_night_operations_2`, `air_chief_night_operations_3`, `air_chief_ground_support_1`, `air_chief_ground_support_2`, `air_chief_ground_support_3`, `air_chief_all_weather_1`, `air_chief_all_weather_2`, `air_chief_all_weather_3`
- **navy_chief** (16): `navy_chief_naval_aviation_1`, `navy_chief_naval_aviation_2`, `navy_chief_naval_aviation_3`, `navy_chief_decisive_battle_1`, `navy_chief_decisive_battle_2`, `navy_chief_decisive_battle_3`, `navy_chief_commerce_raiding_1`, `navy_chief_commerce_raiding_2`, `navy_chief_commerce_raiding_3`, `navy_chief_old_guard`, `navy_chief_reform_1`, `navy_chief_reform_2`, `navy_chief_reform_3`, `navy_chief_maneuver_1`, `navy_chief_maneuver_2`, `navy_chief_maneuver_3`

У советников есть `command_cap_increase`, `experience_gain_*` и множество боевых модификаторов; значения - в самом файле референса.

### Черты компаний (производители техники)

36 черт: `aircraft_manufacturer`, `drone_aircraft_manufacturer`, `light_aircraft_manufacturer`, `light_aircraft_manufacturer_2`, `CAS_manufacturer`, `medium_aircraft_manufacturer`, `fuel_efficient_aircraft_manufacturer`, `heavy_aircraft_manufacturer`, `naval_aircraft_manufacturer`, `tank_refurbishment_plant`, `fast_tank_manufacturer`, `armored_car_manufacturer`, `infantry_tank_manufacturer`, `medium_tank_manufacturer`, `tankograd`, `heavy_tank_manufacturer`, `tank_manufacturer`, `repair_and_refurbishment_plant`, `black_sea_naval_manufacturer`, `pacific_fleet_naval_manufacturer`, `atlantic_fleet_naval_manufacturer`, `battlefleet_designer`, `raiding_fleet_naval_manufacturer`, `convoy_escort_naval_manufacturer`, `mediterranean_naval_manufacturer`, `coastal_defence_naval_manufacturer`, `naval_manufacturer`, `artillery_manufacturer`, `infantry_equipment_manufacturer`, `support_equipment_manufacturer`, `motorized_equipment_manufacturer`, `industrial_concern`, `railway_company`, `construction_company`, `refinery_concern`, `electronics_concern`

## 4. Словарь модификаторов (по идеям SOV)

Показаны ключи, встретившиеся минимум в 3 идеях; значения: минимум / медиана / максимум. Ключи вида `<идеология>_drift` (дрейф партии), `<идеология>_acceptance` (принятие идеологии, значения 25-50), `*_laws_cost_factor` (цена смены законов), `*_minister_cost_factor` (цена смены министров) - TFR-специфика.

| Ключ | Встреч | min | медиана | max | Заметка |
|---|---|---|---|---|---|
| `stability_factor` | 756 | -0.5 | 0.025 | 0.25 | стабильность (доля; 0.05 = 5%) |
| `consumer_goods_factor` | 565 | -0.15 | 0 | 0.7 | доля потребительских товаров |
| `personal_value_factor` | 417 | -0.5 | 0.05 | 0.5 | вклад личных расходов в ВВП (см. cheatsheet 9) |
| `society_development_monthly` | 411 | -0.1 | 0.01 | 0.05 | шкала «Общество» за месяц |
| `business_value_factor` | 396 | -0.5 | 0.025 | 0.5 | вклад бизнеса в ВВП |
| `production_factory_efficiency_gain_factor` | 395 | -0.5 | 0.035 | 0.2 |  |
| `political_power_gain` | 376 | -0.65 | 0.025 | 0.75 | прирост политсилы |
| `income_growth_factor` | 364 | -0.5 | 0.02 | 0.3 | рост доходов |
| `war_support_factor` | 349 | -0.45 | 0.05 | 0.25 | поддержка войны |
| `industrial_capacity_factory` | 339 | -0.5 | 0.05 | 0.9 |  |
| `production_speed_buildings_factor` | 326 | -0.5 | 0.05 | 0.9 |  |
| `political_power_factor` | 289 | -0.5 | -0.03 | 0.5 | множитель политсилы |
| `poverty_development_monthly` | 288 | -0.1 | 0.005 | 0.15 | шкала соцзащиты за месяц (плюс = лучше) |
| `production_factory_max_efficiency_factor` | 283 | -0.5 | 0.05 | 0.3 |  |
| `industrial_development_monthly` | 266 | -0.1 | 0.005 | 0.15 | шкала промышленности за месяц |
| `production_factory_start_efficiency_factor` | 216 | -0.5 | 0.025 | 0.2 |  |
| `army_morale_factor` | 170 | -0.05 | 0.0475 | 0.3 |  |
| `research_speed_factor` | 169 | -0.1 | 0 | 0.3 |  |
| `production_lack_of_resource_penalty_factor` | 159 | -0.2 | 0 | 0.35 |  |
| `production_speed_arms_factory_factor` | 156 | -0.1 | 0 | 0.25 |  |
| `production_speed_industrial_complex_factor` | 149 | -0.15 | 0 | 0.2 |  |
| `army_attack_factor` | 138 | -0.25 | 0.05 | 0.25 |  |
| `conscription_factor` | 136 | -0.5 | 0.02 | 0.35 | множитель призыва |
| `army_org_factor` | 125 | -0.5 | 0.04 | 0.3 |  |
| `local_resources_factor` | 120 | -0.075 | 0 | 0.25 |  |
| `production_speed_office_park_factor` | 119 | -0.2 | 0 | 0.25 |  |
| `military_development_monthly` | 111 | -0.03 | 0.01 | 0.05 | военная шкала за месяц |
| `war_stability_factor` | 110 | -0.1 | 0.05 | 0.3 |  |
| `political_power_cost` | 107 | -0.25 | 0.03 | 0.4 |  |
| `personal_expense_factor` | 107 | -0.35 | 0.03 | 0.5 |  |
| `academic_development_monthly` | 96 | -0.06 | 0.005 | 0.05 | шкала науки за месяц |
| `trade_opinion_factor` | 93 | -0.1 | 0 | 0.25 |  |
| `fascist_drift` | 91 | -0.1 | 0.01 | 0.05 |  |
| `production_speed_infrastructure_factor` | 85 | 0 | 0.05 | 0.25 |  |
| `dtg_threshold` | 84 | 0 | 0 | 0.25 | порог, растёт с уровнем «Общество» (0.3 -> 1.05); смысл [ПРОВЕРИТЬ] |
| `army_defence_factor` | 83 | -0.25 | 0.05 | 0.2 |  |
| `farming_development_monthly` | 81 | 0 | 0 | 0.02 | шкала сельхоза за месяц |
| `authoritarian_democrat_drift` | 80 | -0.1 | 0.02 | 0.15 |  |
| `compliance_growth` | 79 | -0.15 | 0.05 | 0.3 | рост лояльности в оккупации |
| `monthly_population` | 77 | -0.75 | 0 | 0.5 | прирост населения |
| `party_popularity_stability_factor` | 76 | -0.25 | 0.05 | 0.55 | стабильность от популярности правящей партии |
| `mobilization_speed` | 71 | -0.5 | 0.05 | 0.25 |  |
| `social_liberal_drift` | 70 | -0.1 | 0.015 | 0.15 |  |
| `army_core_defence_factor` | 69 | -0.035 | 0.05 | 0.3 |  |
| `conservative_drift` | 64 | -0.1 | 0.0175 | 0.075 |  |
| `drift_defence_factor` | 63 | -0.75 | 0.05 | 0.5 | защита от дрейфа идеологий |
| `social_democrat_drift` | 60 | -0.05 | 0.02 | 0.2 |  |
| `initiative_factor` | 60 | -0.1 | 0.05 | 0.15 | инициатива |
| `battalion_upkeep_factor` | 59 | -0.25 | -0.05 | 0.5 |  |
| `expense_growth_factor` | 55 | -0.15 | 0.05 | 0.2 |  |
| `industrial_capacity_dockyard` | 54 | -0.5 | 0.05 | 0.9 |  |
| `communist_drift` | 53 | -0.15 | 0.01 | 0.15 |  |
| `libertarian_socialist_drift` | 48 | -0.15 | 0.01 | 0.2 |  |
| `breakthrough_factor` | 47 | -0.2 | 0.05 | 0.15 |  |
| `resistance_growth` | 47 | -0.25 | -0.025 | 0.25 | рост сопротивления в оккупации |
| `army_org_regain` | 46 | -0.05 | 0.05 | 0.15 |  |
| `planning_speed` | 38 | -0.15 | 0.1 | 0.3 |  |
| `resistance_decay` | 37 | -0.15 | 0.1 | 0.25 | спад сопротивления |
| `totalitarian_socialist_drift` | 37 | -0.15 | 0.02 | 0.1 |  |
| `army_core_attack_factor` | 36 | -0.05 | 0.05 | 0.2 |  |
| `misc_expense` | 34 | -0.12 | 15 | 50 | постоянный расход, млрд |
| `training_time_factor` | 31 | -0.25 | -0.1 | 5 |  |
| `production_cost_infrastructure_factor` | 30 | -0.15 | -0.005 | 0.15 |  |
| `nationalist_drift` | 29 | -0.1 | 0.03 | 0.1 |  |
| `army_speed_factor` | 29 | -0.15 | 0.035 | 0.15 |  |
| `global_building_slots_factor` | 29 | 0.025 | 0.1 | 0.15 |  |
| `military_factory_upkeep_factor` | 28 | -0.3 | -0.1 | 0.13 |  |
| `interest_rate_factor` | 28 | -0.33 | -0.035 | 0.15 | процентная ставка |
| `conscription` | 27 | -0.1 | -0.0025 | 0.05 | доля призыва (населения) |
| `stability_weekly` | 27 | -0.02 | 0.002 | 0.03 |  |
| `tax_business_rate` | 27 | -0.55 | -0.1 | 0.35 |  |
| `market_liberal_drift` | 26 | -0.2 | 0.01 | 0.1 |  |
| `weekly_manpower` | 26 | -550 | 65 | 750 | живая сила в неделю |
| `production_speed_synthetic_refinery_factor` | 25 | 0.025 | 0.05 | 0.15 |  |
| `army_strength_factor` | 24 | -0.15 | 0.05 | 0.1 |  |
| `army_breakthrough_against_major_factor` | 24 | -0.1 | 0.05 | 0.15 |  |
| `non_core_manpower` | 24 | -0.99 | 0.05 | 0.35 |  |
| `usual_oligarch_influence_monthly` | 23 | -0.01 | 0 | 0.02 | SOV: влияние олигархов (механика России) |
| `experience_gain_army_factor` | 23 | -0.5 | 0.05 | 0.15 |  |
| `root_out_resistance_effectiveness_factor` | 23 | -0.1 | 0.06 | 0.5 |  |
| `tax_business_rate_factor` | 22 | -0.3 | 0 | 0.15 |  |
| `army_attack_against_major_factor` | 22 | 0.015 | 0.085 | 0.15 |  |
| `resistance_target` | 22 | -0.15 | 0.1 | 0.2 |  |
| `army_defence_against_major_factor` | 21 | 0.015 | 0.05 | 0.15 |  |
| `war_support_weekly` | 21 | -0.005 | 0.005 | 0.035 |  |
| `production_speed_nuclear_reactor_factor` | 21 | 0 | 0 | 0.15 |  |
| `aircraft_upkeep_factor` | 21 | -0.25 | -0.05 | 0.5 |  |
| `compliance_gain` | 20 | -0.15 | 0.0325 | 0.1 |  |
| `inflation_monthly` | 20 | -0.15 | -0.001 | 0.5 | инфляция за месяц |
| `max_planning_factor` | 20 | -0.5 | 0.075 | 0.25 |  |
| `production_speed_supply_node_factor` | 19 | 0.03 | 0.05 | 0.25 |  |
| `army_breakthrough_against_minor_factor` | 19 | 0.025 | 0.05 | 0.15 |  |
| `army_attack_speed_factor` | 19 | -0.2 | 0.05 | 0.3 |  |
| `economy_cost_factor` | 19 | -0.5 | -0.15 | 0.35 |  |
| `production_speed_bunker_factor` | 19 | -0.1 | 0.1 | 0.25 |  |
| `production_oil_factor` | 18 | -0.1 | 0.05 | 0.12 |  |
| `coordination_bonus` | 18 | -0.1 | 0.05 | 0.2 |  |
| `production_cost_industrial_complex_factor` | 18 | -0.2 | 0.0425 | 0.1 |  |
| `resistance_activity` | 18 | -0.5 | -0.15 | 0.1 |  |
| `national_socialist_drift` | 18 | -0.01 | 0.02 | 0.06 |  |
| `ship_upkeep_factor` | 18 | -0.25 | -0.075 | 0.5 |  |
| `line_change_production_efficiency_factor` | 17 | 0.03 | 0.1 | 0.2 |  |
| `economic_minister_cost_factor` | 17 | -0.5 | -0.1 | -0.05 |  |
| `dig_in_speed_factor` | 15 | -0.05 | 0.05 | 0.15 |  |
| `cic_to_overlord_factor` | 15 | -0.05 | 0.25 | 0.5 |  |
| `mic_to_overlord_factor` | 15 | -0.05 | 0.25 | 0.5 |  |
| `experience_loss_factor` | 14 | -0.15 | 0.05 | 0.1 |  |
| `supply_consumption_factor` | 13 | -0.15 | 0.025 | 0.1 |  |
| `offensive_war_stability_factor` | 13 | 0.01 | 0.05 | 0.15 |  |
| `interior_minister_cost_factor` | 13 | -0.15 | -0.1 | -0.05 |  |
| `intel_network_gain_factor` | 13 | -0.15 | 0.085 | 0.15 |  |
| `defensive_war_stability_factor` | 12 | 0.03 | 0.1 | 0.15 |  |
| `production_speed_rail_way_factor` | 12 | 0.025 | 0.09 | 0.25 |  |
| `cat_old_land_doctrine_cost_factor` | 12 | -0.15 | -0.05 | 0.25 |  |
| `mobilization_laws_cost_factor` | 12 | -0.5 | -0.2 | -0.1 |  |
| `immigration_laws_cost_factor` | 12 | -0.5 | -0.125 | -0.02 |  |
| `production_speed_fuel_silo_factor` | 12 | 0.015 | 0.075 | 0.25 |  |
| `misc_income` | 11 | 0.25 | 15 | 50 | постоянный доход, млрд |
| `org_loss_when_moving` | 11 | -0.15 | -0.05 | 0.05 |  |
| `decryption` | 11 | 0.5 | 1.5 | 3 |  |
| `inflation_monthly_factor` | 10 | -0.1 | 0 | 0.05 |  |
| `dockyard_upkeep_factor` | 10 | -0.3 | -0.125 | 0.1 |  |
| `supply_factor` | 10 | -0.075 | 0.05 | 0.05 |  |
| `army_fuel_consumption_factor` | 10 | -0.06 | 0.05 | 0.15 |  |
| `max_dig_in_factor` | 10 | 0.025 | 0.0325 | 0.15 |  |
| `tax_personal_rate` | 10 | -0.1 | 0.1 | 0.25 |  |
| `production_speed_air_base_factor` | 10 | 0.03 | 0.2 | 0.25 |  |
| `production_speed_radar_station_factor` | 10 | 0.05 | 0.125 | 0.25 |  |
| `industry_free_repair_factor` | 10 | 0.05 | 0.1 | 0.15 |  |
| `welfare_laws_cost_factor` | 10 | -0.25 | -0.15 | 0.1 |  |
| `encryption` | 10 | 0.5 | 1.25 | 2.5 |  |
| `production_speed_anti_air_building_factor` | 10 | 0.05 | 0.2 | 0.25 |  |
| `combat_width_factor` | 9 | -0.1 | -0.05 | -0.025 |  |
| `supply_node_range` | 9 | 0.025 | 0.05 | 0.15 |  |
| `terrain_penalty_reduction` | 9 | -0.05 | 0.1 | 0.5 |  |
| `resistance_damage_to_garrison` | 9 | -0.2 | -0.1 | 0.15 |  |
| `supply_combat_penalties_on_core_factor` | 9 | -0.25 | -0.15 | -0.1 |  |
| `extra_trade_to_overlord_factor` | 9 | 0.2 | 0.3 | 0.5 |  |
| `autonomy_manpower_share` | 9 | -0.3 | 0.15 | 0.5 |  |
| `opinion_gain_monthly_same_ideology_factor` | 9 | 0.01 | 0.1 | 0.3 |  |
| `resistance_growth_on_our_occupied_states` | 9 | 0.05 | 0.1 | 0.15 |  |
| `production_speed_dockyard_factor` | 9 | 0.035 | 0.15 | 0.25 |  |
| `education_laws_cost_factor` | 9 | -0.35 | -0.1 | -0.02 |  |
| `unit_upkeep_attrition_factor` | 8 | -0.15 | -0.0875 | -0.05 |  |
| `oligarch_influence_monthly` | 8 | -0.03 | 0.01 | 0.02 | SOV: влияние олигархов (механика России) |
| `conversion_cost_civ_to_mil_factor` | 8 | -0.25 | 0.075 | 0.1 |  |
| `out_of_supply_factor` | 8 | -0.1 | -0.0625 | -0.025 |  |
| `experience_gain_army_unit_factor` | 8 | -0.1 | 0.075 | 0.15 |  |
| `overlord_trade_cost_factor` | 8 | -0.3 | -0.175 | 0.05 |  |
| `agency_upgrade_time` | 8 | -0.25 | -0.1125 | -0.05 |  |
| `enemy_operative_detection_chance_factor` | 8 | 0.035 | 0.1 | 0.15 |  |
| `special_forces_cap` | 7 | -0.15 | 0.15 | 0.25 |  |
| `required_garrison_factor` | 7 | -0.3 | -0.1 | -0.05 |  |
| `military_leader_cost_factor` | 7 | -0.3 | -0.25 | -0.1 |  |
| `grant_medal_cost_factor` | 7 | -0.5 | -0.15 | 0.1 |  |
| `min_export` | 7 | -0.15 | -0.1 | 0.2 |  |
| `recon_factor` | 7 | 0.025 | 0.1 | 0.15 |  |
| `military_factory_upkeep` | 7 | -0.05 | 0.2 | 0.5 |  |
| `tax_personal_rate_factor` | 7 | -0.1 | -0.1 | -0.05 |  |
| `lend_lease_tension` | 7 | -0.1 | -0.05 | -0.01 |  |
| `trade_cost_for_target_factor` | 7 | -0.1 | -0.02 | -0.01 |  |
| `tax_laws_cost_factor` | 7 | -0.5 | -0.15 | 0.5 |  |
| `female_laws_cost_factor` | 7 | -0.35 | -0.1 | -0.1 |  |
| `prison_laws_cost_factor` | 7 | -0.35 | -0.1 | -0.1 |  |
| `production_speed_naval_base_factor` | 7 | 0.05 | 0.25 | 0.25 |  |
| `experience_gain_army` | 6 | 0.05 | 0.05 | 0.15 |  |
| `surrender_limit` | 6 | -0.25 | 0.1 | 0.15 |  |
| `recruitable_population` | 6 | 0.015 | 0.03 | 0.1 |  |
| `army_org` | 6 | -3 | 2.5 | 8 |  |
| `trade_laws_cost_factor` | 6 | -0.5 | -0.2 | -0.05 |  |
| `max_command_power` | 5 | -25 | 25 | 25 |  |
| `send_volunteers_tension` | 5 | -0.05 | -0.01 | -0.01 |  |
| `base_fuel_gain_factor` | 5 | -0.15 | -0.05 | 0.15 |  |
| `libertarian_socialist_acceptance` | 5 | -50 | -25 | 25 |  |
| `social_democrat_acceptance` | 5 | 25 | 45 | 45 |  |
| `theorist_minister_cost_factor` | 5 | -0.15 | -0.1 | -0.1 |  |
| `army_bonus_air_superiority_factor` | 5 | 0.025 | 0.1 | 0.15 |  |
| `intelligence_minister_cost_factor` | 5 | -0.15 | -0.1 | -0.05 |  |
| `foreign_minister_cost_factor` | 5 | -0.15 | -0.1 | -0.05 |  |
| `enemy_operative_intel_extraction_rate` | 5 | 0.035 | 0.1 | 0.15 |  |
| `police_laws_cost_factor` | 5 | -0.35 | -0.35 | -0.1 |  |
| `production_speed_coastal_bunker_factor` | 5 | 0.045 | 0.15 | 0.25 |  |
| `industry_repair_factor` | 4 | 0.015 | 0.035 | 0.1 |  |
| `factory_energy_consumption` | 4 | -0.2 | -0.125 | -0.05 |  |
| `land_reinforce_rate` | 4 | 0.05 | 0.075 | 0.1 |  |
| `send_volunteer_size` | 4 | -9 | -3 | 3 |  |
| `dtg_threshold_factor` | 4 | 0.02 | 0.02 | 0.1 |  |
| `red_directors_influence_monthly` | 4 | -0.03 | 0 | 0.02 | SOV: влияние «красных директоров» |
| `operative_slot` | 4 | 1 | 1 | 1 |  |
| `ai_focus_aviation_factor` | 3 | 0.1 | 0.15 | 0.2 |  |
| `ai_focus_war_production_factor` | 3 | 0.1 | 0.15 | 0.2 |  |
| `ai_desired_divisions_factor` | 3 | 1 | 2 | 3 |  |
| `civilian_intel_to_others` | 3 | -25 | -0.25 | -0.15 |  |
| `army_intel_to_others` | 3 | -15 | -0.15 | -0.05 |  |
| `recruitable_population_factor` | 3 | 0.01 | 0.01 | 0.1 |  |
| `local_building_slots` | 3 | -2 | -1 | -1 |  |
| `state_production_speed_buildings_factor` | 3 | 0.015 | 0.025 | 0.05 |  |
| `fuel_gain_factor` | 3 | 0.05 | 0.1 | 25 |  |
| `training_laws_cost_factor` | 3 | -0.35 | -0.25 | -0.15 |  |
| `repair_speed_infrastructure_factor` | 3 | 0.1 | 0.1 | 0.1 |  |
| `social_liberal_acceptance` | 3 | 25 | 25 | 25 |  |
| `personal_expense` | 3 | -0.15 | -0.1 | -0.03 |  |
| `race_laws_cost_factor` | 3 | -0.5 | -0.5 | -0.35 |  |
| `crypto_strength` | 3 | 2.5 | 15 | 25 |  |
| `decryption_power` | 3 | 3.5 | 15 | 25 |  |
| `intelligence_agency_defense` | 3 | 0.1 | 0.1 | 0.1 |  |
| `enemy_operative_forced_into_hiding_time_factor` | 3 | 0.1 | 0.1 | 0.1 |  |
| `operation_cost` | 3 | -0.15 | -0.15 | -0.15 |  |
| `autonomy_gain` | 3 | -0.01 | -0.01 | -0.01 |  |
| `peoples_entrepreneurs_influence_monthly` | 3 | -0.01 | 0.01 | 0.02 | SOV: влияние народных предпринимателей |

Редкие ключи (1-2 раза): `MONTHLY_POPULATION`, `acclimatization_cold_climate_gain_factor`, `ai_focus_defense_factor`, `air_accidents_factor`, `air_agility_factor`, `air_attack_factor`, `air_bombing_targetting`, `air_cas_present_factor`, `air_defence_factor`, `air_home_defence_factor`, `air_interception_detect_factor`, `air_manpower_requirement_factor`, `air_mission_efficiency`, `air_night_penalty`, `air_strategic_bomber_bombing_factor`, `air_strategic_bomber_night_penalty`, `air_superiority_bonus_in_combat`, `air_superiority_efficiency`, `air_volunteer_cap`, `army_defense_against_major_factor`, `army_leader_start_planning_level`, `authoritarian_democrat_acceptance`, `can_master_build_for_us`, `cas_damage_reduction`, `cat_old_air_doctrine_cost_factor`, `command_abilities_cost_factor`, `communist_acceptance`, `conversion_cost_mil_to_civ_factor`, `custom_modifier_tooltip`, `disabled_ideas`, `draft_exemption_laws_cost_factor`, `experience_gain_factor`, `fortification_damage`, `generate_wargoal_tension`, `ground_attack_factor`, `industry_air_damage_factor`, `justify_war_goal_time`, `land_night_attack`, `local_factory_sabotage`, `local_manpower`, `local_non_core_manpower`, `local_non_core_supply_impact_factor`, `local_org_regain`, `local_supplies`, `master_ideology_drift`, `max_fuel_factor`, `max_training`, `military_industrial_organization_design_team_change_cost`, `military_industrial_organization_funds_gain`, `military_industrial_organization_policy_cooldown`, `military_industrial_organization_research_bonus`, `minimum_training_level`, `navy_intel_to_others`, `org_loss_at_low_org_factor`, `pocket_penalty`, `power_balance_weekly`, `production_speed_energy_farm_factor`, `production_speed_power_plant_factor`, `repair_speed_industrial_complex_factor`, `resistance_decay_on_our_occupied_states`, `resistance_target_on_our_occupied_states`, `safety_laws_cost_factor`, `send_volunteer_factor`, `state_resources_factor`, `subjects_autonomy_gain`, `supervision_laws_cost_factor`, `totalitarian_socialist_acceptance`, `truck_attrition_factor`, `unit_mechanized_design_cost_factor`, `unit_modern_armor_design_cost_factor`, `weekly_bombing_war_support`, `weekly_casualties_war_support`.

## 5. Деревья фокусов в референсах: размеры и стоимости

| Файл | Дерево (id) | Фокусов | Самая частая cost |
|---|---|---|---|
| `FRA` | `FRA_initial_tree` | 205 | 5 x171, 3 x19, 2 x4 |
| `GER` | `GER_tree_initial` | 163 | 5 x154, 4 x9 |
| `SOV` | `SOV` | 80 | 4 x60, 5 x7, 6 x6 |
| `SOV_communist_new` | `SOV_communist` | 327 | 5 x197, 3.58 x45, 3 x43 |
| `SOV_dugin` | `SOV_dugin_tree` | 69 | 5 x67, 7.2 x1, 2.2 x1 |
| `SOV_fascist` | `SOV_ldpr_gaming` | 449 | 5 x270, 6 x92, 4 x64 |
| `SOV_medvedev` | `SOV_medvedev` | 654 | 5 x244, 4 x164, 3 x141 |
| `SOV_navalny` | `SOV_navalny_tree` | 9 | 2 x9 |
| `SOV_navalny` | `SOV_navalny_nato_war_tree` | 71 | 5 x28, 4 x26, 2 x13 |
| `SOV_wagner` | `SOV_wagner_tree` | 47 | 5 x39, 4 x3, 7.2 x2 |

## 6. Фильтры фокусов (`search_filters`)

Все встречающиеся в референсах: `FOCUS_FILTER_AIR_XP`, `FOCUS_FILTER_ANNEXATION`, `FOCUS_FILTER_ARMY_XP`, `FOCUS_FILTER_BALANCE_OF_POWER`, `FOCUS_FILTER_INDUSTRY`, `FOCUS_FILTER_INTERNAL_AFFAIRS`, `FOCUS_FILTER_INTERNATIONAL_TRADE`, `FOCUS_FILTER_MANPOWER`, `FOCUS_FILTER_MILITARY_CHARACTER`, `FOCUS_FILTER_NATO_LEADERSHIP`, `FOCUS_FILTER_NAVY_XP`, `FOCUS_FILTER_POLITICAL`, `FOCUS_FILTER_POLITICAL_CHARACTER`, `FOCUS_FILTER_PROPAGANDA`, `FOCUS_FILTER_RESEARCH`, `FOCUS_FILTER_STABILITY`, `FOCUS_FILTER_USA_CONGRESS`, `FOCUS_FILTER_WAR_SUPPORT`.

Использованы в фокусах: `FOCUS_FILTER_POLITICAL` x33, `FOCUS_FILTER_INDUSTRY` x23, `FOCUS_FILTER_NATO_LEADERSHIP` x3, `FOCUS_FILTER_RESEARCH` x3, `FOCUS_FILTER_MANPOWER` x3, `FOCUS_FILTER_ANNEXATION` x2, `FOCUS_FILTER_PROPAGANDA` x1. Фильтры нужны только для поиска по дереву; у большинства фокусов TFR их нет.

## 7. Типы зданий (`buildings`)

Допустимые значения `type =` в `add_building_construction` / `add_offsite_building`. `base_cost` - стоимость уровня в единицах производства стройки (больше = дольше).

| Здание | base_cost | на уровень + | Заметка |
|---|---|---|---|
| `landmark_big_ben` | 20000 |  | не строится, достопримечательность |
| `landmark_colosseum` | 20000 |  | не строится, достопримечательность |
| `landmark_cristo_redentor` | 20000 |  | не строится, достопримечательность |
| `landmark_eiffel_tower` | 20000 |  | не строится, достопримечательность |
| `landmark_statue_of_liberty` | 20000 |  | не строится, достопримечательность |
| `landmark_kremlin` | 20000 |  | не строится, достопримечательность |
| `landmark_hofburg_palace` | 20000 |  | не строится, достопримечательность |
| `landmark_berlin_reichstag` | 20000 |  | не строится, достопримечательность |
| `landmark_berlin_volkshalle` | 20000 |  | не строится, достопримечательность |
| `infrastructure` | 9000 | 900 |  |
| `arms_factory` | 13500 | 1350 |  |
| `industrial_complex` | 18900 | 1890 |  |
| `dockyard` | 13500 | 1350 | только побережье |
| `office_park` | 10800 | 1080 |  |
| `air_base` | 3750 | 375 |  |
| `supply_node` | 16200 |  |  |
| `rail_way` | 600 | 120 |  |
| `naval_base` | 4500 | 450 | только побережье |
| `bunker` | 1400 | 700 |  |
| `coastal_bunker` | 1400 | 700 | только побережье |
| `anti_air_building` | 2500 | 250 |  |
| `synthetic_refinery` | 14500 | 1450 |  |
| `fuel_silo` | 7500 | -500 |  |
| `radar_station` | 4000 | 400 |  |
| `mega_gun_emplacement` | 20000 |  |  |
| `rocket_site` | 2000 | 500 |  |
| `nuclear_reactor` | 54000 | 13500 |  |
| `power_plant` | 10800 | 1080 |  |
| `energy_farm` | 16200 | 1620 |  |
| `dam` | 20000 |  | не строится |
| `dam_mountain` | 20000 |  | не строится |

