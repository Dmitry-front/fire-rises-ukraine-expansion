#!/usr/bin/env python3
"""Карта картинок событий: python3 _tools/art_map.py [--all] [--out ART_MAP.md]

Берёт наши события из events/, их заголовок и текст из localisation/russian, текущую
картинку, и предлагает кандидатов из TFR по смыслу (_tools/tfr_index/event_pictures.txt
и gfx.txt) и из наших спрайтов (interface/UKR_event_pictures.gfx).
По умолчанию - только события с временной картинкой (нет спрайта или заглушка).
Колонка «Решение» в ART_MAP.md сохраняется при перезапуске (по ID события).
Строка-директива над событием: "# art: reuse" - картинка поставлена временно из уже существующего спрайта, событие попадает в карту;
"# art: -" - картинка не нужна (событие страны-ответчика, его видит только игрок за неё), в карту не попадает.
Отдельный раздел карты - значки решений и духов из ICON_SOURCES (ID, что изобразить, имя файла, статус).
Подбор идёт по ключевым словам (ART_THEMES ниже), это подсказка, а не автозамена:
смотреть превью картинок в установленной TFR и записывать выбор в колонку «Решение».
"""
import os, re, sys, glob, collections

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
IDX = os.path.join(ROOT, '_tools', 'tfr_index')

# Заглушки: спрайт либо не определён нигде, либо взят как временный
PLACEHOLDERS = {'GFX_report_event_ukrainian_civil_war'}


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


def event_blocks(c):
    """Верхнеуровневые блоки country_event/news_event с отступом по скобкам; третье значение - номер строки начала."""
    for m in re.finditer(r'^(country_event|news_event)\s*=\s*\{', c, re.M):
        i, d = m.end(), 1
        while i < len(c) and d:
            d += (c[i] == '{') - (c[i] == '}')
            i += 1
        yield m.group(1), c[m.end():i - 1], c.count('\n', 0, m.start())


def art_directive(raw_lines, line_idx):
    """Директива "# art: ..." в ближайшей непустой строке над событием (reuse или -), иначе None."""
    j = line_idx - 1
    while j >= 0 and not raw_lines[j].strip():
        j -= 1
    if j >= 0:
        m = re.match(r'\s*#\s*art:\s*(\S+)', raw_lines[j])
        if m:
            return m.group(1)
    return None


# Значки (решения и духи) с временной или чужой картинкой: (раздел, файл, вид, папка PNG, размер, поле картинки)
ICON_SOURCES = [
    ('decision', 'common/decisions/UKR_decisions_allies.txt', 'gfx/interface/decisions/UKR', '45x45', 'icon'),
    ('idea', 'common/ideas/UKR_ideas_allies.txt', 'gfx/interface/ideas/UKR', '68x68', 'picture'),
    ('idea', 'common/ideas/UKR_ideas_coalition.txt', 'gfx/interface/ideas/UKR', '68x68', 'picture'),
    ('decision', 'common/decisions/UKR_decisions_war_tree.txt', 'gfx/interface/decisions/UKR', '45x45', 'icon'),
    ('idea', 'common/ideas/UKR_ideas_war_tree.txt', 'gfx/interface/ideas/UKR', '68x68', 'picture'),
]


def icon_rows(loc):
    """Значки из ICON_SOURCES: (вид, ключ, название, что изобразить, сейчас, папка, размер, есть_lim)."""
    rows = []
    for kind, rel, folder, size, field in ICON_SOURCES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        text = strip_comments(read(path))
        indent = r'\t' if kind == 'decision' else r'\t\t'
        keys = re.findall(r'^%s(UKR_\w+) = \{' % indent, text, re.M)
        for m in re.finditer(r'^%s(UKR_\w+) = \{' % indent, text, re.M):
            key, i, d = m.group(1), m.end(), 1
            while i < len(text) and d:
                d += (text[i] == '{') - (text[i] == '}')
                i += 1
            body = text[m.end():i - 1]
            pic = re.search(r'^\s*%s\s*=\s*(\S+)' % field, body, re.M)
            if kind == 'idea' and key.endswith('_lim'):
                continue
            desc = clean(loc.get(key + '_desc', ''))
            short = desc.split('. ')[0][:160]
            rows.append((kind, key, clean(loc.get(key, '')), short, pic.group(1) if pic else '-', folder, size,
                         (key + '_lim') in keys))
    return rows


