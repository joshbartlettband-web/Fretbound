/* ---------- stage players v2: rigged, drawn from the Gemini portraits ----------
   A small skeleton in model units (feet at y=0, up is negative). The upper body leans about the hips,
   the head nods about the neck, and both arms are two-bone IK chains: the fretting hand is placed on the
   real spot of the neck for the fret being played, the picking hand on the strings. Frames are rasterized
   with the same vector-first, pixel-snapped, outlined pipeline as the rest of the art and cached by a
   quantized pose key. */
const H2={W:150,H:140,ox:58,oy:133,s:1.05};
const h2cache=new Map();
function h2rot(o,a,x,y){ const c=Math.cos(a), s=Math.sin(a); return {x:o.x+x*c-y*s, y:o.y+x*s+y*c}; }
function h2ik(A,B,l1,l2,bendSign){ // elbow for shoulder A, hand B
  const dx=B.x-A.x, dy=B.y-A.y; let d=Math.hypot(dx,dy); const dm=Math.min(d,l1+l2-0.01); const k=dm/(d||1); B={x:A.x+dx*k,y:A.y+dy*k}; d=dm;
  const a=(l1*l1-l2*l2+d*d)/(2*d), h=Math.sqrt(Math.max(0,l1*l1-a*a)), mx=A.x+dx*a/Math.hypot(dx,dy), my=A.y+dy*a/Math.hypot(dx,dy);
  const nx=-dy/Math.hypot(dx,dy), ny=dx/Math.hypot(dx,dy); return {E:{x:mx+nx*h*bendSign,y:my+ny*h*bendSign},B};
}
const f2=v=>Math.round(v*100)/100;
function h2path(pts,close){ return pts.map((p,i)=>(i?'L ':'M ')+f2(p.x)+' '+f2(p.y)).join(' ')+(close?' Z':''); }
function h2curve(a,c,b){ return 'M '+f2(a.x)+' '+f2(a.y)+' Q '+f2(c.x)+' '+f2(c.y)+' '+f2(b.x)+' '+f2(b.y); }
function h2poly(o,a,pts,col){ return {d:h2path(pts.map(p=>h2rot(o,a,p[0],p[1])),true),c:col}; }
function h2ell(o,a,x,y,rx,ry,col,rot){ const q=h2rot(o,a,x,y); return {e:[q.x,q.y,rx,ry,a+(rot||0)],c:col}; }
function h2line(o,a,pts,w,col){ return {s:h2path(pts.map(p=>h2rot(o,a,p[0],p[1]))),w,c:col}; }

