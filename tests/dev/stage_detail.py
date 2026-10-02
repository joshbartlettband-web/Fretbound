import os,sys
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
URL='file://'+REPO+'/index.html'
import time,base64,io,sys
from playwright.sync_api import sync_playwright
from PIL import Image
S=OUT
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:300])); pg.on("console",lambda m: errs.append(m.text[:300]) if m.type=='error' else None)
    pg.goto(URL); time.sleep(2.5)
    ims=[Image.open(io.BytesIO(base64.b64decode(pg.evaluate("([i,t])=>window.__fb.stageAt(i,t)",['juke',1.3+k*0.23]).split(',')[1]))).convert('RGB') for k in range(6)]
    print('errors',errs); b.close()
ims[0].save(S+'/juke_full.png')
crops=[im.crop((0,60,260,240)).resize((520,360),Image.NEAREST) for im in ims[:2]]; win=ims[0].crop((420,0,600,90)).resize((540,270),Image.NEAREST)
sh=Image.new('RGB',(1048,638)); sh.paste(crops[0],(0,0)); sh.paste(crops[1],(528,0)); sh.paste(win,(0,368)); sh.save(S+'/juke_detail.png')
fr=[im.resize((640,240)) for im in ims]; fr[0].save(S+'/juke_anim.gif',save_all=True,append_images=fr[1:],duration=140,loop=0)
