# -*- coding: utf-8 -*-
# Данные дерева войны (DESIGN.md 8.5, сессия 24). Источник правды для common/national_focus/UKR_war_shared_focus.txt
# и ключей фокусов в localisation/*/UKR_war_tree_l_*.yml. После правки: python3 _tools/gen_war_tree.py --write
#
# Поля: id, x, y, cost, icon, ru, ru_d, en, en_d, prereq (список групп-ИЛИ), excl, avail, allow, reward, ai, tier2
# Сетка: step 2 по x, y от 16 (ниже всех шести деревьев; блок 1 заканчивается на y=14).

T2 = 'OR = { has_country_flag = UKR_coalition_phase has_country_flag = UKR_w_tier2 }'
STARTED = 'has_country_flag = UKR_w_started'

F = []


def focus(**kw):
    kw.setdefault('prereq', [])
    kw.setdefault('excl', [])
    kw.setdefault('avail', '')
    kw.setdefault('allow', STARTED)
    kw.setdefault('ai', 'factor = 20')
    kw.setdefault('tier2', False)
    F.append(kw)


def hate(n):
    s = 'up' if n > 0 else 'down'
    return 'hidden_effect = { add_to_variable = { var = UKRhate value = %d } }\ncustom_effect_tooltip = UKR_w_tt_hate_%s' % (n, s)


def fat(n):
    s = 'up' if n > 0 else 'down'
    return 'hidden_effect = { add_to_variable = { var = UKRwarfatigue value = %d } }\ncustom_effect_tooltip = UKR_w_tt_fatigue_%s' % (n, s)


def lean(name, n):
    return 'hidden_effect = {\n\tadd_to_variable = { var = UKR_%s_lean value = %d }\n\tUKR_clamp_leans = yes\n}' % (name, n)


def timed(idea, days):
    return 'add_timed_idea = { idea = %s days = %d }' % (idea, days)


def unlock(*decs):
    return '\n'.join('unlock_decision_tooltip = %s' % d for d in decs)


def income(v):
    return 'set_temp_variable = { var = income_var_temp value = %s }\nadd_income_with_inflation = yes' % v


# ---------------------------------------------------------------- Вводные
focus(
    id='UKR_w_war_comes_home', x=18, y=16, cost=1, icon='GFX_goal_generic_national_unity',
    allow=STARTED, avail='has_war_with = SOV',
    ai='factor = 1000',
    ru='Война пришла в каждый дом',
    ru_d='Сирены, укрытия, колонны на дорогах. То, о чём говорили годами, стало повседневностью: страна просыпается уже на другой войне.\n\nЭтот фокус завершается сам и отмечает рубеж: с этого дня вся политика, экономика и жизнь подчинены одному вопросу.',
    en='War Comes to Every Home',
    en_d='Sirens, shelters, columns on the roads. What was discussed for years has become daily life: the country wakes up in a different war.\n\nThis focus completes on its own and marks the line: from this day, politics, the economy and everyday life answer to a single question.',
    reward='add_war_support = 0.05',
)

focus(
    id='UKR_w_martial_law', x=18, y=17, cost=1, icon='GFX_goal_generic_defence',
    prereq=[['UKR_w_war_comes_home']], avail='has_war_with = SOV',
    ai='factor = 1000',
    ru='Военное положение и единый штаб',
    ru_d='Военное положение - особый правовой режим: ограничения на выезд и собрания, право государства требовать ресурсы для обороны, запрет выборов. Неделя уходит на указы, голосование в парламенте и создание единого штаба, где сходятся армия, власть и связь.\n\nПока идёт война, выборы не проводятся. Дальше дерево разветвляется: каждый выбор открывает новые решения и временные духи, но закрывает другие пути.',
    en='Martial Law and a Unified Headquarters',
    en_d='Martial law is a special legal regime: limits on travel and assembly, the right of the state to requisition resources for defence, and a ban on elections. A week goes to decrees, a parliamentary vote and the creation of a unified headquarters where the army, the government and communications meet.\n\nWhile the war lasts, no elections are held. From here the tree branches: every choice opens new decisions and temporary national spirits, but closes other paths.',
    reward='\n'.join([
        'add_ideas = UKR_wi_martial_law',
        'add_stability = 0.03',
        'add_political_power = 25',
        'set_country_flag = UKR_w_martial_law',
        'custom_effect_tooltip = UKR_w_tt_election_ban',
        'UKR_martial_law_elections_off = yes',
        'hidden_effect = {',
        '\tcountry_event = { id = ukrainewar.811 days = 1 }',
        '\tcountry_event = { id = ukrainewar.812 days = 120 }',
        '}',
    ]),
)

