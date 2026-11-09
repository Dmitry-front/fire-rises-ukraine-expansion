# Польша (PLD): три запроса и две цепочки (зерно на границе, эксгумации). PROPOSAL_war_europe.md 4.1.
# Факты (реальный прототип) помечены [ПРОВЕРИТЬ] в DESIGN.md, журнал сессии 22.
from .fx import *

W_UPA = ('UKR = { has_country_flag = UKR_np_hero_upa }', -15)  # спор об УПА: Варшава осторожнее

REQ = [
	dict(
		key='pl_hub', tag='PLD', ev=300, res=310, base=40, cd=270, icon='generic_lend_lease',
		pic='GFX_event_UKR_war_support_NATO', scale=True,
		name=T('Просить Варшаву: транзитный хаб', 'Ask Warsaw: a transit hub'),
		desc=T(
			'Просим Польшу принимать союзные грузы на юго-востоке страны и перегружать их для Украины.\n\n'
			'§YЧто это.§! Узловые аэродромы и станции Подкарпатья. На границе меняется колея (в Европе 1435 мм, у нас 1520 мм), поэтому вагоны перегружают или меняют тележки.\n'
			'§YВ реальности.§! С февраля 2022 года через юго-восток Польши, в первую очередь через аэропорт Жешув-Ясёнка, шла значительная часть западной военной помощи; узел прикрывали силами союзников.\n'
			'§YЧто даст.§! Быстрее пополняются потери и склады, приходит техника тыла.',
			'We ask Poland to receive allied cargo in the south-east of the country and to transship it for Ukraine.\n\n'
			'§YWhat it is.§! The junction airfields and railway stations of the Subcarpathian region. The track gauge changes at the border (1435 mm in Europe, 1520 mm in Ukraine), so wagons are transshipped or have their bogies swapped.\n'
			'§YIn reality.§! From February 2022 a large share of Western military aid went through south-eastern Poland, above all through Rzeszow-Jasionka airport; allied forces covered the hub.\n'
			'§YWhat it gives.§! Losses and stockpiles are replenished faster, and rear-area equipment arrives.'),
		req_t=T('Просьба Киева: транзитный коридор', 'Kyiv\'s request: a transit corridor'),
		req_d=T('Украина просит открыть юго-восточные аэродромы и станции для союзных грузов и взять перегрузку на себя. Решение придётся защищать перед избирателями: узел может стать целью.',
			'Ukraine asks us to open the south-eastern airfields and stations to allied cargo and to take on the transshipment. The decision will have to be defended before voters: the hub can become a target.'),
		res_t=T('Ответ Варшавы: транзитный хаб', 'Warsaw\'s answer: the transit hub'),
		res_full=T('Варшава согласилась: аэропорт и станции Подкарпатья работают на союзные грузы круглосуточно. Составы идут в Украину без долгих остановок.',
			'Warsaw has agreed: the airport and the stations of the Subcarpathian region handle allied cargo around the clock. Trains cross into Ukraine without long stops.'),
		res_part=T('Польша открыла коридор не полностью: часть рейсов и составов принята, остальное по особому разрешению. Это лучше, чем ничего.',
			'Poland opened the corridor only in part: some flights and trains are accepted, the rest by special permission. It is better than nothing.'),
		res_no=T('Варшава отказала. В канцелярии опасаются, что узел станет целью, и просят вернуться к вопросу позже.',
			'Warsaw refused. The chancellery fears that the hub would become a target and asks us to return to the question later.'),
		weights=[W_UPA],
		full=[idea('UKR_pl_hub_idea', 365, lim='UKR_pl_hub_idea_lim', lim_days=180), eq('support_equipment_1', 60, 'PLD'),
			flag('UKR_pl_hub_open'), ev(320, 150)],
		part='auto',
	),
	dict(
		key='pl_arms', tag='PLD', ev=301, res=311, base=65, cd=150, icon='GFX_decision_generic_military_support',
		pic='GFX_Generic_Tank_column', scale=True,
		name=T('Просить Варшаву: оружие из польских арсеналов', 'Ask Warsaw: arms from Polish arsenals'),
		desc=T(
			'Просим Польшу передать часть техники и боеприпасов из собственных складов, пока промышленность союзников раскачивается.\n\n'
			'§YЧто это.§! Танки Т-72 и польские ПТ-91 «Твярды» (в польской армии с 1990-х), самоходные гаубицы 155 мм «Краб» (с середины 2010-х) и ПЗРК «Пёрун» (с 2010 года).\n'
			'§YВ реальности.§! В 2022 году Польша первой из НАТО передала более двухсот танков Т-72, затем самоходные гаубицы «Краб» и тысячи ПЗРК «Гром» и «Пёрун».\n'
			'§YЧто даст.§! Артиллерия, зенитные расчёты и бронетехника, которые можно двинуть в бой за недели.',
			'We ask Poland to hand over part of its equipment and ammunition from its own stores while allied industry gets up to speed.\n\n'
			'§YWhat it is.§! T-72 tanks and Polish PT-91 Twardy tanks (in the Polish army since the 1990s), 155 mm Krab self-propelled howitzers (since the mid-2010s) and Piorun man-portable air defence systems (since 2010).\n'
			'§YIn reality.§! In 2022 Poland was the first NATO member to hand over more than two hundred T-72 tanks, then Krab howitzers and thousands of Grom and Piorun launchers.\n'
			'§YWhat it gives.§! Artillery, air defence crews and armour that can be sent into battle within weeks.'),
		req_t=T('Просьба Киева: оружие из польских складов', 'Kyiv\'s request: arms from Polish stores'),
		req_d=T('Украина просит передать часть танков, самоходных гаубиц и зенитных комплексов из арсеналов Войска Польского. Военные предупреждают, что собственные склады опустеют.',
			'Ukraine asks us to hand over part of the tanks, howitzers and air defence systems from the arsenals of the Polish Army. The military warns that our own stores will run empty.'),
		res_t=T('Ответ Варшавы: оружие из арсеналов', 'Warsaw\'s answer: arms from the arsenals'),
		res_full=T('Варшава передала танки, самоходные гаубицы и зенитные комплексы из арсеналов Войска Польского. Колонны уже идут к границе.',
			'Warsaw has handed over tanks, howitzers and air defence systems from the arsenals of the Polish Army. The columns are already moving to the border.'),
		res_part=T('Польша передала только часть запрошенного: остальное нужно самой армии. Но танки и гаубицы уже идут к границе.',
			'Poland handed over only part of what was asked: the rest is needed by its own army. But tanks and howitzers are already moving to the border.'),
		res_no=T('Варшава отказала: министерство обороны считает запасы минимально допустимыми. Просьбу можно повторить позже.',
			'Warsaw refused: the defence ministry considers its stocks to be at the minimum acceptable level. The request can be repeated later.'),
		weights=[('UKR = { has_country_flag = UKR_np_hero_upa }', -20)],
		full=[eq('artillery_equipment_2', 60, 'PLD'), eq('anti_air_equipment_1', 80, 'PLD'), eq('modern_tank_equipment_1', 120, 'PLD')],
		part='auto',
	),
	dict(
		key='pl_medevac', tag='PLD', ev=302, res=312, base=35, cd=270, icon='GFX_decision_generic_army_support',
		pic='GFX_FRA_red_cross_ukraine', scale=False,
		name=T('Просить Варшаву: госпитали и эвакуация раненых', 'Ask Warsaw: hospitals and casualty evacuation'),
		desc=T(
			'Просим Польшу принимать наших раненых в своих госпиталях и организовать медицинскую эвакуацию через границу.\n\n'
			'§YЧто это.§! Эвакуационные поезда и самолёты, места в больницах Подкарпатья и других воеводств, реабилитация. Чем быстрее раненый попадает в госпиталь, тем выше шанс вернуть его в строй.\n'
			'§YВ реальности.§! Польша приняла более миллиона беженцев из Украины, а польские больницы лечили и раненых военных; эвакуацию координировали с ЕС и НАТО.\n'
			'§YЧто даст.§! На время часть потерь возвращается в строй.',
			'We ask Poland to admit our wounded to its hospitals and to organise medical evacuation across the border.\n\n'
			'§YWhat it is.§! Evacuation trains and aircraft, hospital beds in the Subcarpathian and other voivodeships, rehabilitation. The sooner a wounded soldier reaches a hospital, the better the chance of returning him to the ranks.\n'
			'§YIn reality.§! Poland took in more than a million refugees from Ukraine, and Polish hospitals also treated wounded servicemen; evacuation was coordinated with the EU and NATO.\n'
			'§YWhat it gives.§! For a time, part of the casualties return to the ranks.'),
		req_t=T('Просьба Киева: госпитали и эвакуация', 'Kyiv\'s request: hospitals and evacuation'),
		req_d=T('Украина просит принимать раненых военных и организовать эвакуацию через границу. Просьба ложится на плечи больниц, которые и так загружены.',
			'Ukraine asks us to admit wounded servicemen and to organise evacuation across the border. The request falls on hospitals that are already overloaded.'),
		res_t=T('Ответ Варшавы: госпитали и эвакуация', 'Warsaw\'s answer: hospitals and evacuation'),
		res_full=T('Варшава согласилась: эвакуационные поезда и борты идут в Польшу, госпитали выделили сотни коек. Многие раненые вернутся в строй.',
			'Warsaw has agreed: evacuation trains and aircraft head to Poland, and hospitals have set aside hundreds of beds. Many of the wounded will return to the ranks.'),
		res_part=T('Польша выделила места в госпиталях, но эвакуацию придётся вести нашими силами: транспорта не хватает.',
			'Poland has set aside hospital places, but evacuation will have to be carried out by our own means: there is not enough transport.'),
		res_no=T('Варшава отказала: больницы перегружены беженцами. Просим вернуться к вопросу позже.',
			'Warsaw refused: the hospitals are overloaded with refugees. We ask to return to the question later.'),
		weights=[],
		full=[idea('UKR_pl_medevac_idea', 540, lim='UKR_pl_medevac_idea_lim', lim_days=270)],
		part='auto',
	),
]

