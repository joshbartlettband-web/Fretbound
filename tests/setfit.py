import time
from playwright.sync_api import sync_playwright
from PIL import Image
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for vw,vh in [(360,740),(390,844),(412,860),(740,360),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh},device_scale_factor=2); pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.4)
        pg.evaluate("window.__fbNoRecruit=true"); pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.4); pg.click("#btnSound"); time.sleep(0.5)
        r=pg.evaluate("()=>{ const c=document.getElementById('modalCard'), q=c.getBoundingClientRect(); return {top:Math.round(q.top),bottom:Math.round(q.bottom),vh:innerHeight,scrollable:c.scrollHeight>c.clientHeight+1,pageScroll:document.scrollingElement.scrollHeight>innerHeight}; }")
        print(vw,vh,r,'OK' if (r['top']>=0 and r['bottom']<=r['vh'] and not r['scrollable']) else 'CHECK')
        if vw in (360,844): pg.screenshot(path=f"set_{vw}.png"); shots.append(Image.open(f"set_{vw}.png"))
        pg.close()
    b.close()
a,c=shots; a=a.resize((a.width//2,a.height//2)); c=c.resize((c.width//2,c.height//2))
S=Image.new('RGB',(a.width+c.width+10,max(a.height,c.height)),'black'); S.paste(a,(0,0)); S.paste(c,(a.width+10,0)); S.save('set_both.png'); print(S.size)
