import os, time, json
from playwright.sync_api import sync_playwright
# First-night tutorial (v2.03), forced on with window.__fbTut (it is off under automation otherwise).
# A fresh player goes from character select straight to night 1 with the starter board, sees the tips in the caption strip,
# gets the payday note at the merch table, and the next run starts with the normal pedal pick.
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
OPEN=[64,59,55,50,45,40]
ev=lambda pg,js: pg.evaluate(js)
fails=[]
def check(ok,msg):
    print(('  ok   ' if ok else '  FAIL ')+msg)
    if not ok: fails.append(msg)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":844})
    errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.add_init_script("window.__fbTut=true; window.__fbNoRecruit=true")
    pg.goto('file://'+REPO+'/index.html'); time.sleep(0.8)
    pg.evaluate("""window.__tips=[]; (()=>{ const d=document.getElementById('dialog'); new MutationObserver(()=>{ if(d.classList.contains('coach')){ const t=d.textContent; if(t&&!window.__tips.includes(t)) window.__tips.push(t); } }).observe(d,{childList:true,subtree:true,characterData:true,attributes:true}); })()""")
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.6)
    check(ev(pg,"window.__fb.state.screen")=='duel','character select goes straight to night 1 (no pedal pick, no How to Play)')
    check(ev(pg,"window.__fb.state.pedals.map(p=>p.id).join(',')")=='iron,ogre,echo','starter board is Iron Comp, Ogre Drive, Echo Well')
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    pg.click("#vcGo"); time.sleep(0.2)
    for c in range(8):
        for _ in range(200):
            if ev(pg,"window.__fb.state.phase")=="answer": break
            time.sleep(0.1)
        time.sleep(0.2)
        notes=ev(pg,"window.__fb.state.call.notes")
        for k,n in enumerate(notes):
            midi=n['midi']+(1 if (c==0 and k==len(notes)-1) else 0)   # botch the last note of call 1, to see the snap tip
            for tries in range(25):
                s2=ev(pg,"({pos:window.__fb.state.pos,win:window.__fb.state.win,broken:window.__fb.state.broken,g:window.__fb.geo})")
                found=None
                for s in range(6):
                    f=midi-OPEN[s]
                    if not s2['broken'][s] and s2['pos']<=f<s2['pos']+s2['win'] and 0<=f<=15: found=(s,f); break
                if found: break
                anyf=[midi-OPEN[s] for s in range(6) if not s2['broken'][s] and 0<=midi-OPEN[s]<=15][0]
                pg.click("#navR" if anyf>=s2['pos']+s2['win'] else "#navL"); time.sleep(0.35)
            s,f=found; g=s2['g']
            r=ev(pg,"(()=>{const r=document.getElementById('neck').getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height}})()")
            cc=f-s2['pos']; x=r['x']+((g['bounds'][cc]+g['bounds'][cc+1])/2)/g['cw']*r['w']; y=r['y']+g['sy'][s]/g['ch']*r['h']
            pg.mouse.click(x,y); time.sleep(0.3)
        if c==0: pg.screenshot(path=f'{OUT}/tut_call1.png')
        for _ in range(200):
            if ev(pg,"window.__fb.state.phase")=="review" and not ev(pg,"document.getElementById('btnNext').disabled"): break
            time.sleep(0.1)
        if ev(pg,"window.__fb.state.over"): break
        pg.click("#btnNext"); time.sleep(0.4)
    tips=ev(pg,"window.__tips")
    print('  tips seen:'); [print('     ',t) for t in tips]
    over=ev(pg,"window.__fb.state.over"); print('  night 1:',over,'total',ev(pg,"window.__fb.state.total"))
    calls=ev(pg,"window.__fb.state.callIdx"); print('  calls played:',calls)
    check(len(tips)>=4,'at least four tips during night 1')
    for key in ['Listen.','Your turn.','snaps its string','Tone x Hype']+(['REPLAY'] if calls>=3 else []):
        check(any(key in t for t in tips),'tip shown: '+key)
    check(ev(pg,"window.__fb.tutState().done") is True,'tutorial marked done when the night ends')
    if over=='win':
        pg.click("#btnNext"); time.sleep(1.2)
        check(ev(pg,"window.__fb.state.screen")=='shop','cash out goes to the merch table')
        check(pg.is_visible('#mOk') and 'Payday' in ev(pg,"document.getElementById('modalCard').textContent"),'payday note pops up at the merch table')
        pg.screenshot(path=f'{OUT}/tut_shop.png')
        print('  shop note:',ev(pg,"document.getElementById('modalCard').textContent"))
        pg.click('#mOk'); time.sleep(0.3)
        check(ev(pg,"window.__fb.state.screen")=='shop' and not pg.is_visible('#mOk'),'GOT IT closes the note')
        pg.click('#btnNextGig'); time.sleep(0.6)
        check(not ev(pg,"window.__fb.state.tutShop"),'payday note cleared after NEXT SHOW')
    pg.evaluate("window.__fb.state.runId++"); pg.evaluate("document.getElementById('btnPause').click()"); time.sleep(0.2)
    if pg.is_visible('#pQuit'): pg.click('#pQuit'); time.sleep(0.4)
    else: pg.evaluate("document.querySelector('#modal .btn#pRes')&&document.querySelector('#modal .btn#pRes').click()")
    if ev(pg,"window.__fb.state.screen")!='title': pg.evaluate("window.__fb.state.runId++"); pg.evaluate("document.querySelectorAll('.screen').forEach(s=>s.classList.toggle('active',s.id==='scr-title'))"); pg.evaluate("window.__fb.state.screen='title'")
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.5)
    check(ev(pg,"window.__fb.state.screen")=='check','second run opens the normal pedal pick')
    check(not errs,'no page errors '+str(errs[:3]))
    b.close()
print('problems:',len(fails))
