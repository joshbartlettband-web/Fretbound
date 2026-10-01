import time,json
from playwright.sync_api import sync_playwright
from PIL import Image
shots={}
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    for vw,vh in [(360,740),(390,844),(740,360),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:300]))
        pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.5)
        pg.evaluate("()=>{ const d=window.__fb.dexC; const t=window.__fb.TOURS_(); ['spur','tide','dunes','sebene'].forEach((id,i)=>{ const c=d(id); c.faced=2+i; c.won=1+(i%2); c.lost=i%3; c.best=3400+i*500; c.band=i?['lou','hale']:[]; }); }")
        pg.click("#btnBackstage"); time.sleep(0.6); pg.screenshot(path=f"bs_hub_{vw}.png")
        hub=pg.evaluate("()=>({scroll:document.scrollingElement.scrollHeight>innerHeight, over:[...document.querySelectorAll('#scr-backstage .check *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&(r.bottom>innerHeight+1||r.right>innerWidth+1||r.left<-1);}).length, doors:[...document.querySelectorAll('.bs-door')].length})")
        pg.click("[data-door=roster]"); time.sleep(0.5); pg.screenshot(path=f"bs_roster_{vw}.png")
        ros=pg.evaluate("()=>({sub:document.getElementById('rosterSub').innerText, tiles:document.querySelectorAll('.rtile').length, over:[...document.querySelectorAll('#scr-roster .check *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&(r.bottom>innerHeight+1||r.right>innerWidth+1||r.left<-1);}).length, conts:[...document.querySelectorAll('.rconts .ttab')].map(e=>e.textContent)})")
        pg.click(".rtile >> nth=0"); time.sleep(0.4); pg.screenshot(path=f"bs_card_{vw}.png")
        card=pg.evaluate("()=>{ const c=document.getElementById('modalCard'), q=c.getBoundingClientRect(); return {scrollable:c.scrollHeight>c.clientHeight+1,top:Math.round(q.top),bottom:Math.round(q.bottom),vh:innerHeight}; }")
        print(vw,vh,'HUB',hub,'| ROSTER',ros,'| CARD',card); pg.close()
    print('errors',errs); b.close()
