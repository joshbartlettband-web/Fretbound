import time
from playwright.sync_api import sync_playwright
JS="""(tag)=>{ const res=[]; document.querySelectorAll('.ptile canvas, .pedal canvas, #modalCard canvas').forEach(c=>{ const r=c.getBoundingClientRect(); if(!r.width||!r.height) return;
  let e=c.parentElement, cut=null; while(e&&e!==document.body){ const cs=getComputedStyle(e); if(cs.overflow!=='visible'||cs.overflowY!=='visible'||cs.overflowX!=='visible'){ const q=e.getBoundingClientRect(); const lost=Math.max(0,q.top-r.top)+Math.max(0,r.bottom-q.bottom)+Math.max(0,q.left-r.left)+Math.max(0,r.right-q.right); if(lost>1.5){ cut={by:(e.id||e.className||e.tagName).toString().slice(0,30),lost:Math.round(lost),h:Math.round(r.height)}; break; } } e=e.parentElement; }
  if(r.bottom>innerHeight+1||r.top<-1) cut=cut||{by:'viewport',lost:Math.round(Math.max(r.bottom-innerHeight,-r.top)),h:Math.round(r.height)};
  if(cut) res.push(tag+' '+(c.parentElement.className||'').toString().slice(0,18)+' '+JSON.stringify(cut)); }); return res; }"""
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for vw,vh in [(360,740),(390,760),(412,860),(740,360),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh}); pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.4); pg.evaluate("window.__fbNoRecruit=true")
        out=[]; pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3); out+=pg.evaluate(JS,'check')
        for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
        out+=pg.evaluate(JS,'check3')
        pg.evaluate("window.__fb.shop()"); time.sleep(0.5); out+=pg.evaluate(JS,'shop')
        if vw==360: pg.screenshot(path='shop360.png')
        pg.query_selector_all("#shopOffer .ptile")[0].click(); time.sleep(0.3); out+=pg.evaluate(JS,'shopmodal')
        print(vw,vh,len(out),out[:6]); pg.close()
    b.close()
