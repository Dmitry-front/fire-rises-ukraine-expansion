# PROPOSAL: украинские концерны (MIO) и окно «Оборонная промышленность»

**Статус:** проект на утверждение (10.10.2026). Кода и ID в реестре пока нет.
**Источники:** присланные автором файлы TFR `00_generic_organization.txt`, `00_DEBUG_organization.txt`, `TFR_organizations_SOV.txt`, `_template_organization.txt`; референсы `_referenceTFR_decisions_SOV.txt` (стр. 28880-28913), `_referenceTFR_ideas_SOV.txt` (бонусы `equipment_bonus`), `_referenceTFR_national_focus_FRA.txt` (`mio:` и `add_mio_*`). Факты о реальных заводах писались по памяти: **[ПРОВЕРИТЬ]**.

## 1. Как устроено в TFR (по присланным файлам)

- Организация (MIO) - это блок в `common/military_industrial_organization/organizations/*.txt`. У SOV: `include = <архетип>`, свой `icon`, `allowed = { original_tag = SOV }` (у большинства ещё `has_dlc = "Arms Against Tyranny"`), при желании свой `initial_trait`, `override_trait` (сдвиг черты), новые `tree_header_text`.
- Архетипы в `00_generic_organization.txt` помечены `allowed = { always = no }`: игре нужны только как шаблоны.
- **Не закомментированные архетипы (подтверждены):** `generic_infantry_tank`, `mobile_tank`, `medium_tank`, `heavy_tank`, `tank_refurbishment_plant`, `battle_line_ship_DDG`, `submarine`, `black_sea_fleet`, `refurbishment_repair`, `light_aircraft`, `medium_aircraft`, `heavy_aircraft`, `cas_aircraft`, `naval_aircraft`, `multi_role_aircraft`, `high_agility_fighter_aircraft`, `range_focused_aircraft`, `armored_car` (нужен DLC La Resistance), **`generic_TFR_UAV_equipment_organization`** (черты БПЛА и крылатой ракеты, TFR-овский).
- **Закомментированы в присланном файле** (но SOV их `include`-ит, значит они определены в другом файле TFR): `tank`, `task_force_ship`, `escort_ship`, `general_aircraft`, `artillery`, `infantry_equipment`, `support_equipment`, `motorized_mechanized`.
- Награды и усиления: `mio:ID = { add_mio_funds = N add_mio_size = 1 add_mio_research_bonus = X add_mio_task_capacity = N add_mio_size_up_requirement_factor = -X }`. У SOV `add_mio_funds` лежит в `remove_effect` решения (ровно та схема, что нужна: решение отработало, в конце пришли funds).
- Временный бонус к конкретной технике делается **идеей** с `equipment_bonus = { modern_tank_chassis = { build_cost_ic = -0.075 instant = yes } }` (так в TFR сделаны `SOV_*_production`). Обычные модификаторы страны на отдельный тип техники не действуют.

## 2. Что нужно выяснить до кода (вопросы автору)

1. **Откуда сейчас берутся дефолтные компании Украины.** Закомментированный `generic_tank_organization` имел `allowed = NOT = { OR = { tag = SOV tag = ENG ... } }`: это «запасные» организации для всех, кого нет в списке. Скорее всего, остальные запасные (пехота, артиллерия, поддержка, флот) лежат в другом файле TFR и тоже исключают страны списком. Чтобы убрать их у Украины, придётся либо **целиком заменить** такой файл копией с `tag = UKR` в списке исключений (по правилам проекта это допустимо), либо оставить дефолты рядом с нашими. **Прошу прислать список файлов папки `organizations/` и те, где определены `generic_infantry_equipment`, `generic_artillery`, `generic_motorized_mechanized`, `generic_support_equipment`, `generic_tank`, `generic_escort_ship`, `generic_task_force_ship`, `generic_general_aircraft`.**
2. Иконки: берём ванильные `GFX_idea_generic_*_manufacturer_*` (как в архетипах) до появления своего арта (раздел «Нужен арт»)? Предлагаю да.
3. Окно решений: отдельная категория `UKR_defense_industry_category` «Оборонная промышленность» (предлагаю) или в существующие категории?

## 3. Организации, версия 1 (на подтверждённых архетипах)

Префикс `UKR_`, суффикс `_organization`. Все: `allowed = { original_tag = UKR has_dlc = "Arms Against Tyranny" }`. Баланс: у каждой небольшой, но осмысленный уникальный бонус «эффективность, а не масса»; цифры черт ниже - первый заход, правятся после теста.

