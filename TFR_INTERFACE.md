# TFR_INTERFACE.md - локализация, интерфейс, картинки и иконки TFR

Справочник для текстов, окон решений, картинок событий и иконок. Составлен 10.10.2026 по полному референсу (`TFR v1.2025.0b`). **(код)** - прочитано в файлах TFR; **[ПРОВЕРИТЬ]** - нужна проверка в игре. Сами картинки в референс не входят (только описания спрайтов `.gfx`), поэтому имена ниже можно использовать как есть: рисунки лежат в установленном TFR/игре. Список всех спрайтов TFR (36 тысяч имён) хранится в `_tools/tfr_index/gfx.txt` и после удаления референса остаётся поиском по именам: `grep -i "слово" _tools/tfr_index/gfx.txt`.

---

## 1. Локализация

### 1.1. Структура и формат (код)
- Языки TFR: `english` (224 файла), `russian` (192), `german`, `spanish`, `simp_chinese`. Основной контент TFR - английский, русский - перевод сообщества (поэтому часть ключей есть только в английском: `TFR_SYNC.md`).
- Файлы: UTF-8 с BOM, первая строка `l_english:` / `l_russian:`. **TFR пишет строки без номера версии**: ` KEY: "Текст"`; у нас ` KEY:0 "Текст"`. Оба формата читаются, смешивать в одном файле можно.
- Страновые файлы: `TFR_country_localisation_<ТЕГ>_l_<язык>.yml` (названия партий, фокусы, идеи, решения, события страны), `TFR_characters_l_<язык>.yml` (имена и описания персонажей всех стран), `00_TFR_countries_l_*.yml`, `00_TFR_countries_cosmetic_l_*.yml` (названия стран и косметические теги), `TFR_startup_l_english.yml` / `TFR_districts_l_russian.yml` (меню старта и тексты общих окон).
- Одинаковое имя файла означает полную замену (`TFR_SYNC.md`, раздел 2). Точечно перекрывать ключи без замены файла - папка `localisation/<язык>/replace/`.
- Ключи имён персонажей: `<ID персонажа>` и `<ID>_desc`. Ключи партий: `<ТЕГ>_<идеология>_party` / `_party_long`. Ключи названий страны: `<ТЕГ>`, `<ТЕГ>_ADJ`, `<ТЕГ>_DEF`, с идеологией `<ТЕГ>_<идеология>`, `..._ADJ`, `..._DEF`. Для косметических тегов - ключ тега (`UKR_rus`, `UKR_zhir`).

### 1.2. Форматирование текста (код)

**Цвета** (`interface/core.gfx`, `textcolors`; в тексте `§X ... §!`). Чаще всего TFR использует (раз в локализации): `§!` (закрыть) 15939, `§Y` жёлтый 6788, `§R` красный 2810, `§G` зелёный 1791, `§C` голубой 725, `§g` серый 581, `§H` заголовок 395, `§t` ярко-красный 362, `§L` светло-синий 325, `§O` оранжевый 270, `§W` белый 196, `§p` розовый 169, `§s` цвет соцдемов 127, `§a` почти чёрный 111.

| Код | Цвет | Код | Цвет | Код | Цвет |
|---|---|---|---|---|---|
| C | голубой (35 206 255) | W | белый | G | зелёный (0 159 3) |
| L | светло-синий | B | синий | R | красный (255 50 50) |
| b | чёрный | g | серый (176) | Y, H | жёлтый (255 189 0) |
| T | белый (заголовок) | O | оранжевый | p | розовый |
| d | тёмно-красный | A | красный APLA | P | синий PTF |
| n | цвет нацсоцов | s | цвет соцдемов | a | чёрный Atomwaffen |
| V | фиолетовый | y | чисто-жёлтый | `.` | коричнево-оранжевый |
| I | лавандовый | w | золотой | l | светло-жёлтый |
| `0`...`9`, `t` | градиент от фиолетового (0) через синий и зелёный (5-7) к оранжевому (9) и красному (t) | | | | |

Практика TFR: положительные эффекты `§G`, отрицательные `§R`, имена/числа `§Y`, подсказки `§g`. Цвета для сложных тултипов (градиент `§0`...`§t`) используют TFR-системы (например, шкала легитимности).

**Переменные в тексте** (код): `[?имя_переменной|формат]` показывает значение переменной страны. Частые форматы: `|=+1%` (знак, процент, 1 знак после запятой, автоцвет: положительное зелёное, отрицательное красное; 353 раза), `|1%` (230), `|Y1%` (жёлтый процент, 50), `|3` (число, 45), `|=+0` (целое со знаком, 32), `|=-1%` (27), `|Y0` (23), `|%Y2` (16), `|=+2`, `|=-3`. Просто `[?имя]` - без форматирования (288). Для наших видимых счётчиков (Сеть, Подозрение, настрой) этого достаточно: `[?UKRhate|0]`.

