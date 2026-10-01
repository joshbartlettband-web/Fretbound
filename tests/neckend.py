import time,sys
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1] if len(sys.argv)>1 else 'fretbound.html'; out=sys.argv[2] if len(sys.argv)>2 else 'ends.png'
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for k in [2,3,4,0]:
        pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.goto("file:///home/claude/"+F); time.sleep(0.4); pg.click("#btnStart"); time.sleep(0.3)
        pg.query_selector_all("#scr-chars .ctile")[k].click(); time.sleep(0.1); pg.click("#btnCharGo"); time.sleep(0.3)
        for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
        pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
        for _ in range(50):
            if pg.is_visible("#vcGo"): break
            time.sleep(0.1)
        pg.click("#vcGo")
        for _ in range(150):
            if pg.evaluate("window.__fb.state.phase")=="answer": break
            time.sleep(0.1)
        for i in range(20): pg.click("#navR"); time.sleep(0.03)
        time.sleep(0.3)
        r=pg.evaluate("(()=>{const e=document.getElementById('neck').getBoundingClientRect();return {x:e.left,y:e.top-40,width:e.width,height:e.height+40}})()")
        pg.screenshot(path=f"end{k}.png",clip=r); ims.append(Image.open(f"end{k}.png")); print(k,pg.evaluate("[window.__fb.state.guitar,window.__fb.state.pos,window.__fb.state.win]"),errs); pg.close()
    b.close()
w=ims[0].width; h=ims[0].height; c=Image.new('RGB',(w*2+10,h*2+10),'black')
for i,im in enumerate(ims): c.paste(im,((i%2)*(w+10),(i//2)*(h+10)))
c.thumbnail((1300,1300)); c.save(out); print(c.size)
