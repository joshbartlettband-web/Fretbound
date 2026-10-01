/* ---------- the ear report: where on the neck, and which notes, you find or lose ---------- */
const EAR_ZONES=[[0,4,'near the nut'],[5,8,'around frets 5 to 8'],[9,12,'around frets 9 to 12'],[13,15,'above fret 12']];
let earMode='acc';
function earCount(){ return Object.values(store.fret||{}).reduce((a,r)=>a+(r.n||0),0); }
function earCells(){ const F=store.fret||{}, out=[]; Object.keys(F).forEach(k=>{ const p=k.split(',').map(Number), r=F[k]; if(r&&r.n) out.push({s:p[0],f:p[1],n:r.n,ok:r.ok,avg:r.ms/r.n}); }); return out; }
function earSummary(){
  const cells=earCells(), P=store.pc||{}; let N=0,OK=0,MS=0; cells.forEach(c=>{ N+=c.n; OK+=c.ok; MS+=c.avg*c.n; });
  const avg=N?MS/N:0, acc=N?OK/N:0, zones=[];
  for(let g=0;g<2;g++) EAR_ZONES.forEach((z,zi)=>{ const cs=cells.filter(c=>(g?c.s>=3:c.s<=2)&&c.f>=z[0]&&c.f<=z[1]); const n=cs.reduce((a,c)=>a+c.n,0), ok=cs.reduce((a,c)=>a+c.ok,0), ms=cs.reduce((a,c)=>a+c.avg*c.n,0); zones.push({g,zi,n,ok,acc:n?ok/n:null,avg:n?ms/n:null}); });
  const pcs=Object.keys(P).map(k=>({pc:+k,n:P[k].n,ok:P[k].ok,acc:P[k].ok/P[k].n,avg:P[k].ms/P[k].n})).filter(x=>x.n>0);
  const hands=HANDS.filter(h=>store.stats[h.id]&&store.stats[h.id].seen>=2).map(h=>({h,seen:store.stats[h.id].seen,acc:store.stats[h.id].correct/store.stats[h.id].seen}));
  const missed=pcs.filter(x=>x.n>=3&&x.acc<1).sort((a,b)=>a.acc-b.acc||b.n-a.n).slice(0,3);
  const slow=pcs.filter(x=>x.n>=3).sort((a,b)=>b.avg-a.avg).slice(0,3);
  const weakHands=hands.filter(x=>x.acc<1).sort((a,b)=>a.acc-b.acc||b.seen-a.seen).slice(0,3);
  const cand=zones.filter(z=>z.n>=6), weakZone=cand.filter(z=>z.acc<0.8).sort((a,b)=>a.acc-b.acc)[0], slowZone=cand.filter(z=>z.avg>avg*1.35).sort((a,b)=>b.avg-a.avg)[0];
  let text; const zn=z=>'the '+(z.g?'low':'high')+' strings '+EAR_ZONES[z.zi][2];
  if(N<12) text='Play a few more nights and your Ear Report will fill in. So far: '+N+' note'+(N===1?'':'s')+' logged.';
  else { const parts=[];
    if(weakZone) parts.push('You miss the most on '+zn(weakZone)+' ('+Math.round(weakZone.acc*100)+'% found).'); else if(slowZone) parts.push('You hesitate the longest on '+zn(slowZone)+'.');
    const worst=pcs.filter(x=>x.n>=4&&x.acc<=0.75).sort((a,b)=>a.acc-b.acc)[0], slowPc=pcs.filter(x=>x.n>=4).sort((a,b)=>b.avg-a.avg)[0];
    if(worst) parts.push(NN[worst.pc]+' is your toughest note: you find it '+Math.round(worst.acc*100)+'% of the time.');
    else if(!parts.length&&slowPc&&slowPc.avg>avg*1.4) parts.push(NN[slowPc.pc]+' takes you the longest, about '+(slowPc.avg/1000).toFixed(1)+' seconds.');
    text=parts.length?parts.join(' '):(acc>=0.9?'Solid across the neck so far. Nothing stands out yet.':'Nothing stands out yet. Keep playing and this sharpens every night.'); }
  return {N,acc,avg,cells,zones,pcs,missed,slow,weakHands,weakZone:weakZone||slowZone||null,worstPc:missed[0]||null,text};
}
// what the Green Room will practise when you tap PRACTICE THESE
function earWeakSpots(){ const S=earSummary(); return {hands:S.weakHands.map(x=>x.h.id), zone:S.weakZone?{lo:EAR_ZONES[S.weakZone.zi][0],hi:EAR_ZONES[S.weakZone.zi][1],low:!!S.weakZone.g}:null, pcs:S.missed.map(x=>x.pc)}; }
function earColor(mode,c,ref){ const lerp=(a,b,u)=>a.map((v,i)=>Math.round(v+(b[i]-v)*u)), C={red:[224,72,72],org:[240,138,48],yel:[232,208,72],grn:[90,214,106]};
  let u; if(mode==='acc'){ u=c.ok/c.n; } else { const r=c.avg/(ref||1); u=1-Math.min(1,Math.max(0,(r-0.6)/1.0)); }
  const col=u>=0.75?lerp(C.yel,C.grn,(u-0.75)/0.25):u>=0.5?lerp(C.org,C.yel,(u-0.5)/0.25):lerp(C.red,C.org,u/0.5); return col; }
