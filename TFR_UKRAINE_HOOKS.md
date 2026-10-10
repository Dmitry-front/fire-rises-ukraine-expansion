# TFR_UKRAINE_HOOKS.md - как TFR обращается с Украиной

Справочник «какие крючки TFR уже сидят на Украине»: кто и когда вызывает её события, кто делит её при капитуляции, что TFR читает и пишет в наших `UKR_*` объектах. Составлен 10.10.2026 по **полному референсу** `_reference/TFR_Reference/` (версия TFR из строки `on_startup`: `The Fire Rises "Release" v1.2025.0b`). Все утверждения прочитаны в коде (**(код)**), гипотезы помечены **[ПРОВЕРИТЬ]**. Номера строк даны для файлов референса на эту дату и нужны только как подсказка; названия файлов, эффектов и ID достаточно, чтобы найти место в любой версии TFR.

Папка `_reference/` будет удалена, поэтому всё нужное из неё перенесено в текст. Связанные документы: `TFR_CHEATSHEET.md` (рецепты и триггеры; раздел 13 - деревья фокусов SOV), `TFR_SYNC.md` (где наши копии файлов TFR разошлись с оригиналами), `TFR_ENGINE.md` (как устроены on_actions и scripted effects).

---

## 1. Карта Украины: области, ID, названия в игре

Названия файлов `history/states/` устарели, **имя области в игре задаёт локализация** (`STATE_<id>`). Например, файл `200-Rivne.txt` - это Запорожье, а `226-Nikopol.txt` - Днепр. Пользоваться нужно столбцом «в игре».

| ID | В игре | Владелец на старте | Примечание |
|---|---|---|---|
| 1285 | Киев (город) | UKR | столица; ключевая область, точка вызова `russia.76` |
| 193 | Чернигов | UKR | |
| 202 | Киевская область | UKR | |
| 1185 | Переяслав | UKR | |
| 225 | Сумы | UKR | |
| 259 | Полтава | UKR | |
| 221 | Харьков | UKR | |
| 203 | Черкассы | UKR | |
| 201 | Житомир | UKR | |
| 198 | Винница | UKR | |
| 199 | Хмельницкий | UKR | |
| 93 | Волынь | UKR | |
| 91 | Львов | UKR | |
| 89 | Ивано-Франковск | UKR | |
| 80 | Буковина | UKR | |
| 73 | Закарпатье | UKR | в сценариях капитуляции из него делают `DNZ` («Карпатская Русь») |
| 192 | Одесса | UKR | |
| 197 | Николаев | UKR | |
| 196 | Херсон | UKR | |
| 806 | Буджак | UKR | |
| 200 | Запорожье | UKR | в нём ЗАЭС (`UKR_destroyed_zaporozhye`), опорный пункт города 11405 |
| 226 | Днепр | UKR | опорный пункт 11422 |
| 1184 | Синельниково | UKR | |
| 1374 | Мариуполь | UKR | ядра UKR и DPR |
| 1091 | Краматорск | UKR | ядра UKR и DPR |
| 1090 | Северодонецк | UKR | ядра UKR и NOV |
| 1375 | Старобельск | UKR | ядра UKR и NOV |
| 227 | Донецк | **DPR** | отдельная страна, ядро DPR |
| 228 | Луганск | **NOV** | столица Новороссии (NOV) |
| 137, 1059 | Крым, Севастополь | SOV | у UKR только претензии |
| 853, 1396, 1283, 240 | Ростов, Таганрог, Белгород (город и область) | SOV | |

Итого на старте 27 областей принадлежат UKR (по картам TFR; Донецк - у DPR, Луганск - у NOV, Крым и Севастополь - у SOV). Сверка с нашими флагами потерь в `common/on_actions/TFR_on_actions_UKR.txt`: города → области `1285 Киев, 221 Харьков, 225 Сумы, 193 Чернигов, 200 Запорожье, 196 Херсон, 226 Днепр, 201 Житомир, 192 Одесса, 91 Львов` совпадают с локализацией (закрывает последний пункт TD-29: ID областей сверены 10.10.2026).

Названия городов-провинций, которые TFR переименовывает при капитуляции (`set_province_name`): 525 Киев, 418 Харьков, 11479 Львов, 11561 Кривой Рог, 11405 Запорожье, 3543 Гостомель, 11670 Одесса, 3755 Николаев, 3568 Чернигов, 9465 Белая Церковь, 9425 Ивано-Франковск, 11422 Днепр, 502 Славянск, 9481 Винница, 3452 Кропивницкий (переименовывается отдельно).

Теги вокруг Украины:
- **NOV** - Новороссия. Столица Луганск (область 228). Стартует марионеточной «республикой»; Россия аннексирует или передаёт ей области при капитуляции Украины.
- **DPR** - Донецкая народная республика (область 227).
- **DNZ** - в TFR это **«Карпатская Русь»** (название тега осталось от Данцига, `history/countries/DNZ - Danzig.txt`, но капитал - область 73, лидер Пётр Гецко). Не путать с Данцигом.
- **SHL** (Ростовская зона оккупации), **KUB**, **KBK**, **BYA**, **FER**, **UNN** - «республики» на территории России, появляются в сценарии «восстаний» (`ukraine.8/9/10/15/16/18/19`). Украина вмешивается в их судьбу (`give_guarantee`, `puppet`).

---

## 2. Что TFR сам даёт Украине (база, которую мы расширяем)

