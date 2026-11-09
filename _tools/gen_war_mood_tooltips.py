#!/usr/bin/env python3
"""Пересобирает тултипы ступеней военного настроя из определений духов.

Зачем: тултипы ступеней (UKR_HATE_STAGE_N_TOOLTIP, UKR_FATIGUE_STAGE_N_TOOLTIP) раньше были написаны
вручную и разошлись с реальными духами UKR_war_spirit_* (TD-27). Скрипт берёт модификаторы духов из
common/ideas/TFR_ideas_UKR.txt и переписывает в тултипах только списки эффектов. Заголовок и
художественный абзац (первые два блока до "\\n\\n") и хвост "§H..." (если есть) сохраняются.

Запуск (из корня репозитория):
    python3 _tools/gen_war_mood_tooltips.py            # показать, что изменится
    python3 _tools/gen_war_mood_tooltips.py --write    # записать в RU и EN локализацию

После правки модификаторов духов - запустить заново. Новые модификаторы добавляются в LABELS.
Тире (длинное, среднее) и многоточие-символ не используются: шрифт игры показывает их как "?".
"""
import re
import sys

IDEAS = "common/ideas/TFR_ideas_UKR.txt"
LOC = {
    "ru": "localisation/russian/TFR_country_localisation_UKR_l_russian.yml",
    "en": "localisation/english/TFR_country_localisation_UKR_l_english.yml",
}

# модификатор -> (RU, EN, тип). Тип: pct (множитель в процентах), drift (дрейф идеологии, число как есть).
# bad_if_positive: рост значения - это вред для страны.
LABELS = {
    "army_morale_factor": ("Мораль армии", "Army morale", "pct"),
    "war_support_factor": ("Поддержка войны", "War support", "pct"),
    "war_support_weekly": ("Поддержка войны в неделю", "War support per week", "pct"),
    "army_attack_factor": ("Атака армии", "Army attack", "pct"),
    "army_core_defence_factor": ("Защита на своей земле", "Defense in core territory", "pct"),
    "conscription_factor": ("Призыв", "Conscription", "pct"),
    "special_forces_attack_factor": ("Атака спецназа", "Special forces attack", "pct"),
    "stability_factor": ("Стабильность", "Stability", "pct"),
    "stability_weekly": ("Стабильность в неделю", "Stability per week", "pct"),
    "consumer_goods_factor": ("Потребительские товары", "Consumer goods", "pct"),
    "political_power_cost": ("Стоимость политической власти", "Political power cost", "pct"),
    "army_org_factor": ("Организация армии", "Army organization", "pct"),
    "production_factory_efficiency_gain_factor": ("Рост эффективности производства", "Factory efficiency growth", "pct"),
    "mobilization_speed": ("Скорость мобилизации", "Mobilization speed", "pct"),
    "command_power_gain_mult": ("Получение командной власти", "Command power gain", "pct"),
    "surrender_limit": ("Предел капитуляции", "Surrender limit", "pct"),
    # названия идеологий TFR: nationalist = Despotism, fascist = Fascism, social_liberal = Social Liberalism
    "nationalist_drift": ("Ежедневная поддержка Деспотизма", "Daily Despot support", "drift"),
    "fascist_drift": ("Ежедневная поддержка Фашизма", "Daily Fascist support", "drift"),
    "social_liberal_drift": ("Ежедневная поддержка Социал-Либерализма", "Daily Social Liberal support", "drift"),
}
BAD_IF_POSITIVE = {"consumer_goods_factor", "political_power_cost"}

HEAD = {
    "ru": {"good": "§GПоложительные эффекты:§!", "bad": "§RНегативные эффекты:§!", "drift": "§YСдвиг настроений:§!",
           "spirit": "Дух на панели идей: "},
    "en": {"good": "§GPositive effects:§!", "bad": "§RNegative effects:§!", "drift": "§YShift in sentiment:§!",
           "spirit": "Spirit on the ideas panel: "},
}

