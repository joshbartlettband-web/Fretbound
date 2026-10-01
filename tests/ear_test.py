import time,json,random
from playwright.sync_api import sync_playwright
from PIL import Image
random.seed(7); OPEN=[64,59,55,50,45,40]
fret={}; pc={}
for s in range(6):
    for f in range(16):
        if s<3 and f>12 and random.random()<0.7: continue
        if random.random()<0.25: continue
        n=random.randint(2,9); weak=(s>=3 and f>=9)
        p=0.42 if weak else 0.93
        ok=sum(1 for _ in range(n) if random.random()<p); ms=int(n*(4200 if weak else 1500)*random.uniform(0.8,1.25))
        fret[f"{s},{f}"]={'n':n,'ok':ok,'ms':ms}
        k=str((OPEN[s]+f)%12); q=pc.setdefault(k,{'n':0,'ok':0,'ms':0}); q['n']+=n; q['ok']+=ok; q['ms']+=ms
stats={'fifth':{'seen':12,'correct':10,'lastMissed':False},'octave':{'seen':6,'correct':6,'lastMissed':False},'m3':{'seen':7,'correct':3,'lastMissed':True},'maj':{'seen':5,'correct':2,'lastMissed':True}}
def seed(pg,data=True):
    pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.4)
    if data: pg.evaluate("""d=>{ const k=Object.keys(localStorage).find(x=>localStorage.getItem(x).includes('settings'))||'fretbound'; let S={}; try{ S=JSON.parse(localStorage.getItem(k)||'{}'); }catch(e){} S.fret=d.fret; S.pc=d.pc; S.stats=d.stats; localStorage.setItem(k,JSON.stringify(S)); }""",{'fret':fret,'pc':pc,'stats':stats}); pg.reload(); time.sleep(0.5)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    for vw,vh in [(360,740),(390,844),(740,360),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:300]))
        pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4); seed(pg)
        pg.click("#btnBackstage"); time.sleep(0.4); pg.click("[data-door=ear]"); time.sleep(0.6)
        pg.evaluate("()=>{ const c=document.querySelector('.ear-map'); const r=c.getBoundingClientRect(), G=c.__geo; c.dispatchEvent(new PointerEvent('pointerdown',{clientX:r.left+G.lab+11.5*G.cw,clientY:r.top+4.5*G.rh,bubbles:true})); }"); time.sleep(0.2)
        pg.screenshot(path=f"ear_full_{vw}.png")
        full=pg.evaluate("()=>({scroll:document.scrollingElement.scrollHeight>innerHeight, over:[...document.querySelectorAll('#scr-ear .check *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&(r.bottom>innerHeight+1||r.right>innerWidth+1||r.left<-1);}).length, take:document.querySelector('.ear-take').innerText, detail:document.getElementById('earDetail').innerText})")
        pg.click(".ear-mode button >> nth=1"); time.sleep(0.3); pg.screenshot(path=f"ear_speed_{vw}.png")
        pg.click("#btnEarBack"); time.sleep(0.3); pg.click("#btnBsBack"); time.sleep(0.3)
        pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
        pg.evaluate("window.__fb.state.over='win'; window.__fb.state.cleared=['spur','tide','juke']; window.__fb.results()"); time.sleep(0.4); pg.click(".tab[data-t=map]"); time.sleep(0.5); pg.screenshot(path=f"ear_results_{vw}.png")
        res=pg.evaluate("()=>({scroll:document.querySelector('#scr-results .tabbody').scrollHeight>document.querySelector('#scr-results .tabbody').clientHeight+1, pageScroll:document.scrollingElement.scrollHeight>innerHeight, over:[...document.querySelectorAll('#scr-results .check *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&(r.bottom>innerHeight+1||r.right>innerWidth+1||r.left<-1);}).length})")
        print(vw,vh,'FULL',{k:v for k,v in full.items() if k in('scroll','over')},'| RESULTS TAB',res)
        if vw==390: print('TAKEAWAY:',full['take']); print('CELL TAP:',full['detail'])
        pg.close()
    print('errors',errs); b.close()
