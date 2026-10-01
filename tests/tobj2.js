// more roadside company, all dark silhouettes with a rim of light on the lit side
function tln(g,x0,y0,x1,y1,w,c){ const n=Math.max(1,Math.round(Math.max(Math.abs(x1-x0),Math.abs(y1-y0)))); for(let k=0;k<=n;k++) R(g,Math.round(x0+(x1-x0)*k/n),Math.round(y0+(y1-y0)*k/n),w,w,c); }
function tR(g,x,y,w,h,c){ R(g,Math.round(x),Math.round(y),Math.max(1,Math.round(w)),Math.max(1,Math.round(h)),c); }
function tP(g,pts,c){ pfill(g,pts.map(p=>[Math.round(p[0]),Math.round(p[1])]),c); }
function drawTitleObj2(g,o,K,x,y,s,lit,sil,rim,mid,near){
  const k=o.kind, sd=o.seed, w1=Math.max(1,Math.round(0.025*s));
  if(k==='windmill'){ const h=1.5*s, bw=0.17*s, tw=0.035*s, top=y-h;
    tln(g,x-bw,y,x-tw,top,1,sil); tln(g,x+bw,y,x+tw,top,1,sil); if(near) tln(g,x+lit*bw,y,x+lit*tw,top,1,rim);
    for(let q=1;q<=5;q++){ const f0=(q-1)/5, f1=q/5; tln(g,x-bw+(bw-tw)*f0,y-h*f0,x+bw-(bw-tw)*f1,y-h*f1,1,sil); tln(g,x+bw-(bw-tw)*f0,y-h*f0,x-bw+(bw-tw)*f1,y-h*f1,1,sil); }
    tR(g,x-tw*3,top,tw*6,w1,sil); const cy=top-0.05*s, r=0.3*s, sp=TT*0.9*(sd%2?1:-1);
    for(let b=0;b<14;b++){ const an=b/14*Math.PI*2+sp; tln(g,x+Math.cos(an)*r*0.25,cy+Math.sin(an)*r*0.25,x+Math.cos(an)*r,cy+Math.sin(an)*r,1,sil); }
    const tv=(sd%3?1:-1); tln(g,x,cy,x+tv*0.42*s,cy,1,sil); tR(g,tv>0?x+0.36*s:x-0.5*s,cy-0.06*s,0.14*s,0.12*s,sil); return; }
  if(k==='tower'){ const lt=y-1.0*s;
    [-0.2,-0.08,0.08,0.2].forEach(dx=>tln(g,x+dx*s,y,x+dx*0.8*s,lt,w1,sil)); tln(g,x-0.2*s,y-0.1*s,x+0.16*s,lt+0.1*s,1,sil); tln(g,x+0.2*s,y-0.1*s,x-0.16*s,lt+0.1*s,1,sil);
    tR(g,x-0.3*s,lt,0.6*s,w1,sil); tR(g,x-0.26*s,y-1.45*s,0.52*s,0.45*s,sil); tP(g,[[x-0.29*s,y-1.44*s],[x,y-1.66*s],[x+0.29*s,y-1.44*s]],sil);
    tR(g,lit>0?x+0.25*s:x-0.26*s,y-1.45*s,1,0.45*s,rim); tR(g,x-0.26*s,y-1.3*s,0.52*s,1,mid); return; }
  if(k==='pumpjack'){ const py=y-0.45*s, a=Math.sin(TT*1.3+sd)*0.28, ex=Math.cos(a)*0.45*s, ey=Math.sin(a)*0.45*s, bw2=Math.max(1,Math.round(0.035*s));
    tR(g,x-0.5*s,y-0.04*s,1.0*s,0.04*s,sil); tln(g,x-0.12*s,y,x,py,w1,sil); tln(g,x+0.12*s,y,x,py,w1,sil);
    const H={x:x-ex,y:py+ey}, T={x:x+ex,y:py-ey}; tln(g,H.x,H.y,T.x,T.y,bw2,sil);
    tP(g,[[H.x-0.09*s,H.y-0.07*s],[H.x+0.03*s,H.y-0.07*s],[H.x+0.03*s,H.y+0.1*s],[H.x-0.07*s,H.y+0.07*s]],sil); tln(g,H.x-0.06*s,H.y+0.08*s,x-0.5*s,y-0.04*s,1,sil);
    tR(g,T.x-0.05*s,T.y-0.02*s,0.12*s,0.1*s,sil); const cr={x:x+0.36*s+Math.cos(TT*2.6+sd)*0.07*s,y:y-0.16*s+Math.sin(TT*2.6+sd)*0.07*s}; tln(g,T.x,T.y,cr.x,cr.y,1,sil); tR(g,x+0.3*s,y-0.22*s,0.12*s,0.18*s,sil); return; }
  if(k==='billboard'){ const pt=0.6*s; [-0.45,0,0.45].forEach(dx=>tR(g,x+dx*s,y-pt,w1,pt,sil)); tR(g,x-0.62*s,y-pt,1.24*s,w1,sil);
    tR(g,x-0.6*s,y-pt-0.42*s,1.2*s,0.42*s,sil); tR(g,x-0.6*s,y-pt-0.42*s,1.2*s,1,rim); if(near) [-0.35,0,0.35].forEach(dx=>tln(g,x+dx*s,y-pt-0.42*s,x+dx*s,y-pt-0.5*s,1,sil)); return; }
  if(k==='diamond'){ tR(g,x,y-0.46*s,w1,0.46*s,sil); tP(g,[[x,y-0.74*s],[x+0.15*s,y-0.59*s],[x,y-0.44*s],[x-0.15*s,y-0.59*s]],sil); tln(g,x,y-0.74*s,x+lit*0.15*s,y-0.59*s,1,rim); return; }
  if(k==='mailbox'){ tR(g,x,y-0.3*s,w1,0.3*s,sil); tR(g,x-0.07*s,y-0.38*s,0.16*s,0.08*s,sil); tR(g,x-0.06*s,y-0.4*s,0.14*s,0.03*s,sil); tR(g,x+0.09*s,y-0.44*s,1,0.07*s,sil); tR(g,x+0.09*s,y-0.44*s,0.04*s,0.025*s,sil); return; }
  if(k==='fence'){ const xs=[-0.4,-0.13,0.14,0.41].map(d=>x+d*s); xs.forEach(px=>tR(g,px,y-0.3*s,w1,0.3*s,sil)); [0.12,0.22].forEach(hh=>{ for(let q=0;q<xs.length-1;q++) tln(g,xs[q],y-hh*s,xs[q+1],y-hh*s+Math.max(0,Math.round(0.01*s)),1,sil); }); return; }
  if(k==='deadtree'){ const br=(x0,y0,len,an,d)=>{ const x1=x0+Math.sin(an)*len, y1=y0-Math.cos(an)*len; tln(g,x0,y0,x1,y1,Math.max(1,Math.round(d*0.012*s)),sil);
      if(d>0){ br(x1,y1,len*0.66,an-0.35-h2(sd,d)*0.4,d-1); br(x1,y1,len*0.6,an+0.3+h2(sd,d+7)*0.45,d-1); } };
    br(x,y,(0.3+h2(sd,1)*0.15)*s,(h2(sd,2)-0.5)*0.2,3); return; }
  if(k==='ocotillo'){ const n=6+(sd%4), h=(0.5+h2(sd,1)*0.35)*s;
    for(let q=0;q<n;q++){ const an=(q/(n-1)-0.5)*0.9, wob=h2(sd,q+3)*6; let px=x, py=y;
      for(let u=1;u<=Math.max(4,Math.round(h/2));u++){ const f=u/Math.max(4,Math.round(h/2)), nx=x+(q-n/2)*0.4+Math.sin(an)*h*f+Math.sin(f*3+wob)*0.02*s, ny=y-Math.cos(an)*h*f; tln(g,px,py,nx,ny,1,sil); if(near&&u%2) R(g,Math.round(nx)+1,Math.round(ny),1,1,sil); px=nx; py=ny; } } return; }
  if(k==='hoodoo'){ const sc=0.8+h2(sd,1)*0.5;
    tP(g,[[x-0.2*s*sc,y],[x-0.16*s*sc,y-0.26*s*sc],[x+0.14*s*sc,y-0.28*s*sc],[x+0.2*s*sc,y]],sil); tP(g,[[x-0.09*s*sc,y-0.26*s*sc],[x-0.07*s*sc,y-0.56*s*sc],[x+0.08*s*sc,y-0.56*s*sc],[x+0.1*s*sc,y-0.26*s*sc]],sil);
    tP(g,[[x-0.18*s*sc,y-0.56*s*sc],[x-0.12*s*sc,y-0.66*s*sc],[x+0.16*s*sc,y-0.65*s*sc],[x+0.2*s*sc,y-0.56*s*sc]],sil); tR(g,lit>0?x+0.07*s*sc:x-0.08*s*sc,y-0.55*s*sc,1,0.28*s*sc,rim); tR(g,x-0.14*s*sc,y-0.66*s*sc,0.28*s*sc,1,rim); return; }
  if(k==='wreck'){ const f=sd%2?1:-1, P=(a,b)=>[x+a*f*s,y+b*s];
    tP(g,[P(-0.36,-0.05),P(-0.36,-0.16),P(-0.18,-0.18),P(-0.1,-0.3),P(0.13,-0.3),P(0.2,-0.18),P(0.37,-0.15),P(0.37,-0.05)],sil);
    if(near){ tP(g,[P(-0.07,-0.27),P(0.02,-0.27),P(0.02,-0.19),P(-0.12,-0.19)],mid); tP(g,[P(0.05,-0.27),P(0.12,-0.27),P(0.17,-0.19),P(0.05,-0.19)],mid); }
    disc(g,Math.round(x-0.22*f*s),Math.round(y-0.05*s),Math.max(1,Math.round(0.065*s)),sil); tR(g,x+0.18*f*s-0.04*s,y-0.06*s,0.08*s,0.06*s,sil); tR(g,x-0.36*s,y-0.17*s,0.72*s,1,rim); return; }
  if(k==='shack'){ tR(g,x-0.35*s,y-0.4*s,0.7*s,0.4*s,sil); tP(g,[[x-0.43*s,y-0.38*s],[x-0.3*s,y-0.56*s],[x+0.38*s,y-0.5*s],[x+0.43*s,y-0.38*s]],sil);
    tR(g,x-0.12*s,y-0.26*s,0.11*s,0.26*s,mid); tR(g,x+0.12*s,y-0.29*s,0.13*s,0.09*s,mid); tR(g,x+0.24*s,y-0.64*s,0.04*s,0.13*s,sil); tln(g,x-0.3*s,y-0.56*s,x+0.38*s,y-0.5*s,1,rim); return; }
  if(k==='radio'){ const h=2.6*s, bw=0.09*s, tw=0.016*s, top=y-h; tln(g,x-bw,y,x-tw,top,1,sil); tln(g,x+bw,y,x+tw,top,1,sil);
    const n=Math.max(4,Math.round(h/6)); for(let q=0;q<n;q++){ const f0=q/n, f1=(q+1)/n; tln(g,x-bw+(bw-tw)*f0,y-h*f0,x+bw-(bw-tw)*f1,y-h*f1,1,sil); }
    tR(g,x,top-0.3*s,1,0.3*s,sil); [[-0.9,0.35],[0.9,0.35],[-0.7,0.7]].forEach(([dx,hf])=>{ const x1=x+dx*s, n2=Math.round(Math.abs(dx*s)); for(let q=0;q<=n2;q+=2) R(g,Math.round(x+(x1-x)*q/n2),Math.round(y-h*hf+h*hf*q/n2),1,1,sil); }); return; }
}
