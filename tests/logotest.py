import time
from playwright.sync_api import sync_playwright
from PIL import Image
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for vw,vh in [(360,740),(390,844),(412,860),(740,360),(844,390)]:
        pg=b.new_page(viewport={"width":vw,"height":vh},device_scale_factor=2); pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.7)
        r=pg.evaluate("()=>{ const q=s=>{ const e=document.querySelector(s); const r=e.getBoundingClientRect(); return [Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)]; }; const l=q('.title-ui .logo'), tg=q('.title-ui .tagline'), bt=q('#btnStart'), ft=q('.title-foot'); return {logo:l,tagline:tg,start:bt,foot:ft,logoFrac:+((l[2]-l[0])/innerWidth).toFixed(2),overlap:l[3]>tg[1]||tg[3]>bt[1],offscreen:l[0]<0||l[2]>innerWidth,scroll:document.scrollingElement.scrollHeight>innerHeight}; }")
        print(vw,vh,'logo width',r['logoFrac'],'of screen | overlaps:',r['overlap'],'| off-screen:',r['offscreen'],'| scrolls:',r['scroll'],'| start button bottom',r['start'][3],'foot top',r['foot'][1])
        if vw in (390,844): pg.screenshot(path=f"logo_{vw}.png"); shots.append(Image.open(f"logo_{vw}.png"))
        pg.close()
    b.close()
a,c=shots; a=a.resize((a.width//2,a.height//2)); c=c.resize((c.width//2,c.height//2))
S=Image.new('RGB',(a.width+c.width+10,max(a.height,c.height)),'black'); S.paste(a,(0,0)); S.paste(c,(a.width+10,0)); S.save('logo_both.png'); print(S.size)
