import time,sys,json
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1]; out=sys.argv[2]; FONTS=json.loads(sys.argv[3]); TXT=sys.argv[4] if len(sys.argv)>4 else "2 H Z S 5 +2 Hype 22"
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for f,sz,dpr in FONTS:
        pg=b.new_page(viewport={"width":400,"height":200},device_scale_factor=dpr); pg.goto("file:///home/claude/"+F); time.sleep(0.5)
        pg.evaluate("([f,s,t])=>{ const d=document.createElement('div'); d.id='g'; d.style.cssText='position:fixed;left:0;top:0;background:#2A1614;color:#F2E8CE;z-index:99999;padding:3px 5px;white-space:nowrap;font-family:\"'+f+'\";font-size:'+s+'px'; d.textContent=t; document.body.appendChild(d); }",[f,sz,TXT]); time.sleep(0.6)
        pg.query_selector('#g').screenshot(path='g.png'); im=Image.open('g.png').convert('RGB'); k=max(1,int(round(8/dpr*(13/sz)))) if sz<40 else 1
        ims.append(im.resize((im.width*k,im.height*k),Image.NEAREST)); pg.close()
    b.close()
W=max(i.width for i in ims); c=Image.new('RGB',(W,sum(i.height+6 for i in ims)),'black'); y=0
for i in ims: c.paste(i,(0,y)); y+=i.height+6
c.thumbnail((1400,1400)); c.save(out); print(c.size)
