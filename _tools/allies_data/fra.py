# Франция (FRA): артиллерия CAESAR, авиация и ракеты, реестр добровольцев. PROPOSAL_war_europe.md 4.1.
from .fx import *

W_FROZEN = ('UKR = { has_idea = UKR_eu_aid_frozen }', -10)

REQ = [
	dict(
		key='fra_caesar', tag='FRA', ev=420, res=430, base=55, cd=150, icon='GFX_decision_generic_military',
		pic='GFX_FRA_french_soldier', scale=True,
		name=T('Просить Париж: артиллерийский контракт', 'Ask Paris: an artillery contract'),
		desc=T(
			'Просим Францию поставить колёсные самоходные гаубицы и снаряды и заключить длительный контракт с промышленностью.\n\n'
			'§YЧто это.§! CAESAR: 155-мм гаубица на шасси грузовика 6x6; во французской армии с 2008 года, быстро меняет позицию после выстрела и поэтому хуже поддаётся контрбатарейному огню.\n'
			'§YВ реальности.§! С 2022 года Франция передала Украине десятки CAESAR (часть оплатили другие страны, включая Данию) и заказывала новые партии у промышленности.\n'
			'§YЧто даст.§! Мобильная артиллерия и снаряды к ней; ответ зависит от того, сколько Франция может выделить, не оголив собственную армию.',
			'We ask France to supply wheeled self-propelled howitzers and shells and to sign a long-term contract with industry.\n\n'
			'§YWhat it is.§! CAESAR: a 155 mm howitzer on a 6x6 truck chassis; in the French army since 2008, it changes position quickly after firing and is therefore harder to hit with counter-battery fire.\n'
			'§YIn reality.§! Since 2022 France has handed Ukraine dozens of CAESARs (some paid for by other countries, Denmark among them) and ordered new batches from industry.\n'
			'§YWhat it gives.§! Mobile artillery and shells for it; the answer depends on how much France can release without baring its own army.'),
		req_t=T('Просьба Киева: артиллерийский контракт', 'Kyiv\'s request: an artillery contract'),
		req_d=T('Украина просит самоходные гаубицы CAESAR и снаряды. Генштаб предупреждает, что запас снарядов собственной армии ограничен.',
			'Ukraine asks for CAESAR self-propelled howitzers and shells. The general staff warns that the stock of shells for our own army is limited.'),
		res_t=T('Ответ Парижа: артиллерийский контракт', 'Paris\'s answer: the artillery contract'),
		res_full=T('Париж согласился: гаубицы CAESAR и снаряды к ним идут в Украину. Промышленность получила заказ.',
			'Paris has agreed: CAESAR howitzers and shells for them are heading to Ukraine. Industry has received the order.'),
		res_part=T('Франция дала часть запрошенного: гаубиц меньше, снаряды только по графику производства.',
			'France gave part of what was asked: fewer howitzers, and shells only according to the production schedule.'),
		res_no=T('Париж отказал: собственным войскам не хватает снарядов. Просьбу можно повторить позже.',
			'Paris refused: its own forces are short of shells. The request can be repeated later.'),
		weights=[W_FROZEN],
		full=[eq('artillery_equipment_2', 70, 'FRA'), eq('support_equipment_1', 40, 'FRA')],
		part='auto',
	),
	dict(
		key='fra_air', tag='FRA', ev=421, res=431, base=80, cd=240, icon='GFX_decision_generic_air',
		pic='GFX_Generic_Fight_Jet', scale=True,
		name=T('Просить Париж: авиация и зенитные ракеты', 'Ask Paris: aircraft and air defence missiles'),
		desc=T(
			'Просим Францию передать зенитные ракетные комплексы, крылатые ракеты и боевые самолёты.\n\n'
			'§YЧто это.§! ЗРК SAMP/T (франко-итальянский, ракеты «Астер 30»), крылатые ракеты SCALP-EG (двойник британской Storm Shadow, дальность свыше 250 км), истребители «Мираж 2000» (во французской авиации с 1980-х годов).\n'
			'§YВ реальности.§! Франция поставила SCALP в 2023 году, SAMP/T в 2023-2024 годах, а затем готовила передачу «Миражей 2000-5».\n'
			'§YЧто даст.§! Зенитное прикрытие, дальний удар по тылам и боевая авиация; но Париж отдаёт такие системы осторожно.',
			'We ask France to hand over surface-to-air missile systems, cruise missiles and combat aircraft.\n\n'
			'§YWhat it is.§! SAMP/T (Franco-Italian, Aster 30 missiles), SCALP-EG cruise missiles (twin of the British Storm Shadow, range over 250 km) and Mirage 2000 fighters (in French service since the 1980s).\n'
			'§YIn reality.§! France delivered SCALP in 2023 and SAMP/T in 2023-2024, and then prepared the transfer of Mirage 2000-5 aircraft.\n'
			'§YWhat it gives.§! Air defence cover, long-range strikes on the rear and combat aircraft; but Paris gives up such systems cautiously.'),
		req_t=T('Просьба Киева: авиация и зенитные ракеты', 'Kyiv\'s request: aircraft and air defence missiles'),
		req_d=T('Украина просит зенитные ракетные комплексы, крылатые ракеты и истребители. Каждая из этих систем снимается с вооружения самой Франции.',
			'Ukraine asks for surface-to-air missile systems, cruise missiles and fighters. Each of these systems is taken from France\'s own inventory.'),
		res_t=T('Ответ Парижа: авиация и ракеты', 'Paris\'s answer: aircraft and missiles'),
		res_full=T('Париж согласился: на склады приходят зенитные комплексы, крылатые ракеты и истребители. Решение принято на уровне президента.',
			'Paris has agreed: air defence systems, cruise missiles and fighters are arriving at our depots. The decision was taken at presidential level.'),
		res_part=T('Франция выделила часть: зенитные комплексы и ракеты, но самолёты придётся ждать.',
			'France released part: air defence systems and missiles, but the aircraft will have to wait.'),
		res_no=T('Париж отказал: в Елисейском дворце считают такие системы слишком чувствительными. Просьбу можно повторить позже.',
			'Paris refused: the Elysee considers such systems too sensitive. The request can be repeated later.'),
		weights=[W_FROZEN, ('UKR = { has_idea = UKR_anticorruption_wave }', 10)],
		full=[eq('fighter_equipment_2', 24, 'FRA'), eq('anti_air_equipment_2', 30, 'FRA'),
			eq('guided_missile_equipment_1', 30, 'FRA'), var('UKR_air_defense_points', 1)],
		part=[eq('anti_air_equipment_2', 15, 'FRA'), eq('guided_missile_equipment_1', 15, 'FRA')],
	),
	dict(
		key='fra_volunteers', tag='FRA', ev=422, res=432, base=35, cd=300, icon='GFX_decision_generic_army_support',
		pic='GFX_event_UKR_volunteers', scale=False,
		name=T('Просить Париж: реестр иностранных добровольцев', 'Ask Paris: a register of foreign volunteers'),
		desc=T(
			'Просим Францию помочь с учётом и проверкой иностранных добровольцев: принимать заявки при консульствах, согласовывать списки и снять юридические риски с вернувшихся.\n\n'
			'§YЧто это.§! Единый реестр: кто приехал, кем служит, кто за него поручился. Проверка снимает вопрос союзников о том, не пробираются ли в Украину радикалы и наёмники.\n'
			'§YВ реальности.§! С 2022 года в Международный легион обороны Украины ехали тысячи иностранцев, в том числе французы; страны Европы относились к этому по-разному: от молчаливой терпимости до предостережений.\n'
			'§YЧто даст.§! Приток людей и опыта, формальный статус добровольцам и меньше подозрений; но если у нас сильны радикалы, Париж откажет.',
			'We ask France to help with the registration and vetting of foreign volunteers: to accept applications at consulates, to agree lists and to lift legal risks from those who return.\n\n'
			'§YWhat it is.§! A single register: who has come, where he serves, who vouches for him. Vetting removes the allies\' question of whether radicals and mercenaries are slipping into Ukraine.\n'
			'§YIn reality.§! Since 2022 thousands of foreigners, French citizens among them, have joined the International Legion for the Defence of Ukraine; European states took this differently, from silent tolerance to warnings.\n'
			'§YWhat it gives.§! An inflow of people and experience, a formal status for volunteers and fewer suspicions; but if radicals are strong with us, Paris will refuse.'),
		req_t=T('Просьба Киева: реестр добровольцев', 'Kyiv\'s request: a register of volunteers'),
		req_d=T('Украина просит помочь с учётом иностранных добровольцев и разрешить приём заявок при консульствах. Парламентская комиссия спрашивает, кто именно поедет и под чьим командованием.',
			'Ukraine asks us to help with the registration of foreign volunteers and to allow applications at consulates. A parliamentary commission asks who exactly will go and under whose command.'),
		res_t=T('Ответ Парижа: реестр добровольцев', 'Paris\'s answer: the register of volunteers'),
		res_full=T('Париж согласился: консульства принимают заявки, списки проверяются совместно. К добровольцам стало меньше вопросов.',
			'Paris has agreed: consulates accept applications and the lists are checked jointly. There are fewer questions about the volunteers.'),
		res_part=T('Франция разрешила учёт, но приём заявок при консульствах не допустила: добровольцы поедут на свой страх и риск.',
			'France allowed registration but did not permit applications at consulates: volunteers will go at their own risk.'),
		res_no=T('Париж отказал: в Елисейском дворце не хотят отвечать за граждан, воюющих за границей. Просьбу можно повторить позже.',
			'Paris refused: the Elysee does not want to answer for citizens fighting abroad. The request can be repeated later.'),
		weights=[('UKR = { has_idea = UKR_far_right_legalised }', -25), ('UKR = { has_idea = UKR_far_right_meddling }', -15)],
		full=[manpower(15000), xp('army', 8), idea('UKR_vol_vetted_idea', 365, lim='UKR_vol_vetted_idea_lim', lim_days=180),
			flag('UKR_volunteer_registry')],
		part='auto',
	),
]

IDEAS = [
	dict(name='UKR_vol_vetted_idea', picture='generic_infantry_bonus',
		mods={'experience_gain_army_factor': 0.05, 'army_attack_factor': 0.02},
		ru_name='Проверенные добровольцы', en_name='Vetted volunteers',
		ru_desc='Иностранные добровольцы проходят учёт и проверку: армия быстрее набирает опыт.',
		en_desc='Foreign volunteers are registered and vetted: the army gains experience faster.'),
	dict(name='UKR_vol_vetted_idea_lim', picture='generic_infantry_bonus',
		mods={'experience_gain_army_factor': 0.025, 'army_attack_factor': 0.01},
		ru_name='Добровольцы под учётом', en_name='Registered volunteers',
		ru_desc='Учёт добровольцев ведётся частично: эффект скромнее.',
		en_desc='Volunteers are registered only in part: the effect is more modest.'),
]
