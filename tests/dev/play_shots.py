import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import sys,time
from playwright.sync_api import sync_playwright
from PIL import Image
S=OUT
tours=[int(x) for x in sys.argv[1].split(',')]; ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for t in tours:
        pg=b.new_page(viewport={"width":390,"height":844}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:300])); pg.on("console",lambda m: errs.append(m.text[:300]) if m.type=='error' else None)
        pg.goto(URL); time.sleep(1.2); pg.evaluate("window.__fb.store.unlocks={an:true}"); pg.evaluate(f"window.__fb.tour({t})")
        pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.4)
        for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
        pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
        if pg.is_visible("#mOk"): pg.click("#mOk")
        for _ in range(50):
            if pg.is_visible("#vcGo"): break
            time.sleep(0.1)
        pg.click("#vcGo")
        for _ in range(150):
            if pg.evaluate("window.__fb.state.phase")=='answer': break
            time.sleep(0.1)
        time.sleep(1.0); pg.screenshot(path=f'{S}/play_{t}.png'); print(t,errs); ims.append(Image.open(f'{S}/play_{t}.png')); pg.close()
    b.close()
sh=Image.new('RGB',(390*len(ims)+8*(len(ims)-1),844),'black'); [sh.paste(im,(i*398,0)) for i,im in enumerate(ims)]; sh.save(S+'/play_sheet.png')
