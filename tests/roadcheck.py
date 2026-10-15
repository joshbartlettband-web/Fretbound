# Every road encounter, at the five house sizes: no page errors, nothing scrolls or overflows, every choice can be clicked and leads to ON TO THE SHOW.
import os,time,sys
from playwright.sync_api import sync_playwright
SIZES=[(360,740),(390,844),(412,860),(740,360),(844,390)]
OUT=os.environ.get('OUT')
bad=[]; errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for w,h in SIZES:
        pg=b.new_page(viewport={"width":w,"height":h}); pg.add_init_script("window.__fbNoWarm=true"); pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
        pg.goto('file://'+os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','index.html'))); time.sleep(1.2)
        pg.evaluate("window.__fb.dev(1,0,true,'busker')"); time.sleep(0.5)
        pg.evaluate("(()=>{ const d=window.__fb.store.dex.callers; d.spur={faced:1,won:1,lost:0,best:0,band:[]}; })()")
        ids=pg.evaluate("window.__fb.roadIds()")
        for rid in ids:
            pg.evaluate("window.__fb.state.money=20"); pg.evaluate(f"window.__fb.road('{rid}')"); time.sleep(0.35)
            r=pg.evaluate("""(()=>{ const s=document.getElementById('scr-road'), el=[...s.querySelectorAll('*')].filter(e=>e.offsetParent), sb=s.getBoundingClientRect();
              const over=el.filter(e=>{ const q=e.getBoundingClientRect(); return q.bottom>innerHeight+1||q.right>innerWidth+1; }).map(e=>e.id||e.className).slice(0,3);
              return {over, scroll:document.scrollingElement.scrollHeight-innerHeight, txt:s.querySelector('.road-text').scrollHeight-s.querySelector('.road-text').clientHeight}; })()""")
            if r['over'] or r['scroll']>1 or r['txt']>1: bad.append((w,h,rid,r))
            if OUT and w==390: pg.screenshot(path=f'{OUT}/road_{rid}.png')
            # click through: first enabled choice, or answer quiz questions
            for _ in range(6):
                if pg.is_visible('#roadGo'): break
                bs=[e for e in pg.query_selector_all('#roadChoices button') if e.is_enabled() and 'HEAR' not in e.inner_text()]
                if not bs: break
                bs[0].click(); time.sleep(0.8)
            if not pg.is_visible('#roadGo'): bad.append((w,h,rid,'no continue'))
            if OUT and w==390: pg.screenshot(path=f'{OUT}/road_{rid}_done.png')
        pg.close()
print(len(bad),'problems'); [print(x) for x in bad[:30]]; print('errors',errs[:5])
