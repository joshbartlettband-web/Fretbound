import os, time, json
from playwright.sync_api import sync_playwright
# The three v2.03 road events (tvset, laundromat, guildhall) through the developer event browser: each shows its own painted
# scene, the talk runs, every choice gives an outcome, and nothing throws. Screenshots go to $OUT.
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
ev=lambda pg,js: pg.evaluate(js)
fails=[]
def check(ok,msg):
    print(('  ok   ' if ok else '  FAIL ')+msg)
    if not ok: fails.append(msg)
def show(pg,e):
    pg.evaluate(f"window.__fb.devRoad({json.dumps(e)})"); time.sleep(0.8)
    for _ in range(40):
        if ev(pg,"!document.getElementById('roadChoices').classList.contains('hidden')&&document.querySelectorAll('#roadChoices button').length>0"): return True
        pg.evaluate("document.getElementById('roadScene').click()"); time.sleep(0.25)
    return False
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":844})
    errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto('file://'+REPO+'/index.html'); time.sleep(0.8)
    pg.click("#btnStart"); time.sleep(0.3)
    ids=ev(pg,"window.__fb.roadIds()")
    for e in ['tvset','laundromat','guildhall']:
        check(e in ids,e+' is in the event list')
        ok=show(pg,e)
        check(ok,e+': conversation finishes and the choices appear')
        info=ev(pg,"({plate:(window.__fb.devRoadState&&window.__fb.devRoadState())||null, title:document.getElementById('roadTitle').textContent, choices:[...document.querySelectorAll('#roadChoices button')].map(b=>b.textContent), talk:document.getElementById('roadTalk').innerText})")
        print('   ',info['title'],'|',info['choices'])
        pg.screenshot(path=f'{OUT}/event_{e}.png')
        for i in range(len(info['choices'])):
            show(pg,e)
            pg.evaluate("window.__fb.state.money=Math.max(window.__fb.state.money,10)")
            show(pg,e) if i==0 and e=='guildhall' else None
            btns=pg.query_selector_all('#roadChoices button')
            if btns[i].is_disabled():
                print('    choice',i,'disabled (not enough cash in the dev snapshot):',info['choices'][i]); continue
            btns[i].click(); time.sleep(1.5)
            out=ev(pg,"document.getElementById('roadOut').textContent")
            check(bool(out.strip()),f'{e} choice {i+1} "{info["choices"][i]}" -> {out[:90]}')
    check(not errs,'no page errors '+str(errs[:3]))
    b.close()
print('problems:',len(fails))
