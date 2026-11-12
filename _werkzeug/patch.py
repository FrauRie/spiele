import re,glob,sys,os
R='/home/claude/spiele/'
MUSIK=open('/tmp/work/musik.html',encoding='utf-8').read()
log=[]
def rep(s,old,new,n=1,f=''):
    c=s.count(old)
    if c!=n: raise SystemExit(f'FEHLER {f}: "{old[:70]}" kommt {c}x vor, erwartet {n}')
    return s.replace(old,new)
def rep_opt(s,old,new): return s.replace(old,new)
def drop_step(s,f):
    """Schritt <b>Zeigen!</b> aus der Anleitung nehmen und die folgenden Schritte neu nummerieren"""
    m=re.search(r'<div class="st"><span class="n">(\d)</span><b>Zeigen!</b>(?:(?!<div).)*?</div>\s*',s,re.S)
    if not m: raise SystemExit('FEHLER '+f+': Schritt Zeigen nicht gefunden')
    n=int(m.group(1)); head=s[:m.start()]; tail=s[m.end():]
    seg=tail[:1500]
    for k in range(n+1,n+5):
        seg=seg.replace(f'<span class="n">{k}</span>',f'<span class="n">{k-1}</span>',1)
    return head+seg+tail[1500:]
def musik(s,f):
    if 'id="rieMusik"' in s: return s
    i=s.rfind('</body>')
    if i<0: raise SystemExit('FEHLER '+f+': kein </body>')
    return s[:i]+MUSIK+s[i:]
def css(s,rule,f):
    i=s.find('</style>')
    return s[:i]+rule+'\n'+s[i:]

def blitzbild(s,f):
    s=rep(s,' Dann heißt es: Zeigen! Danach kommt die Lösung.',' Danach kommt die Lösung.',1,f)
    s=drop_step(s,f)
    s=rep(s,'btns(["✋ Zeigen!","main"],true,false);','btns(["👁 Lösung","main"],true,false);',1,f)
    s=rep(s,'if(r<=0){clearInterval(st.iv);st.iv=null;zeigen()}};','if(r<=0){clearInterval(st.iv);st.iv=null;loesung()}};',1,f)
    s=rep(s,'write:zeigen,zeigen:loesung,reveal:next','write:loesung,zeigen:loesung,reveal:next',1,f)
    return s
def salat(s,f):
    s=rep(s,'dann „Zeigen!“. Mit Teams','dann kommt die Lösung. Mit Teams',1,f)
    s=rep(s,'Zeit pro Wort (dann „Zeigen!“)','Zeit pro Wort (dann Lösung)',1,f)
    s=rep(s,' → „Zeigen!“ → Lösung',' → Lösung',1,f)
    s=rep(s,'btns(["✋ Zeigen!","main"]','btns(["👁 Lösung","main"]',1,f)
    s=rep(s,'function zeigen(){if(st.phase!=="play")return;clearT();st.phase="zeigen";$("zeigen").hidden=false}','function zeigen(){if(st.phase!=="play")return;loesung(true)}',1,f)
    return s
def wasfehlt(s,f):
    s=rep(s,'Dann „Zeigen!“ – und die Karte dreht sich um.','Dann dreht sich die Karte um.',1,f)
    s=rep(s,'Zeit pro Runde (dann „Zeigen!“)','Zeit pro Runde (dann Lösung)',1,f)
    s=rep(s,' → „Zeigen!“ → die Karte',' → die Karte',1,f)
    s=rep(s,'btns(["✋ Zeigen!","main"],false);','btns(["🔄 Karte umdrehen","main"],false);',1,f)
    s=rep(s,'function zeigen(){if(st.phase!=="play")return;clearT();st.phase="zeigen";$("zeigen").hidden=false}','function zeigen(){if(st.phase!=="play")return;umdrehen()}',1,f)
    return s
def zoom(s,f):
    s=rep(s,'Dann „Zeigen!“. Schritt für Schritt','Schritt für Schritt',1,f)
    s=rep(s,'<b>Zeigen!</b>Alle zeigen. Richtig?','<b>Prüfen</b>Richtig?',1,f)
    s=rep(s,'function zeigen(){stopTimer();$("zeigen").hidden=false}','function zeigen(){stopTimer()}',1,f)
    s=css(s,'#bZeig{display:none!important}',f)
    return s
def pizza(s,f):
    s=rep(s,'<b>Zeigen!</b>Alle zeigen ihr Whiteboard. „💡 Beispiele“','<b>Vergleichen</b>„💡 Beispiele“',1,f)
    s=rep(s,'if(left<=0){stopTimer();$("zeigen").hidden=false}','if(left<=0){stopTimer()}',1,f)
    return s
def quiz3(s,f):  # Exit-Quiz, Boss-Runde, Fehler-Detektiv
    s=drop_step(s,f)
    s=rep(s,'if(left<=0){stopTimer(true);$("zeigen").hidden=false}','if(left<=0){stopTimer(true);loesung()}',1,f)
    s=rep(s,'else{stopTimer(true);$("zeigen").hidden=!$("zeigen").hidden}','else{}',1,f)
    s=css(s,'#bZeig{display:none!important}',f)
    return s
