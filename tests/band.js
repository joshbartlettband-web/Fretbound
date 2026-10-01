/* ---------- the band: musicians and crew who share the van's seats ----------
   Each has one buff and one quirk, draws wages each night, and plays through the groove engine.
   A saved roster (hired with Fame, some unlocked by ear milestones or by meeting them on tour),
   plus in-run recruits who ask to join backstage at the merch table. */
const MEMBERS={
  lou:{name:'Lou Steady',role:'DRUMS',kind:'band',wage:2,cost:20,buff:'Your groove window is 30% wider.',quirk:'Hates waiting: one fewer replay each night.'},
  rosa:{name:'Rosa Rimshot',role:'DRUMS',kind:'band',wage:2,cost:20,buff:'+2 Hype on every Pocket hit.',quirk:'Pushes the tempo up 8 BPM.'},
  dee:{name:'Deep Dee',role:'BASS',kind:'band',wage:2,cost:25,buff:'Walks the bass up to the call\u2019s second note as you start to answer.',quirk:'Owns the low end: 1 less Tone per note on your two lowest strings.'},
  jo:{name:'Ivory Jo',role:'KEYS',kind:'band',wage:2,cost:20,calls:50,buff:'Plays the call\u2019s chord just before it starts: major or minor.',quirk:'Keeps comping through the call, so it\u2019s harder to hear.'},
  hale:{name:'Harmony Hale',role:'VOCALS',kind:'band',wage:3,cost:20,tour:1,buff:'Sings the call\u2019s first note back after every replay.',quirk:'Rerolls at the merch table cost $1 more.'},
  tam:{name:'Twin Axe Tam',role:'GUITAR',kind:'band',wage:2,cost:25,tour:1,buff:'Doubles your lines an octave up: +1 Tone on every note.',quirk:'Steals the spotlight: 1 less Hype on every true call.'},
  brass:{name:'The Brass Tacks',role:'HORNS',kind:'band',wage:3,cost:35,buff:'Big scores earn +$2 in tips and a horn blast.',quirk:'Three mouths to feed: $3 a night.'},
  tech:{name:'Guitar Tech',role:'CREW',kind:'crew',wage:2,cost:20,buff:'Restrings one snapped string each night, before your packs.',quirk:'Wages only.'},
  fay:{name:'Fader Fay',role:'SOUND',kind:'crew',wage:2,cost:20,buff:'+1 replay every night.',quirk:'Wages only.'}
};
META.met=META.met||{};
function trueCallsAllTime(){ return Object.values(store.stats||{}).reduce((a,s)=>a+((s&&s.correct)||0),0); }
function memberStatus(id){ const M=MEMBERS[id]; if(META.hired[id]) return META.lineup.indexOf(id)>=0?'seated':'hired';
  if(M.calls&&trueCallsAllTime()<M.calls) return 'locked'; if(M.tour&&!META.met[id]) return 'locked'; return 'buy'; }
function lockText(id){ const M=MEMBERS[id]; if(M.calls) return 'Nail '+M.calls+' calls to meet them ('+Math.min(M.calls,trueCallsAllTime())+' so far).'; if(M.tour) return 'Meet them backstage on tour.'; return ''; }
// effects
function bandBpm(){ return hasSeat('rosa')?8:0; }
function bandWindow(){ return hasSeat('lou')?1.3:1; }
function bandNoteTone(a){ return (hasSeat('tam')?1:0)-(hasSeat('dee')&&a.s>=NS-2?1:0); }
function bandHype(){ return hasSeat('tam')?-1:0; }
function bandPocket(){ return hasSeat('rosa')?2:0; }
function rerollCost(){ return REROLL_BASE+(hasSeat('hale')?1:0); }
// what they play
function bandKeysHint(c,t){ if(!hasSeat('jo')||!ctx) return; const r=c.root, rel=new Set(c.notes.map(n=>((n.midi-r)%12+12)%12));
  const third=rel.has(3)&&!rel.has(4)?3:rel.has(4)&&!rel.has(3)?4:null, base=48+((r%12)+12)%12, ms=[base,base+7,base+12]; if(third) ms.push(base+third);
  COMPV.keys(ms,t,BAR*0.85,1.8,musicBus); }
function bandBassHint(){ if(!hasSeat('dee')||!ctx||!state.call||!state.call.notes[1]) return; const m=state.call.notes[1].midi, b=28+(((m%12)-4)+12)%12;
  bnote(mtof(b),ctx.currentTime+0.02,BEAT*1.5,musicBus,{ratio:1,index:1.4,idxDecay:0.12,vol:0.2}); }
function bandEcho(){ if(!hasSeat('hale')||!ctx||!state.call) return; let v=state.call.notes[0].midi; while(v<57) v+=12; while(v>72) v-=12;
  const f=mtof(v), t=ctx.currentTime+0.05, o=ctx.createOscillator(), o2=ctx.createOscillator(), g=ctx.createGain(), g2=ctx.createGain(), lp=ctx.createBiquadFilter(), lfo=ctx.createOscillator(), lg=ctx.createGain();
  o.type='triangle'; o2.type='sine'; o.frequency.value=f; o2.frequency.value=f*2; lp.type='lowpass'; lp.frequency.value=1500; lfo.frequency.value=5.2; lg.gain.value=f*0.012;
  lfo.connect(lg); lg.connect(o.frequency); lg.connect(o2.frequency); g2.gain.value=0.25; o2.connect(g2); g2.connect(lp); o.connect(lp); lp.connect(g); g.connect(musicBus);
  g.gain.setValueAtTime(0.0001,t); g.gain.linearRampToValueAtTime(0.17,t+0.12); g.gain.setValueAtTime(0.17,t+0.7); g.gain.linearRampToValueAtTime(0.0001,t+1.1);
  [o,o2,lfo].forEach(x=>{ x.start(t); x.stop(t+1.2); }); }
