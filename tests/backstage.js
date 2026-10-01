/* ---------- backstage: the hub, the roster, and the ear data behind the coming Ear Report ---------- */
store.dex=store.dex||{callers:{}}; store.fret=store.fret||{}; store.pc=store.pc||{};
function dexC(id){ return store.dex.callers[id]||(store.dex.callers[id]={faced:0,won:0,lost:0,best:0,band:[]}); }
function dexC0(id){ return store.dex.callers[id]||{faced:0,won:0,lost:0,best:0,band:[]}; }
function dexFaced(){ try{ const d=dexC(VEN().id); d.faced++; (state.rivalBand||[]).forEach(m=>{ if(d.band.indexOf(m)<0) d.band.push(m); }); save(); }catch(e){} }
function dexNight(over){ try{ if(!over) return; const d=dexC(VEN().id); if(over==='win') d.won++; else d.lost++; d.best=Math.max(d.best,state.total||0); save(); }catch(e){} }
// every answered note, logged against the cell the call asked for: how often it was found, and how long it took
function earLog(){ try{ const c=state.call, ans=state.answer; if(!c||!ans) return; let prev=state.ansT0||0;
  ans.forEach((a,k)=>{ const tg=c.notes[k]; if(!tg) return; const key=tg.s+','+tg.f, ok=a.midi===tg.midi, at=a.t||prev, ms=Math.min(15000,Math.max(0,at-prev)); prev=at;
    const r=store.fret[key]||(store.fret[key]={n:0,ok:0,ms:0}); r.n++; if(ok) r.ok++; r.ms+=ms;
    const pc=((tg.midi%12)+12)%12, q=store.pc[pc]||(store.pc[pc]={n:0,ok:0,ms:0}); q.n++; if(ok) q.ok++; q.ms+=ms; }); save(); }catch(e){} }
function tourStamped(T){ return T.venues.every(v=>dexC0(v.id).won>0); }
const BS_READY={roster:true,ear:false,green:false};
const CONT_LBL={na:'N.AM',af:'AFR',sa:'S.AM',eu:'EUR',as:'ASIA',oc:'OCE',an:'ANT'};

