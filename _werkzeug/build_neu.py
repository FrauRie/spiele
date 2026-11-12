# Baut die Spiele „Was sagen die meisten?“ und „Sortiertafel“ (Stand 12.11.2026).
# Vorher: Dateien aus _werkzeug nach /tmp/work kopieren. Wörter und Bilder kommen aus spiele/vokabelcheck/vokabelcheck.html (dW, dIMG).
import re,json,base64,io,os
from PIL import Image
R='/home/claude/spiele/'; T='/tmp/work/'
fonts=open(T+'fonts.css',encoding='utf-8').read(); musik=open(T+'musik.html',encoding='utf-8').read()
def schreib(ziel,h):
    assert h.count('</body>')==1
    h=h.replace('</body>',musik+'</body>')
    os.makedirs(os.path.dirname(R+ziel),exist_ok=True)
    open(R+ziel,'w',encoding='utf-8').write(h); print(ziel,f'{len(h)/1e6:.1f} MB')
# ---------- Was sagen die meisten? ----------
schreib('spiele/was-sagen-die-meisten/was-sagen-die-meisten.html',open(T+'meisten_tpl.html',encoding='utf-8').read().replace('/*FONTS*/',fonts))
# ---------- Sortiertafel ----------
# wo? / wohin? – von Hand festgelegt, nur für Orte aus dem Wortschatz: Lemma -> (wo, wohin)
WW={'Schule':('in der Schule','in die Schule'),'Klasse':('in der Klasse','in die Klasse'),'Raum':('im Raum','in den Raum'),'Schulbüro':('im Schulbüro','ins Schulbüro'),
'Hamburg':('in Hamburg','nach Hamburg'),'Mensa':('in der Mensa','in die Mensa'),'Kantine':('in der Kantine','in die Kantine'),'Apotheke':('in der Apotheke','in die Apotheke'),
'Arzt':('beim Arzt','zum Arzt'),'Arztpraxis':('in der Arztpraxis','in die Arztpraxis'),'Praxis':('in der Praxis','in die Praxis'),'Bahnhof':('am Bahnhof','zum Bahnhof'),
'Bäcker':('beim Bäcker','zum Bäcker'),'Bäckerei':('in der Bäckerei','in die Bäckerei'),'Büro':('im Büro','ins Büro'),'Café':('im Café','ins Café'),
'Bibliothek':('in der Bibliothek','in die Bibliothek'),'Bushaltestelle':('an der Bushaltestelle','zur Bushaltestelle'),'Haltestelle':('an der Haltestelle','zur Haltestelle'),
'Einkaufszentrum':('im Einkaufszentrum','ins Einkaufszentrum'),'Firma':('in der Firma','in die Firma'),'Fitnessstudio':('im Fitnessstudio','ins Fitnessstudio'),
'Flughafen':('am Flughafen','zum Flughafen'),'Friseur':('beim Friseur','zum Friseur'),'Geschäft':('im Geschäft','ins Geschäft'),'Hafen':('am Hafen','zum Hafen'),
'Hotel':('im Hotel','ins Hotel'),'Kino':('im Kino','ins Kino'),'Kiosk':('am Kiosk','zum Kiosk'),'Krankenhaus':('im Krankenhaus','ins Krankenhaus'),
'Küche':('in der Küche','in die Küche'),'Lager':('im Lager','ins Lager'),'Markt':('auf dem Markt','auf den Markt'),'Museum':('im Museum','ins Museum'),
'Park':('im Park','in den Park'),'Post':('bei der Post','zur Post'),'Restaurant':('im Restaurant','ins Restaurant'),'Schwimmbad':('im Schwimmbad','ins Schwimmbad'),
'Stadt':('in der Stadt','in die Stadt'),'Strand':('am Strand','an den Strand'),'Supermarkt':('im Supermarkt','in den Supermarkt'),'Tankstelle':('an der Tankstelle','zur Tankstelle'),
'Tierpark':('im Tierpark','in den Tierpark'),'Toilette':('auf der Toilette','auf die Toilette'),'Werkstatt':('in der Werkstatt','in die Werkstatt'),
'Wohnung':('in der Wohnung','in die Wohnung'),'Zimmer':('im Zimmer','ins Zimmer'),'Arbeit':('bei der Arbeit','zur Arbeit'),'Bad':('im Bad','ins Bad'),
'Baustelle':('auf der Baustelle','auf die Baustelle'),'Kirche':('in der Kirche','in die Kirche'),'Moschee':('in der Moschee','in die Moschee'),'Synagoge':('in der Synagoge','in die Synagoge'),
'Imbiss':('im Imbiss','zum Imbiss'),'Wald':('im Wald','in den Wald'),'Meer':('am Meer','ans Meer'),'See':('am See','an den See'),'Fluss':('am Fluss','an den Fluss'),
'Dorf':('im Dorf','ins Dorf'),'Haus':('zu Hause','nach Hause'),'Ausland':('im Ausland','ins Ausland'),'Polizei':('bei der Polizei','zur Polizei'),
'Bauernhof':('auf dem Bauernhof','auf den Bauernhof'),'Parkhaus':('im Parkhaus','ins Parkhaus'),'Parkplatz':('auf dem Parkplatz','auf den Parkplatz'),
'Insel':('auf der Insel','auf die Insel'),'Kasse':('an der Kasse','zur Kasse')}
v=open(R+'spiele/vokabelcheck/vokabelcheck.html',encoding='utf-8').read()
W=json.loads(re.search(r'<script[^>]*id="dW"[^>]*>(.*?)</script>',v,re.S).group(1))
IMG=json.loads(re.search(r'<script[^>]*id="dIMG"[^>]*>(.*?)</script>',v,re.S).group(1))
stand=re.search(r"const STAND_DATEN='([^']*)'",v).group(1)
P={'●':1,'●●':2,'●●●':3}; TY={'Nomen':'n','Verb':'v','Adjektiv':'adj'}
out=[];seen={};ww_da=set()
for w in W:
    if not(w.get('occ') and w['wa'] in TY and w.get('bilder')): continue
    b=w['bilder'][0]
    if b.startswith('symbol') or b not in IMG: continue
    wort=w['lemma'] if w['wa']=='Nomen' else w['orig']
    a=w.get('art') or ''
    key=(wort,w['wa'],a)
    occ=[[x['datum'],x['le'],x['thema'],P.get(x['punkte'],P[w['punkte']])] for x in w['occ']]
    if key in seen:  # gleiches Wort zweimal im Wortschatz: Vorkommen zusammenlegen
        seen[key]['o']+=occ; continue
    im=Image.open(io.BytesIO(base64.b64decode(IMG[b].split(',',1)[1]))).convert('RGB'); im.thumbnail((220,220)); o=io.BytesIO(); im.save(o,'WEBP',quality=72,method=6)
    d=dict(i=w['id'],w=wort,t=TY[w['wa']],b='data:image/webp;base64,'+base64.b64encode(o.getvalue()).decode(),o=occ)
    if w['wa']=='Nomen':
        if w.get('nur_plural'): d['a']='pl'
        elif a in('der','die','das'):
            d['a']=a
            pl=(w.get('plural') or '').strip()
            if pl.startswith('die ') and pl[4:]!=wort and '/' not in pl: d['pl']=pl[4:]
        if wort in WW: d['ww']=list(WW[wort]); ww_da.add(wort)
    seen[key]=d; out.append(d)
print(len(out),'Wörter ·',sum(1 for d in out if d.get('a') in('der','die','das')),'mit Artikel ·',sum(1 for d in out if d.get('pl')),'mit Plural ·',len(ww_da),'Orte')
print('WW ohne Wort im Wortschatz:',sorted(set(WW)-ww_da))
h=open(T+'sortiertafel_tpl.html',encoding='utf-8').read()
h=h.replace('/*FONTS*/',fonts).replace('/*DATA*/',json.dumps(out,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('/*STAND*/',stand)
schreib('spiele/sortiertafel/sortiertafel.html',h)
