/* ---------- callers on the rig ----------
   Each caller keeps their own vector costume. The costume leans about the hips and nods about the neck
   (blended over the neckline so collars bend instead of tearing); the rig adds the guitar at the caller's
   scale and two-bone arms whose fretting hand glides to the fret of each note they play. */
function xfPt(x,y,T){ let X=x, Y=y;
  if(T.nod){ const w=Math.max(0,Math.min(1,(T.neckY-Y)/6)); if(w>0){ const a=T.nod*w, c=Math.cos(a), s=Math.sin(a), dx=X, dy=Y-T.neckY; X=dx*c-dy*s; Y=T.neckY+dx*s+dy*c; } }
  if(T.lean){ const c=Math.cos(T.lean), s=Math.sin(T.lean), dx=X, dy=Y-T.hipY; X=dx*c-dy*s; Y=T.hipY+dx*s+dy*c; }
  return [X,Y]; }
function xfPath(str,f){ const tk=String(str).match(/[A-Za-z]|-?\d*\.?\d+(?:e[-+]?\d+)?/g)||[], out=[]; let cmd='';
  for(let i=0;i<tk.length;i++){ const x=tk[i]; if(/[A-Za-z]/.test(x)){ cmd=x.toUpperCase(); out.push(cmd); continue; }
    if(cmd==='A'){ const a=tk.slice(i,i+7).map(Number), p=f(a[5],a[6]); out.push(a[0],a[1],a[2],a[3],a[4],f2(p[0]),f2(p[1])); i+=6; }
    else { const p=f(+tk[i],+tk[i+1]); out.push(f2(p[0]),f2(p[1])); i+=1; } }
  return out.join(' '); }
function xfLayers(L,f,ang){ return L.filter(Boolean).map(l=>{ const o=Object.assign({},l);
  if(l.d) o.d=xfPath(l.d,f); if(l.s) o.s=xfPath(l.s,f);
  if(l.e){ const p=f(l.e[0],l.e[1]); o.e=[p[0],p[1],l.e[2],l.e[3],(l.e[4]||0)+(ang||0)]; }
  if(l.p){ const p=f(l.p[0],l.p[1]); o.p=[p[0],p[1],l.p[2],l.p[3]]; }
  return o; }); }
