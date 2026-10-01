/* ---------- world tour themes: each continent's title scene and theme song, unlocked with its passport stamp ----------
   The lead melody, harmony and chords never change, and the lead is always the same guitar rig;
   each continent brings its own rhythm section and synth patches. */
function riffChordAt(r,st){ let c='E5'; for(const n of SONG_RIFF[r]) if(n[0]<=st) c=n[1]; return c; }
function songLeadBar(B,st,t){ SONG_LEAD[B.j].forEach(n=>{ if(n[0]!==st) return; const d=n[1]*SONG.sx; songLead(SONG.lead,n[2],t,d,n[3]);
  if(B.j>=4&&SONG_HARM[n[2]]) songLead(SONG.harm,B.j===7?87:SONG_HARM[n[2]],t+0.004,d,n[3]?(SONG_HARM[n[3]]||n[3]+3):0,0.2); }); }
function songRhythmGain(B,t,lead,other){ [SONG.L,SONG.R].forEach(r=>{ try{ r.out.gain.setTargetAtTime(B.k==='lead'?lead:other,t,0.04); }catch(e){} }); }
function hiArp(n,t,v,st){ const tones=[n[0]+12,n[1]+12,n[2]+12,n[1]+24], m=tones[[0,2,1,3][st%4]], r=st%2?SONG.R:SONG.L; if(!r) return; const old=r.gate; r.gate=0.16; r.pluck(m,2+(st%3),t,v); r.gate=old; }
function chug(n,t,v){ [SONG.L,SONG.R].forEach((r,k)=>{ if(!r) return; const old=r.gate; r.gate=0.07; r.pluck(n[0],5,t+k*0.006,v); r.pluck(n[1],4,t+k*0.006+0.003,v); r.gate=old; }); }
const LEAD_RIGS={lead:[0.05,['ogre','echo'],'single',1.0],harm:[0.3,['ogre','echo'],'single',0.66]};
const SONG_STYLES={
  // highlife: cowbell bell pattern, congas and shaker, clean chorused guitar arpeggios, a bouncing bass and kalimba plucks
  af:{bpm:126,rigs:Object.assign({L:[-0.55,['glass','echo'],'single',0.5],R:[0.55,['glass'],'single',0.46]},LEAD_RIGS),
    step(B,st,t){ const D=SONG.bus, sx=SONG.sx, chord=B.k==='lead'?B.c:B.k==='riff'?riffChordAt(B.r,st):'E5', n=SONG_PC[chord];
      const hit=(name,pat,v)=>{ const c=pat[st]; if(c&&c!=='.') DRUM[name](t,(c==='x'?1:0.62)*v,D,st,n[0]); };
      if(st===0) songRhythmGain(B,t,0.34,0.52);
      if(B.k==='intro'){ hit('shaker','x.o.x.o.x.o.x.o.',0.8); if(st>=8) DRUM.conga(t,0.5+st*0.03,D,st,n[0]); if(st%4===0) hiArp(n,t,0.4+st*0.02,st); return; }
      hit('kick','x.....x...x.....',0.95); hit('clap','....x.......x...',0.7); hit('shaker','xoxoxoxoxoxoxoxo',0.55); hit('cowbell','x..x..x...x.x...',0.45); hit('conga','..o..o.o..x..o.o',0.7);
      if(st===0&&((B.k==='riff'&&B.r===0)||(B.k==='lead'&&B.j%4===0))) DRUM.crashc(t,0.5,D,st,n[0]);
      const play=B.k==='riff'?'x.xx.x.xx.xx.x.x':'x..x..x.x..x.x..'; if(play[st]==='x') hiArp(n,t,B.k==='riff'?0.8:0.6,st);
      const bc='1..1..5.1..8.5..'[st]; if(bc!=='.'){ let m=n[0]+(bc==='5'?7:bc==='8'?12:0); while(m>52) m-=12; while(m<33) m+=12; BASS.electric(m,t,sx*1.7,D); }
      if(st%4===2) fmNote(mtof(n[(st>>2)%3]+24),t,0.32,{ratio:4.0,index:1.6,idxDecay:0.06,vol:0.04,dest:D});
      if(B.k==='lead') songLeadBar(B,st,t); }},
  // synthwave: four on the floor, gated snare, pulsing octave synth bass, palm-muted chugs, a pad, analog brass stabs
  eu:{bpm:118,rigs:Object.assign({L:[-0.7,['ogre'],'humbucker',0.5],R:[0.7,['ogre'],'humbucker',0.5]},LEAD_RIGS),
    step(B,st,t){ const D=SONG.bus, sx=SONG.sx, chord=B.k==='lead'?B.c:B.k==='riff'?riffChordAt(B.r,st):'E5', n=SONG_PC[chord];
      const hit=(name,pat,v)=>{ const c=pat[st]; if(c&&c!=='.') DRUM[name](t,(c==='x'?1:0.62)*v,D,st,n[0]); };
      if(st===0) songRhythmGain(B,t,0.3,0.5);
      let bm=n[0]; while(bm<33) bm+=12; while(bm>45) bm-=12;
      if(B.k==='intro'){ if(st%2===0) DRUM.snare(t,0.2+st*0.05,D,st,n[0]); if(st>=8) BASS.synth(bm+(st%2?12:0),t,sx*0.85,D); if(st===0) COMPV.pad([n[0]+24,n[1]+24,n[2]+24],t,16*sx,2.2,D); return; }
      hit('kick','x...x...x...x...',1.0); hit('snare','....x.......x...',0.8); hit('clap','....x.......x...',0.45); hit('hat','xoxoxoxoxoxoxoxo',0.5); hit('open','..x...x...x...x.',0.35);
      if(st===0&&((B.k==='riff'&&B.r===0)||(B.k==='lead'&&B.j%4===0))) DRUM.crashc(t,0.55,D,st,n[0]);
      BASS.synth(bm+(st%2?12:0),t,sx*0.85,D);
      if(st===0) COMPV.pad([n[0]+24,n[1]+24,n[2]+24],t,16*sx*0.98,2.4,D);
      if(B.k==='riff'&&st%2===0) chug(n,t,0.6);
      if(B.k==='lead'&&(st===0||st===10)) [n[0]+12,n[1]+12,n[2]+12].forEach(m=>fmNote(mtof(m),t,0.32,{ratio:1,index:2.6,idxDecay:0.25,vol:0.028,dest:D}));
      if(B.k==='lead') songLeadBar(B,st,t); }}
};
const TITLE_THEMES={
  na:{name:'NORTH AMERICA',song:'na'},
  af:{name:'AFRICA',song:'af',skies:SKIES_AF,horizon:horizonAF,kinds:[['acacia',12],['baobab',4],['mound',7],['tuft',12],['scrub',6],['rock',5],['rondavel',3],['giraffe',2],['kmpost',4],['fence',3]],big:{baobab:1,rondavel:1,giraffe:1},near:{kmpost:1}},
  eu:{name:'EUROPE',song:'eu',skies:SKIES_EU,horizon:horizonEU,kinds:[['cypress',9],['oak',10],['wall',8],['bale',6],['cottage',4],['church',2],['mill',3],['mile',4],['fence',5],['rock',3],['scrub',4]],big:{cottage:1,church:1,mill:1},near:{mile:1}}
};
const THEME_ORDER=['na','af','sa','eu','as','oc','an'];
function themeUnlocked(id){ if(!TITLE_THEMES[id]) return false; if(id==='na'||store.settings.previewScenes) return true; const T=TOURS.find(x=>x.id===id); return !!(T&&tourStamped(T)); }
function themeList(){ return THEME_ORDER.filter(id=>TITLE_THEMES[id]&&themeUnlocked(id)); }
function titleThemeId(){ const id=store.settings.titleTheme||'na'; return themeUnlocked(id)?id:'na'; }
function curTheme(){ return TITLE_THEMES[titleThemeId()]; }
function themeSkies(){ return curTheme().skies||SKIES; }
function curTitleKinds(){ const T=curTheme(); return T._k||(T._k={kinds:T.kinds||TKINDS,w:(T.kinds||TKINDS).reduce((a,k)=>a+k[1],0),big:T.big||TBIG,near:T.near||{sign:1,diamond:1,mailbox:1}}); }
function restartTitleSong(){ if(!ctx) return; const was=SONG.on; SONG.on=false; try{ if(SONG.bus) SONG.bus.gain.setTargetAtTime(0,ctx.currentTime,0.05); }catch(e){} clearTimeout(SONG.tearT);
  setTimeout(()=>{ try{ if(SONG.bus) SONG.bus.disconnect(); }catch(e){} ['L','R','lead','harm'].forEach(k=>{ try{ SONG[k].out.disconnect(); }catch(e){} SONG[k]=null; }); try{ if(SONG.bass) SONG.bass.disconnect(); }catch(e){} SONG.bus=null; SONG.ctx=null;
    if(was&&state.screen==='title') startTitleSong(); },240); }
