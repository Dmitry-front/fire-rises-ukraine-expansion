# Темы подбора картинок для _tools/art_map.py (выполняется внутри art_map.py, ART_THEMES уже есть).
# T(название, регулярка по русскому тексту (нижний регистр), слова в именах спрайтов TFR, [готовые спрайты]).
# Готовые спрайты - проверенные по _tools/tfr_index или interface/UKR_event_pictures.gfx; несуществующие
# art_map.py отбрасывает и печатает предупреждение. Дополняйте темы по мере работы.
def T(name, rx, words, ready):
    ART_THEMES.append((name, rx, words, ready))

T('выборы', r'выбор|голосован|бюллетен|избирател|кандидат|тур[а-я]* |рейтинг',
  ['election', 'vote', 'ballot', 'campaign'],
  ['GFX_UKR_2024_election', 'GFX_UKR_2019_election', 'GFX_report_event_election_vote', 'GFX_generic_elections', 'GFX_ukraine_election_zelensky'])
T('кампания, митинг в поддержку', r'кампани|стадион|предвыбор|агитац|штаб',
  ['campaign', 'rally'],
  ['GFX_FRA_campaign_rally', 'GFX_report_event_generic_rally', 'GFX_ukraine_election_zelensky'])
T('Рада, парламент', r'\bрад[аыуе]\b|парламент|фракци|депутат|поправк|закон',
  ['parliament', 'assembly', 'congress'],
  ['GFX_report_event_generic_parliament', 'GFX_UKR_rada_oligarchy', 'GFX_report_event_hungary_parliament'])
T('протест, улица, митинг', r'митинг|протест|улиц|демонстрант|шествие|акци[яи] |требует|забастов',
  ['protest', 'rally', 'riot', 'demonstration'],
  ['GFX_Generic_Protest', 'GFX_report_event_generic_rally', 'GFX_report_event_gathering_protest', 'GFX_Generic_Riot', 'GFX_UKR_protest_land_reform'])
T('майдан, революция', r'майдан|революци|достоинств|граните|восстани',
  ['riot', 'uprising', 'revolt', 'revolution'],
  ['GFX_Kiev_Riots', 'GFX_Ukrainian_Uprising', 'GFX_Generic_Riot'])
T('суд, дело, обыски', r'\bсуд|дело|вакс|набу|обыск|следстви|приговор|обвин|прокурор|прокуратур|заседани',
  ['court', 'trial', 'judge', 'justice', 'police'],
  ['GFX_report_event_gre_trial', 'GFX_rus_court', 'GFX_Supremecourt', 'GFX_UKR_big_corruption_scandal', 'GFX_UKR_ministr_avakov_scandal'])
T('коррупция, скандал, утечка', r'коррупц|скандал|утечк|слив|разоблач|публикаци|взятк|расследован',
  ['corrupt', 'scandal', 'leak', 'newspaper'],
  ['GFX_UKR_big_corruption_scandal', 'GFX_SOV_busted_corruption', 'GFX_UKR_ministr_avakov_scandal'])
T('олигархи, кланы, бизнес', r'олигарх|клан|приват|металл|энергетик|бизнес|концерн|холдинг|коломойск|ахметов|акционер',
  ['oligarch', 'business', 'steel', 'bank'],
  ['GFX_Generic_Oligarchs', 'GFX_UKR_rada_oligarchy', 'GFX_PRC_oligarchs_event'])
T('прощание, траур, память', r'прощани|траур|похорон|памят|погиб|имён|имена|героев|поле марса|мемориал',
  ['funeral', 'mourning', 'memorial'],
  ['GFX_report_event_generic_funeral', 'GFX_report_event_europe_funeral', 'GFX_report_event_poland_funeral'])
T('война, фронт, бои', r'бо[йи] |боев|фронт|наступлен|обстрел|ракет|штурм|оборон|контрнаступ',
  ['battle', 'war', 'offensive', 'combat'],
  ['GFX_event_UKR_stop_enemy', 'GFX_event_UKR_effect_of_war', 'GFX_ukraine_war', 'GFX_Kiev_Offensive', 'GFX_Generic_City_Combat', 'GFX_report_event_generic_battle', 'GFX_ghost_of_kyiv'])
