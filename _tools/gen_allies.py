#!/usr/bin/env python3
# Генератор запросов к европейским странам (этап 3, PROPOSAL_war_europe.md 4.1, DESIGN.md раздел 12).
# Читает данные _tools/allies_data/*.py и пишет:
#   common/decisions/UKR_decisions_allies.txt          решения UKR_req_* и UKR_pl_exhumations
#   events/UKR_events_foreign.txt                      события ukraine_foreign (запрос у страны, итог у Украины, цепочки Польши)
#   common/scripted_effects/UKR_allies_effects.txt     UKR_update_request_costs, UKR_rq_price_apply
#   common/ideas/UKR_ideas_allies.txt                  временные духи запросов
#   localisation/{russian,english}/UKR_foreign_l_*.yml ключи RU и EN
# Запуск: python3 _tools/gen_allies.py  (без аргументов пишет файлы; --check только проверяет данные).
# После ручных правок сгенерированных файлов генератор не запускать: он перезапишет их целиком.
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from allies_data import pld, ger, fra, eng, bal  # noqa: E402

MODULES = [pld, ger, fra, eng, bal]
REQ = [r for m in MODULES for r in m.REQ]
IDEAS = [i for m in MODULES for i in m.IDEAS]

STD_DELAYS = (7, 14, 28, 45)
FAST_DELAYS = (3, 5, 10, 20)
FORBIDDEN = '\u2014\u2013\u2026'  # длинное и среднее тире, символ многоточия: шрифт игры показывает «?»


def w(path, text, bom=False):
	full = os.path.join(ROOT, path)
	os.makedirs(os.path.dirname(full), exist_ok=True)
	with open(full, 'w', encoding='utf-8', newline='\n') as f:
		if bom:
			f.write('\ufeff')
		f.write(text)


def tabs(lines, n):
	return ''.join(('\t' * n + ln if ln else '') + '\n' for ln in lines)


# ---------------------------------------------------------------- эффекты

def round5(n):
	return max(5, int(round(n / 5.0)) * 5)