# ---------------------------------------------------------------- A. Командование (колонка x=3)
focus(
    id='UKR_w_supreme_command', x=3, y=18, cost=3, icon='GFX_goal_generic_army_doctrines',
    prereq=[['UKR_w_martial_law']],
    ru='Ставка Верховного главнокомандующего',
    ru_d='Ставка - орган, где глава государства и военные вместе решают, как вести войну. Единый центр сокращает путь от приказа к исполнению, а Генштаб получает право планировать на всю страну.\n\nОткрывает возможность укрепить границу.',
    en="Supreme Commander's Headquarters",
    en_d='The Headquarters is the body where the head of state and the military decide together how to fight. A single centre shortens the path from order to execution, and the General Staff gains the right to plan for the whole country.\n\nMakes it possible to fortify the border.',
    reward='\n'.join([
        'add_command_power = 30',
        'add_ideas = UKR_wi_stavka',
        unlock('UKR_establish_border_defense_system'),
    ]),
)

focus(
    id='UKR_w_unified_command', x=1, y=19, cost=4, icon='GFX_goal_generic_army_doctrines',
    prereq=[['UKR_w_supreme_command']], excl=['UKR_w_operational_commands'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_authoritarian_lean value = UKR_digital_lean compare = greater_than } }',
    ru='Единое командование',
    ru_d='Вся армия, Территориальная оборона и силы безопасности подчиняются одному штабу. Планирование проще, наступательные операции согласованнее, но местные командиры теряют часть инициативы.\n\nОткрывает наступательное решение.',
    en='Unified Command',
    en_d='The whole army, the Territorial Defence and the security forces answer to a single staff. Planning is simpler and offensive operations are better coordinated, but local commanders lose some initiative.\n\nUnlocks an offensive decision.',
    reward='\n'.join([
        'add_ideas = UKR_wi_unified_command',
        unlock('UKR_rapid_offensive_surge'),
    ]),
)

focus(
    id='UKR_w_operational_commands', x=5, y=19, cost=4, icon='GFX_goal_generic_army_doctrines',
    prereq=[['UKR_w_supreme_command']], excl=['UKR_w_unified_command'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_digital_lean value = UKR_authoritarian_lean compare = greater_than } }',
    ru='Операционные командования',
    ru_d='Фронт делят на направления со своими командующими, которым дано право решать на месте. Подразделения гибче и живучее, но общему плану труднее.\n\nОткрывает решение о быстром бронированном ударе.',
    en='Operational Commands',
    en_d='The front is divided into sectors with their own commanders, who are given the right to decide on the spot. Units become more flexible and resilient, but the overall plan is harder to keep.\n\nUnlocks a decision for a fast armoured thrust.',
    reward='\n'.join([
        'add_ideas = UKR_wi_operational',
        unlock('UKR_rapid_armored_thrust'),
    ]),
)

focus(
    id='UKR_w_battle_experience', x=3, y=20, cost=4, icon='GFX_goal_generic_army_doctrines', tier2=True,
    prereq=[['UKR_w_unified_command', 'UKR_w_operational_commands']], avail=T2,
    ru='Боевой опыт - в доктрину',
    ru_d='Уроки первых месяцев записывают в уставы: что работало, что стоило лишних потерь. Вместо вчерашних учебников - практика фронта. Выигрыш зависит от выбранной системы командования.\n\nОткрывает решение о штурме опорного пункта.',
    en='Battle Experience into Doctrine',
    en_d='The lessons of the first months are written into regulations: what worked, what cost needless losses. Instead of yesterday\'s textbooks, the practice of the front. The gain depends on the chosen command system.\n\nUnlocks a decision for assaulting a fortified position.',
    reward='\n'.join([
        'army_experience = 50',
        'if = {',
        '\tlimit = { has_completed_focus = UKR_w_unified_command }',
        '\t' + timed('UKR_wi_staff_rhythm', 270),
        '}',
        'else = {',
        '\t' + timed('UKR_wi_local_initiative', 270),
        '}',
        'if = {',
        '\tlimit = { has_completed_focus = UKR_army_consolidation }',
        '\tarmy_experience = 25',
        '}',
        unlock('UKR_azov_steel_operation'),
    ]),
)

# ---------------------------------------------------------------- B. Люди и тыл (колонка x=9)
focus(
    id='UKR_w_general_mobilization', x=9, y=18, cost=3, icon='GFX_goal_generic_national_unity',
    prereq=[['UKR_w_martial_law']],
    ru='Всеобщая мобилизация',
    ru_d='Призыв по всей стране: резервисты, добровольцы, специалисты. Людей нужно обучить, одеть и вооружить, а каждый призванный - это человек, ушедший с завода или с поля.\n\nОткрывает вторую и третью волны мобилизации и выбор способа, которым государство будет собирать людей.',
    en='General Mobilization',
    en_d='Conscription across the whole country: reservists, volunteers, specialists. People must be trained, clothed and armed, and every conscript is one person fewer at the factory or in the field.\n\nUnlocks the second and third mobilization waves and a choice of how the state will gather its people.',
    reward='\n'.join([
        'add_manpower = 40000',
        'add_stability = -0.03',
        'add_war_support = 0.02',
        fat(2),
        unlock('UKR_second_mobilization_wave', 'UKR_third_mobilization_wave', 'UKR_wd_mobilization_campaign'),
    ]),
)

