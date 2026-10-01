import time,base64,io,sys,json
from playwright.sync_api import sync_playwright
from PIL import Image
POSES=[{'fret':0.3},{'fret':0},{'fret':1},{'fret':0.3,'strum':1},{'fret':0.3,'gloat':1},{'fret':0.3,'slump':1}]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e.stack)[:300])); pg.goto("file:///home/user/Fretbound/index.html"); time.sleep(0.5)
    ids=["spur","tide","juke"]
    rows=[[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("([c,q])=>window.__fb.rPNG(c,q)",[c,q]).split(',')[1]))).convert('RGBA') for q in POSES] for c in ids]
    print(ids,'errors',errs); b.close()
S=3; w=max(r[0].size[0] for r in rows); h=max(r[0].size[1] for r in rows)
sheet=Image.new('RGB',(len(POSES)*(w*S+4),len(ids)*(h*S+4)),(20,10,8))
for r,row in enumerate(rows):
    for k,im in enumerate(row):
        bg=Image.new('RGBA',im.size,(92,58,38,255)); bg.alpha_composite(im); sheet.paste(bg.resize((im.size[0]*S,im.size[1]*S),Image.NEAREST).convert('RGB'),(k*(w*S+4),r*(h*S+4)))
sheet.thumbnail((1500,2400)); sheet.save(sys.argv[1]); print(sheet.size)
