# Gemini guitars -> game sprites. Key the flat background, straighten the neck, fit to 180 px long, 40 colours, and measure
# the joint (where the body ends) and the nut (where the headstock starts) so the rig can stretch body, neck and head separately.
# usage: python3 tests/procguitar.py [--embed]    (art/gemini_test/guitars/<id>.png -> art/guitars/<id>.png + meta.json; --embed writes the block in index.html)
import glob,os,sys,json,base64,math
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'tests')
from procpedal import key
from arttone import tone
LEN=180
def proc(f):
    im=Image.open(f).convert('RGB'); fg=key(im); a=np.dstack([np.asarray(im),(fg*255).astype(np.uint8)])
    ys,xs=np.where(fg); c=Image.fromarray(a).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    # straighten: fit a line through the middle of the neck region
    al=np.asarray(c)[:,:,3]>0; h,w=al.shape; cols=range(int(w*0.55),int(w*0.82)); X=[];Y=[]
    for x in cols:
        r=np.where(al[:,x])[0]
        if len(r): X.append(x); Y.append((r.min()+r.max())/2)
    slope=np.polyfit(X,Y,1)[0]; ang=math.degrees(math.atan(slope))
    pad=Image.new('RGBA',(w+60,h+60),(0,0,0,0)); pad.paste(c,(30,30)); c=pad.rotate(ang,resample=Image.BICUBIC)
    al=np.asarray(c)[:,:,3]>40; ys,xs=np.where(al); c=c.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    s=LEN/c.width; c=c.resize((LEN,max(8,round(c.height*s))),Image.LANCZOS); a=np.asarray(c).copy(); al=a[:,:,3]>140
    rgb=Image.fromarray(tone(np.clip(a[:,:,:3].astype(float)*1.10,0,255).astype(np.uint8),al)).quantize(colors=40,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    out=Image.fromarray(np.dstack([np.asarray(rgb),al*255]).astype(np.uint8))
    h,w=al.shape; top=np.array([np.where(al[:,x])[0].min() if al[:,x].any() else 0 for x in range(w)]); bot=np.array([np.where(al[:,x])[0].max() if al[:,x].any() else 0 for x in range(w)]); hh=bot-top+1
    mx=hh.max(); xm=int(np.argmax(hh>0.8*mx)); xj=xm
    while xj<w-1 and hh[xj]>0.38*mx: xj+=1
    nh=np.median(hh[int(w*0.62):int(w*0.8)]); xn=w-1
    while xn>xj and hh[xn]<1.7*nh: xn-=1
    yc=float(np.median([(top[x]+bot[x])/2 for x in range(xj+3,xn-3)]))
    return out,dict(w=w,h=h,xj=int(xj),xn=int(xn),yc=round(yc,1),ang=round(ang,2))
if __name__=='__main__' and '--embed' not in sys.argv:
    os.makedirs('art/guitars',exist_ok=True); meta={}
    for f in sorted(glob.glob('art/gemini_test/guitars/*.jpg')):
        i=os.path.basename(f)[:-4]; im,m=proc(f); im.save(f'art/guitars/{i}.png',optimize=True); meta[i]=m; print(i,m,os.path.getsize(f'art/guitars/{i}.png')//1024,'KB')
    json.dump(meta,open('art/guitars/meta.json','w'))
    # debug sheet: joint (red), nut (green), neck line (cyan)
    sh=Image.new('RGB',(LEN*3+20,(max(m['h'] for m in meta.values())*3+10)*2),(60,40,30)); k=0
    for i,m in meta.items():
        im=Image.open(f'art/guitars/{i}.png').resize((LEN*3,m['h']*3),Image.NEAREST); d=ImageDraw.Draw(im)
        d.line([(m['xj']*3,0),(m['xj']*3,im.height)],fill=(255,0,0)); d.line([(m['xn']*3,0),(m['xn']*3,im.height)],fill=(0,255,0)); d.line([(0,m['yc']*3),(im.width,m['yc']*3)],fill=(0,255,255))
        bg=Image.new('RGB',im.size,(60,40,30)); bg.paste(im,(0,0),im); sh.paste(bg,((k%2)*(LEN*3+10),(k//2)*(max(mm['h'] for mm in meta.values())*3+10))); k+=1
    sh.save(os.environ.get('OUT','/tmp')+'/guitars_game.png')
if __name__=='__main__' and '--embed' in sys.argv:
    src={os.path.basename(f)[:-4]:'data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode() for f in sorted(glob.glob('art/guitars/*.png'))}; meta=json.load(open('art/guitars/meta.json'))
    s=open('index.html',encoding='utf-8').read(); a=s.index('/*GUITARS:BEGIN*/'); b=s.index('/*GUITARS:END*/')+len('/*GUITARS:END*/')
    open('index.html','w',encoding='utf-8').write(s[:a]+'/*GUITARS:BEGIN*/\nconst GUITAR_SRC='+json.dumps(src,separators=(',',':'))+', GUITAR_META='+json.dumps(meta,separators=(',',':'))+';\n/*GUITARS:END*/'+s[b:]); print('embedded',len(src),'guitars')
