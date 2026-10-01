/* ---------- the guitar on its stand, in a bay at the left of the pedalboard ----------
   Vector-first shapes (body, guard, pickups, neck, head, stand) through the shared outline rasterizer,
   then pixel-exact details: frets at real spacing, inlays, strings, tuners, poles, knobs. 40x92, headstock up. */
const GS={W:36,H:92,ox:18,oy:90};
const gsCache={};
function gsE(kind){ return kind==='strat'||kind==='lp'||kind==='bari'; }
function guitarStand(id){
  if(gsCache[id]) return gsCache[id];
  const G=G2[id]||G2.single, k=G.kind, gt=GUITAR_BY[id]||{}, L=[], el=gsE(k);
  const yN=k==='bari'?-82:-78, yJ=el?-44:-49, yB=el?-15:-14, nwJ=k==='classical'?3.6:3.2, nwN=k==='classical'?3.2:2.6;
  const poly=(pts,c)=>L.push({d:'M '+pts.map(p=>p[0]+' '+p[1]).join(' L ')+' Z',c}), ell=(x,y,rx,ry,c)=>L.push({e:[x,y,rx,ry,0],c}), line=(pts,w,c)=>L.push({s:'M '+pts.map(p=>p[0]+' '+p[1]).join(' L '),w,c});
  // the stand behind the guitar
  line([[-2,-58],[-14,0]],1.6,'#34343C'); line([[2,-58],[14,0]],1.6,'#44444C'); line([[-13,-6],[13,-6]],1.8,'#2A2A30'); line([[-13,-6],[-14,-9]],1.6,'#2A2A30'); line([[13,-6],[14,-9]],1.6,'#2A2A30');
  // body
  const SH={
    strat:[[-13,-5],[-16,-11],[-16,-19],[-13,-25],[-14,-31],[-12,-40],[-9,-45],[-6,-41],[-3,-38],[3,-38],[5,-42],[8,-47],[11,-46],[12,-40],[11,-33],[14,-27],[16,-18],[15,-9],[11,-4],[4,-2],[-5,-2]],
    lp:[[-14,-5],[-16,-12],[-16,-21],[-13,-27],[-14,-33],[-12,-40],[-8,-44],[-3,-45],[3,-45],[5,-41],[8,-38],[10,-42],[13,-40],[15,-33],[16,-22],[16,-12],[13,-5],[5,-2],[-5,-2]],
    bari:[[-13,-4],[-16,-12],[-15,-22],[-12,-28],[-15,-36],[-14,-43],[-10,-46],[-6,-41],[-3,-39],[3,-39],[6,-43],[8,-48],[11,-46],[12,-39],[14,-30],[16,-20],[14,-9],[9,-3],[1,-1],[-7,-2]]};
  if(SH[k]){ const cx=0, cy=-24, sc=(f)=>SH[k].map(p=>[cx+(p[0]-cx)*f,cy+(p[1]-cy)*f]);
    if(k==='lp') poly(sc(1.06),'#F0E0B8'); poly(SH[k],G.bodyD); poly(sc(0.86),G.body); }
  else { const big=k==='dread'?1.12:1, lo=[0,-17,15*big,12.5*big], up=[0,-39,12*big,9*big];
    ell(lo[0],lo[1],lo[2],lo[3],G.bodyD); ell(up[0],up[1],up[2],up[3],G.bodyD); poly([[-11*big,-32],[11*big,-32],[10*big,-24],[-10*big,-24]],G.bodyD);
    ell(0,-17.5,lo[2]-1.6,lo[3]-1.6,G.body); ell(0,-39,up[2]-1.6,up[3]-1.6,G.body); poly([[-9.5*big,-33],[9.5*big,-33],[8.6*big,-23],[-8.6*big,-23]],G.body); }
  // pickguards, pickups, plates
  if(k==='strat'){ poly([[-10,-10],[-12,-18],[-10,-26],[-8,-33],[-4,-37],[3,-37],[5,-33],[6,-24],[10,-18],[9,-12],[3,-8],[-6,-7]],G.guard); [-33,-27].forEach(y=>poly([[-4.5,y-1.1],[4.5,y-1.1],[4.5,y+1.1],[-4.5,y+1.1]],'#F4ECDC')); poly([[-4.5,-21.8],[4.5,-20.2],[4.5,-18.2],[-4.5,-19.8]],'#F4ECDC'); poly([[-5,-15],[5,-15],[5,-12.6],[-5,-12.6]],'#C8C8D2'); }
  if(k==='lp'){ poly([[5,-41],[9,-37],[10,-30],[6,-28]],G.guard); [-34,-24].forEach(y=>poly([[-5,y-1.7],[5,y-1.7],[5,y+1.7],[-5,y+1.7]],'#F0E0B8')); poly([[-5.5,-19.8],[5.5,-19.8],[5.5,-18.4],[-5.5,-18.4]],'#C8C8D2'); poly([[-6,-14.6],[6,-14.6],[6,-12.8],[-6,-12.8]],'#B0B0BC'); }
  if(k==='bari'){ poly([[-9,-9],[-12,-20],[-9,-30],[-5,-38],[4,-38],[7,-30],[11,-20],[8,-10],[0,-7]],G.guard); [-31,-22].forEach(y=>poly([[-4.5,y-1.6],[4.5,y-1.6],[4.5,y+1.6],[-4.5,y+1.6]],'#1A1A1E')); poly([[-5,-15.6],[5,-15.6],[5,-13.6],[-5,-13.6]],'#C8C8D2'); poly([[-4,-9],[4,-9],[3,-6],[-3,-6]],'#B0B0BC'); }
  if(k==='classical'||k==='dread'){ const r=k==='dread'?5.4:5, cy=k==='dread'?-37:-36;
    ell(0,cy,r+2.4,r+2.4,'#3A1E10'); ell(0,cy,r+1.6,r+1.6,'#E8D8B0'); ell(0,cy,r+0.8,r+0.8,'#2A6A5A'); ell(0,cy,r,r,'#140604');
    if(k==='dread') poly([[4,-31],[10,-32],[12,-26],[9,-21],[5,-24]],G.guard);
    poly([[-7,-15.5],[7,-15.5],[7,-12],[-7,-12]],k==='dread'?'#1E0E08':'#4A2412'); }
  if(k==='reso'){ ell(0,-19,10.5,10.5,'#7A7A86'); ell(0,-19,9.6,9.6,G.guard); ell(0,-19,3,3,'#9A9AA6'); poly([[-1,-24],[1,-24],[1,-14],[-1,-14]],'#6A4020');
    [[-6,-38],[6,-38]].forEach(q=>{ ell(q[0],q[1],3.2,2.2,'#4A4A56'); ell(q[0],q[1],2.4,1.5,'#26262E'); }); poly([[-3,-7],[3,-7],[2,-3.5],[-2,-3.5]],'#B0B0BC'); }
  // neck and headstock
  poly([[-nwJ,yJ+1],[nwJ,yJ+1],[nwN+0.6,yN],[-nwN-0.6,yN]],G.neck); poly([[-nwJ+0.6,yJ+1],[nwJ-0.6,yJ+1],[nwN,yN],[-nwN,yN]],G.board);
  if(k==='strat') poly([[-2.8,yN],[-3.6,yN-5],[-2.6,yN-11],[1,yN-12],[4,yN-10],[5,yN-7],[3,yN-4],[2.8,yN]],G.head);
  else if(k==='lp'||k==='bari') poly([[-2.8,yN],[-4.4,yN-6],[-4,yN-10],[0,yN-11.5],[4,yN-10],[4.4,yN-6],[2.8,yN]],G.head);
  else poly([[-3.2,yN],[-4,yN-11],[4,yN-11],[3.2,yN]],G.head);
  // cable from the jack along the floor toward the board
  const jack=k==='strat'?[11,-8]:k==='lp'?[15,-9]:k==='bari'?[12,-8]:[0,-2];
  L.push({s:'M '+jack[0]+' '+jack[1]+' Q '+(jack[0]+3)+' -1 12 -1 L 18 -1',w:1.4,c:'#141010'});
  // the stand's neck yoke in front
  line([[-4.6,yJ-17],[-4.6,yJ-13],[4.6,yJ-13],[4.6,yJ-17]],1.3,'#34343C');
  const c=rasterLayers(L,1,GS.W,GS.H,GS.ox,GS.oy), g=c.getContext('2d'), P=(x,y,col,w,h)=>R(g,Math.round(GS.ox+x),Math.round(GS.oy+y),w||1,h||1,col);
  // frets at real spacing between nut and bridge, inlays between them
  const fy=n=>yN+(yB-yN)*(1-Math.pow(2,-n/12)), wAt=y=>nwN+(nwJ-nwN)*(y-yN)/(yJ-yN), dot=gt.wood==='maple'?'#1E1410':'#F2EADA';
  for(let n=1;n<24;n++){ const y=fy(n); if(y>yJ+0.5) break; const hw=Math.round(wAt(y)-0.6); P(-hw,y,'#D8D4C8',hw*2,1);
    if([3,5,7,9,15,17].includes(n)){ P(0,(y+fy(n-1))/2-0.5,dot); } if(n===12){ const m=(y+fy(11))/2-0.5; P(-1.6,m,dot); P(1.4,m,dot); } }
  P(-nwN,yN,'#F2EADA',Math.round(nwN*2),1);   // the nut
  // strings: faint over the board so the frets read, clear over the body
  const str=k==='classical'?['#E8E0CC','#E8E0CC','#E8E0CC','#C8C8D2','#C8C8D2','#C8C8D2']:el?['#E8E8F0','#E8E8F0','#E8E8F0','#C8C0A8','#C8C0A8','#C8C0A8']:['#E8E8F0','#E8E8F0','#D8B868','#D8B868','#D8B868','#D8B868'];
  for(let s2=0;s2<6;s2++){ const xn=-nwN+0.5+s2*(2*nwN-1)/5, xb=-4+s2*1.6;
    for(let y=Math.ceil(yN)+1;y<=yB;y++){ const u=(y-yN)/(yB-yN), x=xn+(xb-xn)*u; if(k==='classical'||k==='dread'){ const cy=k==='dread'?-37:-36, rr=k==='dread'?5.4:5; if(Math.abs(y-cy)<rr&&false) continue; }
      g.globalAlpha=y<yJ+1?0.42:(s2%2?0.5:0.8); P(x,y,str[5-s2]); } }
  g.globalAlpha=1;
  // headstock hardware
  const tn='#E8E8F0';
  if(k==='strat') for(let q=0;q<6;q++) P(-4.4,yN-3-q*1.4,tn);
  else if(k==='lp'||k==='bari') for(let q=0;q<3;q++){ P(-5.4,yN-3-q*2.6,'#F0E0B8',1,2); P(4.6,yN-3-q*2.6,'#F0E0B8',1,2); }
  else if(k==='dread') for(let q=0;q<6;q++){ P(-5,yN-2-q*1.5,tn); P(4.4,yN-2-q*1.5,tn); }
  else { P(-1.4,yN-9,'#1A0C08',1,7); P(1,yN-9,'#1A0C08',1,7); for(let q=0;q<3;q++){ P(-5,yN-3-q*2.6,'#F0E0B8',1,2); P(4.4,yN-3-q*2.6,'#F0E0B8',1,2); } }
  // pickup poles, knobs and bridge details
  if(k==='strat'){ [-33,-27].forEach(y=>{ for(let q=0;q<6;q++) P(-3.6+q*1.45,y,'#8A8A92'); }); [[6,-16],[8.4,-12.4],[9.8,-8.8]].forEach(q=>P(q[0],q[1],'#F4ECDC',2,2)); P(11,-8,'#1A1A1E',2,1); for(let q=0;q<6;q++) P(-4.4+q*1.6,-14,'#FFFFFF'); }
  if(k==='lp'){ [-34,-24].forEach(y=>{ for(let q=0;q<6;q++){ P(-3.6+q*1.45,y-1,'#8A7A58'); P(-3.6+q*1.45,y+0.4,'#8A7A58'); } }); [[7,-17],[11,-19],[8,-12],[12,-14]].forEach(q=>P(q[0],q[1],'#E0C070',2,2)); P(-11,-38,'#F0E0B8',1,2); }
  if(k==='bari'){ [[8,-15],[10,-12]].forEach(q=>P(q[0],q[1],'#D8D8E0',2,2)); for(let q=0;q<6;q++) P(-4+q*1.6,-15,'#FFFFFF'); }
  if(k==='classical'){ P(-6,-15,'#F2EADA',12,1); } if(k==='dread'){ for(let q=0;q<12;q++) P(-5.6+q*1,-13,'#F2EADA'); P(-6,-15,'#F2EADA',12,1); }
  if(k==='reso'){ for(let a=0;a<18;a++){ const an=a/18*Math.PI*2; P(Math.cos(an)*7,-19+Math.sin(an)*7,'#6A6A76'); } P(-2,-19.5,'#2A160C',4,1); }
  // a soft floor shadow
  g.fillStyle='rgba(0,0,0,.35)'; g.fillRect(GS.ox-15,GS.oy,30,1); g.fillRect(GS.ox-11,GS.oy+1,22,1);
  return gsCache[id]=c;
}
