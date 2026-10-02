import time
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for vw,vh in [(360,740),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e.stack)[:300]))
        pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.4); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.4)
        pg.evaluate("()=>{ Object.assign(window.__fb.META,{fame:120}); }")
        pg.click("#btnVan"); time.sleep(0.2); pg.click("[data-vt=vanCrew]"); time.sleep(0.2)
        pg.click("[data-m=lou]"); time.sleep(0.2); pg.click("#mHire"); time.sleep(0.2)
        pg.click("[data-m=rosa]"); time.sleep(0.2); pg.click("#mHire"); time.sleep(0.2)
        m=pg.evaluate("()=>{ const M=window.__fb.META; return {fame:M.fame,hired:M.hired,lineup:M.lineup,scroll:document.scrollingElement.scrollHeight,vh:innerHeight,over:[...document.querySelectorAll('#scr-van *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&(r.bottom>innerHeight+1||r.right>innerWidth+1);}).length}; }")
        pg.screenshot(path=f"band_{vw}.png"); pg.click("[data-m=hale]"); time.sleep(0.2); pg.screenshot(path=f"bandm_{vw}.png"); pg.click("#mClose")
        print(vw,vh,m,errs)
        if vw==360:
            pg.click("#btnVanGo"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
            for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
            pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.4)
            for _ in range(3):
                if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
            for _ in range(50):
                if pg.is_visible("#vcGo"): break
                time.sleep(0.1)
            pg.click("#vcGo"); time.sleep(0.5)
            print(' in run:',pg.evaluate("({lineup:window.__fb.state.lineup,replays:window.__fb.state.replays,band:window.__fb.bandPing()})"),errs)
        pg.close()
    b.close()
