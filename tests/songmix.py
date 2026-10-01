import time,sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]; lead_from=int(sys.argv[2])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)[:200])); pg.goto("file:///home/claude/"+f); time.sleep(0.8); pg.click("#btnStart"); time.sleep(0.3)
    pg.evaluate("window.__fb.songTestStyle('as',1,2)")
    for st in ['na','af','sa','eu','as','oc','an']:
        full=pg.evaluate(f"window.__fb.songTestStyle('{st}',{lead_from},4)")
        pg.evaluate("window.__fb.muteLead&&window.__fb.muteLead(true)"); band=pg.evaluate(f"window.__fb.songTestStyle('{st}',{lead_from},4)"); pg.evaluate("window.__fb.muteLead&&window.__fb.muteLead(false)")
        print(f"{st}: melody section {full['rmsDb']} dB (peak {full['peak']}), band alone {band['rmsDb']} dB -> band sits {round(full['rmsDb']-band['rmsDb'],1)} dB under the full mix")
    print('errors',errs); b.close()
