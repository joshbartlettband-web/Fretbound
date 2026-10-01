import time,sys,json
from playwright.sync_api import sync_playwright
F=sys.argv[1]
JS_SETUP="""()=>{
  const o=window.__masterOut, c=o.context, an=c.createAnalyser(); an.fftSize=4096; o.connect(an); window.__an=an; window.__buf=new Float32Array(4096);
  window.__rms=function(ms){ return new Promise(function(res){ const acc=[]; const iv=setInterval(function(){ an.getFloatTimeDomainData(window.__buf); let s=0,pk=0; for(const v of window.__buf){ s+=v*v; pk=Math.max(pk,Math.abs(v)); } acc.push([s/window.__buf.length,pk]); },40);
    setTimeout(function(){ clearInterval(iv); const m=acc.reduce(function(a,x){ return a+x[0]; },0)/acc.length; res({db:Math.round(10*Math.log10(m+1e-12)*10)/10,pk:Math.round(Math.max.apply(null,acc.map(function(x){ return x[1]; }))*1000)/1000}); },ms); }); };
}"""
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); pg=b.new_page(viewport={"width":390,"height":844}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e.stack)[:200]))
    pg.goto("file:///home/claude/"+F); time.sleep(0.4); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.4)
    pg.evaluate("()=>{ window.__fbNoRecruit=true; Object.assign(window.__fb.META,{hired:{lou:1,dee:1,jo:1},lineup:['lou','dee','jo']}); }")
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.4)
    for _ in range(3):
        if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.3)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    pg.click("#vcGo")
    for _ in range(200):
        if pg.evaluate("window.__fb.state.phase")=="answer": break
        time.sleep(0.1)
    pg.evaluate(JS_SETUP); time.sleep(0.3)
    band=pg.evaluate("window.__rms(2500)")
    pg.evaluate("()=>{ window.__mb=window.__dbg.mb(); window.__mb.gain.value=0; }")
    pg.evaluate("()=>{ const d=window.__dbg; [[5,40],[4,47],[3,52]].forEach((n,k)=>d.pl(n[0],n[1]+k*0)); }")
    guitar=pg.evaluate("window.__rms(1200)")
    print(json.dumps({'band_only':band,'player_notes_only':guitar,'errors':errs})); b.close()
