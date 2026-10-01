import time,json,sys
from playwright.sync_api import sync_playwright
exec(open('/home/claude/greentest.py').read().split("with sync_playwright() as p:")[0])
src=open('/home/claude/ear_test.py').read(); head=src[:src.find("with sync_playwright() as p:")]
exec(head)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    # 1+2: a saved run survives practice; a normal run afterwards is normal
    pg=b.new_page(viewport={"width":390,"height":844}); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:400]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.5); pg.evaluate("window.__fbNoRecruit=true")
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.5)
    for _ in range(3):
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
    pg.evaluate("window.__fb.state.money=37; window.__fb.state.over='win'; window.__fb.state.cleared=['spur']; window.__fb.shop()"); time.sleep(0.6)
    keys=lambda: pg.evaluate("Object.keys(localStorage).map(k=>[k,localStorage.getItem(k).length]).filter(x=>x[0].toLowerCase().includes('run'))")
    k0=keys(); print('saved run before practice:',k0)
    pg.reload(); time.sleep(0.6)
    cont=pg.evaluate("!document.getElementById('btnContinue').classList.contains('hidden')"); print('CONTINUE visible after reload:',cont)
    pg.click("#btnBackstage"); time.sleep(0.3); pg.click("[data-door=green]"); time.sleep(0.3); pg.click("#btnGreenGo"); time.sleep(0.6)
    wait_phase(pg,'answer',250)
    for x in pg.evaluate("window.__fb.state.call.notes"): tap(pg,x['s'],x['f'])
    wait_phase(pg,'review',120); time.sleep(0.5); pg.click("#paDone"); time.sleep(0.4); pg.click("#gsBack"); time.sleep(0.4); pg.click("#btnBsBack"); time.sleep(0.4)
    print('saved run after practice :',keys(),'| same size:',keys()==k0)
    pg.click("#btnContinue"); time.sleep(1.0)
    st=pg.evaluate("({screen:window.__fb.state.screen,practice:window.__fb.state.practice,money:window.__fb.state.money,cls:document.getElementById('scr-duel').className,board:getComputedStyle(document.getElementById('board')).display,lab:document.querySelector('#scr-duel .sl-lab').textContent})")
    print('CONTINUE resumes the run:',st)
    pg.close()
    # 2b: starting a brand-new normal run after practice
    pg=b.new_page(viewport={"width":390,"height":844}); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:400]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.5); pg.evaluate("window.__fbNoRecruit=true")
    pg.evaluate("window.__fb.startPractice({preset:'all'})"); time.sleep(0.6); wait_phase(pg,'answer',200); pg.evaluate("window.__fb.finishPracticeSession()"); time.sleep(0.3); pg.click("#gsBack"); time.sleep(0.4); pg.click("#btnBsBack"); time.sleep(0.3)
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.6)
    for _ in range(3):
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    pg.click("#vcGo"); wait_phase(pg,'answer',250)
    st=pg.evaluate("({practice:window.__fb.state.practice,cls:document.getElementById('scr-duel').className,venue:document.getElementById('venueName').innerText,label:document.getElementById('callLabel').innerText,board:getComputedStyle(document.getElementById('board')).display,scoreLab:document.querySelector('#scr-duel .sl-lab').textContent,replay:document.getElementById('btnReplay').innerText})")
    print('NEW NORMAL RUN after practice:',st); pg.close()
    # 3: PRACTICE THESE from the Ear Report
    pg=b.new_page(viewport={"width":390,"height":844}); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:400]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5); seed(pg)
    pg.click("#btnBackstage"); time.sleep(0.3); pg.click("[data-door=ear]"); time.sleep(0.5)
    dis=pg.evaluate("document.getElementById('btnEarPractice').disabled"); lab=pg.evaluate("document.getElementById('btnEarPractice').innerText"); pg.click("#btnEarPractice"); time.sleep(0.5)
    print('PRACTICE THESE enabled:',not dis,lab,'| setup shows:',pg.evaluate("({on:[...document.querySelectorAll('.gchip.on')].map(e=>e.innerText),note:(document.querySelector('.gnote')||{}).innerText,sum:document.querySelector('.gsum').innerText})"))
    print('errors',errs); b.close()
