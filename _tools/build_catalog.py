#!/usr/bin/env python3
# Сборка TFR_CATALOG.md из референсов TFR: python3 _tools/build_catalog.py
# Читает только _reference/*.txt (стандартная библиотека), пишет TFR_CATALOG.md в корень репозитория.
# Таблицы (законы, идеологии, черты, модификаторы, фильтры) строятся автоматически;
# заметки и выводы - в TFR_CHEATSHEET.md (руками). Если в _reference/ появились новые файлы,
# запусти скрипт ещё раз и просмотри diff.
import glob, os, re, sys, collections, statistics

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
REF = os.path.join(ROOT, '_reference')
OUT = os.path.join(ROOT, 'TFR_CATALOG.md')


# ---------- разбор Paradox-скрипта ----------
def tokenize(s):
    s = re.sub(r'#[^\n]*', '', s)
    return re.findall(r'"[^"]*"|[{}=<>]|[^\s{}=<>"]+', s)


def parse(toks, i=0):
    out = []
    while i < len(toks):
        t = toks[i]
        if t == '}':
            return out, i + 1
        if i + 2 < len(toks) and toks[i + 1] in ('=', '<', '>'):
            if toks[i + 2] == '{':
                v, i = parse(toks, i + 3)
                out.append((t, '=', v))
            else:
                out.append((t, toks[i + 1], toks[i + 2]))
                i += 3
        else:
            out.append((None, None, t))
            i += 1
    return out, i


def load(path):
    s = open(path, encoding='utf-8-sig', errors='replace').read()
    return parse(tokenize(s))[0]


def lists(body):
    return [(k, v) for k, _, v in body if isinstance(v, list)]


def scalars(body):
    return {k: v for k, _, v in body if k and isinstance(v, str)}


def walk_values(body, key):
    """Все значения ключа на любой глубине."""
    res = []
    for k, _, v in body:
        if k == key and isinstance(v, str):
            res.append(v)
        if isinstance(v, list):
            res += walk_values(v, key)
    return res


def direct_tags(body):
    """Теги из прямых условий tag/original_tag верхнего уровня и внутри OR (без if/NOT/limit)."""
    res = set()
    for k, _, v in body:
        if k in ('tag', 'original_tag') and isinstance(v, str) and re.match(r'^[A-Z]{3}$', v):
            res.add(v)
        elif k == 'OR' and isinstance(v, list):
            res |= direct_tags(v)
    return res


def avail_summary(b, limit=110):
    """Короткая сводка условий available верхнего уровня (скаляры и NOT со скалярами)."""
    parts = []
    for kk, vv in lists(b):
        if kk != 'available':
            continue
        for k, op, v in vv:
            if k and isinstance(v, str):
                parts.append('%s%s%s' % (k, op if op != '=' else '=', v))
            elif k == 'NOT' and isinstance(v, list):
                inner = ['%s%s%s' % (a, o if o != '=' else '=', c) for a, o, c in v if a and isinstance(c, str)]
                if inner:
                    parts.append('НЕ(%s)' % ', '.join(inner))
    s = '; '.join(parts)
    return s if len(s) <= limit else s[:limit - 3] + '...'


def fnum(x):
    try:
        f = float(x)
        return ('%g' % f)
    except Exception:
        return x


def short_mods(mods, limit=7):
    """Сжимаем модификаторы до «ключ=значение»; tooltip-ключи пропускаем."""
    items = [(k, v) for k, _, v in mods if k and isinstance(v, str) and k != 'custom_modifier_tooltip']
    s = ' '.join('%s=%s' % (k, fnum(v)) for k, v in items[:limit])
    if len(items) > limit:
        s += ' (+%d)' % (len(items) - limit)
    return s


def md(s):
    return str(s).replace('|', '\\|')


out = []
W = out.append

# ---------- заголовок ----------
W('# TFR_CATALOG.md - каталог кода TFR (генерируется)')
W('')
W('Собрано `python3 _tools/build_catalog.py` из `_reference/*.txt`. **Не править руками** - при новых референсах перезапустить скрипт. '
  'Выводы, правила и ограничения - в `TFR_CHEATSHEET.md`; здесь только справочные таблицы: что именно существует в TFR.')
W('')
W('Условные обозначения: **L** = уровень закона (1 - самый «высокий», больший номер - «ниже»); **def** = закон по умолчанию; '
  '**cost** = цена смены в политической силе (у законов развития цены нет, они зависят от шкалы развития); '
  '**[TAG]** = закон доступен только этой стране (по `visible`/`available`/`allowed`). '
  'Страновые законы других стран (SOV, GER, PRC, USB, FAF и т. д.) нам недоступны; смотрим на них как на образец.')
W('')