/* ----- the hub: three doors along a backstage corridor ----- */
function bsDoorArt(kind,locked){
  const W=44,H=76, c=document.createElement('canvas'); c.width=W; c.height=H; c.className='bs-doorcv'; const g=c.getContext('2d');
  const PALS={green:['#62C474','#36914A','#1E5A2E'],ear:['#5A84D8','#3358A0','#1E3868'],roster:['#D4584A','#9A3026','#62201A']}, PAL=PALS[kind]||PALS.green;
  R(g,0,0,W,H,'#140804'); R(g,1,1,W-2,H-1,'#6A4020'); R(g,2,2,W-4,H-2,'#3A2010'); R(g,2,2,W-4,1,'#9A6A38'); R(g,2,2,1,H-2,'#8A5A30');
  for(let y=5;y<H;y++){ const f=(y-5)/(H-5), base=f<0.45?PAL[0]:f<0.82?PAL[1]:PAL[2]; R(g,5,y,W-10,1,base); }
  for(let y=5;y<H;y++) for(let x=5;x<W-5;x++) if(B8[y&7][x&7]/64<0.06+(1-(y-5)/H)*0.06){ g.fillStyle='rgba(255,255,255,.10)'; g.fillRect(x,y,1,1); }
  R(g,5,5,1,H-5,'rgba(255,255,255,.22)'); R(g,W-6,5,1,H-5,'rgba(0,0,0,.38)');
  const pan=(x,y,w,h)=>{ R(g,x,y,w,h,'rgba(0,0,0,.26)'); R(g,x,y,w,1,'rgba(255,255,255,.26)'); R(g,x,y,1,h,'rgba(255,255,255,.16)'); R(g,x,y+h-1,w,1,'rgba(0,0,0,.5)'); R(g,x+w-1,y,1,h,'rgba(0,0,0,.4)'); };
  pan(10,9,24,25); pan(10,40,24,26);
  px(g,33,46,'#7A5A18',4,4); disc(g,35,48,2,'#E0B050'); px(g,34,47,'#FFF0C0',1,1); px(g,32,58,'#140804',7,2);
  R(g,8,H-9,28,6,'#B8842E'); R(g,8,H-9,28,1,'#F4D088'); R(g,8,H-4,28,1,'#6A4812'); [10,34].forEach(x=>px(g,x,H-7,'#3A2408',1,1));
  const cx=22, cy=21;
  if(kind==='green'){ const pts=[]; for(let k=0;k<10;k++){ const an=-Math.PI/2+k*Math.PI/5, rr=k%2?4.4:10; pts.push([Math.round(cx+Math.cos(an)*rr),Math.round(cy+Math.sin(an)*rr)]); }
    pfill(g,pts.map(p=>[p[0]+1,p[1]+1]),'#5A3A08'); pfill(g,pts,'#FFD860'); pfill(g,pts.slice(0,3).concat([[cx,cy]]),'#FFF4B8'); }
  else if(kind==='ear'){ [3,7,12,6,15,9,4].forEach((h,i)=>{ const x=cx-10+i*3; R(g,x,cy-((h/2)|0)+1,2,h,'#0E1830'); R(g,x,cy-((h/2)|0),2,h,i%2?'#7AE8FF':'#B8F4FF'); }); R(g,cx-11,cy+9,22,1,'#0E1830'); }
  else { [[12,12],[24,12]].forEach(q=>{ R(g,q[0],q[1],9,12,'#5A3A08'); R(g,q[0]+1,q[1]+1,7,10,'#F2E4B8'); disc(g,q[0]+4,q[1]+4,2,'#3A2010'); R(g,q[0]+2,q[1]+7,5,3,'#3A2010'); });
    R(g,17,27,10,6,'#5A3A08'); R(g,18,28,8,4,'#F2E4B8'); disc(g,22,29,1,'#3A2010'); }
  if(locked){ R(g,5,5,W-10,H-5,'rgba(14,12,24,.52)'); g.fillStyle='#9A9AA8'; for(let k=0;k<44;k++){ g.fillRect(6+k*0.75|0,14+k*1.1|0,2,2); g.fillRect(38-k*0.75|0,14+k*1.1|0,2,2); }
    R(g,17,40,10,8,'#C8C8D4'); R(g,17,40,10,1,'#FFFFFF'); R(g,17,47,10,1,'#6A6A76'); px(g,21,43,'#3A3A46',2,3); R(g,18,35,2,5,'#8A8A98'); R(g,24,35,2,5,'#8A8A98'); R(g,18,34,8,2,'#8A8A98'); }
  return c; }
