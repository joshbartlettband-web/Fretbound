import time
from playwright.sync_api import sync_playwright
from PIL import Image
shots=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    pg=b.new_page(viewport={"width":844,"height":390},device_scale_factor=1); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:400]))
    pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.6); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.8)
    print('start theme:',pg.evaluate("window.__fb.titleThemeId()"),'| picker:',pg.evaluate("document.getElementById('titleScene').innerText.replace(/\\n/g,' ')"))
    pg.click("#tsNext"); time.sleep(0.4); print('locked toast:',pg.evaluate("document.getElementById('tsToast').innerText"))
    for _ in range(5): pg.click(".title-foot"); time.sleep(0.08)
    time.sleep(0.3); print('after 5 taps:',pg.evaluate("document.getElementById('titleScene').innerText.replace(/\\n/g,' ')"),'|',pg.evaluate("document.getElementById('tsToast').innerText"))
    for theme in ['na','af','eu']:
        pg.evaluate(f"window.__fb.setTitleTheme('{theme}')"); time.sleep(0.5)
        for k in range(3):
            if k: pg.evaluate("window.__fb.nextSky()"); time.sleep(0.6)
            time.sleep(0.5); pg.query_selector('#titlecv').screenshot(path=f'sc_{theme}_{k}.png'); shots.append((theme,k))
    print('errors',errs); b.close()
ims=[Image.open(f'sc_{th}_{k}.png').resize((420,194)) for th,k in shots]
S=Image.new('RGB',(3*424,3*198),'black')
for i,im in enumerate(ims): S.paste(im,((i%3)*424,(i//3)*198))
S.save('scenes_grid.png'); print(S.size)
