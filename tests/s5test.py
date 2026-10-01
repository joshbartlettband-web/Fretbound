import time
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); pg=b.new_page(viewport={"width":360,"height":740},device_scale_factor=2); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e.stack)[:300]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.4)
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
    tours=pg.evaluate("[...document.querySelectorAll('[data-tour],.tour-row')].length"); 
    pg.evaluate("()=>{ window.__fb.state.tourSel=1; }")
    pg.evaluate("()=>{ const S=window.__fb.state; const d=Object.getOwnPropertyDescriptor(S,'legNo'); let v=1; Object.defineProperty(S,'legNo',{get(){return 4;},set(x){v=x;},configurable:true}); }")
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.4)
    for _ in range(3):
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    vid=pg.evaluate("window.__fb.state.tour"); vn=pg.evaluate("document.querySelector('#modalCard h2')&&document.querySelector('#modalCard h2').textContent")
    pg.evaluate("()=>{ const S=window.__fb.state; S.legNo=4; window.__fb.pickRivalBand(); document.querySelector('#modalCard .vrival').insertAdjacentHTML('afterend',window.__fb.rivalBandHTML()); }")
    over=pg.evaluate("(()=>{ const r=document.getElementById('modalCard').getBoundingClientRect(); return {bottom:Math.round(r.bottom),vh:innerHeight}; })()")
    pg.screenshot(path="s5card.png"); print('venue:',vn,'tour',vid,'band:',pg.evaluate("window.__fb.state.rivalBand"),'card fits:',over)
    pg.click("#vcGo")
    for _ in range(100):
        if pg.evaluate("window.__fb.state.phase")=="listen": break
        time.sleep(0.1)
    time.sleep(1.6); pg.query_selector("#stage").screenshot(path="s5stage.png")
    for _ in range(150):
        if pg.evaluate("window.__fb.state.phase")=="answer": break
        time.sleep(0.1)
    print('bpm',pg.evaluate("window.__fb.bandBpm()"),'replays',pg.evaluate("window.__fb.state.replays"),'errors',errs); b.close()