/* guitars, drawn about the body centre; neck angle na. Returns layers plus the nut and the string centre. */
const G2={
  single:{body:'#7FD6B4',bodyD:'#4FA888',guard:'#F4ECDC',neck:'#E8C890',board:'#5A3420',head:'#E8C890',kind:'strat'},
  humbucker:{body:'#E0B040',bodyD:'#A87818',guard:'#F0E0B8',neck:'#5A3420',board:'#2A160C',head:'#1A0C08',kind:'lp'},
  nylon:{body:'#E8A040',bodyD:'#B86A1C',guard:null,neck:'#8A5A30',board:'#2A160C',head:'#6A3A1A',kind:'classical'},
  resonator:{body:'#C8C8D2',bodyD:'#8A8A96',guard:'#E8E8F0',neck:'#6A4020',board:'#1A0C08',head:'#6A4020',kind:'reso'},
  twelve:{body:'#F08A28',bodyD:'#A84A14',guard:'#3A1A0C',neck:'#8A5A30',board:'#2A160C',head:'#3A1A0C',kind:'dread'},
  baritone:{body:'#6A1E3A',bodyD:'#3A0C1E',guard:'#1A0C12',neck:'#5A3420',board:'#1A0C08',head:'#1A0C12',kind:'bari'}
};
function h2guitar(gid,C,na){
  const G=G2[gid]||G2.single, L=[], k=G.kind, big=k==='dread'||k==='reso'?1.12:k==='classical'?1.04:1;
  const neckLen=k==='bari'?31:k==='classical'?26:28, o=C;
  // a dark rim first, so the body reads against the clothes
  const rim=(pts)=>{ const cx=pts.reduce((a,p)=>a+p[0],0)/pts.length, cy=pts.reduce((a,p)=>a+p[1],0)/pts.length; return h2poly(o,na,pts.map(p=>[cx+(p[0]-cx)*1.13,cy+(p[1]-cy)*1.16]),G.bodyD); };
  const SH={strat:[[-11,-6],[-4,-9],[4,-7],[9,-10],[12,-6],[9,-1],[11,5],[4,9],[-6,9],[-12,4]],lp:[[-11,-5],[-5,-9],[3,-8],[8,-6],[11,-1],[10,5],[4,9],[-6,9],[-12,4]],bari:[[-11,-6],[-3,-9],[5,-8],[10,-11],[12,-6],[9,-1],[11,5],[4,9],[-6,9],[-12,4]]};
  if(SH[k]) L.push(rim(SH[k])); else { L.push(h2ell(o,na,-4*big,0,9.2*big,10.8*big,'#2A1206')); L.push(h2ell(o,na,5*big,0,7.6*big,8.7*big,'#2A1206')); }
  // body
  if(k==='strat'){ L.push(h2poly(o,na,[[-11,-6],[-4,-9],[4,-7],[9,-10],[12,-6],[9,-1],[11,5],[4,9],[-6,9],[-12,4]],G.body)); L.push(h2poly(o,na,[[-7,-4],[2,-5],[6,-2],[4,4],[-5,5]],G.guard)); }
  else if(k==='lp'){ L.push(h2poly(o,na,[[-11,-5],[-5,-9],[3,-8],[8,-6],[11,-1],[10,5],[4,9],[-6,9],[-12,4]],G.body)); L.push(h2poly(o,na,[[2,-1],[7,2],[5,6],[1,4]],G.guard)); }
  else if(k==='bari'){ L.push(h2poly(o,na,[[-11,-6],[-3,-9],[5,-8],[10,-11],[12,-6],[9,-1],[11,5],[4,9],[-6,9],[-12,4]],G.body)); }
  else { L.push(h2ell(o,na,-4*big,0,8*big,9.5*big,G.body)); L.push(h2ell(o,na,5*big,0,6.5*big,7.5*big,G.body)); }
  if(k==='reso'){ L.push(h2ell(o,na,-2,0,5.5,5.5,G.guard)); L.push(h2ell(o,na,-2,0,2,2,G.bodyD)); }
  if(k==='classical'||k==='dread'){ L.push(h2ell(o,na,4.5*big,0,2.6,2.6,'#1A0804')); }
  if(k==='dread') L.push(h2poly(o,na,[[6,3],[10,3],[10,6],[6,6]],G.guard));
  // shading on the lower bout
  L.push(h2poly(o,na,[[-12*big,2],[-4,8*big],[6,8.5*big],[10*big,5],[4,7*big],[-6,6.5*big]],G.bodyD));
  // neck, board, headstock
  const nw=k==='classical'?2.2:1.8;
  L.push(h2poly(o,na,[[6,-nw],[6+neckLen,-nw+0.3],[6+neckLen,nw-0.3],[6,nw]],G.neck));
  L.push(h2poly(o,na,[[7,-nw+0.7],[6+neckLen,-nw+0.8],[6+neckLen,nw-0.8],[7,nw-0.7]],G.board));
  const hx=6+neckLen;
  if(k==='strat') L.push(h2poly(o,na,[[hx,-2],[hx+8,-3.5],[hx+10,-2],[hx+9,1],[hx,2]],G.head));
  else if(k==='classical') L.push(h2poly(o,na,[[hx,-2.4],[hx+8,-2.6],[hx+8,2.6],[hx,2.4]],G.head));
  else L.push(h2poly(o,na,[[hx,-2.2],[hx+7,-3.2],[hx+8,0],[hx+7,3.2],[hx,2.2]],G.head));
  // strings as one bright line and the bridge
  L.push(h2poly(o,na,[[-8,-2.2],[-6,-2.2],[-6,2.2],[-8,2.2]],k==='strat'||k==='lp'||k==='bari'?'#B0B0BC':'#2A160C'));
  return {L,nut:h2rot(o,na,hx,0),joint:h2rot(o,na,6,0),pick:h2rot(o,na,k==='strat'||k==='lp'||k==='bari'?-1:2,0),neckLen};
}

