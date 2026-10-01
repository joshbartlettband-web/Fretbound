/* ---------- the band on stage ----------
   Seated band members stand behind their player; a caller's backing band stands behind the caller, mirrored.
   Musicians use the player rig (h2 skeleton, faces, outline pipeline) with their own instruments and play on the beat. */
Object.assign(G2,{bass:{body:'#D8841C',bodyD:'#4A1E08',guard:'#1A0C08',neck:'#E8C890',board:'#5A3420',head:'#E8C890',kind:'bari'},
  dneck:{body:'#C0182A',bodyD:'#6A0A14',guard:'#1A0808',neck:'#5A3420',board:'#1A0C08',head:'#1A0808',kind:'lp'}});
const BANDP={
  lou:{inst:'drums',skin:'#E8B88A',skinD:'#C0906A',eye:'#2A1206',brow:'#9A9AA0',lip:'#9A6A50',top:'#7A5230',topD:'#5A3A20',sleeve:'#7A5230',sleeveB:'#6A4628',pants:'#2E2A2A',pantsD:'#1E1A1A',boots:'#2A1A10',hair:'#B8B8BE',cap:'#5A4632'},
  rosa:{inst:'drums',skin:'#F2C49A',skinD:'#D09470',eye:'#2A1206',brow:'#A83A1A',lip:'#B85A48',top:'#16141A',topD:'#0C0A10',sleeve:'#F2C49A',sleeveB:'#E8B890',pants:'#2A2A36',pantsD:'#1A1A24',boots:'#1A1A1A',hair:'#C8401C',band:'#16141A'},
  dee:{guitar:'bass',skin:'#5A3018',skinD:'#3E200E',eye:'#140804',brow:'#140804',lip:'#3A1A10',top:'#2E7A4A',topD:'#1E5A34',sleeve:'#2E7A4A',sleeveB:'#26683E',pants:'#22222A',pantsD:'#16161C',boots:'#1A1210',strap:'#3A2010'},
  jo:{inst:'keys',skin:'#E8C0A0',skinD:'#C89A7A',eye:'#2A1206',brow:'#8A8A92',lip:'#A85A5A',top:'#7A1A2E',topD:'#56101E',sleeve:'#7A1A2E',sleeveB:'#6A1626',pants:'#2A1A20',pantsD:'#1C1016',boots:'#1A1010',hair:'#D8D8E0'},
  hale:{inst:'mic',skin:'#7A4A2C',skinD:'#5A3018',eye:'#140804',brow:'#140C0A',lip:'#8A2A30',robe:'#E0B040',robeD:'#A87C20',sleeve:'#7A4A2C',sleeveB:'#6A3E24',robeLen:40,hair:'#1A100C'},
  tam:{guitar:'dneck',skin:'#E8C8A0',skinD:'#C8A07A',eye:'#1A0A06',brow:'#140C0A',lip:'#A06A58',top:'#3A2418',topD:'#24160E',sleeve:'#E8E0D0',sleeveB:'#D8D0C0',pants:'#1E1E2A',pantsD:'#12121A',boots:'#1A1410',strap:'#1A1010',hair:'#141018'},
  brass:{inst:'horn',skin:'#C8906A',skinD:'#A06A48',eye:'#1A0A04',brow:'#2A1810',lip:'#8A4A38',top:'#C89A2A',topD:'#9A7218',sleeve:'#C89A2A',sleeveB:'#B08820',pants:'#B08820',pantsD:'#8A6A14',boots:'#3A2410',hat:'#5A3A1E'}
};
const BANDX={
  lou:{head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-6.6,-2],[-6,-6.6],[0,-8],[5.6,-7],[6.6,-4.4],[4,-5],[-2,-4.6],[-5,-1]],P.hair),h2poly(h,a,[[-7.4,-5.6],[-6.2,-9.4],[1,-10.4],[7.4,-8.8],[10.4,-6.2],[7,-5.6],[0,-6.6]],P.cap),
      h2poly(h,a,[[0.6,2.4],[6.6,2.4],[6.2,6.2],[3,8.4],[0,6.4]],P.hair)]; },
    torso:(K,P)=>[...h2torso(K,P),h2poly(K.hip,K.a,[[1,-22],[5,-22],[5,0],[1,0]],'#F0ECE0')]},
  rosa:{head:(K,P)=>{ const h=K.head,a=K.ha; return [h2ell(h,a,-3,-2,7.6,7.4,P.hair),h2ell(h,a,-7,3,3.6,4.4,P.hair),h2ell(h,a,2,-7.4,4,2.6,P.hair),h2line(h,a,[[-6.6,-4.4],[1,-7.6],[6.6,-5]],1.8,P.band)]; },
    torso:(K,P)=>[...h2torso(K,P),h2ell(K.hip,K.a,2,-14,3.2,2.2,'#F4F0E8')]},
  dee:{head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[0.6,2.6],[6.4,2.2],[6,6],[3,7.4],[0,5.8]],'#140804'),h2ell(h,a,3.4,-0.8,1.9,1.6,'#0A0A0E'),h2ell(h,a,-0.4,-0.8,1.6,1.4,'#0A0A0E'),h2line(h,a,[[1.2,-0.8],[1.8,-0.8]],0.8,'#0A0A0E')]; },
    torso:(K,P)=>[...h2torso(K,P),h2line(K.hip,K.a,[[-2,-23],[-2,1]],1.6,'#F0E4C0'),h2line(K.hip,K.a,[[5,-23],[5,1]],1.6,'#F0E4C0')]},
  jo:{head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-7.4,5],[-7.6,-3],[-5,-7.6],[1,-8.6],[6,-7],[7.2,-3.6],[4,-4.6],[-1,-4],[-3,1],[-3.4,6]],P.hair),h2line(h,a,[[1.6,-1],[5.4,-1.2]],1.1,'#1A1A20'),{p:[h2rot(h,a,-5.6,3.4).x,h2rot(h,a,-5.6,3.4).y,1.2,1.2],c:'#F4F4F0'}]; }},
  hale:{head:(K,P)=>{ const h=K.head,a=K.ha; return [h2ell(h,a,-2,-6,9.4,8.4,P.hair),h2ell(h,a,-5.6,1,5,6,P.hair),h2ell(h,a,4.4,-11,2.4,2.2,'#E84A6A'),h2ell(h,a,4.4,-11,0.9,0.9,'#FFD040')]; },
    torso:(K,P)=>[h2poly(K.hip,K.a,[[-8,-24],[8,-24],[9,-12],[-9,-12]],P.robe),{p:[h2rot(K.hip,K.a,-4,-18).x,h2rot(K.hip,K.a,-4,-18).y,1,1],c:'#FFF4C0'},{p:[h2rot(K.hip,K.a,3,-10).x,h2rot(K.hip,K.a,3,-10).y,1,1],c:'#FFF4C0'}]},
  tam:{back:(K,P)=>[h2ell(K.C,K.na,-2,-7.4,9,7.4,'#6A0A14'),h2ell(K.C,K.na,-2,-7.2,7.8,6.4,'#C0182A'),h2poly(K.C,K.na,[[6,-10.6],[35,-10.4],[35,-7.4],[6,-7.6]],'#5A3420'),h2poly(K.C,K.na,[[7,-10],[35,-9.8],[35,-8],[7,-8.2]],'#1A0C08'),h2poly(K.C,K.na,[[35,-11],[42,-12],[43,-9],[42,-6.6],[35,-7]],'#1A0808')],
    head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-7.4,6],[-7.4,-3],[-5,-7.6],[1,-8.6],[6,-7],[7,-4],[3.6,-4.8],[-1,-4],[-3.6,2],[-4.2,7.6]],P.hair),h2line(h,a,[[-5,-5],[-6.4,6]],1.2,'#3A8AF0')]; },
    torso:(K,P)=>[h2poly(K.hip,K.a,[[-7,2],[7,2],[9,-10],[9,-23],[-8,-24],[-8,-10]],'#E8E0D0'),...[-20,-15,-10,-5].map(y=>h2line(K.hip,K.a,[[-7.6,y],[8.6,y]],1.2,'#3A3A4A')),h2poly(K.hip,K.a,[[-8,-24],[-2,-24],[-2,2],[-7,2],[-8,-10]],P.top),h2poly(K.hip,K.a,[[4,-24],[9,-23],[9,-10],[7,2],[4,2]],P.top)]},
  brass:{head:(K,P)=>{ const h=K.head,a=K.ha; return [h2poly(h,a,[[-8.6,-4.4],[-6.4,-10],[0,-11.4],[6,-10],[8.4,-4.8],[12,-4],[4,-3],[-4,-2.6],[-11,-3.2]],P.hat),h2line(h,a,[[-6.6,-5.4],[7.6,-5.8]],1.3,'#2A1A0E')]; },
    torso:(K,P)=>[...h2torso(K,P),h2poly(K.hip,K.a,[[0,-23],[5,-23],[3,-18],[1,-18]],'#F0ECE0'),h2poly(K.hip,K.a,[[0.4,-22],[2.4,-20.4],[4.6,-22],[4.6,-19],[2.4,-20.4],[0.4,-19]],'#5A3A1E')]}
};
// instruments that are not guitars, and the arms that play them
function bandInst(id,K,P,q){ const L=[], hit=q.hit||0, A=[], sk=P.skin;
  const arm=(S,T,sl,up)=>{ const r=h2ik(S,T,13,13,up?-1:1); L.push({s:h2path([S,r.E,r.B]),w:5.4,c:sl},{e:[r.B.x,r.B.y,2.6,2.4,0],c:sk}); return r.B; };
  if(P.inst==='drums'){ // a small kit in front of a seated drummer
    L.push({s:'M -14 -2 L -14 -44',w:1.2,c:'#8A8A96'},{e:[-14,-44,6.4,1.5,0],c:'#E0B040'},{e:[-14,-45.6,6,1.3,0],c:'#F0C850'},{s:'M 19 -2 L 19 -56',w:1.2,c:'#8A8A96'},{e:[19,-56.6,8,1.8,-0.2],c:'#E8C050'});
    L.push({e:[16,-24,6.4,5.2,0],c:'#9A1A2A'},{e:[16,-28.4,6.2,1.6,0],c:'#E8E4DC'});
    const hd=h2ik(K.S2,{x:-12,y:-47+hit*4},12.5,12.5,1), sn=h2ik(K.S1,{x:hit?-2:10,y:hit?-36:-50},13,13,1);
    L.push({s:h2path([K.S2,hd.E,hd.B]),w:5.4,c:P.sleeveB||P.sleeve},{s:h2path([hd.B,{x:hd.B.x-6,y:hd.B.y-2+hit*5}]),w:1.1,c:'#E8D4A8'},{e:[hd.B.x,hd.B.y,2.6,2.4,0],c:sk});
    L.push({e:[-2,-33,7,2.4,0],c:'#D8D4CC'},{e:[-2,-31.6,7,1.8,0],c:'#8A8A96'});
    L.push({s:h2path([K.S1,sn.E,sn.B]),w:5.4,c:P.sleeve},{s:h2path([sn.B,{x:sn.B.x+(hit?-4:6),y:sn.B.y+(hit?3:-4)}]),w:1.1,c:'#E8D4A8'},{e:[sn.B.x,sn.B.y,2.6,2.4,0],c:sk});
    L.push({e:[6,-14,13,13,0],c:'#2A1A3A'},{e:[6,-14,11.2,11.2,0],c:'#E8E4DC'},{e:[6,-14,4,4,0],c:'#C8203A'},{s:'M -4 -1 L 16 -1',w:1.4,c:'#5A5A66'}); }
  if(P.inst==='keys'){ L.push({s:'M -10 0 L 12 -36 M 12 0 L -10 -36',w:1.6,c:'#3A3A44'});
    arm(K.S1,{x:10+hit*2,y:-41},P.sleeve,0); arm(K.S2,{x:-2-hit*2,y:-41},P.sleeveB||P.sleeve,0);
    L.push({d:'M -13 -40 L 16 -40 L 16 -35 L -13 -35 Z',c:'#B01C2A'},{d:'M -12 -41.6 L 15 -41.6 L 15 -39.6 L -12 -39.6 Z',c:'#F4F0E8'});
    for(let k=-10;k<14;k+=3) L.push({p:[k,-41.6,1,1],c:'#1A1A1A'}); }
  if(P.inst==='mic'){ L.push({s:'M 13 -1 L 13 -72',w:1.4,c:'#8A8A96'},{s:'M 8 -1 L 13 -8 L 18 -1',w:1.4,c:'#6A6A74'},{s:'M 13 -72 L 9.6 -80',w:1.2,c:'#8A8A96'},{e:[9.4,-81.6,1.8,2.4,0.4],c:'#D8D8E0'});
    arm(K.S1,{x:9,y:-79},P.sleeve,0); arm(K.S2,hit?{x:-12,y:-92}:{x:-10,y:-60},P.sleeveB||P.sleeve,hit); }
  if(P.inst==='horn'){ const h=K.head, up=(q.raise||0)*0.4, M=h2rot(h,K.ha,6.6,3), dir={x:Math.cos(-0.1-up),y:Math.sin(-0.1-up)}, B={x:M.x+dir.x*17,y:M.y+dir.y*17};
    arm(K.S1,{x:M.x+dir.x*11,y:M.y+dir.y*11+2},P.sleeve,0); arm(K.S2,{x:M.x+dir.x*6,y:M.y+dir.y*6+2.6},P.sleeveB||P.sleeve,0);
    L.push({s:h2path([M,B]),w:1.6,c:'#E8B830'},{s:h2path([{x:M.x+dir.x*5,y:M.y+dir.y*5+2.4},{x:M.x+dir.x*12,y:M.y+dir.y*12+2.4}]),w:1.4,c:'#C89A20'},{e:[B.x,B.y,1.6,3.4,-0.1-up],c:'#F0C840'}); }
  return L; }