# ступень -> (ключ тултипа, идея)
STAGES = []
for kind, prefix in (("HATE", "UKR_war_spirit_hate_"), ("FATIGUE", "UKR_war_spirit_fatigue_")):
    for n, lvl in enumerate((0, 25, 50, 75, 100)):
        STAGES.append((f"UKR_{kind}_STAGE_{n}_TOOLTIP", f"{prefix}{lvl}"))


def spirit_modifiers(text, idea):
    """Достаёт блок modifier = { ... } идеи idea из текста TFR_ideas_UKR.txt (с учётом скобок)."""
    m = re.search(r"\b" + re.escape(idea) + r"\s*=\s*\{", text)
    if not m:
        raise SystemExit(f"Идея {idea} не найдена в {IDEAS}")
    i, depth = m.end(), 1
    while depth:
        depth += {"{": 1, "}": -1}.get(text[i], 0)
        i += 1
    body = text[m.end():i - 1]
    mm = re.search(r"\bmodifier\s*=\s*\{([^{}]*)\}", body)
    if not mm:
        return {}
    mods = {}
    for k, v in re.findall(r"([A-Za-z_]+)\s*=\s*(-?[0-9.]+)", re.sub(r"#[^\n]*", "", mm.group(1))):
        mods[k] = float(v)
    return mods


def fmt_pct(v):
    p = round(v * 100, 2)
    s = f"{p:+g}"
    return s + "%"


def fmt_drift(v):
    return f"{v:+g}"


def build_effects(mods, lang):
    good, bad, drift = [], [], []
    for k, v in mods.items():
        if k not in LABELS:
            raise SystemExit(f"Нет подписи для модификатора {k}: добавьте в LABELS ({__file__})")
        ru, en, typ = LABELS[k]
        name = ru if lang == "ru" else en
        if typ == "drift":
            drift.append(f"• {name}: §Y{fmt_drift(v)}§!")
            continue
        is_good = (v > 0) != (k in BAD_IF_POSITIVE)
        (good if is_good else bad).append(f"• {name}: §{'G' if is_good else 'R'}{fmt_pct(v)}§!")
    # В .yml перенос строки - это два символа "\" и "n", а не настоящий перевод строки.
    nl = "\\n"
    out = []
    if good:
        out.append(HEAD[lang]["good"] + nl + nl.join(good))
    if bad:
        out.append(HEAD[lang]["bad"] + nl + nl.join(bad))
    if drift:
        out.append(HEAD[lang]["drift"] + nl + nl.join(drift))
    return out


def spirit_name(loc_text, idea):
    m = re.search(r"^\s*" + re.escape(idea) + r":\d*\s*\"([^\"]*)\"", loc_text, re.M)
    return m.group(1) if m else idea


def main():
    write = "--write" in sys.argv
    ideas_text = re.sub(r"#[^\n]*", "", open(IDEAS, encoding="utf-8-sig").read())
    changed = 0
    for lang, path in LOC.items():
        raw = open(path, encoding="utf-8", newline="").read()
        for key, idea in STAGES:
            m = re.search(r"^( " + key + r":\d*\s*\")((?:[^\"\\]|\\.)*)(\"[^\n]*)$", raw, re.M)
            if not m:
                raise SystemExit(f"Ключ {key} не найден в {path}")
            parts = m.group(2).split("\\n\\n")
            tail = [p for p in parts[2:] if p.startswith("§H")]
            new_parts = parts[:2] + build_effects(spirit_modifiers(ideas_text, idea), lang)
            new_parts.append(HEAD[lang]["spirit"] + "§Y" + spirit_name(raw, idea) + "§!")
            new_parts += tail
            new_text = "\\n\\n".join(new_parts)
            if new_text != m.group(2):
                changed += 1
                if not write:
                    print(f"--- [{lang}] {key}\n{new_text.replace(chr(92) + 'n', chr(10))}\n")
                raw = raw[:m.start(2)] + new_text + raw[m.end(2):]
        if write:
            open(path, "w", encoding="utf-8", newline="").write(raw)
    print(("Записано" if write else "Будет изменено") + f" тултипов: {changed} (из 20)")


if __name__ == "__main__":
    main()
