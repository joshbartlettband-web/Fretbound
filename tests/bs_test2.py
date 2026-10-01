import time
from playwright.sync_api import sync_playwright
from PIL import Image
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    for vw,vh,tag in [(390,844,'p'),(844,390,'l')]:
        pg=b.new_page(viewport={"width":vw,"height":vh},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:300]))
        pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.5)
        pg.evaluate("()=>{ Object.assign(window.__fb.META,{hired:{lou:1,dee:1},lineup:['lou','dee'],met:{hale:1}}); const d=window.__fb.dexC; ['spur','tide','juke'].forEach(id=>{ const c=d(id); c.faced=3; c.won=2; c.lost=1; c.best=4200; c.band=['lou','rosa']; }); }")
        if tag=='p': pg.screenshot(path='bs_title_p.png')
        pg.click("#btnBackstage"); time.sleep(0.4); pg.click("[data-door=roster]"); time.sleep(0.4)
        pg.screenshot(path=f"bs_roster_full_{tag}.png")
        pg.click(".roster-tabs .tab >> nth=1"); time.sleep(0.4); pg.screenshot(path=f"bs_band_{tag}.png")
        over=pg.evaluate("()=>({scroll:document.scrollingElement.scrollHeight>innerHeight, over:[...document.querySelectorAll('#scr-roster .check *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&(r.bottom>innerHeight+1||r.right>innerWidth+1||r.left<-1);}).length})")
        pg.click(".rtile >> nth=3"); time.sleep(0.3); pg.screenshot(path=f"bs_mcard_{tag}.png")
        card=pg.evaluate("()=>{ const c=document.getElementById('modalCard'); return {scrollable:c.scrollHeight>c.clientHeight+1}; }")
        print(tag,vw,vh,'band tab',over,'member card',card); pg.close()
    print('errors',errs); b.close()
for tag,sz in [('p',(390,844))]:
    pass
a=Image.open('bs_band_p.png'); c=Image.open('bs_mcard_p.png'); t=Image.open('bs_title_p.png')
a=a.resize((a.width//2,a.height//2)); c=c.resize((c.width//2,c.height//2)); t=t.resize((t.width//2,t.height//2))
S=Image.new('RGB',(a.width*3+20,a.height),'black'); S.paste(t,(0,0)); S.paste(a,(a.width+10,0)); S.paste(c,(2*a.width+20,0)); S.save('bs_three2.png')
l1=Image.open('bs_roster_full_l.png'); l2=Image.open('bs_band_l.png'); l1=l1.resize((l1.width//2,l1.height//2)); l2=l2.resize((l2.width//2,l2.height//2))
S2=Image.new('RGB',(l1.width+l2.width+10,l1.height),'black'); S2.paste(l1,(0,0)); S2.paste(l2,(l1.width+10,0)); S2.save('bs_land.png')
