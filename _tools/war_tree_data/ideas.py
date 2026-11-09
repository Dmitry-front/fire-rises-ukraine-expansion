# -*- coding: utf-8 -*-
# Идеи дерева войны (префикс UKR_wi_). Источник правды для common/ideas/UKR_ideas_war_tree.txt и ключей локализации.
# Картинки временные (CLAUDE.md, «Нужен арт»): только готовые generic_* без префикса GFX_idea_.

I = []


def idea(id, pic, mods, ru, ru_d, en, en_d):
    I.append(dict(id=id, pic=pic, mods=mods, ru=ru, ru_d=ru_d, en=en, en_d=en_d))


idea('UKR_wi_martial_law', 'generic_fortify_the_borders',
     {'war_support_factor': 0.1, 'conscription_factor': 0.05, 'stability_factor': -0.03, 'consumer_goods_factor': 0.03},
     'Военное положение',
     'Особый правовой режим военного времени: страна живёт по законам обороны. Люди и ресурсы мобилизуются быстрее, но свободы ограничены, а выборы не проводятся, пока идёт война.',
     'Martial Law',
     'A special wartime legal regime: the country lives by the laws of defence. People and resources are mobilized faster, but freedoms are restricted and no elections are held while the war lasts.')

idea('UKR_wi_stavka', 'generic_stability',
     {'planning_speed': 0.1, 'command_power_gain_mult': 0.1},
     'Ставка',
     'Единый центр военных решений сокращает путь от приказа к исполнению.',
     'The Headquarters',
     'A single centre for military decisions shortens the path from order to execution.')

idea('UKR_wi_unified_command', 'generic_armor',
     {'army_attack_factor': 0.05, 'planning_speed': 0.1, 'dig_in_speed_factor': -0.1},
     'Единое командование',
     'Все силы подчинены одному штабу: наступательные операции согласованы, но местные командиры связаны приказами сверху.',
     'Unified Command',
     'All forces answer to one staff: offensive operations are coordinated, but local commanders are bound by orders from above.')

idea('UKR_wi_operational', 'generic_infantry_bonus',
     {'army_defence_factor': 0.05, 'army_org_factor': 0.05, 'command_power_gain_mult': -0.05, 'experience_gain_army_factor': 0.1},
     'Операционные командования',
     'Направления фронта ведут собственные командующие: гибкость и живучесть растут, общий план становится сложнее.',
     'Operational Commands',
     'Sectors of the front are run by their own commanders: flexibility and resilience grow, the overall plan becomes harder to keep.')

idea('UKR_wi_staff_rhythm', 'generic_stability',
     {'planning_speed': 0.15, 'army_org_factor': 0.03, 'experience_gain_army_factor': 0.05},
     'Штабной ритм',
     'Опыт первых месяцев превратился в чёткие процедуры: планы готовятся быстрее, приказы доходят точнее.',
     'Staff Rhythm',
     'The experience of the first months has become clear procedures: plans are prepared faster and orders arrive more precisely.')

idea('UKR_wi_local_initiative', 'generic_infantry_bonus',
     {'army_org_factor': 0.08, 'army_defence_factor': 0.03, 'experience_gain_army_factor': 0.1},
     'Инициатива на местах',
     'Командиры на направлениях привыкли решать сами: подразделения быстрее учатся и лучше держат позиции.',
     'Local Initiative',
     'Commanders in the sectors have got used to deciding for themselves: units learn faster and hold positions better.')

idea('UKR_wi_military_pay', 'generic_stability',
     {'war_support_factor': 0.05, 'stability_factor': 0.03, 'consumer_goods_factor': 0.03},
     'Достойное содержание армии',
     'Хорошие выплаты бойцам и семьям: люди идут служить охотнее и дольше держатся в строю, но расходы растут каждый месяц.',
     'Decent Army Pay',
     'Good pay for fighters and families: people serve more willingly and stay in the ranks longer, but costs grow every month.')

idea('UKR_wi_patriotic_wave', 'generic_infantry_bonus',
     {'war_support_factor': 0.12, 'conscription_factor': 0.05},
     'Патриотическая волна',
     'Лозунги, история и образ врага подняли добровольцев и дух. Такая волна не бывает вечной и требует новых слов.',
     'Patriotic Wave',
     'Slogans, history and the image of the enemy have raised volunteers and morale. Such a wave is never eternal and needs fresh words.')

idea('UKR_wi_forced_draft', 'generic_infantry_bonus',
     {'conscription_factor': 0.15, 'stability_factor': -0.05, 'war_support_factor': -0.04},
     'Принудительный призыв',
     'Армия получает людей быстро, но каждая облава у военкомата подрывает доверие к власти.',
     'Forced Conscription',
     'The army gets people fast, but every raid at an enlistment office undermines trust in the authorities.')