Оригинальный UKR-контент TFR мал (файлы, которые наши копии заменяют):
- **Решения** (`TFR_decisions_UKR.txt`, 541 строка): категория `UKR_land_reforms` (`land_purchasing_amendments`) и категория `UKR_special_military_operation` - `UKR_novorossiyan_offensive_decision`, три волны мобилизации `UKR_first/second/third_mobilization_wave` и миссия `UKR_special_military_operation_timer`.
- **События** `ukraine.1-19` (1046 строк). Все, кроме `ukraine.13`, - сюжет про Россию и её распад: Минский протокол (1), рейс PS752 (2), «неонацизм» (3), подготовка к войне (4), приглашение в НАТО (5), Белгородская зона (6-8), восстания Ростова, Севастополя, Кубани и Донбасса (9, 10, 15, 19), гарантии Кубани (12), **выборы 2024 (13)**, советское восстание (14), успех российских восстаний (16, 18), бремя оккупации (17). `ukraine.11` - «debug event»: он нужен, чтобы войти в войну; его вызывают деревья Медведева, КПРФ и ЛДПР.
- **Идеи** (`TFR_ideas_UKR.txt`, 29): `UKR_to_each_their_own`, `UKR_russian_spring`, `UKR_corrupt_army_staff`, `UKR_government_corruption`, `UKR_far_right_meddling`, `UKR_zelensky_growing_authoritarism` (и `2`), `UKR_poroshenko_plutocracy`, `UKR_ukrainian_ultranationalism`, `UKR_minsk_protocol`, `UKR_mass_insurgency`, `UKR_embargoed_economy`, `UKR_ukrainianrussian_church_schism`, `UKR_ukranian_orthodox_church`, `UKR_to_the_last`, `UKR_collapsing_military`, `UKR_russian_economic_investements_idea`, `UKR_heorim_slava`, `UKR_kiev_counter_offensive`, `UKR_maidan`, `UKR_legacy_of_kiev_junta_idea`, `UKR_new_berkut_idea`, `UKR_brotherhood_treaty_idea` (и `_2`, `_3`), `UKR_russia_trained_security_force_idea`, `UKR_healthy_patriotism_idea`, скрытые `UKR_bratstvo_stoyaka` и `_1`.
- **Персонажи** (`TFR_characters_UKR.txt`): 37.
- Старт-история `history/countries/UKR - Ukraine.txt`, ООБ (`history/units/UKR_*`), шаблоны ИИ `ai_templates/templates_UKR.txt`.
- Фокусов у Украины в TFR **нет**: дерево `TFR_national_focus_UKR.txt` у нас целиком наше (`has_content_tag` добавлен подмодом, см. `TFR_SYNC.md`).

Что TFR **не локализует** в Украине: тексты `ukraine.6-10`, `15-19` (и `ukraine.1.a`, `2.a`) отсутствуют в локализации самого TFR (проверено по всем пяти языкам). В оригинале они показываются сырыми ключами. Это не наша потеря (закрывает TD-05); `ukraine.13.t/.d` в TFR - заглушка `"Tupoe Govno"` / `"Tupogo Govna"`.

---

## 3. Старт игры: `on_startup` (`00_TFR_on_actions_ZZZ_startup.txt`, `00_..._money.txt`)

(код)
- Общий стартовый эффект ставит глобальный флаг `TFR_startup_global`, запускает таймеры сюжета множеством `country_event = { id = ... days = N }` и настраивает экономику.
- **Экономика Украины на старте:** сначала `change_economy_type_collective_capitalism` (список UKR, BLR, PLD, KAZ, UZB, MON, FRA), затем `change_economy_type_oligopolistic_capitalism` (список UKR, SOV, KAZ, TUR); итог для UKR - `oligopolistic_capitalism`. Инфляция 0.078, долг 77 (у остальных 0.068 и 110). Эти числа задают исходную ликвидность и баланс в `money`-системе.
- **Стартовые события Украины:** только `ukraine.13`, и он планируется **дважды**:
  - `days = 1300` (около **24.07.2023**), без комментария;
  - `days = 1551` (**31.03.2024**), с комментарием «Hohol election».
  Оба вызова безусловные (внутри `on_startup/effect/UKR`). Так как событие `fire_only_once = yes`, срабатывает **более ранний вызов**: в обычной партии TFR показывает выборы 2024 в **июле 2023**, а второй вызов молча пропускается. Это и есть ответ на TD-17: на тесте 28.09.2026 TFR вызвал событие около 25.07.2023. Это либо забытый остаток прежней версии TFR, либо ошибка; поведение TFR, не наша ошибка. В нашем моде оно уже нейтрализовано (в копии события стоит условие, `UKR_events_politics.txt` вызывает его сам 21.04.2024).
- Параллельно для других стран TFR планирует собственные события в тех же блоках (CAN `canada.2` на +740, BLR `belarus.1` на +221, IRQ `iraq.1` на +649, PER `iran.22` на +534 и т. д.). Полный перечень - по списку `country_event` в файле.
- Игровое правило `UKR_election_24` (`common/game_rules/00_game_rules.txt`, DLC `Waking the Tiger`, группа `RULE_GROUP_EUROPE`): опции `UKR_election_UKR_24` («победа Зеленского») и `UKR_election_RUS_24` («победа пророссийской силы»). Влияет только на `ai_chance` опций `ukraine.13.a/.b` (множитель 0 против несовместимой опции). Тексты правил `UKR_election_*_TXT` лежат в локализации TFR. Наше `ukraine_politics` трогать правило не обязано.

---

## 4. Падение и освобождение городов: `on_state_control_changed` (`TFR_on_actions_ZZZ.txt`, строки 2-3300)