/* the skeleton. q: lean, bob, nod, fret (0 nut .. 1 body joint), strum (-1..1), raise, crouch, recoil, slump, blink, mouth */
function h2skel(q){
  const crouch=q.crouch||0, hip={x:0,y:-40+crouch*6+(q.bob||0)};
  const a=((q.lean||0)*4-(q.recoil||0)*9+(q.slump||0)*7)*Math.PI/180;
  const C=h2rot(hip,a,3,-8), na=-0.4-(q.raise||0)*0.6+(q.slump||0)*0.25+a*0.4;
  const neckPt=h2rot(hip,a,1,-26), ha=a+((q.nod||0)*10+(q.slump||0)*14-(q.recoil||0)*6)*Math.PI/180, head=h2rot(neckPt,ha,1.6,-6.6);
  return {hip,a,C,na,neckPt,ha,head,S1:h2rot(hip,a,7,-23),S2:h2rot(hip,a,-5,-23)};
}
function h2arms(K,g,q,P){
  const perp={x:-Math.sin(K.na),y:Math.cos(K.na)}, u=Math.max(0,Math.min(1,q.fret==null?0.3:q.fret)), t=0.14+0.7*u;
  const fh={x:g.nut.x+(g.joint.x-g.nut.x)*t+perp.x*1.2, y:g.nut.y+(g.joint.y-g.nut.y)*t+perp.y*1.2};
  const st=(q.strum||0)*4.6, ph={x:g.pick.x+perp.x*st-1, y:g.pick.y+perp.y*st};
  const A=h2ik(K.S1,fh,15,14.5,1), B=h2ik(K.S2,ph,12.5,12.5,1), L=[], behind=[];
  L.push({s:h2path([K.S2,B.E,B.B]),w:5.4,c:P.sleeveB||P.sleeve}); if(P.cuffB) L.push({s:h2path([{x:B.E.x+(B.B.x-B.E.x)*0.6,y:B.E.y+(B.B.y-B.E.y)*0.6},B.B]),w:5.6,c:P.cuffB});
  L.push({e:[B.B.x,B.B.y,2.7,2.5,0],c:P.skin});
  behind.push({s:h2path([K.S1,A.E,A.B]),w:5.4,c:P.sleeve}); if(P.cuff) behind.push({s:h2path([{x:A.E.x+(A.B.x-A.E.x)*0.6,y:A.E.y+(A.B.y-A.E.y)*0.6},A.B]),w:5.6,c:P.cuff});
  const fg={x:A.B.x-perp.x*2.2,y:A.B.y-perp.y*2.2}; L.push({e:[fg.x,fg.y,2.2,1.8,K.na],c:P.skin});   // fingers over the fretboard
  return {L,behind};
}
function h2legs(K,P){
  const L=[], feet=[{x:-5,y:-1},{x:7,y:-1}];
  [[-3.5,0],[3.5,1]].forEach((hp,i)=>{ const H={x:K.hip.x+hp[0],y:K.hip.y}, R=h2ik(H,feet[i],20.5,20.5,-1);
    L.push({s:h2path([H,R.E,R.B]),w:7.6,c:i?P.pants:P.pantsD});
    L.push({d:h2path([{x:feet[i].x-4,y:0},{x:feet[i].x-4,y:-4},{x:feet[i].x+2,y:-5},{x:feet[i].x+6,y:-2},{x:feet[i].x+6,y:0}],true),c:i?P.boots:P.bootsD||P.boots}); });
  return L;
}
function h2robe(K,P,len){ // a robe from the shoulders to near the ground, swaying with the lean
  const o=K.hip, a=K.a*0.6;
  return [h2poly(o,a,[[-9,-24],[9,-24],[12,-6],[14,len],[-13,len],[-11,-6]],P.robe),h2poly(o,a,[[-13,len],[-11,-6],[-6,-10],[-6,len]],P.robeD)];
}
function h2torso(K,P){ return [h2poly(K.hip,K.a,[[-7,2],[7,2],[9,-10],[9,-23],[-8,-24],[-8,-10]],P.top),h2poly(K.hip,K.a,[[-7,2],[-2,2],[-3,-12],[-8,-12]],P.topD)]; }
function h2head(K,P){ const h=K.head, a=K.ha; return [{s:h2path([K.neckPt,h2rot(K.neckPt,K.a,1,-3)]),w:4.2,c:P.skinD||P.skin},h2ell(h,a,0,0,6.4,7.2,P.skin),h2ell(h,a,-5.6,0.5,1.6,2.2,P.skinD||P.skin)]; }
function h2face(K,P,q){ // pixel-exact features, placed in the head's frame
  const h=K.head, a=K.ha, L=[], E=h2rot(h,a,3.2,-0.6), px=(pt,w,hh,c)=>L.push({p:[pt.x,pt.y,w,hh],c});
  if(q.blink||P.calm) px(E,1.8,0.7,P.eye||'#2A1206'); else px(E,1.2,2.2,P.eye||'#2A1206');
  if(P.brow) px(h2rot(h,a,2.6,-3.4),2.6,0.8,P.brow);
  const M=h2rot(h,a,3.6,3.6); px(M,q.mouth?1.4:2,q.mouth?1.6:0.8,q.mouth?'#5A1810':(P.lip||'#8A4A30'));
  return L;
}
function h2frame(cid,q){
  const P=H2P[cid], K=h2skel(q), g=h2guitar(P.guitar,K.C,K.na), X=H2X[cid]||{};
  const L=[];
  if(X.back) L.push(...X.back(K,P,q));
  if(!P.robe||P.legs) L.push(...h2legs(K,P));
  if(P.robe) L.push(...h2robe(K,P,P.robeLen||-2));
  L.push(...(X.torso?X.torso(K,P,q):h2torso(K,P)));
  if(X.mid) L.push(...X.mid(K,P,q));
  L.push(...h2head(K,P)); if(X.head) L.push(...X.head(K,P,q));
  if(P.strap) L.push({s:h2path([h2rot(K.hip,K.a,-7,-22),g.joint]),w:1.6,c:P.strap});
  const AR=h2arms(K,g,q,P);
  L.push(...AR.behind);
  L.push(...g.L);
  L.push(...AR.L);
  if(X.front) L.push(...X.front(K,P,q));
  L.push(...h2face(K,P,q)); if(X.face) L.push(...X.face(K,P,q));
  return L;
}
function heroFrame2(cid,q){
  const key=cid+'|'+['lean','bob','nod','fret','strum','raise','crouch','recoil','slump'].map(k=>Math.round((q[k]||0)*8)).join(',')+'|'+(q.blink?1:0)+(q.mouth?1:0);
  let c=h2cache.get(key); if(c){ h2cache.delete(key); h2cache.set(key,c); return c; }
  c=rasterLayers(h2frame(cid,q),H2.s,H2.W,H2.H,H2.ox,H2.oy); h2cache.set(key,c);
  if(h2cache.size>400) h2cache.delete(h2cache.keys().next().value);
  return c;
}