idea('UKR_wi_unified_info', 'generic_stability',
     {'war_support_factor': 0.08, 'stability_factor': 0.02, 'political_power_gain': -0.05},
     'Единый информационный эфир',
     'Единая картина дня снижает панику и поднимает дух, но свободные голоса слышны всё хуже.',
     'Unified Information Broadcast',
     'A single picture of the day reduces panic and lifts morale, but free voices are heard less and less.')

idea('UKR_wi_open_comms', 'generic_stability',
     {'stability_factor': 0.04, 'political_power_gain': 0.05, 'war_support_factor': 0.02},
     'Открытая коммуникация',
     'Честные брифинги и публичный спор укрепляют доверие общества и союзников, хотя дают материал и противнику.',
     'Open Communication',
     'Honest briefings and public debate strengthen the trust of society and allies, though they also give material to the enemy.')

idea('UKR_wi_relocation', 'generic_production_bonus',
     {'industry_air_damage_factor': -0.2, 'production_speed_buildings_factor': -0.1, 'consumer_goods_factor': 0.02},
     'Эвакуированная промышленность',
     'Заводы переезжают на запад: сначала простой и расходы, потом выпуск там, куда труднее достать.',
     'Relocated Industry',
     'Factories are moving west: first downtime and costs, then output where it is harder to reach.')

idea('UKR_wi_state_order', 'generic_production_bonus',
     {'industrial_capacity_factory': 0.05, 'production_speed_arms_factory_factor': 0.1, 'production_factory_efficiency_gain_factor': 0.05},
     'Государственный оборонный заказ',
     'Прямые заказы государства дают предсказуемые поставки и понятные сроки.',
     'State Defence Order',
     'Direct state orders give predictable deliveries and clear deadlines.')

idea('UKR_wi_private_contracts', 'generic_production_bonus',
     {'production_factory_efficiency_gain_factor': 0.15, 'consumer_goods_factor': 0.02, 'stability_factor': -0.01},
     'Частные оборонные контракты',
     'Гибкие частные производители быстрее осваивают новое, но государству труднее их контролировать.',
     'Private Defence Contracts',
     'Flexible private producers master new things faster, but the state finds them harder to control.')

idea('UKR_wi_sky_shield', 'generic_anti_air',
     {'production_speed_anti_air_building_factor': 0.15, 'static_anti_air_damage_factor': 0.05, 'industry_air_damage_factor': -0.05},
     'Щит неба',
     'Новые комплексы ПВО и мобильные группы прикрывают города и энергетику.',
     'Shield of the Sky',
     'New air defence systems and mobile groups cover cities and the power system.')

idea('UKR_wi_resilient_grid', 'generic_production_bonus',
     {'stability_factor': 0.02, 'industry_air_damage_factor': -0.1, 'consumer_goods_factor': -0.01},
     'Живучая энергосистема',
     'Распределённая генерация и резервные подстанции: удар по одному узлу уже не гасит город.',
     'Resilient Power Grid',
     'Distributed generation and reserve substations: a strike on one hub no longer blacks out a city.')

idea('UKR_wi_world_sympathy', 'generic_stability',
     {'stability_factor': 0.02, 'war_support_factor': 0.04},
     'Симпатии мира',
     'Обращения к миру подняли внимание прессы и общественное сочувствие. Это не вечный капитал и со временем остывает.',
     'Sympathy of the World',
     'Appeals to the world have drawn the attention of the press and public sympathy. It is not permanent capital and cools with time.')

idea('UKR_wi_europe_course', 'generic_stability',
     {'political_power_gain': 0.05, 'production_speed_arms_factory_factor': -0.05},
     'Европейский курс',
     'Тесная связь с европейскими столицами даёт политический вес, но часть решений приходится согласовывать.',
     'European Course',
     'A close bond with the European capitals gives political weight, but some decisions have to be coordinated.')

idea('UKR_wi_self_reliance', 'generic_production_bonus',
     {'production_speed_arms_factory_factor': 0.1, 'industrial_capacity_factory': 0.05, 'consumer_goods_factor': 0.02},
     'Опора на себя',
     'Ставка на отечественное производство: дольше и дороже, но чужие решения не зависят от нас.',
     'Self-Reliance',
     'A bet on domestic production: slower and more expensive, but other people\'s decisions no longer decide our supply.')

idea('UKR_wi_regional', 'generic_fortify_the_borders',
     {'war_support_factor': 0.03, 'supply_consumption_factor': -0.03},
     'Региональные договорённости',
     'Общие склады и быстрый обмен данными с соседями облегчают снабжение.',
     'Regional Agreements',
     'Shared depots and fast data exchange with neighbours ease supply.')

idea('UKR_wi_drone_surge', 'generic_armor',
     {'army_attack_factor': 0.03, 'army_defence_factor': 0.03, 'experience_gain_army_factor': 0.1},
     'Дроновая волна',
     'Массовые беспилотники дают разведку и дешёвый удар на всём фронте.',
     'Drone Surge',
     'Mass-produced drones provide reconnaissance and a cheap strike along the whole front.')

