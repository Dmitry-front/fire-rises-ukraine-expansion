# -*- coding: utf-8 -*-
# Решения, события и подсказки дерева войны. Источник правды для common/decisions/UKR_decisions_war_tree.txt,
# events/UKR_events_war_tree.txt и части ключей UKR_war_tree_l_*.yml.

D = []


def decision(**kw):
    kw.setdefault('available', 'has_war_with = SOV')
    kw.setdefault('days_remove', None)
    kw.setdefault('modifier', None)
    kw.setdefault('remove', None)
    kw.setdefault('ai', 'factor = 5')
    D.append(kw)


decision(
    id='UKR_wd_operational_pause', icon='GFX_decision_generic_military',
    visible='has_war_with = SOV\nhas_completed_focus = UKR_w_supreme_command',
    cost=15, days_re_enable=90,
    complete='\n'.join([
        'hidden_effect = { add_to_variable = { var = UKRwarfatigue value = -4 } }',
        'custom_effect_tooltip = UKR_w_tt_fatigue_down',
        'add_timed_idea = { idea = UKR_wi_pause days = 30 }',
    ]),
    ru='Оперативная пауза',
    ru_d='Фронту нужно время: пополнить части, сменить уставших, наладить связь. Короткая пауза в активных действиях снижает усталость и поднимает организацию, но противник тоже получает передышку.',
    en='Operational Pause',
    en_d='The front needs time: to refill units, rotate the exhausted, restore communications. A short pause in active operations lowers fatigue and raises organization, but the enemy gets a breather too.',
)

decision(
    id='UKR_wd_mobilization_campaign', icon='GFX_decision_generic_military',
    visible='has_war_with = SOV\nhas_completed_focus = UKR_w_general_mobilization',
    cost=25, days_re_enable=120,
    complete='\n'.join([
        'if = {',
        '\tlimit = { has_completed_focus = UKR_w_pay_the_soldiers }',
        '\tadd_manpower = 12000',
        '\tset_temp_variable = { var = income_var_temp value = -1 }',
        '\tadd_income_with_inflation = yes',
        '}',
        'else_if = {',
        '\tlimit = { has_completed_focus = UKR_w_call_to_the_nation }',
        '\tadd_manpower = 8000',
        '\tadd_war_support = 0.02',
        '\thidden_effect = { add_to_variable = { var = UKRhate value = 2 } }',
        '\tcustom_effect_tooltip = UKR_w_tt_hate_up',
        '}',
        'else_if = {',
        '\tlimit = { has_completed_focus = UKR_w_forced_mobilization }',
        '\tadd_manpower = 20000',
        '\tadd_stability = -0.02',
        '\thidden_effect = { add_to_variable = { var = UKRwarfatigue value = 2 } }',
        '\tcustom_effect_tooltip = UKR_w_tt_fatigue_up',
        '}',
        'else = {',
        '\tadd_manpower = 8000',
        '}',
    ]),
    ru='Мобилизационная кампания',
    ru_d='Очередной набор людей. Результат зависит от выбранного способа мобилизации: деньги дают меньше людей, но спокойнее общество; лозунги поднимают дух и ненависть; принуждение даёт больше всего людей и больше всего недовольства.',
    en='Mobilization Campaign',
    en_d='Another intake of people. The result depends on the chosen method of mobilization: money brings fewer people but a calmer society; slogans lift morale and hatred; coercion brings the most people and the most discontent.',
)

decision(
    id='UKR_wd_factory_dispersal', icon='GFX_decision_generic_construction',
    visible='has_war_with = SOV\nhas_completed_focus = UKR_w_relocate_industry',
    cost=20, days_re_enable=100, days_remove=60,
    modifier='industry_air_damage_factor = -0.15',
    complete='add_stability = 0.01',
    remove='add_political_power = 5',
    ru='Рассредоточение производства',
    ru_d='Цеха разносят по небольшим площадкам, склады прячут, смены переносят. Каждый налёт теперь ломает меньше, хотя эффективность производства падает.',
    en='Dispersal of Production',
    en_d='Workshops are spread across small sites, depots hidden, shifts rearranged. Every raid now breaks less, although production efficiency drops.',
)

