import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for vw,vh in [(390,844),(360,740),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh}); pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.4); pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
        for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
        pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
        for _ in range(50):
            if pg.is_visible("#vcGo"): break
            time.sleep(0.1)
        pg.click("#vcGo"); time.sleep(0.6)
        r=pg.evaluate("""()=>{ const q=s=>{ const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)]; };
          return {board:q('#board'),gtr:q('#board .board-gtr'),pboard:q('#board .pboard'),pedal:q('#board .pedal'),above:q('.win.handline'),below:q('.answer'),page:[innerWidth,innerHeight,document.scrollingElement.scrollHeight]}; }""")
        print(vw,vh,r); print(pg.evaluate("[...document.querySelectorAll('#board *')].slice(0,12).map(e=>e.tagName+'.'+e.className+' '+(e.getBoundingClientRect().width|0)+'x'+(e.getBoundingClientRect().height|0))")); pg.query_selector("#board").screenshot(path=f"board_{vw}.png"); pg.close()
    b.close()