**Иконки в тексте** (`£имя`; спрайт `GFX_имя` из `interface/TFR_interface_texticons*.gfx`, `texticons.gfx`): самые частые - `£decision_icon_small` (181), `£pol_power` (128), `£stability_texticon` (99), `£development` (90), `£command_power` (59), `£dx` (49, деньги), `£boost_popularity_texticon` (47), `£consumer_goods_texticon` (38+), `£mil_factory`, `£civ_factory`, `£attack_texticon`, `£defence_texticon`, `£war_support_texticon`, `£research_speed_texticon`, `£construction_speed_texticon`, `£army_morale_texticon`, `£organization_texticon`, `£efficiency_growth_texticon`, `£political_power_texticon`, `£inflation`, `£GFX_dx_yellow`, `£GFX_dx_blue`, `£GFX_power_balance_texticon`. Все эти имена есть в индексе спрайтов.

**Динамика**: `[Root.GetName]`, `[Root.GetAdjective]`, `[From.GetNameDef]`, `[SOV.GetLeader]`, `[ROOT.GetPowerBalanceName]`, `[GetDateText]`; перенос строки `\n`; ссылки на другой ключ `$KEY$`.

### 1.3. Скриптовая локализация (`common/scripted_localisation`, 54 файла) (код)
- Блоки `defined_text = { name = ИМЯ text = { trigger = {...} localization_key = KEY } ... }`; вызов в тексте `[ИМЯ]`.
- Примеры TFR, полезные для Украины: `GetIdeologySubtype` (строка подидеологии лидера в окне политики, `TFR_subideology_scripted_loc.txt`; для Зеленского с `neoliberalism` - `UKR_liberal_oligarchy`), `TFR_scripted_loc_influence.txt` (преобладающее иностранное влияние), страновые файлы (`TFR_scripted_loc_GER.txt` и др.), `TFR_FBI_Scripted_Loc.txt` (досье страны в меню старта: четыре блока `UKR_country_summary/paths/other` и картинка `GFX_UKR_BG`, **мы дописали их в свою копию**; в оригинале UKR нет).
- Один `defined_text` с тем же именем в двух файлах: объединение не гарантировано; безопаснее давать **новым блокам свои имена** (`UKR_*`).

### 1.4. Конвенции ключей, которые TFR соблюдает
- Событие: `<namespace>.<N>.t`, `.d`, опции `.a`, `.b`, `.c` (у TFR встречается `.o1`, `.o2`).
- Фокус: `<ID>`, `<ID>_desc`; идея: `<ID>`, `<ID>_desc`; решение: `<ID>`, `<ID>_desc`; категория: `<ID>`, `<ID>_desc`; тултипы: `<имя>_tt` / `<имя>_tooltip`.
- Новости: `news.<N>.t/.d/.a`.
- Динамические модификаторы: ключ = ID, описание не требуется (текст подтягивается из `GFX` и ключей модификаторов).

---

## 2. Картинки событий: готовая палитра (код, индекс спрайтов)

TFR определяет 435 спрайтов `GFX_report_event_*`, 228 `GFX_news_event_*` (нумерованные), 113 `GFX_event_*`. Наши события с временной картинкой `GFX_report_event_ukrainian_civil_war` **этого спрайта нет ни в интерфейсе TFR, ни в нашем `UKR_event_pictures.gfx`** (его использует и сам оригинальный `TFR_events_UKR.txt`; вероятно ванильный, но проверьте в игре, не показывается ли пустая рамка) [ПРОВЕРИТЬ]. Вместо него можно взять тематическую картинку из TFR:

