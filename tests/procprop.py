# Painted stage props (Gemini, flat magenta) -> small sprites embedded as PROP_SRC. usage: python3 tests/procprop.py   (then python3 tests/grade.py)
# W: target width in stage pixels per prop
import os,sys,json,base64
import numpy as np
from PIL import Image
sys.path.insert(0,'tests')
from procvan import key
W={'sea_rock':50}
os.makedirs('art/props',exist_ok=True); src={}
for k,w in W.items():
    im=Image.open(f'art/gemini_test/props/{k}.jpg').convert('RGB'); fg=key(im); ys,xs=np.where(fg)
    c=Image.fromarray(np.dstack([np.asarray(im),(fg*255).astype(np.uint8)])).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    c=c.resize((w,max(4,round(c.height*w/c.width))),Image.LANCZOS); a=np.asarray(c).copy(); al=a[:,:,3]>140
    q=Image.fromarray(a[:,:,:3]).quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8)).save(f'art/props/{k}.png',optimize=True)
    src[k]='data:image/png;base64,'+base64.b64encode(open(f'art/props/{k}.png','rb').read()).decode(); print(k,c.size)
s=open('index.html',encoding='utf-8').read(); a=s.index('/*PROPS:BEGIN*/'); b=s.index('/*PROPS:END*/')+len('/*PROPS:END*/')
open('index.html','w',encoding='utf-8').write(s[:a]+'/*PROPS:BEGIN*/\nconst PROP_SRC='+json.dumps(src,separators=(',',':'))+';\n/*PROPS:END*/'+s[b:]); print('embedded',len(src))
