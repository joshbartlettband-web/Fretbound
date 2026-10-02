import time
from playwright.sync_api import sync_playwright
OPEN=[64,59,55,50,45,40]
def ev(pg,js): return pg.evaluate(js)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":760},device_scale_factor=2)
    errs=[]; pg.on("pageerror",lambda e: errs.append(str(e))); pg.on("console",lambda m: errs.append(m.text) if m.type=="error" and "403" not in m.text else None)
    pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','test.html'))); time.sleep(0.4)
    pg.click("#btnStart"); time.sleep(0.4)
    pg.click("#btnCharGo"); time.sleep(0.4)
    lv=ev(pg,"window.__fb.levelTest()")
    for k,v in lv.items():
        if k.startswith('rival') : print(" ",k,v)
    pg.screenshot(path="t_title.png") if False else None
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.15)
    pg.screenshot(path="t_check_cards.png")
    print("check scroll overflow:", pg.evaluate("(()=>{const e=document.querySelector('#scr-check .check'); return e.scrollHeight-e.clientHeight})()"))
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
    if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
    for night in range(3):
        for _ in range(40):
            if pg.is_visible("#vcGo"): break
            time.sleep(0.1)
        pg.screenshot(path=f"t_card{night}.png")
        pg.click("#vcGo"); time.sleep(0.2)
        over=None; c=0
        while not over:
            for _ in range(120):
                if ev(pg,"window.__fb.state.phase")=="answer": break
                time.sleep(0.1)
            if c==0: pg.screenshot(path=f"t_duel{night}.png")
            st=ev(pg,"({call:window.__fb.state.call})")
            for k,n in enumerate(st['call']['notes']):
                midi=n['midi']+(1 if (night==1 and c==0 and k==1) else 0)
                for tries in range(25):
                    s2=ev(pg,"({pos:window.__fb.state.pos,win:window.__fb.state.win,broken:window.__fb.state.broken,g:window.__fb.geo})")
                    found=None
                    for s in range(6):
                        if s2['broken'][s]: continue
                        f=midi-OPEN[s]
                        if s2['pos']<=f<s2['pos']+s2['win'] and 0<=f<=15: found=(s,f); break
                    if found: break
                    anyf=[midi-OPEN[s] for s in range(6) if not s2['broken'][s] and 0<=midi-OPEN[s]<=15][0]
                    pg.click("#navR" if anyf>=s2['pos']+s2['win'] else "#navL")
                s,f=found; g=s2['g']
                r=ev(pg,"(()=>{const r=document.getElementById('neck').getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height}})()")
                cc=f-s2['pos']; x=r['x']+((g['bounds'][cc]+g['bounds'][cc+1])/2)/g['cw']*r['w']; y=r['y']+g['sy'][s]/g['ch']*r['h']
                pg.mouse.click(x,y); time.sleep(0.3)
            for _ in range(150):
                if ev(pg,"window.__fb.state.phase")=="review" and not ev(pg,"document.getElementById('btnNext').disabled"): break
                time.sleep(0.1)
            over=ev(pg,"window.__fb.state.over"); c+=1
            if night==0 and c==1:
                pg.query_selector_all("#board .pedal")[1].click(); time.sleep(0.3); pg.screenshot(path="t_pedalmodal.png"); pg.click("#pmC"); time.sleep(0.2)
            pg.click("#btnNext"); time.sleep(0.5)
        print("night",night,"over",over,"total",ev(pg,"window.__fb.state.total"),"money",ev(pg,"window.__fb.state.money"))
        if over!='win' or night==2: break
        time.sleep(0.4); pg.screenshot(path=f"t_shop{night}.png")
        print("shop scroll overflow:", pg.evaluate("(()=>{const e=document.querySelector('#scr-shop .check'); return e.scrollHeight-e.clientHeight})()"))
        bought=False
        for k in range(3):
            pg.query_selector_all("#shopOffer .ptile")[k].click(); time.sleep(0.2)
            btns=pg.query_selector_all("#smActs .btn, #bmActs .btn")
            if btns and btns[0].inner_text().startswith("BUY") and btns[0].is_enabled(): btns[0].click(); time.sleep(0.3); bought=True; break
            pg.query_selector_all("#smActs .btn, #bmActs .btn")[-1].click(); time.sleep(0.15)
        if pg.query_selector("#btnRestring").is_enabled(): pg.click("#btnRestring"); time.sleep(0.2)
        pg.query_selector_all("#shopBoard .ptile")[0].click(); time.sleep(0.2)
        pg.screenshot(path=f"t_shopb{night}.png"); pg.query_selector_all("#smActs .btn, #bmActs .btn")[-1].click(); time.sleep(0.15)
        print("bought:",bought,"board:",pg.evaluate("window.__fb.state.pedals.length"))
        pg.click("#btnNextGig"); time.sleep(0.5)
    time.sleep(0.5); pg.screenshot(path="t_results.png")
    print("results scroll overflow:", pg.evaluate("(()=>{const e=document.querySelector('#scr-results .check'); return e.scrollHeight-e.clientHeight})()"))
    pg.click("#scr-results .tab[data-t=notes]"); time.sleep(0.2); pg.screenshot(path="t_results2.png")
    print("errors:",errs); b.close()
