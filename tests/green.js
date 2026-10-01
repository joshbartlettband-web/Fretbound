/* ---------- the green room: practice with no score, no pedals and no strings to lose ---------- */
const PRAC_VEN={id:'green',night:0,name:'THE GREEN ROOM',short:'GREEN ROOM',place:'Backstage',rival:'THE GUITAR TECH',rivalSub:'Plays it slowly, as many times as you like',rule:'',ruleText:'',bpm:92,target:1,setLen:99999,tiers:[1],pay:0,
  rig:{guitar:'nylon',fx:[],level:0.85},hats:'none',
  lines:{intro:['Pull up a stool. I will play it, you play it back.','No score in here. Just you and the neck.'],taunt:['Ready when you are.','Listen for the first note.','Take your time.','Here it comes.','Again?'],good:['That is it.','Clean.','You heard it.','Right where it lives.'],bad:['Close. Listen again.','Not quite. Have another go.','Hear where it went?','Happens to everyone.'],win:'',lose:''},liner:{title:'',text:'',listen:''}};
let PR=null, PRSETUP=null;
const PR_FRETS={all:[0,15,'ALL'],a:[0,4,'0-4'],b:[5,8,'5-8'],c:[9,12,'9-12'],d:[12,15,'12-15']};
const IV_NAMES={1:'m2',2:'M2',3:'m3',4:'M3',5:'P4',6:'TT',7:'P5',8:'m6',9:'M6',10:'m7',11:'M7',12:'8ve'};
const PR_PRESETS=[['weak','MY WEAK SPOTS'],['intervals','INTERVALS'],['triads','TRIADS'],['runs','RUNS'],['all','ALL']];
function pracSizes(){ return [...new Set(HANDS.filter(h=>h.iv.length===2).map(h=>Math.abs(h.iv[1])))].filter(v=>IV_NAMES[v]).sort((a,b)=>a-b); }
function pracHands(cfg){
  const one=HANDS.filter(h=>h.iv.length===2), sel=cfg.ivSel&&cfg.ivSel.length?cfg.ivSel:null;
  if(cfg.preset==='weak'){ const w=earWeakSpots().hands; if(w.length) return w; return HANDS.filter(h=>store.stats[h.id]&&store.stats[h.id].seen>=1).sort((a,b)=>store.stats[a.id].correct/store.stats[a.id].seen-store.stats[b.id].correct/store.stats[b.id].seen).slice(0,3).map(h=>h.id); }
  if(cfg.preset==='intervals') return one.filter(h=>!sel||sel.indexOf(Math.abs(h.iv[1]))>=0).map(h=>h.id);
  if(cfg.preset==='triads') return HANDS.filter(h=>h.iv.length===3).map(h=>h.id);
  if(cfg.preset==='runs') return HANDS.filter(h=>h.iv.length>=4).map(h=>h.id);
  return HANDS.map(h=>h.id);
}
function pracDefault(){ return {preset:'intervals',ivSel:null,frets:'all',strings:'all',bpm:92,names:false,glow:true}; }
function practiceOK(p){ if(!state.practice||!PR) return true; const fr=PR.fr;
  if(PR.relax<2&&(p.f<fr[0]||p.f>fr[1])) return false;
  if(PR.relax<1&&PR.str!=='all'&&(PR.str==='high'?p.s>2:p.s<3)) return false;
  return true; }
function practiceCall(){
  const pool=HANDS.filter(h=>PR.hands.indexOf(h.id)>=0), use=pool.length?pool:HANDS;
  for(let ph=0;ph<3;ph++){ PR.relax=ph; for(let a=0;a<140;a++){ const h=weightedPick(use), c=tryBuild(h,a<70); if(c){ PR.relaxed=ph; return c; } } }
  PR.relax=2; PR.relaxed=2; for(const h of use){ for(let a=0;a<40;a++){ const c=tryBuild(h,false); if(c) return c; } }
  return {hand:HANDS[0],root:45,notes:[{midi:45,s:4,f:0},{midi:52,s:3,f:2}],hot:false};
}
function namesOn(){ return !!(store.settings.names||(state.practice&&PR&&PR.names)); }

