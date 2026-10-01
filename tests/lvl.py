import time
from playwright.sync_api import sync_playwright
BOARDS=[[],['hornet'],['goblin','hornet'],['iron','gate','echo','goblin','hornet'],['ogre','swamp'],['ogre','basilisk','dragon'],['ogre','swamp','hornet','basilisk','goblin','dragon','troll']]
res={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for f in ['fretbound_pre_warm.html','fretbound.html']:
        pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.goto("file:///home/claude/"+f); time.sleep(0.4); pg.click("#btnStart"); time.sleep(0.3)
        res[f]=[pg.evaluate("ids=>window.__fb.stackTest(ids)",ids) for ids in BOARDS]; print(f,'errors',errs); pg.close()
    b.close()
for ids,a,c in zip(BOARDS,res['fretbound_pre_warm.html'],res['fretbound.html']):
    print(f"{(','.join(ids) or 'bare'):52} before {a}  after {c}")
