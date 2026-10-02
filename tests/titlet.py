import time,sys,base64,io
from playwright.sync_api import sync_playwright
from PIL import Image
ts=[float(x) for x in sys.argv[2].split(',')]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":844,"height":390}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.5); pg.evaluate("window.__fb.sky(1)"); ims=[]
    for t in ts:
        u=pg.evaluate("t=>{ window.__fb.titleAt(t); const c=document.querySelector('#scr-title canvas, #titleCv, canvas'); return c.toDataURL(); }",t)
        ims.append(Image.open(io.BytesIO(base64.b64decode(u.split(',')[1]))).convert('RGB').crop((0,150,640,300)))
    print('errors',errs); b.close()
w,h=ims[0].size; c=Image.new('RGB',(w*2+4,(h+4)*((len(ims)+1)//2)),'black')
for i,im in enumerate(ims): c.paste(im,((i%2)*(w+4),(i//2)*(h+4)))
c.save(sys.argv[1]); print(c.size)