| Сюжет | Подходящие спрайты (есть в TFR) |
|---|---|
| Выборы, голосование | `GFX_report_event_election_vote`, `GFX_generic_elections`, `GFX_report_event_usa_election_generic` |
| Парламент (Рада) | `GFX_report_event_generic_parliament`, `GFX_report_event_hungary_parliament`, `GFX_report_event_romania_parliament` |
| Митинг, протест | `GFX_report_event_generic_rally`, `..._rally2`, `..._rally_3`, `GFX_report_event_gathering_protest`, `GFX_Generic_Protest`, `GFX_report_event_worker_protests`, `GFX_Generic_Reformer_Rally` |
| Беспорядки | `GFX_report_event_generic_riot`, `GFX_Generic_Riot`, `GFX_Generic_Riot1`, `GFX_Generic_Riot2`, `GFX_event_GER_riot_fire/_gas_masks/_molotov`, `GFX_Kiev_Riots` |
| Забастовка, шахтёры | `GFX_report_event_generic_strike`, `GFX_report_event_worker_protests` |
| Суд, процесс | `GFX_report_event_gre_trial`, `GFX_report_event_soviet_purge_trial`, `GFX_Azov_Trials` |
| Дебаты, пресс-конференция | `GFX_report_event_journalists_speech`, `GFX_report_event_generic_conference`, `GFX_generic_meeting_room` |
| Договор, подписание | `GFX_report_event_generic_sign_treaty1/2/3`, `GFX_report_event_generic_handshake`, `GFX_report_event_canada_treaty` |
| Олигархи | `GFX_Generic_Oligarchs` (наши `GFX_UKR_rada_oligarchy`, `GFX_UKR_big_corruption_scandal`, `GFX_UKR_it_growth` и другие `GFX_UKR_*` определены в нашем `interface/UKR_event_pictures.gfx`, а не в TFR) |
| Прощание, траур | `GFX_report_event_generic_funeral`, `GFX_report_event_europe_funeral` |
| Парад, армия | `GFX_report_event_generic_military_parade`, `GFX_report_event_soldiers_marching`, `GFX_Generic_Marching1/2` |
| Пожар, катастрофа | `GFX_generic_fire`, `GFX_report_event_airplane_crash`, `GFX_news_event_kiev_ruins` |
| Пандемия | `GFX_Generic_COVID1` |
| Земля, сельское хозяйство | `GFX_generic_exploit_land` |

**Картинки Украины в TFR** (можно брать как есть): события - `GFX_ukraine_election_zelensky`, `GFX_ukraine_election_poroshenko`, `GFX_ukraine_election_biletsky`, `GFX_ukraine_war`, `GFX_Battle_of_Kiev`, `GFX_Battle_of_Odessa`, `GFX_ghost_of_kyiv`, `GFX_Kiev_Offensive`, `GFX_Kiev_Riots`, `GFX_Ukrainian_Uprising`, `GFX_Ukrainian_Insurgent_Army`, `GFX_Stepan_Bandera`, `GFX_Volodymyr_Zelensky`, `GFX_war_zelensky`, `GFX_drip_zelensky`, `GFX_Azov_Trials`, `GFX_NO_MORE_AZOV`, `GFX_Generic_Azov`, `GFX_donbass_recognition`, `GFX_GER_lviv_news`, `GFX_GER_odessa_news`, `GFX_GER_second_odessa_news`, `GFX_GER_donetsk_news`, `GFX_Ukraine_War_Intervention`; идеи - `GFX_idea_UKR_Corruption`, `UKR_Military_Corruption`, `UKR_Mass_insurgency`, `UKR_Embargoed_Economy`, `UKR_orthodox_schizm`, `UKR_to_the_last`, `UKR_kiev_counter_offensive`, `UKR_healthy_patriotism_idea` и др. (всего 31 идея); идеологии - `GFX_ideology_UKR_neoliberalism`, `GFX_ideology_UKR_sovereign_democracy_auth_dem`; модификаторы - `GFX_modifiers_UKR_russian_speaking_majority_region`, `..._russian_ghetto`; черты - `GFX_trait_trait_UKR_hero_ukraine`; портреты - `GFX_portrait_Stepan_Bandera`; Новороссия и Донбасс (`GFX_idea_NOV_*`, `GFX_idea_DPR_donetsk_economy`).

Выбор картинки не требует новой графики; в разделе «Нужен арт» `CLAUDE.md` можно заменить временные `GFX_report_event_ukrainian_civil_war` на строки этой таблицы.

---

## 3. Фокусы, идеи, решения: иконки (код)

- Иконки фокусов TFR: `GFX_focus_<ТЕГ>_<имя>` (31 имя связаны с Украиной: `GFX_focus_SOV_russify_kiev`, `GFX_focus_GER_aid_ukraine`, `GFX_focus_FRA_Cement_Ukrainian_Crimea` и др.), общие - `GFX_focus_generic_*` (76 штук). Ванильные `GFX_goal_generic_*` в TFR не определяются (они из самой игры); поэтому для наших временных иконок остаются ванильные.
- Иконки идей: `GFX_idea_<имя>`; в `picture` короткое имя или полное? В TFR 6220 значений короткие (`picture = SAU_petro_dollar` → `GFX_idea_SAU_petro_dollar`) и 565 полных (`picture = GFX_idea_UKR_to_the_last`); подтверждено, что короткая форма работает (5601 из 6220 разрешаются через префикс), для полной в 204 случаях найден точный спрайт. Какой из вариантов безопасен - выясните в игре (`TFR_SYNC.md`, раздел 3, пункт 3); `CLAUDE.md` требует короткую.
- Иконки решений: `GFX_decision_<имя>`; в TFR 59 общих `GFX_decision_generic_*`, 137 `GFX_decision_category_*`.
- Иконки модификаторов (динамических): `GFX_modifiers_<имя>`, 127 штук.
- Логотипы разведки: `GFX_intelligence_agency_logo_<имя>` (42; формат кадров - `CLAUDE.md`).
- Портреты: `GFX_portrait_*` - 1681 в TFR (только для окон событий). Портреты лидеров в `common/characters` указываются путём к файлу (`gfx/leaders/UKR/...`), а не спрайтом.

