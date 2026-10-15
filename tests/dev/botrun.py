# A full run played through the real UI by a bot with a human-ish skill profile, logging every screen and every night.
# usage: OUT=/tmp/run1 python3 tests/dev/botrun.py PROFILE CHAR STRATEGY [WxH] [maxNights]
#   PROFILE: pro | casual | novice   (note accuracy, how late it taps after the beat, how often it names the first note right)
#   STRATEGY: greedy (buy the dearest pedal it can) | thrifty (buy only cheap pedals, keep $5 for interest)
# writes OUT/log.json (nights, money, pedals, timings, texts seen, errors) and OUT/shot_###_<screen>.png at each new screen
import os,sys,time,json,random
from playwright.sync_api import sync_playwright
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')); OUT=os.environ.get('OUT','/tmp/fbrun'); os.makedirs(OUT,exist_ok=True)
PROF={'pro':dict(acc=0.97,sig=0.018,name=0.9,think=0.25),'casual':dict(acc=0.86,sig=0.05,name=0.6,think=0.45),'novice':dict(acc=0.72,sig=0.09,name=0.35,think=0.7)}
prof=sys.argv[1]; P=PROF[prof]; CH=sys.argv[2]; STRAT=sys.argv[3]
size=[a for a in sys.argv[4:] if 'x' in a]; W,H=map(int,(size[0] if size else '390x844').split('x')); MAXN=int(([a for a in sys.argv[4:] if a.isdigit()] or ['40'])[0])
random.seed(hash((prof,CH,STRAT))&0xffff)
log={'profile':prof,'char':CH,'strategy':STRAT,'size':[W,H],'nights':[],'screens':[],'texts':[],'errors':[],'shop':[],'road':[],'names':[0,0]}
# answer one call inside the page: navigate the neck window, then tap each note shortly after a beat (late by |N(0,sig)|), wrong notes a semitone or two off
ANSWER_JS="""async ([acc,sig])=>{ const fb=window.__fb, S=fb.state, sleep=ms=>new Promise(r=>setTimeout(r,ms)), ctx=fb.rigs().ctx;
  const gauss=()=>{ let u=0,v=0; while(!u) u=Math.random(); while(!v) v=Math.random(); return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*v); };
  const notes=S.call.notes.slice(), OPEN=fb.open(), neck=document.getElementById('neck'); let wrong=0;
  for(const n of notes){ if(S.phase!=='answer') break;
    let midi=n.midi; if(Math.random()>acc){ midi+= (Math.random()<0.5?-1:1)*(Math.random()<0.7?1:2); wrong++; }
    let found=null;
    for(let k=0;k<20&&!found;k++){ const g=fb.geo;
      for(let s=0;s<OPEN.length;s++){ const f=midi-OPEN[s]; if(!S.broken[s]&&f>=S.pos&&f<S.pos+S.win&&f>=0&&f<=15){ found={s,f}; break; } }
      if(found) break;
      const cand=[]; for(let s=0;s<OPEN.length;s++){ const f=midi-OPEN[s]; if(!S.broken[s]&&f>=0&&f<=15) cand.push(f); }
      if(!cand.length) return {ok:false,why:'unplayable',wrong};
      document.getElementById(cand[0]>=S.pos+S.win?'navR':'navL').click(); await sleep(360); }
    if(!found) return {ok:false,why:'nav',wrong};
    // wait for a beat (or swung offbeat) on the band's grid, then add a late human error
    for(let k=0;k<200;k++){ const gp=fb.groovePos(ctx.currentTime); if(gp&&gp.off<7) break; await sleep(4); }
    await sleep(Math.abs(gauss()*sig*1000));
    const g=fb.geo, r=neck.getBoundingClientRect(), cc=found.f-S.pos, x=r.left+((g.bounds[cc]+g.bounds[cc+1])/2)/g.cw*r.width, y=r.top+g.sy[found.s]/g.ch*r.height;
    neck.dispatchEvent(new PointerEvent('pointerdown',{clientX:x,clientY:y,bubbles:true,pointerId:1}));
    await sleep(120); }
  return {ok:true,wrong}; }"""
def ev(pg,js,arg=None): return pg.evaluate(js,arg) if arg is not None else pg.evaluate(js)
def vis(pg,sel):
    try: return pg.is_visible(sel)
    except Exception: return False
shots=[0]; seen=set()
def shot(pg,tag,force=False):
    if tag in seen and not force: return
    seen.add(tag); shots[0]+=1; pg.screenshot(path=f'{OUT}/shot_{shots[0]:03d}_{tag}.png')