function drawEarMap(cv,mode){
  const box=cv.parentElement, cssW=Math.max(220,Math.floor(box.clientWidth)), cells=earCells(), maxS=cells.reduce((a,c)=>Math.max(a,c.s),5), NSr=Math.max(6,maxS+1), lab=16, cols=16, cw=(cssW-lab)/cols, rh=Math.min(20,Math.max(14,Math.round(cw*0.85))), botM=13, cssH=Math.round(NSr*rh+botM+2), DPR=2;
  cv.width=Math.round(cssW*DPR); cv.height=cssH*DPR; cv.style.width=cssW+'px'; cv.style.height=cssH+'px'; const g=cv.getContext('2d'); g.setTransform(DPR,0,0,DPR,0,0); g.imageSmoothingEnabled=false;
  const wood=g.createLinearGradient(0,0,0,NSr*rh); wood.addColorStop(0,'#3A1E10'); wood.addColorStop(1,'#241208'); g.fillStyle=wood; g.fillRect(lab,0,cssW-lab,NSr*rh);
  for(let i=0;i<120;i++){ g.fillStyle='rgba(0,0,0,.14)'; g.fillRect(lab+Math.floor(h2(i,11)*(cssW-lab)),Math.floor(h2(i,12)*NSr*rh),3+Math.floor(h2(i,13)*7),1); }
  [3,5,7,9,15].forEach(f=>{ g.fillStyle='rgba(240,230,200,.16)'; g.beginPath(); g.arc(lab+(f+0.5)*cw,NSr*rh/2,Math.min(4,cw*0.2),0,7); g.fill(); }); [NSr*rh/3,2*NSr*rh/3].forEach(y=>{ g.fillStyle='rgba(240,230,200,.16)'; g.beginPath(); g.arc(lab+12.5*cw,y,Math.min(4,cw*0.2),0,7); g.fill(); });
  for(let s=0;s<NSr;s++){ g.fillStyle='rgba(216,204,170,'+(s<3?0.45:0.6)+')'; g.fillRect(lab,Math.round((s+0.5)*rh),cssW-lab,s<3?1:2); }
  g.fillStyle='rgba(150,150,160,.6)'; for(let f=1;f<cols;f++) g.fillRect(Math.round(lab+(f+1)*cw)-1,0,1,NSr*rh); g.fillStyle='#E8E0C8'; g.fillRect(Math.round(lab+cw)-2,0,3,NSr*rh);
  const have={}; cells.forEach(c=>have[c.s+','+c.f]=c); const avs=cells.map(c=>c.avg).sort((a,b)=>a-b), ref=avs.length?avs[avs.length>>1]:1;
  for(let s=0;s<NSr;s++) for(let f=0;f<cols;f++){ const c=have[s+','+f], x=lab+f*cw, y=s*rh;
    if(!c){ g.fillStyle='rgba(255,255,255,.10)'; g.fillRect(Math.round(x+cw/2)-1,Math.round(y+rh/2)-1,2,2); continue; }
    const col=earColor(mode,c,ref), a=0.42+0.58*Math.min(1,c.n/5); g.fillStyle='rgba('+col[0]+','+col[1]+','+col[2]+','+a.toFixed(2)+')'; g.fillRect(Math.round(x)+1.5,y+1.5,Math.round(cw)-3,rh-3);
    g.strokeStyle='rgba(10,4,4,.65)'; g.lineWidth=1; g.strokeRect(Math.round(x)+1.5,y+1.5,Math.round(cw)-3,rh-3); }
  if(cv.__sel){ const s=cv.__sel[0], f=cv.__sel[1]; g.strokeStyle='#FFFFFF'; g.lineWidth=2; g.strokeRect(Math.round(lab+f*cw)+1,s*rh+1,Math.round(cw)-2,rh-2); }
  g.fillStyle='#C8B898'; g.font="12px 'Jersey 10',monospace"; g.textBaseline='middle'; g.textAlign='center'; for(let s=0;s<NSr;s++) g.fillText(SNAMES[s]||'',lab/2,(s+0.5)*rh+1);
  g.font="11px 'Jersey 10',monospace"; g.textBaseline='top'; [0,3,5,7,9,12,15].forEach(f=>g.fillText(String(f),lab+(f+0.5)*cw,NSr*rh+2));
  cv.__geo={lab,cw,rh,NSr,cols};
}
function earCellText(s,f){ const r=(store.fret||{})[s+','+f], nm=SNAMES[s]||''; if(!r||!r.n) return 'String '+nm+', fret '+f+': not tested yet.'; return 'String '+nm+', fret '+f+': found '+r.ok+' of '+r.n+' ('+Math.round(r.ok/r.n*100)+'%), about '+(r.ms/r.n/1000).toFixed(1)+'s.'; }
function earRows(list,fmt){ return list.length?list.map(fmt).join(''):'<div class="ear-row"><span class="dim">Nothing yet</span></div>'; }
function renderEar(root,opts){ opts=opts||{}; const S=earSummary();
  const lists='<div class="ear-lists"><div><h4>MOST MISSED NOTES</h4>'+earRows(S.missed,x=>'<div class="ear-row"><span>'+NN[x.pc]+'</span><b>'+Math.round(x.acc*100)+'%</b><em>'+x.n+'x</em></div>')+'</div>'+
    '<div><h4>SLOWEST NOTES</h4>'+earRows(S.slow,x=>'<div class="ear-row"><span>'+NN[x.pc]+'</span><b>'+(x.avg/1000).toFixed(1)+'s</b><em>'+x.n+'x</em></div>')+'</div>'+
    '<div><h4>WEAKEST CALLS</h4>'+earRows(S.weakHands,x=>'<div class="ear-row"><span>'+x.h.name+'</span><b>'+Math.round(x.acc*100)+'%</b><em>'+x.seen+'x</em></div>')+'</div></div>';
  root.innerHTML='<div class="ear-mode"><button data-m="acc" class="'+(earMode==='acc'?'sel':'')+'">ACCURACY</button><button data-m="spd" class="'+(earMode==='spd'?'sel':'')+'">SPEED</button></div>'+
    '<div class="ear-mapbox"><canvas class="ear-map" aria-label="Fretboard heatmap of your accuracy and speed"></canvas></div>'+
    '<div class="ear-legend"><span>'+(earMode==='acc'?'MISSED':'FAST')+'</span><i class="ear-bar '+earMode+'"></i><span>'+(earMode==='acc'?'FOUND':'SLOW')+'</span></div>'+
    '<div class="ear-detail" id="earDetail">Tap a cell for details.</div><div class="ear-take">'+S.text+'</div>'+(opts.compact?'<button class="btn small blue" id="earFull">FULL REPORT</button>':lists);
  const cv=root.querySelector('.ear-map'); drawEarMap(cv,earMode);
  cv.onpointerdown=e=>{ const r=cv.getBoundingClientRect(), G=cv.__geo, x=e.clientX-r.left, y=e.clientY-r.top, f=Math.floor((x-G.lab)/G.cw), s=Math.floor(y/G.rh); if(f<0||f>=G.cols||s<0||s>=G.NSr) return; cv.__sel=[s,f]; drawEarMap(cv,earMode); root.querySelector('#earDetail').textContent=earCellText(s,f); blip(600+s*40,0.03); };
  root.querySelectorAll('.ear-mode button').forEach(b=>b.onclick=()=>{ earMode=b.dataset.m; blip(700,0.04); renderEar(root,opts); });
  if(opts.compact&&root.querySelector('#earFull')) root.querySelector('#earFull').onclick=()=>{ blip(880,0.06); goEar(); };
}
function goEar(){ $('earSub').textContent=earCount()+' notes logged on your device'; $('btnEarPractice').disabled=!BS_READY.green; $('btnEarPractice').textContent=BS_READY.green?'PRACTICE THESE':'PRACTICE THESE (SOON)'; goScreen('ear'); requestAnimationFrame(()=>requestAnimationFrame(()=>renderEar($('earPanel'),{}))); }