/* the six players, drawn from their Gemini portraits */
const H2P={
  bard:{guitar:'single',skin:'#F2C49A',skinD:'#D09470',eye:'#2A1206',brow:'#B8481C',lip:'#B86A50',top:'#3A8A3A',topD:'#1E5A28',sleeve:'#3A8A3A',sleeveB:'#2E7A30',pants:'#6A4428',pantsD:'#4A2E18',boots:'#3A2010',bootsD:'#2A160A',strap:'#8A4A20',hair:'#E0662A',hairD:'#A8401C',hat:'#B8301C',hatD:'#7A1A10',feather:'#F4ECD8',cape:'#2E4EA8',capeD:'#1C2E70'},
  monk:{guitar:'humbucker',skin:'#C8804A',skinD:'#9A5A30',eye:'#3A1A0A',lip:'#7A3A20',robe:'#F0A020',robeD:'#C06A10',drape:'#8A1E24',drapeD:'#5A1016',sleeve:'#F0A020',sleeveB:'#C8804A',calm:true,strap:'#1E4A2A',beads:'#7A4A20',robeLen:38},
  hermit:{guitar:'nylon',skin:'#C0845A',skinD:'#946038',eye:'#1A0A04',brow:'#F4F4F4',lip:'#7A4A30',robe:'#6A4A30',robeD:'#4A3020',robeL:'#8A6A48',sleeve:'#6A4A30',sleeveB:'#5A3C24',beard:'#F4F4F2',beardD:'#C0C0C0',robeLen:39},
  busker:{guitar:'resonator',skin:'#7A4A2C',skinD:'#5A3018',eye:'#140804',brow:'#140C0A',lip:'#5A2A1A',top:'#6A8AB8',topD:'#48689A',sleeve:'#6A8AB8',sleeveB:'#5A7AA8',pants:'#2A3048',pantsD:'#1E2238',boots:'#E8E8E8',bootsD:'#C0C0C0',hair:'#1A100C',cap:'#6E7684',capD:'#4A5260',scarf:'#D02828',scarfD:'#901818',strap:'#3A2010'},
  luthier:{guitar:'twelve',skin:'#F2C49A',skinD:'#D09470',eye:'#2A1206',brow:'#8A3A18',lip:'#C06A58',top:'#F0E4C8',topD:'#C8B898',sleeve:'#F0E4C8',sleeveB:'#E0D4B4',cuff:'#F2C49A',cuffB:'#E8B890',pants:'#6A4428',pantsD:'#4A2E18',boots:'#3A2010',hair:'#C0501E',hairD:'#80300E',apron:'#9A5A2A',apronD:'#6A3A18',goggle:'#C8963A',lens:'#8ABACA',strap:'#5A3018'},
  carto:{guitar:'baritone',skin:'#C8906A',skinD:'#A06A48',eye:'#1A0A04',brow:'#2A1810',lip:'#8A4A38',top:'#1E6E6E',topD:'#10484A',sleeve:'#1E6E6E',sleeveB:'#185C5C',cuff:'#10484A',cuffB:'#0C3A3C',pants:'#3A2A20',pantsD:'#2A1C14',boots:'#1E140C',hair:'#2A1810',hat:'#3A2418',trim:'#D8A848',vest:'#7A4424',cravat:'#F0E8D8',glass:'#E8E0C0',strap:'#2A1810'}
};
const H2X={
  bard:{
    back:(K,P)=>[h2poly(K.hip,K.a,[[-8,-25],[3,-25],[-2,-14],[-10,6],[-16,18],[-20,12],[-16,-8]],P.cape),h2poly(K.hip,K.a,[[-12,-6],[-8,-2],[-14,16],[-18,12]],P.capeD)],
    torso:(K,P)=>[h2poly(K.hip,K.a,[[-8,7],[8,7],[9,-10],[9,-23],[-8,-24],[-8,-10]],P.top),h2poly(K.hip,K.a,[[-8,7],[-3,7],[-3,-12],[-8,-12]],P.topD),h2line(K.hip,K.a,[[-8,1],[8,1]],1.6,'#5A3018'),
      h2poly(K.hip,K.a,[[1,-25],[9,-24],[10,-18],[4,-19]],P.cape)],
    head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-7.5,-2],[-6.5,-7],[-1,-9],[4,-8.5],[7,-5.5],[6.5,-3.5],[2.5,-4.5],[-0.5,-2],[-3,1.5],[-5,6],[-8,5]],P.hair),h2poly(h,a,[[-8,4],[-5,6],[-7,9],[-9,7]],P.hairD),
      h2poly(h,a,[[-8.5,-5],[-6.5,-10],[0,-12.5],[6.5,-11.5],[9.5,-8],[8.5,-6.5],[1,-6.5],[-5,-4.5]],P.hat),h2line(h,a,[[-7.5,-5.2],[8,-6.8]],1.4,P.hatD),h2line(h,a,[[-4,-10],[-10,-14],[-16,-13]],1.9,P.feather)]; }
  },
  monk:{
    torso:(K,P)=>[h2poly(K.hip,K.a,[[3,-25],[9,-24],[9,-12],[-6,6],[-10,2],[-9,-4]],P.drape),h2poly(K.hip,K.a,[[-9,-4],[-6,6],[-10,2]],P.drapeD),h2poly(K.hip,K.a,[[-9,-24],[-4,-25],[-2,-18],[-9,-12]],P.skin)],
    mid:(K,P)=>[{e:[-6,-1,2.6,1.4,0],c:P.skinD},{e:[8,-1,2.8,1.4,0],c:P.skin}],
    front:(K,P)=>[h2line(K.hip,K.a,[[-3,-25],[-1,-20],[3,-17],[7,-21]],1.3,P.beads)]
  },
  hermit:{
    back:(K,P)=>[],
    torso:(K,P)=>[h2poly(K.hip,K.a*0.6,[[-13,37],[-10,39],[-7,36],[-3,39],[1,36],[5,39],[9,36],[12,39],[14,36],[13,33],[-12,33]],P.robeD),h2line(K.hip,K.a,[[-8,-2],[8,-1]],1.6,'#3A2414')],
    mid:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-8.5,-6],[-4,-10.5],[3,-10.5],[7.5,-6],[8.5,-1],[6,2],[9,9],[-7,10],[-10,4]],P.robe)]; },
    head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-3,-9.5],[4,-9.5],[8,-5],[7.2,-2.8],[3,-6.8],[-3,-6]],P.robe),h2poly(h,a,[[1,0.5],[7,0.8],[7.5,5],[5.5,10],[3,15],[0,17],[-2,12],[-1,5]],P.beard),h2poly(h,a,[[0,9],[3,11],[1,15],[-1,12]],P.beardD)]; },
    front:(K,P)=>{ const l=h2rot(K.hip,K.a,-11,-1); return [{p:[l.x-1.5,l.y-5,3,1.2],c:'#2A1A0A'},{p:[l.x-2,l.y-4,4,4.8],c:'#2A1A0A'},{p:[l.x-1.2,l.y-3.4,2.4,3.6],c:'#FFD070'}]; }
  },
  busker:{
    back:(K,P)=>[h2poly({x:0,y:0},0,[[-30,0],[-31,-3.5],[-15,-3.5],[-14,0]],'#4A1010'),h2poly({x:0,y:0},0,[[-29,-1],[-29.5,-3],[-16,-3],[-15.5,-1]],'#A82828'),{p:[-26,-3.2,1.4,1.2],c:'#FFD060'},{p:[-22,-2.6,1.4,1.2],c:'#FFD060'},{p:[-19,-3.2,1.4,1.2],c:'#E8E8F0'}],
    torso:(K,P)=>[...h2torso(K,P),h2poly(K.hip,K.a,[[1,-22],[5,-22],[5,1],[1,1]],'#F0F0F0'),{p:[h2rot(K.hip,K.a,-6,-16).x,h2rot(K.hip,K.a,-6,-16).y,2,1.8],c:'#E0A020'},{p:[h2rot(K.hip,K.a,6,-8).x,h2rot(K.hip,K.a,6,-8).y,2,1.8],c:'#C82828'}],
    mid:(K,P)=>{ const h=K.head,a=K.ha; return [h2ell(h,a,-3.5,2,8.2,9.2,P.hair),h2ell(h,a,-7,8,4,4,P.hair)]; },
    head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-7,-2],[-6,-6],[0,-7.5],[5,-6.5],[6.5,-4.5],[3,-4],[-1,-3],[-4,0]],P.hair),
      h2poly(h,a,[[-8.5,-4.5],[-7.5,-9.5],[-1,-11.5],[5.5,-10.5],[8.5,-7.5],[10.5,-5],[7,-4.8],[1,-5.2],[-5,-3.6]],P.cap),h2poly(h,a,[[5,-6.2],[11,-5.2],[10,-4],[5,-4.6]],P.capD),
      h2poly(K.hip,K.a,[[-4,-27],[6,-27],[7,-22.5],[3,-19],[4,-12],[1,-12],[0,-20],[-4,-22.5]],P.scarf),h2poly(K.hip,K.a,[[1,-19],[4,-12],[1,-12]],P.scarfD)]; },
    face:(K,P)=>{ const e=h2rot(K.head,K.ha,-2.2,2.4); return [{p:[e.x,e.y,1.2,1.2],c:'#FFD060'}]; }
  },
  luthier:{
    torso:(K,P)=>[...h2torso(K,P),h2poly(K.hip,K.a,[[-2,-18],[7,-18],[8.5,4],[8,9],[-5,9],[-5,0]],P.apron),h2poly(K.hip,K.a,[[-5,0],[-2,0],[-2,9],[-5,9]],P.apronD),h2line(K.hip,K.a,[[-1,-18],[-4,-24]],1.2,P.apronD),h2line(K.hip,K.a,[[6,-18],[7,-24]],1.2,P.apronD)],
    head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-7.5,-1],[-6.5,-7],[-1,-9.2],[4,-8.6],[6.8,-5.5],[3,-5.2],[-1,-3.6],[-4,-0.5],[-6,4],[-8,3]],P.hair),
      h2line(h,a,[[-7,-3],[-1,-8.6],[6,-6.4]],1.5,'#3A2A20'),h2ell(h,a,1.2,-8.6,2.2,1.7,P.goggle),h2ell(h,a,1.2,-8.6,1.2,0.9,P.lens),h2ell(h,a,4.8,-7.4,2,1.6,P.goggle),h2ell(h,a,4.8,-7.4,1.1,0.8,P.lens),
      {s:h2path([h2rot(h,a,-4,4),h2rot(K.hip,K.a,6,-22),h2rot(K.hip,K.a,6,-11)]),w:2.8,c:P.hair},{s:h2path([h2rot(K.hip,K.a,6.4,-19),h2rot(K.hip,K.a,5.8,-12)]),w:1,c:P.hairD}]; },
    face:(K,P)=>{ const f=h2rot(K.head,K.ha,4.4,1.6); return [{p:[f.x,f.y,1.1,1.1],c:'#D08058'}]; }
  },
  carto:{
    back:(K,P)=>[h2poly(K.hip,K.a,[[-8,-6],[-1,-4],[-3,14],[-13,16],[-12,4]],P.topD)],
    torso:(K,P)=>{ const o=K.hip,a=K.a, L=[...h2torso(K,P),h2poly(o,a,[[1,-22],[5,-22],[6,1],[1,2]],P.vest),h2poly(o,a,[[0,-26],[5.5,-26],[4.5,-19],[1,-19]],P.cravat)];
      [-18,-12,-6].forEach(y=>{ const b=h2rot(o,a,6.4,y); L.push({p:[b.x,b.y,1.3,1.3],c:P.trim}); }); L.push(h2poly(o,a,[[-13,-17],[-3,-21],[-2,-18],[-12,-14]],'#F0E4C8'),h2ell(o,a,-13,-15.5,1.4,1.8,'#D8C8A0')); return L; },
    mid:(K,P)=>{ const h=K.head,a=K.ha; return [h2line(h,a,[[-5,2],[-9.5,5]],2.2,P.hair)]; },
    head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-7,-1],[-6.5,-6],[-1,-8],[5,-7],[6.5,-5],[2,-4.5],[-3,-3],[-5,2]],P.hair),
      h2poly(h,a,[[-11,-5],[-6.5,-10.5],[0,-13.5],[6.5,-11.5],[10.5,-7.5],[11.5,-4.5],[6,-6],[0,-7],[-6,-4.5]],P.hat),h2line(h,a,[[-11,-5],[-6,-4.6],[0,-6.8],[6,-5.8],[11.5,-4.5]],1.1,P.trim),
      h2ell(h,a,3.4,-0.4,2.1,2.1,P.glass),h2ell(h,a,3.4,-0.4,1.3,1.3,P.skin)]; }
  }
};

