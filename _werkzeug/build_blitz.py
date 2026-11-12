# Baut die Blitz!-Spiele (Dobble) fürs Repo: spiele/blitz/*.html
# Quelle: AvM2-26_Material/10_Klassenspiele_Mathe/Klassenspiele/Blitz_Dobble/Smartboard/Blitz_Smartboard_*_Rie_v*.html  -> nach /tmp/work/blitz_src/
# Wort-Blitz Blitzlesen: Wortlisten aus blitz_listen.py (aus Blitz_Generator_Blitzlesen_Rie_v1.py), Grundlage ist die Gegensätze-Datei (Farbwelt ritual).
import os, re, json, glob
W = '/tmp/work/'; R = '/home/claude/spiele/'; OUT = R + 'spiele/blitz/'
os.makedirs(OUT, exist_ok=True)
KNOEPFE = open(W + 'knoepfe.html', encoding='utf-8').read(); TON = open(W + 'ton.html', encoding='utf-8').read(); MUSIK = open(W + 'musik.html', encoding='utf-8').read()

def patch(h):
    old = "function lab(it,plain){"
    assert h.count(old) == 1
    h = h.replace(old, old + "if(D.schwarz)return it.t;if(it.a)return '<span class=\"a-'+it.t+'\">'+it.t+'</span>';")
    old = '<button data-v="erkl">Erklären (1 Karte + Mitte)</button>'
    assert h.count(old) == 1
    h = h.replace(old, '<button data-v="erkl">Für sich / Erklären (1 Karte + Mitte)</button>')
    assert h.count('vh*0.72')==1
    h = h.replace('vh*0.72', 'vh*0.66')   # Platz für lange Aufgabenzeile
    # Knopf-Regeln (12.11.2026): „Einstellungen“ darf „Lösung zeigen“ nicht berühren
    h = h.replace('.mini{position:fixed;right:2vh;bottom:1.2vh;', '.mini{position:fixed;right:2vh;bottom:.3vh;', 1).replace('.unten{display:flex;', '.unten{margin-bottom:1.4vh;display:flex;', 1)
    assert '</body>' in h and 'rie-ton' not in h
    return h.replace('</body>', KNOEPFE + '\n' + TON + '\n' + MUSIK + '\n</body>')

def slug(k): return k.lower().replace('ae', 'ä').replace('ä', 'ae')  # Dateinamen ohne Umlaute
NAMEN = {}   # dateiname -> (Gruppe, Titel)
KOPF = {}
for f in sorted(glob.glob(W + 'blitz_src/Blitz_Smartboard_*_Rie_v*.html')):
    key = re.search(r'Blitz_Smartboard_(.+)_Rie_v\d+\.html', f).group(1)
    h = open(f, encoding='utf-8').read()
    kopf = re.search(r'<p class="sub2">(.*?) · Smartboard</p>', h).group(1)
    titel = re.search(r'<h1>(.*?)</h1>', h).group(1)
    KOPF[key] = kopf
    fn = 'blitz-' + key.lower() + '.html'
    open(OUT + fn, 'w', encoding='utf-8').write(patch(h)); NAMEN[fn] = ('Bild-Blitz', kopf if titel == 'Blitz!' else kopf)

# ---- Wort-Blitz Blitzlesen ----
exec(open(W + 'blitz_listen.py', encoding='utf-8').read())
base = open(W + 'blitz_src/Blitz_Smartboard_Gegensaetze_Rie_v2.html', encoding='utf-8').read()
m = re.search(r'const D=(\{.*?\});const IT=D\.items;', base, re.S); assert m
for key, st in SETS.items():
    items = []
    for w, _ in st['items']:
        t = st['typ'][w]; it = dict(t=w, v=(t == 'v'))
        if t == 'a' and ' ' not in w: it['a'] = True
        items.append(it)
    s1, s2, s3 = [x[1] for x in st['stufen']]
    d = dict(key='wort_' + key, zahl=False, items=items, nivName=['', 'Wörter'] * 2, schwarz=st['schwarz'],
             auf=f'<b>●</b> {s1} &nbsp; <b>●●</b> {s2} &nbsp; <b>●●●</b> {s3}')
    h = base.replace(m.group(0), 'const D=' + json.dumps(d, ensure_ascii=False) + ';const IT=D.items;')
    h = h.replace('Blitz!', 'Wort-Blitz!').replace('Gegensätze', st['titel'])
    h = re.sub(r'(<div class="seg" data-k="niv">\s*).*?(</div>)', r'\1<button data-v="1">nur Wörter</button>\2', h, count=1, flags=re.S)
    fn = 'wort-blitz-' + key.lower() + '.html'
    open(OUT + fn, 'w', encoding='utf-8').write(patch(h)); NAMEN[fn] = ('Wort-Blitz', st['titel'])
json.dump(NAMEN, open(W + 'blitz_namen.json', 'w'), ensure_ascii=False, indent=1)
print(len(NAMEN), 'Blitz-Spiele gebaut')