decision(
    id='UKR_wd_donor_conference', icon='GFX_decision_generic_consumer_goods',
    visible='has_war_with = SOV\nhas_completed_focus = UKR_w_appeal_to_the_world',
    cost=30, days_re_enable=180,
    complete='\n'.join([
        'set_temp_variable = { var = income_var_temp value = 2 }',
        'add_income_with_inflation = yes',
        'UKR_trust_diplomacy = yes',
    ]),
    ru='Конференция доноров',
    ru_d='Международная встреча, где страны-доноры объявляют взносы и перечисляют, на что они пойдут: бюджет, энергетика, восстановление. Хорошая подготовка и прозрачные отчёты повышают доверие партнёров.',
    en='Donor Conference',
    en_d='An international meeting where donor countries announce contributions and list what they will go to: budget, energy, reconstruction. Good preparation and transparent reports raise the trust of partners.',
)

decision(
    id='UKR_wd_drone_batch', icon='GFX_decision_generic_army_support',
    visible='has_war_with = SOV\nhas_completed_focus = UKR_w_drone_war',
    cost=15, days_re_enable=60,
    complete='\n'.join([
        'army_experience = 5',
        'UKR_w_mio_drones_batch = yes',
    ]),
    ru='Серия дронов',
    ru_d='Очередная партия беспилотников из мастерских и заводов уходит на передовую. Дёшево, быстро и каждый раз чуть умнее предыдущей.',
    en='Drone Batch',
    en_d='Another batch of drones from workshops and factories goes to the front. Cheap, fast, and a little smarter every time.',
)

decision(
    id='UKR_wd_grid_repair', icon='GFX_decision_generic_construction',
    visible='has_war_with = SOV\nhas_completed_focus = UKR_w_resilient_grid',
    cost=20, days_re_enable=90,
    complete='\n'.join([
        'add_stability = 0.01',
        'add_timed_idea = { idea = UKR_wi_grid_repair days = 45 }',
    ]),
    ru='Ремонтные бригады энергетиков',
    ru_d='Бригады с запасом оборудования выезжают сразу после удара и восстанавливают подстанции под обстрелом. Свет возвращается быстрее, а люди видят, что власть работает.',
    en='Power Repair Crews',
    en_d='Crews with stocks of equipment leave right after a strike and restore substations under fire. The lights come back sooner and people see that the state is working.',
)