T('освобождение города', r'освобожд|вернул контроль|вновь под украинск|вошли в',
  ['liberation', 'victory'],
  ['GFX_Generic_Border_Victory', 'GFX_report_event_french_liberation', 'GFX_Battle_of_Kiev'])
T('Киев, города', r'\bкиев|харьков|одесс|львов|днепр|запорож|херсон|сумы|чернигов|житомир',
  ['kiev', 'kyiv', 'odessa', 'lviv'],
  ['GFX_Battle_of_Kiev', 'GFX_Battle_of_Odessa', 'GFX_news_event_kiev_ruins'])
T('разрушения, восстановление', r'восстановлен|руин|разрушен|развал|эхо|орудия смолкли',
  ['ruins', 'reconstruction', 'destroyed'],
  ['GFX_event_UKR_war_destruction', 'GFX_UKR_big_construction_event', 'GFX_report_event_generic_ruins', 'GFX_news_event_kiev_ruins'])
T('ядерный вопрос, Будапешт', r'ядерн|будапешт|меморандум|бомб',
  ['nuclear', 'nuke', 'atomic'],
  ['GFX_UKR_budapest_memorandum', 'GFX_event_nuke', 'GFX_generic_nuclear_power_plant'])
T('Брюссель, ЕС, Запад', r'брюссел|\bес\b|евросоюз|европейск|запад|вашингтон|финанс.* помощ|транш',
  ['european', 'brussels', 'eu', 'euro'],
  ['GFX_European_Union', 'GFX_GER_brussels_news', 'GFX_UKR_diplomat', 'GFX_UKR_investment_forum'])
T('Москва, Россия, переговоры', r'москв|кремл|росси|переговор|диалог|мир[ау]? |миротвор',
  ['moscow', 'kremlin', 'talks', 'negotiations', 'peace'],
  ['GFX_Generic_Negotiations', 'GFX_SOV_ukraine_talks', 'GFX_UKR_report_RF_attack2014', 'GFX_Mishustin_and_Putin'])
T('Беларусь', r'беларус|минск|лукашенк',
  ['belarus', 'minsk'],
  ['GFX_UKR_help_BLR', 'GFX_belarus_protest', 'GFX_Generic_Lukashenko'])
T('Польша, Венгрия, соседи', r'варшав|польш|венгр|будапешт|орбан|румын|молдов',
  ['poland', 'hungary', 'budapest', 'warsaw'],
  ['GFX_Polish_Border', 'GFX_Generic_Orban', 'GFX_Hungarian_Diplomat', 'GFX_UKR_diplomat'])
T('церковь, религия', r'церков|храм|православн|епифани|патриарх|богослуж',
  ['church', 'orthodox', 'religion'],
  ['GFX_SOV_russian_church', 'GFX_Abandoned_Church', 'GFX_SOV_orthodox_army'])
T('цифра, Дія, дроны, кибер', r'цифров|\bдія\b|дия|дрон|кибер|хакатон|приложени|смартфон|онлайн|электронн|е-голос',
  ['digital', 'cyber', 'drone', 'computer', 'internet'],
  ['GFX_UKR_digital_state', 'GFX_UKR_it_growth', 'GFX_PRC_drone_uav'])
T('телевидение, эфир, соцсети', r'телемарафон|эфир|\bтв\b|телевиз|ток-шоу|ролик|реклам|соцсет|чат|журналист|пресс|канал|\bсми\b|1\+1',
  ['media', 'tv', 'television', 'broadcast', 'press', 'journalists'],
  ['GFX_generic_media', 'GFX_report_event_journalists_speech', 'GFX_USB_white_house_media_room'])
T('дебаты, форум, съезд, совещание', r'дебат|форум|съезд|конвент|комисси|совещани|обед|ужин|встреч|заседани|саммит|конференц',
  ['conference', 'meeting', 'congress', 'summit', 'debate'],
  ['GFX_report_event_generic_conference', 'GFX_generic_meeting_room', 'GFX_report_event_journalists_speech', 'GFX_UKR_investment_forum'])
T('кабинет, назначения, министры', r'кабинет|премьер|министр|назначени|правительств|портфел|команда',
  ['cabinet', 'government', 'ministers'],
  ['GFX_National_Unity_Government', 'GFX_generic_meeting_room', 'GFX_report_event_gre_cabinet_meeting'])