/* the animation driver: gameplay moves the rig */
const HA={u:0.3,ut:0.3,sdir:1,noteAt:-9,flinchAt:-9,last:0};
function heroNote(f){ HA.ut=Math.max(0,Math.min(1,Math.pow(Math.max(0,f)/15,0.85))); HA.sdir=-HA.sdir; HA.noteAt=perfNow(); }
function heroFlinch(){ HA.flinchAt=perfNow(); }
function heroPose(t,st){
  const dt=Math.min(0.1,Math.max(0,t-(HA.last||t))); HA.last=t; HA.u+=(HA.ut-HA.u)*Math.min(1,dt*16);
  const q={fret:HA.u,blink:!!st.blink}, sn=t-HA.noteAt, fl=t-HA.flinchAt, ph=state.phase;
  if(sn>=0&&sn<0.22) q.strum=sn<0.09?HA.sdir*(-1+2*sn/0.09):HA.sdir*(1-(sn-0.09)/0.13);
  if(sn>=0&&sn<0.25) q.crouch=0.4*(1-sn/0.25);
  if(tr.on&&ctx&&state.screen==='duel'){ const b=(ctx.currentTime-tr.t0)/BEAT, fr=b-Math.floor(b); if(b>=0) q.nod=Math.exp(-fr*5)*((state.streak||0)>=3?1:0.5); }
  if(ph==='listen') q.lean=0.8;
  if(t<anim.cheerUntil||(ph==='review'&&state.over==='win')){ q.raise=1; q.crouch=Math.max(q.crouch||0,0.5); q.mouth=1; }
  if(ph==='review'&&state.over==='lose'){ q.slump=1; q.nod=0; }
  if(fl>=0&&fl<0.7){ q.recoil=1-fl/0.7; q.blink=true; q.mouth=1; }
  return q;
}
const H2Q={lean:0.4,nod:0.5,fret:0.1,strum:0.5,raise:0.5,crouch:0.25,recoil:0.34,slump:0.5};
function drawHero(g,cid,x,y,st){
  const t=st.t||0, q=heroPose(t,st), qq={blink:q.blink,mouth:q.mouth};
  Object.keys(H2Q).forEach(k=>{ if(q[k]) qq[k]=Math.round(q[k]/H2Q[k])*H2Q[k]; });
  const bob=Math.round(Math.sin(t*1.7)*0.7), fr=heroFrame2(cid,qq), s=H2.s;
  g.drawImage(fr,x-H2.ox,y-H2.oy+bob);
  const K=h2skel(qq), at=(mx,my)=>({x:Math.round(x+mx*s),y:Math.round(y+my*s)+bob});
  if(cid==='hermit'){ const l0=h2rot(K.hip,K.a,-11,-1), l=at(l0.x,l0.y), f=0.5+0.5*Math.sin(t*9)*Math.sin(t*3.3);
    for(let yy=-12;yy<=12;yy++) for(let xx=-12;xx<=12;xx++){ const d=Math.sqrt(xx*xx+yy*yy); if(d>3&&d<12&&B8[(l.y+yy)&7][(l.x+xx)&7]/64<(1-d/12)*(0.35+0.25*f)) R(g,l.x+xx,l.y+yy,1,1,'rgba(255,200,110,.5)'); } }
  if(cid==='monk'){ const m0=h2rot(K.hip,K.a,-10,3), m=at(m0.x,m0.y), an=Math.sin(t*Math.PI*BPM/60)*0.5;
    R(g,m.x-3,m.y-1,7,1,'#2A1206'); R(g,m.x-2,m.y-5,5,4,'#6A3A18'); R(g,m.x-1,m.y-8,3,3,'#8A5028'); R(g,m.x-3,m.y,7,1,'#2A1206');
    for(let r=1;r<=6;r++) R(g,m.x+Math.round(Math.sin(an)*r),m.y-2-r,1,1,'#E0C070'); R(g,m.x+Math.round(Math.sin(an)*6)-1,m.y-9,2,2,'#FFC857'); }
}
