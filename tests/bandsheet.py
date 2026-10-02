import time,base64,io
from playwright.sync_api import sync_playwright
from PIL import Image
ids=['lou','rosa','dee','jo','hale','tam','brass']; POSES=[{},{'hit':1,'strum':1,'raise':1}]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:200])); pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.5)
    ims=[[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("([i,q])=>window.__fb.bandPNG(i,q)",[i,q]).split(',')[1]))).convert('RGBA') for q in POSES] for i in ids]; print('errors',errs); b.close()
w,h=ims[0][0].size; S=2; c=Image.new('RGB',(len(ids)*(w*S+4)//1,2*(h*S+4)),(20,10,8))
for k,row in enumerate(ims):
    for r,im in enumerate(row):
        bg=Image.new('RGBA',im.size,(92,58,38,255)); bg.alpha_composite(im); c.paste(bg.resize((w*S,h*S),Image.NEAREST).convert('RGB'),(k*(w*S+4),r*(h*S+4)))
c.thumbnail((1600,900)); c.save('bandsheet.png'); print(c.size)
