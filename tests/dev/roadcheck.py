# Opens every road event in the developer event browser, in portrait and landscape, and reports page errors and blank scenes.
# usage: python3 tests/dev/roadcheck.py      (expect "errors: []" and "blank: []")
import os,time,json
from playwright.sync_api import sync_playwright
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]; blank=[]
    for W,H in [(390,844),(844,390)]:
        pg=b.new_page(viewport={"width":W,"height":H}); pg.add_init_script("window.__fbNoWarm=true"); pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
        pg.goto('file://'+REPO+'/index.html'); time.sleep(2); evs=pg.evaluate("window.__fb.eventPlates()")
        for e in evs:
            pg.evaluate(f"window.__fb.devRoad('{e}')"); time.sleep(0.9)
            # the scene has people in it when the relit/cast figures registered their positions
            n=pg.evaluate("window.__fb.relight(window.__fb.relight().on).cast.length")
            if n<2: blank.append((W,e,n))
        pg.close()
    print('events checked',len(evs),'x2'); print('errors:',sorted(set(errs))); print('blank:',blank)
