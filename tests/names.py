import time,json
from playwright.sync_api import sync_playwright
D=json.load(open('/home/claude/names.json'))
def tc(s): return ' '.join(w.capitalize() if w.lower() not in ('of','the','de','du') or k==0 else w.lower() for k,w in enumerate(s.lower().split()))
rows=[("Jacquard 12",30,tc(v)) for v in D['venues']]+[("Jacquard 12",26,n) for n in ["The Bard","The Metronome Monk","The Hermit","The Busker","The Luthier","The Cartographer"]]+[(f,fs,n) for n,f,fs in D['peds']]
html="".join(f"<div style=\"display:inline-block;width:185px;margin:3px 4px;vertical-align:top\"><div style=\"font-family:'{f}';font-size:{min(fs,30)}px;color:#F2E8CE;white-space:nowrap;overflow:hidden\">{n}</div><div style='font:9px monospace;color:#8ED36A'>{f} {fs}</div></div>" for f,fs,n in rows)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":400,"height":1600},device_scale_factor=2); pg.goto('file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','index.html'))); time.sleep(0.6)
    pg.evaluate("h=>{ const d=document.createElement('div'); d.id='nm'; d.style.cssText='position:absolute;left:0;top:0;width:400px;background:#2A1614;z-index:99999'; d.innerHTML=h; document.body.appendChild(d); }",html); time.sleep(0.8)
    pg.query_selector('#nm').screenshot(path='names.png'); b.close()
from PIL import Image; im=Image.open('names.png'); print(im.size)
