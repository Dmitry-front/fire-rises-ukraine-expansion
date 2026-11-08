# Генератор common/scripted_effects/UKR_mio_pillar_effects.txt и ключей UKR_mio_hook_*_tt / UKR_mio_pillar_tt_* в
# localisation/*/UKR_defense_industry_l_*.yml (сессия 20, PROPOSAL_concerns.md 8.1). Запуск: python3 _tools/gen_mio_pillar.py
# Перезапись безопасна: ключи этих имён заменяются, остальные не трогаются. Решения и фокусы скрипт не правит.
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORGS = {  # короткое имя: (id организации, клан, T, L, N, ru-имя, en-имя)
 'malyshev':   ('UKR_malyshev_organization','met', 0,1,0,'Завод имени Малышева','Malyshev Plant'),
 'armor_repair':('UKR_armor_repair_organization','met',0,1,0,'Бронетанковые ремонтные заводы','Armour Repair Plants'),
 'artillery_works':('UKR_artillery_works_organization','met',0,1,1,'Артиллерийские заводы','Artillery Works'),
 'drone_cluster':('UKR_drone_cluster_organization','priv',1,0,0,'Оборонный кластер БПЛА','UAV Defence Cluster'),
 'radio_electronics':('UKR_radio_electronics_organization','priv',1,0,0,'Радиоэлектроника','Radio-Electronics'),
 'sea_drones':('UKR_mykolaiv_yard_organization','priv',1,0,0,'Верфи и морские дроны','Shipyards and Sea Drones'),
 'kraz':('UKR_kraz_organization','gas',0,0,1,'КрАЗ','KrAZ'),
 'fort':('UKR_drone_cluster_organization','gas',0,0,1,'Форт и кластер БПЛА','Fort and UAV Cluster'),
 'antonov':('UKR_antonov_organization','sec',0,1,0,'Антонов','Antonov'),
 'motor_sich':('UKR_motor_sich_organization','sec',0,1,0,'Мотор Сич','Motor Sich'),
 'aircraft_repair':('UKR_motor_sich_organization','sec',0,1,0,'Мотор Сич и авиаремонт','Motor Sich and Aircraft Repair'),
 'mykolaiv_yard':('UKR_mykolaiv_yard_organization','sec',0,1,0,'Николаевские верфи','Mykolaiv Shipyards'),
 'luch':('UKR_artillery_works_organization','sec',1,0,1,'Артём, Луч и Южное','Artem, Luch and Pivdenne'),
}
# хуки фокусов: (опора, фокус) -> [(короткое имя, funds, size)]
HOOKS = [
 ('t','UKR_t_drone_army',[('drone_cluster',300,1),('sea_drones',150,0)]),
 ('t','UKR_t_cyber_troops',[('radio_electronics',250,1)]),
 ('t','UKR_t_digital_mobilization',[('sea_drones',200,0),('luch',150,0)]),
 ('l','UKR_l_oligarch_audit',[('armor_repair',150,0),('aircraft_repair',150,0)]),
 ('l','UKR_l_strategic_sectors',[('motor_sich',300,1),('antonov',300,1)]),
 ('l','UKR_l_army_not_for_oligarchs',[('malyshev',250,1),('artillery_works',200,0)]),
 ('o','UKR_ol_procurement',[('antonov',60,0),('motor_sich',60,0),('aircraft_repair',60,0),('mykolaiv_yard',60,0),('luch',60,0)]),
 ('o','UKR_ol_clan_industry',[('malyshev',100,0),('armor_repair',100,0),('artillery_works',100,0)]),
 ('o','UKR_ol_mobilization_reserve',[('kraz',100,0),('fort',100,0),('drone_cluster',70,0),('radio_electronics',70,0),('sea_drones',70,0)]),
 ('n','UKR_np_army_artels',[('fort',250,1),('kraz',100,0)]),
 ('n','UKR_np_army_arms',[('artillery_works',250,1),('luch',150,0)]),
 ('n','UKR_np_ethnic_economy',[('kraz',200,1),('malyshev',100,0)]),
]
WIN_FUNDS = 100
# Девять организаций после объединения (08.11.2026): имя в подсказках по id организации
ORG_NAME = {
 'UKR_malyshev_organization':('Завод имени Малышева','Malyshev Plant'),
 'UKR_armor_repair_organization':('Бронетанковые заводы','Armoured Plants'),
 'UKR_kraz_organization':('КрАЗ','KrAZ'),
 'UKR_drone_cluster_organization':('Форт и кластер БПЛА','Fort and UAV Cluster'),
 'UKR_antonov_organization':('Антонов','Antonov'),
 'UKR_motor_sich_organization':('Мотор Сич и авиаремонт','Motor Sich and Aircraft Repair'),
 'UKR_mykolaiv_yard_organization':('Верфи и морские дроны','Shipyards and Sea Drones'),
 'UKR_artillery_works_organization':('Артём, Луч и Южное','Artem, Luch and Pivdenne'),
 'UKR_radio_electronics_organization':('Радиоэлектроника','Radio-Electronics'),
}
def agg(lst):
    # складывает funds и размер по организациям (несколько программ могут вести в одну организацию)
    d={}
    for sname,f,sz in lst:
        oid=ORGS[sname][0]
        a=d.setdefault(oid,[0,0]); a[0]+=f; a[1]=max(a[1],sz)
    return [(oid,f,sz) for oid,(f,sz) in d.items()]
