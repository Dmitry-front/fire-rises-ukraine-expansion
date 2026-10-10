#!/usr/bin/env python3
"""Сравнение наших файлов, заменяющих файлы TFR, с оригиналом: python3 _tools/tfr_drift.py [путь к референсу]

Берёт каждый файл репозитория (кроме папок на «_» и .git), у которого есть файл с тем же путём в референсе
(_reference/TFR_Reference), и показывает:
- .yml: ключи, потерянные нами (есть в TFR, нет нигде в нашей локализации), наши лишние и различающиеся по тексту;
- .txt (события, решения, идеи, персонажи, категории): объекты идентичные / изменённые / только в TFR / только у нас;
- прочее: число отличающихся строк.
Нужен, пока лежит референс; результаты на 10.10.2026 записаны в TFR_SYNC.md.
"""
import os, re, sys, glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
REF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_reference', 'TFR_Reference')
os.chdir(ROOT)
if not os.path.isdir(REF):
    sys.exit('Референс не найден: %s' % REF)


def read(p):
    return open(p, 'rb').read().decode('utf-8-sig', errors='replace').replace('\r', '')


def strip(t):
    return re.sub(r'#[^\n]*', '', t)


def norm(b):
    return re.sub(r'\s+', ' ', b).strip()


def objects(text, rel):
    """Объекты верхнего уровня по типу файла: {имя: нормализованное тело}."""
    t = strip(text)
    out, stack, depth = {}, [], 0
    if rel.startswith('events/'): kind = 'event'
    elif rel.startswith('common/ideas/'): kind = 'ideas'
    elif rel.startswith('common/decisions/categories/'): kind = 'cats'
    elif rel.startswith('common/decisions/'): kind = 'decisions'
    elif rel.startswith('common/characters/'): kind = 'chars'
    else: return None
    for m in re.finditer(r'([\w:.\-]+)\s*=\s*\{|\{|\}', t):
        s = m.group(0)
        if s.endswith('{'):
            stack.append((m.group(1), m.start(), depth)); depth += 1
        else:
            depth -= 1
            n, st, dd = stack.pop()
            body = t[st:m.end()]
            if kind == 'event' and dd == 0 and n in ('country_event', 'news_event'):
                i = re.search(r'id\s*=\s*([\w.]+)', body)
                if i: out[i.group(1)] = norm(body)
            elif kind == 'ideas' and dd == 2 and n: out[n] = norm(body)
            elif kind == 'decisions' and dd == 1 and n: out[n] = norm(body)
            elif kind == 'cats' and dd == 0 and n: out[n] = norm(body)
            elif kind == 'chars' and dd == 1 and n: out[n] = norm(body)
    return out


def loc_keys(text):
    d = {}
    for l in text.split('\n'):
        m = re.match(r'^\s+([\w\.\-]+):\d*\s*"(.*)"', l)
        if m: d[m.group(1)] = m.group(2)
    return d


own_files = []
for d, dirs, fs in os.walk('.'):
    if os.path.normpath(d) == '.': dirs[:] = [x for x in dirs if not x.startswith(('_', '.'))]
    for f in fs:
        own_files.append(os.path.relpath(os.path.join(d, f), '.').replace(os.sep, '/'))

# все наши ключи по языкам (потерянным считается ключ, которого нет нигде в нашей локализации языка)
our_loc = {}
for p in own_files:
    m = re.match(r'localisation/(\w+)/.*\.yml$', p)
    if m: our_loc.setdefault(m.group(1), {}).update(loc_keys(read(p)))

pairs = sorted(p for p in own_files if os.path.exists(os.path.join(REF, p)))
print('Файлов с двойником в референсе:', len(pairs), '\n')
for p in pairs:
    o, r = read(p), read(os.path.join(REF, p))
    if o == r:
        print('= идентичен   ', p); continue
    if p.endswith('.yml'):
        lang = re.match(r'localisation/(\w+)/', p).group(1)
        ok, rk = loc_keys(o), loc_keys(r)
        lost = [k for k in rk if k not in our_loc.get(lang, {})]
        extra = [k for k in ok if k not in rk]
        diff = [k for k in ok if k in rk and ok[k] != rk[k]]
        print(f'~ локализация  {p}: TFR {len(rk)}, у нас {len(ok)}, потеряно {len(lost)}, наших лишних {len(extra)}, текст иначе {len(diff)}')
        continue
    oo, ro = objects(o, p), objects(r, p)
    if oo is not None and ro is not None:
        same = [k for k in ro if k in oo and oo[k] == ro[k]]
        changed = [k for k in ro if k in oo and oo[k] != ro[k]]
        only_r = [k for k in ro if k not in oo]
        only_o = [k for k in oo if k not in ro]
        print(f'~ объекты      {p}: TFR {len(ro)}, у нас {len(oo)}; идентично {len(same)}, изменено {len(changed)}, только в TFR {len(only_r)}, только у нас {len(only_o)}')
        if changed: print('    изменено:', ', '.join(changed[:20]))
        if only_r: print('    только в TFR:', ', '.join(only_r[:20]))
        continue
    import difflib
    n = sum(1 for l in difflib.unified_diff(r.split('\n'), o.split('\n'), lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++', '---')))
    print(f'~ строки       {p}: отличающихся строк {n}')
