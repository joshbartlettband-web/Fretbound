import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.5)
    for name,ml,mr in [('full',0,0),('lead+bass+drums',0,1),('rhythm+bass+drums',1,0)]:
        pg.evaluate("([a,b])=>{ window.__fb.SONG.muteL=!!a; window.__fb.SONG.muteR=!!b; }",[ml,mr])
        print(f"{name:20} pass1",pg.evaluate("window.__fb.songTest(9,4)")['rmsDb'],' twin',pg.evaluate("window.__fb.songTest(13,4)")['rmsDb'],' riff',pg.evaluate("window.__fb.songTest(1,2)")['rmsDb'])
    b.close()