| ID | Прототип (по памяти) | Архетип | Уникальные черты (идея) |
|---|---|---|---|
| `UKR_malyshev_organization` | Завод им. Малышева, КБ им. Морозова (Харьков) | `generic_medium_tank` | двигатель 6ТД (надёжность, скорость); динамическая защита (броня, защита); начальная черта: броня +, цена - |
| `UKR_armor_repair_organization` | бронетанковые ремонтные заводы (Львов, Киев, Николаев) | `generic_tank_refurbishment_plant` | «трофейный фонд» (ремонт и переделка трофейных машин дешевле), эффективность линии |
| `UKR_kraz_organization` | КрАЗ (Кременчуг), «Богдан» | `generic_armored_car` | колёсные бронемашины: скорость, надёжность, цена |
| `UKR_drone_cluster_organization` | оборонный кластер БПЛА (стартапы, волонтёры) | `generic_TFR_UAV_equipment` | «гаражные мастерские» (рост эффективности, но надёжность -), «волонтёрское финансирование» (`funds_gain`), «нейронавигация» (soft_attack) |
| `UKR_antonov_organization` | «Антонов» | `generic_heavy_aircraft` | транспортная авиация: дальность, цена; мрачных шуток про потери нет |
| `UKR_motor_sich_organization` | «Мотор Сич», «Ивченко-Прогресс» | `generic_range_focused_aircraft` | двигатели: дальность, топливо, надёжность |
| `UKR_aircraft_repair_organization` | авиаремонтные заводы (Львов, Николаев, Чугуев) | `generic_high_agility_fighter_aircraft` | модернизация МиГ-29 и Су-27: манёвренность, цена |
| `UKR_mykolaiv_yard_organization` | Черноморский судостроительный завод, «Зоря-Машпроект» (Николаев) | `generic_black_sea_fleet` | малый флот: корветы, береговая оборона, газотурбины |

**Очередь 2 (после ответа на вопрос 1):** `UKR_malyshev`-родня для лёгких танков (`generic_infantry_tank`/`mobile_tank`), «Форт» и стрелковое оружие (`infantry_equipment`), «Артём» и артиллерия (`artillery`), «Луч»/«Южное» и крылатая ракета «Нептун» (отдельная организация на архетипе БПЛА с упором на `tfr_mio_trait_cruise_missile`), морские дроны, «Укрзализныця» как `train_equipment` в `refurbishment`-ветке. Привязка к опорам блока 3: технократы усиливают `UKR_drone_cluster` (`UKR_t_drone_army`), олигархи получают кланы-владельцев (закупки «через приближённые компании», дух `UKR_eggs_scandal`), левые - национализация, националисты - `UKR_np_import_substitution`.

Техника: каждая организация - короткий блок `include` + `icon` + `allowed` + `initial_trait` + 2-3 своих `trait` (позиции относительно существующих токенов архетипа, `any_parent`/`all_parents` из него же) + `override_trait` при необходимости. Ключи локализации: имя организации, описание, имя начальной черты, имена новых черт (ru + en).

## 4. Окно «Оборонная промышленность»: решения при военных фокусах

Каждый подходящий военный фокус даёт 1 решение (подсказка `unlock_decision_tooltip` в награде фокуса; правка в нашем `TFR_national_focus_UKR.txt`, стоимость фокуса не меняем).

**Схема решения** (как `UKR_national_startup_fund`, но многоразовая с кулдауном):

- `cost` = 25-50 политической власти (меньше для малых организаций).
- Деньги: `custom_cost_trigger = { income_var >= N }` и списание в `complete_effect` через `add_income_with_inflation` (`income_var_temp = -2…-6`, масштаб млрд, как в уже существующих фокусах, сверить с `TFR_CHEATSHEET.md` 1.2).
- `complete_effect`: `add_ideas = UKR_mio_<имя>_boost` (идея с `equipment_bonus`, цена конкретной техники -6…-10%, `instant = yes`).
- `days_remove` = 120-180 (срок действия бонуса).
- `remove_effect`: `remove_ideas = UKR_mio_<имя>_boost`, затем `mio:UKR_<имя>_organization = { add_mio_funds = 150-400 }` (по образцу SOV: 300 у Калашникова, 500 у ГАЗ, 1000 у Renault; Украина слабее, поэтому ниже).
- Кулдаун `days_re_enable` 240-360 дней или `fire_only_once = yes` у крупных.
- `visible`: фокус выполнен; `ai_will_do` осмысленный.

