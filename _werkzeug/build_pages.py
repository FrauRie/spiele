import re,html,json,collections,subprocess,os
R='/home/claude/spiele/'
exec(open('/tmp/work/build_index.py',encoding='utf-8').read().split("e=html.escape")[0].replace("old=open(R+'index.html',encoding='utf-8').read()","old=open('/tmp/work/index_old.html',encoding='utf-8').read()"))
DESC['bingo']=('Bingo','Ohne Ausdrucken: 3 × 3 aufs Whiteboard, das Smartboard zieht die Wörter.')
einzel.insert(1,('Bingo',DESC['bingo'][1],'spiele/bingo/bingo-rufer.html'))
# neu am 12.11.2026: Sortiertafel und „Was sagen die meisten?“ (gebaut mit build_neu.py)
DESC['sortiertafel']=('Sortiertafel','Bildkarten in Spalten ziehen: der/die/das, Singular/Plural, wo?/wohin? – auch als Tafelbild.')
DESC['was-sagen-die-meisten']=('Was sagen die meisten?','Wie Familien-Duell: Welche Antwort ist am häufigsten? Mit fertigen Fragen (Deutschland) oder mit den Antworten der Klasse.')
def nach(titel,neu):
    i=[x[0] for x in einzel].index(titel); einzel.insert(i+1,(DESC[neu][0],DESC[neu][1],'spiele/%s/%s.html'%(neu,neu)))
nach('Satz-Chaos','sortiertafel'); nach('Was fehlt?','was-sagen-die-meisten')
# neu am 12.11.2026: Suchsel (nur ●-Wörter, Bild oder Bild + Wort; Quelle: Suchsel_Generator topics.json/topics2.json)
DESC['suchsel']=('Suchsel','Wörter im Buchstabengitter suchen: 36 Themen, nur ●-Wörter, mit Bild oder mit Bild + Wort.')
nach('Sortiertafel','suchsel')
e=html.escape
def rows(cards,merge=False,byurl=False):
    items=[]
    for t,links,_ in cards: items.append([t,[(u,l) for _,u,l in links]])
    if byurl: items.sort(key=lambda x:x[1][0][0])
    if merge:  # gleiche Datei-Basis (…-n1 / …-n2) in eine Zeile
        out=collections.OrderedDict()
        for t,ls in items:
            k=re.sub(r'-n\d\.html$','',ls[0][0])
            if k in out: out[k][1]+=ls; out[k][2].append(t)
            else: out[k]=[t,list(ls),[t]]
        items=[[v[0],sorted(v[1]),v[2]] for v in out.values()]
    h=''
    for it in items:
        t,ls=it[0],it[1]; alle=' '.join(it[2]) if len(it)>2 else t
        sub=f'<small>●● {e(it[2][1].split(" · ",1)[-1])}</small>' if len(it)>2 and len(it[2])>1 else ''
        b=''.join(f'<a class="lvl n{l.count("●")}" href="{u}" aria-label="{e(t)} Stufe {l.count("●")}">{l}</a>' for u,l in ls)
        h+=f'<div class="row" data-s="{e(alle.lower())}"><span class="t">{e(t)}{sub}</span><span class="lv">{b}</span></div>'
    return h
