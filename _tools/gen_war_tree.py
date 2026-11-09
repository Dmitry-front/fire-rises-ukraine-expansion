#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Генератор дерева войны Украины (DESIGN.md 8.5, сессия 24).

Источник правды - _tools/war_tree_data/*.py. Скрипт собирает:
  common/national_focus/UKR_war_shared_focus.txt   (shared_focus, одно определение на все шесть деревьев)
  common/ideas/UKR_ideas_war_tree.txt
  common/decisions/UKR_decisions_war_tree.txt
  events/UKR_events_war_tree.txt
  localisation/{russian,english}/UKR_war_tree_l_*.yml
и подключает фокусы строками `shared_focus = ...` к шести деревьям (идемпотентно, между маркерами).

Запуск: python3 _tools/gen_war_tree.py            (только проверка, ничего не пишет)
        python3 _tools/gen_war_tree.py --write    (проверка и запись)
Руками правят данные в _tools/war_tree_data/, а не сгенерированные файлы.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_tools', 'war_tree_data'))
sys.dont_write_bytecode = True

import focuses as FO  # noqa: E402
import ideas as ID  # noqa: E402
import decisions as DE  # noqa: E402

WRITE = '--write' in sys.argv
errors = []

TREES = [
    'common/national_focus/TFR_national_focus_UKR.txt',
    'common/national_focus/UKR_block2_focus.txt',
    'common/national_focus/UKR_block3_technocrats_focus.txt',
    'common/national_focus/UKR_block3_left_focus.txt',
    'common/national_focus/UKR_block3_oligarchs_focus.txt',
    'common/national_focus/UKR_block3_nationalists_focus.txt',
]
MARK_BEGIN = '\t# Общее дерево войны: те же фокусы во всех шести деревьях (_tools/gen_war_tree.py, DESIGN.md 8.5). Не править руками.'
MARK_END = '\t# Конец общего дерева войны'


def ind(text, n):
    pad = '\t' * n
    return '\n'.join((pad + l) if l.strip() else l for l in text.split('\n'))


def num(v):
    return ('%g' % v)


# ---------------------------------------------------------------- проверки
def check():
    ids = [f['id'] for f in FO.F]
    if len(ids) != len(set(ids)):
        errors.append('дубли ID фокусов')
    idset = set(ids)
    idea_ids = {i['id'] for i in ID.I}
    dec_new = {d['id'] for d in DE.D}
    existing_decisions = set()
    for p in ('common/decisions/TFR_decisions_UKR.txt', 'common/decisions/TFR_decisions_UKR_war.txt'):
        t = open(os.path.join(ROOT, p), encoding='utf-8-sig').read()
        existing_decisions |= set(re.findall(r'\n\t(UKR_\w+) = \{', t))
    used_ideas = set()
    for f in FO.F:
        for grp in f['prereq']:
            for p in grp:
                if p not in idset:
                    errors.append('%s: нет prerequisite %s' % (f['id'], p))
        for e in f['excl']:
            if e not in idset:
                errors.append('%s: нет mutually_exclusive %s' % (f['id'], e))
            else:
                other = next(x for x in FO.F if x['id'] == e)
                if f['id'] not in other['excl']:
                    errors.append('исключение несимметрично: %s <-> %s' % (f['id'], e))
        for k in ('ru', 'ru_d', 'en', 'en_d'):
            if not f.get(k):
                errors.append('%s: нет текста %s' % (f['id'], k))
        for m in re.finditer(r'(?:add_ideas = |idea = )(UKR_wi_\w+)', f['reward']):
            used_ideas.add(m.group(1))
            if m.group(1) not in idea_ids:
                errors.append('%s: нет идеи %s' % (f['id'], m.group(1)))
        for m in re.finditer(r'unlock_decision_tooltip = (\w+)', f['reward']):
            if m.group(1) not in existing_decisions | dec_new:
                errors.append('%s: нет решения %s' % (f['id'], m.group(1)))
        for m in re.finditer(r'has_completed_focus = (UKR_w_\w+)', f['reward']):
            if m.group(1) not in idset:
                errors.append('%s: нет фокуса %s' % (f['id'], m.group(1)))
    for d in DE.D:
        for m in re.finditer(r'(?:add_ideas = |idea = )(UKR_wi_\w+)', d['complete']):
            used_ideas.add(m.group(1))
            if m.group(1) not in idea_ids:
                errors.append('%s: нет идеи %s' % (d['id'], m.group(1)))
        for m in re.finditer(r'has_completed_focus = (UKR_w_\w+)', d['visible'] + '\n' + d['complete']):
            if m.group(1) not in idset:
                errors.append('%s: нет фокуса %s' % (d['id'], m.group(1)))
    unused = idea_ids - used_ideas
    if unused:
        errors.append('идеи без ссылок: %s' % sorted(unused))
    # координаты: фокусы с одним allow (общим для всех) не должны совпадать; слоты опор делят клетки намеренно
    seen = {}
    for f in FO.F:
        key = (f['x'], f['y'])
        pillar = f['allow'].startswith('has_country_flag = UKR_pillar_chosen_')
        group = ('pillar', f['allow']) if pillar else ('common',)
        for other_group, other_id in seen.get(key, []):
            if other_group == group or (group == ('common',)) or (other_group == ('common',)):
                errors.append('наложение клеток %s и %s на %s' % (f['id'], other_id, key))
        seen.setdefault(key, []).append((group, f['id']))
    for i in ID.I:
        for k in ('ru', 'ru_d', 'en', 'en_d'):
            if not i.get(k):
                errors.append('%s: нет текста %s' % (i['id'], k))
    # символы, которые шрифт игры показывает как «?»
    bad = re.compile('[—–…]')
    for name, text in all_loc('ru') + all_loc('en'):
        if bad.search(text):
            errors.append('запрещённый символ в %s' % name)
        if '"' in text:
            errors.append('двойная кавычка в %s' % name)


# ---------------------------------------------------------------- локализация
def all_loc(lang):
    out = []
    ru = lang == 'ru'
    for f in FO.F:
        out.append((f['id'], f['ru'] if ru else f['en']))
        out.append((f['id'] + '_desc', f['ru_d'] if ru else f['en_d']))
    for i in ID.I:
        out.append((i['id'], i['ru'] if ru else i['en']))
        out.append((i['id'] + '_desc', i['ru_d'] if ru else i['en_d']))
    for d in DE.D:
        out.append((d['id'], d['ru'] if ru else d['en']))
        out.append((d['id'] + '_desc', d['ru_d'] if ru else d['en_d']))
    for e in DE.E:
        n = 'ukrainewar.%d' % e['id']
        out.append((n + '.t', e['t_ru'] if ru else e['t_en']))
        out.append((n + '.d', e['d_ru'] if ru else e['d_en']))
        out.append((n + '.a', e['a_ru'] if ru else e['a_en']))
    for k, (a, b) in DE.TT.items():
        out.append((k, a if ru else b))
    return out


def loc_file(lang):
    head = 'l_russian:' if lang == 'ru' else 'l_english:'
    lines = [head]
    for k, v in all_loc(lang):
        lines.append(' %s:0 "%s"' % (k, v.replace('\n', '\\n')))
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------- фокусы
def focus_file():
    out = ['# Общее дерево войны Украины (DESIGN.md 8.5, сессия 24). ГЕНЕРИРУЕТСЯ _tools/gen_war_tree.py из _tools/war_tree_data/focuses.py.',
           '# Один набор shared_focus подключён строками shared_focus = ... ко всем шести деревьям (блок 1, блок 2, четыре опоры).',
           '# Сетка: y от 16 (ниже всех деревьев), шаг 2 по x. Слоты опор (x = 15) делят клетки: на экране виден один фокус, остальные скрыты allow_branch.',
           '# Все фокусы - available_if_capitulated = yes. Вводный фокус завершается скриптом (UKR_w_start_war_tree из ukrainewar.1).', '']
    for f in FO.F:
        b = ['shared_focus = {', '\tid = %s' % f['id'], '\ticon = %s' % f['icon'],
             '\tx = %d' % f['x'], '\ty = %d' % f['y'], '\tcost = %s' % num(f['cost'])]
        for grp in f['prereq']:
            b.append('\tprerequisite = { %s }' % ' '.join('focus = %s' % p for p in grp))
        if f['excl']:
            b.append('\tmutually_exclusive = { %s }' % ' '.join('focus = %s' % p for p in f['excl']))
        b.append('\tallow_branch = {')
        b.append(ind(f['allow'], 2))
        b.append('\t}')
        b.append('\tavailable_if_capitulated = yes')
        if f['avail']:
            b.append('\tavailable = {')
            b.append(ind(f['avail'], 2))
            b.append('\t}')
        b.append('\tai_will_do = {')
        b.append(ind(f['ai'], 2))
        b.append('\t}')
        b.append('\tcompletion_reward = {')
        b.append(ind(f['reward'], 2))
        b.append('\t}')
        b.append('}')
        out.append('\n'.join(b))
        out.append('')
    return '\n'.join(out)


# ---------------------------------------------------------------- идеи
def ideas_file():
    out = ['# Духи дерева войны (DESIGN.md 8.5, сессия 24). ГЕНЕРИРУЕТСЯ _tools/gen_war_tree.py из _tools/war_tree_data/ideas.py.',
           '# Иконки временные (CLAUDE.md, «Нужен арт»). Выдаются фокусами UKR_w_* и решениями UKR_wd_*.',
           'ideas = {', '\tcountry = {']
    for i in ID.I:
        out.append('\t\t%s = {' % i['id'])
        out.append('\t\t\tpicture = %s' % i['pic'])
        out.append('\t\t\tallowed = {\n\t\t\t\toriginal_tag = UKR\n\t\t\t}')
        out.append('\t\t\tremoval_cost = -1')
        out.append('\t\t\tmodifier = {')
        for k, v in i['mods'].items():
            out.append('\t\t\t\t%s = %s' % (k, num(v)))
        out.append('\t\t\t}')
        out.append('\t\t}')
        out.append('')
    out.append('\t}')
    out.append('}')
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------- решения
def decisions_file():
    out = ['# Решения дерева войны (DESIGN.md 8.5, сессия 24). ГЕНЕРИРУЕТСЯ _tools/gen_war_tree.py из _tools/war_tree_data/decisions.py.',
           '# Видны после соответствующего фокуса UKR_w_*; категория общая с остальными военными решениями.',
           'UKR_against_occupiers = {', '']
    for d in DE.D:
        out.append('\t%s = {' % d['id'])
        out.append('\t\ticon = %s' % d['icon'])
        out.append('\t\tvisible = {\n%s\n\t\t}' % ind(d['visible'], 3))
        out.append('\t\tavailable = {\n%s\n\t\t}' % ind(d['available'], 3))
        out.append('\t\tfire_only_once = no')
        out.append('\t\tcost = %d' % d['cost'])
        out.append('\t\tdays_re_enable = %d' % d['days_re_enable'])
        if d['days_remove']:
            out.append('\t\tdays_remove = %d' % d['days_remove'])
        if d['modifier']:
            out.append('\t\tmodifier = {\n%s\n\t\t}' % ind(d['modifier'], 3))
        out.append('\t\tcomplete_effect = {\n%s\n\t\t}' % ind(d['complete'], 3))
        if d['remove']:
            out.append('\t\tremove_effect = {\n%s\n\t\t}' % ind(d['remove'], 3))
        out.append('\t\tai_will_do = {\n%s\n\t\t}' % ind(d['ai'], 3))
        out.append('\t}')
        out.append('')
    out.append('}')
    return '\n'.join(out) + '\n'


# ---------------------------------------------------------------- события
def events_file():
    out = ['# Дерево войны: события ukrainewar.810-812 (DESIGN.md 8.5, сессия 24). ГЕНЕРИРУЕТСЯ _tools/gen_war_tree.py.',
           '# 810 - вводное (из UKR_w_start_war_tree), 811 - военное положение (из UKR_w_martial_law), 812 - вторая ступень дерева.',
           '', 'add_namespace = ukrainewar', '']
    for e in DE.E:
        n = 'ukrainewar.%d' % e['id']
        trig = ['tag = UKR']
        if e['id'] == 812:
            trig += ['has_country_flag = UKR_w_started', 'NOT = { has_country_flag = UKR_w_tier2 }']
        out.append('# art: reuse')
        out.append('country_event = {')
        out.append('\tid = %s' % n)
        out.append('\ttitle = %s.t' % n)
        out.append('\tdesc = %s.d' % n)
        out.append('\tpicture = %s' % e['pic'])
        out.append('')
        out.append('\tis_triggered_only = yes')
        out.append('\tfire_only_once = yes')
        out.append('')
        out.append('\ttrigger = {\n%s\n\t}' % ind('\n'.join(trig), 2))
        out.append('')
        out.append('\toption = {')
        out.append('\t\tname = %s.a' % n)
        if e['effect']:
            out.append(ind(e['effect'], 2))
        out.append('\t}')
        out.append('}')
        out.append('')
    return '\n'.join(out)


# ---------------------------------------------------------------- подключение к деревьям
def patch_tree(path):
    t = open(os.path.join(ROOT, path), encoding='utf-8-sig').read()
    raw = open(os.path.join(ROOT, path), 'rb').read()
    bom = raw.startswith(b'\xef\xbb\xbf')
    block = MARK_BEGIN + '\n' + '\n'.join('\tshared_focus = %s' % f['id'] for f in FO.F) + '\n' + MARK_END + '\n'
    if MARK_BEGIN in t:
        pre, rest = t.split(MARK_BEGIN, 1)
        _, post = rest.split(MARK_END + '\n', 1)
        t2 = pre + block + post
    else:
        m = re.search(r'\n(\t# [^\n]*\n)*\tfocus = \{', t)
        if not m:
            errors.append('не найден первый focus в %s' % path)
            return
        t2 = t[:m.start() + 1] + block + '\n' + t[m.start() + 1:]
    return t2, bom


def write(path, text, bom=False):
    full = os.path.join(ROOT, path)
    with open(full, 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='\n') as fh:
        fh.write(text)


def main():
    check()
    if errors:
        print('ОШИБКИ:')
        for e in errors:
            print('  ', e)
        sys.exit(1)
    outputs = {
        'common/national_focus/UKR_war_shared_focus.txt': (focus_file(), False),
        'common/ideas/UKR_ideas_war_tree.txt': (ideas_file(), False),
        'common/decisions/UKR_decisions_war_tree.txt': (decisions_file(), False),
        'events/UKR_events_war_tree.txt': (events_file(), False),
        'localisation/russian/UKR_war_tree_l_russian.yml': (loc_file('ru'), True),
        'localisation/english/UKR_war_tree_l_english.yml': (loc_file('en'), True),
    }
    for t in TREES:
        r = patch_tree(t)
        if r:
            outputs[t] = r
    if errors:
        print('ОШИБКИ:')
        for e in errors:
            print('  ', e)
        sys.exit(1)
    print('фокусов: %d, идей: %d, решений: %d, событий: %d, ключей локализации: %d'
          % (len(FO.F), len(ID.I), len(DE.D), len(DE.E), len(all_loc('ru'))))
    for p, (text, bom) in outputs.items():
        if WRITE:
            write(p, text, bom)
            print('записано', p)
        else:
            print('(проверка) ', p)
    if not WRITE:
        print('Ничего не записано: добавьте --write')


if __name__ == '__main__':
    main()
