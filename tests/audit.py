import time, json
from playwright.sync_api import sync_playwright
AUDIT="""(()=>{ const out=[]; const vw=innerWidth, vh=innerHeight;
 const roots=[document.querySelector('.screen.active')]; const m=document.querySelector('#modal:not(.hidden)'); if(m) roots.push(m);
 roots.forEach(root=>root.querySelectorAll('*').forEach(el=>{ const cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden') return;
   if(el.closest('.hidden')) return; const r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
   const txt=[...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim());
   const tag=(el.id?'#'+el.id:'')+(typeof el.className==='string'&&el.className?'.'+el.className.split(' ').join('.'):'')||el.tagName;
   if(txt&&el.scrollWidth>el.clientWidth+1&&cs.overflowX!=='visible') out.push('CLIPX '+tag+' "'+el.textContent.trim().slice(0,24)+'" '+el.scrollWidth+'>'+el.clientWidth);
   if(txt&&el.tagName==='BUTTON'&&el.scrollWidth>el.clientWidth+1) out.push('BTNOVER '+tag+' "'+el.textContent.trim().slice(0,24)+'"');
   if(r.right>vw+1.5||r.left<-1.5) out.push('OFFX '+tag+' '+Math.round(r.left)+'..'+Math.round(r.right));
   const w=el.parentElement&&el.parentElement.closest('.win,.pc,.pco,.modal-card'); if(w&&txt){ const R=w.getBoundingClientRect(); if(r.right>R.right+1.5||r.left<R.left-1.5) out.push('SPILL '+tag+' "'+el.textContent.trim().slice(0,20)+'" past '+(w.id||w.className.split(' ')[0])); }
 })); return [...new Set(out)]; })()"""
def ready(pg):
    for _ in range(40):
        if pg.is_visible("#vcGo"): return
        time.sleep(0.1)
def run(w,h):
    res={}
    with sync_playwright() as p:
        b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        pg=b.new_page(viewport={"width":w,"height":h})
        pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','test.html'))); pg.evaluate('window.__fbNoRecruit=true'); time.sleep(0.8); pg.evaluate("window.__fb.store.unlocks={an:true}")
        A=lambda k: res.__setitem__(k,pg.evaluate(AUDIT))
        A('title'); pg.click("#btnStart"); time.sleep(0.3)
        print("  chars overflow:",pg.evaluate("(()=>{const e=document.querySelector('#scr-chars .check'); return e.scrollHeight-e.clientHeight})()"))
        for i in range(6): pg.query_selector_all("#charTiles .ctile")[i].click(); time.sleep(0.05); A('chars'+str(i))
        pg.query_selector_all("#charTiles .ctile")[0].click(); pg.click("#btnCharGo"); time.sleep(0.3)
        for i in range(5): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05); A('check'+str(i))
        pg.click("#btnSound"); time.sleep(0.2); A('settings'); pg.click("#pRes")
        pg.click("#btnHowto2"); time.sleep(0.2); A('howto'); pg.click("#mOk")
        pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.2)
        ready(pg); A('venuecard'); pg.click("#vcGo"); time.sleep(4.5); A('duel')
        for i in range(3):
            for tries in range(5):
                try: pg.query_selector_all("#board .pedal")[i].click(); break
                except Exception: time.sleep(0.3)
            time.sleep(0.15); A('pedalmodal'+str(i)); pg.click("#pmC")
        pg.evaluate("window.__fb.shop()"); time.sleep(0.4); A('shop')
        for k in range(3): pg.query_selector_all("#shopOffer .ptile")[k].click(); time.sleep(0.15); A('shopcard'+str(k)); pg.query_selector_all("#smActs .btn, #bmActs .btn")[-1].click()
        pg.evaluate("window.__fb.state.over='win'; window.__fb.state.cleared=['spur','tide','juke']; window.__fb.results()"); time.sleep(0.3); A('results')
        pg.click("#scr-results .tab[data-t=notes]"); time.sleep(0.2); A('notes')
        print("  results body overflow:",pg.evaluate("(()=>{const e=document.querySelector('#scr-results .tabbody'); return e.scrollHeight-e.clientHeight})()"),"chars overflow:",pg.evaluate("(()=>{const e=document.querySelector('#scr-chars .check'); return e.scrollHeight-e.clientHeight})()") if False else '')
        b.close()
    return res
for vp in [(360,740),(390,760),(412,860),(740,360),(844,390)]:
    r=run(*vp); flat=sorted(set(x for v in r.values() for x in v))
    print(vp, len(flat), "issues")
    for x in flat[:40]: print("   ",x)