def load_loc():
    loc = {}
    for p in glob.glob(os.path.join(ROOT, 'localisation', 'russian', '*.yml')):
        for line in read(p).split('\n'):
            m = re.match(r'\s*([\w\.\-]+):\d*\s+"(.*)"\s*$', line)
            if m: loc[m.group(1)] = m.group(2)
    return loc


def clean(s):
    s = re.sub(r'§.', '', s)
    s = re.sub(r'\\n|\[[^\]]*\]|\$[^$]*\$|£\w+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def load_sprites():
    tfr = {}
    for line in read(os.path.join(IDX, 'event_pictures.txt')).split('\n'):
        if line and not line.startswith('#'):
            n, f = line.split('\t')
            tfr[n] = f
    allgfx = set(l for l in read(os.path.join(IDX, 'gfx.txt')).split('\n') if l and not l.startswith('#'))
    ours = {}
    for p in glob.glob(os.path.join(ROOT, 'interface', '*.gfx')):
        for m in re.finditer(r'name\s*=\s*"?(GFX_\w+)"?[^}]*?texturefile\s*=\s*"([^"]+)"', read(p), re.S):
            ours[m.group(1)] = os.path.basename(m.group(2))
    return tfr, allgfx, ours


# Темы: (название, регулярка по русскому тексту события, слова для поиска в именах спрайтов TFR, готовые кандидаты)
# Готовые кандидаты проверяются на существование; если спрайта нет, молча пропускаются.
ART_THEMES = []
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'art_themes.py'), encoding='utf-8').read())


def check_themes(known):
    bad = [(n, s) for n, _, _, ready in ART_THEMES for s in ready if s not in known]
    for n, s in bad:
        print('ПРЕДУПРЕЖДЕНИЕ: тема «%s»: спрайт %s не найден, будет пропущен' % (n, s), file=sys.stderr)


def tokens(name, fname):
    s = (name.replace('GFX_', '') + ' ' + os.path.splitext(fname)[0]).lower()
    return set(re.findall(r'[a-z0-9]+', s))


def suggest(title, desc, tfr, allgfx, ours, limit=4):
    """Возвращает (темы, [(спрайт, откуда, балл)]). Совпадение в заголовке весит втрое больше, чем в описании;
    тема засчитывается, если есть совпадение в заголовке или два в описании."""
    tl, dl = title.lower(), desc.lower()
    themes, scores = [], collections.OrderedDict()
    for name, rx, words, ready in ART_THEMES:
        w = 3 * min(len(re.findall(rx, tl)), 2) + min(len(re.findall(rx, dl)), 2)
        if w < 2: continue
        themes.append((w, name))
        for s in ready:
            if s in ours: scores[s] = (scores.get(s, (0, ''))[0] + 5 * w, 'наш')
            elif s in allgfx or s in tfr: scores[s] = (scores.get(s, (0, ''))[0] + 4 * w, 'TFR')
        wset = set(words)
        for pool, tag, mul in ((ours, 'наш*', 2), (tfr, 'TFR*', 1)):
            for s, f in pool.items():
                if tokens(s, f) & wset and s not in scores:
                    scores[s] = (mul * w * len(tokens(s, f) & wset), tag)
    themes.sort(reverse=True)
    ranked = sorted(scores.items(), key=lambda kv: -kv[1][0])
    return [t for _, t in themes[:3]], [(s, v[1], v[0]) for s, v in ranked[:limit]]


def file_name(eid):
    """Имя файла картинки события: UKR_<id с подчёркиваниями>.png (папка gfx/event_pictures/)."""
    return 'UKR_%s.png' % eid.replace('.', '_')