# ---------- Liste aller Spiele für die Spielstunde ----------
SP=[]
KIND={'activity':'activity','bingo':'bingo','boss-runde':'boss','buchstaben-pizza':'pizza','eis-schmilzt':'eis','exit-quiz':'exit','fehler-detektiv':'fehler','satz-chaos':'satz','vokabelcheck':'vokabel','was-fehlt':'wasfehlt','wer-bin-ich':'wer','sortiertafel':'sortier','was-sagen-die-meisten':'meisten','suchsel':'suchsel'}
for t,d,u in einzel: SP.append(dict(t=t,u=u,k=KIND[u.split('/')[1]],g='Klassenspiele'))
for t,u in zoomA: SP.append(dict(t='Zoom-Bild · '+t,u=u,k='zoom',g='Zoom-Bild'))
for t,u in zoomL: SP.append(dict(t='Zoom-Bild · '+t,u=u,k='zoom',g='Zoom-Bild'))
for t,u in salat: SP.append(dict(t='Buchstaben-Salat · '+t,u=u,k='salat',g='Buchstaben-Salat'))
# neu am 12.11.2026: Blitz! (Dobble) – gebaut mit build_blitz.py, Namen in blitz_namen.json
BZ=json.load(open('/tmp/work/blitz_namen.json',encoding='utf-8'))
bzB=[(t,'spiele/blitz/'+f) for f,(g,t) in BZ.items() if g=='Bild-Blitz']; bzW=[(t,'spiele/blitz/'+f) for f,(g,t) in BZ.items() if g=='Wort-Blitz']
for t,u in bzB: SP.append(dict(t='Blitz! · '+t,u=u,k='dobble',g='Blitz! · Bild-Blitz'))
for t,u in bzW: SP.append(dict(t='Wort-Blitz! · '+t,u=u,k='dobble',g='Blitz! · Wort-Blitz'))
for h in ['Blitzbild · Lerneinheiten','Blitzbild · Alltag','Blitzbild · Grammatik','Blitzbild · Extra']:
    for t,links,_ in data[h]:
        for _,u,l in links: SP.append(dict(t='Blitzbild · '+t.split(' · Wörter nach')[0]+' '+l,u=u,k='blitz',g=h))