idea('UKR_wi_deep_strike', 'generic_air_bonus',
     {'army_attack_factor': 0.02, 'war_support_factor': 0.04},
     'Удары вглубь',
     'Удары за линией фронта ломают логистику врага и поднимают дух, но тревожат европейские столицы.',
     'Deep Strikes',
     'Strikes behind the front line break the enemy\'s logistics and lift morale, but worry the European capitals.')

idea('UKR_wi_attrition', 'generic_fortify_the_borders',
     {'army_defence_factor': 0.06, 'dig_in_speed_factor': 0.15, 'supply_consumption_factor': -0.05},
     'Оборона на истощение',
     'Минные поля и рубежи в глубину: враг платит за каждый километр.',
     'Defence of Attrition',
     'Minefields and defence in depth: the enemy pays for every kilometre.')

idea('UKR_wi_black_sea', 'generic_air_bonus',
     {'stability_factor': 0.01, 'war_support_factor': 0.02},
     'Чёрное море',
     'Безэкипажные катера сковывают флот противника и открывают морские пути.',
     'The Black Sea',
     'Uncrewed boats pin down the enemy fleet and open the sea lanes.')

idea('UKR_wi_pause', 'generic_stability',
     {'army_org_factor': 0.08, 'land_reinforce_rate': 0.05},
     'Оперативная пауза',
     'Части получили время на пополнение и отдых; организация выше, пополнение быстрее.',
     'Operational Pause',
     'Units have had time to refit and rest; organization is higher and reinforcement is faster.')

idea('UKR_wi_grid_repair', 'generic_production_bonus',
     {'stability_factor': 0.02, 'industry_air_damage_factor': -0.1},
     'Ремонтные бригады энергетиков',
     'Бригады уже на местах: свет возвращается быстрее.',
     'Power Repair Crews',
     'The crews are already in place: the lights come back sooner.')

# ---- духи опор
idea('UKR_wi_p_tech_digital_hq', 'generic_stability',
     {'command_power_gain_mult': 0.1, 'planning_speed': 0.1, 'land_reinforce_rate': 0.05},
     'Цифровой штаб',
     'Заявки, карты и учёт в одной системе: решения принимаются быстрее.',
     'Digital Headquarters',
     'Requests, maps and records in one system: decisions are made faster.')

idea('UKR_wi_p_tech_drone_command', 'generic_armor',
     {'army_attack_factor': 0.04, 'army_defence_factor': 0.04},
     'Командование беспилотных систем',
     'Отдельный род войск с собственной подготовкой операторов и связью.',
     'Unmanned Systems Command',
     'A separate branch of the forces with its own operator training and communications.')

idea('UKR_wi_p_left_labor_front', 'generic_production_bonus',
     {'industrial_capacity_factory': 0.04, 'political_power_gain': 0.05, 'consumer_goods_factor': -0.02},
     'Трудовой фронт',
     'Профсоюзы и трудовые коллективы помогают тылу: заказы, ремонт, помощь семьям.',
     'Labour Front',
     'Trade unions and work collectives help the rear: orders, repairs, help for families.')

idea('UKR_wi_p_left_people_defense', 'generic_infantry_bonus',
     {'conscription_factor': 0.08, 'stability_factor': 0.02},
     'Народная оборона',
     'Местные отряды самообороны расширяют базу мобилизации.',
     'People\'s Defence',
     'Local self-defence detachments widen the mobilization base.')

idea('UKR_wi_p_olig_business_cabinet', 'generic_production_bonus',
     {'production_factory_efficiency_gain_factor': 0.1, 'stability_factor': -0.02},
     'Бизнес в военном кабинете',
     'Собственники в оперативных советах ускоряют решения, но деньги влияют на политику сильнее.',
     'Business in the War Cabinet',
     'Owners in operational councils speed up decisions, but money influences politics more.')

idea('UKR_wi_p_olig_patron_battalions', 'generic_infantry_bonus',
     {'army_org_factor': 0.05, 'army_defence_factor': 0.03},
     'Шефство над частями',
     'Холдинги обеспечивают отдельные части снабжением и ремонтом.',
     'Patronage of Units',
     'Holdings supply and repair individual units.')

idea('UKR_wi_p_nat_nation_council', 'generic_stability',
     {'war_support_factor': 0.08, 'conscription_factor': 0.03},
     'Совет нации',
     'Идейное руководство мобилизацией задаёт тон общественному настрою.',
     'Council of the Nation',
     'Ideological leadership of mobilization sets the tone of public mood.')

idea('UKR_wi_p_nat_volunteer_corps', 'generic_infantry_bonus',
     {'army_attack_factor': 0.04, 'experience_gain_army_factor': 0.1},
     'Добровольческие корпуса',
     'Добровольческие формирования получили статус и снабжение; дух высок, но споров о контроле хватает.',
     'Volunteer Corps',
     'Volunteer formations have received status and supplies; spirit is high, but there is no shortage of disputes over control.')
