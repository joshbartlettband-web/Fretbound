import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4); pg.click("#btnStart"); time.sleep(0.3)
    out={}
    for L in ['drums','bass','comp','extra']:
        out[L]=pg.evaluate("window.__fb.grooveTest(null,{modes:[3],solo:'%s'})"%L)
    print(f"{'venue':9} {'drums':>7} {'bass':>7} {'comp':>7} {'extra':>7}   (level 3, dB)")
    for k in out['drums']:
        print(f"{k:9} "+" ".join(f"{out[L][k]['3']['db']:7.1f}" for L in ['drums','bass','comp','extra']))
    b.close()
