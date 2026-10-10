# TFR_POLITICS.md - партии, популярность, коалиции и выборы в TFR

Справочник для блоков 1-3 (выборы в Раду 2023, президентская кампания 2024, опоры). Составлен 10.10.2026 по полному референсу (`TFR v1.2025.0b`). Помечено **(код)** - прочитано в определении эффекта или файла; **[ПРОВЕРИТЬ]** - вывод по аналогии. Что TFR делает с Украиной - `TFR_UKRAINE_HOOKS.md`; экономика и движок - `TFR_ENGINE.md`; перечни идеологий и подидеологий - `TFR_CHEATSHEET.md` (раздел 4) и `TFR_CATALOG.md`.

---

## 1. Что такое «партия» в TFR (код)

- Партий **11** (они же идеологические группы HOI4): `totalitarian_socialist`, `communist`, `libertarian_socialist`, `social_democrat`, `social_liberal`, `market_liberal`, `conservative`, `authoritarian_democrat`, `nationalist`, `fascist`, `national_socialist`. У каждой страны одна «партия» на идеологию, а **имя** партии берётся из локализации: `<ТЕГ>_<идеология>_party` (короткое) и `<ТЕГ>_<идеология>_party_long` (длинное). Менять названия в игре: `set_party_name = { ideology = X name = KEY long_name = KEY_long }`.
- Лидер и подидеология: `country_leader = { ideology = <подидеология> }` (180 подидеологий, `TFR_CATALOG.md`, раздел 2); подидеология показывается строкой в окне политики через скриптовую локализацию `GetIdeologySubtype` (`TFR_subideology_scripted_loc.txt`): например, у Зеленского с подидеологией `neoliberalism` выводится ключ `UKR_liberal_oligarchy`. Новый текст подтипа требует блока `text = { trigger = ... localization_key = ... }` в этом файле. Файл у нас **не заменён** (`TFR_SYNC.md`, раздел 1), а допустимо ли добавлять блоки в `defined_text` с тем же именем из своего файла, неизвестно [ПРОВЕРИТЬ]. Решение по умолчанию: пользоваться существующими подидеологиями (CLAUDE.md).
- Партии Украины, как их называет сам TFR (`TFR_country_localisation_UKR_l_*`):

| Идеология | Партия в TFR |
|---|---|
| `social_liberal` | «Слуга народа» (`UKR_social_liberal_party`) |
| `market_liberal` | «За будущее» (`UKR_market_liberal_party`) |
| `conservative` | «Европейская солидарность» (`UKR_conservative_party`) |
| `authoritarian_democrat` | ОП-ЗЖ (`UKR_authoritarian_democrat_party`) |
| `social_democrat` | Радикальная партия Ляшко |
| `libertarian_socialist` | «Союз левых сил» (`UKR_libertarian_socialist_party`, ULF) |
| `communist` | КПУ |
| `totalitarian_socialist` | ПСПУ |
| `nationalist` | ВСУ (`UKR_nationalist_party`, как «партия армии») |
| `fascist` | «Национальный корпус» |
| `national_socialist` | «Свобода» |
| дополнительные | `UKR_medvechyk_party` («Новая партия регионов»), `UKR_murayev_party` («Сила людей»), `UKR_korolevskaya_party` («Украина - вперёд!»), `UKR_plp(_short)` («Платформа за жизнь и мир»); их выдают события «Свободные выборы в Украине» (`russia.451`) и победа Медведева |

Наши блоки уже опираются на эти имена («Слуги народа» + «За будущее» в 2023). Менять `UKR_*_party` ключи не нужно, достаточно `set_party_name` при сюжетных переименованиях.

---

## 2. Популярность

### 2.1. Как её меняет TFR
- Основной способ - **`add_popularity = { ideology = X popularity = 0.05 }`** (долю): 5027 вхождений в TFR. Так делает почти весь контент (деревья SOV Медведева: 170 вхождений).
- Обёртки `add_<идеология>_popularity = yes` + `<идеология>_popularity_var_temp = N` (11 штук, файл `00_TFR_scripted_effects_ZZZ_popularity.txt`) встречаются всего 152 раза (США, АТВ, ГЕР и т. п.). У них **затухание прироста** (код): при `N > 0` прирост умножается на
  - `x < 0.33` - ×1.0 (полный);
  - `0.33 ≤ x < 0.5` - ×0.66;
  - `0.5 ≤ x < 0.66` - ×0.5;
  - `0.66 ≤ x < 0.75` - ×0.34;
  - `x ≥ 0.75` - ×0.25,
  где `x` - текущая популярность этой идеологии; отрицательные приросты не затухают. Плюс показывается красивый тултип `add_<идеология>_popularity_tooltip`. Для APA вызывается `APA_popularity_change`.
