# Play a few calls on every night of every tour with a full band, a different player each night, and screenshot each phase.
# usage: OUT=/tmp/tour python3 tests/dev/playtour.py [WxH] [tour ...]     writes <OUT>/<venue>_<phase>.png and <OUT>/report.json (errors, totals)
import os,sys,time,json
from playwright.sync_api import sync_playwright
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')); OUT=os.environ.get('OUT','/tmp/tour'); os.makedirs(OUT,exist_ok=True)
size=[a for a in sys.argv[1:] if 'x' in a]; W,H=map(int,(size[0] if size else '390x844').split('x')); tours=[a for a in sys.argv[1:] if 'x' not in a]
OPEN=[64,59,55,50,45,40]; CH=['bard','monk','hermit','busker','luthier','carto']
ev=lambda pg,js: pg.evaluate(js)
def wait(pg,cond,n=200):
    for _ in range(n):
        if ev(pg,cond): return True
        time.sleep(0.1)
    return False
def answer(pg,wrong=False):
    notes=ev(pg,"window.__fb.state.call.notes"); OPEN=ev(pg,"window.__fb.open()")
    for k,n in enumerate(notes):
        midi=n['midi']+(1 if wrong and k==len(notes)-1 else 0); found=None
        for _ in range(25):
            s2=ev(pg,"({pos:window.__fb.state.pos,win:window.__fb.state.win,broken:window.__fb.state.broken,g:window.__fb.geo})")
            for s in range(len(OPEN)):
                f=midi-OPEN[s]
                if not s2['broken'][s] and s2['pos']<=f<s2['pos']+s2['win'] and 0<=f<=15: found=(s,f); break
            if found: break
            cand=[midi-OPEN[s] for s in range(len(OPEN)) if not s2['broken'][s] and 0<=midi-OPEN[s]<=15]
            if not cand: return False
            pg.click("#navR" if cand[0]>=s2['pos']+s2['win'] else "#navL"); time.sleep(0.35)
        if not found: return False
        s,f=found; g=s2['g']; r=ev(pg,"(()=>{const r=document.getElementById('neck').getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height}})()")
        cc=f-s2['pos']; pg.mouse.click(r['x']+((g['bounds'][cc]+g['bounds'][cc+1])/2)/g['cw']*r['w'], r['y']+g['sy'][s]/g['ch']*r['h']); time.sleep(0.25)
    return True
rep={'errors':[],'nights':[]}
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); pg=b.new_page(viewport={"width":W,"height":H}); pg.add_init_script("window.__fbNoWarm=true"); 
    pg.on("pageerror",lambda e: rep['errors'].append(str(e)[:300])); pg.on("console",lambda m: rep['errors'].append(m.text[:300]) if m.type=='error' else None)
    pg.goto('file://'+REPO+'/index.html'); time.sleep(1.5)
    T=ev(pg,"window.__fb.tours()"); k=0
    for ti,t in enumerate(T):
        if tours and t['id'] not in tours: continue
        for vi,vid in enumerate(t['v']):
            ch=CH[k%6]; k+=1
            ev(pg,f"window.__fb.dev({ti},{vi},true,'{ch}')"); time.sleep(0.6)
            if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
            wait(pg,"!!document.getElementById('vcGo')&&document.getElementById('vcGo').offsetParent!==null",60)
            pg.screenshot(path=f'{OUT}/{vid}_0card.png')
            if pg.is_visible("#vcGo"): pg.click("#vcGo")
            time.sleep(0.8); pg.screenshot(path=f'{OUT}/{vid}_1intro.png')
            night={'venue':vid,'char':ch,'calls':[]}
            for c in range(2):
                if not wait(pg,"window.__fb.state.phase==='answer'",250): night['calls'].append('no answer phase'); break
                if c==0: pg.screenshot(path=f'{OUT}/{vid}_2answer.png')
                ok=answer(pg,wrong=(c==1))
                wait(pg,"window.__fb.state.phase==='review'&&!document.getElementById('btnNext').disabled",200); time.sleep(0.2)
                pg.screenshot(path=f'{OUT}/{vid}_{3+c}review.png'); night['calls'].append(dict(ok=ok,total=ev(pg,"window.__fb.state.total")))
                if ev(pg,"window.__fb.state.over") or not pg.is_visible("#btnNext"): break
                pg.click("#btnNext"); time.sleep(0.4)
            if ev(pg,"window.__fb.state.screen")=='duel': ev(pg,"window.__fb.devWin()")
            time.sleep(1.0); pg.screenshot(path=f'{OUT}/{vid}_5after.png')
            rep['nights'].append(night); print(vid,ch,night['calls'],len(rep['errors']),flush=True)
    json.dump(rep,open(f'{OUT}/report.json','w'),indent=1); print('errors',rep['errors'][:10])
