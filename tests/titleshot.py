import time,sys
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1]; out=sys.argv[2]; skies=[int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else [0]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":844,"height":390},device_scale_factor=1); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto("file:///home/claude/"+F); time.sleep(0.5); ims=[]
    for k in skies:
        pg.evaluate(f"window.__fb.sky({k})"); time.sleep(0.6)
        u=pg.evaluate("(()=>{ const c=document.querySelector('#scr-title canvas, #titleCv, canvas'); return c.toDataURL(); })()")
        import base64,io; ims.append(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB'))
    print('errors',errs, [i.size for i in ims]); b.close()
w,h=ims[0].size; c=Image.new('RGB',(w,h*len(ims)+4*len(ims)),'black')
for i,im in enumerate(ims): c.paste(im,(0,i*(h+4)))
c.save(out)
