import time,base64,io,sys,json
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1]; out=sys.argv[2]; ids=json.loads(sys.argv[3])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:200])); pg.goto("file:///home/claude/"+F); time.sleep(0.5)
    ims=[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("id=>window.__fb.rPNG(id,{fret:0.3})",i).split(',')[1]))).convert('RGBA') for i in ids]; print('errors',errs); b.close()
T=150; cols=4; rows=(len(ids)+cols-1)//cols; c=Image.new('RGB',(cols*(2*T+10),rows*(T+6)),(40,24,18))
for k,(i,im) in enumerate(zip(ids,ims)):
    x=(k%cols)*(2*T+10); y=(k//cols)*(T+6)
    pt=Image.open(f'newport/{i}.png').convert('RGBA').resize((T,T),Image.NEAREST); bg=Image.new('RGBA',(T,T),(60,34,24,255)); bg.alpha_composite(pt); c.paste(bg.convert('RGB'),(x,y))
    bb=im.getbbox(); cr=im.crop(bb); s=min(T/cr.width,T/cr.height); cr=cr.resize((max(1,int(cr.width*s)),max(1,int(cr.height*s))),Image.NEAREST); bg=Image.new('RGBA',(T,T),(92,58,38,255)); bg.alpha_composite(cr,((T-cr.width)//2,T-cr.height)); c.paste(bg.convert('RGB'),(x+T+2,y))
c.save(out); print(c.size)
