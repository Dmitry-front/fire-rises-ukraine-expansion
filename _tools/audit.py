import os, re, sys, collections
# Статический аудит мода: python3 _tools/audit.py [путь к моду]
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(ROOT)
OWN = lambda p: not p.startswith('_')

def files(ext, base='.'):
    out = []
    for d, _, fs in os.walk(base):
        if '.git' in d: continue
        for f in fs:
            if f.endswith(ext): out.append(os.path.join(d, f)[2:] if d.startswith('./') or d == '.' else os.path.join(d, f))
    # Windows: пути приводим к виду с / (скрипт писался под Linux)
    out = [o.replace(chr(92), '/') for o in out]
    out = [o[2:] if o.startswith('./') else o for o in out]
    return sorted(out)

def read(p):
    b = open(p, 'rb').read()
    bom = b.startswith(b'\xef\xbb\xbf')
    return b.decode('utf-8-sig', errors='replace'), bom

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

print('=== BOM / кодировка / имена')
for p in files('.yml'):
    t, bom = read(p)
    first = t.lstrip().split('\n')[0].strip()
    print(f'{p}: BOM={bom} header={first}')
for p in files('.yml'):
    t, _ = read(p)
    for n, line in enumerate(t.split('\n'), 1):
        if any(c in line for c in '—–…'): print(f'ТИРЕ/МНОГОТОЧИЕ (в игре «?»): {p}:{n}')
for p in files('.txt'):
    if p.endswith('.txt.txt'): print('ДВОЙНОЕ РАСШИРЕНИЕ:', p)
    # BOM нужен только в .yml; в скриптах он портит первый токен и игра теряет первый блок файла
    if read(p)[1] and not p.startswith('_reference'): print('BOM В СКРИПТЕ (удалить):', p)

print('\n=== Баланс скобок')
texts = {}
for p in files('.txt') + files('.gui') + files('.gfx'):
    t, _ = read(p)
    c = strip_comments(t)
    texts[p] = c
    depth, minl = 0, None
    for i, line in enumerate(c.split('\n'), 1):
        for ch in line:
            if ch == '{': depth += 1
            elif ch == '}':
                depth -= 1
                if depth < 0 and minl is None: minl = i
    if depth != 0 or minl:
        print(f'{p}: итог={depth}' + (f', уход в минус на строке {minl}' if minl else ''))

def depth_at(c, pos):
    return c[:pos].count('{') - c[:pos].count('}')
def blocks_ids(p, pattern, depth=None):
    c = texts[p]
    return [(m.group(1), p, c[:m.start()].count('\n') + 1) for m in re.finditer(pattern, c) if depth is None or depth_at(c, m.start()) == depth]

print('\n=== Дубли ID событий (определения)')
evdefs = collections.defaultdict(list)
ev_re = r'(?:country_event|news_event|state_event|unit_leader_event|operative_leader_event)\s*=\s*\{\s*id\s*=\s*([\w\.]+)'
for p in [x for x in texts if x.startswith('events/') or 'events' in x and x.startswith('_reference/')]:
    for i, f, l in blocks_ids(p, ev_re, 0): evdefs[i].append((f, l))
# Индекс событий TFR из удалённого референса events_SOV (русские пространства имён); см. _tools/tfr_known_events.txt
known_tfr_events = set()
_kp = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tfr_known_events.txt')
if os.path.exists(_kp):
    known_tfr_events = {l.strip() for l in open(_kp, encoding='utf-8') if l.strip() and not l.startswith('#')}
own_ev = {k: [x for x in v if OWN(x[0])] for k, v in evdefs.items()}
for k, v in own_ev.items():
    if len(v) > 1: print(k, v)
print('\n=== Наши события, пересекающиеся с референсом SOV (дубль при загрузке)')
for k, v in evdefs.items():
    if any(OWN(x[0]) for x in v) and any(not OWN(x[0]) for x in v): print(k, v)
for k, v in own_ev.items():
    if v and k in known_tfr_events and not any(not OWN(x[0]) for x in evdefs[k]): print(k, v, '(есть в индексе TFR)')