function setTitleTheme(id){ if(!themeUnlocked(id)) return; store.settings.titleTheme=id; save(); titleStatic=null; skyIdx=-1; renderTitleScene(); restartTitleSong(); }
function renderTitleScene(){ const el=$('titleScene'); if(!el) return; const id=titleThemeId(), n=themeList().length;
  el.style.setProperty('--cc',CONT_COL[id]||'#E8883A'); $('tsName').textContent=TITLE_THEMES[id].name; $('tsCount').textContent=(store.settings.previewScenes?'PREVIEW ':'')+n+' / 7 SCENES'; }
function tsToast(msg){ const e=$('tsToast'); if(!e) return; e.textContent=msg; e.classList.add('show'); clearTimeout(tsToast.t); tsToast.t=setTimeout(()=>e.classList.remove('show'),3200); }
function stepTitleScene(d){ const L=themeList(); if(L.length<2){ blip(240,0.08); tsToast('Earn a continent\u2019s passport stamp to unlock its scene and song.'); return; }
  const i=L.indexOf(titleThemeId()); blip(760,0.05); setTitleTheme(L[(i+d+L.length)%L.length]); }
// a newly stamped continent becomes the title scene, once, with a note to say so
function checkNewScenes(){ if(store.settings.previewScenes) return; const seen=store.settings.scenesSeen||['na'], fresh=themeList().filter(id=>seen.indexOf(id)<0);
  if(!fresh.length) return; store.settings.scenesSeen=seen.concat(fresh); const id=fresh[fresh.length-1]; save(); setTitleTheme(id); tsToast('New scene unlocked: '+TITLE_THEMES[id].name+', with its own take on the theme.'); }
