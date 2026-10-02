import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import sys,time
from playwright.sync_api import sync_playwright
from PIL import Image
S=OUT
sizes=[(360,740),(390,844),(412,860),(740,360),(844,390)]; ims=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    for w,h in sizes:
        pg=b.new_page(viewport={"width":w,"height":h}); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
        pg.goto(URL); time.sleep(1.2); pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.4)
        for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
        pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
        if pg.is_visible("#mOk"): pg.click("#mOk")
        for _ in range(50):
            if pg.is_visible("#vcGo"): break
            time.sleep(0.1)
        pg.click("#vcGo"); time.sleep(2.5)
        ov=pg.evaluate("(()=>{const d=document.getElementById('scr-duel'); return {sh:d.scrollHeight,ch:d.clientHeight,doc:document.documentElement.scrollHeight,win:innerHeight, dlg:document.getElementById('dialog').className}})()")
        print((w,h),ov,errs); pg.screenshot(path=f'{S}/sz_{w}x{h}.png'); ims.append(Image.open(f'{S}/sz_{w}x{h}.png')); pg.close()
    b.close()
H=max(i.height for i in ims); W=sum(i.width for i in ims)+8*len(ims); sh=Image.new('RGB',(W,H),'black'); x=0
for i in ims: sh.paste(i,(x,0)); x+=i.width+8
sh.save(S+'/sizes.png'); print(sh.size)
