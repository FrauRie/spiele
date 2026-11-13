# Setzt den Handy-Baustein (handy.html) in alle Spiele ein oder erneuert ihn (13.11.2026).
# Er steht direkt vor dem Knopf-Baustein und bekommt pro Datei den Spielnamen (data-rie-spiel = Ordnername).
# Außerdem: Blitz! (Dobble) rechnet die Kartengröße am Handy hochkant für Karten untereinander.
# Nach jedem Bauskript laufen lassen (danach wie immer build_knoepfe.py) – das Skript ist wiederholbar.
import os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = open(os.path.join(R, '_werkzeug', 'handy.html'), encoding='utf-8').read().strip() + '\n'
ALT = re.compile(r'<script>document\.documentElement\.setAttribute\(\'data-rie-spiel\'[^<]*</script>\n<!-- rie-handy v\d+.*?</script>\n', re.S)

# Blitz!: alte Größenberechnung (Karten nebeneinander) -> am Handy hochkant untereinander
BLITZ_HANDY = re.compile(r"function groesse\(\)\{\n  const n=S\.modus==='duell'\?3:2;const vw=innerWidth,vh=innerHeight;\n  const g=vh/100;let k=[^\n]*\n  if\(vw<vh&&vw<=900\)\{/\* rie-handy.*?\}\n", re.S)  # frühere Handy-Fassung
BLITZ_ALT = """function groesse(){
  const n=S.modus==='duell'?3:2;const vw=innerWidth,vh=innerHeight;
  const g=vh/100;const k=Math.min((vw-6*g-(n-1)*3*g)/n, vh*0.66);"""
BLITZ_NEU = """function groesse(){
  const n=S.modus==='duell'?3:2;const vw=innerWidth,vh=innerHeight;
  const g=vh/100;let k=Math.min((vw-6*g-(n-1)*3*g)/n, vh*0.66);
  if(vw<vh&&vw<=900){/* rie-handy: Handy hochkant, Karten untereinander */
    const t=document.getElementById('tisch');const hoehe=(t&&t.clientHeight>100)?t.clientHeight:vh*0.6;
    k=n===3?Math.min((vw-9*g)/2,(hoehe-1.4*g-2*6.8*g)/2):Math.min(vw-6*g,(hoehe-1.4*g-2*6.8*g)/2);}"""

def spielname(p):
    teile = os.path.relpath(p, R).split(os.sep)
    if teile[0] == 'blitzbild': return 'blitzbild'
    if teile[0] == 'spiele' and len(teile) > 2: return teile[1]
    return ''

n = b = 0
for d, _, fs in os.walk(R):
    if '/_werkzeug' in d or '/.git' in d:
        continue
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(d, f)
        name = spielname(p)
        if not name:
            continue
        t = open(p, encoding='utf-8').read()
        t2 = ALT.sub('', t)
        if name == 'blitz' and 'rie-handy: Handy hochkant' in t2:
            t2 = BLITZ_HANDY.sub(lambda m: BLITZ_ALT + '\n', t2)
        if name == 'blitz' and BLITZ_ALT in t2:
            t2 = t2.replace(BLITZ_ALT, BLITZ_NEU); b += 1
        block = "<script>document.documentElement.setAttribute('data-rie-spiel','%s')</script>\n" % name + H
        pos = [t2.find(m) for m in ('<!-- rie-knoepfe', '<!-- rie-ton', '<!-- rie-auto', '<!-- rie-musik') if t2.find(m) >= 0]
        i = min(pos) if pos else t2.rfind('</body>')
        if i < 0:
            print('ohne </body>:', p); continue
        t2 = t2[:i] + block + t2[i:]
        if t2 != t:
            open(p, 'w', encoding='utf-8').write(t2); n += 1
print(n, 'Dateien aktualisiert,', b, 'Blitz-Dateien mit neuer Kartengröße')