# ---------------------------------------------------------------- События ukrainewar.810-818
# opts: список вариантов (ru, en, эффект). 810-812 - вводные (один вариант), 813-818 - реакции на выбор игрока (два варианта).
# extra: дополнительные условия trigger. Картинки временные (`# art: reuse` ставит генератор).
E = [
    dict(id=810, pic='GFX_event_UKR_start_war',
         t_ru='Война пришла в каждый дом', t_en='War Comes to Every Home',
         d_ru='Утро начинается не с будильника, а с сирены. В подвалах и метро - соседи с детьми и сумками, на трассах - колонны, у банкоматов - тишина. Ещё вчера страна спорила о кабинетах и налогах, сегодня все разговоры о том, где выход и сколько у нас времени.\n\nВ канцеляриях не спят: военное положение, единый штаб, мобилизация и связь с партнёрами решаются в одну неделю. Дальше начинается дерево войны: каждое решение открывает новые возможности, но закрывает другие. Выбирать придётся быстро.',
         d_en='The morning begins not with an alarm clock but with a siren. In basements and the metro, neighbours with children and bags; on the highways, columns; at cash machines, silence. Only yesterday the country argued about cabinets and taxes, today every conversation is about where the exit is and how much time we have.\n\nNobody sleeps in the offices: martial law, a unified headquarters, mobilization and contact with partners must be settled in a single week. Then the war tree begins: every decision opens new possibilities but closes others. We will have to choose fast.',
         opts=[('Мы к этому шли. Теперь - работать.', 'We have been heading here. Now, to work.', 'custom_effect_tooltip = UKR_w_tt_tree_intro')]),
    dict(id=811, pic='GFX_UKR_preparing_for_war',
         t_ru='Военное положение', t_en='Martial Law',
         d_ru='Парламент проголосовал за военное положение и всеобщую мобилизацию. Указ вводит ограничения на выезд и собрания, запрещает выборы на время войны и передаёт часть полномочий военным администрациям. Это не победа и не поражение, а инструмент: он позволяет государству требовать то, без чего оборона невозможна, и именно поэтому его нельзя растягивать без нужды.\n\nЕдиный штаб собрал армию, Территориальную оборону, пограничников, разведку и гражданскую власть под одной крышей. Теперь вопрос не в том, что делать, а в том, как.',
         d_en='Parliament has voted for martial law and general mobilization. The decree restricts travel and assembly, bans elections for the duration of the war and hands part of the powers to military administrations. It is neither victory nor defeat but an instrument: it lets the state demand what defence cannot do without, and that is exactly why it must not be stretched without need.\n\nThe unified headquarters has brought the army, the Territorial Defence, the border guards, intelligence and civilian authority under one roof. The question is no longer what to do, but how.',
         opts=[('Так нужно.', 'It has to be so.', '')]),
    dict(id=812, pic='GFX_Generic_Tank_column',
         t_ru='Война затягивается', t_en='The War Drags On',
         d_ru='Первые недели позади. Фронт стабилизировался, но стало ясно, что быстрой развязки не будет. Нужны другие инструменты: учить, строить, договариваться, производить. Пора думать не о первых днях, а о первых месяцах и годах.\n\nНа дереве войны открываются фокусы второй ступени.',
         d_en='The first weeks are behind us. The front has stabilized, but it is clear that there will be no quick resolution. Other tools are needed: to train, to build, to negotiate, to produce. It is time to think not about the first days but about the first months and years.\n\nSecond-tier focuses open on the war tree.',
         extra=['has_country_flag = UKR_w_started', 'NOT = { has_country_flag = UKR_w_tier2 }'],
         opts=[('Готовимся к долгой войне.', 'We prepare for a long war.', 'set_country_flag = UKR_w_tier2\ncustom_effect_tooltip = UKR_w_tt_tier2')]),
    dict(id=813, pic='GFX_Development_Military',
         t_ru='Контракт, который читают вслух', t_en='A Contract Read Aloud',
         d_ru='Выплаты бойцам и семьям стали главной темой в очередях у пунктов набора. Контракт читают вслух: сумма, страховка, компенсация за ранение. Люди сравнивают его с зарплатой на заводе и с тем, что обещают другие армии, и всё чаще выбирают службу по договору, а не повестку.\n\nНо деньги не безграничны. Финансисты напоминают: выплаты нужно индексировать вместе с ценами, иначе через полгода контракт обесценится, а в войсках начнутся разговоры о задержках. Либо часть средств можно направить на снаряжение, которого не хватает.',
         d_en='Pay for fighters and their families has become the main topic in the queues at recruitment points. The contract is read aloud: the sum, the insurance, compensation for wounds. People compare it with a factory wage and with what other armies promise, and more and more often choose a contract over a summons.\n\nBut money is not unlimited. The financiers remind us: payments must be indexed with prices, otherwise in half a year the contract will lose its value and talk of delays will begin in the ranks. Or part of the funds could go to the equipment that is short.',
         opts=[('Индексировать выплаты.', 'Index the payments.',
                'set_temp_variable = { var = income_var_temp value = -1 }\nadd_income_with_inflation = yes\nadd_manpower = 5000\nhidden_effect = { add_to_variable = { var = UKRwarfatigue value = -2 } }\ncustom_effect_tooltip = UKR_w_tt_fatigue_down'),
               ('Направить средства на снаряжение.', 'Put the funds into equipment.',
                'add_equipment_to_stockpile = { type = support_equipment amount = 300 producer = UKR }\nadd_stability = -0.01')]),
    dict(id=814, pic='GFX_UKR_preparing_for_war',
         t_ru='Лозунг на каждой остановке', t_en='A Slogan at Every Stop',
         d_ru='Плакаты, песни, ролики и выступления: страну заливает волна лозунгов. Добровольцы идут целыми классами и трудовыми коллективами, очереди растут. В первые месяцы такая мобилизация работает лучше любых приказов.\n\nПроблема в том, что лозунги не заменяют ротацию, обучение и отпуска. А резкая риторика доходит и до европейских столиц, где её читают внимательно: партнёры готовы помогать обороне, но не войне на уничтожение.',
         d_en='Posters, songs, videos and speeches: a wave of slogans floods the country. Volunteers come by whole classes and work collectives, the queues grow. In the first months such mobilization works better than any orders.\n\nThe trouble is that slogans do not replace rotation, training and leave. And sharp rhetoric reaches the European capitals too, where it is read closely: partners are ready to help a defence, but not a war of annihilation.',
         opts=[('Поддержать волну.', 'Ride the wave.',
                'add_war_support = 0.02\nadd_popularity = { ideology = nationalist popularity = 0.005 }\nhidden_effect = { add_to_variable = { var = UKRhate value = 2 } }\ncustom_effect_tooltip = UKR_w_tt_hate_up'),
               ('Говорить о праве, а не о ненависти.', 'Speak of right, not of hatred.',
                'add_stability = 0.01\nUKR_trust_restraint = yes\nhidden_effect = { add_to_variable = { var = UKRhate value = -2 } }\ncustom_effect_tooltip = UKR_w_tt_hate_down')]),
    dict(id=815, pic='GFX_Generic_Tank_column',
         t_ru='Повестки у остановок', t_en='Summonses at the Bus Stops',
         d_ru='В очередях у военкоматов появились жалобы: повестки вручают на улице, документы проверяют у выходов из метро, в соцсетях разлетаются ролики о задержаниях. Власти объясняют: фронту нужны люди, а ответственность за уклонение предусмотрена законом. Родные призванных пишут в приёмные, депутаты шлют запросы.\n\nПартнёры эту тему обсуждают спокойно: любая армия, воюющая долго, сталкивается с тем же. Но общество требует правил, и от вас зависит, получит ли оно их.',
         d_en='Complaints have appeared in the queues at enlistment offices: summonses are served in the street, documents are checked at metro exits, videos of detentions spread on social media. The authorities explain: the front needs people, and liability for evasion is provided by law. Relatives of conscripts write to reception offices, deputies send inquiries.\n\nPartners discuss the subject calmly: any army that fights for long faces the same. But society demands rules, and it is up to you whether it gets them.',
         opts=[('Ограничить злоупотребления.', 'Curb the abuses.',
                'add_stability = 0.01\nadd_manpower = -5000\nhidden_effect = { add_to_variable = { var = UKRwarfatigue value = -2 } }\ncustom_effect_tooltip = UKR_w_tt_fatigue_down'),
               ('Людей нужно фронту.', 'The front needs people.',
                'add_manpower = 10000\nadd_stability = -0.01\nhidden_effect = { add_to_variable = { var = UKRwarfatigue value = 2 } }\ncustom_effect_tooltip = UKR_w_tt_fatigue_up')]),
    dict(id=816, pic='GFX_UKR_big_construction_event',
         t_ru='Эшелоны на запад', t_en='Trains to the West',
         d_ru='К железнодорожным узлам тянутся составы: станки в разобранном виде, ящики с документацией, вагоны с семьями рабочих. Предприятие, которое разбирали неделю, собирают заново месяцами: сначала крыша и электричество, потом станки и только потом смена.\n\nВ штабе вопрос ребром: что грузить первым. Сохранить людей и оборудование или сначала оборонные цеха, которые нужны фронту уже сейчас.',
         d_en='Trains stream to the railway hubs: machine tools in pieces, crates of documentation, carriages with workers\' families. A plant that took a week to dismantle takes months to reassemble: first a roof and electricity, then the machines, and only then a shift.\n\nThe headquarters faces the question squarely: what to load first. To save people and equipment, or to start with the defence workshops the front needs right now.',
         opts=[('Сохранить людей и оборудование.', 'Save people and equipment.', 'add_stability = 0.02\nadd_political_power = 10'),
               ('Сначала оборонные цеха.', 'Defence workshops first.',
                'add_equipment_to_stockpile = { type = support_equipment amount = 300 producer = UKR }\nadd_stability = -0.01')]),
    dict(id=817, pic='GFX_PRC_drone_uav',
         t_ru='Дроны из гаража', t_en='Drones from the Garage',
         d_ru='При волонтёрских центрах и в гаражах собирают дроны: из серийных камер, плат и моторов, часто за одну ночь. Командиры на передовой берут всё, что летит, но вместе с ними приходят и проблемы: разные частоты, разное качество, нет учёта и запчастей.\n\nГенштаб предлагает навести порядок: стандарты, закупки, обучение операторов. Волонтёры опасаются, что бюрократия убьёт скорость. Решать вам.',
         d_en='At volunteer centres and in garages, drones are assembled from off-the-shelf cameras, boards and motors, often overnight. Commanders at the front take anything that flies, but problems come with them: different frequencies, different quality, no accounting and no spare parts.\n\nThe General Staff proposes to put things in order: standards, procurement, operator training. Volunteers fear that bureaucracy will kill the speed. It is for you to decide.',
         opts=[('Принять в армию и стандартизировать.', 'Take them into the army and standardize.', 'army_experience = 5\nUKR_w_mio_drones_batch = yes'),
               ('Поддержать волонтёров грантами.', 'Support the volunteers with grants.',
                'set_temp_variable = { var = income_var_temp value = -1 }\nadd_income_with_inflation = yes\nadd_war_support = 0.02')]),
    dict(id=818, pic='GFX_UKR_diplomat',
         t_ru='Столицы отвечают', t_en='The Capitals Respond',
         d_ru='Выступления в парламентах, свидетельства очевидцев и ежедневные материалы для прессы дали результат: в европейских столицах заговорили о помощи, а в профильных комитетах появились рабочие группы. Но симпатии не равны поставкам, а поставки не равны гарантиям.\n\nПартнёры просят одного: отчётности. Куда идут деньги и техника, кто за это отвечает. Прозрачность закрывает дверь для подозрений, но открывает её для вопросов.',
         d_en='Speeches in parliaments, eyewitness accounts and daily material for the press have produced results: the European capitals have started talking about aid, and working groups have appeared in the relevant committees. But sympathy is not deliveries, and deliveries are not guarantees.\n\nPartners ask for one thing: accountability. Where the money and equipment go, and who answers for it. Transparency closes the door to suspicion, but opens it to questions.',
         opts=[('Принять помощь и отчитаться.', 'Accept the aid and report.', 'add_political_power = 10\nUKR_trust_transparency = yes'),
               ('Принять помощь и просить больше.', 'Accept the aid and ask for more.', 'add_political_power = 20')]),
]

