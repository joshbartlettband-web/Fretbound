# Hand-erase the arms of a Gemini standing body (arms hanging at the sides). Polygons are in crop coordinates (crop origin OX,OY of the 864x1184 source).
# usage: python3 armless.py OUT.png [overlay]   -> OUT.png RGBA armless body; with 'overlay' also writes OUT_ov.png showing the polygons
import sys,numpy as np
from PIL import Image,ImageDraw
OX,OY=200,330
LEFT=[(78,118),(112,108),(146,104),(147,332),(150,346),(143,372),(140,428),(122,436),(90,410),(86,338),(76,322),(72,200)]
HAND2=[(143,346),(162,352),(162,428),(140,430)]
RIGHT=[(344,250),(352,240),(374,300),(367,352),(365,420),(346,420),(346,380),(344,300)]
im=Image.open('chars/bard_body.jpg').convert('RGB').crop((OX,OY,OX+520,OY+770))
if len(sys.argv)>2:
    ov=im.copy(); d=ImageDraw.Draw(ov)
    for P in (LEFT,RIGHT): d.polygon(P,outline=(255,255,0))
    ov.save(sys.argv[1][:-4]+'_ov.png'); sys.exit()
a=np.asarray(im).astype(float); H,W,_=a.shape
bg=np.median(np.concatenate([a[0],a[-1]]),axis=0)
ml=Image.new('L',(W,H),0); ImageDraw.Draw(ml).polygon(LEFT,fill=255); mr=Image.new('L',(W,H),0); ImageDraw.Draw(mr).polygon(RIGHT,fill=255)
ml=np.asarray(ml)>0; mr=np.asarray(mr)>0; out=a.copy(); alpha=np.ones((H,W))
# left arm: continue the cape with a smooth colour taken from the cape just left of the arm
for y in range(H):
    xs=np.where(ml[y])[0]
    if len(xs):
        x0=xs.min(); lo=max(0,y-14); hi=min(H,y+15); band=a[lo:hi,max(x0-12,0):max(x0-3,1)].reshape(-1,3); out[y,xs]=np.median(band,axis=0)
# the fingers that lay over the trousers become trouser brown
mh=Image.new('L',(W,H),0); ImageDraw.Draw(mh).polygon(HAND2,fill=255); mh=np.asarray(mh)>0
for y in range(H):
    xs=np.where(mh[y])[0]
    if len(xs): out[y,xs]=a[y,min(xs.max()+6,W-1)]
# clean dark seam where the tunic now meets the cape
for y in range(106,334): out[y,146:149]=(24,62,30)
# right arm: becomes background
for y in range(H):
    xs=np.where(mr[y])[0]
    if len(xs): alpha[y,xs]=0
for y in range(250,420):
    xs=np.where(mr[y])[0]
    if len(xs): out[y,xs.min()-2:xs.min()]=(24,62,30) if y<345 else out[y,xs.min()-2:xs.min()]
rgba=np.dstack([out,alpha*255]).astype(np.uint8); Image.fromarray(rgba).save(sys.argv[1]); print('saved')
