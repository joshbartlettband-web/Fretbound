import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import time,json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.add_init_script("window.__fbNoWarm=true"); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:300]))
    pg.goto(URL); time.sleep(2.5)
    r=pg.evaluate("""()=>{ const out=[], fb=window.__fb;
      for(const p of fb.PEDALS){ for(const o of [{},{compact:true},{lit:true}]){ try{ fb.face(p.id,o); }catch(e){ out.push('face '+p.id+' '+e.message); } } try{ fb.pcard(p.id); }catch(e){ out.push('pcard '+p.id+' '+e.message); } }
      const chars=['bard','monk','hermit','busker','luthier','carto'], ids=['spur','tide','juke','dunes','sebene','azmari','rio','milonga','chicha','paris','cave','frost','tokyo','ghat','bali','lanai','outback','grotto','mess','aurora','pole'];
      for(const c of chars){ fb.state.char=c; for(const v of ids){ try{ fb.stageAt(v,1.3); }catch(e){ out.push('stage '+c+' '+v+' '+e.message); } } 
        for(const q of [{fret:0},{fret:1},{fret:0.5,strum:1},{fret:0.5,strum:-1},{lean:1},{raise:1,crouch:0.5,mouth:1},{slump:1},{recoil:1,blink:1,mouth:1},{fret:0.3,nod:1}]){ try{ fb.h2PNG(c,q); }catch(e){ out.push('h2 '+c+' '+JSON.stringify(q)+' '+e.message); } } }
      return out; }""")
    print(len(r),'problems'); [print(' ',x) for x in r[:20]]; print('page errors',errs); b.close()