/* ----- the session ----- */
function resetPracticeHud(on){
  const d=$('scr-duel'); d.classList.toggle('practice',on);
  const lab=document.querySelector('#scr-duel .sl-lab'); if(lab) lab.textContent=on?'FOUND':'SCORE';
  if(!on){ state.practice=false; }
}
function startPractice(cfg){
  initAudio(); cfg=Object.assign(pracDefault(),cfg||{});
  const fr=PR_FRETS[cfg.frets]||PR_FRETS.all, tok=++state.runId; trStop(); hideDialog();
  PR={cfg,hands:pracHands(cfg),fr:[fr[0],fr[1]],str:cfg.strings,bpm:cfg.bpm,names:cfg.names,glow:cfg.glow,relax:0,relaxed:0,calls:0,found:0,streak:0,best:0,notes:0,noteOk:0,missed:{},log:[],t0:Date.now()};
  PRAC_VEN.bpm=cfg.bpm;
  state.practice=true; state.char=store.settings.char||state.char||'bard'; state.seven=false;
  applyTuning();
  Object.assign(state,{pedals:[],lineup:[],rivalBand:[],money:0,venueIdx:0,legNo:1,tour:0,broken:Array(NS).fill(false),total:0,callIdx:0,replays:999,blind:false,call:null,answer:[],phase:'idle',sel:-1,over:null,used:{},beat:-1,pos:0,spareUsed:false,noGlow:!PR.glow,streak:0,trueCalls:0,best:0,notesPlayed:0,grooveHits:0,callsTotal:0,spares:0,gauge:'standard',tough:0,loopCharge:0});
  for(let k=0;k<7;k++){ vib[k]=null; press[k]=null; snap[k]=null; }
  resetPracticeHud(true); state.practice=true;
  applyVenue(PRAC_VEN); try{ heroWarm(state.char); rivalWarm('green'); }catch(e){}
  $('toneBox').textContent='0'; $('hypeBox').textContent='0'; setHand('READY?','',''); renderPracticeHud();
  goScreen('duel'); state.practice=true; $('scr-duel').classList.add('practice');
  (async()=>{ say(RIVAL,PRAC_VEN.lines.intro[0]); await sleep(2200); if(!alive(tok)) return; say(RIVAL,PRAC_VEN.lines.intro[1]); await sleep(1900); if(!alive(tok)) return; startCall(tok); })();
}
// change the tempo: at once while you are answering or reviewing (the groove restarts on the new grid so the next replay is at the new speed), or at the next call if the tech is mid-phrase
function applyPracticeTempo(b){ if(!PR) return; b=Math.max(40,Math.min(140,Math.round(b/4)*4)); PR.bpm=b; PRAC_VEN.bpm=b; const ph=state.phase;
  if(ph==='answer'||ph==='review'){ setTempo(b); if(tr.on&&ctx){ trStart('duel',ctx.currentTime+0.1); try{ grooveMix(ph==='answer'?'answer':'listen',true); }catch(e){} } PR.tempoPending=false; }
  else PR.tempoPending=true;
  renderPracticeHud(); }