# ---------- 1. законы ----------
W('## 1. Законы (идеи-законы)')
W('')
cat_files = sorted(glob.glob(os.path.join(REF, '*TFR_laws_*.txt')))
group_of = {}
tags_re = re.compile(r'^[A-Z]{3}$')
for f in cat_files:
    base = os.path.basename(f)
    tree = load(f)
    for k, v in lists(tree):
        if k != 'ideas':
            continue
        for slot, body in lists(v):
            W('### %s' % slot)
            W('')
            W('Файл: `%s`.' % base)
            W('')
            W('| Идея | L | cost | Ограничение | Условие (available) | Эффекты (модификатор) |')
            W('|---|---|---|---|---|---|')
            rows = []
            for name, b in lists(body):
                d = scalars(b)
                tags = set()
                for key in ('allowed', 'visible', 'available'):
                    for kk, vv in lists(b):
                        if kk == key:
                            tags |= direct_tags(vv)
                avail = avail_summary(b)
                mods = []
                for kk, vv in lists(b):
                    if kk == 'modifier':
                        mods = vv
                rows.append((int(d.get('level', 99)) if d.get('level', '99').isdigit() else 99, name,
                             d.get('level', ''), d.get('cost', ''), tags, d.get('default') == 'yes', mods, avail))
            rows.sort(key=lambda r: r[0])
            for _, name, lvl, cost, tags, default, mods, avail in rows:
                lim = ('[%s]' % ','.join(sorted(tags))) if tags else ''
                if not lim:
                    m = re.match(r'^([A-Z]{3})_', name)
                    if m:
                        lim = '[%s]' % m.group(1)
                W('| `%s`%s | %s | %s | %s | %s | %s |' % (name, ' (def)' if default else '', lvl, cost, lim, md(avail), md(short_mods(mods))))
            W('')

# ---------- 2. идеологии ----------
W('## 2. Идеологии и подидеологии')
W('')
W('11 идеологий (партий) - допустимые значения `ideology =` в `add_popularity`, `set_party_name`, `set_politics`. '
  'Подидеология (`types`) задаётся лидеру: `country_leader = { ideology = <подидеология> }`, `promote_character = { ideology = ... }`. '
  'Звёздочка `*` - `can_be_randomly_selected = no` (специальная подидеология: назначается скриптом, случайно не выпадает).')
W('')
ifile = glob.glob(os.path.join(REF, '*TFR_ideologies.txt'))
if ifile:
    for k, v in lists(load(ifile[0])):
        for name, b in lists(v):
            types = []
            for kk, vv in lists(b):
                if kk == 'types':
                    for tn, tb in lists(vv):
                        hid = any(a == 'can_be_randomly_selected' and c == 'no' for a, _, c in tb)
                        types.append(tn + ('*' if hid else ''))
            d = scalars(b)
            ai = [x for x in d if x.startswith('ai_')]
            W('- **`%s`** (%d): %s' % (name, len(types), ', '.join('`%s`' % t for t in types)))
            W('  - ИИ: %s; `war_impact_on_world_tension` = %s' % (', '.join(ai) or '-', d.get('war_impact_on_world_tension', '-')))
    W('')

# ---------- 3. министры и лидеры ----------
W('## 3. Черты (leader_traits)')
W('')
W('Формат: `имя - главные эффекты`. Черты не привязаны к стране в самом определении (`random = no`); ограничения накладывает идея-министр (`allowed`) или персонаж. '
  'Новых имён не придумывать - брать из списка (ограничение «имя должно существовать в TFR», иначе будет ошибка в `error.log`).')
W('')
slot_titles = [
    ('head_minister', 'Глава правительства (`hog_*`, `party_*`)', 7),
    ('economic_minister', 'Министр экономики (`eco_*`)', 7),
    ('foreign_minister', 'Министр иностранных дел (`for_*`)', 7),
    ('interior_minister', 'Министр внутренних дел (`sec_*`)', 7),
    ('intelligence_minister', 'Глава разведки (`int_*`)', 8),
]
skip_keys = {'random', 'ai_will_do', 'sprite', 'slot', 'allowed', 'visible', 'equipment_bonus'}
for slot, title, lim in slot_titles:
    fs = glob.glob(os.path.join(REF, '*TFR_traits_%s.txt' % slot))
    if not fs:
        continue
    W('### %s' % title)
    W('')
    for k, v in lists(load(fs[0])):
        for name, b in lists(v):
            mods = [(a, c) for a, _, c in b if isinstance(c, str) and a not in skip_keys]
            if any(a == 'equipment_bonus' for a, _, _ in b):
                mods.append(('equipment_bonus', '{..}'))
            W('- `%s` - %s' % (name, ' '.join('%s=%s' % (a, fnum(c)) for a, c in mods[:lim]) or '(без эффектов)'))
    W('')