focus(
    id='UKR_w_pay_the_soldiers', x=7, y=19, cost=4, icon='GFX_goal_generic_consumer_goods',
    prereq=[['UKR_w_general_mobilization']], excl=['UKR_w_call_to_the_nation', 'UKR_w_forced_mobilization'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_left_lean value = UKR_nationalist_lean compare = greater_than } }',
    ru='Достойное содержание',
    ru_d='Контракт с достойной оплатой, выплаты семьям, льготы раненым. Люди идут охотнее и держатся на фронте дольше, но бюджет платит каждый месяц.\n\nВзаимоисключающий выбор: способ мобилизации - деньги, лозунги или принуждение.',
    en='Decent Pay',
    en_d='A contract with decent pay, payments to families, benefits for the wounded. People enlist more willingly and stay at the front longer, but the budget pays every month.\n\nMutually exclusive choice: the method of mobilization - money, slogans or coercion.',
    reward='\n'.join([
        income('-2'),
        'add_ideas = UKR_wi_military_pay',
        'hidden_effect = { country_event = { id = ukrainewar.813 days = 20 } }',
        fat(-3),
        lean('left', 2),
    ]),
)

focus(
    id='UKR_w_call_to_the_nation', x=9, y=19, cost=4, icon='GFX_goal_generic_propaganda',
    prereq=[['UKR_w_general_mobilization']], excl=['UKR_w_pay_the_soldiers', 'UKR_w_forced_mobilization'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_nationalist_lean value = UKR_left_lean compare = greater_than } }',
    ru='Призыв к нации',
    ru_d='Мобилизация лозунгами: история, язык, образ врага. Волна добровольцев и высокий дух, но такая риторика подпитывает ненависть и усиливает националистов.\n\nВзаимоисключающий выбор: способ мобилизации.',
    en='Call to the Nation',
    en_d='Mobilization by slogans: history, language, the image of the enemy. A wave of volunteers and high morale, but such rhetoric feeds hatred and strengthens the nationalists.\n\nMutually exclusive choice: the method of mobilization.',
    reward='\n'.join([
        timed('UKR_wi_patriotic_wave', 365),
        'hidden_effect = { country_event = { id = ukrainewar.814 days = 20 } }',
        'add_manpower = 15000',
        hate(4),
        'add_popularity = { ideology = nationalist popularity = 0.01 }',
        lean('nationalist', 3),
    ]),
)

focus(
    id='UKR_w_forced_mobilization', x=11, y=19, cost=4, icon='GFX_goal_generic_dangerous_deal',
    prereq=[['UKR_w_general_mobilization']], excl=['UKR_w_pay_the_soldiers', 'UKR_w_call_to_the_nation'],
    ai='factor = 4\nmodifier = { factor = 3 check_variable = { var = UKR_authoritarian_lean value = 40 compare = greater_than } }',
    ru='Принудительный призыв',
    ru_d='Облавы у военкоматов, повестки на улице, штрафы за уклонение. Армия получает людей быстро, но общество недовольно: жалобы на злоупотребления множатся, а доверие к власти падает. Платит за это стабильность, а не репутация у союзников.\n\nВзаимоисключающий выбор: способ мобилизации.',
    en='Forced Conscription',
    en_d='Raids at enlistment offices, summonses served in the street, fines for evasion. The army gets people fast, but society is unhappy: complaints about abuses multiply and trust in the authorities falls. The price is paid in stability, not in standing with allies.\n\nMutually exclusive choice: the method of mobilization.',
    reward='\n'.join([
        'add_manpower = 60000',
        'add_ideas = UKR_wi_forced_draft',
        'hidden_effect = { country_event = { id = ukrainewar.815 days = 20 } }',
        fat(5),
        lean('authoritarian', 3),
    ]),
)

focus(
    id='UKR_w_reserve_and_veterans', x=9, y=20, cost=4, icon='GFX_goal_generic_national_unity', tier2=True,
    prereq=[['UKR_w_pay_the_soldiers', 'UKR_w_call_to_the_nation', 'UKR_w_forced_mobilization']], avail=T2,
    ru='Резерв и ветераны',
    ru_d='Бывшие бойцы возвращаются инструкторами, раненых лечат и переучивают, резервисты проходят подготовку. Результат зависит от того, как страна мобилизовала людей раньше.\n\nОткрывает решения по памяти погибших и помощи ветеранам.',
    en='Reserve and Veterans',
    en_d='Former fighters return as instructors, the wounded are treated and retrained, reservists complete their training. The result depends on how the country mobilized its people earlier.\n\nUnlocks decisions on honouring the fallen and helping veterans.',
    reward='\n'.join([
        'if = {',
        '\tlimit = { has_completed_focus = UKR_w_pay_the_soldiers }',
        '\tadd_manpower = 15000',
        '\tarmy_experience = 10',
        '}',
        'else_if = {',
        '\tlimit = { has_completed_focus = UKR_w_call_to_the_nation }',
        '\tadd_manpower = 20000',
        '\t' + hate(2).replace('\n', '\n\t'),
        '}',
        'else = {',
        '\tadd_manpower = 25000',
        '\t' + fat(3).replace('\n', '\n\t'),
        '}',
        unlock('UKR_honor_fallen', 'UKR_veteran_psych_care'),
    ]),
)

