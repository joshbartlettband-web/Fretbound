import json,time,sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":760})
    errs=[]; pg.on("pageerror",lambda e: errs.append(str(e))); pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5)
    pg.click("#btnStart"); time.sleep(0.3)
    r=pg.evaluate("window.__fb.grooveTest()")
    leg=r['legacy']['1']['db']
    print(f"legacy answer level: {leg} dB\n")
    print(f"{'venue':9} {'listen':>7} {'L0':>6} {'L1':>6} {'L2':>6} {'L3':>6}   peak   (dB relative to legacy)")
    for k,v in r.items():
        print(f"{k:9} "+" ".join(f"{v[m]['db']-leg:+6.1f}" for m in ['listen','0','1','2','3'])+f"   {max(x['pk'] for x in v.values()):.2f}")
    json.dump(r,open('gtest.json','w'))
    print("errors:",errs)
    b.close()
