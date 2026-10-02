import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import sys,time
from playwright.sync_api import sync_playwright
k=int(sys.argv[1]); out=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:400])); pg.on("console",lambda m: errs.append('console:'+m.text[:300]) if m.type=='error' else None)
    pg.goto(URL); time.sleep(1.5); pg.click("#btnStart"); time.sleep(0.4)
    pg.query_selector_all("#scr-chars .ctile")[k].click(); time.sleep(0.2); pg.click("#btnCharGo"); time.sleep(0.5)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.1)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.4)
    if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    pg.click("#vcGo"); time.sleep(2.0); pg.screenshot(path=out)
    print('state', pg.evaluate("({phase:window.__fb.state.phase,screen:window.__fb.state.screen,char:window.__fb.state.char})")); print('errors',errs); b.close()