def clickText(pg,sel,rx):
    for b in pg.query_selector_all(sel):
        try:
            if b.is_visible() and b.is_enabled() and __import__('re').search(rx,b.inner_text()): b.click(); return True
        except Exception: pass
    return False
with sync_playwright() as p:
    b=p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"]); pg=b.new_page(viewport={"width":W,"height":H})
    pg.on("pageerror",lambda e: log['errors'].append(str(e)[:300])); pg.on("console",lambda m: log['errors'].append(m.text[:300]) if m.type=='error' else None)
    pg.goto('file://'+REPO+'/index.html'); time.sleep(0.5); ev(pg,"()=>{ localStorage.clear(); }"); pg.reload(); t_load=time.time(); time.sleep(1.5)
    T0=time.time(); last_screen=None; t_screen=time.time(); nights=0; night=None; calls=0; stuck=0; done=False
    fails=0
    while not done and time.time()-T0<3600:
      try:
          try: st=ev(pg,"({sc:window.__fb.state.screen,ph:window.__fb.state.phase,over:window.__fb.state.over})")
          except Exception as e: log['errors'].append('eval '+str(e)[:200]); time.sleep(0.5); continue
          sc=st['sc']
          if sc!=last_screen:
              if last_screen: log['screens'].append([last_screen,round(time.time()-t_screen,1)])
              last_screen=sc; t_screen=time.time(); shot(pg,sc+('_'+str(nights) if sc in('duel','results','road') else ''))
          # any modal first: recruits, leg picks, rules
          if vis(pg,'#modal:not(.hidden)') and not vis(pg,'#vcGo'):
              txt=ev(pg,"document.getElementById('modalCard').innerText.slice(0,240)"); log['texts'].append(['modal',txt]); shot(pg,'modal_'+txt[:12].replace(' ','_').replace('/',''))
              if vis(pg,'#rYes'): pg.click('#rYes')
              elif pg.query_selector('.legbtn'): pg.query_selector_all('.legbtn')[0].click()
              elif vis(pg,'#mOk'): pg.click('#mOk')
              elif not clickText(pg,'#modalCard button',r'OK|GOT IT|CLOSE|CONTINUE|YES|PLAY'): pg.keyboard.press('Escape')
              time.sleep(0.4); continue
          if sc=='title': pg.click('#btnStart'); time.sleep(0.6); continue
          if sc=='chars':
              tiles=pg.query_selector_all('#scr-chars .ctile'); ids=ev(pg,"[...document.querySelectorAll('#scr-chars .ctile')].map(t=>t.dataset.id||t.getAttribute('aria-label')||t.innerText)")
              k=next((i for i,t in enumerate(ids) if CH.lower() in (t or '').lower()),0); tiles[k].click(); time.sleep(0.3); shot(pg,'chars_picked'); pg.click('#btnCharGo'); time.sleep(0.6); continue
          if sc=='check':
              for i in range(3):
                  tl=pg.query_selector_all('#offer .ptile')
                  if i<len(tl): tl[i].click(); time.sleep(0.2)
              shot(pg,'check_picked'); ev(pg,"document.getElementById('btnReady').click()"); time.sleep(0.6); continue
          if vis(pg,'#vcGo'):
              v=ev(pg,"({v:window.__fb.state.venueIdx,name:document.getElementById('venueName').textContent,rule:(document.querySelector('#scr-duel .vcard, .vcard')||{}).innerText||''})")
              shot(pg,'venuecard_'+str(nights),True); log['texts'].append(['venuecard',v['rule'][:400]])
              night={'venue':v['name'],'start':time.time(),'calls':[],'money0':ev(pg,"window.__fb.state.money")}; calls=0
              pg.click('#vcGo'); time.sleep(0.5); continue
          if sc=='duel':
              if st['ph']=='answer':
                  time.sleep(P['think']); r=ev(pg,ANSWER_JS,[P['acc'],P['sig']]); calls+=1
                  if night is not None: night['calls'].append(r)
                  # the FIRST NOTE? quiz after a true call
                  for _ in range(30):
                      if vis(pg,'#namePick:not(.hidden) button'): break
                      if ev(pg,"window.__fb.state.phase")!='answer': pass
                      time.sleep(0.1)
                  if vis(pg,'#namePick:not(.hidden) button'):
                      time.sleep(random.uniform(0.9,2.6)); pc=ev(pg,"((window.__fb.state.call.notes[0].midi%12)+12)%12"); btns=pg.query_selector_all('#namePick button')
                      right=random.random()<P['name']; log['names'][1]+=1
                      tgt=[x for x in btns if (x.get_attribute('data-pc')==str(pc))==right]
                      if tgt: tgt[0].click(); log['names'][0]+=int(right)
                  continue
              if st['ph']=='review':
                  if st['over']:
                      if night is not None:
                          night.update(dict(result=st['over'],total=ev(pg,"window.__fb.state.total"),target=ev(pg,"window.__fb.state.target||null"),secs=round(time.time()-night['start']),money1=ev(pg,"window.__fb.state.money"),pedals=ev(pg,"window.__fb.state.pedals.map(p=>p.id)")))
                          night.pop('start',None); log['nights'].append(night); nights+=1; print(prof,CH,'night',nights,night['venue'],night['result'],night['total'],flush=True); night=None; json.dump(log,open(f'{OUT}/log.json','w'),indent=1)
                      shot(pg,'duel_end_'+str(nights),True)
                  if vis(pg,'#btnNext') and ev(pg,"!document.getElementById('btnNext').disabled"): pg.click('#btnNext'); time.sleep(0.5); continue
              time.sleep(0.2); stuck+=1
              if stuck>600: log['errors'].append('stuck in duel '+json.dumps(st)); break
              continue
          stuck=0
          if sc=='shop':
              S=ev(pg,"({m:window.__fb.state.money,shop:window.__fb.state.shop.map(it=>it.b?null:{id:it.p.id,price:window.__fb.pedalArt()[it.p.id].price,sold:!!it.sold}),n:window.__fb.state.pedals.length,broken:window.__fb.state.broken.filter(Boolean).length})")
              shot(pg,'shop_'+str(nights)); buys=[]
              if S['broken'] and vis(pg,'#btnRestring') and ev(pg,"!document.getElementById('btnRestring').disabled"): pg.click('#btnRestring'); time.sleep(0.3); buys.append('restring')
              opts=[(i,x) for i,x in enumerate(S['shop']) if x and not x['sold']]
              budget=S['m']-(5 if STRAT=='thrifty' else 0)
              opts=[o for o in opts if o[1]['price']<=budget and (STRAT=='greedy' or o[1]['price']<=5)]
              if opts:
                  i,x=max(opts,key=lambda o:o[1]['price']) if STRAT=='greedy' else min(opts,key=lambda o:o[1]['price'])
                  pg.query_selector_all('#shopOffer > *')[i].click(); time.sleep(0.4)
                  if clickText(pg,'#smActs button',r'BUY'): buys.append(x['id'])
                  else: clickText(pg,'#smActs button',r'CLOSE')
                  time.sleep(0.4)
              log['shop'].append(dict(after_night=nights,money=S['m'],board=S['n'],bought=buys))
              if nights>=MAXN: done=True; break
              if vis(pg,'#btnNextGig'): pg.click('#btnNextGig'); time.sleep(0.8)
              continue
          if sc=='road':
              title=ev(pg,"document.getElementById('roadTitle').textContent"); story=ev(pg,"document.getElementById('roadStory').textContent"); shot(pg,'road_'+title[:10].replace(' ','_'),True)
              for _ in range(8):
                  if vis(pg,'#roadGo'): break
                  bs=[x for x in pg.query_selector_all('#roadChoices button') if x.is_visible() and x.is_enabled() and 'HEAR' not in x.inner_text()]
                  if bs: random.choice(bs).click(); time.sleep(1.4)
                  else: time.sleep(0.4)
              out=ev(pg,"document.getElementById('roadOut').textContent"); log['road'].append([title,story,out]); log['texts'].append(['road',title+': '+story+' / '+out])
              if vis(pg,'#roadGo'): pg.click('#roadGo'); time.sleep(0.8)
              continue
          if sc=='results':
              shot(pg,'results_'+str(nights),True); log['texts'].append(['results',ev(pg,"document.getElementById('scr-results').innerText.slice(0,600)")])
              if vis(pg,'#btnNextLeg'): pg.click('#btnNextLeg'); time.sleep(0.8); continue
              done=True; break
          time.sleep(0.3)
      except Exception as e:
        fails+=1; log['errors'].append('bot '+str(e).split(chr(10))[0][:200]); time.sleep(0.5)
        if fails>40: break
    log['screens'].append([last_screen,round(time.time()-t_screen,1)]); log['total_secs']=round(time.time()-T0)
    json.dump(log,open(f'{OUT}/log.json','w'),indent=1); print('done',prof,CH,STRAT,'nights',len(log['nights']),'errors',len(log['errors']),'secs',log['total_secs'])
    b.close()
