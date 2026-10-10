import os, re, sys, collections
# Статический аудит мода: python3 _tools/audit.py [путь к моду]
# Проверяется ТОЛЬКО наш код: папки на «_» (_reference, _tools) в обход не попадают.
# С TFR сверяемся по индексу _tools/tfr_index/ (python3 _tools/build_tfr_index.py), а не по самому референсу:
# папку _reference можно удалить, аудит продолжит работать.
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(ROOT)


def load_index(name):
    """Индекс TFR: строки 'ключ' или 'ключ<TAB>файл'. Без индекса сверка с TFR пропускается."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tfr_index', name)
    if not os.path.exists(path): return {}
    out = {}
    for l in open(path, encoding='utf-8'):
        l = l.rstrip('\n')
        if not l or l.startswith('#'): continue
        k, _, v = l.partition('\t')
        out.setdefault(k, set()).add(v)
    return out

def files(ext, base='.'):
    out = []
    for d, dirs, fs in os.walk(base):
        if '.git' in d: continue
        if os.path.normpath(d) == os.path.normpath(base): dirs[:] = [x for x in dirs if not x.startswith('_')]
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
    if read(p)[1]: print('BOM В СКРИПТЕ (удалить):', p)

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
def block_end(c, start):
    """Позиция закрывающей скобки блока, чья открывающая скобка первая после start."""
    d, i = 0, c.index('{', start)
    for j in range(i, len(c)):
        if c[j] == '{': d += 1
        elif c[j] == '}':
            d -= 1
            if d == 0: return j
    return len(c)

hidden_ev = set()  # скрытые события: игроку не показываются, заголовка и текста нет
for p in [x for x in texts if x.startswith('events/')]:
    for i, f, l in blocks_ids(p, ev_re, 0): evdefs[i].append((f, l))
    c = texts[p]
    for m in re.finditer(ev_re, c):
        if depth_at(c, m.start()) != 0: continue
        body = c[m.start():block_end(c, m.start())]
        # hidden = yes только на первом уровне блока события (глубже - это опции и эффекты)
        if any(depth_at(body, h.start()) == 1 for h in re.finditer(r'\bhidden\s*=\s*yes\b', body)):
            hidden_ev.add(m.group(1))
tfr_events = load_index('events.txt')  # id -> {файлы TFR}
own_files = {os.path.basename(f) for v in evdefs.values() for f, _ in v}
for k, v in evdefs.items():
    if len(v) > 1: print(k, v)
print('\n=== Наши события с ID, который TFR определяет в другом файле (дубль при загрузке)')
# файл с тем же именем, что у файла TFR, заменяет его целиком - совпадение ID там ожидаемо
for k, v in evdefs.items():
    other = {f for f in tfr_events.get(k, ()) if f not in own_files}
    if other: print(k, v, 'в TFR:', sorted(other))

print('\n=== Вызовы событий, не определённых у нас (могут быть в TFR)')
call_re = r'(?:country_event|news_event|state_event|unit_leader_event)\s*=\s*(?:\{[^{}]*?id\s*=\s*([\w]+\.\d+)|([\w]+\.\d+))'
calls = collections.defaultdict(list)
for p in texts:
    for m in re.finditer(call_re, texts[p]):
        e = m.group(1) or m.group(2)
        calls[e].append(f'{p}:{texts[p][:m.start()].count(chr(10))+1}')
for e, locs in sorted(calls.items()):
    if e not in evdefs:
        print(e, '(есть в TFR)' if e in tfr_events else 'НЕТ НИ У НАС, НИ В TFR', locs[:3])

print('\n=== Дубли ID фокусов')
fdefs = collections.defaultdict(list)
for p in [x for x in texts if x.startswith('common/national_focus/')]:
    for i, f, l in blocks_ids(p, r'focus\s*=\s*\{\s*id\s*=\s*(\w+)', 1): fdefs[i].append((f, l))
tfr_focuses = load_index('focuses.txt')
own_focus_files = {os.path.basename(f) for v in fdefs.values() for f, _ in v}
for k, v in fdefs.items():
    if len(v) > 1: print(k, v)
    other = {f for f in tfr_focuses.get(k, ()) if f not in own_focus_files}
    if other: print(k, v, 'ID есть в TFR в другом файле:', sorted(other))
ukr_focus = set(fdefs)

print('\n=== Ссылки на фокусы UKR, которых нет')
for p in texts:
    for m in re.finditer(r'(?:focus|has_completed_focus|complete_national_focus|unlock_national_focus)\s*=\s*(UKR_\w+)', texts[p]):
        if m.group(1) not in ukr_focus:
            print(m.group(1), f'{p}:{texts[p][:m.start()].count(chr(10))+1}')

print('\n=== Идеи')
tfr_ideas, tfr_dyn = load_index('ideas.txt'), load_index('dynamic_modifiers.txt')
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
    c = texts[p]
    for m in re.finditer(r'(?:add_ideas|remove_ideas|has_idea|add_timed_idea\s*=\s*\{\s*idea|swap_ideas\s*=\s*\{\s*(?:remove_idea|add_idea)|modify_timed_idea\s*=\s*\{\s*idea)\s*=\s*(\{[^{}]*\}|\w+)', c):
        v = m.group(1)
        for name in re.findall(r'\w+', v):
            if name.startswith('UKR_'): used[name].append(f'{p}:{c[:m.start()].count(chr(10))+1}')
for k, v in sorted(used.items()):
    if k not in idea_defs and k not in tfr_ideas: print('нет идеи:', k, v[:2])
for m_ in sorted(set(re.findall(r'add_dynamic_modifier\s*=\s*\{\s*modifier\s*=\s*(UKR_\w+)', '\n'.join(texts.values())))):
    if m_ not in dyn_defs and m_ not in tfr_dyn: print('нет dynamic_modifier:', m_)

print('\n=== Персонажи')
chars = set(re.findall(r'^\t(UKR_\w+)\s*=\s*\{', texts['common/characters/TFR_characters_UKR.txt'], re.M))
for p in texts:
    for m in re.finditer(r'(?:recruit_character|character|retire_character|promote_character|has_character|has_country_leader\s*=\s*\{\s*character)\s*=\s*(UKR_\w+)', texts[p]):
        if m.group(1) not in chars: print('нет персонажа:', m.group(1), f'{p}:{texts[p][:m.start()].count(chr(10))+1}')

print('\n=== GFX')
tfr_gfx = load_index('gfx.txt')  # спрайты TFR (картинок в репозитории нет, определения - в индексе)
gfx_defs = set()
for p in files('.gfx'):
    gfx_defs |= set(re.findall(r'name\s*=\s*"?(GFX_\w+)', texts[p]))
gfx_used = collections.defaultdict(list)
for p in texts:
    if p.endswith('.gfx'): continue
    for m in re.finditer(r'\b(GFX_\w+)', texts[p]): gfx_used[m.group(1)].append(p)
for g in sorted(gfx_used):
    if g not in gfx_defs and g not in tfr_gfx and ('UKR' in g or 'ukr' in g.lower()):
        print('GFX с UKR не определён локально:', g, sorted(set(gfx_used[g]))[:2])
# файлы текстур
for p in files('.gfx'):
    for m in re.finditer(r'texturefile\s*=\s*"([^"]+)"', texts[p]):
        f = m.group(1)
        if ('UKR' in f or 'ukr' in f.lower()) and not os.path.exists(f) and not os.path.exists(f.replace('.dds', '.png')):
            print('нет файла текстуры:', f, 'в', p)

# --- пути и формат графики (см. CLAUDE.md, «Графика»)
print('\n=== GFX: пути, форматы, дубли')
sprite_names = collections.defaultdict(list)
goal_sprites = []
for p in files('.gfx'):
    if p.startswith('_'): continue
    for blk in re.finditer(r'[sS]prite[tT]ype\s*=\s*\{', texts[p]):
        # тело спрайта: до парной закрывающей скобки
        i, depth = blk.end(), 1
        while i < len(texts[p]) and depth:
            depth += {'{': 1, '}': -1}.get(texts[p][i], 0); i += 1
        body = texts[p][blk.end():i]
        nm = re.search(r'name\s*=\s*"?(GFX_\w+)', body)
        if not nm: continue
        sprite_names[nm.group(1)].append(p)
        tf = re.search(r'texturefile\s*=\s*"([^"]+)"', body)
        # иконка фокуса: пара GFX_x + GFX_x_shine, а блик (_shine) обязан иметь buttonstate.lua и анимацию
        if tf and '/interface/goals/' in tf.group(1):
            if nm.group(1).endswith('_shine'):
                if 'buttonstate.lua' not in body or 'animation' not in body: print('SHINE БЕЗ buttonstate.lua/animation:', nm.group(1), p)
            else:
                goal_sprites.append(nm.group(1))
for g in goal_sprites:
    if g + '_shine' not in sprite_names: print('ФОКУС-ИКОНКА БЕЗ ПАРЫ _shine:', g)
for n, ps in sprite_names.items():
    if len(ps) > 1: print('СПРАЙТ ОПРЕДЕЛЁН НЕСКОЛЬКО РАЗ:', n, ps)
# формат файла по содержимому, а не по расширению (PNG, переименованный в .dds, в игре не грузится)
for d, _, fs in os.walk('gfx'):
    for f in fs:
        pth = os.path.join(d, f).replace(chr(92), '/')
        head = open(pth, 'rb').read(8)
        if f.lower().endswith('.dds') and not head.startswith(b'DDS '): print('ФАЙЛ .dds НЕ ЯВЛЯЕТСЯ DDS:', pth)
        if f.lower().endswith('.png') and not head.startswith(b'\x89PNG'): print('ФАЙЛ .png НЕ ЯВЛЯЕТСЯ PNG:', pth)
# пути gfx/... в скриптах (портреты персонажей и т.п.): наши UKR-файлы должны существовать
for p in texts:
    if p.endswith('.gfx'): continue
    for m in re.finditer(r'"(gfx/[^"]*/UKR/[^"]+\.(?:png|dds|tga))"', texts[p]):
        if not os.path.exists(m.group(1)): print('НЕТ ФАЙЛА ПО ПУТИ:', m.group(1), p)
# idea: picture = X ищет GFX_idea_X (префикс игра добавляет сама, picture = GFX_... даёт GFX_idea_GFX_... и пустую иконку)
for p in texts:
    if p.startswith('common/ideas/'):
        for m in re.finditer(r'\bpicture\s*=\s*"?(GFX_\w+)', texts[p]): print('ИДЕЯ: picture с префиксом GFX_ (убрать GFX_idea_):', m.group(1), p)
# idea picture = X -> GFX_idea_X, если X начинается с UKR_ (наш арт), спрайт должен быть определён
for p in texts:
    if not p.startswith('common/ideas/'): continue
    for m in re.finditer(r'\bpicture\s*=\s*"?(UKR_\w+)"?', texts[p]):
        if 'GFX_idea_' + m.group(1) not in sprite_names:
            print('ИДЕЯ: нет спрайта GFX_idea_%s (если арт из TFR - проигнорировать):' % m.group(1), p)
for p in texts:
    if not p.startswith('common/intelligence_agencies/'): continue
    for m in re.finditer(r'picture\s*=\s*(GFX_\w*(?:Ukraine|UKR)\w*)', texts[p]):
        if m.group(1) not in sprite_names: print('АГЕНТСТВО: нет спрайта', m.group(1))

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
for e, v in evdefs.items():
    if v and e not in hidden_ev:
        need |= {e + '.t', e + '.d'}
for lang, d in loc.items():
    # описание с вариантами (desc = { trigger ... text = X.d_court }) - ключа X.d нет, есть X.d_*
    miss = sorted(k for k in need if k not in d and not (k.endswith('.d') and any(x.startswith(k + '_') for x in d)))
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
    t, _ = read(p)
    in_setpol = False
    for n, line in enumerate(strip_comments(t).split('\n'), 1):
        if 'set_politics' in line: in_setpol = True
        for rx, msg in BAD:
            if 'ruling_party как триггер' in msg and in_setpol: continue
            if re.search(rx, line): print(f'{p}:{n}: {msg}')
        if in_setpol and '}' in line and 'set_politics' not in line: in_setpol = False

print('\n=== Имена TFR: сверка с индексом TFR (подидеологии, черты, типы государства/экономики)')
GOV_TYPES = set(load_index('gov_types.txt'))
ECON_TYPES = set(load_index('econ_types.txt'))
ideo_names = set(load_index('ideologies.txt'))
trait_names = set(load_index('traits.txt'))
if not (GOV_TYPES and ECON_TYPES and ideo_names and trait_names):
    print('индекс TFR не найден (python3 _tools/build_tfr_index.py) - сверка имён пропущена')
TRAIT_PREFIX = re.compile(r'\b((?:hog|eco|for|sec|int|hos|army_chief|air_chief|navy_chief|theorist)_[a-z0-9_]+)\b')
bad_names = 0
for p in files('.txt'):
    c = strip_comments(read(p)[0])
    for n, line in enumerate(c.split('\n'), 1):
        for m in re.finditer(r'\b(?:ideology|ruling_party)\s*=\s*"?([A-Za-z_]+)"?', line):
            if ideo_names and m.group(1) not in ideo_names:
                print(f'{p}:{n}: идеология/подидеология не найдена в TFR: {m.group(1)}'); bad_names += 1
        for m in re.finditer(r'\bchange_government_type_(\w+)\s*=', line):
            if GOV_TYPES and m.group(1) not in GOV_TYPES:
                print(f'{p}:{n}: нет такого типа государства в TFR: {m.group(1)}'); bad_names += 1
        for m in re.finditer(r'\bchange_economy_type_(\w+)\s*=', line):
            if ECON_TYPES and m.group(1) not in ECON_TYPES:
                print(f'{p}:{n}: нет такого типа экономики в TFR: {m.group(1)}'); bad_names += 1
        if trait_names and 'trait' in line:
            for m in TRAIT_PREFIX.finditer(line):
                if m.group(1) not in trait_names:
                    print(f'{p}:{n}: черта не найдена в TFR: {m.group(1)}'); bad_names += 1
print('несовпадений имён TFR:', bad_names)
