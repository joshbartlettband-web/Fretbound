# Gemini vans -> game sprites. Keys the magenta, crops to the vehicle, scales to a target width per level and view, 48 colours.
# usage: python3 tests/procvan.py        (art/gemini_test/vans/v<L>_<view>.png -> art/vans/v<L>_<view>.png + vans.json)   ;   python3 tests/procvan.py --embed   (writes VANART_SRC/META in index.html)
import sys,os,json,glob,base64
import numpy as np
from PIL import Image
sys.path.insert(0,'tests')
from procpedal import key
# target widths in game pixels: title (rear three-quarter, 640x360 canvas) and Van screen (side, 2x-scaled canvas)
W={'v0_rear':66,'v1_rear':96,'v2_rear':128,'v0_side':76,'v1_side':98,'v2_side':122}
def build():
    os.makedirs('art/vans',exist_ok=True); meta={}
    for k,tw in W.items():
        f=f'art/gemini_test/vans/{k}.png'
        if not os.path.exists(f): f=f[:-4]+'.jpg'
        im=Image.open(f).convert('RGB'); fg=key(im); a=np.dstack([np.asarray(im),(fg*255).astype(np.uint8)]); ys,xs=np.where(fg)
        c=Image.fromarray(a).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); s=tw/c.width; nw,nh=tw,max(8,round(c.height*s)); c=c.resize((nw,nh),Image.LANCZOS)
        b=np.asarray(c).copy(); al=b[:,:,3]>140
        q=Image.fromarray(np.clip(b[:,:,:3].astype(float)*1.06,0,255).astype(np.uint8)).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
        Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8)).save(f'art/vans/{k}.png',optimize=True); meta[k]=dict(w=nw,h=nh); print(k,nw,nh,os.path.getsize(f'art/vans/{k}.png')//1024,'KB')
    json.dump(meta,open('art/vans/vans.json','w'))
def embed(path='index.html'):
    meta=json.load(open('art/vans/vans.json')); src={k:'data:image/png;base64,'+base64.b64encode(open(f'art/vans/{k}.png','rb').read()).decode() for k in meta}
    s=open(path,encoding='utf-8').read(); a=s.index('/*VANART:BEGIN*/'); b=s.index('/*VANART:END*/')+len('/*VANART:END*/')
    open(path,'w',encoding='utf-8').write(s[:a]+'/*VANART:BEGIN*/\nconst VANART_SRC='+json.dumps(src,separators=(',',':'))+', VANART_META='+json.dumps(meta,separators=(',',':'))+';\n/*VANART:END*/'+s[b:]); print('embedded',len(src))
if __name__=='__main__': embed() if '--embed' in sys.argv else build()