(код) Один огромный блок: на каждый «исторический» город - `if = { #Название limit = { FROM.FROM = { state = ID } ... } ... }`. Правила чтения:
- **ROOT** - новый контролёр области, **FROM** - прежний контролёр, **FROM.FROM** - область (так в `on_state_control_changed` HOI4).
- В `limit` почти везде есть `has_global_flag = SOV_nato_war_begins_global` (блок работает только с начала Первой европейской войны) и `NOT = { has_global_flag = captured_<город> }` (однократность). Затем `set_global_flag = captured_<город>`, новости `news.NNN`, иногда события для SOV/GER.
- Блоки Второй европейской войны требуют `second_nato_war_flag`.

### 4.1. Крючки на области Украины и соседей (из 157 блоков, 31 упоминает UKR)

| Блок (комментарий TFR) | Область | Флаг-замок | Что запускает | Условие войны |
|---|---|---|---|---|
| **Kiev** | 1285 | `captured_kiev` | `news.195` сразу; контролёру (ROOT) +0.03 поддержки войны, продление идей `SOV_soviet_storm`/`SOV_russian_storm` на 35 дней, срок миссии `SOV_nato_war_deadline` +35 дней; **`random_list`: 70% `news.230` + Украине дух `UKR_kiev_counter_offensive` на 60 дней; 30% `russia.76` (Залужный) через 15 дней**; также `russia.83` (7 дней) и `NEP: russia.217`; GER получает `NATO_escalate_the_war_effect`; в Киеве -2 слота зданий; создаются добровольческие бригады ополчения (`Natsionalna Hvardiya 2`) на область | `SOV_nato_war_begins_global` |
| **Second Battle of Kiev** | 1285 | `captured_kiev_second` | `news.201`; SOV -0.03 поддержки и срок `SOV_nato_war_deadline` на -25 дней; в Киеве -2 слота | освобождение Киева союзниками UKR/GER |
| **Odessa** / **Second Battle** | 192 | `captured_odessa` / `_second` | `news.208` / `news.209` | |
| **Sevastopol** | 1059 | `captured_sevastopol` | `news.199` | |
| **Bahkmut** | 1091 | `captured_bakhmut` | `news.270` | без флага войны |
| **Lviv** | 91 | `captured_lviv` | `news.602` | |
| **shebekino** | 1283 | `captured_shebekino` | событие SOV `russia.766` | |
| **Minsk** / **Second Battle of Minsk** | 206 | `captured_minsk(_second)` | `news.194` / `news.200` | |
| **Zaporozhye NPP** | 200 | `UKR_destroyed_zaporozhye` | `russia.89` («Украинцы разрушили ЗАЭС»), `news.205` ядерная катастрофа | без флага войны |
| **Bandera Statue Destroyed** | 91 | `UKR_destroyed_bandera` | `russia.119` | после победы SOV (`SOV_first_nato_war_victory`) |
| **Notice of Conduct** | 226 | `SOV_notice_of_conduct` | `russia.235`, `russia.236` | |
| **Ukrainian Defenses Collapse** | 197, 202, 203, 226, 1285 | `SOV_dniper_collapse` | `germany.103` | вторая война (`second_nato_war_flag`) |
| **Ukrainian Uprising** | 196 | `SOV_ukrainian_uprising` | `germany.181` | вторая война |
| **Anti Communist/Anti Russian Uprising** | 91 | `UKR_bandera_uprising` | `germany.183` | вторая война |
| **Battle of Kiev fascist** (три раза) | 1285 | `battle_of_kiev_fascist`, `second_`, `third_` | `news.299/300/301`, `germany.171` | вторая война, фашистская Германия |
| **Looting the Crown** | 947 | `SOV_crown_looted` | `russia.245` | |
| **Cobasna Ammunition Depot Explosion** | 857 | `TRA_destroyed_cobasna` | `news.276` | Приднестровье |
| **SOV event The Hunt** | 5,10,88,90,92,97,98 | `SOV_the_hunt` | `russia.782` | |

Остальные блоки (Германия, Польша, Прибалтика, США, Китай, Япония...) в таблицу не вошли.

### 4.2. Что это значит для нас
- Наш `common/on_actions/TFR_on_actions_UKR.txt` вешает свой `on_state_control_changed` рядом с этим (на области 1285, 221, 225, 193, 200, 196, 226, 201, 192, 91). Конфликта нет: эффекты из разных файлов с одним ключом `on_state_control_changed` выполняются **оба** (TFR не использует `on_daily` вообще, только `on_weekly`/`on_monthly`/`on_startup`).
- Флаг-замки TFR глобальные (`captured_*`). Если после освобождения города наш мод ждёт «повторного» падения, TFR уже ничего не покажет (замок стоит), поэтому наши события (`ukrainewar.100-119`) на эти флаги не опираются, и это правильно.
- **Залужный (`russia.76`).** Единственный вызов - `TFR_on_actions_ZZZ.txt`, блок «Kiev» (30% при падении Киева в Первой европейской войне). Событие для сцены SOV: `trigger = { UKR = { NOT = { is_puppet_of = SOV } exists = yes } }`, одна опция: Украине `-0.2` стабильности, `remove_ideas UKR_to_the_last`, `add_ideas UKR_collapsing_military`, правящая `nationalist` без выборов, лидер Залужный (`military_junta`), национализм +0.26. Наша копия `events/TFR_events_SOV_UKR.txt` перекрывает событие условием `always = no`; пустая «ветка 30%» в `random_list` просто ничего не делает (новость `news.230` тоже не показывается в этих 30%). Это решение корректно и ничего не ломает [ПРОВЕРИТЬ в игре: нет жалобы на дубль ID в `error.log`]. Закрывает TD-01 по части «кто вызывает».

---

## 5. Запуск и завершение Первой европейской войны