fs = glob.glob(os.path.join(REF, '*TFR_traits_head_of_state.txt'))
if fs:
    W('### Глава государства (`hos_*` и страновые)')
    W('')
    W('Префикс показывает «хозяина» (`usb_` США-Б, `gma_`, `fra_`, `faf_` и т. д.); общие для любой страны - `hos_*`. Эффекты: `stab` = `stability_factor`, '
      '`pp` = `political_power_gain`, `ws` = `war_support_factor`.')
    W('')
    abbr = {'stability_factor': 'stab', 'political_power_gain': 'pp', 'war_support_factor': 'ws'}
    groups = collections.OrderedDict()
    for k, v in lists(load(fs[0])):
        for name, b in lists(v):
            pre = name.split('_')[0].lower()
            pre = pre if pre in ('hos',) else 'другие'
            mods = [(a, c) for a, _, c in b if isinstance(c, str) and a not in skip_keys]
            groups.setdefault(pre, []).append((name, mods))
    for g, items in groups.items():
        W('**%s** (%d):' % ('`hos_*`' if g == 'hos' else 'страновые и прочие', len(items)))
        W('')
        for name, mods in items:
            W('- `%s` - %s' % (name, ' '.join('%s=%s' % (abbr.get(a, a), fnum(c)) for a, c in mods[:5]) or '-'))
        W('')

fs = glob.glob(os.path.join(REF, '*TFR_traits_military_minister.txt'))
if fs:
    W('### Военные советники (армия, авиация, флот, теоретик)')
    W('')
    names = collections.defaultdict(list)
    for k, v in lists(load(fs[0])):
        for name, b in lists(v):
            if name.startswith('army_chief'):
                names['army_chief'].append(name)
            elif name.startswith('air_chief'):
                names['air_chief'].append(name)
            elif name.startswith('navy_chief'):
                names['navy_chief'].append(name)
            elif name.startswith('theorist') or name.endswith('theorist'):
                names['theorist'].append(name)
            else:
                names['другие'].append(name)
    for g, ns in names.items():
        W('- **%s** (%d): %s' % (g, len(ns), ', '.join('`%s`' % n for n in ns)))
    W('')
    W('У советников есть `command_cap_increase`, `experience_gain_*` и множество боевых модификаторов; значения - в самом файле референса.')
    W('')

fs = glob.glob(os.path.join(REF, '*TFR_traits_company.txt'))
if fs:
    W('### Черты компаний (производители техники)')
    W('')
    ns = [name for k, v in lists(load(fs[0])) for name, b in lists(v)]
    W('%d черт: %s' % (len(ns), ', '.join('`%s`' % n for n in ns)))
    W('')

# ---------- 4. модификаторы ----------
W('## 4. Словарь модификаторов (по идеям SOV)')
W('')
ifiles = glob.glob(os.path.join(REF, '*TFR_ideas_SOV.txt'))
if ifiles:
    mod = collections.defaultdict(list)
    for k, v in lists(load(ifiles[0])):
        if k != 'ideas':
            continue
        for cat, ib in lists(v):
            for name, b in lists(ib):
                for kk, vv in lists(b):
                    if kk == 'modifier':
                        for a, _, c in vv:
                            if a and isinstance(c, str):
                                try:
                                    mod[a].append(float(c))
                                except ValueError:
                                    pass
    notes = {
        'stability_factor': 'стабильность (доля; 0.05 = 5%)',
        'political_power_gain': 'прирост политсилы',
        'political_power_factor': 'множитель политсилы',
        'war_support_factor': 'поддержка войны',
        'society_development_monthly': 'шкала «Общество» за месяц',
        'poverty_development_monthly': 'шкала соцзащиты за месяц (плюс = лучше)',
        'industrial_development_monthly': 'шкала промышленности за месяц',
        'military_development_monthly': 'военная шкала за месяц',
        'academic_development_monthly': 'шкала науки за месяц',
        'farming_development_monthly': 'шкала сельхоза за месяц',
        'consumer_goods_factor': 'доля потребительских товаров',
        'personal_value_factor': 'вклад личных расходов в ВВП (см. cheatsheet 9)',
        'business_value_factor': 'вклад бизнеса в ВВП',
        'income_growth_factor': 'рост доходов',
        'party_popularity_stability_factor': 'стабильность от популярности правящей партии',
        'drift_defence_factor': 'защита от дрейфа идеологий',
        'dtg_threshold': 'порог, растёт с уровнем «Общество» (0.3 -> 1.05); смысл [ПРОВЕРИТЬ]',
        'misc_expense': 'постоянный расход, млрд',
        'misc_income': 'постоянный доход, млрд',
        'interest_rate_factor': 'процентная ставка',
        'inflation_monthly': 'инфляция за месяц',
        'monthly_population': 'прирост населения',
        'compliance_growth': 'рост лояльности в оккупации',
        'resistance_growth': 'рост сопротивления в оккупации',
        'resistance_decay': 'спад сопротивления',
        'initiative_factor': 'инициатива',
        'conscription': 'доля призыва (населения)',
        'conscription_factor': 'множитель призыва',
        'weekly_manpower': 'живая сила в неделю',
        'usual_oligarch_influence_monthly': 'SOV: влияние олигархов (механика России)',
        'oligarch_influence_monthly': 'SOV: влияние олигархов (механика России)',
        'red_directors_influence_monthly': 'SOV: влияние «красных директоров»',
        'peoples_entrepreneurs_influence_monthly': 'SOV: влияние народных предпринимателей',
        'disabled_ideas': 'блокирует слот идей (используется SOV в кризисных духах)',
    }
    rows = sorted(mod.items(), key=lambda kv: -len(kv[1]))
    W('Показаны ключи, встретившиеся минимум в 3 идеях; значения: минимум / медиана / максимум. Ключи вида `<идеология>_drift` (дрейф партии), '
      '`<идеология>_acceptance` (принятие идеологии, значения 25-50), `*_laws_cost_factor` (цена смены законов), `*_minister_cost_factor` (цена смены министров) - TFR-специфика.')
    W('')
    W('| Ключ | Встреч | min | медиана | max | Заметка |')
    W('|---|---|---|---|---|---|')
    for k, v in rows:
        if len(v) < 3:
            continue
        W('| `%s` | %d | %s | %s | %s | %s |' % (k, len(v), fnum(min(v)), fnum(statistics.median(v)), fnum(max(v)), notes.get(k, '')))
    W('')
    rare = [k for k, v in rows if len(v) < 3]
    W('Редкие ключи (1-2 раза): %s.' % ', '.join('`%s`' % k for k in sorted(rare)))
    W('')