TXT={'blitz':['Ein Bild blitzt ganz kurz auf. Alle schreiben das Wort auf ihr Mini-Whiteboard. Danach kommt die Lösung.','Am Start wählen: Spielform, 20 Bilder, Schreibzeit 20 s.'],
'salat':['Die Buchstaben liegen durcheinander. Alle schreiben das richtige Wort auf ihr Mini-Whiteboard.','Am Start „Ganze Klasse“ wählen.'],
'zoom':['Ein Bild ist ganz nah. Was ist das? Alle schreiben einen Tipp. Schritt für Schritt sieht man mehr vom Bild.','Wer richtig getippt hat, dreht das Whiteboard um.'],
'satz':['Die Wörter eines Satzes liegen durcheinander. Alle schreiben den Satz richtig auf. Dann fliegen die Kärtchen an ihren Platz.','Die Stufe ● ist am leichtesten.'],
'fehler':['In einem Satz steckt ein Fehler – oder keiner. Alle schreiben den Satz richtig auf.','Mit „Lösung“ sieht man den Fehler in Rot.'],
'wasfehlt':['Drei Karten liegen offen, eine Karte ist verdeckt. Welche Karte fehlt? Alle schreiben sie auf.',''],
'bingo':['Alle zeichnen 3 × 3 Kästchen und schreiben 9 Wörter hinein. Das Smartboard zieht die Wörter. 3 in einer Reihe: „Bingo!“','Zuerst die Lerneinheit wählen. Dann haben alle Zeit zum Schreiben.'],
'activity':['Eine Person erklärt, zeichnet oder spielt ein Wort vor. Alle anderen schreiben das Wort auf.',''],
'boss':['Die ganze Klasse spielt zusammen gegen die Chefin. Es gibt 3 Level.','Gut als Probe vor der Lernkontrolle.'],
'pizza':['Eine Kategorie und ein Buchstabe: Alle schreiben ein passendes Wort auf.',''],
'eis':['Ein Bild erscheint. Alle schreiben das Wort, bevor das Eis schmilzt.',''],
'exit':['Eine Frage, vier Antworten. Alle schreiben A, B, C oder D auf.',''],
'vokabel':['Ein Bild erscheint. Alle schreiben das Wort und kontrollieren selbst.',''],
'wer':['Drei Sätze sind Tipps. Wer oder was ist es? Alle schreiben ihren Tipp auf.',''],
'sortier':['Unten liegen Bildkarten. Jede Karte kommt in die richtige Spalte, zum Beispiel der, die oder das.','Am Start „Karte für Karte – alle schreiben“ wählen: Alle schreiben die Spalte auf ihr Mini-Whiteboard, dann kommt die Lösung.'],
'meisten':['Viele Menschen haben geantwortet. Welche Antwort ist am häufigsten? Alle schreiben eine Antwort auf ihr Mini-Whiteboard. Dann kommen die Antworten mit der Zahl.','Am Start „Deutschland (fertig)“ wählen – oder „unsere Klasse“ und die Antworten vorher eintragen.'],
'suchsel':['Im Gitter sind Wörter versteckt. Die Bilder helfen. Wer ein Wort findet, zieht mit dem Finger darüber.','Am Smartboard kommt immer eine Person nach vorn. Oder alle spielen am Handy.'],
'dobble':['Zwei Karten haben immer genau ein gleiches Motiv. Wer es zuerst findet, tippt es auf der eigenen Karte an und sagt das Wort laut.','Am Start „Für sich / Erklären“ wählen – oder „Duell“: zwei kommen nach vorn.'],
'pause':['Aufstehen, Fenster auf, etwas trinken. Whiteboards sauber wischen.','']}
BL='blitzbild/extra/alles-gemischt-n2.html'; SA='spiele/buchstaben-salat/buchstaben-salat-gemischt.html'; SC='spiele/satz-chaos/satz-chaos-grammatik.html'
ZO='spiele/zoom-bild/zoom-bild-le0-schulsachen.html'; FD='spiele/fehler-detektiv/fehler-detektiv-grammatik-dienstag.html'; WF='spiele/was-fehlt/was-fehlt-quartett.html'; BI='spiele/bingo/bingo-rufer.html'
P45=[[BL,10],[SC,15],[ZO,10],[BI,10]]; P90=[[BL,10],[SA,15],[SC,15],['pause',5],[ZO,10],[FD,15],[WF,10],[BI,10]]
assert sum(b[1] for b in P45)==45 and sum(b[1] for b in P90)==90
for b in P45+P90: assert b[0]=='pause' or os.path.exists(R+b[0]),b
J=lambda x:json.dumps(x,ensure_ascii=False,separators=(',',':'))
s=open('/tmp/work/stunde_tpl.html',encoding='utf-8').read()
s=s.replace('/*SPIELE*/',J(SP)).replace('/*TXT*/',J(TXT)).replace('/*P45*/',J(P45)).replace('/*P90*/',J(P90))
open(R+'spielstunde.html','w',encoding='utf-8').write(s)
# ---------- Handy-Seite ----------
URL='https://fraurie.github.io/spiele/handy.html'
qr=subprocess.run(['node','-e',"const q=require('/tmp/work/package/qrcode.js')(0,'M');q.addData(process.argv[1]);q.make();console.log(q.createSvgTag({cellSize:4,margin:2,scalable:true}))",URL],capture_output=True,text=True).stdout.strip()
assert qr.startswith('<svg')
hl=[('Bingo · Meine Karte','Tipp den Spielcode von der Tafel ein. Du bekommst 9 Bilder. Hör zu und tipp auf das Bild.','spiele/bingo/bingo-rufer.html')]+[('Buchstaben-Salat · '+t,'Tipp die Buchstaben an und leg das Wort. Wähl am Start „Allein“.',u) for t,u in salat]+[('Suchsel','Such die Wörter im Gitter. Zieh mit dem Finger über das Wort.','spiele/suchsel/suchsel.html')]+[('Sortiertafel','Zieh die Karten in die richtige Spalte. Oder: Tipp die Karte an, dann die Spalte.','spiele/sortiertafel/sortiertafel.html'),('Vokabelcheck','Sieh das Bild, schreib das Wort, kontrollier selbst.','spiele/vokabelcheck/vokabelcheck.html')]
# neu am 13.11.2026: Klassenspiele mit Handy-Layout (handy.html-Baustein) – am Handy „Jeder für sich“, Antwort auf Papier oder ins Heft
U={x[0]:x[2] for x in einzel}
hk=[('Boss-Runde','Spiel gegen die Chefin. Schreib die Antwort auf Papier. Dann tipp auf „Lösung“.'),
 ('Exit-Quiz','Tipp auf A, B, C oder D. Du siehst sofort, ob es richtig ist.'),
 ('Fehler-Detektiv','Im Satz ist ein Fehler. Schreib den Satz richtig auf Papier.'),
 ('Satz-Chaos','Die Wörter sind durcheinander. Schreib den Satz richtig auf Papier.'),
 ('Wer bin ich?','Lies die Sätze. Wer oder was ist das? Schreib deinen Tipp auf.'),
 ('Was fehlt?','Eine Karte ist verdeckt. Welche Karte fehlt? Schreib sie auf.'),
 ('Eis schmilzt','Schreib das Wort, bevor das Eis schmilzt.'),
 ('Buchstaben-Pizza','Kategorie und Buchstabe: Schreib ein passendes Wort auf.')]
