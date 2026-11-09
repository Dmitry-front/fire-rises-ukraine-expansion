# Британия (ENG): разведка, учебная миссия, ракеты, морская коалиция. PROPOSAL_war_europe.md 4.1.
from .fx import *

REQ = [
	dict(
		key='eng_intel', tag='ENG', ev=440, res=450, base=40, cd=300, icon='generic_intelligence_document',
		pic='GFX_UKR_diplomat', scale=False,
		name=T('Просить Лондон: разведывательное партнёрство', 'Ask London: an intelligence partnership'),
		desc=T(
			'Просим Британию делиться разведданными и помочь защитить наши каналы связи.\n\n'
			'§YЧто это.§! Данные радио- и радиотехнической разведки, спутниковые снимки, совместная оценка угроз и защита шифров.\n'
			'§YВ реальности.§! Перед вторжением 2022 года Британия и США рассекретили часть данных о планах России, а с февраля 2022 года британское Министерство обороны публикует регулярные обзоры хода войны.\n'
			'§YЧто даст.§! На время растут возможности перехвата и накопления данных; но Лондон делится только с теми, кто умеет хранить секреты.',
			'We ask Britain to share intelligence and to help protect our communication channels.\n\n'
			'§YWhat it is.§! Signals and electronic intelligence, satellite imagery, joint threat assessment and cipher protection.\n'
			'§YIn reality.§! Before the 2022 invasion Britain and the United States declassified part of the data on Russia\'s plans, and since February 2022 the British Ministry of Defence has published regular reviews of the course of the war.\n'
			'§YWhat it gives.§! For a time, interception and data gathering improve; but London shares only with those who can keep secrets.'),
		req_t=T('Просьба Киева: обмен разведданными', 'Kyiv\'s request: intelligence sharing'),
		req_d=T('Украина просит постоянный обмен данными и помощь в защите связи. Разведывательные службы напоминают: источники уязвимы, а утечки стоят дорого.',
			'Ukraine asks for permanent data sharing and help in protecting its communications. The intelligence services remind us: sources are vulnerable and leaks are expensive.'),
		res_t=T('Ответ Лондона: разведывательное партнёрство', 'London\'s answer: the intelligence partnership'),
		res_full=T('Лондон согласился: открыт постоянный канал обмена, данные приходят ежедневно. Контрразведка проверяет наши каналы связи.',
			'London has agreed: a permanent channel of exchange is open and data arrives daily. Counter-intelligence is checking our communication channels.'),
		res_part=T('Британия согласилась на ограниченный обмен: часть данных мы получим только в виде оценок, без первоисточников.',
			'Britain agreed to a limited exchange: part of the data we will receive only as assessments, without the original sources.'),
		res_no=T('Лондон отказал: службы не уверены в защите наших каналов. Просьбу можно повторить позже.',
			'London refused: the services are not sure our channels are secure. The request can be repeated later.'),
		weights=[('UKR = { has_country_flag = UKR_pillar_chosen_technocrats }', 10),
			('UKR = { has_country_flag = UKR_pillar_chosen_oligarchs }', -10),
			('UKR = { has_idea = UKR_eu_aid_frozen }', -10)],
		full=[idea('UKR_uk_intel_idea', 365, lim='UKR_uk_intel_idea_lim', lim_days=180), flag('UKR_uk_intel_partnership')],
		part='auto',
	),
	dict(
		key='eng_training', tag='ENG', ev=441, res=451, base=50, cd=240, icon='GFX_decision_generic_army_support',
		pic='GFX_FRA_training', scale=False,
		name=T('Просить Лондон: учебная миссия', 'Ask London: a training mission'),
		desc=T(
			'Просим Британию организовать на своей территории подготовку наших новобранцев и офицеров.\n\n'
			'§YЧто это.§! Курсы на британских полигонах: общевойсковая подготовка, тактика малых подразделений, медицина, сапёрное дело, обучение командиров.\n'
			'§YВ реальности.§! С июня 2022 года Британия руководила операцией «Интерфлекс»: инструкторы из нескольких стран за несколько недель готовили новобранцев, и за годы операции обучение прошли десятки тысяч человек.\n'
			'§YЧто даст.§! Опыт армии и более быстрая подготовка дивизий на время миссии.',
			'We ask Britain to organise the training of our recruits and officers on its territory.\n\n'
			'§YWhat it is.§! Courses at British training areas: combined-arms training, small-unit tactics, medicine, combat engineering, commander training.\n'
			'§YIn reality.§! From June 2022 Britain led Operation Interflex: instructors from several countries trained recruits in a few weeks, and over the years of the operation tens of thousands of people were trained.\n'
			'§YWhat it gives.§! Army experience and faster training of divisions for the duration of the mission.'),
		req_t=T('Просьба Киева: учебная миссия', 'Kyiv\'s request: a training mission'),
		req_d=T('Украина просит принять новобранцев и офицеров на подготовку на британских полигонах. Армия оценивает, сколько инструкторов можно снять с собственных частей.',
			'Ukraine asks us to take recruits and officers for training at British training areas. The army is assessing how many instructors can be pulled from its own units.'),
		res_t=T('Ответ Лондона: учебная миссия', 'London\'s answer: the training mission'),
		res_full=T('Лондон согласился: наши новобранцы и офицеры едут на британские полигоны, инструкторы начинают набор. Подготовка займёт недели, а не месяцы.',
			'London has agreed: our recruits and officers are going to British training areas and instructors begin recruitment. Training will take weeks, not months.'),
		res_part=T('Британия приняла меньше курсантов: офицеры ждут следующего набора, новобранцы пройдут обучение в сокращённом виде.',
			'Britain accepted fewer trainees: officers wait for the next intake, recruits will go through shortened training.'),
		res_no=T('Лондон отказал: инструкторов не хватает для собственных частей. Просьбу можно повторить позже.',
			'London refused: there are not enough instructors for its own units. The request can be repeated later.'),
		weights=[],
		full=[xp('army', 20), idea('UKR_uk_training_idea', 540, lim='UKR_uk_training_idea_lim', lim_days=270)],
		part='auto',
	),
	dict(
		key='eng_missiles', tag='ENG', ev=442, res=452, base=70, cd=180, icon='GFX_decision_generic_military_support',
		pic='GFX_UKR_preparing_for_war', scale=True,
		name=T('Просить Лондон: противотанковые и дальнобойные ракеты', 'Ask London: anti-tank and long-range missiles'),
		desc=T(
			'Просим Британию передать противотанковые комплексы и ракеты дальнего действия.\n\n'
			'§YЧто это.§! NLAW (шведско-британский одноразовый противотанковый комплекс, в британской армии с 2009 года), Starstreak (зенитный комплекс с лазерным наведением, с 1997 года), Storm Shadow (крылатая ракета с дальностью свыше 250 км, у британских ВВС с начала 2000-х).\n'
			'§YВ реальности.§! В 2022 году Британия передала тысячи NLAW, затем Starstreak, а в мае 2023-го первой из западных стран поставила Storm Shadow, ограничив их применение.\n'
			'§YЧто даст.§! Противотанковая и зенитная техника и дальний удар по тылам; Лондон просит гарантий, что ракеты не уйдут на сторону.',
			'We ask Britain to hand over anti-tank systems and long-range missiles.\n\n'
			'§YWhat it is.§! NLAW (a Swedish-British disposable anti-tank weapon, in the British army since 2009), Starstreak (a laser-guided air defence system, since 1997) and Storm Shadow (a cruise missile with a range of over 250 km, with the RAF since the early 2000s).\n'
			'§YIn reality.§! In 2022 Britain handed over thousands of NLAWs, then Starstreak, and in May 2023 became the first Western country to supply Storm Shadow, restricting how it could be used.\n'
			'§YWhat it gives.§! Anti-tank and air defence equipment and a long-range strike on the rear; London asks for guarantees that the missiles will not be misused.'),
		req_t=T('Просьба Киева: ракеты', 'Kyiv\'s request: missiles'),
		req_d=T('Украина просит противотанковые и зенитные комплексы и ракеты дальнего действия. Министерство обороны обсуждает условия применения.',
			'Ukraine asks for anti-tank and air defence systems and long-range missiles. The Ministry of Defence is discussing the conditions of use.'),
		res_t=T('Ответ Лондона: ракеты', 'London\'s answer: missiles'),
		res_full=T('Лондон согласился: противотанковые и зенитные комплексы и ракеты дальнего действия поставлены Украине. Условия применения оговорены.',
			'London has agreed: anti-tank and air defence systems and long-range missiles are supplied to Ukraine. The conditions of use are set out.'),
		res_part=T('Британия передала часть запрошенного: противотанковые и зенитные комплексы, а по дальнобойным ракетам решения пока нет.',
			'Britain handed over part of what was asked: anti-tank and air defence systems, while there is no decision on the long-range missiles yet.'),
		res_no=T('Лондон отказал: условия применения не согласованы. Просьбу можно повторить позже.',
			'London refused: the conditions of use have not been agreed. The request can be repeated later.'),
		weights=[],
		full=[eq('anti_tank_equipment_1', 100, 'ENG'), eq('anti_air_equipment_2', 30, 'ENG'), eq('guided_missile_equipment_1', 30, 'ENG')],
		part=[eq('anti_tank_equipment_1', 50, 'ENG'), eq('anti_air_equipment_2', 15, 'ENG')],
	),
	dict(
		key='eng_naval', tag='ENG', ev=443, res=453, base=55, cd=270, icon='GFX_decision_generic_military',
		pic='GFX_PRC_drone_uav', scale=False,
		name=T('Просить Лондон: морская коалиция и дроны', 'Ask London: a maritime coalition and drones'),
		desc=T(
			'Просим Британию возглавить морскую коалицию и помочь Украине флотом без флота: безэкипажные катера, тральщики, обучение моряков.\n\n'
			'§YЧто это.§! Безэкипажные катера и подводные дроны, тральщики и береговая оборона, пока большие корабли заперты проливами.\n'
			'§YВ реальности.§! В 2022 году Украина первой применила безэкипажные катера в бою; в 2023 году Британия и Норвегия создали Коалицию морского потенциала, а Лондон передал Украине тральщики типа Sandown.\n'
			'§YЧто даст.§! Деньги и технологии для кластера БПЛА и морских дронов, опыт морякам и шаг к безопасности Чёрного моря.',
			'We ask Britain to lead a maritime coalition and to help Ukraine with a fleet without a fleet: uncrewed boats, minehunters, training of sailors.\n\n'
			'§YWhat it is.§! Uncrewed surface and underwater drones, minehunters and coastal defence while the large ships are locked behind the straits.\n'
			'§YIn reality.§! In 2022 Ukraine was the first to use uncrewed boats in combat; in 2023 Britain and Norway created the Maritime Capability Coalition, and London handed Ukraine Sandown-class minehunters.\n'
			'§YWhat it gives.§! Funds and technology for the drone and naval drone cluster, experience for the sailors and a step towards the security of the Black Sea.'),
		req_t=T('Просьба Киева: морская коалиция', 'Kyiv\'s request: a maritime coalition'),
		req_d=T('Украина просит возглавить морскую коалицию и помочь с безэкипажными катерами, тральщиками и обучением. Адмиралтейство напоминает: корабли не могут войти в Чёрное море из-за режима проливов.',
			'Ukraine asks us to lead a maritime coalition and to help with uncrewed boats, minehunters and training. The Admiralty reminds us that ships cannot enter the Black Sea because of the strait regime.'),
		res_t=T('Ответ Лондона: морская коалиция', 'London\'s answer: the maritime coalition'),
		res_full=T('Лондон согласился: создаётся морская коалиция, оборонные организации получают финансирование, моряки места в британских училищах.',
			'London has agreed: a maritime coalition is being formed, defence organisations receive funding and sailors get places in British schools.'),
		res_part=T('Британия согласилась на часть: помощь с обучением и скромное финансирование, но коалиция откладывается.',
			'Britain agreed to part: help with training and modest funding, but the coalition is postponed.'),
		res_no=T('Лондон отказал: Адмиралтейство не готово брать на себя обязательства по Чёрному морю. Просьбу можно повторить позже.',
			'London refused: the Admiralty is not ready to take on commitments in the Black Sea. The request can be repeated later.'),
		weights=[],
		full=[mio('UKR_drone_cluster_organization', 150), xp('navy', 15)],
		part='auto',
	),
]

