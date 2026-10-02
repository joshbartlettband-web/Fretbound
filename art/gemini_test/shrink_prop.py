# Shrink a prop in a stage source by hand: cut out (polygon/ellipse mask), fill the hole by stretching the surroundings vertically, paste back scaled.
# usage: python3 shrink_prop.py ID SCALE ANCHOR_X ANCHOR_Y  (shapes are edited in the SHAPES dict below)  -> writes stages/ID_edit.png
import sys,numpy as np
from PIL import Image,ImageDraw,ImageFilter
SHAPES={'juke':dict(grow=45,rects=[(388,102,432,145),(400,140,422,255)],ells=[(412,270,56,30),(412,335,63,72)],bbox=(345,95,480,415))}
i,sc,ax,ay=sys.argv[1],float(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]); S=SHAPES[i]
im=Image.open(f'stages/{i}.jpg').convert('RGB'); W,H=im.size
m=Image.new('L',(W,H),0); d=ImageDraw.Draw(m)
for r in S['rects']: d.rectangle(r,fill=255)
for cx,cy,rx,ry in S['ells']: d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=255)
mk=m.filter(ImageFilter.MaxFilter(S.get('grow',21)))   # include outline and shadow
a=np.asarray(im).astype(float); mm=np.asarray(mk)>0; fill=a.copy()
SH=int(S.get('shift',180)); off=np.zeros((H,3)); has=np.zeros(H,bool)
for y in range(H):
    xs=np.where(mm[y])[0]
    if len(xs)==0: continue
    xl,xr=xs.min(),xs.max(); tgt=(a[y,max(xl-4,0):max(xl-1,1)].mean(axis=0)+a[y,min(xr+2,W-1):min(xr+5,W)].mean(axis=0))/2
    patch=np.stack([a[y,min(x+SH,W-1)] for x in xs]).mean(axis=0); off[y]=tgt-patch; has[y]=True
from scipy.ndimage import uniform_filter1d
off=uniform_filter1d(off,25,axis=0)
for y,x in zip(*np.where(mm)): fill[y,x]=a[y,min(x+SH,W-1)]+off[y]
out=Image.fromarray(fill.clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0))
# paste the shrunken prop
x0,y0,x1,y1=S['bbox']; prop=im.crop((x0,y0,x1,y1)); alpha=mk.crop((x0,y0,x1,y1))
nw,nh=round(prop.width*sc),round(prop.height*sc); prop=prop.resize((nw,nh),Image.LANCZOS); alpha=alpha.resize((nw,nh),Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.6))
# keep the prop's own hang point: top-centre of the original shapes maps to (ax,ay)
cx=(x0+x1)//2; px=ax-nw//2; py=ay
out.paste(prop,(px,py),alpha); out.save(f'stages/{i}_edit.png'); print('saved',i)