hk=[(t,d,U[t]) for t,d in hk]
chips=lambda L:''.join(f'<a class="chip" href="{u}">{e(t)}</a>' for t,u in L)
hgr=[('Zoom-Bild','Ein Bild ist ganz nah. Was ist das? Schreib deinen Tipp auf.',zoomA+zoomL),
 ('Blitz!','Zwei Karten haben ein gleiches Bild. Finde es und tipp es an.',bzB),
 ('Wort-Blitz!','Zwei Karten haben ein gleiches Wort. Finde es und tipp es an.',bzW)]
CSS_HEAD='''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>%s</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&display=swap" rel="stylesheet">'''
handy=CSS_HEAD%'Spiele für das Handy · Frau Rie'+f'''<style>
:root{{--bg:#F1EFEB;--ink:#1A1A1A;--muted:#6B655C;--line:#DDD7CE;--orange:#D9690A;--gruen:#07A045;--rosa:#F2A7C3}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font-family:Andika,Verdana,sans-serif;font-size:18px;line-height:1.3}}a{{color:inherit;text-decoration:none}}
.in{{max-width:760px;margin:auto;padding:18px 16px 50px}}h1{{margin:0 0 4px;font-size:1.7rem;display:flex;align-items:center;gap:12px}}h1:before{{content:"";width:38px;height:6px;border-radius:3px;background:var(--ink)}}
p.l{{color:var(--muted);margin:0 0 16px}}.tiles{{display:grid;gap:12px}}
.tile{{background:#fff;border-radius:16px;padding:16px 18px;border-left:10px solid var(--orange);box-shadow:0 1px 3px #0001;display:flex;flex-direction:column;gap:4px}}
.tile:nth-child(3n+2){{border-left-color:var(--gruen)}}.tile:nth-child(3n){{border-left-color:var(--rosa)}}.tile b{{font-size:1.25rem}}.tile span{{color:var(--muted)}}
.qr{{background:#fff;border-radius:16px;padding:18px;margin-top:22px;display:flex;gap:18px;align-items:center;flex-wrap:wrap}}.qr svg{{width:210px;height:210px}}.qr b{{font-size:1.2rem}}
.gr{{background:#fff;border-radius:16px;padding:16px 18px;border-left:10px solid var(--gruen);box-shadow:0 1px 3px #0001}}.gr b{{font-size:1.25rem}}.gr p{{margin:4px 0 10px;color:var(--muted)}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}.chip{{background:var(--bg);border-radius:99px;padding:6px 12px;font-size:.95rem;font-weight:700}}
h2{{font-size:1.3rem;margin:26px 0 4px}}
.zur{{display:inline-block;margin-top:18px;font-weight:700;background:#fff;border-radius:99px;padding:8px 16px;border:2px solid var(--line)}}
@media (max-width:600px){{.qr{{display:none}}}}
</style></head><body><div class="in"><h1>Spiele für das Handy</h1><p class="l">Diese Spiele kannst du allein spielen.</p>
<div class="tiles">{''.join(f'<a class="tile" href="{u}"><b>{e(t)}</b><span>{e(d)}</span></a>' for t,d,u in hl)}</div>
<h2>Klassenspiele – auch am Handy</h2><p class="l">Am Handy ist „Jeder für sich“ schon gewählt. Du brauchst Papier oder dein Heft.</p>
<div class="tiles">{''.join(f'<a class="tile" href="{u}"><b>{e(t)}</b><span>{e(d)}</span></a>' for t,d,u in hk)}{''.join(f'<div class="gr"><b>{e(t)}</b><p>{e(d)}</p><div class="chips">{chips(L)}</div></div>' for t,d,L in hgr)}</div>
<div class="qr">{qr}<div><b>Mit dem Handy öffnen</b><br>Scann den Code mit der Kamera.<br><span style="color:var(--muted)">fraurie.github.io/spiele/handy.html</span></div></div>
<a class="zur" href="index.html">← alle Spiele</a></div></body></html>
'''
for t,d,u in hl+hk+[(t,'',u) for _,_,L in hgr for t,u in L]: assert os.path.exists(R+u),u
open(R+'handy.html','w',encoding='utf-8').write(handy)
# ---------- Startseite ----------
def tile(i,x): return f'<a class="tile c{i%3}" href="{x[2]}" data-id="{x[2]}" data-s="{e((x[0]+" "+x[1]).lower())}"><b>{e(x[0])}</b><span>{e(x[1])}</span></a>'
def pill(t,u,pre): return f'<a class="row link" href="{u}" data-id="{u}" data-n="{e(pre+" · "+t)}" data-s="{e(t.lower())}"><span class="t">{e(t)}</span><span class="go" aria-hidden="true">▶</span></a>'
def rows2(cards,**kw):
    h=rows(cards,**kw)
    def fix(m):
        first=re.search(r'href="([^"]+)"',m.group(0)).group(1); t=re.search(r'<span class="t">(.*?)(?:<small>|</span>)',m.group(0)).group(1)
        return m.group(0).replace('<div class="row" ',f'<div class="row" data-id="{first}" data-n="Blitzbild · {t}" ',1)
    return re.sub(r'<div class="row" .*?</span></div>',fix,h)