focus(
    id='UKR_w_united_news', x=7, y=21, cost=4, icon='GFX_goal_generic_propaganda',
    prereq=[['UKR_w_reserve_and_veterans']], excl=['UKR_w_open_communication'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_authoritarian_lean value = UKR_digital_lean compare = greater_than } }',
    ru='Единые новости',
    ru_d='Все телеканалы выпускают общий эфир: единая картина, меньше паники, нет противоречий. Но свободные СМИ теряют голос, а доверие к официальной версии держится только на успехах.\n\nВзаимоисключающий выбор: информационная политика военного времени. Открывает кампанию стойкости.',
    en='United News',
    en_d='All television channels broadcast one shared programme: a single picture, less panic, no contradictions. But free media lose their voice, and trust in the official version rests only on successes.\n\nMutually exclusive choice: wartime information policy. Unlocks the resilience campaign.',
    reward='\n'.join([
        'add_ideas = UKR_wi_unified_info',
        hate(2),
        lean('authoritarian', 4),
        unlock('UKR_resilience_campaign'),
    ]),
)

focus(
    id='UKR_w_open_communication', x=11, y=21, cost=4, icon='GFX_goal_generic_scientific_exchange',
    prereq=[['UKR_w_reserve_and_veterans']], excl=['UKR_w_united_news'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_digital_lean value = UKR_authoritarian_lean compare = greater_than } }',
    ru='Открытая коммуникация',
    ru_d='Ежедневные брифинги, честные потери, спор в эфире. Доверие и прозрачность растут, союзники видят открытую страну, но враг читает всё, что мы говорим.\n\nВзаимоисключающий выбор: информационная политика военного времени. Открывает культурную кампанию.',
    en='Open Communication',
    en_d='Daily briefings, honest casualty figures, debate on air. Trust and transparency grow and allies see an open country, but the enemy also reads everything we say.\n\nMutually exclusive choice: wartime information policy. Unlocks the cultural campaign.',
    reward='\n'.join([
        'add_ideas = UKR_wi_open_comms',
        lean('digital', 4),
        'UKR_trust_transparency = yes',
        unlock('UKR_cultural_morale_boost'),
    ]),
)

# ---------------------------------------------------------------- C. Промышленность, тыл, ПВО (колонка x=21)
focus(
    id='UKR_w_relocate_industry', x=21, y=18, cost=3, icon='GFX_goal_generic_construct_civ_factory',
    prereq=[['UKR_w_martial_law']],
    ru='Эвакуация промышленности на запад',
    ru_d='Заводы разбирают и вывозят с востока и юга на запад: станки, люди, архивы. Месяцы простоя, но потом производство возвращается там, куда сложнее достать.\n\nОткрывает карпатский логистический план и рассредоточение производства.',
    en='Relocate Industry to the West',
    en_d='Factories are dismantled and moved from the east and south to the west: machine tools, people, archives. Months of downtime, but then production returns where it is harder to reach.\n\nUnlocks the Carpathian logistics plan and the dispersal of production.',
    reward='\n'.join([
        timed('UKR_wi_relocation', 180),
        'hidden_effect = { country_event = { id = ukrainewar.816 days = 30 } }',
        unlock('UKR_carpathian_logistics_plan', 'UKR_wd_factory_dispersal'),
    ]),
)

focus(
    id='UKR_w_state_war_order', x=19, y=19, cost=4, icon='GFX_goal_generic_construct_mil_factory',
    prereq=[['UKR_w_relocate_industry']], excl=['UKR_w_private_contracts'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_left_lean value = UKR_digital_lean compare = greater_than } }',
    ru='Государственный оборонный заказ',
    ru_d='Государство размещает заказы напрямую, определяет цены и сроки. Предсказуемо и подконтрольно, но частная инициатива ограничена. Усиливает танковые, ремонтные и артиллерийские предприятия.\n\nВзаимоисключающий выбор: кто управляет военным производством. Открывает дополнительный оборонный проект.',
    en='State Defence Order',
    en_d='The state places orders directly and sets prices and deadlines. Predictable and controlled, but private initiative is limited. Strengthens the tank, repair and artillery enterprises.\n\nMutually exclusive choice: who runs wartime production. Unlocks an additional defence project.',
    reward='\n'.join([
        'add_ideas = UKR_wi_state_order',
        'UKR_w_mio_state_order = yes',
        unlock('UKR_project_asgard'),
    ]),
)

