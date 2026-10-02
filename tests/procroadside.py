# Painted title roadside objects (Gemini, flat magenta) -> sprites embedded as ROADSIDE_SRC. usage: python3 tests/procroadside.py
# Heights are in source pixels at 180 px per road unit; the game scales each sprite from its ladder and turns it into a silhouette (paintedObj).
import os,sys,json,base64
import numpy as np
from PIL import Image
sys.path.insert(0,'tests')
from procvan import key
UNIT=180
# sprite -> height in road units (the wheel and the sails: their diameter, since they are square); CROP: Gemini drew a frame round these
H={'saguaro_a':1.0,'saguaro_b':0.85,'joshua_a':0.95,'joshua_b':0.8,'billboard':1.1,'shack':0.62,'windmill_tower':1.6,'windmill_wheel':0.7,
   'acacia_a':0.8,'acacia_b':0.65,'baobab':1.2,'rondavel':0.65,'giraffe':1.4,
   'cypress_a':1.5,'oak':0.95,'cottage':0.7,'church':1.5,'mill_tower':1.1,'mill_sails':1.35,
   'agave':0.6,'llama':0.55,'chapel':0.65,
   'bamboo':1.5,'pine':1.2,'torii':0.8,'pagoda':1.7,'toro':0.6,'vending_c':0.62,
   'gum':1.6,'roosign_c':0.8,'kanga':0.75,'tank':1.2,
   'berg_c':0.5,'flag_c':0.9,'penguin_c':0.45,'hut_c':0.55,'beacon_c':0.9}
# the *_c sprites are full colour (they keep their own colours, only dusked a little); the rest become dark silhouettes in the game
CROP={'windmill_wheel':24,'mill_sails':24}
os.makedirs('art/roadside',exist_ok=True); src={}
for k,h in H.items():
    im=Image.open(f'art/gemini_test/roadside/{k}.jpg').convert('RGB'); cr=CROP.get(k,0); im=im.crop((cr,cr,im.width-cr,im.height-cr)) if cr else im; fg=key(im); ys,xs=np.where(fg)
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