IDEAS = [
	dict(name='UKR_uk_intel_idea', picture='generic_research',
		mods={'decryption_factor': 0.10, 'intel_network_gain_factor': 0.15},
		ru_name='Британское разведывательное партнёрство', en_name='British intelligence partnership',
		ru_desc='Лондон делится разведданными и помогает защищать наши каналы связи.',
		en_desc='London shares intelligence and helps protect our communication channels.'),
	dict(name='UKR_uk_intel_idea_lim', picture='generic_research',
		mods={'decryption_factor': 0.05, 'intel_network_gain_factor': 0.075},
		ru_name='Ограниченный обмен с Британией', en_name='Limited exchange with Britain',
		ru_desc='Лондон делится только оценками, без первоисточников.',
		en_desc='London shares only assessments, without the original sources.'),
	dict(name='UKR_uk_training_idea', picture='generic_military_org',
		mods={'training_time_factor': -0.10, 'experience_gain_army_factor': 0.05},
		ru_name='Британская учебная миссия', en_name='British training mission',
		ru_desc='Новобранцы и офицеры проходят подготовку на британских полигонах: дивизии учатся быстрее.',
		en_desc='Recruits and officers train at British training areas: divisions train faster.'),
	dict(name='UKR_uk_training_idea_lim', picture='generic_military_org',
		mods={'training_time_factor': -0.05, 'experience_gain_army_factor': 0.025},
		ru_name='Сокращённая британская миссия', en_name='Shortened British mission',
		ru_desc='Британия принимает меньше курсантов: эффект скромнее.',
		en_desc='Britain accepts fewer trainees: the effect is more modest.'),
]