focus(
    id='UKR_w_private_contracts', x=23, y=19, cost=4, icon='GFX_goal_generic_trade',
    prereq=[['UKR_w_relocate_industry']], excl=['UKR_w_state_war_order'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_digital_lean value = UKR_left_lean compare = greater_than } }',
    ru='Контракты для частных производителей',
    ru_d='Заказы получают частные компании: дроны, радиоэлектроника, катера. Скорость и изобретательность выше, но контроль слабее, а прибыль уходит владельцам.\n\nВзаимоисключающий выбор: кто управляет военным производством. Открывает дополнительный оборонный проект.',
    en='Private Producer Contracts',
    en_d='Orders go to private companies: drones, radio electronics, boats. Speed and inventiveness are higher, but control is weaker and profits go to the owners.\n\nMutually exclusive choice: who runs wartime production. Unlocks an additional defence project.',
    reward='\n'.join([
        'add_ideas = UKR_wi_private_contracts',
        'UKR_w_mio_private = yes',
        unlock('UKR_project_asgard'),
    ]),
)

focus(
    id='UKR_w_sky_shield', x=21, y=20, cost=4, icon='GFX_goal_generic_defence', tier2=True,
    prereq=[['UKR_w_state_war_order', 'UKR_w_private_contracts']], avail=T2,
    ru='Щит неба',
    ru_d='Многослойная ПВО: дальнобойные комплексы вокруг столицы и узлов энергетики, зенитные расчёты и мобильные огневые группы прикрывают города. Каждый комплекс стоит дорого, но удары по инфраструктуре становятся реже и слабее.',
    en='Shield of the Sky',
    en_d='Layered air defence: long-range systems around the capital and energy hubs, anti-aircraft crews and mobile fire groups cover the cities. Every system is expensive, but strikes on infrastructure become rarer and weaker.',
    reward='\n'.join([
        'add_to_variable = { var = UKR_air_defense_points value = 1 }',
        'UKR_update_air_defense_level = yes',
        'custom_effect_tooltip = UKR_w_tt_air_point',
        timed('UKR_wi_sky_shield', 180),
    ]),
)

focus(
    id='UKR_w_resilient_grid', x=21, y=21, cost=4, icon='GFX_goal_generic_construct_civ_factory', tier2=True,
    prereq=[['UKR_w_sky_shield']],
    ru='Живучая энергосистема',
    ru_d='Распределённая генерация, резервные подстанции, мобильные ремонтные бригады. Удары по энергетике по-прежнему болезненны, но свет возвращается быстрее.\n\nОткрывает решение о ремонтных бригадах энергетиков.',
    en='Resilient Power Grid',
    en_d='Distributed generation, reserve substations, mobile repair crews. Strikes on the power system still hurt, but the lights come back sooner.\n\nUnlocks a decision for power repair crews.',
    reward='\n'.join([
        'add_ideas = UKR_wi_resilient_grid',
        'add_stability = 0.02',
        unlock('UKR_wd_grid_repair'),
    ]),
)

# ---------------------------------------------------------------- D. Союзники (колонка x=27)
focus(
    id='UKR_w_appeal_to_the_world', x=27, y=18, cost=3, icon='GFX_goal_generic_improve_relations',
    prereq=[['UKR_w_martial_law']],
    ru='Обращение к миру',
    ru_d='Выступления в парламентах и международных организациях, свидетельства очевидцев, ежедневные материалы для прессы. Симпатии мира - ресурс, который нужно постоянно обновлять.\n\nОткрывает пакет западной помощи, коалицию сопротивления и конференцию доноров.',
    en='Appeal to the World',
    en_d='Speeches in parliaments and international organizations, eyewitness accounts, daily material for the press. The sympathy of the world is a resource that has to be renewed constantly.\n\nUnlocks the Western aid package, the resistance coalition and a donor conference.',
    reward='\n'.join([
        'add_political_power = 20',
        timed('UKR_wi_world_sympathy', 150),
        'hidden_effect = { country_event = { id = ukrainewar.818 days = 12 } }',
        'UKR_trust_diplomacy = yes',
        unlock('UKR_western_aid_package', 'UKR_resistance_coalition', 'UKR_wd_donor_conference'),
    ]),
)

