# Gemini vans -> game sprites. Keys the magenta, crops to the vehicle, scales to a target width per level and view, 48 colours.
# usage: python3 tests/procvan.py        (art/gemini_test/vans/v<L>_<view>.png -> art/vans/v<L>_<view>.png + vans.json)   ;   python3 tests/procvan.py --embed   (writes VANART_SRC/META in index.html)
import sys,os,json,glob,base64
import numpy as np
from PIL import Image
sys.path.insert(0,'tests')
from scipy import ndimage as ndi
# magenta key that will not eat the red livery: the backdrop has strong blue, the red paint almost none, so blue counts double
def key(im):
    a=np.asarray(im.convert('RGB')).astype(int); bg=np.median(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]),axis=0)
    d=np.abs(a[:,:,0]-bg[0])+np.abs(a[:,:,1]-bg[1])+2*np.abs(a[:,:,2]-bg[2]); near=d<110
    lab,n=ndi.label(near); edge=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0); fg=~np.isin(lab,list(edge))
    fg=ndi.binary_opening(fg,iterations=1); lab,n=ndi.label(fg); sz=ndi.sum(fg,lab,range(1,n+1)); keep=[i+1 for i in range(n) if sz[i]>0.02*sz.max()]
    fg=ndi.binary_fill_holes(np.isin(lab,keep))
    # Gemini paints a magenta-tinted shadow under the bumper; the red livery has almost no blue, so a magenta hue is never paint
    return fg&~((a[:,:,0]-a[:,:,1]>45)&(a[:,:,2]-a[:,:,1]>35))
# target widths in game pixels: title (rear three-quarter, 640x360 canvas) and Van screen (side, 2x-scaled canvas)
# straight rear views since the title fix (the three-quarter views are kept as v<L>_rear34.jpg); nothing is mirrored now
FLIP=set()
W={'v0_rear':48,'v1_rear':58,'v2_rear':68,'v0_side':76,'v1_side':98,'v2_side':122}
def build():
    os.makedirs('art/vans',exist_ok=True); meta={}
    for k,tw in W.items():
        f=f'art/gemini_test/vans/{k}.png'
        if not os.path.exists(f): f=f[:-4]+'.jpg'
        im=Image.open(f).convert('RGB'); fg=key(im); a=np.dstack([np.asarray(im),(fg*255).astype(np.uint8)]); ys,xs=np.where(fg)
        c=Image.fromarray(a).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); c=c.transpose(Image.FLIP_LEFT_RIGHT) if k in FLIP else c; s=tw/c.width; nw,nh=tw,max(8,round(c.height*s)); c=c.resize((nw,nh),Image.LANCZOS)
        b=np.asarray(c).copy(); al=b[:,:,3]>140
        q=Image.fromarray(np.clip(b[:,:,:3].astype(float)*1.06,0,255).astype(np.uint8)).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
        Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8)).save(f'art/vans/{k}.png',optimize=True); meta[k]=dict(w=nw,h=nh); print(k,nw,nh,os.path.getsize(f'art/vans/{k}.png')//1024,'KB')
    json.dump(meta,open('art/vans/vans.json','w'))
def embed(path='index.html'):
    meta=json.load(open('art/vans/vans.json')); src={k:'data:image/png;base64,'+base64.b64encode(open(f'art/vans/{k}.png','rb').read()).decode() for k in meta}
    s=open(path,encoding='utf-8').read(); a=s.index('/*VANART:BEGIN*/'); b=s.index('/*VANART:END*/')+len('/*VANART:END*/')
    open(path,'w',encoding='utf-8').write(s[:a]+'/*VANART:BEGIN*/\nconst VANART_SRC='+json.dumps(src,separators=(',',':'))+', VANART_META='+json.dumps(meta,separators=(',',':'))+';\n/*VANART:END*/'+s[b:]); print('embedded',len(src))
if __name__=='__main__': embed() if '--embed' in sys.argv else build()
