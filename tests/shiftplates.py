# Put every title plate's true horizon on the row where the road converges (TITLE_HZ = 224).
# H = the row of the painted horizon in the original 640x224 plate (read off with a ruler). Each plate and its sky mask are moved down by 224-H;
# the new top rows repeat the old top row (sky) and the rows pushed past 224 (ground below the horizon) are dropped, because the game draws the ground itself.
# usage: python3 tests/shiftplates.py   (works on art/plates/<id>.png + <id>_mask.png, once; keeps the originals in art/plates/orig/ ; then re-embeds TITLE_PLATES / TITLE_MASKS in index.html)
import os,re,base64,shutil
import numpy as np
from PIL import Image
H={'na':220,'af':218,'sa':224,'eu':214,'as':222,'oc':220,'an':221}
os.makedirs('art/plates/orig',exist_ok=True)
for cid,h in H.items():
    d=224-h
    for suf in ('','_mask'):
        f=f'art/plates/{cid}{suf}.png'; o=f'art/plates/orig/{cid}{suf}.png'
        if not os.path.exists(o): shutil.copy(f,o)
        im=Image.open(o); a=np.asarray(im).copy()
        if d>0: a=np.concatenate([np.repeat(a[:1],d,axis=0),a[:224-d]],axis=0)
        Image.fromarray(a,mode=im.mode).save(f,optimize=True)
s=open('index.html',encoding='utf-8').read()
def embed(block,pat):
    global s
    a=s.index('const '+block+'={'); b=s.index('};',a)
    body=s[a:b]
    for cid in H:
        f=f'art/plates/{cid}{pat}.png'; b64=base64.b64encode(open(f,'rb').read()).decode()
        body=re.sub(r"(\n  %s:')data:image/png;base64,[A-Za-z0-9+/=]+(')"%cid,lambda m:m.group(1)+'data:image/png;base64,'+b64+m.group(2),body)
    s=s[:a]+body+s[b:]
embed('TITLE_PLATES',''); embed('TITLE_MASKS','_mask')
open('index.html','w',encoding='utf-8').write(s); print('shifted and re-embedded')