---

## 4. Окна и scripted_gui (код)

В TFR 32 файла `scripted_guis`: `TFR_scripted_guis_ZZZ_economy.txt` (окно экономики с ИИ: `ai_enabled = { has_content_tag = yes }`, банк, автоплатёж, экономические действия), `TFR_economy_ledger.txt`, `00_political_parties.txt` (индикатор популярности партии в верхней панели `party_popularity_number`, окно крыльев `TFR_ruling_party_wings_GUI`), `TFR_hog_gui.txt` (значок главы правительства, флаг `head_of_gov_ui_enabled`), `TFR_peace_popup.txt`, `TFR_startup_menu.txt`, `TFR_FBI_gui.txt` (досье страны), `TFR_nato_gui.txt`, `war_escalation_scripted_gui.txt`, а также окна SOV, GER, USB, USC и др.

Каркас (код; наш `UKR_war_mood_gui.txt` ему следует):
```
scripted_gui = {
	UKR_имя = {
		context_type = player_context      # или decision_category, selected_country_context
		window_name = "ИМЯ_окна_в_.gui"
		parent_window_token = top_bar      # куда вешается окно
		ai_enabled = { always = no }
		visible = { ... }                  # показывать ли окно
		properties = { ... }               # привязки элементов к данным
		effects = { кнопка_click = { ... } }   # действия при нажатии
		triggers = { элемент_visible = { ... } }  # условия видимости элементов
	}
}
```
Правила: имя окна и элементов с префиксом `UKR_`; `.gui` и `.gfx` в `interface/` только в файлах `UKR_*.gui/.gfx` (иначе замена файла TFR; `CLAUDE.md`); `parent_window_token` брать из существующих токенов TFR (`top_bar`, `decision_category_entry`, `selected_country_view_diplomacy`, `ruling_party_wings_bg_anchor`).

---

## 5. Решения и категории (код)

- Категория решений (ключи, количество в TFR): `icon` (356), `allowed` (360), `visible` (328), `visible_when_empty` (263), `priority` (192), `picture` (95), `scripted_gui` (28), `on_map_area` (19), `custom_icon` (9). Опечатка TFR `pciture` (3 раза) - ошибка в их коде.
- Категория показывается, если выполнено нужное условие (`visible = { has_completed_focus = X }`), для пустой категории задаётся `visible_when_empty = yes`.
- Каркас решения, статистика по стоимости/длительности, миссии - `TFR_CHEATSHEET.md`, раздел 7.
- Есть общий блок экономических действий (`print_money`, `war_taxes`, `develop_state`, ...): они вызываются из окна экономики (scripted GUI), а не из решений; триггеры лежат в `TFR_scripted_triggers_ZZZ_economic_actions.txt`.

---

## 6. Карта интерфейса TFR (для ориентира)

- `interface/*.gfx`: 160 файлов описаний спрайтов, 163 `.gui`. Ключевые для нас: `TFR_ideas.gfx` (иконки идей), `TFR_goals.gfx` + `TFR_goals_shine.gfx` (иконки фокусов и их пары `_shine`), `TFR_decisions_category.gfx`, `TFR_decisions_picture.gfx`, `TFR_interface_decisions*.gfx`, `TFR_event_pictures.gfx`, `eventpictures.gfx`, `TFR_interface_texticons*.gfx`, `TFR_countrypoliticsview_ideologies.gfx` (картинки подидеологий для окна политики; у Украины `GFX_ideology_UKR_neoliberalism`, `..._sovereign_democracy_auth_dem`), `frontendgamesetupview.gui/.gfx` (меню выбора страны; наш блок `backdrop_6` и `GFX_UKR_intro`).
- `core.gfx` содержит цвета текста и шрифты (`textcolors`, `bitmapfont`); **заменять его нельзя**.
- `common/focus_inlay_windows`, `common/continuous_focus`, `common/bop`: окна поверх дерева фокусов и шкалы баланса сил (см. `TFR_CHEATSHEET.md`, 4.5).
