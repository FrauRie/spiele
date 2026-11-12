import re,html,collections
R='/home/claude/spiele/'
old=open(R+'index.html',encoding='utf-8').read()
secs=re.findall(r'<section><h2>(.*?)</h2><div class="grid">(.*?)</div></section>',old,re.S)
data=collections.OrderedDict()
for h,body in secs:
    cards=[]
    for t,rest in re.findall(r'<div class="card"[^>]*>(?:<span class="t">(.*?)</span>|)(.*?)</div>(?=<div class="card"|$)',body,re.S):
        links=re.findall(r'<a class="(\w+)" href="([^"]+)"[^>]*>(.*?)</a>',rest,re.S)
        cards.append((html.unescape(t),links,rest))
    data[html.unescape(h)]=cards
ks=data['Klassenspiele']
# Klassenspiele: Karte = ganzer Link
kb=[b for h,b in secs if h=='Klassenspiele'][0]
kl=[(html.unescape(t),u) for u,t in re.findall(r'<a class="card link" href="([^"]+)"[^>]*><span class="t">(.*?)</span>',kb)]
assert len(kl)==28,len(kl)
DESC={'activity':('Activity','Erklären, zeichnen oder Pantomime – die Klasse rät das Wort.'),
'boss-runde':('Boss-Runde','Probe vor der Lernkontrolle: alle zusammen gegen die Chefin, 3 Level.'),
'buchstaben-pizza':('Buchstaben-Pizza','Kategorie und Buchstabe – wer findet ein passendes Wort?'),
'eis-schmilzt':('Eis schmilzt','Wort schreiben oder Buchstaben raten, bevor das Eis schmilzt.'),
'exit-quiz':('Exit-Quiz','Abschluss am Donnerstag: eine Frage, vier Antworten A–D.'),
'fehler-detektiv':('Fehler-Detektiv','Den Fehler im Satz finden und den Satz richtig schreiben.'),
'satz-chaos':('Satz-Chaos','Die Wörter liegen durcheinander – den Satz richtig schreiben.'),
'vokabelcheck':('Vokabelcheck','Bild sehen, Wort schreiben, selbst kontrollieren.'),
'was-fehlt':('Was fehlt?','Drei Karten offen, eine verdeckt – welche Karte fehlt?'),
'wer-bin-ich':('Wer bin ich?','Drei Sätze als Tipps – wer oder was ist es?')}
einzel=[];zoomA=[];zoomL=[];salat=[]
for t,u in kl:
    d=u.split('/')[1]
    if d=='zoom-bild':
        n=t.replace('Zoom-Bild · ','')
        (zoomA if n.startswith('Alltag') else zoomL).append((n.replace('Alltag · ',''),u))
    elif d=='buchstaben-salat': salat.append((t.replace('Buchstaben-Salat · ',''),u))
    else: einzel.append((DESC[d][0],DESC[d][1],u))
