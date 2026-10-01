import time,sys,json
from playwright.sync_api import sync_playwright
F=sys.argv[1]; out=sys.argv[2]; FONTS=json.loads(sys.argv[3])
TXT="0123456789 +$%/x 2H 22 HH<br>ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":420,"height":900},device_scale_factor=3); pg.goto("file:///home/claude/"+F); time.sleep(0.6)
    html="".join(f"<div style=\"font-family:'{f}';font-size:{sz}px;color:#F2E8CE;margin:6px 4px;line-height:1.25\"><span style='font:10px monospace;color:#8ED36A'>{f} {sz}px</span><br>{TXT}</div>" for f,sz in FONTS)
    pg.evaluate("h=>{ const d=document.createElement('div'); d.id='spec'; d.style.cssText='position:fixed;left:0;top:0;width:420px;background:#2A1614;z-index:99999;padding:4px'; d.innerHTML=h; document.body.appendChild(d); }",html); time.sleep(0.8)
    pg.query_selector('#spec').screenshot(path=out); b.close()
