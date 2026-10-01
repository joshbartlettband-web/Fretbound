import time,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e))); pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.5)
    for a,n,name in [(0,1,'intro'),(1,4,'riff'),(9,4,'lead pass 1'),(13,4,'lead pass 2 (twin)')]:
        print(f"{name:20}",pg.evaluate("([a,n])=>window.__fb.songTest(a,n)",[a,n]))
    print('bare guitar through master (reference):',pg.evaluate("window.__fb.stackTest([])")); print('errors',errs); b.close()
