#!/usr/bin/env python3
"""Индекс имён TFR для audit.py: python3 _tools/build_tfr_index.py [путь к референсу]

Читает референс (по умолчанию _reference/TFR_Reference) и пишет компактные списки в _tools/tfr_index/.
audit.py проверяет только НАШ код и сверяется с этим индексом, а не с самим референсом.
Индекс лежит в репозитории, поэтому папку _reference можно удалить - аудит продолжит работать.
Пересобирать индекс нужно при обновлении референса (новая версия TFR).
"""
import os, re, sys, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
REF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_reference', 'TFR_Reference')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tfr_index')

if not os.path.isdir(REF):
    sys.exit('Референс не найден: %s' % REF)
os.makedirs(OUT, exist_ok=True)


def read(p):
    return open(p, 'rb').read().decode('utf-8-sig', errors='replace')


def strip_comments(t):
    out = []
    for line in t.split('\n'):
        res, q = '', False
        for ch in line:
            if ch == '"': q = not q
            if ch == '#' and not q: break
            res += ch
        out.append(res)
    return '\n'.join(out)


def walk(sub, ext):
    base = os.path.join(REF, sub)
    for d, _, fs in os.walk(base):
        for f in sorted(fs):
            if f.endswith(ext): yield os.path.join(d, f)


def depth_at(c, pos):
    return c[:pos].count('{') - c[:pos].count('}')


def write(name, rows, header):
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# %s\n# Сгенерировано _tools/build_tfr_index.py из референса TFR, не править руками.\n' % header)
        for r in sorted(set(rows)):
            f.write(r + '\n')
    print('%-16s %6d' % (name, len(set(rows))))


# --- события: id <TAB> файл (определения на верхнем уровне)
ev_re = re.compile(r'(?:country_event|news_event|state_event|unit_leader_event|operative_leader_event)\s*=\s*\{\s*id\s*=\s*([\w\.]+)')
rows = []
for p in walk('events', '.txt'):
    c = strip_comments(read(p))
    for m in ev_re.finditer(c):
        if depth_at(c, m.start()) == 0: rows.append('%s\t%s' % (m.group(1), os.path.basename(p)))
write('events.txt', rows, 'События TFR: id, файл')

# --- фокусы: id <TAB> файл
rows = []
for p in walk(os.path.join('common', 'national_focus'), '.txt'):
    c = strip_comments(read(p))
    for m in re.finditer(r'\bfocus\s*=\s*\{\s*id\s*=\s*(\w+)', c):
        rows.append('%s\t%s' % (m.group(1), os.path.basename(p)))
write('focuses.txt', rows, 'Фокусы TFR: id, файл')

# --- спрайты (определения в .gfx)
rows = []
for sub in ('interface', 'gfx'):
    for p in walk(sub, '.gfx'):
        rows += re.findall(r'name\s*=\s*"?(GFX_\w+)', strip_comments(read(p)))
write('gfx.txt', rows, 'Спрайты TFR (определения в .gfx; самих картинок в индексе нет)')

# --- подидеологии: все идентификаторы из файла идеологий (как делал аудит раньше)
rows = []
for p in walk(os.path.join('common', 'ideologies'), '.txt'):
    rows += re.findall(r'[A-Za-z_][A-Za-z_0-9]*', strip_comments(read(p)))
write('ideologies.txt', rows, 'Идентификаторы из common/ideologies TFR (подидеологии и прочее)')

# --- черты лидеров и министров
rows = []
for p in walk(os.path.join('common', 'country_leader'), '.txt'):
    rows += re.findall(r'^\t([A-Za-z_][A-Za-z_0-9]*)\s*=\s*\{', strip_comments(read(p)), re.M)
write('traits.txt', rows, 'Черты (common/country_leader TFR)')

# --- типы государства и экономики: по всему референсу
gov, eco = [], []
for sub in ('common', 'events', 'history'):
    for p in walk(sub, '.txt'):
        t = read(p)
        gov += re.findall(r'\bchange_government_type_(\w+)', t)
        eco += re.findall(r'\bchange_economy_type_(\w+)', t)
gov = [x for x in gov if not x.endswith('_tt')]  # *_tt - ключи подсказок, не типы
eco = [x for x in eco if not x.endswith('_tt')]
write('gov_types.txt', gov, 'Типы государства: change_government_type_<имя> в TFR')
write('econ_types.txt', eco, 'Типы экономики: change_economy_type_<имя> в TFR')

# --- идеи (ideas = { категория = { идея = { ...) и динамические модификаторы
rows = []
for p in walk(os.path.join('common', 'ideas'), '.txt'):
    c = strip_comments(read(p))
    depth = 0
    for m in re.finditer(r'(\w+)\s*=\s*\{|\{|\}', c):
        if m.group(0).endswith('{'):
            if depth == 2 and m.group(1): rows.append(m.group(1))
            depth += 1
        else: depth -= 1
write('ideas.txt', rows, 'Идеи TFR (common/ideas, третий уровень вложенности)')
rows = []
for p in walk(os.path.join('common', 'dynamic_modifiers'), '.txt'):
    c = strip_comments(read(p))
    # файл может быть как списком на верхнем уровне, так и обёрнут в dynamic_modifiers = { ... }
    rows += [m.group(1) for m in re.finditer(r'^[ \t]*(\w+)\s*=\s*\{', c, re.M)
             if depth_at(c, m.start()) in (0, 1) and m.group(1) != 'dynamic_modifiers']
write('dynamic_modifiers.txt', rows, 'Динамические модификаторы TFR')
