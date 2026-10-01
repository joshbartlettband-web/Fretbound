import time,sys
from playwright.sync_api import sync_playwright
OPEN=[64,59,55,50,45,40]
ev=lambda pg,js: pg.evaluate(js)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":760})
    errs=[]; pg.on("pageerror",lambda e: errs.append(str(e.stack)[:300]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4)
    pg.evaluate("()=>{ const M=window.__fb.META; Object.assign(M,{fame:100,van:{bigvan:2},hired:{jo:1,dee:1,tam:1,hale:1},lineup:[\'jo\',\'dee\',\'tam\',\'hale\']}); }")
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.1)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
    if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    print("venue:",ev(pg,"window.__fb.state.venueIdx"), ev(pg,"document.getElementById('venueName').textContent"))
    pg.click("#vcGo"); time.sleep(0.2)
    for c in range(3):
        for _ in range(150):
            if ev(pg,"window.__fb.state.phase")=="answer": break
            time.sleep(0.1)
        if c==1:
            pg.click("#btnReplay"); time.sleep(0.2); print(" replay phase:",ev(pg,"window.__fb.state.phase"))
            for _ in range(150):
                if ev(pg,"window.__fb.state.phase")=="answer": break
                time.sleep(0.1)
        notes=ev(pg,"window.__fb.state.call.notes")
        for k,n in enumerate(notes):
            midi=n['midi']+(1 if (c in (0,1) and k==len(notes)-1) else 0)   # botch the last note of call 1
            for tries in range(25):
                s2=ev(pg,"({pos:window.__fb.state.pos,win:window.__fb.state.win,broken:window.__fb.state.broken,g:window.__fb.geo})")
                found=None
                for s in range(6):
                    f=midi-OPEN[s]
                    if not s2['broken'][s] and s2['pos']<=f<s2['pos']+s2['win'] and 0<=f<=15: found=(s,f); break
                if found: break
                anyf=[midi-OPEN[s] for s in range(6) if not s2['broken'][s] and 0<=midi-OPEN[s]<=15][0]
                pg.click("#navR" if anyf>=s2['pos']+s2['win'] else "#navL")
            s,f=found; g=s2['g']
            r=ev(pg,"(()=>{const r=document.getElementById('neck').getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height}})()")
            cc=f-s2['pos']; x=r['x']+((g['bounds'][cc]+g['bounds'][cc+1])/2)/g['cw']*r['w']; y=r['y']+g['sy'][s]/g['ch']*r['h']
            pg.mouse.click(x,y); time.sleep(0.3)
        time.sleep(0.3)
        time.sleep(1.2); print(f" call {c+1}: lineup {ev(pg,'window.__fb.state.lineup')} | gauge {ev(pg,'window.__fb.state.gauge')} heavySaved {ev(pg,'window.__fb.state.heavySaved')} techUsed {ev(pg,'window.__fb.state.techUsed')} | tape delay now {ev(pg,'window.__fb.tapeDelay&&window.__fb.tapeDelay()')}, streak {ev(pg,'window.__fb.state.streak')}, broken {sum(ev(pg,'window.__fb.state.broken'))}")
        for _ in range(150):
            if ev(pg,"window.__fb.state.phase")=="review" and not ev(pg,"document.getElementById('btnNext').disabled"): break
            time.sleep(0.1)
        if ev(pg,"window.__fb.state.over"): break
        pg.click("#btnNext"); time.sleep(0.4)
    print("total",ev(pg,"window.__fb.state.total"),"errors:",errs)
    b.close()