- `add_ruling_party_popularity = yes` (читает `ruling_popularity_var_temp`) прибавляет популярность правящей партии через соответствующую обёртку (для текущего `has_government`).
- `change_ruling_party_popularity` (читает `ideology_change_var`; если по модулю больше 1, считает как проценты: умножает на 0.01).
- Для нас: `add_popularity` остаётся нормой (как у TFR). Затухающие обёртки нужны, если хотим «потолок» популярности (например, чтобы «Слуга народа» не залетал выше 0.75 одним событием).

### 2.2. Популярность → политсила и стабильность
- Модификатор **`party_popularity_dynamic_modifier`**: `political_power_gain = party_popularity@ruling_party` (код, `00_TFR_dynamic_modifiers_ZZZ_generic.txt`). То есть **прирост политсилы страны (в долях) равен популярности правящей партии** (базовый приход - `NPolitics.BASE_POLITICAL_POWER_INCREASE = 1.5` в день).
- К нему прибавляются **коалиция** (`party_popularity_dynamic_modifier_coalition`: `political_power_gain = coalition_pp_gain`) и **крылья правящей партии** (`..._ruling_party_wings`: `ruling_party_wings_pp_gain`). Пересчёт раз в неделю (`on_weekly` → `update_party_popularity`, код):
  - `coalition_pp_gain = 0.5 × Σ party_popularity партнёров (массив coalition_partners_array)`;
  - `ruling_party_wings_pp_gain = 0.9 × Σ party_popularity крыльев (массив ruling_party_wings_array)`.
  Пример: правящая `social_liberal` 0.5, в коалиции `market_liberal` 0.2, крыло `conservative` 0.1: `+0.5 + 0.5×0.2 + 0.9×0.1 = +0.69` к приросту политсилы.
- Стабильность от популярности: `BASE_STABILITY_PARTY_POPULARITY_FACTOR = 0` в defines, поэтому вклад идёт только через ключ `party_popularity_stability_factor` у идей (шпаргалка, раздел 9).
- `map_party_popularity_PP_gain_to_ideology` (читает `political_power_ideology_var = token:X`): прирост политсилы считается по популярности **другой** идеологии, а не правящей (нужно, когда правящая «вывеска» не совпадает с реальной опорой). Снимает: `disable_party_popularity_PP_gain` (убирает оба динамических модификатора), восстановление - `default_party_popularity_PP_gain`.

---

## 3. Коалиция и крылья: полный API (код)

```
set_temp_variable = { coalition_partner_var_temp = token:market_liberal }
add_to_coalition = yes          # добавить партнёра (в массив coalition_partners_array,
                                # флаг переменной is_in_coalition_with_<идеология> = 1,
                                # динамический модификатор party_popularity_dynamic_modifier_coalition)
remove_from_coalition = yes     # убрать (читает ту же временную переменную)
end_coalition = yes             # распустить всю коалицию

set_temp_variable = { ruling_party_wing_var_temp = token:conservative }
add_ruling_party_wing = yes     # крыло внутри правящей партии (массив ruling_party_wings_array)
remove_ruling_party_wing = yes
end_ruling_party_wings = yes
```

- Оба `add_*` проверяют, что идеология ещё не в списке и не является правящей (иначе тултип и эффект пропускаются), и в конце делают скрытый `add_ruling_party_popularity` с `0.001` (чтобы обновить интерфейс) и `update_party_popularity = yes`.
- Триггеры: `is_in_coalition`, `is_in_coalition_with_<идеология>`, `has_coalition_with_target`; интерфейс: `TFR_ruling_party_wings_GUI` и индикатор `party_popularity_number` в верхней панели (`00_political_parties.txt`).
- Для нашего «союза Слуг народа и За будущее» (2023) готовые средства: `add_to_coalition` с `token:market_liberal` и коалиционная выплата политсилы; распад союза - `remove_from_coalition`. Не нужно делать собственный механизм.
- Сохранение и откат политики: `get_current_government_type` (запоминает правящую идеологическую группу в `original_government_type`, все 11 популярностей в `original_popularities`, коалицию в `original_coalitions`, флаг выборов и тип подчинения) и `restore_previous_government_type` (возвращает всё, включая `set_popularities`). Годится для «временной» смены режима (например, кризис с последующим возвратом). Параметры хранятся в переменных, так что вложенно использовать нельзя.

---

## 4. Выборы: как это устроено (код)

1. **Нет общего механизма.** `TFR_on_actions_ZZZ_elections.txt` содержит только `on_new_term_election` для США (`usa.90`); у Германии, USB, USC - свои. Для Украины, Беларуси, Молдовы и остальных выборы - **отдельные события** с таймером: `on_startup` планирует `country_event = { id = X days = N }`.
2. **Паттерн события выборов** (пример: `belarus.1`, `ukraine.13`):
   - заголовок/описание/опции;
   - в опциях `hidden_effect` с `random_list` (веса исходов, у каждого `modifier = { factor = 0 has_game_rule = { rule = ... option = ... } }`, чтобы правило игры отключало ненужный исход);
   - результат: `set_politics = { ruling_party = X elections_allowed = yes/no last_election = "Г.М.Д" election_frequency = 48 }`, `add_popularity`, `set_party_name`, `add_timed_idea` (дух на 150-200 дней), `set_portraits`, `news_event`, смена лидера;
   - в конце цепочки - «новость» (`news_event`).
