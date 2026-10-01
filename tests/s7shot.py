import time,sys
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e.stack)[:600]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4)
    pg.evaluate("()=>{ Object.assign(window.__fb.META,{seven:1,sevenOn:1}); }")
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
    for _ in range(3):
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    pg.click("#vcGo")
    for _ in range(150):
        if pg.evaluate("window.__fb.state.phase")=="answer": break
        time.sleep(0.1)
    print('NS strings:',pg.evaluate("window.__fb.state.broken.length"),' stringsUI:',pg.evaluate("document.getElementById('stringsUI').children.length"))
    r=pg.evaluate("(()=>{const e=document.getElementById('neck').getBoundingClientRect();return {x:e.left-40,y:e.top-60,width:e.width+50,height:e.height+60}})()")
    pg.screenshot(path="s7neck.png",clip=r); print('errors',errs); b.close()