PILLARS = {'t':'UKR_pillar_chosen_technocrats','l':'UKR_pillar_chosen_left','o':'UKR_pillar_chosen_oligarchs','n':'UKR_pillar_chosen_nationalists'}

out=[]
out.append("""# Связка украинских организаций MIO с опорами блока 3 (PROPOSAL_concerns.md, раздел 8.1).
# Файл генерируется скриптом; руками правят значения, тексты и ключи локализации держат в паре.
# 1) UKR_mio_hook_<фокус>: награда фокуса-крючка опоры (funds и размер организаций), вызывается из completion_reward.
# 2) UKR_mio_pillar_window_<имя> / UKR_mio_pillar_window_tt_<имя>: бонус опоры при завершении программы окна
#    «Оборонная промышленность» (remove_effect и подсказка в complete_effect решения UKR_mio_*).
# Все mio:-эффекты обёрнуты в has_dlc = "Arms Against Tyranny": без DLC организаций нет.
# Кланы-владельцы (абстракция мода, не утверждение о реальной собственности): met - Малышева, бронетанковые заводы, артиллерия;
# priv - БПЛА, радиоэлектроника, морские дроны; gas - КрАЗ, Форт; sec - Антонов, Мотор Сич, авиаремонт, верфи, Луч.
""")
for p,focus,lst in HOOKS:
    out.append(f"UKR_mio_hook_{focus[4:]} = {{\n\tif = {{\n\t\tlimit = {{ has_dlc = \"Arms Against Tyranny\" }}")
    out.append(f"\t\tcustom_effect_tooltip = UKR_mio_hook_{focus[4:]}_tt")
    out.append("\t\thidden_effect = {")
    for oid,f,sz in agg(lst):
        out.append(f"\t\t\tmio:{oid} = {{")
        out.append(f"\t\t\t\tadd_mio_funds = {f}")
        if sz: out.append(f"\t\t\t\tadd_mio_size = {sz}")
        out.append("\t\t\t}")
    out.append("\t\t}\n\t}\n}\n")
