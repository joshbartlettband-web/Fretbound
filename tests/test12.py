import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for (w,h,nm) in [(390,760,'p'),(844,390,'l')]:
        pg=b.new_page(viewport={"width":w,"height":h},device_scale_factor=2)
        errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','test.html'))); time.sleep(1.2)
        pg.screenshot(path=f"f_{nm}_title.png")
        pg.click("#btnStart"); time.sleep(0.4)
        pg.screenshot(path=f"f_{nm}_chars.png")
        pg.click("#btnCharGo"); time.sleep(0.4)
        for i in [0,2,4]: pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.15)
        pg.screenshot(path=f"f_{nm}_check.png")
        ov=pg.evaluate("(()=>{const e=document.querySelector('#scr-check .check'); return e.scrollHeight-e.clientHeight})()")
        pg.click("#btnSound"); time.sleep(0.3); pg.screenshot(path=f"f_{nm}_sound.png"); pg.click("#pRes"); time.sleep(0.2)
        pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.2)
        if pg.is_visible("#mOk"): pg.click("#mOk")
        for _ in range(30):
            if pg.is_visible("#vcGo"): break
            time.sleep(0.1)
        pg.screenshot(path=f"f_{nm}_card.png"); pg.click("#vcGo")
        time.sleep(5.4); pg.screenshot(path=f"f_{nm}_duel.png")
        pg.query_selector_all("#board .pedal")[0].click(); time.sleep(0.3); pg.screenshot(path=f"f_{nm}_pedal.png"); pg.click("#pmC"); time.sleep(0.2)
        pg.evaluate("window.__fb.shop()"); time.sleep(0.5); pg.screenshot(path=f"f_{nm}_shop.png")
        ov2=pg.evaluate("(()=>{const e=document.querySelector('#scr-shop .check'); return e.scrollHeight-e.clientHeight})()")
        pg.query_selector_all("#shopOffer .ptile")[0].click(); time.sleep(0.3); pg.screenshot(path=f"f_{nm}_shopcard.png")
        dov=pg.evaluate("(()=>{const e=document.querySelector('#modal .modal-card'); return e.scrollHeight-e.clientHeight})()")
        print(nm,"overflow check/shop/modal:",ov,ov2,dov,errs); pg.close()
    b.close()
