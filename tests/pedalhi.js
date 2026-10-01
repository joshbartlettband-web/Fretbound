function pedalMini(p,on){
  const key=p.id+(on?'1':'0'); if(miniCache[key]) return cloneCv(miniCache[key]);
  // drawn at twice the old 42x60 grid: finer finish, bevels, screws, knob scales, an inset label window
  const S=2, A=PEDAL_ART[p.id], W=42*S, H=60*S, c=document.createElement('canvas'); c.width=W; c.height=H; c.className='pm'; const g=c.getContext('2d');
  const body=p.color, b3=rgbOf(body), lt2=mixHex(body,0.5), dk2=mixHex(body,-0.55), seed=p.id.charCodeAt(0)*13+p.id.length, O='#0A0404';
  const lum=(b3[0]*0.3+b3[1]*0.59+b3[2]*0.11)/255, tick=lum>0.55?mixHex(body,-0.6):mixHex(body,0.6);
  [[0,28],[W-4,28]].forEach(q=>{ px(g,q[0],q[1],'#1E1E22',4,18); px(g,q[0],q[1]+2,'#A8A8B4',4,14); px(g,q[0],q[1]+2,'#E8E8F0',4,2); px(g,q[0],q[1]+13,'#6A6A76',4,2); });
  const R=7, ins=(x,y,m)=>{ const x0=5+m,x1=W-6-m,y0=m,y1=H-1-m; if(x<x0||x>x1||y<y0||y>y1) return false; const cx=x<x0+R?x0+R:x>x1-R?x1-R:x, cy=y<y0+R?y0+R:y>y1-R?y1-R:y; return (x-cx)*(x-cx)+(y-cy)*(y-cy)<=R*R+2; };
  const img=g.getImageData(0,0,W,H), d=img.data, cols=[rgbOf(mixHex(body,0.24)),b3,rgbOf(mixHex(body,-0.24))];
  for(let y=0;y<H;y++) for(let x=0;x<W;x++){ if(!ins(x,y,0)) continue; const i=(y*W+x)*4; let col;
    if(!ins(x,y,2)) col=[10,4,4];
    else { const t=y/H, th=B8[y&7][x&7]/64, base=t<0.5?(t*2>th?cols[1]:cols[0]):((t-0.5)*2>th?cols[2]:cols[1]);
      col=finishPixel(A,base,x>>1,y>>1,seed).slice(); const n=(h2(x*3+seed,y*5+seed)-0.5)*9; col=col.map(v=>Math.max(0,Math.min(255,v+n)));
      if(!ins(x,y,4)){ const top=y<H*0.5&&(y<8||x<14), f=top?1.22:0.74; col=col.map(v=>Math.max(0,Math.min(255,v*f))); } }
    d[i]=col[0]; d[i+1]=col[1]; d[i+2]=col[2]; d[i+3]=255; }
  g.putImageData(img,0,0);
  [[13,9],[W-14,9],[13,H-10],[W-14,H-10]].forEach(q=>{ disc(g,q[0]+1,q[1]+1,3,'rgba(0,0,0,.4)'); disc(g,q[0],q[1],3,'#16161A'); disc(g,q[0],q[1],2,'#C8C8D2'); px(g,q[0]-2,q[1],'#56565E',4,1); px(g,q[0]-1,q[1]-2,'#F4F4F8'); });
  const K=KNOB[A.knob], lay={1:[[20,9,5]],2:[[13,9,4],[28,9,4]],3:[[10,9,3],[20,9,3],[31,9,3]],4:[[9,8,2],[16,8,2],[25,8,2],[32,8,2]]}[A.knobs];
  lay.forEach((q,k)=>{ const cx=q[0]*S+1, cy=q[1]*S+2, r=q[2]*S+(q[2]<3?1:0);
    for(let s=0;s<7;s++){ const an=(-225+s*45)*Math.PI/180, rr=r+4; px(g,Math.round(cx+Math.cos(an)*rr),Math.round(cy+Math.sin(an)*rr),tick); }
    drawKnob(g,cx,cy,r,K,-2.4+h2(k,seed)*3.3); });
  drawLED(g,41,37,2,on); px(g,40,36,'rgba(255,255,255,.55)');
  const L0=A.label; px(g,8,44,O,68,40); px(g,10,46,L0,64,36);
  const ec=document.createElement('canvas'); ec.width=31; ec.height=18; EMBLEM[p.id](ec.getContext('2d')); g.imageSmoothingEnabled=false; g.drawImage(ec,10,46,62,36);
  px(g,10,46,'rgba(0,0,0,.28)',64,2); px(g,10,46,'rgba(0,0,0,.2)',2,36); px(g,10,80,'rgba(255,255,255,.18)',64,2); px(g,12,48,'rgba(255,255,255,.22)',22,1);
  px(g,7,43,mixHex(body,-0.4),70,1); px(g,7,85,mixHex(body,0.35),70,1);
  for(let x=18;x<64;x+=2) if(h2(x>>1,seed+3)>0.3) px(g,x,89,dk2,2,1);
  drawSwitch(g,41,103,10); disc(g,41,103,13,'rgba(0,0,0,0)');
  miniCache[key]=c; return cloneCv(c);
}
