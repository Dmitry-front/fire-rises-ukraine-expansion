# Прибалтика: Эстония, Латвия, Литва - по одному запросу на страну, ответ быстрее (fast=True). PROPOSAL_war_europe.md 4.1.
from .fx import *

REQ = [
	dict(
		key='est_package', tag='EST', ev=460, res=470, base=30, cd=120, icon='generic_shaking_hands',
		pic='GFX_event_UKR_war_support_NATO', scale=True, fast=True,
		name=T('Просить Таллин: быстрый пакет', 'Ask Tallinn: a quick package'),
		desc=T(
			'Просим Эстонию срочно передать из собственных запасов то, что можно отправить за несколько дней.\n\n'
			'§YЧто это.§! Малый, но быстрый пакет: 155-мм гаубицы FH-70 (в европейских армиях с 1970-х), переносные противотанковые комплексы Javelin (с 1990-х), боеприпасы.\n'
			'§YВ реальности.§! Эстония передала Украине гаубицы FH-70 и Javelin и вошла в число стран, дающих помощи больше всех в процентах от ВВП; поставки начались ещё до начала полномасштабного вторжения.\n'
			'§YЧто даст.§! Небольшая, но срочная помощь; Таллин отвечает быстрее других.',
			'We ask Estonia to hand over at once from its own stocks whatever can be shipped within days.\n\n'
			'§YWhat it is.§! A small but quick package: 155 mm FH-70 howitzers (in European armies since the 1970s), Javelin portable anti-tank systems (since the 1990s) and ammunition.\n'
			'§YIn reality.§! Estonia handed Ukraine FH-70 howitzers and Javelins and is among the countries giving the most aid as a share of GDP; deliveries began even before the start of the full-scale invasion.\n'
			'§YWhat it gives.§! Small but urgent help; Tallinn answers faster than the others.'),
		req_t=T('Просьба Киева: срочный пакет', 'Kyiv\'s request: an urgent package'),
		req_d=T('Украина просит передать из запасов то, что можно отправить за несколько дней. У Эстонии немного, но решение принимается без долгих споров.',
			'Ukraine asks us to hand over from our stocks whatever can be shipped within days. Estonia has little, but the decision is taken without long arguments.'),
		res_t=T('Ответ Таллина: быстрый пакет', 'Tallinn\'s answer: the quick package'),
		res_full=T('Таллин согласился: гаубицы, противотанковые комплексы и боеприпасы уже в пути. Пакет невелик, но пришёл вовремя.',
			'Tallinn has agreed: howitzers, anti-tank systems and ammunition are already on their way. The package is small, but it arrived in time.'),
		res_part=T('Эстония передала то, что может: часть гаубиц и боеприпасов. Остального у неё просто нет.',
			'Estonia handed over what it can: part of the howitzers and ammunition. It simply has nothing more.'),
		res_no=T('Таллин отказал: запасы после прошлых передач на минимуме. Просьбу можно повторить позже.',
			'Tallinn refused: stocks after earlier transfers are at a minimum. The request can be repeated later.'),
		weights=[],
		full=[eq('artillery_equipment_1', 30, 'EST'), eq('anti_tank_equipment_1', 60, 'EST')],
		part='auto',
	),
	dict(
		key='lat_drones', tag='LAT', ev=461, res=471, base=35, cd=180, icon='GFX_decision_generic_research',
		pic='GFX_PRC_drone_uav', scale=True, fast=True,
		name=T('Просить Ригу: коалиция дронов', 'Ask Riga: a drone coalition'),
		desc=T(
			'Просим Латвию вместе с Британией возглавить коалицию по беспилотникам: общие закупки, финансирование мастерских и поставки.\n\n'
			'§YЧто это.§! Совместные закупки и финансирование производства: разведывательные дроны, ударные FPV, наземные роботы. Латвия берёт на себя координацию.\n'
			'§YВ реальности.§! В 2024 году Латвия и Британия возглавили «Коалицию дронов» в формате «Рамштайн»; Латвия также передавала Украине зенитные комплексы «Стингер».\n'
			'§YЧто даст.§! Деньги для кластера БПЛА и зенитные ракеты.',
			'We ask Latvia, together with Britain, to lead a coalition on drones: joint purchases, funding of workshops and deliveries.\n\n'
			'§YWhat it is.§! Joint purchases and production funding: reconnaissance drones, strike FPVs, ground robots. Latvia takes on the coordination.\n'
			'§YIn reality.§! In 2024 Latvia and Britain led the «Drone Coalition» in the Ramstein format; Latvia also handed Ukraine Stinger air defence systems.\n'
			'§YWhat it gives.§! Funds for the drone cluster and air defence missiles.'),
		req_t=T('Просьба Киева: коалиция дронов', 'Kyiv\'s request: a drone coalition'),
		req_d=T('Украина просит возглавить коалицию по беспилотникам: общие закупки и финансирование мастерских. Армия готова скоординировать, если партнёры подтвердят свои взносы.',
			'Ukraine asks us to lead a coalition on drones: joint purchases and funding of workshops. The army is ready to coordinate if partners confirm their contributions.'),
		res_t=T('Ответ Риги: коалиция дронов', 'Riga\'s answer: the drone coalition'),
		res_full=T('Рига согласилась: коалиция создана, первые деньги идут на мастерские, зенитные ракеты уже в пути.',
			'Riga has agreed: the coalition is formed, the first money goes to the workshops and air defence missiles are already on their way.'),
		res_part=T('Латвия согласилась на часть: скромные взносы и зенитные ракеты, но общая коалиция пока без партнёров.',
			'Latvia agreed to part: modest contributions and air defence missiles, but the common coalition is for now without partners.'),
		res_no=T('Рига отказала: без согласия партнёров Латвия не готова брать на себя координацию. Просьбу можно повторить позже.',
			'Riga refused: without the consent of partners Latvia is not ready to take on the coordination. The request can be repeated later.'),
		weights=[],
		full=[mio('UKR_drone_cluster_organization', 150), eq('anti_air_equipment_1', 40, 'LAT')],
		part='auto',
	),
	dict(
		key='lit_support', tag='LIT', ev=462, res=472, base=35, cd=150, icon='GFX_decision_generic_protection',
		pic='GFX_event_UKR_volunteers', scale=True, fast=True,
		name=T('Просить Вильнюс: зенитные ракеты и инструкторы', 'Ask Vilnius: air defence missiles and instructors'),
		desc=T(
			'Просим Литву передать переносные зенитные комплексы и командировать инструкторов.\n\n'
			'§YЧто это.§! ПЗРК «Стингер» (в армиях НАТО с 1980-х) и инструкторы для подготовки расчётов и сапёров.\n'
			'§YВ реальности.§! Литва передала Украине «Стингеры», а общество собирало деньги на помощь: в 2022 году народный сбор на беспилотник «Байрактар» был настолько быстрым, что производитель решил подарить машину.\n'
			'§YЧто даст.§! Зенитные ракеты, опыт и шаг к защите неба.',
			'We ask Lithuania to hand over portable air defence systems and to send instructors.\n\n'
			'§YWhat it is.§! Stinger man-portable air defence systems (in NATO armies since the 1980s) and instructors to train crews and sappers.\n'
			'§YIn reality.§! Lithuania handed Ukraine Stingers, and society raised money for aid: in 2022 a popular fundraiser for a Bayraktar drone was so quick that the manufacturer decided to donate the machine.\n'
			'§YWhat it gives.§! Air defence missiles, experience and a step towards protecting the sky.'),
		req_t=T('Просьба Киева: ПВО и инструкторы', 'Kyiv\'s request: air defence and instructors'),
		req_d=T('Украина просит переносные зенитные комплексы и инструкторов. Литва отвечает осторожно: собственные запасы малы, но общество требует помогать.',
			'Ukraine asks for portable air defence systems and instructors. Lithuania answers carefully: its own stocks are small, but society demands help.'),
		res_t=T('Ответ Вильнюса: ПВО и инструкторы', 'Vilnius\'s answer: air defence and instructors'),
		res_full=T('Вильнюс согласился: зенитные ракеты идут Украине, инструкторы готовят расчёты. Литовцы собрали деньги ещё до решения правительства.',
			'Vilnius has agreed: air defence missiles are heading to Ukraine and instructors are training crews. Lithuanians raised money even before the government decided.'),
		res_part=T('Литва передала часть ракет, инструкторов обещала позже.',
			'Lithuania handed over part of the missiles and promised instructors later.'),
		res_no=T('Вильнюс отказал: правительство ждёт ответа партнёров по Балтии. Просьбу можно повторить позже.',
			'Vilnius refused: the government awaits the answer of its Baltic partners. The request can be repeated later.'),
		weights=[],
		full=[eq('anti_air_equipment_1', 50, 'LIT'), xp('army', 5), var('UKR_air_defense_points', 1)],
		part=[eq('anti_air_equipment_1', 25, 'LIT'), xp('army', 3)],
	),
]

IDEAS = []