def satzchaos(s,f):
    s=rep(s,'<div class="st"><span class="n">3</span><b>Zeigen!</b><p>Alle Whiteboards hoch.<span class="teamonly"> 1 Punkt pro Team, wenn mind. die Hälfte richtig hat.</span></p></div>','',1,f)
    s=rep(s,'<span class="n">4</span><b>Lösung</b><p>Die Kärtchen fliegen an ihren Platz. <span class="teamonly">Richtig? Punkte fürs Team.</span>','<span class="n">3</span><b>Lösung</b><p>Die Kärtchen fliegen an ihren Platz. <span class="teamonly">1 Punkt pro Team, wenn mind. die Hälfte richtig hat.</span>',1,f)
    s=rep(s,'if(left<=0){stopTimer(true);zeigen()}','if(left<=0){stopTimer(true);loesung()}',1,f)
    s=rep(s,'function zeigen(){if(st.phase!=="chaos")return;stopTimer(true);$("zeigen").hidden=false}','function zeigen(){}',1,f)
    s=rep(s,'$("bZeigen").hidden=ph!=="chaos";','$("bZeigen").hidden=true;',1,f)
    return s
def eis(s,f):
    s=rep(s,'Dann: Zeigen! Die Lösung kommt Buchstabe für Buchstabe','Dann kommt die Lösung Buchstabe für Buchstabe',1,f)
    s=rep(s,'["Zeigen!","Alle Whiteboards gleichzeitig hoch."]','["Zeit um","Die Lösung kommt sofort."]',1,f)
    s=rep(s,'$("coneTxt").textContent="Zeit ist um!";\n  $("zeigen").hidden=false;','$("coneTxt").textContent="Zeit ist um!";\n  aufloesen();',1,f)
    return s
def werbinich(s,f):
    s=rep(s,'<b>Zeigen!</b>Alle zeigen gleichzeitig. Dann kommt die Auflösung.','<b>Auflösung</b>Alle vergleichen mit der Auflösung.',1,f)
    s=rep(s,'löst sofort auf (erst „Zeigen!“)','löst sofort auf',1,f)
    s=rep(s,'title="Schon jetzt auflösen: erst Zeigen!, dann Auflösung"','title="Schon jetzt auflösen"',1,f)
    s=rep(s,'G.step===3?"Zeigen!":G.step===4?"Auflösung":nach','G.step===3?"Auflösung":G.step===4?"Auflösung":nach',1,f)
    s=rep(s,'G.step=4;upd();$("zeigen").hidden=false;$("tipp").innerHTML=`Zeigen!<small>Alle Whiteboards gleichzeitig hoch.</small>`}','G.step=4;upd();solve()}',1,f)
    return s
def activity(s,f):
    s=rep(s,'– dann „Zeigen!“.','– dann kommt die Lösung.',1,f)
    s=rep(s,'<b>Zeigen!</b>Alle Boards hoch. Die Lösung steht groß am Beamer.','<b>Lösung</b>Die Lösung steht groß am Beamer.',1,f)
    s=rep(s,'onclick="toZeigen()">Zeigen!</button>','onclick="toZeigen()">Lösung</button>',1,f)
    s=rep(s,"function toZeigen(){stopTimer();G.phase='zeigen';saveG();renderStage()}","function toZeigen(){stopTimer();toSol()}",1,f)
    s=rep(s,"if(e.code==='Space') togglePause(); else toZeigen()}","if(e.code==='Space') togglePause(); else if(e.key==='Enter'||e.key==='ArrowRight') toZeigen()}",1,f)
    return s
def vokabel(s,f):
    s=rep(s,'dann <b>„Zeigen!“</b> bzw. Lösung','dann kommt die <b>Lösung</b>',1,f)
    s=rep(s,'id="bZ">Zeigen!</button>','id="bZ">Lösung</button>',1,f)
    s=rep(s,"function plenumZeigen(){\n  clearInterval(timer);\n","function plenumZeigen(){\n  clearInterval(timer);plenumLoesung();return;\n",1,f)
    return s

FAM=[('blitzbild/',blitzbild),('spiele/buchstaben-salat/',salat),('spiele/was-fehlt/',wasfehlt),('spiele/zoom-bild/',zoom),('spiele/buchstaben-pizza/',pizza),
     ('spiele/exit-quiz/',quiz3),('spiele/boss-runde/',quiz3),('spiele/fehler-detektiv/',quiz3),('spiele/satz-chaos/',satzchaos),('spiele/eis-schmilzt/',eis),
     ('spiele/wer-bin-ich/',werbinich),('spiele/activity/',activity),('spiele/vokabelcheck/',vokabel)]
files=sorted(glob.glob(R+'blitzbild/**/*.html',recursive=True)+glob.glob(R+'spiele/**/*.html',recursive=True))
out={}
for p in files:
    f=p[len(R):]
    fn=[fn for pre,fn in FAM if f.startswith(pre)]
    if len(fn)!=1: raise SystemExit('keine Familie: '+f)
    s=open(p,encoding='utf-8',newline='').read()
    s2=musik(fn[0](s,f),f)
    out[p]=s2
for p,s in out.items(): open(p,'w',encoding='utf-8',newline='').write(s)
print('geändert:',len(out))
