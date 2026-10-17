# v1.96: the pictures for the project page (landing/): real screenshots of the current build at phone size, a wide title shot and the share card.
# usage: python3 tests/dev/site_shots.py     -> landing/shots/*.png, landing/hero.png, landing/card.png   (needs Playwright; run from the repo root)
import sys,os,time,io
from playwright.sync_api import sync_playwright
from PIL import Image
OUT='landing'; os.makedirs(f'{OUT}/shots',exist_ok=True); URL='file://'+os.path.abspath('index.html')
def save(raw,name,w):
    im=Image.open(io.BytesIO(raw)).convert('RGB'); im=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
    im.quantize(colors=160,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save(f'{OUT}/shots/{name}.png',optimize=True)
with sync_playwright() as p:
    b=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); pg.add_init_script("window.__fbNoWarm=true"); pg.goto(URL); time.sleep(2.2)
    save(pg.screenshot(),'title',560)
    pg.click('#btnStart'); time.sleep(1.0); pg.query_selector_all('#charTiles .ctile')[6].click(); time.sleep(0.4); pg.evaluate("document.querySelectorAll('.sbub').forEach(b=>b.remove())"); save(pg.screenshot(),'players',560)
    pg.click('#btnCharGo'); time.sleep(0.5)
    for i in range(3): pg.query_selector_all('#offer .ptile')[i].click(); time.sleep(0.1)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.5)
    if pg.is_visible('#mOk'): pg.click('#mOk'); time.sleep(0.2)
    for _ in range(50):
        if pg.is_visible('#vcGo'): break
        time.sleep(0.1)
    pg.evaluate("window.__fb.state.lineup=['lou','dee','brass']"); pg.click('#vcGo')
    for _ in range(200):
        if pg.evaluate("window.__fb.state.phase")=='answer': break
        time.sleep(0.1)
    time.sleep(0.6); save(pg.screenshot(),'duel',560)
    pg.evaluate("window.__fb.askNameTest(true)"); time.sleep(1.1); save(pg.screenshot(),'nameit',560); pg.close()
    pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); pg.goto(URL); time.sleep(1.0); pg.evaluate("window.__fb.devRoad()"); time.sleep(0.4); got={}
    for k in range(28):
        ev=pg.evaluate("window.__fb.devRoadState().ev")
        if ev in ('unicorn','motel') and ev not in got:
            time.sleep(4.4 if ev=='unicorn' else 2.2); pg.evaluate("(()=>{ const b=document.getElementById('devRoadBar'); if(b) b.style.display='none'; const s=document.getElementById('scr-road'); if(s) s.style.paddingTop='0'; })()"); time.sleep(0.5)
            save(pg.screenshot(),'event_'+ev,560); got[ev]=1; pg.evaluate("(()=>{ const b=document.getElementById('devRoadBar'); if(b) b.style.display=''; })()")
        pg.click('#devRoadBar [data-dr=ne]'); time.sleep(0.15)
    pg.close()
    pg=b.new_page(viewport={'width':844,'height':390},device_scale_factor=2); pg.goto(URL); time.sleep(2.2); raw=pg.screenshot(); pg.close(); b.close()
im=Image.open(io.BytesIO(raw)).convert('RGB'); im.resize((860,round(im.height*860/im.width)),Image.LANCZOS).quantize(colors=200,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save(f'{OUT}/hero.png',optimize=True)
w=int(im.height*1200/630); x=(im.width-w)//2; im.crop((x,0,x+w,im.height)).resize((1200,630),Image.LANCZOS).save(f'{OUT}/card.png',optimize=True)
print('done')
