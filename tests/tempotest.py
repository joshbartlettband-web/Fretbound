import time,json,sys
from playwright.sync_api import sync_playwright
exec(open('/home/claude/greentest.py').read().split("with sync_playwright() as p:")[0])
def drag(pg,sel,val): pg.evaluate("([s,v])=>{ const e=document.querySelector(s); e.value=v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }",[sel,val])
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:400]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.5)
    pg.click("#btnBackstage"); time.sleep(0.3); pg.click("[data-door=green]"); time.sleep(0.3)
    print('setup label:',pg.evaluate("document.querySelector('.gtempo h4').innerText"))
    drag(pg,"#gTempo",56); time.sleep(0.3); print('after dragging setup slider to 56:',pg.evaluate("document.querySelector('.gtempo h4').innerText"),'|',pg.evaluate("document.querySelector('.gsum').innerText"))
    pg.screenshot(path='tempo_setup.png')
    pg.click("#btnGreenGo"); time.sleep(0.6); print('session tempo at start:',pg.evaluate("window.__fb.bpm()"))
    wait_phase(pg,'answer',250); time.sleep(0.3)
    print('panel:',pg.evaluate("document.getElementById('paBpm').innerText"),'| slider value:',pg.evaluate("document.getElementById('paTempo').value"))
    pg.screenshot(path='tempo_duel.png')
    drag(pg,"#paTempo",120); time.sleep(0.4); print('dragged to 120 while answering ->',pg.evaluate("window.__fb.bpm()"),'| label:',pg.evaluate("document.getElementById('paBpm').innerText"))
    pg.click("#btnReplay"); time.sleep(0.5); print('replay started:',pg.evaluate("window.__fb.bpm()"))
    wait_phase(pg,'answer',250); print('back to answering after the replay at the new tempo:',pg.evaluate("window.__fb.bpm()"))
    # answer it, then change during review, then check the next call uses it
    for x in pg.evaluate("window.__fb.state.call.notes"): tap(pg,x['s'],x['f'])
    wait_phase(pg,'review',120); time.sleep(0.5); drag(pg,"#paTempo",64); time.sleep(0.3); print('dragged to 64 during review ->',pg.evaluate("window.__fb.bpm()"))
    for _ in range(40):
        if not pg.evaluate("document.getElementById('btnNext').disabled"): break
        time.sleep(0.1)
    pg.click("#btnNext"); time.sleep(0.5); print('next call (listening) tempo:',pg.evaluate("window.__fb.bpm()"))
    # change while the tech is playing: should wait for the next call
    drag(pg,"#paTempo",100); time.sleep(0.3); print('dragged to 100 while listening ->',pg.evaluate("window.__fb.bpm()"),'| label:',pg.evaluate("document.getElementById('paBpm').innerText"))
    wait_phase(pg,'answer',250)
    for x in pg.evaluate("window.__fb.state.call.notes"): tap(pg,x['s'],x['f'])
    wait_phase(pg,'review',120)
    for _ in range(40):
        if not pg.evaluate("document.getElementById('btnNext').disabled"): break
        time.sleep(0.1)
    pg.click("#btnNext"); time.sleep(0.6); print('the call after that runs at:',pg.evaluate("window.__fb.bpm()"),'| label:',pg.evaluate("document.getElementById('paBpm').innerText"))
    print('errors',errs); b.close()
