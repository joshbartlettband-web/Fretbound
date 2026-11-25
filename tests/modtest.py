import os, time, json
from playwright.sync_api import sync_playwright
# Pedal mods (v2.03): the scaling rules, and buying, maxing and selling a mod at the merch table.
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
OUT=os.environ.get('OUT','/tmp/fbout'); os.makedirs(OUT,exist_ok=True)
ev=lambda pg,js: pg.evaluate(js)
fails=[]
def check(ok,msg):
    print(('  ok   ' if ok else '  FAIL ')+msg)
    if not ok: fails.append(msg)
CASES=[  # pedal id, effect as the pedal returns it, level, expected op, expected label
 ('iron',{'op':{'hype':1},'label':'+1 HYPE','col':'hype'},1,{'hype':2},'+2 HYPE'),
 ('iron',{'op':{'hype':1},'label':'+1 HYPE','col':'hype'},2,{'hype':3},'+3 HYPE'),
 ('ogre',{'op':{'hype':3},'label':'+3 HYPE','col':'hype'},1,{'hype':5},'+5 HYPE'),
 ('ogre',{'op':{'hype':3},'label':'+3 HYPE','col':'hype'},2,{'hype':6},'+6 HYPE'),
 ('troll',{'op':{'tone':10},'label':'+10 TONE','col':'tone'},1,{'tone':15},'+15 TONE'),
 ('troll',{'op':{'tone':10},'label':'+10 TONE','col':'tone'},2,{'tone':20},'+20 TONE'),
 ('dragon',{'op':{'hypeMul':1.5},'label':'X1.5 HYPE','col':'hype'},1,{'hypeMul':1.75},'X1.75 HYPE'),
 ('dragon',{'op':{'hypeMul':1.5},'label':'X1.5 HYPE','col':'hype'},2,{'hypeMul':2},'X2 HYPE'),
 ('harpy',{'op':{'tone':24,'hype':-1},'label':'+24 TONE -1 HYPE','col':'tone'},1,{'tone':36,'hype':-1},'+36 TONE -1 HYPE'),
 ('phoenix',{'op':{'hype':1,'hypeMul':1.5},'label':'RISES +1 X1.5 HYPE','col':'hype'},1,{'hype':2,'hypeMul':1.75},'RISES +2 X1.75 HYPE'),
 ('rotary',{'op':{'hype':0.5},'label':'+0.5 HYPE','col':'hype'},1,{'hype':2},'+2 HYPE'),
 ('gremlin',{'op':{'tone':12},'label':'AGAIN +12 TONE','col':'tone'},2,{'tone':24},'AGAIN +24 TONE'),
 ('echo',{'op':{'tone':21},'label':'+21 TONE','col':'tone'},0,{'tone':21},'+21 TONE'),
]
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    pg=b.new_page(viewport={"width":390,"height":844}); pg.add_init_script("window.__fbNoWarm=true; window.__fbNoRecruit=true")
    errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
    pg.goto('file://'+REPO+'/index.html'); time.sleep(0.8)
    for pid,r,lv,op,lab in CASES:
        out=ev(pg,f"(()=>{{ window.__fb.state.mods={{}}; window.__fb.setMod({json.dumps(pid)},{lv}); return window.__fb.modFx({json.dumps(pid)},{json.dumps(r)}); }})()")
        check(out['op']==op and out['label']==lab,f'{pid} mod {lv}: {r["label"]} -> {out["label"]} {out["op"]}')
    # the merch table
    pg.click("#btnStart"); time.sleep(0.3); pg.click("#btnCharGo"); time.sleep(0.3)
    for i in range(3): pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.05)
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.3)
    if pg.is_visible("#mOk"): pg.click("#mOk"); time.sleep(0.2)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        time.sleep(0.1)
    pg.click("#vcGo"); time.sleep(0.5)
    check(ev(pg,"JSON.stringify(window.__fb.mods())")=='{}','a new run starts with no mods')
    pg.evaluate("window.__fb.shop()"); time.sleep(0.6); pg.evaluate("window.__fb.state.money=40; document.getElementById('btnNextGig')&&0")
    pg.evaluate("window.__fb.state.shop.forEach(x=>x.sold=true)")
    pg.evaluate("window.__fb.state.money=30; window.__fb.shop()"); time.sleep(0.5); pg.evaluate("window.__fb.state.money=40")
    pid=ev(pg,"window.__fb.state.pedals[0].id")
    check(ev(pg,"[...document.querySelectorAll('#shopBoard .modtag')].filter(e=>e.offsetWidth>0).length")>=1,'MOD tags show on board tiles when a mod is affordable')
    def open_first():
        pg.locator('#shopBoard .ptile').first.click(); time.sleep(0.3)
    def acts(): return ev(pg,"[...document.querySelectorAll('#smActs .btn')].map(b=>b.textContent+(b.disabled?' (off)':''))")
    open_first(); a=acts(); print('  board pedal buttons:',a,'| hint:',ev(pg,"(document.querySelector('.modhint')||{}).textContent"))
    pg.screenshot(path=f'{OUT}/mod_modal.png')
    check(any(x.startswith('MOD $10') and '(off)' not in x for x in a),'MOD $10 offered with $40')
    pg.evaluate("[...document.querySelectorAll('#smActs .btn')].find(b=>b.textContent.startsWith('MOD')).click()"); time.sleep(0.4)
    check(ev(pg,f"window.__fb.mods()[{json.dumps(pid)}]")==1 and ev(pg,"window.__fb.state.money")==30,'first mod bought: level 1, $30 left')
    check(ev(pg,"[...document.querySelectorAll('#shopBoard .modpip')].filter(e=>e.offsetWidth>0).length")==1,'board tile shows the mod badge')
    print('  board note:',ev(pg,"document.getElementById('boardNote').textContent"))
    open_first(); pg.evaluate("[...document.querySelectorAll('#smActs .btn')].find(b=>b.textContent.startsWith('MOD')).click()"); time.sleep(0.4)
    check(ev(pg,f"window.__fb.mods()[{json.dumps(pid)}]")==2 and ev(pg,"window.__fb.state.money")==10,'second mod: level 2, $10 left')
    open_first(); a=acts(); print('  after two mods:',a)
    check(any(x.startswith('MAXED') and '(off)' in x for x in a),'MAXED and disabled at level 2')
    sell=[x for x in a if x.startswith('SELL')][0]; price=ev(pg,f"window.__fb.state.pedals[0]&&({{}}).x");
    pg.screenshot(path=f'{OUT}/mod_modal_maxed.png')
    pg.evaluate("[...document.querySelectorAll('#smActs .btn')].find(b=>b.textContent.startsWith('CLOSE')).click()"); time.sleep(0.2)
    pg.click('#btnNextGig'); time.sleep(2.0)
    for _ in range(50):
        if pg.is_visible("#vcGo"): break
        if pg.is_visible("#roadGo"): pg.click('#roadGo'); time.sleep(0.5)
        bs=pg.query_selector_all('#roadChoices button')
        if bs and not pg.is_visible('#roadGo'):
            try: bs[-1].click(); time.sleep(1.2)
            except Exception: pass
        time.sleep(0.2)
    saved=ev(pg,"JSON.parse(localStorage.getItem('fretbound.run.v1')||'{}').mods")
    check(saved and saved.get(pid)==2,'the run save keeps the mods '+str(saved))
    if pg.is_visible("#vcGo"): pg.click("#vcGo"); time.sleep(0.6)
    check(ev(pg,"[...document.querySelectorAll('#board .pedal .modpip')].filter(e=>e.offsetWidth>0).length")==1,'duel pedalboard shows the mod badge')
    pg.screenshot(path=f'{OUT}/mod_duel.png')
    print('  sell button with two mods:',sell)
    check(not errs,'no page errors '+str(errs[:3]))
    b.close()
print('problems:',len(fails))