function drawBackstageScene(){
  const cv=$('bsScene'); if(!cv) return; const r=cv.getBoundingClientRect(); if(!r.width) return;
  const W=Math.max(120,Math.round(r.width/2)), H=Math.max(120,Math.round(r.height/2)); cv.width=W; cv.height=H; const g=cv.getContext('2d'), fl=Math.round(H*0.84);
  for(let y=0;y<fl;y+=5){ const off=((y/5)&1)?6:0; for(let x=-12;x<W;x+=12){ const hh=h2(x*3+y,y+7), base=hh<0.3?'#3A1E1A':hh<0.7?'#452422':'#502A26'; R(g,x+off,y,11,4,base); R(g,x+off,y,11,1,'rgba(255,200,160,.10)'); R(g,x+off,y+3,11,1,'rgba(0,0,0,.22)'); } R(g,0,y+4,W,1,'#1E0E0C'); }
  R(g,0,0,W,9,'#1A1A20'); R(g,0,2,W,2,'#3A3A46'); R(g,0,7,W,2,'#0C0C10');
  for(let x=0;x<W;x+=2){ const y=Math.round(17+Math.sin(x/W*Math.PI*2.4)*5); R(g,x,y,2,2,'#0C0808'); }
  R(g,0,fl-3,W,3,'#140808'); R(g,0,fl,W,H-fl,'#2A1A12'); for(let y=fl+1;y<H;y+=6){ R(g,0,y,W,1,'#180E08'); for(let x=((y/6)&1)*9;x<W;x+=22) R(g,x,y,1,6,'#180E08'); } R(g,0,fl,W,1,'#6A4028');
  const dr=[...document.querySelectorAll('.bs-door')].map(b=>{ const q=b.getBoundingClientRect(); return (q.left+q.right)/2-r.left; }), xs=[];
  for(let k=0;k<dr.length-1;k++) xs.push(Math.round((dr[k]+dr[k+1])/4)); if(!xs.length) xs.push(W/3,2*W/3);
  xs.forEach(sx=>{ const sy=Math.round(fl*0.4);
    for(let y=sy-34;y<=sy+34;y++) for(let x=sx-34;x<=sx+34;x++){ if(x<0||x>=W||y<0||y>=H) continue; const d=Math.hypot(x-sx,(y-sy)*1.1)/34; if(d<1&&B8[y&7][x&7]/64<(1-d)*0.42){ g.fillStyle='rgba(255,188,100,.55)'; g.fillRect(x,y,1,1); } }
    R(g,sx-1,sy-6,3,12,'#3A2A1A'); R(g,sx-3,sy-9,7,4,'#C8963A'); R(g,sx-3,sy-9,7,1,'#F4D088'); R(g,sx-4,sy-5,9,9,'#FFD890'); R(g,sx-3,sy-4,7,7,'#FFF0C8'); R(g,sx-4,sy+4,9,2,'#8A5A1A'); });
  const cs=(x,w,h)=>{ R(g,x,fl-h,w,h,'#2A2A32'); R(g,x,fl-h,w,2,'#5A5A66'); R(g,x+1,fl-h+2,1,h-2,'#3A3A44'); R(g,x,fl-h,3,3,'#A8A8B4'); R(g,x+w-3,fl-h,3,3,'#A8A8B4'); R(g,x,fl-3,3,3,'#A8A8B4'); R(g,x+w-3,fl-3,3,3,'#A8A8B4'); R(g,x+5,fl-(h>>1)-2,w-10,6,'#E0C060'); R(g,x+6,fl-(h>>1)-1,w-12,4,'#2A2A32'); for(let k=0;k<(w-14)/4;k++) R(g,x+8+k*4,fl-(h>>1),2,2,'#E0C060'); };
  cs(3,30,24); cs(W-36,32,30); cs(W-32,26,14);
}
function renderBackstage(){
  const bits=[['green','GREEN ROOM','green'],['ear','EAR REPORT','ear'],['roster','THE ROSTER','roster']];
  const ALL=TOURS.flatMap(T=>T.venues), met=ALL.filter(v=>dexC0(v.id).faced>0).length;
  $('bsDoors').innerHTML=''; 
  bits.forEach(([kind,label,key])=>{ const ready=BS_READY[key], b=document.createElement('button'); b.className='bs-door'+(ready?'':' locked'); b.dataset.door=key; b.setAttribute('aria-label',label+(ready?'':' (opening soon)'));
    b.appendChild(bsDoorArt(kind,!ready));
    const pl=document.createElement('span'); pl.className='bs-plate'; pl.innerHTML=label+'<i>'+(ready?(key==='roster'?met+' / '+ALL.length+' met':''):'OPENING SOON')+'</i>'; b.appendChild(pl);
    b.onclick=()=>{ if(!ready){ blip(240,0.09); $('bsMsg').textContent={green:'The Green Room is being wired for sound. Opening soon.',ear:'The Ear Report is still being written. Opening soon.'}[key]||''; clearTimeout(renderBackstage.t); renderBackstage.t=setTimeout(()=>{ $('bsMsg').textContent=''; },2600); return; }
      blip(880,0.06); if(key==='roster') goRoster(); };
    $('bsDoors').appendChild(b); });
  $('bsMsg').textContent='';
}
function goBackstage(){ renderBackstage(); goScreen('backstage'); requestAnimationFrame(()=>requestAnimationFrame(drawBackstageScene)); }