# ---------------------------------------------------------------- Подсказки и служебные ключи
TT = {
    'UKR_w_tt_hate_up': ('Ненависть к врагу §Rрастёт§!', 'Hatred of the enemy §Rgrows§!'),
    'UKR_w_tt_hate_down': ('Ненависть к врагу §Gснижается§!', 'Hatred of the enemy §Gfalls§!'),
    'UKR_w_tt_fatigue_up': ('Усталость от войны §Rрастёт§!', 'War weariness §Rgrows§!'),
    'UKR_w_tt_fatigue_down': ('Усталость от войны §Gснижается§!', 'War weariness §Gfalls§!'),
    'UKR_w_tt_air_point': ('Очки ПВО: §G+1§!', 'Air defence points: §G+1§!'),
    'UKR_w_tt_seat_up': ('Место Украины в штабе коалиции §Gповышается§!', 'Ukraine\'s seat in the coalition headquarters §Grises§!'),
    'UKR_w_tt_election_ban': ('Выборы не проводятся, пока идёт война', 'No elections are held while the war lasts'),
    'UKR_w_tt_tree_intro': ('Открыто дерево войны: пять направлений и фокусы вашей опоры', 'The war tree is open: five directions and the focuses of your pillar'),
    'UKR_w_tt_tier2': ('Открыты фокусы второй ступени', 'Second-tier focuses are open'),
    'UKR_w_tt_mio_drones': ('Кластер беспилотных систем (оборонная промышленность): §G+300§! средств', 'Drone cluster (defence industry): §G+300§! funds'),
    'UKR_w_tt_mio_drones_batch': ('Кластер беспилотных систем (оборонная промышленность): §G+100§! средств', 'Drone cluster (defence industry): §G+100§! funds'),
    'UKR_w_tt_mio_state_order': ('Малышев, ремонт бронетехники и артиллерийские заводы: §G+250§! средств каждой организации', 'Malyshev, armour repair and artillery works: §G+250§! funds to each organization'),
    'UKR_w_tt_mio_private': ('Беспилотники, радиоэлектроника и верфь: §G+250§! средств каждой организации', 'Drones, radio electronics and the shipyard: §G+250§! funds to each organization'),
    'UKR_w_tt_mio_self_reliance': ('КрАЗ, Антонов и Мотор Сич: §G+150§! средств каждой организации', 'KrAZ, Antonov and Motor Sich: §G+150§! funds to each organization'),
    'UKR_w_tt_mio_sea': ('Николаевская верфь (морские дроны): §G+250§! средств', 'Mykolaiv shipyard (naval drones): §G+250§! funds'),
}