focus(
    id='UKR_w_europe_first', x=25, y=19, cost=4, icon='GFX_goal_generic_improve_relations',
    prereq=[['UKR_w_appeal_to_the_world']], excl=['UKR_w_own_strength'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_digital_lean value = UKR_nationalist_lean compare = greater_than } }',
    ru='Европа - первым делом',
    ru_d='Курс на прочную связь с европейскими столицами: общие штабы, консультации, открытость. Помощь течёт увереннее, но мы берём на себя обязательства и теряем часть самостоятельности.\n\nВзаимоисключающий выбор: на кого опираться. Открывает ленд-лиз и разведывательную операцию с НАТО.',
    en='Europe First',
    en_d='A course for a firm bond with the European capitals: joint staffs, consultations, openness. Aid flows more reliably, but we take on obligations and lose some independence.\n\nMutually exclusive choice: whom to lean on. Unlocks lend-lease and an intelligence operation with NATO.',
    reward='\n'.join([
        'add_ideas = UKR_wi_europe_course',
        'UKR_trust_euro_course = yes',
        'set_country_flag = UKR_w_europe_first',
        unlock('UKR_lend_lease_program', 'UKR_nato_intelligence_operation'),
    ]),
)

focus(
    id='UKR_w_own_strength', x=29, y=19, cost=4, icon='GFX_goal_generic_secret_weapon',
    prereq=[['UKR_w_appeal_to_the_world']], excl=['UKR_w_europe_first'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_nationalist_lean value = UKR_digital_lean compare = greater_than } }',
    ru='Опора на собственные силы',
    ru_d='Не просить, а производить. Ставка на отечественные заводы и конструкторов: дольше и дороже, но чужие решения от нас не зависят.\n\nВзаимоисключающий выбор: на кого опираться. Добавляет средства организациям оборонной промышленности.',
    en='Self-Reliance',
    en_d='Not to ask but to produce. A bet on domestic factories and designers: slower and more expensive, but we do not depend on other people\'s decisions.\n\nMutually exclusive choice: whom to lean on. Adds funds to the defence industry organizations.',
    reward='\n'.join([
        'add_ideas = UKR_wi_self_reliance',
        'UKR_w_mio_self_reliance = yes',
        'set_country_flag = UKR_w_own_strength',
    ]),
)

focus(
    id='UKR_w_regional_security', x=27, y=20, cost=5, icon='GFX_goal_generic_improve_relations', tier2=True,
    prereq=[['UKR_w_europe_first', 'UKR_w_own_strength']], avail=T2,
    ru='Региональная безопасность',
    ru_d='Договоры с ближайшими соседями: общие склады, общая ПВО, быстрый обмен данными. Это не вступление в союз, но шаг к нему.\n\nОткрывает региональный союз, а при хорошем доверии коалиции поднимает место Украины в штабе.',
    en='Regional Security',
    en_d='Agreements with the nearest neighbours: shared depots, shared air defence, fast data exchange. This is not joining an alliance, but a step toward one.\n\nUnlocks the regional alliance and, with good coalition trust, raises Ukraine\'s seat in the headquarters.',
    reward='\n'.join([
        'add_political_power = 25',
        timed('UKR_wi_regional', 270),
        'if = {',
        '\tlimit = {',
        '\t\thas_country_flag = UKR_coalition_phase',
        '\t\tcheck_variable = { var = UKR_hq_seat value = 2 compare = less_than }',
        '\t\tcheck_variable = { var = UKR_nato_trust value = 55 compare = greater_than_or_equals }',
        '\t}',
        '\tset_temp_variable = { var = UKR_seat_new value = UKR_hq_seat }',
        '\tadd_to_temp_variable = { var = UKR_seat_new value = 1 }',
        '\tUKR_set_hq_seat = yes',
        '\tcustom_effect_tooltip = UKR_w_tt_seat_up',
        '}',
        unlock('UKR_regional_alliance'),
    ]),
)

# ---------------------------------------------------------------- E. Асимметричная война (колонка x=33)
focus(
    id='UKR_w_drone_war', x=33, y=18, cost=3, icon='GFX_goal_generic_secret_weapon',
    prereq=[['UKR_w_martial_law']],
    ru='Дроны на передовой',
    ru_d='Серийные беспилотники разведки и удара, собранные в мастерских и на заводах, дают то, чего не хватает артиллерии: глаза на передовой и дешёвый удар.\n\nОткрывает координацию ударов и серию дронов.',
    en='Drones at the Front',
    en_d='Mass-produced reconnaissance and strike drones, assembled in workshops and factories, provide what artillery lacks: eyes on the front line and a cheap strike.\n\nUnlocks strike coordination and a drone batch.',
    reward='\n'.join([
        timed('UKR_wi_drone_surge', 180),
        'hidden_effect = { country_event = { id = ukrainewar.817 days = 25 } }',
        'UKR_w_mio_drones = yes',
        unlock('UKR_bayraktar_strike_coordination', 'UKR_wd_drone_batch'),
    ]),
)

