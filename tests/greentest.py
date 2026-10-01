import time,json,sys
from playwright.sync_api import sync_playwright
OPEN=[64,59,55,50,45,40]
def tap(pg,s,f):
    for tries in range(30):
        st=pg.evaluate("({pos:window.__fb.state.pos,win:window.__fb.state.win,broken:window.__fb.state.broken,g:window.__fb.geo})")
        if st['pos']<=f<st['pos']+st['win']: break
        pg.click("#navR" if f>=st['pos']+st['win'] else "#navL"); time.sleep(0.03)
    g=st['g']; r=pg.evaluate("(()=>{const r=document.getElementById('neck').getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height}})()")
    cc=f-st['pos']; x=r['x']+((g['bounds'][cc]+g['bounds'][cc+1])/2)/g['cw']*r['w']; y=r['y']+g['sy'][s]/g['ch']*r['h']; pg.mouse.click(x,y); time.sleep(0.25)
def wait_phase(pg,ph,n=200):
    for _ in range(n):
        if pg.evaluate("window.__fb.state.phase")==ph: return True
        time.sleep(0.1)
    return False
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    pg=b.new_page(viewport={"width":390,"height":844}); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:400]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.5)
    pg.evaluate("window.__fbNoRecruit=true")
    pg.click("#btnBackstage"); time.sleep(0.3); pg.click("[data-door=green]"); time.sleep(0.3)
    # choose: intervals, only P5 and M3, frets 5-8, high strings, 88 bpm
    for a,v in [('frets','b'),('strings','high')]: pg.click(f"[data-a={a}][data-v={v}]"); time.sleep(0.1)
    pg.click("#btnGreenGo"); time.sleep(0.6)
    st=pg.evaluate("({practice:window.__fb.state.practice,cls:document.getElementById('scr-duel').className,venue:document.getElementById('venueName').innerText,cash:document.getElementById('topCash').innerText,board:getComputedStyle(document.getElementById('board')).display,aids:getComputedStyle(document.getElementById('pracAids')).display,hands:window.__fb.PR_().hands.length,fr:window.__fb.PR_().fr,str:window.__fb.PR_().str})")
    print('SESSION START:',st)
    results=[]; before=pg.evaluate("({money:window.__fb.state.money,total:window.__fb.state.total})")
    for n in range(6):
        if not wait_phase(pg,'answer',250): print('never reached answer phase at call',n); break
        call=pg.evaluate("({id:window.__fb.state.call.hand.id,notes:window.__fb.state.call.notes,relaxed:window.__fb.PR_().relaxed})")
        inrange=all(5<=x['f']<=8 and x['s']<=2 for x in call['notes'])
        miss = (n in (2,4))
        notes=call['notes']
        for k,x in enumerate(notes):
            s,f=x['s'],x['f']
            if miss and k==len(notes)-1:
                # play a wrong note: the same cell one fret up (different pitch)
                f=min(15,f+1) if f<15 else f-1
            tap(pg,s,f)
        ok=wait_phase(pg,'review',120)
        time.sleep(0.4)
        hud=pg.evaluate("({found:document.getElementById('totalNum').innerText,calls:document.getElementById('targetNum').innerText,streak:document.getElementById('topCash').innerText,dots:document.querySelectorAll('#paDots i').length,nextDisabled:document.getElementById('btnNext').disabled})")
        results.append((call['id'],len(notes),'in-range' if inrange else 'RELAXED/OUT',call['relaxed'],'miss' if miss else 'hit',hud['found']+'/'+hud['calls'],hud['streak'],hud['dots']))
        for _ in range(40):
            if not pg.evaluate("document.getElementById('btnNext').disabled"): break
            time.sleep(0.1)
        if n<5: pg.click("#btnNext"); time.sleep(0.4)
    for r in results: print(' call',r)
    after=pg.evaluate("({money:window.__fb.state.money,total:window.__fb.state.total,cells:(()=>{const k=Object.keys(localStorage).find(x=>localStorage.getItem(x).includes('settings')); const S=JSON.parse(localStorage.getItem(k)); return Object.keys(S.fret||{}).length+' cells, '+Object.values(S.fret||{}).reduce((a,r)=>a+r.n,0)+' notes logged';})()})")
    print('BEFORE',before,'AFTER',after)
    pg.click("#paDone"); time.sleep(0.5); print('SUMMARY:',pg.evaluate("document.querySelector('#modalCard').innerText.replace(/\\n+/g,' | ')")); pg.screenshot(path='green_summary.png')
    pg.click("#gsBack"); time.sleep(0.5); print('AFTER BACK: screen',pg.evaluate("window.__fb.state.screen"),'| practice flag',pg.evaluate("window.__fb.state.practice"),'| duel class',pg.evaluate("document.getElementById('scr-duel').className"))
    print('errors',errs); b.close()