/* ----- the roster ----- */
let rosterTab='callers', rosterCont=0;
function stampCv(T,earned){ const c=document.createElement('canvas'); c.width=30; c.height=30; c.className='rstamp-cv'; const g=c.getContext('2d'), col=earned?(CONT_COL[T.id]||'#C8963A'):'#4A3A30';
  R(g,0,0,30,30,earned?'#F2E4B8':'#2A1C14'); for(let k=0;k<30;k+=3){ [[k,0],[k,29],[0,k],[29,k]].forEach(q=>px(g,q[0],q[1],'#140804',2,2)); }
  R(g,3,3,24,24,earned?'#E8D8A8':'#1E120C'); g.strokeStyle=col; g.lineWidth=2; g.beginPath(); g.arc(15,15,9,0,Math.PI*2); g.stroke();
  if(earned){ g.fillStyle=col; [[9,15],[10,16],[11,17],[12,18],[13,17],[14,16],[15,15],[16,14],[17,13],[18,12],[19,11]].forEach(q=>g.fillRect(q[0],q[1],2,2)); } else { px(g,14,10,'#6A5A4A',2,7); px(g,14,19,'#6A5A4A',2,2); }
  return c; }
function rosterCallerCard(v,T){ const d=dexC0(v.id), met=d.faced>0, cc=CONT_COL[T.id]||'#C8963A', img='<img class="rc-por'+(met?'':' lock')+'" alt="" src="'+(RIVAL_PORT[v.id]||'')+'" style="border-color:'+cc+'">';
  const kick='<div class="kicker">'+T.name+' &middot; Night '+v.night+'</div>';
  if(!met){ openModal('<div class="rc-top">'+img+'<div class="rc-meta">'+kick+'<h3>? ? ?</h3><div class="mem-l">Someone is waiting at <b>'+v.short+'</b>, '+v.place+'.</div></div></div><div class="mem-l mem-lock">Face them on tour to meet them.</div><div class="row-btns"><button class="btn blue" id="rcX">CLOSE</button></div>'); }
  else { const band=(d.band||[]).filter(id=>MEMBERS[id]).map(id=>(MEMBER_PORT[id]?'<img class="vb-por" alt="" src="'+MEMBER_PORT[id]+'">':'')+MEMBERS[id].name).join(' &middot; ');
    openModal('<div class="rc-top">'+img+'<div class="rc-meta">'+kick+'<h3>'+titleCase(v.rival)+'</h3><div class="mem-l rc-sub">'+v.rivalSub+'</div><div class="mem-l"><b>PLAYS</b> '+v.name+', '+v.place+'</div><div class="mem-l"><b>RULE</b> '+v.rule+'. '+v.ruleText+'</div></div></div>'+
      '<div class="mem-l"><b>RECORD</b> Faced '+d.faced+', beaten '+d.won+', lost '+d.lost+(d.best?'. Best night '+d.best:'')+'</div>'+(band?'<div class="mem-l"><b>HEARD WITH</b> '+band+'</div>':'')+
      (v.liner?'<div class="rc-liner"><b>'+v.liner.title+'</b><span>'+v.liner.text+'</span>'+(v.liner.listen?'<em>Listen: '+v.liner.listen+'</em>':'')+'</div>':'')+
      '<div class="row-btns"><button class="btn blue" id="rcX">CLOSE</button></div>'); }
  $('rcX').onclick=()=>closeModal(); }
function rosterMemberCard(id){ const M=MEMBERS[id], st=memberStatus(id), locked=st==='locked', stTxt={seated:'In your van',hired:'Hired',buy:'For hire in the Van',locked:''}[st];
  const img='<img class="rc-por'+(locked?' lock':'')+'" alt="" src="'+(MEMBER_PORT[id]||'')+'" style="border-color:var(--brass)">';
  openModal('<div class="rc-top">'+img+'<div class="rc-meta"><div class="kicker">'+M.role+(M.kind==='crew'?' &middot; CREW':'')+'</div><h3>'+(locked?'? ? ?':M.name)+'</h3>'+(locked?'<div class="mem-l mem-lock">'+lockText(id)+'</div>':memberLines(M)+'<div class="mem-l"><b>STATUS</b> '+stTxt+'</div>')+'</div></div><div class="row-btns"><button class="btn blue" id="rcX">CLOSE</button></div>');
  $('rcX').onclick=()=>closeModal(); }