assert len(einzel)==10
e=html.escape
def tile(i,x): return f'<a class="tile c{i%3}" href="{x[2]}" data-s="{e((x[0]+" "+x[1]).lower())}"><b>{e(x[0])}</b><span>{e(x[1])}</span></a>'
def pill(t,u): return f'<a class="row link" href="{u}" data-s="{e(t.lower())}"><span class="t">{e(t)}</span><span class="go" aria-hidden="true">▶</span></a>'
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
n_links=old.count('href="blitzbild/')+old.count('href="spiele/')
page=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Smartboard-Spiele · Frau Rie</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#F1EFEB;--cell:#fff;--ink:#1A1A1A;--muted:#6B655C;--line:#DDD7CE;--orange:#D9690A;--gruen:#07A045;--hell:#CDEBD6;--rosa:#F2A7C3}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:150px}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:Andika,Verdana,sans-serif;font-size:18px;line-height:1.3}}
a{{color:inherit;text-decoration:none}}
.top{{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:2px solid var(--line)}}
.in{{max-width:1240px;margin:auto;padding:0 18px}}
.head{{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between;padding-top:14px}}
h1{{margin:0;font-size:1.7rem;display:flex;align-items:center;gap:12px}}h1:before{{content:"";width:38px;height:6px;border-radius:3px;background:var(--ink)}}
h1 small{{font-size:1rem;color:var(--muted);font-weight:400}}
#q{{font:inherit;padding:9px 14px;border:2px solid var(--line);border-radius:99px;background:#fff;width:min(340px,100%)}}#q:focus{{outline:3px solid var(--orange);border-color:var(--orange)}}
.chips{{display:flex;gap:8px;overflow-x:auto;padding:12px 0 12px;scrollbar-width:none}}.chips::-webkit-scrollbar{{display:none}}
.chip{{flex:none;font:inherit;font-weight:700;border:2px solid var(--line);background:#fff;border-radius:99px;padding:8px 16px;cursor:pointer;color:var(--ink)}}
.chip i{{font-style:normal;font-weight:400;color:var(--muted);margin-left:6px}}
.chip.on{{background:var(--ink);border-color:var(--ink);color:#fff}}.chip.on i{{color:#ddd}}
main{{padding-bottom:50px}}
section{{margin-top:26px}}
h2{{margin:0 0 4px;font-size:1.45rem;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}}
h2 span{{font-size:1rem;font-weight:400;color:var(--muted)}}
h3{{margin:18px 0 8px;font-size:.95rem;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:12px;margin-top:12px}}
.tile{{background:var(--cell);border-radius:16px;padding:16px 18px;border-left:10px solid var(--orange);box-shadow:0 1px 3px #0001;display:flex;flex-direction:column;gap:4px;min-height:96px}}
.tile.c1{{border-left-color:var(--gruen)}}.tile.c2{{border-left-color:var(--rosa)}}
.tile b{{font-size:1.3rem}}.tile span{{color:var(--muted);font-size:.98rem}}
.list{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:8px 12px}}
.row{{background:var(--cell);border-radius:12px;padding:8px 10px 8px 16px;display:flex;justify-content:space-between;align-items:center;gap:10px;min-height:56px;box-shadow:0 1px 2px #0001}}
.row .t small{{display:block;color:var(--muted);font-size:.85rem}}
.lv{{display:flex;gap:6px;flex:none}}
.lvl{{min-width:52px;text-align:center;border-radius:10px;padding:9px 10px;font-size:.95rem;letter-spacing:2px;background:var(--hell);color:#0B5A2A;font-weight:700}}
.lvl.n2{{background:var(--gruen);color:#fff}}
.go{{color:var(--orange);font-size:1.2rem;padding-right:8px}}
.tile:hover,.tile:focus-visible,.row.link:hover,.row.link:focus-visible,.lvl:hover,.lvl:focus-visible{{outline:3px solid var(--orange);outline-offset:1px}}
.hide{{display:none!important}}
#leer{{margin-top:30px;color:var(--muted);font-size:1.1rem}}
footer{{text-align:center;color:var(--muted);font-size:.9rem;padding:10px 0 30px}}
@media (max-width:600px){{body{{font-size:16px}}h1{{font-size:1.35rem}}html{{scroll-padding-top:190px}}.list{{grid-template-columns:1fr}}.tiles{{grid-template-columns:1fr}}.tile{{min-height:0}}}}
</style></head><body>
<div class="top"><div class="in">
<div class="head"><h1>Smartboard-Spiele <small>Frau Rie · AvM</small></h1><input id="q" type="search" placeholder="Suchen … z. B. Wetter" aria-label="Spiel suchen"></div>
<nav class="chips" aria-label="Spielart wählen">
<button class="chip on" data-f="">Alle</button><button class="chip" data-f="klassen">Klassenspiele<i>10</i></button><button class="chip" data-f="zoom">Zoom-Bild<i>12</i></button><button class="chip" data-f="salat">Buchstaben-Salat<i>6</i></button><button class="chip" data-f="blitz">Blitzbild<i>72</i></button>
</nav></div></div>
<main class="in">
<section data-g="klassen"><h2>Klassenspiele <span>je ein Spiel – Inhalte wählt man im Spiel</span></h2>
<div class="tiles">{''.join(tile(i,x) for i,x in enumerate(einzel))}</div></section>
<section data-g="zoom"><h2>Zoom-Bild <span>Ein Bild ist ganz nah. Was ist das?</span></h2>
<div class="sub"><h3>Alltag</h3><div class="list">{''.join(pill(t,u) for t,u in zoomA)}</div></div>
<div class="sub"><h3>Lerneinheiten</h3><div class="list">{''.join(pill(t,u) for t,u in zoomL)}</div></div></section>
<section data-g="salat"><h2>Buchstaben-Salat <span>Die Buchstaben liegen durcheinander. Welches Wort ist das?</span></h2>
<div class="sub"><div class="list" style="margin-top:12px">{''.join(pill(t,u) for t,u in salat)}</div></div></section>
<section data-g="blitz"><h2>Blitzbild <span>Ein Bild blitzt kurz auf. Alle schreiben das Wort. &nbsp;● leichter · ●● mehr Wörter oder schwerer</span></h2>
<div class="sub"><h3>Lerneinheiten</h3><div class="list">{rows(data['Blitzbild · Lerneinheiten'])}</div></div>
<div class="sub"><h3>Alltag</h3><div class="list">{rows(data['Blitzbild · Alltag'],byurl=True)}</div></div>
<div class="sub"><h3>Grammatik</h3><div class="list">{rows(data['Blitzbild · Grammatik'],merge=True)}</div></div>
<div class="sub"><h3>Extra</h3><div class="list">{rows(data['Blitzbild · Extra'],merge=True)}</div></div></section>
<p id="leer" class="hide">Nichts gefunden. Anderes Wort probieren oder oben „Alle“ antippen.</p>
</main>
<footer>Unterrichtsmaterial für den eigenen Unterricht.</footer>
<script>
(function(){{
var q=document.getElementById('q'),chips=[].slice.call(document.querySelectorAll('.chip')),f='';
function zeig(){{
  var v=q.value.trim().toLowerCase(),n=0;
  document.querySelectorAll('section').forEach(function(s){{
    var passt=!f||s.dataset.g===f,da=0;
    s.querySelectorAll('[data-s]').forEach(function(c){{var ok=passt&&(!v||c.dataset.s.indexOf(v)>=0);c.classList.toggle('hide',!ok);if(ok)da++}});
    s.querySelectorAll('.sub').forEach(function(u){{u.classList.toggle('hide',!u.querySelector('[data-s]:not(.hide)'))}});
    s.classList.toggle('hide',!da);n+=da;
  }});
  document.getElementById('leer').classList.toggle('hide',n>0);
}}
chips.forEach(function(c){{c.addEventListener('click',function(){{f=c.dataset.f;chips.forEach(function(x){{x.classList.toggle('on',x===c)}});
  try{{localStorage.setItem('rie_start_filter',f)}}catch(e){{}}zeig();window.scrollTo(0,0)}})}});
q.addEventListener('input',zeig);
try{{var a=localStorage.getItem('rie_start_filter');if(a){{var c=chips.filter(function(x){{return x.dataset.f===a}})[0];if(c){{f=a;chips.forEach(function(x){{x.classList.toggle('on',x===c)}})}}}}}}catch(e){{}}
zeig();
}})();
</script></body></html>
'''
n2=page.count('href="blitzbild/')+page.count('href="spiele/')
assert n2==n_links==101,(n2,n_links)
import os
for u in re.findall(r'href="((?:blitzbild|spiele)/[^"]+)"',page): assert os.path.exists(R+u),u
open(R+'index.html','w',encoding='utf-8').write(page)
print('ok',n2,'Links')
