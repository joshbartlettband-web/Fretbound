/* ---------- title song: a galloping E minor riff, then a soaring twin lead ----------
   Rhythm guitars are the game's own string models through a real rig (double tracked left and right),
   the lead is a sustaining voice fed into a single coil rig with drive and echo so it can hold, bend and
   sing with vibrato. Bass and drums are synthesized. Scheduled on the audio clock, 16th-note grid. */
const SONG={bpm:138,on:false,t0:0,i:0,timer:null,bus:null,loopFrom:1};
const SONG_PC={E5:[40,47,52],G5:[43,50,55],A5:[45,52,57],D5:[50,57,62],C5:[48,55,60],B5:[47,54,59],Fs5:[42,49,54]};
// riff bars: [step, chord, 16ths long, palm muted]
const SONG_GAL=c=>[[0,c,1,1],[2,c,1,1],[3,c,1,1],[4,c,1,1],[6,c,1,1],[7,c,1,1]];
const SONG_RIFF=[
  [...SONG_GAL('E5'),[8,'G5',4,0],[12,'A5',4,0]],
  [...SONG_GAL('E5'),[8,'D5',4,0],[12,'C5',2,0],[14,'B5',2,0]],
  [...SONG_GAL('E5'),[8,'G5',4,0],[12,'A5',3,0],[15,'A5',1,1]],
  [...SONG_GAL('E5'),[8,'G5',2,0],[10,'Fs5',2,0],[12,'E5',4,0]]];
const SONG_PROG=['E5','C5','D5','B5','E5','C5','D5','B5'];
const SONG_LEAD=[ // [step, 16ths long, midi, bend-from]
  [[0,6,71],[6,2,76],[8,8,79]], [[0,2,78],[2,2,76],[4,4,74],[8,8,76]], [[0,6,74],[6,2,78],[8,8,81]], [[0,2,79],[2,2,78],[4,4,76],[8,8,78,76]],
  [[0,4,71],[4,4,76],[8,4,79],[12,4,83]], [[0,6,84,83],[6,2,83],[8,4,81],[12,4,79]], [[0,4,78],[4,4,79],[8,4,81],[12,4,86,84]], [[0,16,83,81]]];
const SONG_HARM={71:74,76:79,79:83,83:86,84:88,81:84,78:81,86:90,74:78};
// bar plan: 0 intro, 1-8 riff, 9-16 lead; loops back to bar 1
const SONG_BARS=[{k:'intro'},...[0,1,2,3,0,1,2,3].map(r=>({k:'riff',r})),...SONG_PROG.map((c,j)=>({k:'lead',c,j}))];
function songSetup(){
  if(SONG.bus&&SONG.ctx===ctx) return; SONG.ctx=ctx;
  SONG.bus=G(0.85); SONG.bus.connect(musicBus);
  const mk=(pan,fx,gid,lvl)=>{ const r=makeRig({pan,amp:true,room:0.12,dest:SONG.bus,level:lvl}); r.setGuitar(GUITAR_BY[gid]); r.setPedals(fx); return r; };
  SONG.L=mk(-0.75,['dragon'],'humbucker',0.62); SONG.R=mk(0.75,['dragon'],'humbucker',0.62);
  SONG.lead=mk(0.05,['ogre','echo'],'single',0.7); SONG.harm=mk(0.3,['ogre','echo'],'single',0.5);
  SONG.bass=G(0.5); const lp=ctx.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value=620; lp.Q.value=0.8; SONG.bassIn=lp; lp.connect(SONG.bass); SONG.bass.connect(SONG.bus);
}
function songChord(c,t,len,pm,vel){ const n=SONG_PC[c], d=len*SONG.sx;
  [SONG.L,SONG.R].forEach((r,k)=>{ const old=r.gate; r.gate=pm?0.07:Math.max(0.12,d-0.03); const tt=t+(k?0.006:0);
    n.forEach((m,j)=>r.pluck(m,5-j,tt+j*0.003,(pm?0.62:0.85)*(vel||1))); r.gate=old; });
  songBass(n[0]-12,t,pm?Math.min(d,0.1):d*0.92); }
function songBass(m,t,d){ const o=ctx.createOscillator(), g=ctx.createGain(); o.type='sawtooth'; o.frequency.value=mtof(m);
  g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(0.22,t+0.008); g.gain.setTargetAtTime(0.0001,t+d,0.03); o.connect(g); g.connect(SONG.bassIn); o.start(t); o.stop(t+d+0.2); }
function songLead(r,m,t,d,from,vol){ // pick attack from the string model, then a held, singing voice with delayed vibrato
  const old=r.gate; r.gate=0.06; r.pluck(from||m,0,t,0.7); r.gate=old;
  const f=mtof(m), f0=mtof(from||m), g=ctx.createGain(), lfo=ctx.createOscillator(), lg=ctx.createGain(), os=[];
  [-6,6].forEach(dt=>{ const o=ctx.createOscillator(); o.type='sawtooth'; o.detune.value=dt; o.frequency.setValueAtTime(f0,t); if(from) o.frequency.setTargetAtTime(f,t+0.05,0.05); o.connect(g); lg.connect(o.frequency); os.push(o); });
  lfo.frequency.value=5.6; lfo.connect(lg); lg.gain.setValueAtTime(0,t); lg.gain.setValueAtTime(0,t+Math.min(0.28,d*0.45)); lg.gain.linearRampToValueAtTime(f*0.014,t+Math.min(0.6,d*0.8));
  g.gain.setValueAtTime(0.0001,t); g.gain.exponentialRampToValueAtTime(vol||0.16,t+0.012); g.gain.setTargetAtTime(0.0001,t+d-0.02,0.04); g.connect(r.input);
  [...os,lfo].forEach(o=>{ o.start(t); o.stop(t+d+0.25); }); }
