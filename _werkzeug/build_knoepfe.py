# Setzt den Knopf-Baustein (knoepfe.html) in alle Seiten des Repos ein oder erneuert ihn.
# Er steht direkt vor dem Ton-/Automatik-/Musik-Baustein, sonst vor </body>.
import os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = open(os.path.join(R, '_werkzeug', 'knoepfe.html'), encoding='utf-8').read().strip() + '\n'
ALT = re.compile(r'<!-- rie-knoepfe v\d+.*?</script>\n', re.S)
n = 0
for d, _, fs in os.walk(R):
    if '/_werkzeug' in d or '/.git' in d:
        continue
    for f in fs:
        if not f.endswith('.html'):
            continue
        p = os.path.join(d, f)
        t = open(p, encoding='utf-8').read()
        t2 = ALT.sub('', t)
        pos = [t2.find(m) for m in ('<!-- rie-ton', '<!-- rie-auto', '<!-- rie-musik') if t2.find(m) >= 0]
        i = min(pos) if pos else t2.rfind('</body>')
        if i < 0:
            print('ohne </body>:', p); continue
        t2 = t2[:i] + K + t2[i:]
        if t2 != t:
            open(p, 'w', encoding='utf-8').write(t2); n += 1
print(n, 'Dateien aktualisiert')