3. **Игровые правила** (`has_game_rule`, `common/game_rules/00_game_rules.txt`) позволяют игроку выбрать исход (`UKR_election_24`, `BLR_20_election`, `The_MOL_2020_election` и т. д.). Для нашего мода своё правило не нужно (исход для игрока - выбор опции, для ИИ - `ai_chance`).
4. Параметры `set_politics`: `last_election` строкой `"2019.4.21"` (формат `"Г.М.Д"`), `election_frequency` в **месяцах**. Если `elections_allowed = yes`, игра сама вызовет `on_new_term_election` в момент, когда пройдёт период; для Украины обработчика нет, поэтому ванильные «выборы» ничего не делают, кроме обновления даты (`TECH_DEBT.md`, TD-17: мы сдвигаем `last_election`, чтобы они не совпали с нашими событиями).
5. **Результаты выборов не считаются автоматически.** Победитель, коалиция и перераспределение популярностей - всегда явные эффекты в событии (`set_politics`, `add_popularity`, `add_to_coalition`, `set_party_name`).
6. Количественный ориентир по `belarus.1`/`belarus.2`: победа на выборах сопровождается `add_popularity` +0.25...+0.36, `add_stability -0.2` при кризисе, на 150-200 дней идея-дух («Демократизация Беларуси», «Подавление оппозиции»).

**Рецепт для выборов в Раду 2023** (в соответствии с `DESIGN.md`, 5):
1. Подготовка: события с `add_popularity` для социал-либералов, `market_liberal`, консерваторов, `nationalist`, левых; духи сезона (уже есть).
2. День выборов 29.10.2023: событие `ukraine_politics.1xx` со всеми расчётами популярностей и `set_variable` результата.
3. Формирование: `add_to_coalition` с `token:market_liberal`.
4. Через 2-6 месяцев: слухи, распад (`remove_from_coalition`, `add_popularity`) - как в `DESIGN.md`.
5. Не вызывать ванильные выборы: поставить `last_election` так, чтобы следующее ванильное окно не совпало (как уже сделано).

---

## 5. Правящая партия и режим (код)

- `has_government = X` проверяет **правящую идеологическую группу** (`current_party_ideology_group`), а не тип государства (`ZZZ_*`, `TFR_ENGINE.md`, 1.6). Три разных слоя: идеологическая группа (партия), подидеология лидера (`country_leader = { ideology = Y }`), тип государства и тип экономики (идеи `ZZZ_*`).
- Смена правящей: `set_politics = { ruling_party = X ... }`. Дополнительно для восстановления реальных значений часто требуется `add_popularity` на ту же идеологию (иначе игра вернёт прежнюю по текущим долям при следующем пересчёте: правящая партия задаётся скриптом, а не расчётом).
- Смена лидера: `add_country_leader_role = { character = X promote_leader = yes country_leader = { ideology = Y expire = "1.1.1.1" traits = {...} } }`; затем при необходимости `retire_country_leader`, `kill_country_leader`. Черты главы государства (`hos_*`) - `add_country_leader_trait`, `swap_ruler_traits`.
- Для опор блока 3 хорошо сходятся существующие подидеологии: см. `TFR_CHEATSHEET.md`, 4.1 (список «полезное для Украины»).
- **TFR сам перекраивает политику Украины после победы НАТО** в зависимости от текущего лидера (Зеленский / Порошенко / Залужный) и доли `authoritarian_democrat > 19`; подробности и риск наложения на наши блоки - `TFR_UKRAINE_HOOKS.md`, 5.4. Бойко и «Платформа за жизнь и мир» прописаны в победе Медведева (`TFR_UKRAINE_HOOKS.md`, 5.3).

---

## 6. Другие политические системы TFR, которые Украину не касаются

- **Россия (SOV):** полный блок легитимности, одобрения, партий (`SOV_add_party_*`, `SOV_update_party_legitimacy`...), окно в `TFR_scripted_guis_SOV.txt`. Для UKR не использовать (`TFR_CHEATSHEET.md`, 12).
- **Германия:** парламент Бундестага (партии, поддержка, `GER_has_*_popularity_*`), ЕС (`GER_add_eu_*`).
- **США и Китай:** собственные шкалы влияния и фракций (`USA_*`, `USB_*`, `PRC_*`).
- **Влияние держав** (`Russian_Influence`...): переменные есть, механики-потребителя нет (`TFR_ENGINE.md`, 4).
- **Парламент Украины** в TFR не моделируется; «места» не нужны: популярность партий показываем процентами (`CLAUDE.md`).
