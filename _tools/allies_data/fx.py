# Конструкторы эффектов для запросов к странам (этап 3, PROPOSAL_war_europe.md 4.1).
# Каждый эффект - кортеж; генератор _tools/gen_allies.py превращает его в код в области UKR.
# Эффекты 'full' - полный пакет; 'part' - частичный: либо явный список, либо 'auto' (половина по правилам gen_allies.half()).


def eq(type_, n, producer):
    """Техника на склад Украины; объём умножается на множитель единства НАТО (UKR_nato_aid_scale)."""
    return ('eq', type_, n, producer)


def money(income, debt):
    """Деньги (ликвидность) и долг в млрд; сумма income умножается на множитель единства НАТО."""
    return ('money', income, debt)


def xp(kind, n):
    """Опыт: kind = army, navy, air."""
    return ('xp', kind, n)


def manpower(n):
    return ('manpower', n)


def mio(org, n):
    """Деньги организации MIO (mio:ORG = { add_mio_funds = N })."""
    return ('mio', org, n)


def idea(name, days, lim=None, lim_days=None):
    """Временный дух; lim - урезанная версия для частичного пакета."""
    return ('idea', name, days, lim, lim_days)


def flag(name):
    """Постоянный флаг страны."""
    return ('flag', name)


def var(name, n):
    """Прибавить к переменной UKR."""
    return ('var', name, n)


def ev(event_id, days):
    """Отправить Украине событие через days дней."""
    return ('ev', event_id, days)


def raw(code):
    """Готовый код (строки с табами относительно блока)."""
    return ('raw', code)


def T(ru, en):
    """Пара текстов RU/EN."""
    return {'ru': ru, 'en': en}