IDEAS = [
	dict(name='UKR_pl_hub_idea', picture='generic_supply_lines', mods={'land_reinforce_rate': 0.05},
		ru_name='Польский транзитный хаб', en_name='Polish transit hub',
		ru_desc='Через юго-восток Польши идут союзные грузы: быстрее пополняются потери и склады.',
		en_desc='Allied cargo flows through south-eastern Poland: losses and stockpiles are replenished faster.'),
	dict(name='UKR_pl_hub_idea_lim', picture='generic_supply_lines', mods={'land_reinforce_rate': 0.025},
		ru_name='Ограниченный польский хаб', en_name='Limited Polish hub',
		ru_desc='Польша пропускает часть союзных грузов: пополнение идёт чуть быстрее.',
		en_desc='Poland lets part of the allied cargo through: reinforcement is slightly faster.'),
	dict(name='UKR_pl_medevac_idea', picture='generic_stability', mods={'casualty_trickleback': 0.12},
		ru_name='Польская медицинская эвакуация', en_name='Polish medical evacuation',
		ru_desc='Раненых лечат в польских госпиталях: часть возвращается в строй.',
		en_desc='The wounded are treated in Polish hospitals: part of them return to the ranks.'),
	dict(name='UKR_pl_medevac_idea_lim', picture='generic_stability', mods={'casualty_trickleback': 0.06},
		ru_name='Ограниченная эвакуация в Польшу', en_name='Limited evacuation to Poland',
		ru_desc='Польша принимает часть раненых: меньше возвращается в строй.',
		en_desc='Poland takes part of the wounded: fewer return to the ranks.'),
]

