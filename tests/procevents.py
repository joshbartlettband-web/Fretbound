# v1.93: Gemini event backdrops -> 480x200 plates, 64 colours, same as the Van scenes (tests/procvanscene.py), plus each one's top-row sky colour.
# usage: python3 tests/procevents.py   (art/gemini_test/events/<id>.png -> art/events/<id>.png) ;  --embed  writes EVENT_SRC/EVENT_TOP into index.html
import sys,os,glob,json,base64
import numpy as np
from PIL import Image
sys.path.insert(0,'tests')
from procstage import trim
W,H=480,200
def build():
    os.makedirs('art/events',exist_ok=True); top={}
    for f in sorted(glob.glob('art/gemini_test/events/*.png')):
        i=os.path.basename(f)[:-4]; im=trim(Image.open(f).convert('RGB')); im=im.crop((6,6,im.width-6,im.height-6)); s=W/im.width; h=round(im.height*s); c=im.resize((W,h),Image.LANCZOS)
        if h>=H: c=c.crop((0,h-H,W,h))
        else: c=c.resize((round(W*H/h),H),Image.LANCZOS); x=(c.width-W)//2; c=c.crop((x,0,x+W,H))
        q=c.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE); q.save(f'art/events/{i}.png',optimize=True)
        a=np.asarray(q.convert('RGB'))[:3].reshape(-1,3); top[i]='#%02X%02X%02X'%tuple(int(v) for v in np.median(a,axis=0))
    json.dump(top,open('art/events/top.json','w')); print('built',len(top),sum(os.path.getsize(f'art/events/{i}.png') for i in top)//1024,'KB')
def embed(path='index.html'):
    top=json.load(open('art/events/top.json')); src={i:'data:image/png;base64,'+base64.b64encode(open(f'art/events/{i}.png','rb').read()).decode() for i in top}
    s=open(path,encoding='utf-8').read(); blk='/*EVENTS:BEGIN*/\nconst EVENT_SRC='+json.dumps(src,separators=(',',':'))+', EVENT_TOP='+json.dumps(top,separators=(',',':'))+';\n/*EVENTS:END*/'
    if '/*EVENTS:BEGIN*/' in s: a=s.index('/*EVENTS:BEGIN*/'); b=s.index('/*EVENTS:END*/')+len('/*EVENTS:END*/'); s=s[:a]+blk+s[b:]
    else: a=s.index('/*VSP:BEGIN*/'); s=s[:a]+blk+'\n'+s[a:]
    open(path,'w',encoding='utf-8').write(s); print('embedded',len(src))
if __name__=='__main__': embed() if '--embed' in sys.argv else build()
