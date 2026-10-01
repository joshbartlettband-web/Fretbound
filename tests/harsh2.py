import time,numpy as np
from playwright.sync_api import sync_playwright
from harsh import bands
CFG={'before':dict(os=0,amp=0,hornet=0),'round two':dict(os=0,amp=1,hornet=1)}
CASES=[('nylon',['goblin','hornet']),('nylon',['iron','gate','echo','goblin','hornet']),('single',['iron','gate','echo','goblin','hornet'])]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4)
    print(f"{'fix':12} {'case':30} {'2-4k':>6} {'4-12k':>6} {'level':>6}")
    for name,c in CFG.items():
        pg.evaluate("c=>Object.assign(window.__fb.warm,{os:!!c.os,amp:!!c.amp,hornet:!!c.hornet})",c)
        for g,ids in CASES:
            pr,fz,lv=bands(pg.evaluate("([g,ids])=>window.__fb.rigRender(g,ids)",[g,ids]))
            print(f"{name:12} {g+(' full' if len(ids)>2 else ' gob+hor'):30} {pr:6.1f} {fz:6.1f} {lv:6.1f}")
    print("errors:",errs); b.close()