function renderPracticeHud(){
  if(!state.practice||!PR) return;
  $('venueName').textContent='GREEN ROOM'; $('callLabel').textContent='CALL '+Math.max(1,state.callIdx);
  $('topCash').textContent='STREAK '+PR.streak; $('totalNum').textContent=PR.found; $('targetNum').textContent=PR.calls;
  $('barFill').style.width=(PR.calls?PR.found/PR.calls*100:0)+'%'; $('replayN').textContent='';
  const dots=$('paDots'); if(dots) dots.innerHTML=PR.log.slice(-14).map(x=>'<i class="'+(x.ok?'ok':'no')+'"></i>').join('');
  const nb=$('paNames'); if(nb) nb.querySelector('b').textContent=PR.names?'ON':'OFF'; const gb=$('paGlow'); if(gb) gb.querySelector('b').textContent=PR.glow?'ON':'OFF'; const bp=$('paBpm'); if(bp) bp.textContent=PR.bpm+' BPM'+(PR.tempoPending?' NEXT':''); const sl=$('paTempo'); if(sl&&document.activeElement!==sl) sl.value=PR.bpm;
  $('paNames').classList.toggle('on',!!PR.names); $('paGlow').classList.toggle('on',!!PR.glow);
}
async function finishPractice(tok){
  const c=state.call, ans=state.answer, correct=ans.map((a,k)=>!!(c.notes[k]&&a.midi===c.notes[k].midi)), perfect=correct.every(Boolean);
  const st=store.stats[c.hand.id]||(store.stats[c.hand.id]={seen:0,correct:0,lastMissed:false}); st.seen++; if(perfect) st.correct++; st.lastMissed=!perfect; save();
  PR.calls++; PR.notes+=ans.length; PR.noteOk+=correct.filter(Boolean).length; PR.log.push({id:c.hand.id,ok:perfect});
  if(perfect){ PR.found++; PR.streak++; PR.best=Math.max(PR.best,PR.streak); if(PR.streak>=3){ anim.cheerUntil=perfNow()+1.2; } } else { PR.streak=0; PR.missed[c.hand.id]=(PR.missed[c.hand.id]||0)+1; heroFlinch(); state.shake=4; }
  renderPracticeHud(); state.phase='review';
  const minF=Math.min(...c.notes.map(n=>n.f)); state.pos=state.win<=6?minF-1:minF-2; clampPos();
  $('btnNext').disabled=true; renderNeck(); setPhase();
  say(RIVAL,perfect?choose(PRAC_VEN.lines.good):choose(PRAC_VEN.lines.bad));
  await sleep(1100); if(!alive(tok)) return;
  const names=c.notes.map(n=>NN[n.midi%12]).join(' - '), miss=ans.map((a,k)=>a.midi!==c.notes[k].midi?NN[a.midi%12]:null).filter(Boolean);
  say('THE CALL WAS',c.hand.name+': '+names+'. '+c.hand.desc[0].toUpperCase()+c.hand.desc.slice(1)+'.'+(miss.length?' Your wrong notes: '+miss.join(', ')+'.':''),0,true);
  $('btnNext').textContent='NEXT CALL'; $('btnNext').disabled=false;
}
function finishPracticeSession(){
  if(!PR){ goBackstage(); return; }
  const tok=++state.runId; trStop(); hideDialog();
  const pct=PR.calls?Math.round(PR.found/PR.calls*100):0, npct=PR.notes?Math.round(PR.noteOk/PR.notes*100):0, mins=Math.max(1,Math.round((Date.now()-PR.t0)/60000));
  const hard=Object.keys(PR.missed).sort((a,b)=>PR.missed[b]-PR.missed[a])[0], hh=hard&&HANDS.find(h=>h.id===hard);
  const cfg=PR.cfg;
  openModal('<div class="kicker">Green Room</div><h3>'+(PR.calls?'Session over':'No calls yet')+'</h3>'+
    (PR.calls?'<div class="mem-l"><b>CALLS</b> '+PR.found+' found of '+PR.calls+' ('+pct+'%)</div><div class="mem-l"><b>NOTES</b> '+PR.noteOk+' of '+PR.notes+' ('+npct+'%)</div><div class="mem-l"><b>BEST STREAK</b> '+PR.best+'</div><div class="mem-l"><b>TIME</b> about '+mins+' min</div>'+(hh?'<div class="mem-l"><b>HARDEST</b> '+hh.name+' (missed '+PR.missed[hard]+')</div>':'<div class="mem-l">A clean session.</div>'):'<div class="mem-l">Play a few calls and this fills in.</div>')+
    '<div class="row-btns"><button class="btn gold" id="gsAgain">PRACTICE MORE</button><button class="btn blue" id="gsEar">EAR REPORT</button><button class="btn blue" id="gsBack">BACKSTAGE</button></div>');
  $('gsAgain').onclick=()=>{ closeModal(); openGreenRoom(null,cfg); };
  $('gsEar').onclick=()=>{ closeModal(); leavePractice(); goEar(); };
  $('gsBack').onclick=()=>{ closeModal(); leavePractice(); goBackstage(); };
}
function leavePractice(){ if(state.practice||$('scr-duel').classList.contains('practice')){ state.runId++; try{ trStop(); }catch(e){} hideDialog(); state.practice=false; $('scr-duel').classList.remove('practice'); const lab=document.querySelector('#scr-duel .sl-lab'); if(lab) lab.textContent='SCORE'; state.inVenue=false; } PR=null; }

