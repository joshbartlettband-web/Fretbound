/* strings and crew: packs, the guitar tech, van seats and gauges */
Object.assign(META,Object.assign({gauge:'standard',rack:0,hired:{},lineup:[]},META));
GARAGE.push({id:'bigvan',name:'Bigger Van',max:2,cost:[30,45],text:l=>'+1 seat for band and crew ('+(2+Math.max(1,l))+' seats).'});
const PACK=3, PACK_MAX=3;
const CREW={tech:{name:'Guitar Tech',cost:20,wage:2,text:'Restrings one snapped string each night, before your packs.'}};
const GAUGES={standard:{name:'Standard',text:'No change.'},heavy:{name:'Heavy',text:'Your first miss each night does not snap. Every note scores 1 less Tone.'},light:{name:'Light',text:'+2 Tone on every note. A miss also snaps the next string.'}};
function vanSeats(){ return 2+(META.van.bigvan||0); }
function hasSeat(id){ return !!(state.lineup&&state.lineup.indexOf(id)>=0); }
function gaugeTone(){ return state.gauge==='heavy'?-1:state.gauge==='light'?2:0; }
function crewWages(){ return (state.lineup||[]).reduce((a,id)=>a+((CREW[id]&&CREW[id].wage)||0),0); }
function crewRestring(){ const s=state.broken.findIndex(Boolean); if(s<0) return; let who='';
  if(hasSeat('tech')&&!state.techUsed){ state.techUsed=true; who='TECH RESTRUNG'; } else if(state.spares>0){ state.spares--; who='SPARE STRING'; }
  if(!who) return; state.broken[s]=false; snap[s]=null; renderStrings(); const el=$('stringsUI').children[5-s]; if(el) pop(el,who,'#8ED36A',true); blip(990,0.06); }
function renderVanStrings(){ const o=$('vanStr');
  if(!META.rack){ const c=15; o.innerHTML='<div class="van-row"><div class="van-txt"><b>String Rack</b><span>Unlocks string gauges: heavy strings that forgive, or light strings that score.</span></div><button class="btn small'+(META.fame>=c?' gold':'')+'" id="vRack"'+(META.fame>=c?'':' disabled')+'>'+c+' &#9733;</button></div>';
    $('vRack').onclick=()=>{ if(META.fame<c) return; META.fame-=c; META.rack=1; save(); blip(990,0.08); renderVan(); }; return; }
  o.innerHTML='<div class="van-gauges">'+Object.keys(GAUGES).map(k=>'<button class="btn small'+(META.gauge===k?' gold':' blue')+'" data-g="'+k+'">'+GAUGES[k].name.toUpperCase()+'</button>').join('')+'</div><div class="van-rules"><span>'+GAUGES[META.gauge].text+'</span></div>';
  o.querySelectorAll('[data-g]').forEach(b=>b.onclick=()=>{ META.gauge=b.dataset.g; save(); blip(700,0.04); renderVan(); }); }
function renderVanCrew(){ const o=$('vanCrew'), seats=vanSeats(); META.lineup=META.lineup.filter(id=>META.hired[id]).slice(0,seats);
  o.innerHTML='<div class="van-seats">Seats <b>'+META.lineup.length+' / '+seats+'</b> &middot; band members join in a later update</div>'+Object.keys(CREW).map(id=>{ const C=CREW[id], h=META.hired[id], sat=META.lineup.indexOf(id)>=0;
    return '<div class="van-row"><div class="van-txt"><b>'+C.name+'</b><span>'+C.text+' Wages $'+C.wage+' a night.</span></div>'+
      (!h?'<button class="btn small'+(META.fame>=C.cost?' gold':'')+'" data-hire="'+id+'"'+(META.fame>=C.cost?'':' disabled')+'>HIRE '+C.cost+' &#9733;</button>':'<button class="btn small '+(sat?'gold':'blue')+'" data-seat="'+id+'"'+(!sat&&META.lineup.length>=seats?' disabled':'')+'>'+(sat?'SEATED':'SEAT')+'</button>')+'</div>'; }).join('');
  o.querySelectorAll('[data-hire]').forEach(b=>b.onclick=()=>{ const id=b.dataset.hire, C=CREW[id]; if(META.fame<C.cost) return; META.fame-=C.cost; META.hired[id]=1; if(META.lineup.length<vanSeats()) META.lineup.push(id); save(); blip(990,0.08); renderVan(); });
  o.querySelectorAll('[data-seat]').forEach(b=>b.onclick=()=>{ const id=b.dataset.seat, i=META.lineup.indexOf(id); if(i>=0) META.lineup.splice(i,1); else if(META.lineup.length<vanSeats()) META.lineup.push(id); save(); blip(700,0.04); renderVan(); }); }
