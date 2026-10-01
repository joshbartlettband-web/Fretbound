
/* ---------- the callers' bands ---------- */
const RIVAL_FX={lou:'plays it straight: groove window 25% tighter',rosa:'rushes: tempo up 6',dee:'decoy bass: the band sits a fourth off home during the call',jo:'keys mask the call',hale:'sings through your soundcheck: one fewer replay',tam:'trades licks: 1 less Hype per true call',brass:'whips up the crowd: rowdy all night'};
function rivalHas(id){ return !!(state.rivalBand&&state.rivalBand.indexOf(id)>=0); }
function pickRivalBand(){ const n=[0,1,2,3][Math.min(3,(state.legNo||1)-1)]; const pool=Object.keys(MEMBERS).filter(id=>MEMBERS[id].kind==='band'&&!hasSeat(id));
  let seed=((state.runSeed||7)*31+(state.legNo||1)*977+(state.venueIdx||0)*131)|0; const rnd=()=>{ seed=(seed*1103515245+12345)&0x7fffffff; return seed/0x7fffffff; };
  const out=[]; while(out.length<n&&pool.length) out.push(pool.splice(Math.floor(rnd()*pool.length),1)[0]); state.rivalBand=out; return out; }
function rivalBandHTML(){ const b=state.rivalBand||[]; if(!b.length) return '';
  return '<div class="vband"><span class="dim">Backing band</span>'+b.map(id=>'<span><b>'+MEMBERS[id].name+'</b> <i>'+MEMBERS[id].role.toLowerCase()+'</i>: '+RIVAL_FX[id]+'</span>').join('')+'</div>'; }