def half(fxs):
	"""Частичный пакет из полного: половина объёма, урезанные духи."""
	out = []
	for f in fxs:
		k = f[0]
		if k == 'eq':
			out.append(('eq', f[1], round5(f[2] / 2.0), f[3]))
		elif k == 'money':
			out.append(('money', max(1, f[1] // 2), max(0, f[2] // 2)))
		elif k == 'xp':
			out.append(('xp', f[1], max(1, f[2] // 2)))
		elif k == 'manpower':
			out.append(('manpower', f[1] // 2))
		elif k == 'mio':
			out.append(('mio', f[1], f[2] // 2))
		elif k == 'idea':
			# частичный пакет: урезанный дух (если он есть), иначе без духа
			if f[3]:
				out.append(('idea_part', f[3], f[4], f[1]))
		elif k == 'var':
			if f[2] // 2 > 0:
				out.append(('var', f[1], f[2] // 2))
		else:  # flag, ev, raw
			out.append(f)
	return out


def render_fx(fxs, base_tabs):
	lines = []
	for f in fxs:
		k = f[0]
		if k == 'eq':
			lines += [
				'set_temp_variable = { var = UKR_aid_base value = %d }' % f[2],
				'UKR_nato_aid_scale = yes',
				'add_equipment_to_stockpile = {',
				'\ttype = %s' % f[1],
				'\tamount = UKR_aid_amount',
				'\tproducer = %s' % f[3],
				'}',
			]
		elif k == 'money':
			lines += [
				'set_temp_variable = { var = UKR_aid_base value = %d }' % f[1],
				'UKR_nato_aid_scale = yes',
				'set_temp_variable = { var = income_var_temp value = UKR_aid_amount }',
				'add_income_with_inflation = yes',
			]
			if f[2] > 0:
				lines += [
					'set_temp_variable = { var = debt_var_temp value = %d }' % f[2],
					'add_debt_with_inflation = yes',
				]
		elif k == 'xp':
			lines.append('%s_experience = %d' % (f[1], f[2]))
		elif k == 'manpower':
			lines.append('add_manpower = %d' % f[1])
		elif k == 'mio':
			lines += ['mio:%s = {' % f[1], '\tadd_mio_funds = %d' % f[2], '}']
		elif k == 'idea':
			if f[3]:
				lines += ['if = {', '\tlimit = { has_idea = %s }' % f[3], '\tremove_ideas = %s' % f[3], '}']
			lines += ['add_timed_idea = {', '\tidea = %s' % f[1], '\tdays = %d' % f[2], '}']
		elif k == 'idea_part':
			# урезанный дух, только если полный сейчас не действует
			lines += [
				'if = {',
				'\tlimit = { NOT = { has_idea = %s } }' % f[3],
				'\tadd_timed_idea = {',
				'\t\tidea = %s' % f[1],
				'\t\tdays = %d' % f[2],
				'\t}',
				'}',
			]
		elif k == 'flag':
			lines.append('set_country_flag = %s' % f[1])
		elif k == 'var':
			lines.append('add_to_variable = { var = %s value = %d }' % (f[1], f[2]))
		elif k == 'ev':
			lines.append('country_event = { id = ukraine_foreign.%d days = %d }' % (f[1], f[2]))
		elif k == 'raw':
			lines += f[1].split('\n')
	return tabs(lines, base_tabs)


# ---------------------------------------------------------------- решения

def render_decision(r):
	key = r['key']
	delays = FAST_DELAYS if r.get('fast') else STD_DELAYS
	wait_tt = 'UKR_req_wait_b_tt' if r.get('fast') else 'UKR_req_wait_tt'
	var_ = 'UKR_req_tier'
	branch = []
	for i, d in enumerate(delays, start=1):
		head = 'if' if i == 1 else ('else_if' if i < 4 else 'else')
		cond = '' if i == 4 else '\tlimit = { check_variable = { var = %s value = %d compare = equals } }\n' % (var_, i)
		branch.append('%s = {\n%s\t%s = { country_event = { id = ukraine_foreign.%d days = %d } }\n}' % (head, cond, r['tag'], r['ev'], d))
	branch_txt = '\n'.join(branch)
	branch_txt = ''.join('\t\t\t\t' + ln + '\n' for ln in branch_txt.split('\n'))
	tt = ''
	if r.get('scale'):
		tt = '\t\t\tcustom_effect_tooltip = UKR_nato_aid_scale_tt\n'
	return (
		'\tUKR_req_%(key)s = {\n'
		'\t\ticon = %(icon)s\n'
		'\n'
		'\t\tvisible = {\n'
		'\t\t\thas_war_with = SOV\n'
		'\t\t\tcountry_exists = %(tag)s\n'
		'\t\t}\n'
		'\t\tavailable = {\n'
		'\t\t\tNOT = { has_country_flag = UKR_req_%(key)s_pending }\n'
		'\t\t}\n'
		'\n'
		'\t\tcost = UKR_req_cost_%(key)s\n'
		'\n'
		'\t\tfire_only_once = no\n'
		'\t\tdays_re_enable = %(cd)d\n'
		'\n'
		'\t\tcomplete_effect = {\n'
		'\t\t\tset_country_flag = { flag = UKR_req_%(key)s_pending days = 60 }\n'
		'\t\t\tcustom_effect_tooltip = %(wait)s\n'
		'%(tt)s'
		'\t\t\thidden_effect = {\n'
		'%(branch)s'
		'\t\t\t}\n'
		'\t\t}\n'
		'\n'
		'\t\tai_will_do = {\n'
		'\t\t\tfactor = %(ai)d\n'
		'\t\t}\n'
		'\t}\n'
	) % dict(key=key, icon=r['icon'], tag=r['tag'], cd=r['cd'], wait=wait_tt, tt=tt, branch=branch_txt,
		ai=2 if r['base'] >= 70 else 4)


EXH_DECISION = (
	'\tUKR_pl_exhumations = {\n'
	'\t\ticon = GFX_decision_generic_political_discourse\n'
	'\n'
	'\t\tvisible = {\n'
	'\t\t\thas_war_with = SOV\n'
	'\t\t\tcountry_exists = PLD\n'
	'\t\t\tNOT = { has_country_flag = UKR_pl_exhumations_done }\n'
	'\t\t}\n'
	'\t\tavailable = {\n'
	'\t\t\tNOT = { has_country_flag = UKR_pl_exhumations_done }\n'
	'\t\t}\n'
	'\n'
	'\t\tcost = 40\n'
	'\t\tfire_only_once = yes\n'
	'\n'
	'\t\tcomplete_effect = {\n'
	'\t\t\tset_country_flag = UKR_pl_exhumations_done\n'
	'\t\t\tPLD = {\n'
	'\t\t\t\tadd_opinion_modifier = { target = UKR modifier = ukr_allies_exhumations }\n'
	'\t\t\t}\n'
	'\t\t\tUKR_trust_warsaw_dialogue = yes\n'
	'\t\t\tadd_stability = -0.01\n'
	'\t\t\tadd_popularity = {\n'
	'\t\t\t\tideology = nationalist\n'
	'\t\t\t\tpopularity = -0.01\n'
	'\t\t\t}\n'
	'\t\t\tcountry_event = { id = ukraine_foreign.321 days = 3 }\n'
	'\t\t}\n'
	'\n'
	'\t\tai_will_do = {\n'
	'\t\t\tfactor = 2\n'
	'\t\t}\n'
	'\t}\n'
)


def gen_decisions():
	head = (
		'# Запросы к европейским странам (этап 3, PROPOSAL_war_europe.md 4.1, DESIGN.md раздел 12).\n'
		'# Файл создан генератором _tools/gen_allies.py (данные - _tools/allies_data/*.py); после ручных правок генератор не запускать.\n'
		'# Цена в политсиле - переменная UKR_req_cost_<запрос> (база x доверие, UKR_update_request_costs); ответ страны приходит событием\n'
		'# ukraine_foreign.3xx/4xx через 7/14/28/45 дней (Прибалтика 3/5/10/20) и зависит от отношения страны к Украине, доверия и прошлого.\n'
		'# Блокировка до ответа - флаг UKR_req_<запрос>_pending (до 60 дней); потом действует перезарядка days_re_enable.\n'
		'UKR_allies_category = {\n'
	)
	body = '\n'.join(render_decision(r) for r in REQ)
	return head + body + '\n' + EXH_DECISION + '}\n'


# ---------------------------------------------------------------- события

# Веса опций ai_chance страны (PROPOSAL_war_europe.md 4.1): (база, {полоса: вес})
OPT = {
	'full': (25, {'opinion_high': 25, 'opinion_mid': 10, 'opinion_low': -20,
		'trust_top': 25, 'trust_high': 15, 'trust_mid': 0, 'trust_low': -10, 'trust_none': -20, 'phase': 10}),
	'part': (35, {'opinion_high': -10, 'opinion_mid': 5, 'opinion_low': 0,
		'trust_top': -15, 'trust_high': -5, 'trust_mid': 10, 'trust_low': 10, 'trust_none': 5, 'phase': 0}),
	'no': (15, {'opinion_high': -10, 'opinion_mid': 0, 'opinion_low': 25,
		'trust_top': -10, 'trust_high': -5, 'trust_mid': 0, 'trust_low': 10, 'trust_none': 25, 'phase': -5}),
}
BAND_TRIGGER = {
	'opinion_high': 'UKR_ally_opinion_high = yes', 'opinion_mid': 'UKR_ally_opinion_mid = yes',
	'opinion_low': 'UKR_ally_opinion_low = yes',
	'trust_top': 'UKR_ally_trust_top = yes', 'trust_high': 'UKR_ally_trust_high = yes',
	'trust_mid': 'UKR_ally_trust_mid = yes', 'trust_low': 'UKR_ally_trust_low = yes',
	'trust_none': 'UKR_ally_trust_none = yes',
	'phase': 'has_global_flag = SOV_nato_war_begins_global',
}


def ai_chance(kind, wmods):
	base, bands = OPT[kind]
	lines = ['ai_chance = {', '\tbase = %d' % base]
	for band, val in bands.items():
		if val == 0:
			continue
		lines.append('\tmodifier = { add = %d %s }' % (val, BAND_TRIGGER[band]))
	# прошлое: идеи и флаги Украины. Положительный вес - за полный, отрицательный - в отказ (и наоборот)
	for trig, d in wmods:
		if kind == 'full':
			lines.append('\tmodifier = { add = %d %s }' % (d, trig))
		elif kind == 'no':
			lines.append('\tmodifier = { add = %d %s }' % (-d, trig))
	lines.append('}')
	return lines


def render_request_event(r):
	key, ev, res, tag = r['key'], r['ev'], r['res'], r['tag']
	full = r['full']
	part = half(full) if r['part'] == 'auto' else r['part']
	out = []
	out.append('country_event = {')
	out.append('\tid = ukraine_foreign.%d' % ev)
	out.append('\ttitle = ukraine_foreign.%d.t' % ev)
	out.append('\tdesc = ukraine_foreign.%d.d' % ev)
	out.append('\tpicture = %s' % r['pic'])
	out.append('')
	out.append('\tis_triggered_only = yes')
	out.append('')
	for kind, letter, name_key, fx in (('full', 'a', 'UKR_req_opt_full', full), ('part', 'b', 'UKR_req_opt_part', part), ('no', 'c', 'UKR_req_opt_no', None)):
		out.append('\toption = {')
		out.append('\t\tname = %s' % name_key)
		out += ['\t\t' + ln for ln in ai_chance(kind, r['weights'])]
		if kind == 'full':
			out.append('\t\tadd_opinion_modifier = { target = UKR modifier = ukr_allies_request_met }')
		elif kind == 'part':
			out.append('\t\tadd_opinion_modifier = { target = UKR modifier = ukr_allies_request_partial }')
		out.append('\t\tUKR = {')
		out.append('\t\t\tclr_country_flag = UKR_req_%s_pending' % key)
		out.append('\t\t\tset_country_flag = { flag = UKR_req_%s_%s days = 10 }' % (key, kind))
		if fx:
			out.append(render_fx(fx, 3).rstrip('\n'))
		out.append('\t\t\tcountry_event = { id = ukraine_foreign.%d days = 1 }' % res)
		out.append('\t\t}')
		out.append('\t}')
		out.append('')
	out.pop()
	out.append('}')
	return '\n'.join(out) + '\n'


def render_result_event(r):
	key, res = r['key'], r['res']
	out = []
	out.append('country_event = {')
	out.append('\tid = ukraine_foreign.%d' % res)
	out.append('\ttitle = ukraine_foreign.%d.t' % res)
	for kind in ('full', 'part', 'no'):
		out.append('\tdesc = {')
		out.append('\t\ttext = ukraine_foreign.%d.d_%s' % (res, kind))
		out.append('\t\ttrigger = { has_country_flag = UKR_req_%s_%s }' % (key, kind))
		out.append('\t}')
	out.append('\tpicture = %s' % r['pic'])
	out.append('')
	out.append('\tis_triggered_only = yes')
	out.append('')
	for kind, wrap in (('full', 'UKR_trust_request_full = yes'), ('part', 'UKR_trust_request_part = yes'), ('no', None)):
		out.append('\toption = {')
		out.append('\t\tname = UKR_req_res_%s' % kind)
		out.append('\t\ttrigger = { has_country_flag = UKR_req_%s_%s }' % (key, kind))
		if wrap:
			out.append('\t\t' + wrap)
		out.append('\t\tclr_country_flag = UKR_req_%s_%s' % (key, kind))
		out.append('\t\tai_chance = { base = 100 }')
		out.append('\t}')
		out.append('')
	out.pop()
	out.append('}')
	return '\n'.join(out) + '\n'


GRAIN_EVENT = '''country_event = {
	id = ukraine_foreign.320
	title = ukraine_foreign.320.t
	desc = ukraine_foreign.320.d
	picture = GFX_UKR_agricultural_success

	is_triggered_only = yes
	fire_only_once = yes

	trigger = {
		has_war_with = SOV
		country_exists = PLD
	}

	# Согласиться на запрет, пустить зерно через «коридоры солидарности»
	option = {
		name = ukraine_foreign.320.a
		PLD = {
			add_opinion_modifier = { target = UKR modifier = ukr_allies_grain_solidarity }
		}
		UKR_trust_warsaw_dialogue = yes
		set_temp_variable = { var = income_var_temp value = -0.8 }
		add_income_with_inflation = yes
		ai_chance = { base = 40 }
	}

	# Жаловаться в ВТО и давить через Брюссель
	option = {
		name = ukraine_foreign.320.b
		PLD = {
			add_opinion_modifier = { target = UKR modifier = ukr_allies_grain_dispute }
		}
		UKR_trust_warsaw_dispute = yes
		add_political_power = 15
		ai_chance = { base = 20 }
	}

	# Тихие переговоры: лицензии на вывоз и квоты
	option = {
		name = ukraine_foreign.320.c
		PLD = {
			add_opinion_modifier = { target = UKR modifier = ukr_allies_request_partial }
		}
		set_temp_variable = { var = income_var_temp value = -0.4 }
		add_income_with_inflation = yes
		ai_chance = { base = 40 }
	}
}
'''

EXH_EVENT = '''country_event = {
	id = ukraine_foreign.321
	title = ukraine_foreign.321.t
	desc = ukraine_foreign.321.d
	picture = GFX_UKR_diplomat

	is_triggered_only = yes

	option = {
		name = ukraine_foreign.321.a
		ai_chance = { base = 100 }
	}
}
'''


AID_EVENT = '''country_event = {
	id = ukraine_foreign.480
	title = ukraine_foreign.480.t
	desc = ukraine_foreign.480.d
	picture = GFX_event_UKR_war_support_NATO

	is_triggered_only = yes

	# Прибытие пакета западной помощи (решение UKR_western_aid_package, задержка 3/5/7/10 дней по доверию)
	immediate = {
		set_temp_variable = { var = UKR_aid_base value = 400 }
		UKR_nato_aid_scale = yes
		add_equipment_to_stockpile = {
			type = infantry_equipment_1
			amount = UKR_aid_amount
			producer = PLD
		}
		set_temp_variable = { var = UKR_aid_base value = 80 }
		UKR_nato_aid_scale = yes
		add_equipment_to_stockpile = {
			type = support_equipment
			amount = UKR_aid_amount
			producer = GER
		}
		set_temp_variable = { var = UKR_aid_base value = 60 }
		UKR_nato_aid_scale = yes
		add_equipment_to_stockpile = {
			type = anti_tank_equipment_1
			amount = UKR_aid_amount
			producer = ENG
		}
	}

	option = {
		name = ukraine_foreign.480.a
		ai_chance = { base = 100 }
	}
}
'''

LL_EVENT = '''country_event = {
	id = ukraine_foreign.481
	title = ukraine_foreign.481.t
	desc = ukraine_foreign.481.d
	picture = GFX_Generic_Tank_column

	is_triggered_only = yes

	# Прибытие ленд-лиза (решение UKR_lend_lease_program, задержка 7/10/14/21 день по доверию; раньше 30 дней)
	immediate = {
		set_country_flag = UKR_lend_lease_approved
		add_timed_idea = {
			idea = UKR_idea_lend_lease
			days = 150
		}
		set_temp_variable = { var = UKR_aid_base value = 1500 }
		UKR_nato_aid_scale = yes
		add_equipment_to_stockpile = {
			type = infantry_equipment_1
			amount = UKR_aid_amount
			producer = FRA
		}
		set_temp_variable = { var = UKR_aid_base value = 400 }
		UKR_nato_aid_scale = yes
		add_equipment_to_stockpile = {
			type = support_equipment
			amount = UKR_aid_amount
			producer = GER
		}
		set_temp_variable = { var = UKR_aid_base value = 150 }
		UKR_nato_aid_scale = yes
		add_equipment_to_stockpile = {
			type = anti_tank_equipment_1
			amount = UKR_aid_amount
			producer = ENG
		}
		set_temp_variable = { var = UKR_aid_base value = 120 }
		UKR_nato_aid_scale = yes
		add_equipment_to_stockpile = {
			type = motorized_equipment
			amount = UKR_aid_amount
			producer = PLD
		}
		set_temp_variable = { var = UKR_aid_base value = 500 }
		UKR_nato_aid_scale = yes
		add_equipment_to_stockpile = {
			type = infantry_equipment_1
			amount = UKR_aid_amount
			producer = ITA
		}
	}

	option = {
		name = ukraine_foreign.481.a
		ai_chance = { base = 100 }
	}
}
'''


def gen_events():
	head = (
		'add_namespace = ukraine_foreign\n'
		'\n'
		'# События запросов к европейским странам (этап 3, PROPOSAL_war_europe.md 4.1, DESIGN.md раздел 12).\n'
		'# Файл создан генератором _tools/gen_allies.py (данные - _tools/allies_data/*.py); после ручных правок генератор не запускать.\n'
		'# Запрос (область страны-ответчика): три опции - полный пакет, частичный, отказ; выбирает ИИ по ai_chance (отношение страны к Украине,\n'
		'# доверие европейского НАТО, прошлое Украины), человек выбирает сам. Опция выдаёт эффекты Украине (в области UKR) и шлёт итог.\n'
		'# Итог (область Украины): один текст на исход по флагу UKR_req_<запрос>_full/_part/_no и одна подходящая кнопка.\n'
		'# Картинки временные (существующие спрайты); учёт арта - ART_MAP.md. Строка "# art:" над событием читает _tools/art_map.py:\n'
		'# "# art: reuse" - картинка временная, событие попадает в ART_MAP.md; "# art: -" - картинка не нужна (событие страны-ответчика).\n'
		'\n'
	)
	parts = []
	for r in REQ:
		parts.append('# %s -> %s\n# art: -\n' % (r['tag'], r['key']) + render_request_event(r))
		parts.append('# art: reuse\n' + render_result_event(r))
	parts.append('# Цепочка Польши: зерно на границе (через 150 дней после согласия на транзитный хаб)\n# art: reuse\n' + GRAIN_EVENT)
	parts.append('# Цепочка Польши: итог решения UKR_pl_exhumations\n# art: reuse\n' + EXH_EVENT)
	parts.append('# Прибытие пакета западной помощи (старое решение UKR_western_aid_package)\n# art: reuse\n' + AID_EVENT)
	parts.append('# Прибытие ленд-лиза (старое решение UKR_lend_lease_program)\n# art: reuse\n' + LL_EVENT)
	return head + '\n'.join(parts)


# ---------------------------------------------------------------- цены

def gen_effects():
	lines = [
		'# Европейское НАТО, этап 3 (PROPOSAL_war_europe.md 4.1): ступень доверия, цены и сроки запросов к странам.',
		'# Файл создан генератором _tools/gen_allies.py. Область - Украина. Вызывается из UKR_trust_apply (при каждом изменении доверия),',
		'# из on_daily (TFR_on_actions_UKR.txt) и из фокуса UKR_secure_western_aid.',
		'',
		'# Вход: временная UKR_rq_base (базовая цена), выход: временная UKR_rq_price (база x UKR_req_pct / 100, округлено).',
		'UKR_rq_price_apply = {',
		'\tset_temp_variable = { var = UKR_rq_price value = UKR_rq_base }',
		'\tmultiply_temp_variable = { var = UKR_rq_price value = UKR_req_pct }',
		'\tdivide_temp_variable = { var = UKR_rq_price value = 100 }',
		'\tround_temp_variable = UKR_rq_price',
		'}',
		'',
		'# Ступень доверия: 1 - от 65, 2 - 45-64, 3 - 25-44, 4 - ниже 25. Цена: 100/115/130/150 процентов; ответ: 7/14/28/45 дней',
		'# (Прибалтика 3/5/10/20; старые решения помощи: пакет 3/5/7/10, ленд-лиз 7/10/14/21). Затем цены всех запросов UKR_req_cost_<запрос> и двух старых решений.',
		'UKR_update_request_costs = {',
		'\tset_variable = { var = UKR_req_tier value = 4 }',
		'\tset_variable = { var = UKR_req_pct value = 150 }',
		'\tset_variable = { var = UKR_req_delay value = 45 }',
		'\tset_variable = { var = UKR_req_delay_b value = 20 }',
		'\tset_variable = { var = UKR_aid_delay value = 10 }',
		'\tset_variable = { var = UKR_ll_delay value = 21 }',
	]
	for lo, tier, pct, d, db, ad, ld in ((25, 3, 130, 28, 10, 7, 14), (45, 2, 115, 14, 5, 5, 10), (65, 1, 100, 7, 3, 3, 7)):
		lines += [
			'\tif = {',
			'\t\tlimit = { check_variable = { var = UKR_nato_trust value = %d compare = greater_than_or_equals } }' % lo,
			'\t\tset_variable = { var = UKR_req_tier value = %d }' % tier,
			'\t\tset_variable = { var = UKR_req_pct value = %d }' % pct,
			'\t\tset_variable = { var = UKR_req_delay value = %d }' % d,
			'\t\tset_variable = { var = UKR_req_delay_b value = %d }' % db,
			'\t\tset_variable = { var = UKR_aid_delay value = %d }' % ad,
			'\t\tset_variable = { var = UKR_ll_delay value = %d }' % ld,
			'\t}',
		]
	lines.append('')
	for r in REQ:
		lines += [
			'\tset_temp_variable = { var = UKR_rq_base value = %d }' % r['base'],
			'\tUKR_rq_price_apply = yes',
			'\tset_variable = { var = UKR_req_cost_%s value = UKR_rq_price }' % r['key'],
		]
	lines += [
		'',
		'\t# Старые решения помощи: база растёт у пакета западной помощи (+10 за нажатие), у ленд-лиза постоянна',
		'\tset_temp_variable = { var = UKR_rq_base value = UKR_western_aid_cost }',
		'\tUKR_rq_price_apply = yes',
		'\tset_variable = { var = UKR_western_aid_price value = UKR_rq_price }',
		'\tset_temp_variable = { var = UKR_rq_base value = 100 }',
		'\tUKR_rq_price_apply = yes',
		'\tset_variable = { var = UKR_lend_lease_price value = UKR_rq_price }',
		'}',
	]
	return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------- духи

def gen_ideas():
	lines = [
		'# Временные духи запросов к европейским странам (этап 3, PROPOSAL_war_europe.md 4.1). Полная версия при полном ответе страны,',
		'# урезанная (_lim) при частичном. Иконки временные (CLAUDE.md, «Нужен арт»). Файл создан генератором _tools/gen_allies.py.',
		'ideas = {',
		'\tcountry = {',
	]
	for i in IDEAS:
		lines += [
			'\t\t%s = {' % i['name'],
			'\t\t\tpicture = %s' % i['picture'],
			'\t\t\tallowed = {',
			'\t\t\t\toriginal_tag = UKR',
			'\t\t\t}',
			'\t\t\tremoval_cost = -1',
			'\t\t\tmodifier = {',
		]
		for k, v in i['mods'].items():
			lines.append('\t\t\t\t%s = %s' % (k, repr(v)))
		lines += ['\t\t\t}', '\t\t}', '']
	lines.pop()
	lines += ['\t}', '}']
	return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------- локализация

def esc(s):
	return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')


SHARED = {
	'UKR_req_opt_full': ('Согласиться полностью.', 'Agree in full.'),
	'UKR_req_opt_part': ('Согласиться частично.', 'Agree in part.'),
	'UKR_req_opt_no': ('Отказать.', 'Refuse.'),
	'UKR_req_res_full': ('Благодарим. Помощь будет использована с отчётом.', 'We thank you. The aid will be used with full accounting.'),
	'UKR_req_res_part': ('Это лучше, чем ничего. Благодарим.', 'It is better than nothing. We thank you.'),
	'UKR_req_res_no': ('Понимаем. Вернёмся к вопросу позже.', 'We understand. We will return to the question later.'),
	'UKR_req_wait_tt': ('Ответ придёт примерно через §Y[?UKR_req_delay|0]§! дн.; цена и срок зависят от доверия (сейчас §Y[?UKR_req_pct|0]%§! от базовой цены).',
		'The answer will come in about §Y[?UKR_req_delay|0]§! days; price and delay depend on trust (now §Y[?UKR_req_pct|0]%§! of the base price).'),
	'UKR_req_wait_b_tt': ('Ответ придёт примерно через §Y[?UKR_req_delay_b|0]§! дн. (Прибалтика отвечает быстро); цена зависит от доверия (сейчас §Y[?UKR_req_pct|0]%§! от базовой цены).',
		'The answer will come in about §Y[?UKR_req_delay_b|0]§! days (the Baltic states answer quickly); the price depends on trust (now §Y[?UKR_req_pct|0]%§! of the base price).'),
	'UKR_trust_reason_20': ('§G+2§! просьба к европейской стране выполнена', '§G+2§! a request to a European country was met'),
	'UKR_trust_reason_21': ('§G+1§! просьба выполнена частично', '§G+1§! a request was partly met'),
	'UKR_trust_tt_request_full': ('Доверие европейского НАТО: §G+2§!', 'European NATO trust: §G+2§!'),
	'UKR_trust_tt_request_part': ('Доверие европейского НАТО: §G+1§!', 'European NATO trust: §G+1§!'),
	'UKR_aid_package_tt': ('Состав пакета: стрелковое оружие и боеприпасы (Польша), снаряжение поддержки (Германия), противотанковые комплексы (Британия).',
		'Contents of the package: small arms and ammunition (Poland), support equipment (Germany), anti-tank systems (Britain).'),
	'UKR_lend_lease_tt': ('Состав поставки: стрелковое оружие (Франция, Италия), снаряжение поддержки (Германия), противотанковые комплексы (Британия), грузовики и транспортёры (Польша); на 150 дней действует дух ленд-лиза.',
		'Contents of the shipment: small arms (France, Italy), support equipment (Germany), anti-tank systems (Britain), trucks and carriers (Poland); the lend-lease spirit lasts 150 days.'),
	'UKR_aid_delay_tt': ('Пакет придёт примерно через §Y[?UKR_aid_delay|0]§! дн.; чем ниже доверие, тем дольше.',
		'The package will arrive in about §Y[?UKR_aid_delay|0]§! days; the lower the trust, the longer.'),
	'UKR_aid_delay_ll_tt': ('Поставка придёт примерно через §Y[?UKR_ll_delay|0]§! дн.; чем ниже доверие, тем дольше.',
		'The shipment will arrive in about §Y[?UKR_ll_delay|0]§! days; the lower the trust, the longer.'),
	'ukr_allies_request_met': ('Просьба Украины выполнена', 'Ukraine\'s request met'),
	'ukr_allies_request_partial': ('Просьба Украины выполнена частично', 'Ukraine\'s request partly met'),
	'ukr_allies_grain_dispute': ('Спор о зерне: жалобы и давление', 'The grain dispute: complaints and pressure'),
	'ukr_allies_grain_solidarity': ('Согласие на ограничения для зерна', 'Agreement to the grain restrictions'),
	'ukr_allies_exhumations': ('Разрешены эксгумации на Волыни', 'Exhumations in Volhynia allowed'),
}


def gen_loc(lang):
	i = 0 if lang == 'ru' else 1
	header = 'l_russian:' if lang == 'ru' else 'l_english:'
	lines = [header]

	def put(k, v):
		lines.append(' %s:0 "%s"' % (k, esc(v)))

	for k, (ru, en) in SHARED.items():
		# ключи причин и подсказок доверия живут в UKR_allies_l_*.yml (рядом с остальными причинами), здесь только новые общие
		if k.startswith('UKR_trust_'):
			continue
		put(k, ru if i == 0 else en)
	lines.append('')
	for r in REQ:
		put('UKR_req_%s' % r['key'], r['name'][lang])
		put('UKR_req_%s_desc' % r['key'], r['desc'][lang])
		put('ukraine_foreign.%d.t' % r['ev'], r['req_t'][lang])
		put('ukraine_foreign.%d.d' % r['ev'], r['req_d'][lang])
		put('ukraine_foreign.%d.t' % r['res'], r['res_t'][lang])
		put('ukraine_foreign.%d.d_full' % r['res'], r['res_full'][lang])
		put('ukraine_foreign.%d.d_part' % r['res'], r['res_part'][lang])
		put('ukraine_foreign.%d.d_no' % r['res'], r['res_no'][lang])
		lines.append('')
	c = pld.CHAIN
	put('ukraine_foreign.320.t', c['grain']['t'][lang])
	put('ukraine_foreign.320.d', c['grain']['d'][lang])
	put('ukraine_foreign.320.a', c['grain']['a'][lang])
	put('ukraine_foreign.320.b', c['grain']['b'][lang])
	put('ukraine_foreign.320.c', c['grain']['c'][lang])
	put('UKR_pl_exhumations', c['exh']['name'][lang])
	put('UKR_pl_exhumations_desc', c['exh']['desc'][lang])
	put('ukraine_foreign.321.t', c['exh']['res_t'][lang])
	put('ukraine_foreign.321.d', c['exh']['res_d'][lang])
	put('ukraine_foreign.321.a', c['exh']['res_a'][lang])
	put('ukraine_foreign.480.t', 'Пакет западной помощи прибыл' if lang == 'ru' else 'The Western aid package has arrived')
	put('ukraine_foreign.480.d', ('Очередная партия помощи пересекла границу: польская стрелковая техника и боеприпасы, немецкое снаряжение поддержки и британские противотанковые комплексы. Каждый такой пакет невелик, но между крупными поставками он держит армию на ходу. Размер партии зависит от единства НАТО.'
		if lang == 'ru' else 'Another batch of aid has crossed the border: Polish small arms and ammunition, German support equipment and British anti-tank systems. Each such package is small, but between the large deliveries it keeps the army going. The size of the batch depends on the unity of NATO.'))
	put('ukraine_foreign.480.a', 'Принять и распределить по бригадам.' if lang == 'ru' else 'Accept and distribute among the brigades.')
	put('ukraine_foreign.481.t', 'Ленд-лиз: первая поставка' if lang == 'ru' else 'Lend-lease: the first shipment')
	put('ukraine_foreign.481.d', ('Программа ленд-лиза заработала: из Франции и Италии пришли стрелковые комплексы, из Германии снаряжение поддержки, из Британии противотанковые комплексы, из Польши грузовики и транспортёры. Поставки рассчитаны на месяцы, поэтому действует и временный дух ленд-лиза.\n\n§YВ реальности.§! Закон о ленд-лизе для Украины США приняли в 2022 году: он упростил передачу техники без немедленной оплаты и ускорил поставки.'
		if lang == 'ru' else 'The lend-lease programme is under way: small arms arrived from France and Italy, support equipment from Germany, anti-tank systems from Britain, trucks and carriers from Poland. The deliveries are planned for months, so the temporary lend-lease spirit applies as well.\n\n§YIn reality.§! The United States adopted the lend-lease act for Ukraine in 2022: it simplified the transfer of equipment without immediate payment and sped up deliveries.'))
	put('ukraine_foreign.481.a', 'Принять поставку.' if lang == 'ru' else 'Accept the shipment.')
	lines.append('')
	for idea in IDEAS:
		put(idea['name'], idea['%s_name' % lang])
		put(idea['name'] + '_desc', idea['%s_desc' % lang])
	return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------- проверка

def check():
	problems = []
	ev_ids = set()
	keys = set()
	for r in REQ:
		for fld in ('ev', 'res'):
			if r[fld] in ev_ids:
				problems.append('дубль события %s' % r[fld])
			ev_ids.add(r[fld])
		if r['key'] in keys:
			problems.append('дубль запроса %s' % r['key'])
		keys.add(r['key'])
		for name in ('name', 'desc', 'req_t', 'req_d', 'res_t', 'res_full', 'res_part', 'res_no'):
			for lang in ('ru', 'en'):
				s = r[name][lang]
				if any(ch in s for ch in FORBIDDEN):
					problems.append('%s %s %s: запрещённый символ (тире или многоточие)' % (r['key'], name, lang))
				if not s.strip():
					problems.append('%s %s %s пусто' % (r['key'], name, lang))
		if 'part' not in r or 'full' not in r:
			problems.append('%s: нет full/part' % r['key'])
	for ev in (320, 321):
		if ev in ev_ids:
			problems.append('событие %d занято запросом' % ev)
	idea_names = {i['name'] for i in IDEAS}
	for r in REQ:
		for f in r['full']:
			if f[0] == 'idea':
				for n in (f[1], f[3]):
					if n and n not in idea_names:
						problems.append('%s: нет духа %s' % (r['key'], n))
	return problems


def main():
	problems = check()
	if problems:
		print('\n'.join(problems))
		return 1
	if '--check' in sys.argv:
		print('данные в порядке: %d запросов, %d духов' % (len(REQ), len(IDEAS)))
		return 0
	w('common/decisions/UKR_decisions_allies.txt', gen_decisions())
	w('events/UKR_events_foreign.txt', gen_events())
	w('common/scripted_effects/UKR_allies_effects.txt', gen_effects())
	w('common/ideas/UKR_ideas_allies.txt', gen_ideas())
	w('localisation/russian/UKR_foreign_l_russian.yml', gen_loc('ru'), bom=True)
	w('localisation/english/UKR_foreign_l_english.yml', gen_loc('en'), bom=True)
	# хвост общих ключей доверия (причины 20-21 и подсказки) добавляется в UKR_allies_l_*.yml вручную (см. DESIGN.md, раздел 12)
	print('записано: %d запросов, %d духов' % (len(REQ), len(IDEAS)))
	return 0


if __name__ == '__main__':
	sys.exit(main())
