import time
from playwright.sync_api import sync_playwright
from PIL import Image
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(); errs=[]
    for vw,vh,tab in [(360,740,'vanList'),(390,844,'vanCrew'),(844,390,'vanList')]:
        pg=b.new_page(viewport={"width":vw,"height":vh},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
        pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.4); pg.evaluate("()=>{ localStorage.clear(); }"); pg.reload(); time.sleep(0.4)
        pg.evaluate("()=>{ Object.assign(window.__fb.META,{fame:60,van:{bigvan:1},hired:{lou:1,hale:1,dee:1},lineup:['lou','hale','dee']}); }")
        pg.click("#btnVan"); time.sleep(0.3); pg.click(f"[data-vt={tab}]"); time.sleep(0.6); pg.screenshot(path=f"vs_{vw}.png"); shots.append(Image.open(f"vs_{vw}.png"))
        print(vw,vh,'scroll',pg.evaluate("document.scrollingElement.scrollHeight"),'over',pg.evaluate("[...document.querySelectorAll('#scr-van .check *')].filter(e=>{const r=e.getBoundingClientRect(); return r.width&&(r.bottom>innerHeight+1||r.right>innerWidth+1);}).length")); pg.close()
    print('errors',errs); b.close()
a,b2,c3=shots; a=a.resize((a.width//2,a.height//2)); b2=b2.resize((b2.width//2,b2.height//2)); c3=c3.resize((c3.width//2,c3.height//2))
S=Image.new('RGB',(a.width+b2.width+10,max(a.height,b2.height)+c3.height+10),'black'); S.paste(a,(0,0)); S.paste(b2,(a.width+10,0)); S.paste(c3,(0,max(a.height,b2.height)+10)); S.thumbnail((1100,1500)); S.save('vs_sheet.png'); print(S.size)
