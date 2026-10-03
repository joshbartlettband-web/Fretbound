# v1.56: how often and how hard does each pedal fire? Perfect answers on random calls, one pedal added to an Iron Comp, no other bonuses.
# usage: python3 tests/pedalsim.py [id ...]
import os,sys,json
from playwright.sync_api import sync_playwright
ids=sys.argv[1:]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":390,"height":760}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto('file://'+os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','index.html'))); pg.wait_for_timeout(500)
    r=pg.evaluate('(ids)=>window.__fb.fxTest(ids,400)',ids)
    for k,v in r.items(): print(f"{k:11s} fires {v['fire']:.2f}  avg gain {v['gain']:5.0f} of {v['base']:.0f}  ({v['pct']:.0f}%)")
    print('errors',errs)