focus(
    id='UKR_w_deep_strikes', x=31, y=19, cost=4, icon='GFX_goal_generic_dangerous_deal',
    prereq=[['UKR_w_drone_war']], excl=['UKR_w_attrition_defense'],
    ai='factor = 8\nmodifier = { factor = 2 check_variable = { var = UKR_nationalist_lean value = 35 compare = greater_than } }',
    ru='Удары вглубь территории противника',
    ru_d='Склады, штабы и переправы за линией фронта становятся целями. Это ломает логистику врага и поднимает дух, но европейские столицы опасаются эскалации.\n\nВзаимоисключающий выбор: как вести войну. Открывает ночные рейды, диверсионную войну и ответ всеми средствами.',
    en='Deep Strikes',
    en_d='Depots, headquarters and crossings behind the front line become targets. This breaks the enemy\'s logistics and lifts morale, but European capitals fear escalation.\n\nMutually exclusive choice: how to fight. Unlocks night raids, a sabotage war and an all-out response.',
    reward='\n'.join([
        timed('UKR_wi_deep_strike', 180),
        'add_war_support = 0.03',
        hate(3),
        'UKR_trust_escalation = yes',
        unlock('UKR_night_raids_operation', 'UKR_sabotage_at_any_cost', 'UKR_everything_against_enemy'),
    ]),
)

focus(
    id='UKR_w_attrition_defense', x=35, y=19, cost=4, icon='GFX_goal_generic_defence',
    prereq=[['UKR_w_drone_war']], excl=['UKR_w_deep_strikes'],
    ai='factor = 10\nmodifier = { factor = 2 check_variable = { var = UKR_digital_lean value = UKR_nationalist_lean compare = greater_than } }',
    ru='Оборона на истощение',
    ru_d='Не рваться вперёд, а выматывать: минные поля, глубоко эшелонированные рубежи, огонь по наступающим колоннам. Меньше риска и больше доверия партнёров, но инициатива у врага.\n\nВзаимоисключающий выбор: как вести войну. Открывает оборону стратегического треугольника.',
    en='Defence of Attrition',
    en_d='Not to lunge forward but to wear down: minefields, defence in depth, fire on advancing columns. Less risk and more trust from partners, but the initiative belongs to the enemy.\n\nMutually exclusive choice: how to fight. Unlocks the defence of the strategic triangle.',
    reward='\n'.join([
        'add_ideas = UKR_wi_attrition',
        'UKR_trust_restraint = yes',
        unlock('UKR_strategic_triangle_defense'),
    ]),
)

focus(
    id='UKR_w_black_sea_drones', x=33, y=20, cost=4, icon='GFX_goal_generic_secret_weapon', tier2=True,
    prereq=[['UKR_w_deep_strikes', 'UKR_w_attrition_defense']], avail=T2,
    ru='Чёрное море: безэкипажные катера',
    ru_d='Флот без кораблей: катера, несущие взрывчатку и разведку, сковывают противника в акватории. Дёшево и эффективно против больших кораблей.\n\nОткрывает морскую операцию.',
    en='Black Sea: Uncrewed Boats',
    en_d='A fleet without ships: boats carrying explosives and reconnaissance pin the enemy down in the sea. Cheap and effective against large ships.\n\nUnlocks a naval operation.',
    reward='\n'.join([
        'navy_experience = 25',
        timed('UKR_wi_black_sea', 270),
        'UKR_w_mio_sea = yes',
        unlock('UKR_serpents_path_assault'),
    ]),
)

# ---------------------------------------------------------------- Опоры (колонка x=15, общий слот: на экране виден один фокус)
PIL_A = 'prereq=[["UKR_w_martial_law"]]'


def pillar(tag, flag, a, b):
    """a, b - словари для первого и второго фокуса опоры."""
    allow = 'has_country_flag = UKR_pillar_chosen_%s' % flag
    focus(id=a['id'], x=15, y=18, cost=3, icon=a['icon'], allow=allow,
          prereq=[['UKR_w_martial_law']], ru=a['ru'], ru_d=a['ru_d'], en=a['en'], en_d=a['en_d'],
          reward=a['reward'], ai='factor = 30')
    focus(id=b['id'], x=15, y=20, cost=5, icon=b['icon'], allow=allow, tier2=True,
          prereq=[[a['id']]], avail=T2, ru=b['ru'], ru_d=b['ru_d'], en=b['en'], en_d=b['en_d'],
          reward=b['reward'], ai='factor = 30')


pillar('tech', 'technocrats',
       dict(id='UKR_w_p_tech_digital_hq', icon='GFX_goal_generic_scientific_exchange',
            ru='Цифровой штаб',
            ru_d='Единая цифровая платформа для командиров, волонтёров и логистики: заявки, карты, учёт. Технократы строят управление войной как систему данных.\n\nФокус доступен только на пути технократов.',
            en='Digital Headquarters',
            en_d='A single digital platform for commanders, volunteers and logistics: requests, maps, records. The technocrats build the management of the war as a data system.\n\nThis focus is available only on the technocrat path.',
            reward='\n'.join([timed('UKR_wi_p_tech_digital_hq', 365), 'add_command_power = 20', lean('digital', 3)])),
       dict(id='UKR_w_p_tech_drone_command', icon='GFX_goal_generic_secret_weapon',
            ru='Командование беспилотных систем',
            ru_d='Отдельный род войск: дроны, связь, подготовка операторов. Технократы переносят опыт стартапов на фронт.',
            en='Unmanned Systems Command',
            en_d='A separate branch of the forces: drones, communications, operator training. The technocrats carry startup experience to the front.',
            reward='\n'.join([timed('UKR_wi_p_tech_drone_command', 365), 'army_experience = 25', 'UKR_w_mio_drones = yes'])))