### 5.1. Вход (подробности деревьев - `TFR_CHEATSHEET.md`, 13.2)
(код)
1. Одно из деревьев России (Медведев, КПРФ, ЛДПР) вызывает `ukraine.11` и `nato.15` (через 55-60 дней).
2. `nato.15` (`events/TFR_events_ZZZ_NATO.txt`) в `immediate` активирует миссию `NATO_intervention_timer`.
3. **`NATO_intervention_timer`** (`TFR_decisions_SOV.txt`, категория `SOV_NATO_war_category`, `days_mission_timeout = 60`). Её `timeout_effect` и есть момент начала европейской войны: `news.237`, Украине `ukraine.5` («Приглашение в НАТО»), Германии `nato.22`, `germany.23/28`, `germany.93` (если у Die Linke > 15%), Франции `nato.22`, Италии флаг `ITA_first_war_tree_enabled_flag`, **глобальный флаг `SOV_nato_war_begins_global`**; SOV: убираются идеи `SOV_special_military_operation(_1)`, активируется миссия `SOV_nato_war_deadline`, всем в блоке Германии (кроме UKR) идея `NATO_european_war`; при датах в нужном окне `nato.12` всем союзникам (ITA, GER, FRA, PLD, ROM, UKR, ENG, CZE, SPR); Польше черта `hos_hates_russians`, `russia.65` через 230 дней.
4. Параллельная старая цепочка: миссия **`UKR_special_military_operation_timer`** (`TFR_decisions_UKR.txt`, 2500 дней; активируют `ukraine.11`, событие SOV `russia.188`, фокус Медведева и фокус КПРФ `communist_new`). Её `cancel_effect` делает то же самое, если `surrender_progress > 0.51` у UKR. Без `timeout_effect`. Это и есть «устаревший» вариант из TD-26: в оригинале TFR он идентичен нашему. Какой из двух таймеров сработает первым, тот и запустит войну; флаг `SOV_nato_war_begins_global` защищает от повторной активации (у обеих миссий `visible = NOT has_global_flag SOV_nato_war_begins_global`).
   Различия, перечисленные в TD-26 (ITA, `PLD` вместо `POL`, `germany.25`, `GER_die_linke_popularity_var`), **подтверждаются**: в ссылках TFR на Польшу в этом блоке стоит `PLD`; `POL` как действующая Польша не используется [ПРОВЕРИТЬ в `history/countries`: есть оба файла `POL - Poland.txt` и PLD, у PLD поля `ideas`]. Отдельный пункт в `TFR_SYNC.md`.

### 5.2. Выход
(код, `TFR_decisions_SOV.txt`, категория `SOV_NATO_war_category`)
- **`SOV_nato_war_deadline`** - миссия с условием `available` (захват Венгрии/Молдовы/Польши/Балтии в разных сочетаниях; перечислены наборы областей, например 10, 43, 854, 855 под полным контролем SOV). Три выхода:
  - `complete_effect` - **`SOV_russian_victory = yes`** (победа России);
  - `cancel_effect` («NATO Kill SOV») - **`SOV_russian_defeat = yes`** (поражение России);
  - `timeout_effect` - `SOV_increase_war_exhaustion` и повторная активация миссии (бесконечный цикл усталости).
- **`SOV_unconditional_surrender`** (`available: surrender_progress > 0.25`, `ai_will_do base 90`) - `remove_mission SOV_nato_war_deadline`, `SOV_russian_defeat`.
- Эффекты ставят итоговые глобальные флаги: победа SOV - `SOV_first_nato_war_victory` и `SOV_first_nato_war_victory_MVD` (когда выиграла Россия Медведева); победа НАТО - `nato_nato_won_nato_war`. Они же - ветвление для нашего блока 4 (`CLAUDE.md`).

### 5.3. Что `SOV_russian_victory` делает с Украиной (`TFR_scripted_effects_SOV.txt`, строки ~2674-4576)
(код) Эффект огромный (1900 строк) и ветвится по режиму победившей России:
- **Общее для всех:** UKR снимаются идеи `UKR_to_the_last`, `UKR_government_corruption`, `UKR_corrupt_army_staff`, `UKR_mass_insurgency`, `UKR_embargoed_economy`, `UKR_ukrainianrussian_church_schism`, `UKR_collapsing_military`, `UKR_kiev_counter_offensive` и др.; страны региона (UKR, NOV, BLR, TRA, MOL, Прибалтика, Закавказье, Средняя Азия...) вызывают `SOV_leave_ADS = yes`; всем бывшим соседям (UKR, MLD, HUN, ROM, BUL, ...) идея `SOV_devastated_industry_idea`; `complete_national_focus = SOV_russian_victory`, флаг `SOV_first_nato_war_victory_MVD`.
- **Россия Медведева / ЕР** (`has_government = authoritarian_democrat`, ветка ~3228-3437): события `russia.312` (сопротивление в Украине) и `russia.452`, новость `news.216`, `european_union.1` для Бельгии. Прибалтика и Молдова становятся марионетками. **Если UKR не стала марионеткой SOV:** `set_country_flag = UKR_has_not_capitulated` (читает достижение), `SOV = { white_peace = UKR }`, UKR выходит из фракции, **промоут `UKR_yuri_boyko`**, `set_politics ruling_party = conservative elections_allowed = yes`, партия `UKR_plp` / `UKR_plp_short`, консерваторам +0.35 - то есть «мирная» победа Медведева над не сдавшейся Украиной оставляет страну под Бойко.
- **Жириновский** (ветка ~3437): `SOV = { annex_country UKR; annex_country NOV; annex_country DPR }` (все без войск), русские названия городов (`aleksandrovsk_city`...), SOV получает ядра на 227 и 228 и области Украины.
- **КПРФ** (`SOV_cprf_won`, ветка ~4327): аннексия UKR и добавление SOV-ядер на 12 областей востока, `SOV_leave_ADS` для UKR.
- **Оговорка по коду:** во многих местах `if = { limit = { NOT = { is_puppet_of = SOV } } }` оставлен без тела, а следующие за ним эффекты стоят уже вне условия (например, `EST`/`LIT`/`LAT`/`MOL` и ветки Жириновского/КПРФ). В результате эти аннексии и марионетки выполняются безусловно. Это ошибка TFR; нам важно лишь, что условие «UKR не марионетка» **не защищает** от аннексии в ветках Жириновского и КПРФ, а в ветке Медведева оно действительно работает (там тело `if` заполнено).

