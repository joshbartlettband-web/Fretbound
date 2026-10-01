import time,sys
from playwright.sync_api import sync_playwright
from PIL import Image
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto("file:///home/claude/"+F); time.sleep(0.4); pg.click("#btnStart"); time.sleep(0.3)
    pg.query_selector_all("#scr-chars .ctile")[2].click(); time.sleep(0.3); pg.screenshot(path="u_chars.png")
    pg.click("#btnCharGo"); time.sleep(0.3)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
    if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    pg.screenshot(path="u_modal.png"); pg.click("#vcGo")
    for _ in range(150):
        if pg.evaluate("window.__fb.state.phase")=="answer": break
        time.sleep(0.1)
    pg.screenshot(path="u_duel.png"); print('errors',errs); b.close()
a=Image.open('u_chars.png').crop((0,1150,780,1690)); d=Image.open('u_duel.png').crop((0,0,780,540))
c=Image.new('RGB',(780,a.height+d.height+10),'black'); c.paste(a,(0,0)); c.paste(d,(0,a.height+10)); c.save('u_sheet.png'); print(c.size)
