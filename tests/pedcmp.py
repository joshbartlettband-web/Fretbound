import time,base64,io,sys
from playwright.sync_api import sync_playwright
from PIL import Image
ids=['goblin','hornet','glass','echo','wyrm','cathedral','dragon','looper']
def grab(F):
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(); pg.goto("file:///home/claude/"+F); time.sleep(0.5)
        r=[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("i=>window.__fb.pmPNG(i,true)",i).split(',')[1]))).convert('RGBA') for i in ids]; b.close(); return r
old=grab('test_oldped.html'); new=grab('fretbound.html')
T=(126,180); c=Image.new('RGB',(len(ids)*(T[0]+8),2*(T[1]+8)),(42,24,20))
for k,(a,bb) in enumerate(zip(old,new)):
    c.paste(a.resize(T,Image.NEAREST),(k*(T[0]+8),0),a.resize(T,Image.NEAREST)); c.paste(bb.resize(T,Image.NEAREST),(k*(T[0]+8),T[1]+8),bb.resize(T,Image.NEAREST))
c.save('pedcmp.png'); print(c.size)
