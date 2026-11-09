# Германия (GER): ПВО, кредитная линия, тяжёлая техника. PROPOSAL_war_europe.md 4.1.
from .fx import *

W_FROZEN = ('UKR = { has_idea = UKR_eu_aid_frozen }', -20)
W_ANTICORR = ('UKR = { has_idea = UKR_anticorruption_wave }', 15)
W_EURO = ('UKR = { has_idea = UKR_euro_momentum }', 10)

REQ = [
	dict(
		key='ger_air', tag='GER', ev=400, res=410, base=70, cd=180, icon='GFX_decision_generic_air',
		pic='GFX_UKR_status_NATO', scale=True,
		name=T('Просить Берлин: щит для неба', 'Ask Berlin: a shield for the sky'),
		desc=T(
			'Просим Германию передать зенитные комплексы и самоходные установки для защиты городов и энергосистемы.\n\n'
			'§YЧто это.§! Зенитные комплексы средней дальности IRIS-T SLM, самоходные зенитные установки «Гепард» (были на вооружении бундесвера с 1976 до 2010 года) и ЗРК «Пэтриот».\n'
			'§YВ реальности.§! С осени 2022 года Германия передавала IRIS-T SLM и около полусотни «Гепардов», а позже, вместе с партнёрами, и батареи «Пэтриот».\n'
			'§YЧто даст.§! Зенитная техника на склад и шаг к защите инфраструктуры от ударов с воздуха.',
			'We ask Germany to hand over air defence systems and self-propelled guns to protect our cities and the power grid.\n\n'
			'§YWhat it is.§! IRIS-T SLM medium-range air defence systems, Gepard self-propelled anti-aircraft guns (in Bundeswehr service from 1976 until 2010) and Patriot missile systems.\n'
			'§YIn reality.§! From autumn 2022 Germany supplied IRIS-T SLM and about fifty Gepards, and later, together with partners, Patriot batteries.\n'
			'§YWhat it gives.§! Air defence equipment for the stockpile and a step towards protecting infrastructure from air strikes.'),
		req_t=T('Просьба Киева: противовоздушный щит', 'Kyiv\'s request: an air defence shield'),
		req_d=T('Украина просит зенитные комплексы для защиты городов и энергосистемы. Ответ определит, сколько ракет и систем Германия может выделить, не оголив собственную ПВО.',
			'Ukraine asks for air defence systems to protect its cities and the power grid. The answer will decide how many missiles and systems Germany can release without baring its own air defence.'),
		res_t=T('Ответ Берлина: щит для неба', 'Berlin\'s answer: a shield for the sky'),
		res_full=T('Берлин согласился: на склады приходят зенитные комплексы средней дальности и самоходные установки. У городов больше шансов пережить удары.',
			'Berlin has agreed: medium-range air defence systems and self-propelled guns are arriving at our depots. The cities have a better chance of surviving the strikes.'),
		res_part=T('Германия выделила часть запрошенных систем: остальное, по словам канцелярии, нужно собственной армии и ждёт заказов промышленности.',
			'Germany released part of the systems requested: the rest, the chancellery says, is needed by its own army and awaits industrial orders.'),
		res_no=T('Берлин отказал: канцелярия ссылается на пустеющие склады и ждёт нового заказа промышленности. Просьбу можно повторить позже.',
			'Berlin refused: the chancellery cites emptying depots and awaits a new order for industry. The request can be repeated later.'),
		weights=[W_FROZEN, W_ANTICORR],
		full=[eq('anti_air_equipment_2', 60, 'GER'), eq('spaa_equipment_1', 40, 'GER'), var('UKR_air_defense_points', 2)],
		part='auto',
	),
	dict(
		key='ger_credit', tag='GER', ev=401, res=411, base=50, cd=240, icon='GFX_decision_generic_industry',
		pic='GFX_UKR_investment_forum', scale=True,
		name=T('Просить Берлин: кредитная линия', 'Ask Berlin: a credit line'),
		desc=T(
			'Просим Германию возглавить финансовую поддержку: льготные займы, гарантии и прямые гранты на бюджет и закупки.\n\n'
			'§YЧто это.§! Часть помощи приходит грантом, часть льготным займом, привязанным к реформам и отчётности. Заём увеличивает долг, грант нет.\n'
			'§YВ реальности.§! С 2022 года Германия давала гранты и гарантии, участвовала в макрофинансовой помощи ЕС и в общей программе G7; выплаты привязывали к реформам и отчётам.\n'
			'§YЧто даст.§! Деньги в бюджет и часть долга. Чем меньше коррупции, тем охотнее дают.',
			'We ask Germany to lead financial support: concessional loans, guarantees and direct grants for the budget and procurement.\n\n'
			'§YWhat it is.§! Part of the aid comes as a grant, part as a concessional loan tied to reforms and reporting. A loan increases debt, a grant does not.\n'
			'§YIn reality.§! From 2022 Germany provided grants and guarantees and took part in EU macro-financial assistance and the common G7 programme; payments were tied to reforms and reports.\n'
			'§YWhat it gives.§! Money for the budget and some debt. The less corruption there is, the more readily it is given.'),
		req_t=T('Просьба Киева: финансовая поддержка', 'Kyiv\'s request: financial support'),
		req_d=T('Украина просит кредитную линию и бюджетные гранты. Министерство финансов напоминает, что деньги придётся отчитывать перед бундестагом.',
			'Ukraine asks for a credit line and budget grants. The finance ministry reminds us that the money will have to be accounted for before the Bundestag.'),
		res_t=T('Ответ Берлина: кредитная линия', 'Berlin\'s answer: the credit line'),
		res_full=T('Берлин согласился: часть средств придёт грантом, часть льготным кредитом под реформы. Бюджет на ближайшие месяцы закрыт.',
			'Berlin has agreed: part of the funds will come as a grant, part as a concessional loan tied to reforms. The budget for the coming months is covered.'),
		res_part=T('Германия дала меньше запрошенного: гарантии на часть займа и скромный грант. Остальное после отчёта о реформах.',
			'Germany gave less than requested: guarantees for part of the loan and a modest grant. The rest only after a report on reforms.'),
		res_no=T('Берлин отказал: канцелярия требует сначала отчитаться о прошлых траншах и реформах. Просьбу можно повторить позже.',
			'Berlin refused: the chancellery demands that we first account for past tranches and reforms. The request can be repeated later.'),
		weights=[('UKR = { has_idea = UKR_eu_aid_frozen }', -25), W_ANTICORR,
			('UKR = { has_country_flag = UKR_pillar_chosen_technocrats }', 10),
			('UKR = { has_country_flag = UKR_pillar_chosen_oligarchs }', -10)],
		full=[money(12, 6)],
		part='auto',
	),
	dict(
		key='ger_armor', tag='GER', ev=402, res=412, base=85, cd=240, icon='GFX_decision_generic_tank',
		pic='GFX_Generic_Tank_column', scale=True,
		name=T('Просить Берлин: тяжёлая техника', 'Ask Berlin: heavy equipment'),
		desc=T(
			'Просим Германию передать танки, боевые машины пехоты и самоходные гаубицы из запасов бундесвера и промышленности.\n\n'
			'§YЧто это.§! Танки «Леопард 2» (в Германии с 1979 года, модификация 2А6 с 2001-го), боевые машины пехоты «Мардер» (с 1971 года) и самоходные гаубицы PzH 2000 (с 1998 года).\n'
			'§YВ реальности.§! В 2022 году Германия передала первые PzH 2000, а в январе 2023-го, после месяцев споров, согласилась на «Леопарды 2» и «Мардеры», когда США и другие союзники решили присоединиться.\n'
			'§YЧто даст.§! Бронетехника и артиллерия для наступательных операций; но без доверия решение у Берлина вырвать трудно.',
			'We ask Germany to hand over tanks, infantry fighting vehicles and self-propelled howitzers from Bundeswehr stocks and from industry.\n\n'
			'§YWhat it is.§! Leopard 2 tanks (in Germany since 1979, the 2A6 version since 2001), Marder infantry fighting vehicles (since 1971) and PzH 2000 self-propelled howitzers (since 1998).\n'
			'§YIn reality.§! In 2022 Germany handed over the first PzH 2000, and in January 2023, after months of dispute, agreed to Leopard 2 and Marder when the United States and other allies decided to join.\n'
			'§YWhat it gives.§! Armour and artillery for offensive operations; but without trust it is hard to extract such a decision from Berlin.'),
		req_t=T('Просьба Киева: тяжёлая техника', 'Kyiv\'s request: heavy equipment'),
		req_d=T('Украина просит танки, боевые машины пехоты и самоходные гаубицы. Канцлер колеблется: не хочет эскалации и ждёт, что решат союзники.',
			'Ukraine asks for tanks, infantry fighting vehicles and self-propelled howitzers. The chancellor hesitates: he does not want escalation and waits to see what the allies decide.'),
		res_t=T('Ответ Берлина: тяжёлая техника', 'Berlin\'s answer: heavy equipment'),
		res_full=T('Берлин согласился: «Леопарды», «Мардеры» и самоходные гаубицы идут на склады. Решение далось тяжело, но дорога открыта.',
			'Berlin has agreed: Leopards, Marders and self-propelled howitzers are heading for our depots. The decision came with difficulty, but the road is open.'),
		res_part=T('Германия передала часть техники: остальное, по словам канцелярии, придёт, когда к решению присоединятся союзники.',
			'Germany handed over part of the equipment: the rest, the chancellery says, will follow once the allies join the decision.'),
		res_no=T('Берлин отказал: канцелярия не хочет «идти впереди союзников». Просьбу можно повторить позже.',
			'Berlin refused: the chancellery does not want to «walk ahead of the allies». The request can be repeated later.'),
		weights=[W_EURO, W_FROZEN],
		full=[eq('modern_tank_equipment_2', 50, 'GER'), eq('mechanized_equipment_1', 100, 'GER'), eq('artillery_equipment_2', 40, 'GER')],
		part='auto',
	),
]

IDEAS = []
