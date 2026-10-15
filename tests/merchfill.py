# v1.84: fill the dark hole in the middle of the merch-room painting (it is in Gemini's original) with brick that continues the wall's
# own courses and joints, coloured from the wall beside it. Called by tests/procrooms.py after it makes the master.
# usage: python3 tests/merchfill.py IN.png OUT.png   (also writes OUT_mask.png)
import sys,numpy as np
from PIL import Image
from scipy import ndimage as ndi
src,out=sys.argv[1],sys.argv[2]
im=Image.open(src).convert('RGB'); a=np.asarray(im).astype(float); H,W,_=a.shape; L=a.mean(2)
rng=np.random.default_rng(7)
rows=[61,78,96,114,129,146,161,179,196,212,228,245,262,279,296]
BOX=(219,88,427,294)                      # x0,y0,x1,y1 around the hole
EXCL=[(377,259,430,320),(0,285,292,360)]  # cash box, record stacks and table
# what the wall looks like away from the hole, per row: brick colour and mortar colour
def brickish(p): return (p[...,0]>p[...,1]*1.85)&(p[...,0]>p[...,2]*2.2)
outside=np.ones((H,W),bool); outside[:,BOX[0]-2:BOX[2]+2]=False
lm=ndi.uniform_filter(L,9)
exp=np.zeros(H); bcol=np.zeros((H,3)); mcol=np.zeros((H,3))
for y in range(H):
    m=outside[y]&brickish(a[y])
    if m.sum()<10: continue
    v=L[y][m]; hi=v>=np.percentile(v,40)
    if hi.sum()<3: continue
    bcol[y]=np.median(a[y][m][hi],0); exp[y]=np.median(lm[y][m])
# rows without samples: nearest filled
idx=np.where(exp>0)[0]
for y in range(H):
    if exp[y]==0: j=idx[np.argmin(abs(idx-y))]; exp[y]=exp[j]; bcol[y]=bcol[j]
bcol=ndi.uniform_filter1d(bcol,25,axis=0,mode='nearest'); exp=ndi.uniform_filter1d(exp,9)
# the hole: much darker on average than the wall at that height
hole=lm<0.95*exp[:,None]
box=np.zeros((H,W),bool); box[BOX[1]:BOX[3],BOX[0]:BOX[2]]=True
for x0,y0,x1,y1 in EXCL: box[y0:y1,x0:x1]=False
hole&=box; hole=ndi.binary_closing(hole,iterations=4); hole=ndi.binary_fill_holes(hole); hole=ndi.binary_dilation(hole,iterations=3)&box
hole=ndi.binary_fill_holes(ndi.binary_closing(hole,iterations=6))&box
# joints per course: anchor on real joints at the hole's left and right edges
P=37.3
def joints_in(y0,y1,xa,xb):
    col=L[y0:y1].mean(0); return [x for x in range(xa,xb) if col[x]<0.78*np.median(col[max(0,x-10):x+10]) and col[x]<=col[x-1] and col[x]<=col[x+1]]
res=a.copy(); prev=None
for i in range(len(rows)-1):
    y0,y1=rows[i],rows[i+1]                       # mortar row y0..y0+1, brick y0+2..y1-1
    ys=np.arange(y0,y1); hm=hole[y0:y1]
    if not hm.any(): continue
    xs=np.where(hm.any(0))[0]; hx0,hx1=xs.min(),xs.max()
    lj=[x for x in joints_in(y0+2,y1-1,hx0-40,hx0+2)]; rj=[x for x in joints_in(y0+2,y1-1,hx1-2,min(W-1,hx1+40))]
    left=lj[-1] if lj else (prev+P/2 if prev is not None else hx0-10)
    while left>hx0: left-=P
    right=rj[0] if rj else None
    if right is not None and right>left:
        n=max(1,round((right-left)/P)); sp=(right-left)/n
    else: sp=P
    J=[left+k*sp for k in range(int((hx1-left)/sp)+3)]
    prev=left
    mort=np.median(a[y0:y0+2][:, (outside[y0]&brickish(a[y0+4]))] ,axis=0) if False else None
    for k in range(len(J)-1):
        xa,xb=int(round(J[k])),int(round(J[k+1]))
        tint=1+rng.normal(0,0.05); warm=rng.normal(0,0.025)
        spk={}   # a few worn pixels per brick, like the painted ones
        for _ in range(rng.integers(1,4)):
            sx,sy=rng.integers(xa+3,max(xa+4,xb-1)),rng.integers(y0+3,max(y0+4,y1-1)); spk[(sx,sy)]=0.86; spk[(sx+1,sy)]=0.9
        for y in range(y0,y1):
            c=bcol[y]*tint; c=c*np.array([1+warm,1,1-warm])
            for x in range(max(0,xa),min(W,xb)):
                if not hole[y,x]: continue
                if y<y0+2 or x<xa+2:                      # mortar: the wall's own mortar is about 62% of the brick
                    v=bcol[y]*0.6
                elif y==y0+2: v=c*1.13                    # a lit top edge, like the painted bricks
                elif y==y1-1: v=c*0.9
                else: v=c*(1+rng.normal(0,0.018))*(0.97+0.06*(x-xa)/max(1,xb-xa))*spk.get((x,y),1)
                res[y,x]=v
Image.fromarray(np.clip(res,0,255).astype(np.uint8)).save(out)
m=Image.fromarray((hole*255).astype(np.uint8)); m.save(out.replace('.png','_mask.png')); print('filled',int(hole.sum()),'px')