print('\n=== Вызовы событий, не определённых у нас (могут быть в TFR)')
call_re = r'(?:country_event|news_event|state_event|unit_leader_event)\s*=\s*(?:\{[^{}]*?id\s*=\s*([\w]+\.\d+)|([\w]+\.\d+))'
calls = collections.defaultdict(list)
for p in texts:
    if not OWN(p): continue
    for m in re.finditer(call_re, texts[p]):
        e = m.group(1) or m.group(2)
        calls[e].append(f'{p}:{texts[p][:m.start()].count(chr(10))+1}')
for e, locs in sorted(calls.items()):
    if e not in own_ev or not own_ev[e]:
        inref = e in evdefs or e in known_tfr_events
        print(e, '(есть в референсе SOV)' if inref else '', locs[:3])

print('\n=== Дубли ID фокусов')
fdefs = collections.defaultdict(list)
for p in [x for x in texts if x.startswith('common/national_focus/') or 'national_focus' in x and x.startswith('_reference/')]:
    for i, f, l in blocks_ids(p, r'focus\s*=\s*\{\s*id\s*=\s*(\w+)', 1): fdefs[i].append((f, l))
for k, v in fdefs.items():
    if len(v) > 1: print(k, v)
ukr_focus = {k for k, v in fdefs.items() if any(OWN(x[0]) for x in v)}

print('\n=== Ссылки на фокусы UKR, которых нет')
for p in texts:
    if not OWN(p): continue
    for m in re.finditer(r'(?:focus|has_completed_focus|complete_national_focus|unlock_national_focus)\s*=\s*(UKR_\w+)', texts[p]):
        if m.group(1) not in ukr_focus:
            print(m.group(1), f'{p}:{texts[p][:m.start()].count(chr(10))+1}')

print('\n=== Идеи')
idea_defs = set()
for p in [x for x in texts if x.startswith('common/ideas/')]:
    c = texts[p]
    # идеи на глубине 3: ideas = { category = { idea = {
    depth = 0; tok = ''
    for m in re.finditer(r'(\w+)\s*=\s*\{|\{|\}', c):
        s = m.group(0)
        if s.endswith('{'):
            if depth == 2 and m.group(1): idea_defs.add(m.group(1))
            depth += 1
        else: depth -= 1
dyn_defs = set()
for p in [x for x in texts if x.startswith('common/dynamic_modifiers/')]:
    for m in re.finditer(r'^(\w+)\s*=\s*\{', texts[p], re.M): dyn_defs.add(m.group(1))
used = collections.defaultdict(list)
for p in texts:
    if not OWN(p): continue
    c = texts[p]
    for m in re.finditer(r'(?:add_ideas|remove_ideas|has_idea|add_timed_idea\s*=\s*\{\s*idea|swap_ideas\s*=\s*\{\s*(?:remove_idea|add_idea)|modify_timed_idea\s*=\s*\{\s*idea)\s*=\s*(\{[^{}]*\}|\w+)', c):
        v = m.group(1)
        for name in re.findall(r'\w+', v):
            if name.startswith('UKR_'): used[name].append(f'{p}:{c[:m.start()].count(chr(10))+1}')
for k, v in sorted(used.items()):
    if k not in idea_defs: print('нет идеи:', k, v[:2])
for m_ in sorted(set(re.findall(r'add_dynamic_modifier\s*=\s*\{\s*modifier\s*=\s*(UKR_\w+)', '\n'.join(t for p,t in texts.items() if OWN(p))))):
    if m_ not in dyn_defs: print('нет dynamic_modifier:', m_)

print('\n=== Персонажи')
chars = set(re.findall(r'^\t(UKR_\w+)\s*=\s*\{', texts['common/characters/TFR_characters_UKR.txt'], re.M))
for p in texts:
    if not OWN(p): continue
    for m in re.finditer(r'(?:recruit_character|character|retire_character|promote_character|has_character|has_country_leader\s*=\s*\{\s*character)\s*=\s*(UKR_\w+)', texts[p]):
        if m.group(1) not in chars: print('нет персонажа:', m.group(1), f'{p}:{texts[p][:m.start()].count(chr(10))+1}')

