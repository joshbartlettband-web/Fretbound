import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import sys,time,base64,io
from playwright.sync_api import sync_playwright
from PIL import Image
out=sys.argv[1]; ths=['na','af','sa','eu','as','oc','an']
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":844}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
    pg.goto(URL); time.sleep(1.0)
    for th in ths:
        pg.evaluate("(th)=>{ const s=window.__fb.store; s.settings.previewScenes=true; s.settings.titleTheme=th; window.__fb.sky(0); }",th); time.sleep(2.5)
        u=pg.evaluate("document.getElementById('titlecv').toDataURL()"); ims.append(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'))
    print('errors',errs); b.close()
w,h=ims[0].size; sh=Image.new('RGB',(w*2,h*4),'black')
for i,im in enumerate(ims): sh.paste(im,((i%2)*w,(i//2)*h))
sh.save(out); print(sh.size)
