import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import time,base64,io
from playwright.sync_api import sync_playwright
from PIL import Image
S=OUT
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    res={}
    for name,vp in (('port',(390,844)),('land',(844,390))):
        pg=b.new_page(viewport={"width":vp[0],"height":vp[1]},device_scale_factor=2); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:300])); pg.on("console",lambda m: errs.append(m.text[:300]) if m.type=='error' else None)
        pg.goto(URL); time.sleep(3.0); ts=[]; vs=[]
        for lvl in (0,1,2):
            pg.evaluate("(l)=>{ window.__fb.store.meta.van.bigvan=l; }",lvl); time.sleep(1.2)
            u=pg.evaluate("document.getElementById('titlecv').toDataURL()"); ts.append(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'))
        pg.evaluate("window.__fb.store.meta.lineup=['lou','dee','jo','hale']") if False else None
        pg.click("#btnVan"); time.sleep(1.0)
        for lvl in (0,1,2):
            pg.evaluate("(l)=>{ window.__fb.store.meta.van.bigvan=l; }",lvl); time.sleep(0.6)
            u=pg.evaluate("document.getElementById('vanScene').toDataURL()"); vs.append(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'))
        res[name]=(ts,vs); print(name,errs); pg.close()
    b.close()
ts=res['port'][0]; tc=[t.crop((200,170,470,300)).resize((540,260),Image.NEAREST) for t in ts]
sh=Image.new('RGB',(540*3+8,260),'black'); [sh.paste(t,(i*544,0)) for i,t in enumerate(tc)]; sh.save(S+'/vans_title2.png')
def scene(vs,k,crop_h):
    w,h=vs[0].size; return [v.crop((0,h-crop_h,w,h)).resize((w*k,crop_h*k),Image.NEAREST) for v in vs]
a=scene(res['port'][1],3,130); b2=scene(res['land'][1],2,130)
W=max(sum(x.width+6 for x in a),sum(x.width+6 for x in b2)); sh=Image.new('RGB',(W,a[0].height+b2[0].height+6),'black'); x=0
for im in a: sh.paste(im,(x,0)); x+=im.width+6
x=0
for im in b2: sh.paste(im,(x,a[0].height+6)); x+=im.width+6
sh.save(S+'/vans_scene2.png'); print(sh.size)