function songTom(t,f,v){ const o=ctx.createOscillator(), g=ctx.createGain(); o.frequency.setValueAtTime(f,t); o.frequency.exponentialRampToValueAtTime(f*0.6,t+0.2); g.gain.setValueAtTime(v,t); g.gain.exponentialRampToValueAtTime(0.001,t+0.3); o.connect(g); g.connect(musicBus); o.start(t); o.stop(t+0.32); }
function songCrash(t,v){ noiseHit(t,{type:'highpass',freq:4200,dur:1.4,v:v||0.07,dest:musicBus}); }
function songStep(i,t){
  const nb=SONG_BARS.length, bi=i>>4, st=i&15, bar=bi<nb?bi:SONG.loopFrom+((bi-nb)%(nb-SONG.loopFrom)), B=SONG_BARS[bar];
  if(B.k==='intro'){ if(st%2===0) songChord('E5',t,1,1,0.35+st/24); snare(t,0.05+st*0.012); if(st>=12) songTom(t,st===12?180:st===13?150:st===14?120:95,0.35); return; }
  if(B.k==='riff'){
    SONG_RIFF[B.r].forEach(n=>{ if(n[0]===st) songChord(n[1],t,n[2],n[3]); });
    if(st===0&&(B.r===0)) songCrash(t);
    if([0,2,3,4,6,7,8,12].includes(st)) kick(t,st===8||st===12?0.55:0.4);
    if(st===4||st===12) snare(t,0.24); if(st%2===0) hat(t,st%4===0?0.05:0.03);
    return; }
  if(B.k==='lead'){
    if(st===0) songChord(B.c,t,6,0); else if(st>=6&&st%2===0) songChord(B.c,t,1,1,0.8);
    if(st===0&&B.j%2===0) songCrash(t,B.j===4?0.1:0.07);
    if(st%2===0) kick(t,0.32); if(st===4||st===12) snare(t,0.26); if(st%2===0) hat(t,0.045);
    if(B.j===7&&st>=12) songTom(t,[200,160,130,100][st-12],0.4);
    SONG_LEAD[B.j].forEach(n=>{ if(n[0]!==st) return; const d=n[1]*SONG.sx;
      songLead(SONG.lead,n[2],t,d,n[3]);
      if(B.j>=4&&SONG_HARM[n[2]]) songLead(SONG.harm,B.j===7?87:SONG_HARM[n[2]],t+0.004,d,n[3]?(SONG_HARM[n[3]]||n[3]+3):0,0.12); });
  }
}
function songTick(){ if(!SONG.on||!ctx) return; let t=SONG.t0+SONG.i*SONG.sx;
  while(t<ctx.currentTime+0.15){ if(t>=ctx.currentTime-0.02) try{ songStep(SONG.i,t); }catch(e){} SONG.i++; t=SONG.t0+SONG.i*SONG.sx; } }
function startTitleSong(){
  if(!ctx||SONG.on) return; songSetup(); SONG.sx=60/SONG.bpm/4;
  const now=ctx.currentTime; SONG.bus.gain.cancelScheduledValues(now); SONG.bus.gain.setValueAtTime(0.85,now);
  SONG.on=true; SONG.t0=now+0.12; SONG.i=0; if(!SONG.timer) SONG.timer=setInterval(songTick,25); songTick(); }
function stopTitleSong(){ if(!SONG.on) return; SONG.on=false; if(ctx&&SONG.bus){ const now=ctx.currentTime; SONG.bus.gain.cancelScheduledValues(now); SONG.bus.gain.setTargetAtTime(0,now,0.12); } }
// offline render for level checks: bars from..from+n through the full master chain
async function songTest(from,n){
  const saved={ctx,master,musicBus,roomIn,noiseBuf,SB:SONG.bus,SC:SONG.ctx}, sr=44100, sx=60/SONG.bpm/4, sec=n*16*sx+1.2;
  try{ const off=new OfflineAudioContext(2,Math.floor(sr*sec),sr); ctx=off; master=G(volGain()); master.connect(buildMaster(off)); musicBus=G(musicGain()); musicBus.connect(master);
    noiseBuf=makeNoise(1); roomIn=G(0.5); roomIn.connect(master); SONG.bus=null; songSetup(); SONG.sx=sx;
    for(let i=from*16;i<(from+n)*16;i++) songStep(i,0.05+(i-from*16)*sx);
    const b=await off.startRendering(), L=b.getChannelData(0), R2=b.getChannelData(1), per=[]; let pk=0, ss=0, bad=0;
    const bl=Math.floor(16*sx*sr); for(let k=0;k<n;k++){ let s2=0; for(let j=k*bl;j<(k+1)*bl&&j<L.length;j++){ const v=(L[j]+R2[j])/2; s2+=v*v; } per.push(+(10*Math.log10(s2/bl+1e-12)).toFixed(1)); }
    for(let j=0;j<L.length;j++){ const v=Math.max(Math.abs(L[j]),Math.abs(R2[j])); if(!isFinite(v)) bad++; pk=Math.max(pk,v); ss+=(L[j]*L[j]+R2[j]*R2[j])/2; }
    return {rmsDb:+(10*Math.log10(ss/L.length)).toFixed(1),peak:+pk.toFixed(3),bad,perBar:per};
  } finally { ctx=saved.ctx; master=saved.master; musicBus=saved.musicBus; roomIn=saved.roomIn; noiseBuf=saved.noiseBuf; SONG.bus=saved.SB; SONG.ctx=saved.SC; }
}

