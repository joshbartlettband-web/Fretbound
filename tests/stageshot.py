import time,sys
from playwright.sync_api import sync_playwright
from PIL import Image
OPEN=[64,59,55,50,45,40]; shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for k in [int(x) for x in sys.argv[1].split(',')]:
        pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4); pg.click("#btnStart"); time.sleep(0.3)
        pg.query_selector_all("#scr-chars .ctile")[k].click(); time.sleep(0.1); pg.click("#btnCharGo"); time.sleep(0.3)
        for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
        pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
        for _ in range(50):
            if pg.is_visible("#vcGo"): break
            time.sleep(0.1)
        time.sleep(1.0); t0=time.time(); pg.click("#vcGo")
        for _ in range(100):
            if pg.evaluate("window.__fb.state.phase")=="listen": break
            time.sleep(0.1)
        time.sleep(0.6); el=pg.query_selector("#stage"); el.screenshot(path=f"st{k}a.png")
        for _ in range(150):
            if pg.evaluate("window.__fb.state.phase")=="answer": break
            time.sleep(0.1)
        n=pg.evaluate("window.__fb.state.call.notes[1]"); pg.evaluate("f=>{window.__fb.HA.ut=Math.pow(f/15,0.85);}",n['f']); time.sleep(0.25)
        pg.evaluate("()=>{ const H=window.__fb.HA; H.sdir=-H.sdir; H.noteAt=performance.now()/1000; }"); time.sleep(0.05); el.screenshot(path=f"st{k}b.png")
        shots.append((Image.open(f"st{k}a.png"),Image.open(f"st{k}b.png"))); print(k,'errors',errs); pg.close()
    b.close()
w,h=shots[0][0].size; c=Image.new('RGB',(w*2+8,len(shots)*(h+8)),'black')
for i,(a,bb) in enumerate(shots): c.paste(a,(0,i*(h+8))); c.paste(bb,(w+8,i*(h+8)))
c.thumbnail((1500,1500)); c.save('stage_sheet.png'); print(c.size)
