import time,base64,io,sys
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1]; S=4; ids=['single','humbucker','nylon','resonator','twelve','baritone']
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e))); pg.goto("file:///home/claude/"+F); time.sleep(0.5)
    ims=[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("id=>window.__fb.gsPNG(id)",i).split(',')[1]))).convert('RGBA') for i in ids]; print('errors',errs); b.close()
w,h=ims[0].size; c=Image.new('RGB',(6*(w*S+8),h*S),(23,16,18))
for k,im in enumerate(ims):
    bg=Image.new('RGBA',im.size,(23,16,18,255)); bg.alpha_composite(im); c.paste(bg.resize((w*S,h*S),Image.NEAREST).convert('RGB'),(k*(w*S+8),0))
c.save(sys.argv[2]); print(c.size)
