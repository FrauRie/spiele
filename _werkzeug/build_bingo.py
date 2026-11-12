import re,json,base64,io,os
from PIL import Image
R='/home/claude/spiele/'
v=open(R+'spiele/vokabelcheck/vokabelcheck.html',encoding='utf-8').read()
W=json.loads(re.search(r'<script[^>]*id="dW"[^>]*>(.*?)</script>',v,re.S).group(1))
IMG=json.loads(re.search(r'<script[^>]*id="dIMG"[^>]*>(.*?)</script>',v,re.S).group(1))
stand=re.search(r"const STAND_DATEN='([^']*)'",v).group(1)
P={'●':1,'●●':2,'●●●':3}; T={'Nomen':'n','Verb':'v','Adjektiv':'adj'}
out=[]
for w in W:
    if not(w.get('occ') and w['wa'] in T and w['punkte'] in('●','●●') and w.get('bilder')): continue
    b=w['bilder'][0]
    if b.startswith('symbol') or b not in IMG: continue
    im=Image.open(io.BytesIO(base64.b64decode(IMG[b].split(',',1)[1]))).convert('RGB'); im.thumbnail((260,260)); o=io.BytesIO(); im.save(o,'WEBP',quality=74,method=6)
    a=w.get('art') or ''
    d=dict(i=w['id'],w=w['lemma'] if w['wa']=='Nomen' else w['orig'],t=T[w['wa']],b='data:image/webp;base64,'+base64.b64encode(o.getvalue()).decode(),
           o=[[x['datum'],x['le'],x['thema'],P.get(x['punkte'],P[w['punkte']])] for x in w['occ']])
    if a in('der','die','das'): d['a']=a
    out.append(d)
print(len(out),'Wörter')
tpl=open('/tmp/work/bingo_tpl.html',encoding='utf-8').read()
fonts=open('/tmp/work/fonts.css',encoding='utf-8').read()
qr=open('/tmp/work/package/qrcode.js',encoding='utf-8').read()
musik=open('/tmp/work/musik.html',encoding='utf-8').read()
h=tpl.replace('/*FONTS*/',fonts).replace('/*QRLIB*/',qr.replace('</script>','<\\/script>')).replace('/*DATA*/',json.dumps(out,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')).replace('/*STAND*/',stand)
h=h.replace('</body>',musik+'</body>')
os.makedirs(R+'spiele/bingo',exist_ok=True)
open(R+'spiele/bingo/bingo-rufer.html','w',encoding='utf-8').write(h); print(f'{len(h)/1e6:.1f} MB')
