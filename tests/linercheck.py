# Every Keep reading page and every roster caller card must fit the screen without scrolling, at the five house sizes.
import os,time,json
from playwright.sync_api import sync_playwright
SIZES=[(360,740),(390,844),(412,860),(740,360),(844,390)]
bad=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for w,h in SIZES:
        pg=b.new_page(viewport={"width":w,"height":h}); pg.goto('file://'+os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','index.html'))); time.sleep(1.2)
        L=pg.evaluate("window.__fb.lore()"); ids=[v['id'] for T in L['tours'] for v in T['venues']]
        chk="(()=>{ const c=document.getElementById('modalCard'), r=c.getBoundingClientRect(); return {over:c.scrollHeight-c.clientHeight, top:r.top, bot:r.bottom, vh:innerHeight}; })()"
        for vid in ids:
            n=pg.evaluate(f"(window.__fb.linerMore('{vid}',0), document.querySelector('.lmore .kicker')?document.querySelector('.lmore .kicker').textContent:'')")
            if not n: continue
            pages=int(n.split(' of ')[1])
            for k in range(pages):
                pg.evaluate(f"window.__fb.linerMore('{vid}',{k})"); r=pg.evaluate(chk)
                if r['over']>1 or r['top']<0 or r['bot']>r['vh']: bad.append((w,h,vid,'page',k+1,r))
            pg.evaluate(f"window.__fb.rosterCard('{vid}')"); r=pg.evaluate(chk)
            if r['over']>1 or r['top']<0 or r['bot']>r['vh']: bad.append((w,h,vid,'roster',r))
        pg.close()
print(len(bad),'problems'); [print(x) for x in bad[:30]]
