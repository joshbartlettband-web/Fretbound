import time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto("file:///home/claude/fretbound.html"); time.sleep(0.4)
    r=pg.evaluate("""()=>{ const out={}; for(const c of ['bard','monk','hermit','busker','luthier','carto']){ const t0=performance.now(); let n=0;
      for(let f=0;f<=1.001;f+=0.1) for(const s of [-1,0,1]){ window.__fb.h2PNG(c,{fret:f,strum:s,nod:0.5}); n++; } out[c]=+((performance.now()-t0)/n).toFixed(2); } return out; }""")
    print('ms per new frame (incl. PNG encode):',r); b.close()