| Решение | Фокус-источник (уже в дереве) | Бонус на время | Организация, куда придут funds |
|---|---|---|---|
| `UKR_mio_malyshev_overhaul` | `UKR_modernize_tank_forces` | цена `modern_tank_chassis`, `light_tank_chassis` | `UKR_malyshev` |
| `UKR_mio_trophy_repair` | `UKR_military_industrial_complex` | цена и ремонт танков | `UKR_armor_repair` |
| `UKR_mio_kraz_armored` | `UKR_special_forces_equipment` | `armored_car_equipment` | `UKR_kraz` |
| `UKR_mio_drone_workshops` | `UKR_UAV_warfare_revolution` | `infantry_equipment` (БПЛА в TFR идут по пехотной ветке) | `UKR_drone_cluster` |
| `UKR_mio_antonov` | `UKR_develop_domestic_industry` | `large_plane_airframe`, `transport_plane_equipment` | `UKR_antonov` |
| `UKR_mio_motor_sich` | `UKR_develop_domestic_industry` | `small_plane_airframe`, `medium_plane_airframe` | `UKR_motor_sich` |
| `UKR_mio_aircraft_overhaul` | `UKR_military_adaptability` | `small_plane_airframe` (модернизация) | `UKR_aircraft_repair` |
| `UKR_mio_mykolaiv_yard` | `UKR_maritime_revival` | цена кораблей малого флота | `UKR_mykolaiv_yard` |

В дереве **нет авиационных фокусов**, поэтому авиация привязана к общим (`develop_domestic_industry`, `military_adaptability`). Если нужно, добавим отдельную авиационную ветку (обсудим позже).

Склонности: решения БПЛА дают `UKR_digital_lean`, закупки на трофеях и заводах дают `UKR_authoritarian_lean`/нейтрально (мелко, скрыто), как остальные фокусы.

## 5. Реестр (к переносу в `DESIGN.md`, раздел 12, после утверждения)

- Организации: `UKR_malyshev_organization`, `UKR_armor_repair_organization`, `UKR_kraz_organization`, `UKR_drone_cluster_organization`, `UKR_antonov_organization`, `UKR_motor_sich_organization`, `UKR_aircraft_repair_organization`, `UKR_mykolaiv_yard_organization`.
- Категория: `UKR_defense_industry_category`.
- Решения: `UKR_mio_malyshev_overhaul`, `UKR_mio_trophy_repair`, `UKR_mio_kraz_armored`, `UKR_mio_drone_workshops`, `UKR_mio_antonov`, `UKR_mio_motor_sich`, `UKR_mio_aircraft_overhaul`, `UKR_mio_mykolaiv_yard`.
- Идеи: `UKR_mio_<имя>_boost` (8 штук). Флаги кулдауна `UKR_mio_<имя>_cooldown`, если понадобятся.
- Файлы: `common/military_industrial_organization/organizations/UKR_organizations.txt`; решения - `common/decisions/UKR_decisions_defense_industry.txt`; категория - в `common/decisions/categories/`; идеи - `common/ideas/UKR_ideas_defense_industry.txt`; локализация - `localisation/{russian,english}/UKR_defense_industry_l_*.yml`.

## 6. Риски

- **[ПРОВЕРИТЬ]** тип `equipment_bonus` в идеях: ключи техники (`modern_tank_chassis`, `armored_car_equipment`, `small_plane_airframe`, корабельные) брать только из примеров TFR/ванили; для флота нужна сверка в игре.
- **[ПРОВЕРИТЬ]** конфликт токенов черт при `include`: свои трейты нужно ставить на свободные позиции, иначе перекрытие в UI.
- MIO работают только с DLC Arms Against Tyranny: без него решения должны быть скрыты (`has_dlc` в `visible`/`allowed` категории).
- Если дефолтные запасные организации останутся, у Украины будет «и дефолт, и наша» для одной техники (не ошибка, но захламление).
- Архетипы из раздела «закомментированы» пока не используем: ссылка на неопределённый `include` даст ошибку в `error.log`.
- Проверить игрой: появляются ли организации сразу на старте 2020 и сколько стартовых funds выдаёт игра.

## 7. Порядок работ (после утверждения)

1. Ответы на вопросы раздела 2.
2. Реестр в `DESIGN.md`, затем файл организаций (8 штук) + локализация ru/en.
3. Идеи-бонусы, категория, 8 решений, правки наград 7 фокусов (`unlock_decision_tooltip`).
4. `python3 _tools/audit.py`, правка `DESIGN.md` (журнал), `HANDOFF.md`.
5. Очередь 2 и привязка к опорам блока 3.
