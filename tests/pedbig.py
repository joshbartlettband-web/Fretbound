import time
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e)[:200]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4); pg.evaluate("window.__fbNoRecruit=true"); pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.4)
    pg.screenshot(path="pb_check.png"); pg.evaluate("window.__fb.shop()"); time.sleep(0.5); pg.query_selector_all("#shopOffer .ptile")[0].click(); time.sleep(0.4); pg.screenshot(path="pb_shop.png")
    print('scroll',pg.evaluate("document.scrollingElement.scrollHeight"),'errors',errs); b.close()
a=Image.open('pb_check.png').crop((0,700,780,1500)); b2=Image.open('pb_shop.png').crop((0,400,780,1500))
c=Image.new('RGB',(a.width+b2.width+10,max(a.height,b2.height)),'black'); c.paste(a,(0,0)); c.paste(b2,(a.width+10,0)); c.thumbnail((1200,900)); c.save('pb_both.png'); print(c.size)
