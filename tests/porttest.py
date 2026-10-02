import time
from playwright.sync_api import sync_playwright
from PIL import Image
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    for tour in [1,0]:
        pg=b.new_page(viewport={"width":360,"height":740},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
        pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.4); pg.evaluate("window.__fbNoRecruit=true"); pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
        pg.evaluate(f"()=>{{ window.__fb.state.tourSel={tour}; }}")
        for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
        pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.4)
        for _ in range(3):
            if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
        for _ in range(50):
            if pg.is_visible("#vcGo"): break
            time.sleep(0.1)
        time.sleep(0.4); pg.query_selector(".vbanner").screenshot(path=f"pc_{tour}.png"); shots.append(Image.open(f"pc_{tour}.png")); pg.close()
    pg=b.new_page(viewport={"width":360,"height":740},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
    pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.4); pg.evaluate("()=>{ Object.assign(window.__fb.META,{fame:50}); }")
    pg.click("#btnVan"); time.sleep(0.2); pg.click("[data-vt=vanCrew]"); time.sleep(0.2); pg.click("[data-m=fay]"); time.sleep(0.4)
    pg.query_selector("#modalCard").screenshot(path="pc_fay.png"); shots.append(Image.open("pc_fay.png")); print('errors',errs); b.close()
w=max(s.width for s in shots); c=Image.new('RGB',(w,sum(s.height+8 for s in shots)),'black'); y=0
for s in shots: c.paste(s,(0,y)); y+=s.height+8
c.thumbnail((700,1400)); c.save('porttest.png'); print(c.size)
