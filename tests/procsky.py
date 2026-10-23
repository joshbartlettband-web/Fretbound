# Real night skies for the road events (v1.99). Josh: the event skies look like an AI's starry night; use real references.
# Data: d3-celestial's star catalogue (Hipparcos to magnitude 6, BSD-3-Clause, github.com/ofrohn/d3-celestial) and its Milky Way outline.
#   python3 tests/procsky.py CELESTIAL_DATA_DIR [--embed]
# writes art/sky/stars.json (ra, dec, mag, B-V of every star to mag 5.6), art/sky/milkyway.png (the Milky Way's brightness on an
# equirectangular map, RA 0..360 left to right, Dec +90..-90 top to bottom, 0.5 degree a pixel) and art/sky/<event>_skymask.png
# (white where an event painting's own sky is, cut away at run time so the real sky shows), and with --embed the SKY block in index.html.
import sys,os,json,base64,io
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(ROOT,'art','sky'); os.makedirs(OUT,exist_ok=True)
D=sys.argv[1]
st=json.load(open(os.path.join(D,'stars.6.json')))['features']; rows=[]
for f in st:
    m=f['properties']['mag']; 
    if m>5.6: continue
    ra,dec=f['geometry']['coordinates']; ra=ra%360; bv=float(f['properties'].get('bv') or 0.6)
    rows+=[round(ra*10),round(dec*10),round(m*10),round(bv*100)]
json.dump(rows,open(os.path.join(OUT,'stars.json'),'w'),separators=(',',':')); print('stars',len(rows)//4)
mw=json.load(open(os.path.join(D,'mw.json')))['features']; W,H=720,360; acc=np.zeros((H,W),float)
for f in mw:
    lvl={'ol1':1,'ol2':2,'ol3':3,'ol4':4,'ol5':5}.get(f['id'],1); im=Image.new('L',(W,H),0); d=ImageDraw.Draw(im)
    for poly in f['geometry']['coordinates']:
        for ring in poly[:1]:
            pts=[(((x%360)/360)*W,((90-y)/180)*H) for x,y in ring]
            segs=[[pts[0]]]
            for a,b in zip(pts,pts[1:]):
                if abs(b[0]-a[0])>W/2: segs.append([])
                segs[-1].append(b)
            for sgm in segs:
                if len(sgm)>2: d.polygon(sgm,fill=255)
    acc+=np.asarray(im,float)/255*(1 if lvl<5 else 1)
acc=acc/acc.max(); mwim=Image.fromarray((acc*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.5)); mwim.save(os.path.join(OUT,'milkyway.png'),optimize=True)
# moonbet: its painted sky (paper lanterns, glowing smudges, noisy stars) goes; the tree, the signpost, the treeline and the fields stay
pl=np.asarray(Image.open(os.path.join(ROOT,'art','events','moonbet.png')).convert('RGB')).astype(int); h,w=pl.shape[:2]; m=np.zeros((h,w),np.uint8)
r,g,b=pl[...,0],pl[...,1],pl[...,2]; lum=0.3*r+0.59*g+0.11*b
keep=[(122,40,168,120),(300,12,384,100)]   # the signpost and the moss tree (x0,y0,x1,y1): their own pixels (not navy sky) stay
HZ=72                                      # everything above this row is the painted sky; the low band (treeline glow, fireflies) stays
for x in range(w):
    for y in range(HZ):
        inside=any(x0<=x<=x1 and y0<=y<=y1 for x0,y0,x1,y1 in keep)
        if inside and not (b[y,x]>r[y,x]+12 and lum[y,x]<60): continue
        m[y,x]=255
k=(m==0); kept=np.pad(k,1).astype(int); nb=sum(np.roll(np.roll(kept,dy,0),dx,1) for dy in (-1,0,1) for dx in (-1,0,1))[1:-1,1:-1]-k
m[(k)&(nb<3)&(np.arange(h)[:,None]<HZ)]=255   # lone painted stars beside the tree go too
mi=Image.fromarray(m).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(3)); ma=Image.new('LA',mi.size,255); ma.putalpha(mi); ma.save(os.path.join(OUT,'moonbet_skymask.png'),optimize=True)   # the sky as alpha, for destination-out
print('moonbet sky rows per column, median', int(np.median((np.asarray(mi)>0).sum(0))))
if '--embed' in sys.argv:
    b64=lambda p:'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
    blk='/*SKY:BEGIN*/\nconst SKY_STARS='+open(os.path.join(OUT,'stars.json')).read()+';\nconst SKY_MW_SRC="'+b64(os.path.join(OUT,'milkyway.png'))+'";\nconst SKY_MASK_SRC='+json.dumps({'moonbet':b64(os.path.join(OUT,'moonbet_skymask.png'))})+';/*SKY:END*/'
    p=os.path.join(ROOT,'index.html'); s=open(p,encoding='utf-8').read()
    if '/*SKY:BEGIN*/' in s: i=s.index('/*SKY:BEGIN*/'); j=s.index('/*SKY:END*/')+len('/*SKY:END*/'); s=s[:i]+blk+s[j:]
    else: a='/*EVENTS:END*/'; assert s.count(a)==1; s=s.replace(a,a+'\n'+blk)
    open(p,'w',encoding='utf-8').write(s); print('embedded',len(blk))
