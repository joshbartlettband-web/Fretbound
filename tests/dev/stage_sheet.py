import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import sys,time,base64,io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
ids=sys.argv[2:] or "spur tide juke dunes sebene azmari rio milonga chicha paris cave frost tokyo ghat bali lanai outback grotto mess aurora pole".split()
JS="([id,ts])=>ts.map(t=>window.__fb.stageAt(id,t))"
TS=[1.3,1.55,1.8,2.05]
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":900,"height":600}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
    pg.goto(URL); time.sleep(2.0)
    print("plates loaded:",len(pg.evaluate("window.__fb.stagePlates()")))
    for i in ids:
        try:
            ims=[Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB') for u in pg.evaluate(JS,[i,TS])]
        except Exception as e: print(i,'ERROR',str(e)[:200]); continue
        diff=[sum(1 for x in ImageChops.difference(ims[0],im).getdata() if sum(x)>30) for im in ims[1:]]
        res[i]=ims; print(i,'changed px vs t0:',diff)
    print('page errors',errs); b.close()
out=sys.argv[1]; ks=list(res)
for n in range(0,len(ks),4):
    sheet=Image.new('RGB',(1290,2*252),'black')
    for j,i in enumerate(ks[n:n+4]):
        im=res[i][0]; sheet.paste(im,((j%2)*650,(j//2)*252))
    sheet.save(f'{out}_{n//4}.png')
import pickle; pickle.dump({i:[im for im in v] for i,v in res.items()},open(out+'.pkl','wb'))
