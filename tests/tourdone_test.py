import os, sys, time, json
from playwright.sync_api import sync_playwright
# The Tour Complete screen (v2.03) at the five house sizes: no scrolling, nothing clipped, a stamp per leg, no page errors.
# Screenshots go to $OUT (default /tmp/fbout).
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
sys.path.insert(0,os.path.join(REPO,'tests'))
AUDIT=open(os.path.join(REPO,'tests','audit.py')).read().split('AUDIT="""')[1].split('"""')[0]
bad=0
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for w,h in [(360,740),(390,844),(412,860),(740,360),(844,390)]:
        pg=b.new_page(viewport={"width":w,"height":h}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.goto('file://'+REPO+'/index.html'); time.sleep(1.0)
        pg.click("#btnStart"); time.sleep(0.3)
        pg.evaluate("window.__fb.tourDoneTest()"); time.sleep(5.0)
        info=pg.evaluate("""(()=>{ const c=document.querySelector('#scr-tourdone .check'), box=document.getElementById('tdMapBox').getBoundingClientRect();
          return {screen:window.__fb.state.screen, over:c.scrollHeight-c.clientHeight, stamps:document.querySelectorAll('#tdMapBox .td-stamp').length,
            segs:document.querySelectorAll('#tdRoute line').length, map:[Math.round(box.width),Math.round(box.height)], title:document.getElementById('tdTitle').textContent}; })()""")
        issues=pg.evaluate(AUDIT)
        pg.screenshot(path=f'{OUT}/tourdone_{w}x{h}.png')
        ok=info['screen']=='tourdone' and info['over']<=0 and info['stamps']==5 and info['segs']==4 and not issues and not errs
        bad+=0 if ok else 1
        print((w,h),'ok' if ok else 'FAIL',json.dumps(info),issues[:6],errs[:3])
        if (w,h)==(390,844):
            pg.click('#btnTdEars'); time.sleep(0.4); print('  ears ->',pg.evaluate("window.__fb.state.screen"))
        pg.close()
    b.close()
print('problems:',bad)
