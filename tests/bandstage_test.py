import time
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4); pg.evaluate("()=>{ localStorage.clear(); }"); pg.reload(); time.sleep(0.4)
    pg.evaluate("()=>{ window.__fbNoRecruit=true; Object.assign(window.__fb.META,{van:{bigvan:1},hired:{lou:1,dee:1,jo:1},lineup:['lou','dee','jo']}); const S=window.__fb.state; Object.defineProperty(S,'legNo',{get(){return 3;},set(x){},configurable:true}); }")
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.4)
    for _ in range(3):
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    pg.click("#vcGo")
    for _ in range(150):
        if pg.evaluate("window.__fb.state.phase")=="answer": break
        time.sleep(0.1)
    time.sleep(2.6); pg.query_selector("#stage").screenshot(path="bandstage.png")
    print('lineup',pg.evaluate("window.__fb.state.lineup"),'rival band',pg.evaluate("window.__fb.state.rivalBand"),'errors',errs); b.close()