### 5.4. Что `SOV_russian_defeat` делает с Украиной (победа НАТО; начало `TFR_scripted_effects_SOV.txt`)
(код) Это основа для нашего блока 4 «Победа НАТО» (`DESIGN.md`, 10.2): TFR уже переписывает Украину после победы, причём в зависимости от того, кто ею правит.
- Если UKR была марионеткой SOV: `SOV = { end_puppet = UKR }`, `drop_cosmetic_tag`.
- Если UKR не в одной фракции с GER, **лидер НАТО** (страна с флагом `NATO_current_leader`) вступает в фракцию UKR.
- UKR: снимается `UKR_corrupt_army_staff`, выдаётся общая идея `GER_scars_of_nato_war`, **аннексируются NOV и DPR** (без войск), `UKR_to_the_last` меняется на **`UKR_heorim_slava`**; с областей снимаются динамические модификаторы `UKR_russian_speaking_majority_region` (192, 196, 200, 221, 1090, 1091, 1184: ресурсы -10%, живая сила -30%, скорость стройки -10%) и `SOV_DPR_modifier` / `SOV_LPR_modifier` (227, 228).
- **Передаёт Украине все её области**, включая Крым (137, 1059) и Донбасс (227, 228): `transfer_state` по списку из 35 вызовов. Для нас это значит: территориальные исходы в блоке 4 не нужно строить заново, достаточно читать итоговый список областей.
- Герои: персонажи `UKR_volodymyr_zelenskyy`, `UKR_denys_prokopenko`, `UKR_mykhailo_zabrodskyi`, `UKR_mykola_balan`, `UKR_valeriy_heletey`, `UKR_mariana_bezuglaya` получают черту `trait_UKR_hero_ukraine`; `UKR_viktor_medvedchuk` уходит на пенсию (`retire_character`).
- **Внутренняя политика зависит от действующего лидера** (`has_country_leader = { character = ... ruling_only = yes }`):

| Лидер UKR | Условие | Результат |
|---|---|---|
| `UKR_volodymyr_zelensky` | `authoritarian_democrat > 19` | снимается `UKR_zelensky_growing_authoritarism2`; он остаётся лидером с идеологией `oligarchist`; правящая `authoritarian_democrat`, выборы запрещены, партия `UKR_social_liberal_party`, популярность +0.1 |
| `UKR_volodymyr_zelensky` | `authoritarian_democrat < 19` | `social_liberal` +0.1, черта `hog_beacon_of_Ukrainian_liberty` |
| `UKR_petro_poroshenko` | - | лидер `neoconservative`, правящая `conservative`, без выборов, партия `UKR_conservative_party` |
| `UKR_valery_zaluzhny` | - | лидер `military_junta`, правящая `nationalist` без выборов, национализм +0.16 |

  Всем `communist -1` (коммунисты вычищаются). **Для нашего мода:** к концу блока 3 лидер и доля `authoritarian_democrat` определяют, какая из веток сработает; если мы сделаем лидером кого-то другого (например, технократа Фёдорова), ни одна ветка не сработает и политика останется нашей. Это хорошо, но тогда Бойко/Зеленский-ветки не должны возникнуть случайно: вернём лидера Зеленского - TFR применит свою ветку поверх нашей. [ПРОВЕРИТЬ в игре]
- Добавляет UKR марионеток из бывшей России (`KBK`, `BYA`, `SHL`...) и вводит страны в её фракцию.

---

## 6. Капитуляция Украины: `on_capitulation` (`TFR_on_actions_ZZZ_peace.txt`)

Файл на 27 тысяч строк, отвечает за мирный договор по итогам любой капитуляции, и авторы TFR предупреждают в шапке: «DO NOT TOUCH». Принципы (код):
- ROOT - капитулировавший, FROM - победитель. В начале сохраняются `event_target:winning_country` и `event_target:losing_country`, ставится `show_peace_popup_alert`.
- Основной «аннексионный блок» запускается, только если ROOT **последний выживший** в своей фракции (иначе он ждёт капитуляции остальных). Дальше идёт длинный список `if = { # Описание limit = {...} ... set_global_flag = skip_default_capitulation }` - по одному на каждую пару «победитель-проигравший». Флаг `skip_default_capitulation` отключает ванильный мир (аннексия/передача областей по умолчанию), его нужно ставить в конце каждого собственного блока.
- Блоки идут в строгом порядке; **последовательность важна** (комментарий: «некоторые аннексии работали, потом сломались по неизвестным причинам»).
- `on_capitulation_immediate` (строка ~27207) нужен только для `transfer_navy`.
- `TFR_on_actions_ZZZ.txt` также содержит `on_capitulation` (небольшой: Корея, Грузия, Тунис, Алжир...), `TFR_on_actions_ZZZ_map_modes.txt` - обновление карт.

### 6.1. «SOV Kill UKR» (Россия или союзник России выигрывает у UKR, Первая европейская война; строки ~18893-19302)