for s,(oid,clan,T,L,N,ru,en) in ORGS.items():
    out.append(f"# {ru}: клан {clan}")
    out.append(f"UKR_mio_pillar_window_{s} = {{\n\tif = {{\n\t\tlimit = {{ has_dlc = \"Arms Against Tyranny\" }}")
    flags=[('t',T),('l',L),('n',N),('o',1)]
    for p,on in flags:
        if not on: continue
        lim = f"has_country_flag = {PILLARS[p]}"
        if p=='o': lim += "\n\t\t\t\thas_country_flag = UKR_ol_vertical_done"
        out.append(f"\t\tif = {{\n\t\t\tlimit = {{\n\t\t\t\t{lim}\n\t\t\t}}")
        out.append(f"\t\t\tmio:{oid} = {{\n\t\t\t\tadd_mio_funds = {WIN_FUNDS}\n\t\t\t}}")
        if p=='l': out.append("\t\t\tadd_stability = 0.01")
        if p=='n': out.append("\t\t\tadd_war_support = 0.01")
        if p=='o':
            out.append(f"\t\t\thidden_effect = {{\n\t\t\t\tset_temp_variable = {{ UKR_ol_amt = 8 }}\n\t\t\t\tUKR_ol_claim_{clan} = yes\n\t\t\t\tset_temp_variable = {{ UKR_ol_sh = 1 }}\n\t\t\t\tUKR_ol_share_{clan} = yes\n\t\t\t}}")
        out.append("\t\t}")
    out.append("\t}\n}\n")
    out.append(f"UKR_mio_pillar_window_tt_{s} = {{\n\tif = {{\n\t\tlimit = {{ has_dlc = \"Arms Against Tyranny\" }}")
    for p,on in flags:
        if not on: continue
        lim = f"has_country_flag = {PILLARS[p]}"
        if p=='o': lim += "\n\t\t\t\thas_country_flag = UKR_ol_vertical_done"
        out.append(f"\t\tif = {{\n\t\t\tlimit = {{\n\t\t\t\t{lim}\n\t\t\t}}\n\t\t\tcustom_effect_tooltip = UKR_mio_pillar_tt_{p}{'_'+clan if p=='o' else ''}\n\t\t}}")
    out.append("\t}\n}\n")
open(os.path.join(ROOT,'common/scripted_effects/UKR_mio_pillar_effects.txt'),'w',encoding='utf-8',newline='').write("\n".join(out))

# локализация
ru=[];en=[]
def add(k,r,e): ru.append(f' {k}:0 "{r}"'); en.append(f' {k}:0 "{e}"')
nm=lambda s,i:ORGS[s][5+i]
for p,focus,lst in HOOKS:
    key=f"UKR_mio_hook_{focus[4:]}_tt"
    def fmt(i):
        parts=[]
        for oid,f,sz in agg(lst):
            parts.append(f"{ORG_NAME[oid][i]} §G+{f}§!"+((" (размер +1)" if i==0 else " (size +1)") if sz else ""))
        return "; ".join(parts)
    add(key,"Финансирование организаций: "+fmt(0),"Organisation funding: "+fmt(1))
add('UKR_mio_pillar_tt_t',"Опора технократов: организация получит ещё §G100§! ед. финансирования","Technocrat pillar: the organisation will receive another §G100§! funds")
add('UKR_mio_pillar_tt_l',"Опора левых: организация получит ещё §G100§! ед. финансирования, стабильность §G+1%§!","Left pillar: the organisation will receive another §G100§! funds, stability §G+1%§!")
add('UKR_mio_pillar_tt_n',"Опора националистов: организация получит ещё §G100§! ед. финансирования, поддержка войны §G+1%§!","Nationalist pillar: the organisation will receive another §G100§! funds, war support §G+1%§!")
clans={'met':('Металл и энергетика','Metal and Energy'),'priv':('Приват','Privat'),'gas':('Газ и химия','Gas and Chemicals'),'sec':('Силовой круг','Security Circle')}
for c,(r,e) in clans.items():
    add(f'UKR_mio_pillar_tt_o_{c}',f"Опора олигархов: организация получит ещё §G100§! ед. финансирования; клан «{r}»: претензии §R+8§!, доля §G+1§!",f"Oligarch pillar: the organisation will receive another §G100§! funds; clan \"{e}\": claims §R+8§!, share §G+1§!")
for lang,lines in (('russian',ru),('english',en)):
    p=os.path.join(ROOT,f'localisation/{lang}/UKR_defense_industry_l_{lang}.yml')
    raw=open(p,'rb').read().decode('utf-8-sig').rstrip('\n')
    # убрать прежние версии ключей
    keys={l.split(':')[0] for l in lines}
    kept=[l for l in raw.split('\n') if l.split(':')[0] not in keys]
    open(p,'wb').write(b'\xef\xbb\xbf'+("\n".join(kept+lines)+"\n").encode('utf-8'))
