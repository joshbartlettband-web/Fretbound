# Painted audience silhouettes (Gemini, flat magenta) -> sprites embedded as CROWD_SRC. usage: python3 tests/proccrowd.py   (then python3 tests/grade.py is NOT needed: they are dark silhouettes)
# Heights are in play-screen art pixels (the crowd is drawn on a 320x120 layer, shown at 2x); the figures are cropped at the waist.
import os,sys,json,base64
import numpy as np
from PIL import Image
sys.path.insert(0,'tests')
from procvan import key
H={'crowd_a':24,'crowd_b':26,'crowd_c':24,'crowd_d':24,'crowd_hat':25,'crowd_arms':31,'crowd_arm1':31,'crowd_board':36,'crowd_penguin':19}
os.makedirs('art/crowd',exist_ok=True); src={}
for k,h in H.items():
    im=Image.open(f'art/gemini_test/crowd/{k}.jpg').convert('RGB'); fg=key(im); ys,xs=np.where(fg)
    c=Image.fromarray(np.dstack([np.asarray(im),(fg*255).astype(np.uint8)])).crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    c=c.resize((max(4,round(c.width*h/c.height)),h),Image.LANCZOS); a=np.asarray(c).copy(); al=a[:,:,3]>140
    q=Image.fromarray(a[:,:,:3]).quantize(colors=16,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8)).save(f'art/crowd/{k}.png',optimize=True)
    src[k]='data:image/png;base64,'+base64.b64encode(open(f'art/crowd/{k}.png','rb').read()).decode(); print(k,c.size,os.path.getsize(f'art/crowd/{k}.png')//1024,'KB')
s=open('index.html',encoding='utf-8').read(); B,E='/*CROWD:BEGIN*/','/*CROWD:END*/'
blk=B+'\nconst CROWD_SRC='+json.dumps(src,separators=(',',':'))+';\n'+E
if B in s: a=s.index(B); b=s.index(E)+len(E); s=s[:a]+blk+s[b:]
else:
    m='function drawCrowdFront('; assert s.count(m)==1; s=s.replace(m,blk+'\n'+m)
open('index.html','w',encoding='utf-8').write(s); print('embedded',len(src))
