/* ---------- the meta game: Fame, the Van, the Garage and Tough Crowd ----------
   Saved in store.meta (versioned). Fame is paid when a run ends. Garage upgrades are small conveniences;
   Tough Crowd levels, unlocked by winning, push back. */
store.meta=Object.assign({v:1,fame:0,van:{},tough:0,toughMax:0,runs:0,wins:0},store.meta||{});
const META=store.meta;
const GARAGE=[
  {id:'trunk',name:'Merch Trunk',max:2,cost:[12,20],text:l=>'Start each run with +$'+(2*Math.max(1,l))+'.'},
  {id:'tire',name:'Spare Tire',max:1,cost:[18],text:()=>'+1 replay on the first night of every leg.'},
  {id:'cooler',name:'Van Cooler',max:1,cost:[15],text:()=>'+$1 for every night you clear.'}];
const TOUGH=[
  {name:'Picky Crowd',text:'Targets are 15% higher.'},
  {name:'Short Soundcheck',text:'One fewer replay every night.'},
  {name:'Lights Out',text:'In the final leg, the first note never glows.'}];
function toughMult(){ return (state.tough||0)>=1?1.15:1; }
function metaVenue(){ const t=state.tough||0;
  if(META.van.tire&&state.venueIdx===0) state.replays++;
  if(t>=2) state.replays=Math.max(0,state.replays-1);
  if(t>=3&&(state.legNo||1)>=RUN_LEGS) state.noGlow=true; }
function metaRunEnd(won){
  const nights=((state.legNo||1)-1)*3+(state.cleared?state.cleared.length:0), t=state.tough||0;
  const gain=2*nights+(won?10+4*t:0)+Math.floor((state.money||0)/5);
  META.fame+=gain; META.runs++; if(won){ META.wins++; if(t>=META.toughMax&&t<TOUGH.length) META.toughMax=t+1; }
  save(); state.fameGain=gain; state.fameWon=won; return gain; }
function renderVan(){
  $('vanFame').innerHTML='Fame <b>'+META.fame+' &#9733;</b> &middot; '+META.runs+' runs, '+META.wins+' tours won';
  $('vanList').innerHTML=GARAGE.map(u=>{ const l=META.van[u.id]||0, done=l>=u.max, c=done?0:u.cost[l];
    return '<div class="van-row"><div class="van-txt"><b>'+u.name+(u.max>1?' '+('&#9679;'.repeat(l))+('&#9675;'.repeat(u.max-l)):'')+'</b><span>'+u.text(done?l:l+1)+'</span></div>'+
      (done?'<span class="van-own">OWNED</span>':'<button class="btn small'+(META.fame>=c?' gold':'')+'" data-van="'+u.id+'"'+(META.fame>=c?'':' disabled')+'>'+c+' &#9733;</button>')+'</div>'; }).join('');
  $('vanList').querySelectorAll('[data-van]').forEach(b=>b.onclick=()=>{ const u=GARAGE.find(x=>x.id===b.dataset.van), l=META.van[u.id]||0, c=u.cost[l];
    if(META.fame<c||l>=u.max) return; META.fame-=c; META.van[u.id]=l+1; save(); blip(990,0.08); renderVan(); });
  const t=Math.min(META.tough,META.toughMax);
  $('vanTough').innerHTML='<div class="van-tt"><button class="btn small blue" id="tDown"'+(t>0?'':' disabled')+'>&lt;</button><b>TOUGH CROWD '+t+'</b><button class="btn small blue" id="tUp"'+(t<META.toughMax?'':' disabled')+'>&gt;</button></div>'+
    '<div class="van-rules">'+(t?TOUGH.slice(0,t).map((r,i)=>'<span><b>'+(i+1)+'. '+r.name+'.</b> '+r.text+'</span>').join(''):'<span>The house crowd. Win a tour to unlock Tough Crowd '+(META.toughMax?'levels':'1')+'.</span>')+'</div>';
  const set=v=>{ META.tough=Math.max(0,Math.min(META.toughMax,v)); save(); blip(700,0.04); renderVan(); };
  $('tDown').onclick=()=>set(t-1); $('tUp').onclick=()=>set(t+1);
}
function goVan(){ renderVan(); goScreen('van'); }
