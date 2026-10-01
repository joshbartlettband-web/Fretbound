import time,json
from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); errs=[]
    pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2); pg.on("pageerror",lambda e: errs.append(str(e.stack)[:250]))
    pg.goto("file:///home/claude/test_lvl.html"); time.sleep(0.4); pg.evaluate("()=>localStorage.clear()"); pg.reload(); time.sleep(0.4)
    pg.evaluate("window.__fbNoRecruit=true"); pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.4)
    pg.click("#btnSound"); time.sleep(0.5)
    r=pg.evaluate("()=>({has:!!document.getElementById('sBand'),val:document.getElementById('sBand')&&document.getElementById('sBand').value,label:document.querySelector('#sBand').closest('.setrow').innerText.replace(/\\n/g,' | '),card:(()=>{const c=document.getElementById('modalCard').getBoundingClientRect(); return [Math.round(c.top),Math.round(c.bottom),innerHeight];})()})"); print(r)
    pg.query_selector("#modalCard").screenshot(path="band_settings.png")
    pg.evaluate("()=>{ const o=window.__masterOut, an=o.context.createAnalyser(); an.fftSize=4096; o.connect(an); window.__an=an; window.__buf=new Float32Array(4096); window.__pk=0; setInterval(()=>{ an.getFloatTimeDomainData(window.__buf); for(const v of window.__buf) window.__pk=Math.max(window.__pk,Math.abs(v)); },30); }")
    for label,val in [('0%',0),('70%',70),('100%',100)]:
        time.sleep(4.0)
        pg.evaluate("()=>{ window.__pk=0; }"); time.sleep(0.4); floor=pg.evaluate("window.__pk"); pg.evaluate("()=>{ window.__pk=0; }")
        pg.evaluate("v=>{ const e=document.getElementById('sBand'); e.value=v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true})); }",val); time.sleep(2.8)
        print('slider at %-4s preview peak %.3f   (silence before it: %.4f)'%(label,pg.evaluate("window.__pk"),floor))