print('\n=== GFX')
gfx_defs = set()
for p in files('.gfx'):
    gfx_defs |= set(re.findall(r'name\s*=\s*"?(GFX_\w+)', texts[p]))
gfx_used = collections.defaultdict(list)
for p in texts:
    if not OWN(p) or p.endswith('.gfx'): continue
    for m in re.finditer(r'\b(GFX_\w+)', texts[p]): gfx_used[m.group(1)].append(p)
for g in sorted(gfx_used):
    if g not in gfx_defs and ('UKR' in g or 'ukr' in g.lower()):
        print('GFX с UKR не определён локально:', g, sorted(set(gfx_used[g]))[:2])
# файлы текстур
for p in files('.gfx'):
    for m in re.finditer(r'texturefile\s*=\s*"([^"]+)"', texts[p]):
        f = m.group(1)
        if ('UKR' in f or 'ukr' in f.lower()) and not os.path.exists(f) and not os.path.exists(f.replace('.dds', '.png')):
            print('нет файла текстуры:', f, 'в', p)

print('\n=== Локализация')
loc = {}
for p in files('.yml'):
    t, _ = read(p)
    lang = 'ru' if 'russian' in p else 'en'
    d = loc.setdefault(lang, collections.defaultdict(list))
    for i, line in enumerate(t.split('\n'), 1):
        m = re.match(r'^\s+([\w\.\-]+):\d*\s*"(.*)', line)
        if m: d[m.group(1)].append((p, i, m.group(2)))
for lang, d in loc.items():
    dups = {k: v for k, v in d.items() if len(v) > 1}
    print(f'[{lang}] дублей ключей: {len(dups)}')
    for k, v in list(dups.items())[:400]:
        print('  ', k, [(os.path.basename(a), b) for a, b, _ in v])
ru, en = loc['ru'], loc['en']
only_en = sorted(set(en) - set(ru)); only_ru = sorted(set(ru) - set(en))
print(f'Ключей только в EN: {len(only_en)}; только в RU: {len(only_ru)}')
print('  только EN (первые 60):', only_en[:60])
print('  только RU (первые 60):', only_ru[:60])
lat = [k for k, v in ru.items() if re.search(r'[A-Za-z]{4,}', v[-1][2]) and not re.search('[А-Яа-яЁё]', v[-1][2]) and v[-1][2].strip('"').strip()]
print(f'RU-ключей без кириллицы (вероятно не переведены): {len(lat)}')
print('  ', lat[:80])
# необходимые ключи
need = set()
for f in ukr_focus: need |= {f}
for e, v in own_ev.items():
    if v:
        need |= {e + '.t', e + '.d'}
for lang, d in loc.items():
    miss = sorted(k for k in need if k not in d)
    print(f'[{lang}] нет ключей для наших фокусов/событий: {len(miss)}', miss[:80])

print('\n=== Известные неверные конструкции (по error.log)')
BAD = [
    (r'\bis_tag\s*=', 'is_tag не существует: tag = X'),
    (r'\bhas_command_power\b', 'has_command_power не существует: command_power > X'),
    (r'^\s*stability\s*[<>]', 'stability как триггер: has_stability > X'),
    (r'^\s*ruling_party\s*=\s*\w+\s*$', 'ruling_party как триггер: has_government = X (допустимо только внутри set_politics)'),
    (r'\bhas_party\s*=', 'has_party не существует: <идеология> > 0.4'),
    (r'\bhas_popularity\s*=', 'has_popularity не существует: <идеология> > 0.4'),
    (r'\benemy_has_capitulated\b', 'enemy_has_capitulated не существует'),
    (r'\badd_army_experience\b', 'add_army_experience не существует: army_experience = X'),
    (r'\bunlock_decision_category\s*=', 'unlock_decision_category не существует: видимость категории через visible'),
    (r'\bruling_party_drift\b', 'ruling_party_drift не существует'),
    (r'\bproduction_speed_(tac_bomber|CAS|fighter)\w*_factor\b', 'такого модификатора нет'),
    (r'\bremove_timed_idea\b', 'remove_timed_idea не существует: remove_ideas'),
]
for p in files('.txt'):
    if p.startswith(('_reference', '_tools')): continue
    t, _ = read(p)
    in_setpol = False
    for n, line in enumerate(strip_comments(t).split('\n'), 1):
        if 'set_politics' in line: in_setpol = True
        for rx, msg in BAD:
            if 'ruling_party как триггер' in msg and in_setpol: continue
            if re.search(rx, line): print(f'{p}:{n}: {msg}')
        if in_setpol and '}' in line and 'set_politics' not in line: in_setpol = False

