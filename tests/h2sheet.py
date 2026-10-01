import time,base64,io,sys,json
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1]; out=sys.argv[2]; S=int(sys.argv[3]) if len(sys.argv)>3 else 2
POSES=json.loads(sys.argv[4]) if len(sys.argv)>4 else [{'fret':0.3},{'fret':0},{'fret':1},{'fret':0.3,'strum':1},{'fret':0.5,'raise':1,'crouch':0.4},{'fret':0.3,'recoil':1,'blink':1},{'fret':0.3,'slump':1}]
ids=json.loads(sys.argv[5]) if len(sys.argv)>5 else ['bard','monk','hermit','busker','luthier','carto']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e))); pg.goto("file:///home/claude/"+F); time.sleep(0.4)
    rows=[[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("([c,q])=>window.__fb.h2PNG(c,q)",[c,q]).split(',')[1]))).convert('RGBA') for q in POSES] for c in ids]
    print('errors',errs); b.close()
w,h=rows[0][0].size
sheet=Image.new('RGB',(len(POSES)*(w*S+4),len(ids)*(h*S+4)),(20,10,8))
for r,row in enumerate(rows):
    for k,im in enumerate(row):
        bg=Image.new('RGBA',im.size,(92,58,38,255)); bg.alpha_composite(im); sheet.paste(bg.resize((w*S,h*S),Image.NEAREST).convert('RGB'),(k*(w*S+4),r*(h*S+4)))
sheet.save(out); print(sheet.size)
