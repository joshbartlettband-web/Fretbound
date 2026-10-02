# Painted title roadside objects (Gemini, flat magenta) -> sprites embedded as ROADSIDE_SRC. usage: python3 tests/procroadside.py
# Heights are in source pixels at 180 px per road unit; the game scales each sprite from its ladder and turns it into a silhouette (paintedObj).
import os,sys,json,base64
import numpy as np
from PIL import Image
sys.path.insert(0,'tests')
from procvan import key
UNIT=180
H={'saguaro_a':1.0,'saguaro_b':0.85,'joshua_a':0.95,'joshua_b':0.8,'billboard':1.1,'windmill':1.85,'shack':0.62}
os.makedirs('art/roadside',exist_ok=True); src={}
for k,h in H.items():
    im=Image.open(f'art/gemini_test/roadside/{k}.jpg').convert('RGB'); fg=key(im); ys,xs=np.where(fg)
    c=Image.fromarray(np.dstack([np.asarray(im),(fg*255).astype(np.uint8)])).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    th=round(h*UNIT); c=c.resize((max(4,round(c.width*th/c.height)),th),Image.LANCZOS); a=np.asarray(c).copy(); al=a[:,:,3]>140
    q=Image.fromarray(a[:,:,:3]).quantize(colors=24,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8)).save(f'art/roadside/{k}.png',optimize=True)
    src[k]='data:image/png;base64,'+base64.b64encode(open(f'art/roadside/{k}.png','rb').read()).decode(); print(k,c.size,os.path.getsize(f'art/roadside/{k}.png')//1024,'KB')
s=open('index.html',encoding='utf-8').read(); B,E='/*ROADSIDE:BEGIN*/','/*ROADSIDE:END*/'
blk=B+'\nconst ROADSIDE_SRC='+json.dumps(src,separators=(',',':'))+';\n'+E
if B in s: a=s.index(B); b=s.index(E)+len(E); s=s[:a]+blk+s[b:]
else:
    m='/* a sprite ladder: a painting pre-scaled'; assert s.count(m)==1; s=s.replace(m,blk+'\n'+m)
open('index.html','w',encoding='utf-8').write(s); print('embedded',len(src))