Условие: FROM - SOV или союзник SOV, `ROOT original_tag = UKR` (и, как всегда, UKR - последняя в фракции).
Общие эффекты: переименование городов (русские названия: `kiev_city`, `kharkov_city`...), `GER = { NATO_unity_decrease }`, Франции при потерях < 5 тысяч - `france.221`, потом ветка по режиму России, затем `russia.117` (через 20 дней), если SOV завершила `SOV_invest_in_CSTO_members` - UKR вступает в техгруппу `csto_research`, `ROM`/`HUN` загружают ООБ `*_ukraine_capitulation` (оккупация западных областей), `set_global_flag = skip_default_capitulation`.

Ветки в порядке проверки (первая сработавшая выигрывает; все остальные - `else_if`):

| № | Условие (в SOV) | Результат |
|---|---|---|
| 1 | глобальный флаг `NOV_red_ukraine_flag` (КПРФ-«красная Украина»; ставится в `events/TFR_events_SOV.txt` около стр. 16255) | белый мир; **NOV аннексирует UKR**, получает столицу Киев (1285), автономия `autonomy_ssr` под SOV; лидер Пётр Симоненко (`marxism_leninism`/`reformist_socialism`), `russia.127` |
| 2 | флаг `NOV_red_novorossiya_flag` (стр. ~16113) | белый мир; NOV получает ядра и области 1184, 200, 196, 1091, 221, 1090, 226, 197, 192, 806, 1375, 1374 и входит во фракцию SOV; UKR остаётся республикой `autonomy_ssr` с Симоненко (`communist_populism`), `russia.127` |
| 3 | у руля SOV Жириновский | UKR становится **марионеткой**; SOV получает области 1185, 193, 225, 259, 1184, 200, 196, 1091, 221, 1090, 1375, 1374; UKR: `nationalist` без выборов, популярность 0.35, лидер Золотов (`military_junta`), партия `UKR_zhir_governship`, косметика `UKR_zhir`; NOV аннексируется |
| 4 | у руля SOV Миронов или Медведев | UKR - марионетка; NOV получает 12 областей и входит во фракцию; **DNZ (Карпатская Русь) получает область 73 и становится марионеткой SOV** (`nationalist` 0.6, `authoritarian_democrat` 0.15, `communist` 0.25, ООБ `DNZ_2020`); UKR: Азаров (`hybrid_regime`), `authoritarian_democrat` 0.45, партия `UKR_medv_governship(_short)`, косметика `UKR_rus_malorossiya` (если у SOV `SOV_push_back_the_west`) иначе `UKR_rus` |
| 5 | SOV - `national_socialist` | белый мир, `puppet = ROOT`, `annex_country UKR` без войск |
| 6 | у руля Пригожин | то же |

Остальные Россия-лидеры (Дугин, Вагнер, Навальный, Алиханов...) обрабатываются в других блоках файла или в `SOV_*_victory` scripted effects; также есть блоки `SOV_navalny_russia_flag` + `second_nato_war_flag` (стр. ~16836, 21995), где UKR - ROOT.

### 6.2. «Europe Kill UKR» (германский блок побеждает UKR во Второй европейской войне; стр. ~24250-24340)

Условие: FROM - GER или союзник GER, у FROM флаг `second_nato_war_flag`, ROOT - UKR. Результат зависит от режима Германии:

| Условие (в GER) | Результат |
|---|---|
| `fascist` или `national_socialist` | `GER puppet UKR`, лидер Андрей Тарасенко (`ethno_nationalism`), без косметики |
| `nationalist` | марионетка, лидер Анатолий Шевченко (`autocrat`), косметика `UKR_cossack` |
| завершён фокус `GER_a_new_october` | марионетка, косметика `UKR_euro`, идея `GER_chaotic_revolution` |
| завершён фокус `GER_democracy_falters` | марионетка, косметика `UKR_euro_commission`, эффект `GER_ultralib_eu_puppet` |

Рядом: «Europe Kill NOV» - **UKR аннексирует NOV**, если выиграла Германия (`UKR = { annex_country = { target = ROOT } }`), «Europe Kill OVO TRA MOL» и т. п.

### 6.3. Другие блоки, где UKR - участник
- Донбасс и Ростов: победа в войне над SHL/BYA/KBK и пр. (стр. ~9811-9877) - когда не осталось ни одного из них, UKR получает `ukraine.16` («Русские восстания успешны»).
- Блок «кто убивает GER» (стр. ~6395): при белом мире с Германией `end_puppet SOV/UKR/BLR/TTS/ROM/HUN/BUL` - Германию нельзя «убить» до Второй европейской войны.
- Блоки «Navalny Russia + second_nato_war» (стр. ~16836, 21995).
- UKR в больших `OR`-списках (стр. 16541, 16936, 17188, 17400, 18149, 20933, 21367, 21619, 21700, 22094, 22343): списки «стран, которые Россия обязательно аннексирует/держит» (FER, CHE, KBK, BYA, UNN, UKR, BLR, LIT, LAT...) - не дополнительные эффекты, а условия.