print('\n=== Имена TFR: сверка с _reference (подидеологии, черты, типы государства/экономики)')
# Типы государства и экономики собраны по всем референсам, включая удалённые из рабочей копии (events_SOV, bop_SOV); 04.10.2026.
GOV_TYPES = set('''provisional_government presidential_dictatorship socialist_republic semi_presidential_system parliamentary_republic
communist_party_state presidential_republic military_dictatorship revolutionary_front ultranationalist_dictatorship theocracy
semi_constitutional_monarchy constitutional_monarchy absolute_monarchy peoples_democracy fascist_dictatorship eurasianist_system
counterintelligence_state'''.split())
ECON_TYPES = set('''welfare_capitalism capitalism socialist_market mixed_economy planned_economy state_capitalism left_corporatism
command_economy oligopolistic_capitalism military_controlled worker_controlled corporatism liberal_corporatism minarchism
developed_socialism'''.split())

def ref_text(pattern):
    import glob as _g
    out = ''
    for f in _g.glob(os.path.join('_reference', pattern)):
        out += read(f)[0]
    return out

ideo_src = strip_comments(ref_text('*TFR_ideologies.txt'))
ideo_names = set(re.findall(r'[A-Za-z_][A-Za-z_0-9]*', ideo_src)) if ideo_src else set()
trait_names = set()
for f in __import__('glob').glob(os.path.join('_reference', '*TFR_traits_*.txt')):
    trait_names |= set(re.findall(r'^\t([A-Za-z_][A-Za-z_0-9]*)\s*=\s*\{', strip_comments(read(f)[0]), re.M))
TRAIT_PREFIX = re.compile(r'\b((?:hog|eco|for|sec|int|hos|army_chief|air_chief|navy_chief|theorist)_[a-z0-9_]+)\b')
bad_names = 0
for p in files('.txt'):
    if p.startswith(('_reference', '_tools')): continue
    c = strip_comments(read(p)[0])
    for n, line in enumerate(c.split('\n'), 1):
        for m in re.finditer(r'\b(?:ideology|ruling_party)\s*=\s*"?([A-Za-z_]+)"?', line):
            if ideo_names and m.group(1) not in ideo_names:
                print(f'{p}:{n}: идеология/подидеология не найдена в TFR: {m.group(1)}'); bad_names += 1
        for m in re.finditer(r'\bchange_government_type_(\w+)\s*=', line):
            if m.group(1) not in GOV_TYPES:
                print(f'{p}:{n}: нет такого типа государства в референсах: {m.group(1)}'); bad_names += 1
        for m in re.finditer(r'\bchange_economy_type_(\w+)\s*=', line):
            if m.group(1) not in ECON_TYPES:
                print(f'{p}:{n}: нет такого типа экономики в референсах: {m.group(1)}'); bad_names += 1
        if trait_names and 'trait' in line:
            for m in TRAIT_PREFIX.finditer(line):
                if m.group(1) not in trait_names:
                    print(f'{p}:{n}: черта не найдена в референсах: {m.group(1)}'); bad_names += 1
print('несовпадений имён TFR:', bad_names)