page=open('/tmp/work/index_new_tpl.html',encoding='utf-8').read()
page=(page.replace('/*TILES*/',''.join(tile(i,x) for i,x in enumerate(einzel)))
 .replace('/*ZA*/',''.join(pill(t,u,'Zoom-Bild') for t,u in zoomA)).replace('/*ZL*/',''.join(pill(t,u,'Zoom-Bild') for t,u in zoomL)).replace('/*BZB*/',''.join(pill(t,u,'Blitz!') for t,u in bzB)).replace('/*BZW*/',''.join(pill(t,u,'Wort-Blitz!') for t,u in bzW)).replace('/*SA*/',''.join(pill(t,u,'Buchstaben-Salat') for t,u in salat))
 .replace('/*BLE*/',rows2(data['Blitzbild · Lerneinheiten'])).replace('/*BAL*/',rows2(data['Blitzbild · Alltag'],byurl=True)).replace('/*BGR*/',rows2(data['Blitzbild · Grammatik'],merge=True)).replace('/*BEX*/',rows2(data['Blitzbild · Extra'],merge=True)))
n=len(set(re.findall(r'href="((?:blitzbild|spiele)/[^"]+)"',page)))
assert n==134,n
for u in re.findall(r'href="([^"#]+\.html)"',page): assert os.path.exists(R+u),u
open(R+'index.html','w',encoding='utf-8').write(page); print('Seiten gebaut:',len(SP),'Spiele in der Auswahl,',n,'Links auf der Startseite')