let bandRig=null;
function bandDouble(midi,s){ if(!hasSeat('tam')||!ctx) return;
  if(!bandRig||bandRig.ctx0!==ctx){ bandRig=makeRig({pan:0.45,amp:true,dest:musicBus,level:0.32}); bandRig.setGuitar(GUITAR_BY.single); bandRig.setPedals(['glass']); bandRig.ctx0=ctx; }
  bandRig.pluck(midi+12,s,ctx.currentTime+0.02,0.5); }
function bandHorns(t){ const r=tr.root||45, base=55+((r%12)+12)%12;
  [0,0.2].forEach((dt,k)=>[base,base+7,base+12].forEach(m=>bnote(mtof(m),t+dt,k?0.5:0.14,musicBus,{ratio:1,index:3.2,idxDecay:0.25,vol:0.06}))); }
function bandTips(){ if(!hasSeat('brass')) return; state.money+=2; renderCash(); const el=$('topCash'); if(el) pop(el,'+$2 TIPS','#FFC857'); if(ctx) bandHorns(ctx.currentTime+0.05); }
// the van's band tab
function renderVanCrew(){ const o=$('vanCrew'), seats=vanSeats(); META.lineup=META.lineup.filter(id=>META.hired[id]).slice(0,seats);
  o.innerHTML='<div class="van-seats">Seats <b>'+META.lineup.length+' / '+seats+'</b> &middot; tap anyone for details</div><div class="band-grid">'+Object.keys(MEMBERS).map(id=>{ const M=MEMBERS[id], st=memberStatus(id);
    return '<button class="band-tile '+st+'" data-m="'+id+'"><b>'+(st==='locked'?'? ? ?':M.name)+'</b><span>'+M.role+'</span><i>'+(st==='seated'?'SEATED':st==='hired'?'HIRED':st==='buy'?M.cost+' &#9733;':'LOCKED')+'</i></button>'; }).join('')+'</div>';
  o.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>{ blip(700,0.04); memberModal(b.dataset.m); }); }
function memberLines(M){ return '<div class="mem-l"><b>BUFF</b> '+M.buff+'</div><div class="mem-l"><b>QUIRK</b> '+M.quirk+'</div><div class="mem-l"><b>WAGES</b> $'+M.wage+' a night</div>'; }
function memberModal(id){ const M=MEMBERS[id], st=memberStatus(id), full=META.lineup.length>=vanSeats(); let btn='';
  if(st==='buy') btn='<button class="btn gold" id="mHire"'+(META.fame>=M.cost?'':' disabled')+'>HIRE '+M.cost+' &#9733;</button>';
  else if(st==='hired') btn='<button class="btn gold" id="mSeat"'+(full?' disabled':'')+'>'+(full?'SEATS FULL':'SEAT')+'</button>';
  else if(st==='seated') btn='<button class="btn blue" id="mSeat">UNSEAT</button>';
  openModal('<div class="kicker">'+M.role+(M.kind==='crew'?' &middot; CREW':'')+'</div><h3>'+(st==='locked'?'Not met yet':M.name)+'</h3>'+memberLines(M)+
    (st==='locked'?'<div class="mem-l mem-lock">'+lockText(id)+'</div>':'')+'<div class="row-btns">'+btn+'<button class="btn blue" id="mClose">CLOSE</button></div>');
  $('mClose').onclick=()=>closeModal();
  if($('mHire')) $('mHire').onclick=()=>{ if(META.fame<M.cost) return; META.fame-=M.cost; META.hired[id]=1; if(META.lineup.length<vanSeats()) META.lineup.push(id); save(); blip(990,0.08); closeModal(); renderVan(); };
  if($('mSeat')) $('mSeat').onclick=()=>{ const i=META.lineup.indexOf(id); if(i>=0) META.lineup.splice(i,1); else if(META.lineup.length<vanSeats()) META.lineup.push(id); save(); blip(700,0.05); closeModal(); renderVan(); }; }
// backstage recruits at the merch table
function maybeRecruit(force){ if(!state.lineup) state.lineup=[]; if(state.lineup.length>=vanSeats()) return;
  const key=(state.legNo||1)+':'+state.venueIdx; if(state.recruitAsked===key) return; const boss=state.venueIdx===VENUES.length-1;
  if(!force&&!boss&&Math.random()>0.3) return; state.recruitAsked=key;
  const pool=Object.keys(MEMBERS).filter(id=>MEMBERS[id].kind==='band'&&state.lineup.indexOf(id)<0); if(!pool.length) return;
  const id=pool[Math.floor(Math.random()*pool.length)], M=MEMBERS[id];
  openModal('<div class="kicker">Backstage at '+VEN().name+'</div><h3>'+M.name+' wants in</h3><div class="mem-l">'+M.role.charAt(0)+M.role.slice(1).toLowerCase()+'. Wants to join you for the rest of this tour.</div>'+memberLines(M)+
    '<div class="row-btns"><button class="btn gold" id="rYes">TAKE THEM ON</button><button class="btn blue" id="rNo">NOT NOW</button></div>');
  $('rYes').onclick=()=>{ if(state.lineup.length<vanSeats()) state.lineup.push(id); META.met[id]=1; save(); saveRun(); blip(990,0.08); closeModal(); try{ renderShop(); }catch(e){} };
  $('rNo').onclick=()=>{ META.met[id]=1; save(); blip(660,0.05); closeModal(); }; }
