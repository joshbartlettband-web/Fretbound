import time,base64,io,sys,json
from playwright.sync_api import sync_playwright
from PIL import Image
ids=json.loads(sys.argv[2])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:200])); pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.6)
    ims=[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("i=>window.__fb.snap(i)",i).split(',')[1]))).convert('RGB') for i in ids]; print('errors',errs); b.close()
w,h=ims[0].size; c=Image.new('RGB',(2*w+6,((len(ims)+1)//2)*(h+6)),'black')
for k,im in enumerate(ims): c.paste(im,((k%2)*(w+6),(k//2)*(h+6)))
c.save(sys.argv[1]); print(c.size, w, h)