/* ----- the setup screen ----- */
function renderGreen(){
  const C=PRSETUP||(PRSETUP=pracDefault()), sizes=pracSizes(), weak=earWeakSpots(), hasWeak=weak.hands.length>0||Object.keys(store.stats||{}).length>0;
  const chip=(act,val,label,on,dis)=>'<button class="gchip'+(on?' on':'')+(dis?' dis':'')+'" data-a="'+act+'" data-v="'+val+'"'+(dis?' disabled':'')+'>'+label+'</button>';
  $('greenBody').innerHTML=
    '<div class="gsec"><h4>WHAT TO PRACTISE</h4><div class="gchips">'+PR_PRESETS.map(([k,l])=>chip('preset',k,l,C.preset===k,k==='weak'&&!hasWeak)).join('')+'</div>'+
    (C.preset==='intervals'?'<div class="gchips gsub">'+sizes.map(v=>chip('iv',v,IV_NAMES[v],!C.ivSel||C.ivSel.indexOf(v)>=0)).join('')+'</div>':'')+
    (C.preset==='weak'?'<div class="gnote">'+(weak.hands.length?'Your weakest calls: '+weak.hands.map(id=>HANDS.find(h=>h.id===id).name.toLowerCase()).join(', ')+(weak.zone?'. Frets and strings set for you.':'.'):'Play a little first, and this will pick your weak spots.')+'</div>':'')+'</div>'+
    '<div class="gsec gcol"><div><h4>FRETS</h4><div class="gchips">'+Object.keys(PR_FRETS).map(k=>chip('frets',k,PR_FRETS[k][2],C.frets===k)).join('')+'</div></div>'+
    '<div><h4>STRINGS</h4><div class="gchips">'+[['all','ALL'],['high','HIGH'],['low','LOW']].map(([k,l])=>chip('strings',k,l,C.strings===k)).join('')+'</div></div></div>'+
    '<div class="gsec gcol"><div class="gtempo"><h4>TEMPO <span id="gBpm">'+C.bpm+' BPM</span></h4><input type="range" id="gTempo" min="40" max="140" step="4" value="'+C.bpm+'" aria-label="Tempo in beats per minute"></div>'+
    '<div><h4>AIDS</h4><div class="gchips">'+chip('names','1','NAMES '+(C.names?'ON':'OFF'),C.names)+chip('glow','1','GLOW '+(C.glow?'ON':'OFF'),C.glow)+'</div></div></div>';
  const gt=$('gTempo'); if(gt){ gt.oninput=()=>{ $('gBpm').textContent=gt.value+' BPM'; }; gt.onchange=()=>{ C.bpm=+gt.value; blip(700,0.04); renderGreen(); }; }
  $('greenBody').querySelectorAll('[data-a]').forEach(b=>b.onclick=()=>{ const a=b.dataset.a, v=b.dataset.v; blip(700,0.04);
    if(a==='preset'){ C.preset=v; if(v==='weak'){ const w=earWeakSpots(); if(w.zone){ const z=Object.keys(PR_FRETS).find(k=>k!=='all'&&PR_FRETS[k][0]<=w.zone.lo&&PR_FRETS[k][1]>=w.zone.hi); C.frets=z||'all'; C.strings=w.zone.low?'low':'high'; } } }
    else if(a==='iv'){ const n=+v, cur=C.ivSel||sizes.slice(); const i=cur.indexOf(n); if(i>=0){ if(cur.length>1) cur.splice(i,1); } else cur.push(n); C.ivSel=cur.length===sizes.length?null:cur; }
    else if(a==='frets') C.frets=v; else if(a==='strings') C.strings=v; else if(a==='bpm') C.bpm=Math.max(40,Math.min(140,C.bpm+(+v)));
    else if(a==='names') C.names=!C.names; else if(a==='glow') C.glow=!C.glow;
    renderGreen(); });
}
function openGreenRoom(preset,cfg){ initAudio(); leavePractice(); PRSETUP=Object.assign(pracDefault(),cfg||{}); if(preset){ PRSETUP.preset=preset; if(preset==='weak'){ const w=earWeakSpots(); if(w.zone){ const z=Object.keys(PR_FRETS).find(k=>k!=='all'&&PR_FRETS[k][0]<=w.zone.lo&&PR_FRETS[k][1]>=w.zone.hi); PRSETUP.frets=z||'all'; PRSETUP.strings=w.zone.low?'low':'high'; } } } renderGreen(); goScreen('green'); }
window.startGreenRoom=()=>openGreenRoom('weak');