T('инаугурация, присяга', r'инаугураци|присяг|вступлени[ея] в должност',
  ['inauguration', 'oath'],
  ['GFX_USB_inauguration_day', 'GFX_UKR_2024_election'])
T('ветераны, добровольцы, армия', r'ветеран|доброволц|армия|военн|комбат|командир|мобилизац|призыв|служб[аы]',
  ['veterans', 'soldiers', 'army', 'volunteers'],
  ['GFX_event_UKR_volunteers', 'GFX_event_UKR_successful_mobilization', 'GFX_UKR_preparing_for_war', 'GFX_AST_Veteran_March', 'GFX_FRA_veterans', 'GFX_Generic_Marching1'])
T('закупки, склады, снабжение', r'закупк|склад|снабжен|поставщик|контракт|боеприпас|логистик|оборонзаказ',
  ['factory', 'supply', 'logistics', 'trucks'],
  ['GFX_report_event_generic_factory', 'GFX_report_event_generic_truck', 'GFX_report_event_generic_lend_lease', 'GFX_UKR_big_construction_event'])
T('шахтёры, рабочие, заводы', r'шахт|кривбасс|кривой рог|рабоч|завод|тариф|зарплат|профсоюз|горняк',
  ['workers', 'strike', 'factory', 'miners'],
  ['GFX_report_event_generic_strike', 'GFX_report_event_worker_protests', 'GFX_report_event_generic_factory'])
T('левые, профсоюзы, Первомай', r'левы|коммунист|социалист|первомай|красн[а-я]* лини|труд|профсоюз',
  ['communist', 'socialist', 'left', 'workers'],
  ['GFX_report_event_generic_communist_congress', 'GFX_report_event_communists_cheer', 'GFX_Generic_Reformer_Rally'])
T('правые, националисты, ультра', r'националист|правы[ех]|ультра|азов|корпус|колонн|факел|мова|язык',
  ['nationalist', 'azov', 'far', 'right'],
  ['GFX_Generic_Azov', 'GFX_Ukrainian_Insurgent_Army', 'GFX_Stepan_Bandera'])
T('история Украины', r'1918|1919|1921|1985|1989|1990|1991|крут[ыа]|холодн[а-я]* яр|стус|\bрух\b|независимост',
  ['ukrainian', 'independence', 'uprising', 'soviet'],
  ['GFX_UKR_independence', 'GFX_Ukrainian_Insurgent_Army', 'GFX_Ukrainian_Uprising', 'GFX_Stepan_Bandera'])
T('граница, паспорта, беженцы', r'паспорт|граница|граждан|беженц|вид на жительство|миграц',
  ['border', 'passport', 'refugee'],
  ['GFX_Polish_Border', 'GFX_SOV_refugee_camp', 'GFX_Generic_Border_Victory'])
T('референдум, конституция', r'референдум|конституц|вертикал|конституцион',
  ['referendum', 'constitution'],
  ['GFX_SOV_putin_constitution_referendum', 'GFX_SOV_good_constitution_referendum'])
T('юмор, быт, кафе, футбол', r'борщ|пив[оа]|кофе|бариста|вышиванк|футбол|сборн|матч|мем',
  ['cafe', 'football', 'beer', 'food'],
  [])
T('Эстония, Литва, Латвия', r'кайтселийт|союз стрелков|земессардзе|эстони|литв|латви|балт',
  ['baltic', 'estonia', 'lithuania', 'latvia'],
  ['GFX_report_event_baltic_entente', 'GFX_report_event_latvian_soldiers', 'GFX_report_event_lithuania_army'])

# Города: у нас есть арт «потерян» для каждого города (смысл обратный, но это местные кадры города).
for _rx, _city, _spr in [(r'\bкиев', 'Киев', 'Kyiv'), (r'харьков', 'Харьков', 'Kharkov'), (r'\bсум[ыа]', 'Сумы', 'Sum'),
                         (r'чернигов', 'Чернигов', 'Chernigov'), (r'запорож', 'Запорожье', 'Zaporozhye'),
                         (r'херсон', 'Херсон', 'Kherson'), (r'днепр', 'Днепр', 'Dnipro'), (r'житомир', 'Житомир', 'Zhytomyr'),
                         (r'одесс', 'Одесса', 'Odessa'), (r'львов', 'Львов', 'Lviv'), (r'полтав', 'Полтава', 'Poltava')]:
    T('город: %s (наш арт «потерян»)' % _city, _rx, [_city.lower()], ['GFX_event_UKR_war_%s_lost' % _spr])

