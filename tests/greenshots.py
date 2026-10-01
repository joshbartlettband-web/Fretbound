import time,sys
from playwright.sync_api import sync_playwright
from PIL import Image
sys.argv=['x']; exec(open('/home/claude/greentest.py').read().split("with sync_playwright() as p:")[0])
shots={}
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    for vw,vh in [(360,740),(390,844),(740,360),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:300]))
        pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.5)
        pg.click("#btnBackstage"); time.sleep(0.3); pg.click("[data-door=green]"); time.sleep(0.4)
        pg.screenshot(path=f"gr_setup_{vw}.png")
        setup=pg.evaluate("()=>({scroll:document.scrollingElement.scrollHeight>innerHeight, over:[...document.querySelectorAll('#scr-green .check *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&(r.bottom>innerHeight+1||r.right>innerWidth+1||r.left<-1);}).length})")
        pg.click("[data-a=preset][data-v=all]"); pg.click("#btnGreenGo"); time.sleep(0.5)
        wait_phase(pg,'answer',250); time.sleep(0.4); pg.screenshot(path=f"gr_duel_{vw}.png")
        duel=pg.evaluate("()=>({scroll:document.scrollingElement.scrollHeight>innerHeight, over:[...document.querySelectorAll('#scr-duel .duel *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&r.height&&(r.bottom>innerHeight+2||r.right>innerWidth+2||r.left<-2)&&getComputedStyle(e).display!=='none';}).map(e=>e.id||e.className).slice(0,4)})")
        call=pg.evaluate("window.__fb.state.call.notes")
        for x in call: tap(pg,x['s'],x['f'])
        wait_phase(pg,'review',120); time.sleep(2.2); pg.screenshot(path=f"gr_review_{vw}.png")
        pg.click("#paDone"); time.sleep(0.5); pg.screenshot(path=f"gr_sum_{vw}.png")
        card=pg.evaluate("()=>{ const c=document.getElementById('modalCard'); return {scrollable:c.scrollHeight>c.clientHeight+1}; }")
        print(vw,vh,'SETUP',setup,'| DUEL',duel,'| SUMMARY',card); pg.close()
    print('errors',errs); b.close()
a=Image.open('gr_duel_390.png'); c=Image.open('gr_review_390.png'); d=Image.open('gr_setup_390.png')
a=a.resize((a.width//2,a.height//2)); c=c.resize((c.width//2,c.height//2)); d=d.resize((d.width//2,d.height//2))
S=Image.new('RGB',(a.width*3+20,a.height),'black'); S.paste(d,(0,0)); S.paste(a,(a.width+10,0)); S.paste(c,(2*a.width+20,0)); S.save('gr_three.png')
l=Image.open('gr_duel_844.png'); l=l.resize((l.width//2,l.height//2)); l.save('gr_land.png')