pillar('left', 'left',
       dict(id='UKR_w_p_left_labor_front', icon='GFX_goal_generic_consumer_goods',
            ru='Трудовой фронт',
            ru_d='Профсоюзы и трудовые коллективы берут на себя часть работы тыла: оборонные заказы, ремонт, помощь семьям. Президент расширяет охват аудитории: война подаётся как общее дело, а не только забота армии.\n\nФокус доступен только на пути левых.',
            en='Labour Front',
            en_d='Trade unions and work collectives take on part of the work of the rear: defence orders, repairs, help for families. The president widens his audience: the war is presented as a common cause rather than the army\'s concern alone.\n\nThis focus is available only on the left path.',
            reward='\n'.join([timed('UKR_wi_p_left_labor_front', 365), 'add_popularity = { ideology = social_democrat popularity = 0.01 }', lean('left', 3)])),
       dict(id='UKR_w_p_left_people_defense', icon='GFX_goal_generic_national_unity',
            ru='Народная оборона',
            ru_d='Местные отряды самообороны, дружины в посёлках, обучение гражданских базовым навыкам. База мобилизации расширяется за счёт добровольцев на местах.',
            en='People\'s Defence',
            en_d='Local self-defence detachments, village patrols, basic skills training for civilians. The mobilization base widens through volunteers on the ground.',
            reward='\n'.join([timed('UKR_wi_p_left_people_defense', 365), 'add_manpower = 20000', 'add_stability = 0.02'])))

pillar('olig', 'oligarchs',
       dict(id='UKR_w_p_olig_business_cabinet', icon='GFX_goal_generic_trade',
            ru='Бизнес в военном кабинете',
            ru_d='Крупные собственники входят в оперативные советы: логистика, топливо, связь. Дела идут быстрее, но влияние денег на государственные решения растёт.\n\nФокус доступен только на пути олигархов.',
            en='Business in the War Cabinet',
            en_d='Major owners join operational councils: logistics, fuel, communications. Things move faster, but the influence of money on state decisions grows.\n\nThis focus is available only on the oligarch path.',
            reward='\n'.join([timed('UKR_wi_p_olig_business_cabinet', 365), income('1.5'), lean('authoritarian', 2)])),
       dict(id='UKR_w_p_olig_patron_battalions', icon='GFX_goal_generic_construct_mil_factory',
            ru='Шефство над частями',
            ru_d='Холдинги закрепляют за собой отдельные части: снабжение, транспорт, ремонт. Фронт получает больше техники, а владельцы - политический капитал.',
            en='Patronage of Units',
            en_d='Holdings take responsibility for individual units: supply, transport, repair. The front gets more equipment, and the owners gain political capital.',
            reward='\n'.join([timed('UKR_wi_p_olig_patron_battalions', 365),
                              'add_equipment_to_stockpile = { type = infantry_equipment_1 amount = 3000 producer = UKR }',
                              'add_equipment_to_stockpile = { type = support_equipment amount = 300 producer = UKR }'])))

pillar('nat', 'nationalists',
       dict(id='UKR_w_p_nat_nation_council', icon='GFX_goal_generic_propaganda',
            ru='Совет нации',
            ru_d='Идейное руководство мобилизацией: память, язык, ритуалы, образ врага. Националисты задают тон общественному настрою.\n\nФокус доступен только на пути националистов.',
            en='Council of the Nation',
            en_d='Ideological leadership of mobilization: memory, language, ritual, the image of the enemy. The nationalists set the tone of public mood.\n\nThis focus is available only on the nationalist path.',
            reward='\n'.join([timed('UKR_wi_p_nat_nation_council', 365), hate(3), 'add_popularity = { ideology = nationalist popularity = 0.01 }', lean('nationalist', 3)])),
       dict(id='UKR_w_p_nat_volunteer_corps', icon='GFX_goal_generic_army_doctrines',
            ru='Добровольческие корпуса',
            ru_d='Добровольческие формирования получают официальный статус и снабжение. Боевой дух высок, но контроль над ними вызывает споры и тревожит союзников.',
            en='Volunteer Corps',
            en_d='Volunteer formations receive official status and supplies. Fighting spirit is high, but control over them provokes disputes and worries allies.',
            reward='\n'.join([timed('UKR_wi_p_nat_volunteer_corps', 365), 'add_manpower = 25000', 'army_experience = 10', lean('nationalist', 2)])))