# ---------- 5. деревья фокусов ----------
W('## 5. Деревья фокусов в референсах: размеры и стоимости')
W('')
W('| Файл | Дерево (id) | Фокусов | Самая частая cost |')
W('|---|---|---|---|')
for f in sorted(glob.glob(os.path.join(REF, '*TFR_national_focus_*.txt'))):
    for k, v in lists(load(f)):
        if k != 'focus_tree':
            continue
        tid = scalars(v).get('id', '?')
        costs = collections.Counter()
        n = 0
        for kk, vv in lists(v):
            if kk == 'focus':
                n += 1
                c = scalars(vv).get('cost')
                if c:
                    costs[c] += 1
        top = ', '.join('%s x%d' % c for c in costs.most_common(3))
        W('| `%s` | `%s` | %d | %s |' % (os.path.basename(f).replace('_referenceTFR_national_focus_', '').replace('.txt', ''), tid, n, top))
W('')

# ---------- 6. фильтры ----------
W('## 6. Фильтры фокусов (`search_filters`)')
W('')
filt = collections.Counter()
decl = set()
for f in sorted(glob.glob(os.path.join(REF, '*TFR_national_focus_*.txt'))):
    s = open(f, encoding='utf-8-sig', errors='replace').read()
    decl |= set(re.findall(r'FOCUS_FILTER_[A-Z_]+', s))
    for k, v in lists(load(f)):
        if k == 'focus_tree':
            for kk, vv in lists(v):
                if kk == 'focus':
                    for k3, v3 in lists(vv):
                        if k3 == 'search_filters':
                            for _, _, z in v3:
                                filt[z] += 1
W('Все встречающиеся в референсах: %s.' % ', '.join('`%s`' % x for x in sorted(decl)))
W('')
W('Использованы в фокусах: %s. Фильтры нужны только для поиска по дереву; у большинства фокусов TFR их нет.' % ', '.join('`%s` x%d' % kv for kv in filt.most_common()))
W('')


# ---------- 7. здания ----------
W('## 7. Типы зданий (`buildings`)')
W('')
W('Допустимые значения `type =` в `add_building_construction` / `add_offsite_building`. `base_cost` - стоимость уровня в единицах производства стройки (больше = дольше).')
W('')
W('| Здание | base_cost | на уровень + | Заметка |')
W('|---|---|---|---|')
for f in sorted(glob.glob(os.path.join(REF, '*buildings.txt'))):
    for k, v in lists(load(f)):
        if k != 'buildings':
            continue
        for name, b in lists(v):
            d = scalars(b)
            note = []
            if d.get('only_costal') == 'yes':
                note.append('только побережье')
            if d.get('is_buildable') == 'no':
                note.append('не строится')
            if name.startswith('landmark_'):
                note.append('достопримечательность')
            W('| `%s` | %s | %s | %s |' % (name, d.get('base_cost', ''), d.get('per_level_extra_cost', ''), ', '.join(note)))
W('')

open(OUT, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('Записано %s (%d строк)' % (OUT, len(out)))