### 6.4. Как встроиться в капитуляцию (рекомендация для блока 4, [ПРОВЕРИТЬ в игре])
- Свой `on_capitulation = { effect = {...} }` в нашем файле `common/on_actions/TFR_on_actions_UKR.txt` **выполнится вместе** с TFR (эффекты разных файлов складываются). Файлы читаются по имени, `TFR_on_actions_UKR.txt` идёт **раньше** `TFR_on_actions_ZZZ_peace.txt`, значит наш код видит состояние до решения TFR. Если нужно прочитать итог, надёжнее использовать `country_event = { id = ... days = 1 }` (событие придёт уже после) или флаги TFR после выполнения (`UKR_has_not_capitulated`, `skip_default_capitulation`, косметические теги `UKR_rus`, `UKR_rus_malorossiya`, `UKR_zhir`, `UKR_euro*`, `UKR_cossack`, область 73 у `DNZ`, статус марионетки через `is_puppet_of`).
- Тип победителя и режима лучше читать **по тем же признакам, что TFR**: `has_country_leader = { character = SOV_... ruling_only = yes }`, глобальные флаги `NOV_red_*`, `has_government`, `has_completed_focus`, а не по своим переменным.
- Не ставить `skip_default_capitulation` вне своих блоков: флаг глобальный, его сбрасывает конец блока TFR.
- Тег `UKR` у игрока сохраняется: все ветки TFR работают через `puppet = ROOT`/`annex_country`; для «сохранить тег» нужна своя логика (нельзя полагаться на TFR). Это задача блока 4, проектировать отдельно. До согласования - ничего не менять (CLAUDE.md).

---

## 7. Остальные места, где TFR читает/пишет Украину

### 7.1. События других стран
- **SOV** (`events/TFR_events_SOV.txt`): `russia.43` (Украина выходит из Минских соглашений, снимает `UKR_minsk_protocol`), `russia.76` (Залужный), `russia.83` (химатака в Обухове), `russia.89` (ЗАЭС), `russia.91` («Призрак Киева», ООБ `UKR_kiev_ghost`), `russia.108` («День Победы»), `russia.123` (восстание в Закарпатье), `russia.157` (Распутица), `russia.188` (покушение на Жириновского: включает таймер `UKR_special_military_operation_timer`), `russia.228-230` (террор/переговоры, если UKR не существует), `russia.312-314` (сопротивление и протесты в Украине: `UKR_maidan`, `SOV_UKR_resistance`), `russia.321-323` (репарации НАТО), `russia.332` (открытое восстание на Западной Украине), `russia.336` («Красный Донбасс»), `russia.441`, `russia.451` («Свободные выборы в Украине»: Арестович, Мураев, Медведчук, Бойко; партии `UKR_medvechyk_party`, `UKR_plp(_short)`, `UKR_murayev_party`, `UKR_korolevskaya_party`), `russia.562` (конец раскольников), `russia.770` (переговоры Украина-Россия), `russia.874`, `russia.2029` («Жёлтая гвардия»).
- **Новости** (`TFR_events_ZZZ_news.txt`): `news.200/201/203/205/208/209/230`; **НАТО** (`nato.10`, `nato.12`, `nato.15`, `nato.22`); **ГЕР** (`germany.19`, `97` - парад в Киеве: Порошенко и Зеленский, `118`, `183`); **Донецк** (`donetsk.3/4`); **БЛР** (`belarus.667` «Украина создаёт НАТО 2», `belarus.700`, плюс наш флаг `BLR_maidan`); **ФРА** (`france.279` Франция требует распустить «Азов», `france.2732`); США (`usa.16`); Иран (`iran.2`, рейс PS752).
- Все эти ID **существуют в TFR** (индекс `_tools/tfr_index/events.txt`), поэтому вызовы из наших файлов безопасны (закрывает TD-07 для `germany.*`, `nato.*`, `news.*`, `moldova.2`, `syria.25`).

### 7.2. Решения SOV для Украины
Список в `TFR_CHEATSHEET.md`, 13.1. Дополнительно: цепочка сопротивления `SOV_ukrainian_insurgencies_category` ведёт `SOV_UKR_resistance` (области 80, 91, 89, 93, 199 → расширение `SOV_UKR_resistance_spread1` (198, 201) → `spread2` (202, 203, 1285)), в каждой области динамический модификатор **`UKR_resistance`**: ресурсы -15%, живая сила -35%, скорость стройки -10%, саботаж фабрик +30%; снимается глобальным флагом `SOV_destroyed_resistance`. Это основа для «Сети» блока 4 (у нас - свои счётчики).

### 7.3. ИИ-стратегии (`common/ai_strategy/`)
- `UKR_our_home_is_more_important` (при войне с SOV): не защищать границы союзников LIT, LAT, EST, POL (`dont_defend_ally_borders` 700).
- `UKR_retake_keeeeeeeeeeeeeev` (если Киев у SOV, NOV или BLR): фронт-контроль против SOV с максимальным приоритетом.
- `UKR_one_million_ghosts` (всегда): `force_build_armies 200` - ИИ-Украина строит много армий.
- Союзники: `HOL/AST/SPR_support_UKR`; Венгрия защищает границу Украины; SOV имеет ~19 стратегий против Украины (`TFR_ai_strategy_SOV.txt`), `prepare_for_war UKR -100` в одной из них (перед войной НЕ готовиться - ждать триггера дерева).
- Нашему ИИ-мозгу (дерево фокусов UKR, `ai_will_do`) эти стратегии не мешают, но не заменяют его: они работают на уровне армий и дипломатии.

### 7.4. Прочее
- Динамические модификаторы TFR для Украины: `UKR_russian_ghetto` (область 1283, 853, 1059; ставит `ukraine.6`), `UKR_russian_speaking_majority_region`, `UKR_resistance`, `UKR_fortetsiya_gigant` (+25% фабрик, +25% скорости мобилизации), `UKR_ukrainian_crimea_defense_modifier` (Франция, фокус обороны Крыма). Лежат в `TFR_dynamic_modifiers_SOV/GER/FRA.txt`, не в наших файлах; закрывает TD-04.
- Идея `UKR_gdp_fix` выдаётся в стартовой истории и определена в TFR (`00_TFR_ideas_ZZZ_economic_hidden.txt`); закрывает TD-03.
- Стартовые техи, ООБ и `UKR_first_mobilization`, `UKR_second_mobilization`, `UKR_foreign_volunteers`, `UKR_territorial_defense`, `UKR_abrams`, `UKR_kiev_ghost` лежат в `history/units/` TFR. **Третьей ООБ мобилизации нет** (закрывает пункт TD-29 про `UKR_third_mobilization_wave`: она грузит `UKR_second_mobilization`).
- Реалии `UKR_ssr` и `UKR_alikhanov_puppet`: косметические теги (`common/countries/cosmetic.txt`), используются в фокусах/решениях России.