function bandLayers(id,q){ const P=BANDP[id], X=BANDX[id]||{};
  if(P.inst==='drums') q=Object.assign({},q,{crouch:1});
  const K=h2skel(q), g=P.inst?null:h2guitar(P.guitar,K.C,K.na), L=[];
  if(X.back) L.push(...X.back(K,P,q));
  if(!P.robe) L.push(...h2legs(K,P)); else L.push(...h2robe(K,P,P.robeLen||-2));
  L.push(...(X.torso?X.torso(K,P,q):h2torso(K,P)));
  L.push(...h2head(K,P)); if(X.head) L.push(...X.head(K,P,q));
  if(g){ if(P.strap) L.push({s:h2path([h2rot(K.hip,K.a,-7,-22),g.joint]),w:1.6,c:P.strap}); const AR=h2arms(K,g,q,P); L.push(...AR.behind,...g.L,...AR.L); }
  else L.push(...bandInst(id,K,P,q));
  L.push(...h2face(K,P,q)); return L; }
const bcache=new Map(), BS={W:160,H:140,ox:66,oy:133,s:0.92};
function bandFrame(id,q,mirror){ const key=id+'|'+(mirror?1:0)+'|'+['nod','hit','strum','fret','raise'].map(k=>Math.round((q[k]||0)*4)).join(',')+(q.blink?'b':'');
  let c=bcache.get(key); if(c) return c;
  const raw=rasterLayers(bandLayers(id,q),BS.s,BS.W,BS.H,BS.ox,BS.oy);
  if(mirror){ c=document.createElement('canvas'); c.width=BS.W; c.height=BS.H; const g=c.getContext('2d'); g.translate(BS.W,0); g.scale(-1,1); g.drawImage(raw,0,0); } else c=raw;
  bcache.set(key,c); if(bcache.size>300) bcache.delete(bcache.keys().next().value); return c; }