# Дополнительные темы (по неохваченным событиям)
T('МВД, силовики, контрразведка', r'мвд|нацгвард|полици|силов|сбу|контрразвед|разведк|аваков|малюк|секрет',
  ['police', 'security', 'spetsnaz', 'intelligence'],
  ['GFX_UKR_ministr_avakov_scandal', 'GFX_UKR_ministr_avakov_leave', 'GFX_Generic_National_Guard', 'GFX_Generic_SOBR'])
T('газ, зима, энергетика', r'газ[а-я]* |облгаз|зим[аы]|тариф|отоплен|энергет|свет[а-я]* |блэкаут|электричеств',
  ['gas', 'energy', 'winter', 'oil', 'power'],
  ['GFX_UKR_energy_crisis', 'GFX_Moscow_Winter', 'GFX_generic_nuclear_power_plant'])
T('письмо, адвокаты, экстрадиция, Вена', r'письм|адвокат|выдач|экстрадиц|вен[аы]|юрист|нота',
  ['diplomat', 'letter', 'court', 'trial'],
  ['GFX_UKR_diplomat', 'GFX_report_event_finnish_letter', 'GFX_report_event_gre_trial'])
T('кризис, распад, падение', r'кризис|распад|падени|крах|развал|плен|восстани[ея] элит|раскол|отставк',
  ['collapse', 'crisis', 'coup', 'fall'],
  ['GFX_Generic_Collapse', 'GFX_UKR_status_economy', 'GFX_UKR_big_corruption_scandal'])
T('ближний круг, Офис, власть', r'ближн[а-я]* круг|офис|вертикал|\bвласть|временно исполняющ|списки|назначени|окружени',
  ['government', 'cabinet', 'president'],
  ['GFX_generic_meeting_room', 'GFX_UKR_rada_oligarchy', 'GFX_Volodymyr_Zelensky'])
T('Зеленский, президент', r'зеленск|президент[а-я]* |глав[аы] государства',
  ['zelensky', 'president'],
  ['GFX_Volodymyr_Zelensky', 'GFX_war_zelensky', 'GFX_ukraine_election_zelensky'])
T('встреча с избирателями, регионы', r'встреч[аи] с избирател|полтавщин|регион|громад|село|сельск|пенсионер',
  ['rally', 'villagers', 'peasants', 'campaign'],
  ['GFX_FRA_campaign_rally', 'GFX_UKR_agricultural_success', 'GFX_report_event_peasant_revolt'])
T('анархисты, Махно, самоуправление', r'махно|анарх|кооператив|самоуправлен|гуляйполе|фестивал',
  ['anarchist', 'peasant', 'cooperative'],
  ['GFX_Anarchist_Meeting', 'GFX_report_event_spr_anarchists', 'GFX_report_event_peasant_revolt'])
T('НАТО', r'нато|альянс|членств',
  ['nato'],
  ['GFX_UKR_status_NATO', 'GFX_Generic_NATO'])
T('Кубань, Россия, аннексия', r'кубан|казак|аннекс|присоедин',
  ['cossack', 'kuban', 'russia'],
  ['GFX_report_event_SOV_cossack_cavalry', 'GFX_UKR_report_RF_attack2014'])
T('выборы: итоги, жалоба', r'после .*тура|итог|подсчёт|протокол|жалоб|оспар|центризбирком|цик',
  ['election', 'vote'],
  ['GFX_report_event_election_vote', 'GFX_UKR_2024_election'])
T('портрет страны, итоги', r'портрет|итоги|республик|государство-|модель',
  ['news', 'report'],
  ['GFX_UKR_status_economy', 'GFX_UKR_rada_oligarchy'])
T('Ермак, опора, дело', r'ермак|опор[аыу]|межигор|бюро|ваке?с',
  ['corrupt', 'scandal', 'court'],
  ['GFX_UKR_big_corruption_scandal', 'GFX_UKR_ministr_avakov_scandal', 'GFX_report_event_gre_trial'])
