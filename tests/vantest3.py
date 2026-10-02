import time
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); shots=[]
    for vw,vh in [(360,740),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.5)
        pg.evaluate("()=>{ localStorage.clear(); }"); pg.reload(); time.sleep(0.5)
        pg.evaluate("()=>{ const M=window.__fb.META; M.fame=80; M.toughMax=2; }")
        pg.click("#btnVan"); time.sleep(0.3)
        pg.click("[data-van=trunk]"); time.sleep(0.1); pg.click("[data-vt=vanStr]"); time.sleep(0.1); pg.click("#vRack"); time.sleep(0.1); pg.click("[data-g=heavy]"); time.sleep(0.1); pg.click("[data-vt=vanCrew]"); time.sleep(0.1); pg.click("[data-hire=tech]"); time.sleep(0.2)
        m=pg.evaluate("()=>{ const M=window.__fb.META; return {fame:M.fame,van:M.van,gauge:M.gauge,rack:M.rack,lineup:M.lineup,scroll:document.scrollingElement.scrollHeight,vh:innerHeight, over:[...document.querySelectorAll('#scr-van *')].filter(e=>{const r=e.getBoundingClientRect(); return r.bottom>innerHeight+1||r.right>innerWidth+1;}).length}; }")
        print(vw,vh,m,errs); pg.screenshot(path=f"van_{vw}.png"); shots.append(Image.open(f"van_{vw}.png"))
        if vw==360:
            pg.click("#btnVanGo"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
            for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
            pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.4)
            for _ in range(3):
                if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
            print(' run: tough',pg.evaluate("window.__fb.state.tough"),' money',pg.evaluate("window.__fb.state.money"))
        pg.close()
    b.close()
