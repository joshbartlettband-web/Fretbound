# Find the indicator LED on each painted pedal (a small round dot between the knobs and the art window, near the middle).
# usage: python3 tests/dev/pedalled.py [OUTDIR]  -> prints PEDAL_LED json {id:[x,y,r]} in the 84x120 pedal space, writes a check sheet
import glob,os,sys,json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
out={}
ims=[]
for f in sorted(glob.glob('art/pedals/*.png')):
    i=os.path.basename(f)[:-4]; a=np.asarray(Image.open(f).convert('RGBA')).astype(float); rgb=a[:,:,:3]; al=a[:,:,3]>128
    L=rgb@[0.299,0.587,0.114]; sat=(rgb.max(2)-rgb.min(2))/np.maximum(1,rgb.max(2)); red=(rgb[:,:,0]-np.maximum(rgb[:,:,1],rgb[:,:,2]))
    # candidates: compact blobs that differ from their surroundings, in the middle band
    loc=ndi.uniform_filter(L,9); diff=np.abs(L-loc)+np.clip(red,0,None)*0.6
    best=None
    for thr in (40,30,22,15):
        m=(diff>thr)&al; m[:16]=False; m[70:]=False; m[:,:26]=False; m[:,58:]=False
        lab,n=ndi.label(m)
        for k in range(1,n+1):
            ys,xs=np.where(lab==k); A=len(ys)
            if A<3 or A>40: continue
            h=ys.max()-ys.min()+1; w=xs.max()-xs.min()+1
            if max(h,w)>8 or abs(h-w)>2: continue
            cx,cy=xs.mean(),ys.mean(); score=diff[ys,xs].mean()+np.clip(red[ys,xs],0,None).mean()-abs(cx-42)*1.5
            if best is None or score>best[0]: best=(score,cx,cy,max(h,w)/2)
        if best: break
    if best: out[i]=[round(best[1],1),round(best[2],1),round(best[3],1)]
    im=Image.open(f).convert('RGBA').resize((168,240),Image.NEAREST); d=ImageDraw.Draw(im)
    if best: x,y,r=best[1]*2,best[2]*2,best[3]*2+3; d.ellipse([x-r,y-r,x+r,y+r],outline=(0,255,255,255),width=2)
    ims.append(im)
print(json.dumps(out)); print(len(out),'of',len(ims))
if len(sys.argv)>1:
    sh=Image.new('RGBA',(12*172,2*244),(40,20,20,255))
    for k,im in enumerate(ims): sh.alpha_composite(im,((k%12)*172,(k//12)*244))
    sh.save(sys.argv[1]+'/pedalled.png')