---

## 8. Контракт с TFR: что в наших `UKR_*` нельзя переименовывать и удалять

Наши файлы-замены (`TFR_ideas_UKR*.txt`, `TFR_characters_UKR.txt`, `TFR_decisions_UKR*.txt`, `TFR_events_UKR.txt`, `TFR_country_localisation_UKR_l_*.yml`, `00_TFR_scripted_triggers_ZZZ_generic.txt` и др.) подменяют оригиналы целиком, а TFR из чужих файлов продолжает на них ссылаться. Если ссылки пропадут, получим молчаливые ошибки или сырые ключи.

Проверено автоматическим сравнением (все токены `UKR_*`, которые встречаются в референсе вне файлов, которые мы заменяем; 97 из них, 53 присутствуют у нас, остальные 44 определены в самом TFR вне наших файлов: ключи партий `UKR_plp`, `UKR_zhir_governship`, косметика `UKR_rus`..., динамические модификаторы, ключи правил). Обязательное для нас:
- **Идеи**, которые TFR выдаёт и снимает: `UKR_to_the_last`, `UKR_heorim_slava`, `UKR_collapsing_military`, `UKR_kiev_counter_offensive`, `UKR_corrupt_army_staff`, `UKR_government_corruption`, `UKR_mass_insurgency`, `UKR_embargoed_economy`, `UKR_ukrainianrussian_church_schism`, `UKR_ukranian_orthodox_church`, `UKR_minsk_protocol`, `UKR_maidan`, `UKR_legacy_of_kiev_junta_idea`, `UKR_new_berkut_idea`, `UKR_brotherhood_treaty_idea/_2/_3`, `UKR_russia_trained_security_force_idea`, `UKR_healthy_patriotism_idea`, `UKR_russian_economic_investements_idea`, `UKR_bratstvo_stoyaka(_1)`, `UKR_zelensky_growing_authoritarism(2)`, `UKR_poroshenko_plutocracy`.
- **Персонажи** (по ID): `UKR_volodymyr_zelenskyy`, `UKR_yuri_boyko`, `UKR_nikolai_azarov`, `UKR_petro_symonenko`, `UKR_valery_zaluzhny`, `UKR_petro_poroshenko`, `UKR_volodymyr_zelensky` (двойное написание у TFR, см. `germany.97`), `UKR_denys_prokopenko`, `UKR_mykhailo_zabrodskyi`, `UKR_mykola_balan`, `UKR_valeriy_heletey`, `UKR_mariana_bezuglaya`, `UKR_alexey_arestovich`, `UKR_evgenyy_murayev`, `UKR_viktor_medvedchuk`.
- **Решения/миссии:** `UKR_special_military_operation_timer` (активируют `russia.188`, дерево Медведева; ID менять нельзя), категории `UKR_special_military_operation`, `UKR_land_reforms`.
- **Страновые флаги:** `UKR_has_not_capitulated` (TFR ставит), `UKR_kiev_ghost` (ООБ).
- **Ключи локализации** в `TFR_country_localisation_UKR_l_*` (105-107 ключей оригинала сохранены все).
- **Статус «контент-тега»:** `has_content_tag` содержит UKR (наше изменение в копии `00_TFR_scripted_triggers_ZZZ_generic.txt`) - при обновлении файла из TFR оно пропадёт (`TFR_SYNC.md`).

---

## 9. Итог по закрытым вопросам (перенести в `DESIGN.md`/`TECH_DEBT.md`)

| Вопрос | Ответ |
|---|---|
| TD-01: кто вызывает `russia.76` | `on_state_control_changed`, блок «Kiev», 30% при падении Киева в Первой европейской войне; наша копия `always = no` корректна |
| TD-02: что с `on_capitulation` | механизм описан в разделе 6; перехват безопасен, если не ломать `skip_default_capitulation`, не менять файл TFR и работать флагами/событиями с задержкой |
| TD-03, TD-04 | идея и модификатор определены в TFR |
| TD-05 | в TFR тексты `ukraine.6-10, 15-19` отсутствуют сами |
| TD-07 | все вызываемые нами события TFR существуют |
| TD-17: кто вызывает `ukraine.13` | `on_startup`, **дважды**: +1300 (24.07.2023) и +1551 (31.03.2024); срабатывает первый |
| TD-26 | оригинальный `UKR_special_military_operation_timer` идентичен нашему; актуальный запуск войны - `NATO_intervention_timer` (раздел 5) |
| TD-29, последний пункт | ID областей сверены (раздел 1) |

## 10. Что ещё не проверено ([ПРОВЕРИТЬ])
1. Как ведёт себя дублирующее по ID событие `russia.76`: берёт ли игра нашу копию (файл грузится позже `TFR_events_SOV.txt`, потому что `.` идёт раньше `_` в сортировке) - по `error.log`.
2. Порядок выполнения одноимённых блоков `on_capitulation` из разных файлов.
3. Действующая Польша: `POL` или `PLD` (см. `TFR_SYNC.md`).
4. Роль переменной `GER_die_linke_popularity_var` в актуальной версии TFR (в нашей копии таймера устаревшая `_temp`-форма).
