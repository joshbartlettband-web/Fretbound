# Gemini Van-screen scenes -> 480x200 plates (horizon about row 116, ground below), 64 colours; also the sky colour of the top row for filling above the plate.
# usage: python3 tests/procvanscene.py   (art/gemini_test/vanscenes/<id>.png|jpg -> art/vanscenes/<id>.png)  ;  --embed  writes VSP_SRC/VSP_TOP in index.html
import sys,os,glob,json,base64
import numpy as np
from PIL import Image
sys.path.insert(0,'tests')
from procstage import trim
W,H=480,200
def build():
    os.makedirs('art/vanscenes',exist_ok=True); top={}
    for f in sorted(glob.glob('art/gemini_test/vanscenes/*.png')+glob.glob('art/gemini_test/vanscenes/*.jpg')):
        i=os.path.basename(f)[:-4]; im=trim(Image.open(f).convert('RGB')); im=im.crop((6,6,im.width-6,im.height-6)); s=W/im.width; h=round(im.height*s); c=im.resize((W,h),Image.LANCZOS)
        if h>=H: c=c.crop((0,h-H,W,h))
        else: c=c.resize((round(W*H/h),H),Image.LANCZOS); c=c.crop((0,0,W,H))
        q=c.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE); q.save(f'art/vanscenes/{i}.png',optimize=True)
        a=np.asarray(q.convert('RGB'))[:3].reshape(-1,3); top[i]='#%02X%02X%02X'%tuple(int(v) for v in np.median(a,axis=0)); print(i,os.path.getsize(f'art/vanscenes/{i}.png')//1024,'KB',top[i])
    json.dump(top,open('art/vanscenes/top.json','w'))
def embed(path='index.html'):
    top=json.load(open('art/vanscenes/top.json')); src={i:'data:image/png;base64,'+base64.b64encode(open(f'art/vanscenes/{i}.png','rb').read()).decode() for i in top}
    s=open(path,encoding='utf-8').read(); a=s.index('/*VSP:BEGIN*/'); b=s.index('/*VSP:END*/')+len('/*VSP:END*/')
    open(path,'w',encoding='utf-8').write(s[:a]+'/*VSP:BEGIN*/\nconst VSP_SRC='+json.dumps(src,separators=(',',':'))+', VSP_TOP='+json.dumps(top,separators=(',',':'))+';\n/*VSP:END*/'+s[b:]); print('embedded',len(src))
if __name__=='__main__': embed() if '--embed' in sys.argv else build()