function rivalRigLayers(id,q){
  const R=RIVAL_VEC[id], P=R.P, p={s:R.s,sway:0,strum:0,blink:!!q.blink};
  const lean=((q.lean||0)*4-(q.slump||0)*6-(q.gloat||0)*5)*Math.PI/180, nod=((q.nod||0)*9+(q.slump||0)*12-(q.gloat||0)*9)*Math.PI/180;
  const T={hipY:-44,neckY:R.neckY||-80,lean,nod}, f=(x,y)=>xfPt(x,y,T), P2=(x,y)=>{ const r=f(x,y); return {x:r[0],y:r[1]}; };
  const L=xfLayers(R.body(P,p),f,lean);
  // the guitar, at this caller's scale and in their colours
  const sc=1.25, a0=-0.33+(q.slump||0)*0.22-(q.gloat||0)*0.25+lean*0.5, C=P2(1,-52.5), gt=R.gt;
  const pal=Object.assign({},G2[gt.id]||G2.single,{body:gt.body[1],bodyD:gt.body[0],board:FB_WOOD[gt.wood]||'#2A160C'});
  const G=h2guitar(gt.id,C,a0,pal), s2=(x,y)=>[C.x+(x-C.x)*sc,C.y+(y-C.y)*sc], S=v=>{ const r=s2(v.x,v.y); return {x:r[0],y:r[1]}; };
  const GL=xfLayers(G.L,s2,0), nut=S(G.nut), joint=S(G.joint), pick=S(G.pick);
  // arms: fretting hand on the real spot of the neck, picking hand on the strings
  const S1=P2(9,-70), S2=P2(-9,-70), perp={x:-Math.sin(a0),y:Math.cos(a0)}, u=Math.max(0,Math.min(1,q.fret==null?0.3:q.fret)), tt=0.14+0.7*u;
  const fh={x:nut.x+(joint.x-nut.x)*tt+perp.x*1.6,y:nut.y+(joint.y-nut.y)*tt+perp.y*1.6}, st=(q.strum||0)*5.6, ph={x:pick.x+perp.x*st-1,y:pick.y+perp.y*st};
  const A=h2ik(S1,fh,15.5,16,1), B=h2ik(S2,ph,13,13.5,1), o=R.arm||{}, w=o.wide?8:6.4, sl=P.sleeve||P.top, sd=P.sleeveD||P.topD, fa=o.bare?P.skin:sl, fad=o.bare?P.skinD:sd;
  const cuffAt=(E,Bp)=>({x:E.x+(Bp.x-E.x)*0.8,y:E.y+(Bp.y-E.y)*0.8});
  const back=[{s:h2path([S1,A.E]),w,c:sl},{s:h2path([A.E,A.B]),w:5.4,c:fa}]; if(o.cuff) back.push({s:h2path([cuffAt(A.E,A.B),A.B]),w:5.8,c:o.cuff});
  const front=[{s:h2path([S2,B.E]),w,c:sd},{s:h2path([B.E,B.B]),w:5.4,c:fad}]; if(o.cuff) front.push({s:h2path([cuffAt(B.E,B.B),B.B]),w:5.8,c:o.cuff});
  front.push({e:[B.B.x,B.B.y,3.6,2.9,0.3],c:P.skin},{e:[A.B.x-perp.x*2.6,A.B.y-perp.y*2.6,2.8,2.2,a0],c:P.skin});
  return [...L,{s:h2path([P2(-9.5,-72),joint]),w:2.4,c:'#2A1A10'},...back,...GL,...front];
}
const rcache2=new Map(), RQ={lean:0.4,nod:0.5,fret:0.1,strum:0.5,slump:0.5,gloat:0.5};
function rivalFrame2(id,q){ const R=RIVAL_VEC[id], qq={blink:q.blink}; Object.keys(RQ).forEach(k=>{ if(q[k]) qq[k]=Math.round(q[k]/RQ[k])*RQ[k]; });
  const key=id+'|'+Object.keys(RQ).map(k=>Math.round((qq[k]||0)*8)).join(',')+'|'+(qq.blink?1:0);
  let c=rcache2.get(key); if(c){ rcache2.delete(key); rcache2.set(key,c); return c; }
  const raw=rasterLayers(rivalRigLayers(id,qq),R.s,R.W,R.H,R.ox,R.oy); c=document.createElement('canvas'); c.width=R.W; c.height=R.H;
  const g=c.getContext('2d'); g.translate(R.W,0); g.scale(-1,1); g.drawImage(raw,0,0); rcache2.set(key,c); if(rcache2.size>500) rcache2.delete(rcache2.keys().next().value); return c; }
// the driver: the caller's own notes, the beat, and how your answers land
const RA={u:0.3,ut:0.3,sdir:1,noteAt:-9,last:0,moodAt:-9,mood:0};
function rivalNote(f){ RA.ut=Math.max(0,Math.min(1,Math.pow(Math.max(0,f||0)/15,0.85))); RA.sdir=-RA.sdir; RA.noteAt=perfNow(); }
function rivalMood(m){ RA.mood=m; RA.moodAt=perfNow(); }
function rivalPose(t,st){ const dt=Math.min(0.1,Math.max(0,t-(RA.last||t))); RA.last=t; RA.u+=(RA.ut-RA.u)*Math.min(1,dt*16);
  const q={fret:RA.u,blink:!!st.blink}, sn=t-RA.noteAt, md=t-RA.moodAt, ph=state.phase;
  if(sn>=0&&sn<0.22) q.strum=sn<0.09?RA.sdir*(-1+2*sn/0.09):RA.sdir*(1-(sn-0.09)/0.13);
  if(tr.on&&ctx&&state.screen==='duel'){ const b=(ctx.currentTime-tr.t0)/BEAT, fr=b-Math.floor(b); if(b>=0) q.nod=Math.exp(-fr*5)*0.5; }
  if(ph==='listen') q.lean=0.8;
  if(md>=0&&md<1.6){ if(RA.mood>0) q.gloat=1; else q.slump=1; }
  if(ph==='review'&&state.over==='lose'){ q.gloat=1; q.nod=0; } if(ph==='review'&&state.over==='win'){ q.slump=1; q.nod=0; }
  return q; }
function rivalWarm(id){ if(!RIVAL_VEC[id]) return; const list=[]; for(let f=0;f<=10;f++) for(const s of [0,-1,1,-0.5,0.5]) for(const n of [0,0.5]) list.push({fret:f/10,strum:s,nod:n});
  let i=0; const step=()=>{ for(let k=0;k<3&&i<list.length;k++,i++){ const q={}; Object.keys(list[i]).forEach(key=>{ if(list[i][key]) q[key]=list[i][key]; }); rivalFrame2(id,q); } if(i<list.length) setTimeout(step,0); }; setTimeout(step,0); }