const BAND_SLOTS=[[62,190],[252,191],[22,195],[292,196]];
function bandPose(id,t,i){ const q={nod:0,hit:0,fret:0.3+0.1*(i%3)}; if(tr.on&&ctx&&state.screen==='duel'){ const b=(ctx.currentTime-tr.t0)/BEAT, fr=b-Math.floor(b), e2=(b*2)-Math.floor(b*2);
    if(b>=0){ q.nod=fr<0.25?0.5:0; const P=BANDP[id]; if(P.inst==='drums') q.hit=e2<0.35?1:0; else if(P.inst==='mic') q.hit=(Math.floor(b)%4===0&&fr<0.6)?1:0; else if(P.inst==='keys') q.hit=Math.floor(b*2)%2; else if(P.inst==='horn') q.raise=(t<anim.cheerUntil)?1:0; else if(fr<0.2) q.strum=Math.floor(b)%2?1:-1; } }
  return q; }
function drawBandSide(g,t,ids,mirror){ ids=ids.filter(id=>BANDP[id]); const order=ids.slice().sort((a,b)=>(BANDP[b].inst==='drums')-(BANDP[a].inst==='drums'));
  order.slice(0,4).forEach((id,i)=>{ const s=BAND_SLOTS[i], x=mirror?640-s[0]:s[0], y=s[1]; g.drawImage(bandFrame(id,bandPose(id,t,i),mirror),Math.round(x-(mirror?BS.W-BS.ox:BS.ox)),Math.round(y-BS.oy)); }); }
function drawBandStage(g,t){ try{ drawBandSide(g,t,state.lineup||[],false); drawBandSide(g,t,state.rivalBand||[],true); }catch(e){} }
