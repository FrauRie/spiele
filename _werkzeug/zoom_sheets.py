import re,json,glob,base64,io,os,sys,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
CW,CH=1150,710
def crop_rect(iw,ih,bb,zm,p):
    s0=min(CW*.96/iw,CH*.96/ih); bw=(bb[2]-bb[0])*iw*s0; bh=(bb[3]-bb[1])*ih*s0
    zf=max(1,min(CW*.92/bw,CH*.92/bh)); zEnd=zf*1.3; z=max(min(8,zm or 8),zEnd*2.5)
    s0=min(CW*.96/iw,CH*.96/ih); s=s0*z; W=iw*s; H=ih*s; px=p[0]*W; py=p[1]*H
    ox=min(0,max(CW-W,CW/2-px)) if W>CW else (CW-W)/2
    oy=min(0,max(CH-H,CH/2-py)) if H>CH else (CH-H)/2
    return max(0,-ox/W),max(0,-oy/H),min(1,CW/W),min(1,CH/H),z
def load(f):
    s=open(f,encoding='utf-8').read(); m=re.search(r'const DATA=(\{.*?\});\s*\n',s,re.S); return s,m,json.loads(m.group(1))
def feats(im):
    g=np.asarray(im.convert('L'),dtype=np.float32); rgb=np.asarray(im.convert('RGB'),dtype=np.float32)
    white=((rgb.min(axis=2)>235)).astype(np.float32)
    gx=np.abs(np.diff(g,axis=1,prepend=g[:,:1])); gy=np.abs(np.diff(g,axis=0,prepend=g[:1,:])); edge=np.clip(gx+gy,0,80)
    return white,edge
def integ(a): return np.pad(a.cumsum(0).cumsum(1),((1,0),(1,0)))
def boxsum(I,x0,y0,x1,y1): return I[y1,x1]-I[y0,x1]-I[y1,x0]+I[y0,x0]
if __name__=='__main__':
    try: font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
    except: font=ImageFont.load_default()
    allrows=[]
    for f in sorted(glob.glob('/home/claude/spiele/spiele/zoom-bild/*.html')):
        s,m,d=load(f); name=os.path.basename(f)[10:-5]
        for i,it in enumerate(d['items']):
            im=Image.open(io.BytesIO(base64.b64decode(it['src'].split(',',1)[1]))).convert('RGB'); iw,ih=im.size
            bb=it.get('bb') or [0,0,1,1]; p=[it['zx'],it['zy']]
            rx,ry,rw,rh,z=crop_rect(iw,ih,bb,it.get('zm'),p)
            white,edge=feats(im); IW,IE=integ(white),integ(edge)
            def stat(rx,ry):
                x0,y0=int(rx*iw),int(ry*ih); x1,y1=min(iw,int((rx+rw)*iw)),min(ih,int((ry+rh)*ih)); a=max(1,(x1-x0)*(y1-y0))
                return boxsum(IW,x0,y0,x1,y1)/a, boxsum(IE,x0,y0,x1,y1)/a
            w0,e0=stat(rx,ry)
            best=None
            for gy in np.linspace(bb[1],bb[3],21):
                for gx in np.linspace(bb[0],bb[2],21):
                    r=crop_rect(iw,ih,bb,it.get('zm'),[gx,gy]); w,e=stat(r[0],r[1])
                    sc=e*(1-max(0,w-.25)*2.2)
                    if best is None or sc>best[0]: best=(sc,gx,gy,w,e,r)
            allrows.append(dict(f=name,i=i,w=it['w'],im=im,cur=(rx,ry,rw,rh),p=p,w0=w0,e0=e0,cand=best,fix=it.get('fix')))
    json.dump([dict(f=r['f'],i=r['i'],w=r['w'],p=r['p'],w0=float(r['w0']),e0=float(r['e0']),cx=float(r['cand'][1]),cy=float(r['cand'][2]),cw=float(r['cand'][3]),ce=float(r['cand'][4])) for r in allrows],open('/tmp/zoom/stats.json','w'))
    TW,TH=228,141; per=16
    for si in range(0,len(allrows),per):
        rows=allrows[si:si+per]; sheet=Image.new('RGB',(2*(3*TW+24),8*(TH+26)+6),'#888'); dr=ImageDraw.Draw(sheet)
        for k,r in enumerate(rows):
            col,row=k//8,k%8; X=col*(3*TW+24)+6; Y=row*(TH+26)+4
            im=r['im']; iw,ih=im.size
            th=im.copy(); th.thumbnail((TW,TH)); bg=Image.new('RGB',(TW,TH),'white'); ox,oy=(TW-th.width)//2,(TH-th.height)//2; bg.paste(th,(ox,oy)); d2=ImageDraw.Draw(bg)
            def box(rc,colr):
                d2.rectangle([ox+rc[0]*th.width,oy+rc[1]*th.height,ox+(rc[0]+rc[2])*th.width,oy+(rc[1]+rc[3])*th.height],outline=colr,width=2)
            box(r['cur'],'#E0700A'); c=r['cand'][5]; box(c[:4],'#1565C0')
            sheet.paste(bg,(X,Y+20))
            def cr(rc):
                a=im.crop((int(rc[0]*iw),int(rc[1]*ih),int((rc[0]+rc[2])*iw),int((rc[1]+rc[3])*ih))).resize((TW,TH))
                return a
            sheet.paste(cr(r['cur']),(X+TW+4,Y+20)); sheet.paste(cr(c[:4]),(X+2*TW+8,Y+20))
            dr.text((X,Y+1),f"{si+k} {r['f'][:14]} · {r['w'][:22]}  JETZT weiß {r['w0']*100:.0f}% | AUTO weiß {r['cand'][3]*100:.0f}%",fill='white',font=font)
        sheet.save(f'/tmp/zoom/sheet_{si//per:02d}.jpg',quality=80)
    print(len(allrows),'Bilder')