def main():
    show_all = '--all' in sys.argv
    out = os.path.join(ROOT, 'ART_MAP.md')
    if '--out' in sys.argv: out = sys.argv[sys.argv.index('--out') + 1]
    loc = load_loc()
    tfr, allgfx, ours = load_sprites()
    known = set(tfr) | allgfx | set(ours)
    check_themes(known)
    tfr_events = set(l.split('\t')[0] for l in read(os.path.join(IDX, 'events.txt')).split('\n') if l and not l.startswith('#'))
    rows = []
    for p in sorted(glob.glob(os.path.join(ROOT, 'events', '*.txt'))):
        base = os.path.basename(p)
        raw = read(p)
        raw_lines = raw.split('\n')
        for kind, b, ln in event_blocks(strip_comments(raw)):
            directive = art_directive(raw_lines, ln)
            if directive == '-': continue
            mid = re.search(r'\bid\s*=\s*([\w\.]+)', b)
            pic = re.search(r'^\s*picture\s*=\s*(\w+)', b, re.M)
            if not mid: continue
            eid = mid.group(1)
            cur = pic.group(1) if pic else ''
            hidden = bool(re.search(r'^\s*hidden\s*=\s*yes', b, re.M))
            missing = bool(cur) and cur not in known and cur not in PLACEHOLDERS
            reuse = (directive == 'reuse')
            temp = (cur in PLACEHOLDERS) or missing or reuse
            if not show_all and not temp: continue
            t = clean(loc.get(eid + '.t', ''))
            d = clean(loc.get(eid + '.d', '') or loc.get(eid + '.d_full', ''))
            themes, cands = suggest(t, d, tfr, allgfx, ours)
            if not t and not d:
                themes = ['нет текста у нас (служебное событие TFR, картинка не важна)']
            elif hidden:
                themes = ['скрытое событие'] + themes
            rows.append(dict(file=base, id=eid, kind=kind, title=t, desc=d, cur=cur, missing=missing, reuse=reuse,
                             orig=(eid in tfr_events), hidden=hidden,
                             temp=temp, themes=themes, cands=cands))
    # сохранить ручные колонки «Решение» и «Статус» (по ID события)
    decided, status = {}, {}
    if os.path.exists(out):
        for line in read(out).split('\n'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            m = re.match(r'`([\w\.]+)`$', cells[0]) if cells and len(cells) >= 7 else None
            if not m: continue
            if cells[6]: decided[m.group(1)] = cells[6]
            if len(cells) >= 9 and cells[8]: status[m.group(1)] = cells[8]
    by = collections.OrderedDict()
    for r in sorted(rows, key=lambda r: (r['hidden'], r['orig'])):
        pre = 'Скрытые (hidden = yes), картинка не видна: ' if r['hidden'] else ('Оригинал TFR: ' if r['orig'] else '')
        by.setdefault(pre + r['file'], []).append(r)
    L = ['# ART_MAP.md - карта картинок событий', '',
         'Генерируется `python3 _tools/art_map.py` (темы подбора - `_tools/art_themes.py`). '
         'Колонка «Решение» заполняется вручную и сохраняется при перезапуске. '
         'Кандидаты: **наш** - спрайт из `interface/UKR_event_pictures.gfx`; **TFR** - готовое попадание по теме; '
         '**TFR\\*** - совпадение по словам в имени (слабее, смотреть превью). '
         'Прежде чем ставить картинку, проверить её в игре: ни имена, ни этот файл не заменяют превью.', '',
         '**Своя картинка (снимок из прессы и т. п.):** сохранить в `gfx/event_pictures/` под именем из колонки «Имя файла» (PNG, **500x250**, пропорция 2:1), '
         'дописать спрайт `GFX_UKR_<имя без UKR_ и .png>` в `interface/UKR_event_pictures.gfx` и поставить его в `picture =` события. '
         '**Статус** (вручную, сохраняется при перезапуске): `найдено` - снимок выбран; `обработано` - обрезан, фильтр общего стиля, лежит в `gfx/event_pictures/`; '
         '`в моде` - спрайт описан и стоит в событии. Если файл с таким именем уже лежит в `gfx/event_pictures/`, статус «в моде» ставится автоматически. '
         'Для скрытых и служебных событий имя файла `-` (картинка не нужна). '
         'Событие с временной картинкой из уже существующего спрайта помечается в коде строкой `# art: reuse` над `country_event` и попадает в таблицу '
         '(колонка «Сейчас» - `(временная, чужая)`); строка `# art: -` означает, что картинка не нужна (событие страны-ответчика), и в таблицу такое событие не попадает.', '']
    n = sum(1 for r in rows if r['temp'])
    nm = sum(1 for r in rows if r['missing'])
    no = sum(1 for r in rows if r['orig'] and not r['hidden'])
    nh = sum(1 for r in rows if r['hidden'])
    nr = sum(1 for r in rows if r.get('reuse'))
    L += ['Событий с временной картинкой: **%d** (из них спрайт не определён нигде: **%d**; оригиналы TFR: %d; скрытые, картинка не видна: %d; временные из существующих спрайтов, `# art: reuse`: %d); в таблице: %d.' % (n, nm, no, nh, nr, len(rows)),
          'Заглушка `GFX_report_event_ukrainian_civil_war` не найдена ни в индексе TFR, ни у нас: возможно, ванильный спрайт [ПРОВЕРИТЬ в игре, нет ли пустой рамки]. '
          '«Нет спрайта!» - картинка точно нигде не определена, в игре будет пустая рамка.', '']
    for f, rs in by.items():
        L += ['## %s (%d)' % (f, len(rs)), '',
              '| ID | Заголовок | Контекст | Сейчас | Темы | Кандидаты | Решение | Имя файла | Статус |', '|---|---|---|---|---|---|---|---|---|']
        for r in rs:
            ctx = r['desc'][:140].replace('|', '/') + ('...' if len(r['desc']) > 140 else '')
            cur = '`%s`' % r['cur'] if r['cur'] else '-'
            if r['missing']: cur += ' (**нет спрайта!**)'
            elif r.get('reuse'): cur += ' (временная, чужая)'
            elif r['temp']: cur += ' (заглушка)'
            cands = '<br>'.join('`%s` (%s)' % (s, w) for s, w, _ in r['cands']) or '-'
            skip = r['hidden'] or not (r['title'] or r['desc'])
            fname = '-' if skip else file_name(r['id'])
            st = status.get(r['id'], '')
            if not st and not skip and os.path.exists(os.path.join(ROOT, 'gfx', 'event_pictures', fname)):
                st = 'в моде'
            L.append('| `%s` | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                r['id'], r['title'].replace('|', '/'), ctx, cur, ', '.join(r['themes']) or '-', cands,
                decided.get(r['id'], '').replace('|', '/'), '`%s`' % fname if not skip else '-', st))
        L.append('')
    icons = icon_rows(loc)
    if icons:
        L += ['## Значки решений и духов (временные, чужие)', '',
              'Решение: PNG **45x45** в `gfx/interface/decisions/UKR/<имя>.png`, спрайт `GFX_decision_<ключ>` в `interface/UKR_decisions.gfx`, '
              'в решении `icon = GFX_decision_<ключ>`. Дух: PNG **68x68** в `gfx/interface/ideas/UKR/<имя>.png`, спрайт `GFX_idea_<ключ>` в `interface/UKR_ideas.gfx`, '
              'в идее `picture = <ключ>` (без `GFX_idea_`). Статус и решение вносятся вручную и сохраняются при перезапуске; если файл с таким именем уже лежит в папке, '
              'статус «в моде» ставится автоматически. Урезанная версия духа (`_lim`) использует тот же значок.', '',
              '| ID | Название | Что изобразить | Сейчас | Темы | Кандидаты | Решение | Имя файла | Статус |', '|---|---|---|---|---|---|---|---|---|']
        for kind, key, name, short, cur, folder, size, has_lim in icons:
            fname = '%s.png' % key
            st = status.get(key, '')
            if not st and os.path.exists(os.path.join(ROOT, folder, fname)):
                st = 'в моде'
            kind_ru = 'решение' if kind == 'decision' else 'дух'
            what = short.replace('|', '/') + (' (общий значок с `_lim`)' if has_lim else '')
            L.append('| `%s` | %s (%s) | %s | `%s` (чужой) | - | - | %s | `%s/%s` (%s) | %s |' % (
                key, name.replace('|', '/'), kind_ru, what, cur, decided.get(key, '').replace('|', '/'), folder, fname, size, st))
        L.append('')
    open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(L))
    print('событий в карте: %d (с временной картинкой %d); без кандидатов (видимые): %d; значков: %d -> %s' % (
        len(rows), n, sum(1 for r in rows if not r['cands'] and not r['hidden'] and (r['title'] or r['desc'])), len(icons), os.path.relpath(out, ROOT)))


if __name__ == '__main__':
    main()