function renderRoster(){
  const ALL=TOURS.flatMap(T=>T.venues), met=ALL.filter(v=>dexC0(v.id).faced>0).length, beaten=ALL.filter(v=>dexC0(v.id).won>0).length, stamps=TOURS.filter(tourStamped).length;
  $('rosterSub').innerHTML='Met <b>'+met+'/'+ALL.length+'</b> &middot; Beaten <b>'+beaten+'</b> &middot; Stamps <b>'+stamps+'/'+TOURS.length+'</b>';
  document.querySelectorAll('.roster-tabs .tab').forEach(b=>b.classList.toggle('sel',b.dataset.rt===rosterTab));
  const body=$('rosterBody'); body.innerHTML='';
  if(rosterTab==='callers'){
    const T=TOURS[Math.min(rosterCont,TOURS.length-1)], cc=CONT_COL[T.id]||'#C8963A';
    const tabs=document.createElement('div'); tabs.className='rconts';
    TOURS.forEach((t2,i)=>{ const b=document.createElement('button'); b.className='ttab'+(i===rosterCont?' sel':''); b.style.setProperty('--cc',CONT_COL[t2.id]||'#C8963A'); b.textContent=CONT_LBL[t2.id]||t2.short; b.setAttribute('aria-label',t2.name); b.onclick=()=>{ rosterCont=i; blip(700,0.04); renderRoster(); }; tabs.appendChild(b); });
    body.appendChild(tabs);
    const head=document.createElement('div'); head.className='rhead'; head.innerHTML='<b>'+T.name+'</b><span>'+T.blurb+'</span>'; body.appendChild(head);
    const grid=document.createElement('div'); grid.className='rgrid'; grid.style.setProperty('--cc',cc);
    T.venues.forEach(v=>{ const d=dexC0(v.id), met2=d.faced>0, b=document.createElement('button'); b.className='rtile'+(met2?'':' unmet')+(d.won?' beaten':''); b.style.setProperty('--cc',cc);
      b.innerHTML='<img class="rt-por'+(met2?'':' lock')+'" alt="" src="'+(RIVAL_PORT[v.id]||'')+'">'+(d.won?'<i class="rt-medal"></i>':'')+'<span class="rt-name">'+(met2?titleCase(v.rival):'? ? ?')+'</span><span class="rt-rec">'+(met2?('Beaten '+d.won+' &middot; Lost '+d.lost):v.short)+'</span>';
      b.onclick=()=>{ blip(700,0.04); rosterCallerCard(v,T); }; grid.appendChild(b); });
    body.appendChild(grid);
    const done=T.venues.filter(v=>dexC0(v.id).won>0).length, earned=done===T.venues.length, row=document.createElement('div'); row.className='rstamp'+(earned?' earned':'');
    row.appendChild(stampCv(T,earned)); const tx=document.createElement('span'); tx.innerHTML=earned?'<b>Passport stamped.</b> You beat all three callers in '+T.name+'.':'<b>Passport stamp.</b> Beat all three callers in '+T.name+' ('+done+'/'+T.venues.length+').'; row.appendChild(tx); body.appendChild(row);
  } else {
    const ids=Object.keys(MEMBERS), grid=document.createElement('div'); grid.className='rgrid rband';
    ids.forEach(id=>{ const M=MEMBERS[id], st=memberStatus(id), locked=st==='locked', b=document.createElement('button'); b.className='rtile'+(locked?' unmet':'')+(st==='seated'||st==='hired'?' beaten':'');
      b.innerHTML='<img class="rt-por'+(locked?' lock':'')+'" alt="" src="'+(MEMBER_PORT[id]||'')+'"><span class="rt-name">'+(locked?'? ? ?':M.name)+'</span><span class="rt-rec">'+(locked?M.role:({seated:'IN THE VAN',hired:'HIRED',buy:'FOR HIRE'}[st]))+'</span>';
      b.onclick=()=>{ blip(700,0.04); rosterMemberCard(id); }; grid.appendChild(b); });
    body.appendChild(grid);
  }
}
function goRoster(){ renderRoster(); goScreen('roster'); }
