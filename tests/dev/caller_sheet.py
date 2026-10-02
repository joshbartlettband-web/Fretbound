import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import time,base64,io,sys,json
from playwright.sync_api import sync_playwright
from PIL import Image
S=OUT
ids=sys.argv[2].split(',') if len(sys.argv)>2 else "spur tide juke dunes sebene azmari rio milonga chicha paris cave frost tokyo ghat bali lanai outback grotto mess aurora pole".split()
POSES=[{'fret':0.0},{'fret':0.6},{'fret':0.3,'strum':1},{'fret':0.3,'lean':1},{'fret':0.3,'gloat':1},{'fret':0.3,'slump':1}]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:300])); pg.on("console",lambda m: errs.append(m.text[:300]) if m.type=='error' else None)
    pg.goto(URL); time.sleep(2.5)
    rows=[[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("([c,q])=>window.__fb.rivalPNG(c,q)",[c,q]).split(',')[1]))).convert('RGBA') for q in POSES] for c in ids]
    print('errors',errs); b.close()
w=max(r[0].size[0] for r in rows); h=max(r[0].size[1] for r in rows); K=2
sh=Image.new('RGB',(len(POSES)*(w*K+4),len(ids)*(h*K+4)),(20,10,8))
for r,row in enumerate(rows):
    for k,im in enumerate(row):
        bg=Image.new('RGBA',im.size,(92,58,38,255)); bg.alpha_composite(im); sh.paste(bg.resize((im.width*K,im.height*K),Image.NEAREST).convert('RGB'),(k*(w*K+4),r*(h*K+4)))
sh.save(sys.argv[1]); print(sh.size)