# Цепочки Польши: тексты событий 320 (зерно, у Украины), 321 (итог эксгумаций) и решения UKR_pl_exhumations
CHAIN = dict(
	grain=dict(
		t=T('Зерно на польской границе', 'Grain on the Polish border'),
		d=T('Украинское зерно, идущее транзитом через Польшу, оседает на местном рынке и обрушивает цены для польских фермеров. Варшава грозит запретом ввоза, а фермеры и перевозчики блокируют переходы. В нашей реальности так было весной 2023 года: Польша, Венгрия и Словакия закрыли рынки для украинского зерна, ЕС ввёл временные ограничения, а Киев жаловался в ВТО.\n\nТеперь нужно решить, как отвечать.',
			'Ukrainian grain moving in transit through Poland settles on the local market and collapses prices for Polish farmers. Warsaw threatens an import ban, and farmers and hauliers block the crossings. In our reality this happened in the spring of 2023: Poland, Hungary and Slovakia closed their markets to Ukrainian grain, the EU introduced temporary restrictions, and Kyiv complained to the WTO.\n\nWe must now decide how to respond.'),
		a=T('Согласиться на запрет и пустить зерно через «коридоры солидарности».', 'Accept the ban and send the grain through the «solidarity lanes».'),
		b=T('Жаловаться в ВТО и давить через Брюссель.', 'Complain to the WTO and press through Brussels.'),
		c=T('Тихие переговоры: лицензии на вывоз и квоты.', 'Quiet talks: export licences and quotas.'),
	),
	exh=dict(
		name=T('Разрешить эксгумации на Волыни', 'Allow exhumations in Volhynia'),
		desc=T(
			'Даём Варшаве разрешение искать и эксгумировать останки польских жертв Волынской трагедии 1943-1944 годов и ухаживать за захоронениями. Взамен просим такого же отношения к украинским могилам в Польше.\n\n'
			'§YЧто это.§! Комиссии историков и судебных экспертов, работы в сёлах Волыни и Галичины, согласование с местными властями. Тема болезненная: это вопрос памяти и для поляков, и для украинцев.\n'
			'§YВ реальности.§! В 2025 году, впервые за много лет, в селе Пузники (Тернопольская область) начались эксгумации по согласованию Киева и Варшавы.\n'
			'§YЧто даст.§! Заметно теплеет отношение Польши, растёт доверие; часть националистов недовольна.',
			'We give Warsaw permission to search for and exhume the remains of Polish victims of the Volhynia tragedy of 1943-1944 and to tend the burial sites. In return we ask for the same treatment of Ukrainian graves in Poland.\n\n'
			'§YWhat it is.§! Commissions of historians and forensic experts, work in the villages of Volhynia and Galicia, coordination with local authorities. The subject is painful: it is a matter of memory for both Poles and Ukrainians.\n'
			'§YIn reality.§! In 2025, for the first time in many years, exhumations began in the village of Puzhnyky (Ternopil Oblast), agreed between Kyiv and Warsaw.\n'
			'§YWhat it gives.§! Poland\'s attitude warms noticeably and trust grows; part of the nationalists are displeased.'),
		res_t=T('Эксгумации начались', 'The exhumations have begun'),
		res_d=T('Польские и украинские эксперты начали работу в поле. Первые останки найдены и приняты с уважением. Вопрос остаётся трудным, но разговор начался, и в Варшаве это заметили.',
			'Polish and Ukrainian experts have begun their work in the field. The first remains have been found and received with respect. The question remains difficult, but the conversation has begun, and Warsaw has noticed.'),
		res_a=T('Работаем дальше.', 'We continue the work.'),
	),
)
