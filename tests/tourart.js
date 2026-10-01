/* ---------- world tour title scenes: each continent's sky, horizon and roadside ---------- */
const SKIES_AF=[
  {id:'sunset',stops:['#1A0A12','#3A1420','#7A2A22','#C24A1E','#E8761E','#F8A830','#FFD060'],glow:[44,24,4],sun:'striped',sunCols:['#FFF6C8','#FFE07A','#FFB040','#FF8A30'],moon:null,stars:90,
   cloud:['#4A1A18','#7A2E1E','#D8682A','#FFC060'],mesa:['#4A1C14','#3A1610','#5A2418','#E8803A','#FFE0B0'],ground:['#3A1A0E','#2A1208','#1A0A04','#5A3018'],haze:'#A04A20',
   wood:['#3A1C10','#4C2816','#5E341E','#6E4028','#1A0C06'],refl:[56,30,6],sil:'#140604',rim:'#F09040',mid:'#3A160C'},
  {id:'dusk',stops:['#0A0618','#1A0E30','#3A1A48','#6A2A50','#B04A40','#E88A40','#FFC870'],glow:[36,18,10],sun:'below',sunCols:['#FFE6A8','#FFC070','#F08048','#C0503A'],moon:'crescent',stars:380,
   cloud:['#22122E','#3A1A3E','#9A4A50','#FFB070'],mesa:['#26122A','#1E0E22','#2E1630','#E07A50','#FFD8B0'],ground:['#24120E','#1A0C0A','#100606','#42241A'],haze:'#6A2A40',
   wood:['#2E1810','#3C2014','#4A2A1A','#5A3422','#140806'],refl:[46,20,16],sil:'#0C0408',rim:'#E07A50',mid:'#2A1214'},
  {id:'night',stops:['#02020A','#05081A','#0A1028','#101A34','#182640','#22344E','#2E4058'],glow:[18,20,28],sun:'moon',sunCols:['#F8F4E0','#DCD8C8','#BCB8AC','#9C9890'],moon:null,stars:1100,
   cloud:['#0C1020','#141A2E','#34405A','#9AA6C0'],mesa:['#0C0E1A','#080A14','#10141E','#8094B8','#C8D4EC'],ground:['#14120E','#0E0C0A','#080706','#2C2820'],haze:'#202A40',
   wood:['#24160E','#2E1C12','#3A2418','#46301E','#0E0806'],refl:[26,28,36],sil:'#04050A',rim:'#8AA0C8',mid:'#141822'}];
const SKIES_EU=[
  {id:'dusk',stops:['#06081A','#0E1630','#1C2848','#2E3E60','#4A5A78','#8A8A98','#D8B8A0'],glow:[20,22,30],sun:'below',sunCols:['#FFE8C0','#F8C890','#D89070','#A86A5A'],moon:'crescent',stars:320,
   cloud:['#141A2E','#202A40','#5A6480','#D8C0B0'],mesa:['#18223A','#121A2E','#1E2A44','#8A9AC0','#D0D8EC'],ground:['#16220E','#101A0A','#0A1206','#2C3A1E'],haze:'#3A4A64',
   wood:['#2A1A10','#362216','#422A1A','#4E3420','#120A06'],refl:[30,34,44],sil:'#060A0E',rim:'#9AA8C8',mid:'#141C24'},
  {id:'storm',stops:['#0A0C12','#12161E','#1A2028','#242A34','#2E343E','#3E4448','#525850'],glow:[16,18,18],sun:'hidden',sunCols:['#E8ECE0','#C8CCC0','#A8ACA0','#888C80'],moon:null,stars:0,
   cloud:['#101318','#1A1E26','#363C46','#7A8088'],mesa:['#141A1C','#101416','#181E22','#6A7880','#A8B4B8'],ground:['#121A0E','#0E140A','#080E06','#26301E'],haze:'#2A3234',
   wood:['#24160E','#2E1C12','#3A2418','#46301E','#0E0806'],refl:[22,26,26],sil:'#05070A',rim:'#7A8A94',mid:'#12181C',rain:true},
  {id:'dawn',stops:['#2A3A5A','#3E5476','#62789A','#9AA2B4','#D8C0B0','#F2D8B8','#FFEED0'],glow:[30,28,18],sun:'pale',sunCols:['#FFFDF0','#FFF2CC','#FFDCA8','#F8C890'],moon:'faint',stars:30,
   cloud:['#7A8296','#98A0B0','#E8D0C0','#FFF0D8'],mesa:['#5A6A7A','#4C5C6C','#687888','#F8D8B8','#FFF0DA'],ground:['#3A4A2C','#2E3E22','#22301A','#5A6A42'],haze:'#B8C0C8',
   wood:['#4A2616','#5C321E','#6E3E26','#80502E','#241208'],refl:[56,50,36],sil:'#1E2A2C',rim:'#FFD8A8',mid:'#304040'}];
// horizons, painted once into the static layer
function horizonAF(g,K,W,HZ,sx){ const M=K.mesa;
  for(let x=0;x<W;x++){ const h=Math.round(3+5*vnoise(x*0.012,141)+3*vnoise(x*0.05,142)); g.fillStyle=M[0]; g.fillRect(x,HZ-h,1,h); }
  const mx=452, top=HZ-78; pfill(g,[[mx-170,HZ],[mx-70,HZ-36],[mx-30,top+10],[mx-6,top+1],[mx+4,top],[mx+30,top+8],[mx+80,HZ-34],[mx+190,HZ]],M[1]);
  pfill(g,[[mx-30,top+10],[mx-6,top+1],[mx+4,top],[mx+30,top+8],[mx+20,top+15],[mx+10,top+10],[mx+2,top+17],[mx-8,top+12],[mx-18,top+18]],M[4]);
  g.fillStyle=M[3]; for(let y=top+10;y<HZ-2;y++){ const xx=Math.round(mx-30-(y-top-10)/(HZ-top-12)*140); g.fillRect(xx,y,1,1); }
  const acacia=(x,h,w)=>{ g.fillStyle=M[2]; g.fillRect(x,HZ-h,1,h); g.fillRect(x-w,HZ-h-2,w*2+1,2); g.fillRect(x-w+2,HZ-h-3,w*2-3,1); };
  [[64,9,9],[118,7,7],[236,6,6],[300,8,8],[588,10,10],[620,6,6]].forEach(q=>acacia(...q));
  const giraffe=(x,s)=>{ g.fillStyle=M[2]; g.fillRect(x,HZ-6*s,5*s,2*s); [0,4].forEach(d=>g.fillRect(x+d*s,HZ-4*s,1,4*s)); for(let k=0;k<6*s;k++) g.fillRect(x+4*s+Math.round(k*0.4),HZ-6*s-k,1,1); g.fillRect(x+4*s+Math.round(6*s*0.4),HZ-12*s-1,2,1); };
  giraffe(170,1); giraffe(184,1); giraffe(536,1);
}
function horizonEU(g,K,W,HZ,sx){ const M=K.mesa;
  [[M[0],26,0.006,151],[M[2],16,0.011,152],[M[1],9,0.022,153]].forEach(([c,amp,f,seed])=>{ for(let x=0;x<W;x++){ const h=Math.round(amp*(0.35+0.65*vnoise(x*f,seed))); g.fillStyle=c; g.fillRect(x,HZ-h,1,h); } });
  const hillY=x=>HZ-Math.round(26*(0.35+0.65*vnoise(x*0.006,151)));
  // a castle on the far hill, its windows lit
  const cx=140, cb=hillY(cx)+2, col=M[2];
  g.fillStyle=col; g.fillRect(cx-22,cb-14,44,14); [[-24,-24,8],[18,-22,8],[-4,-30,9]].forEach(([dx,dy,w])=>{ g.fillRect(cx+dx,cb+dy,w,-dy); for(let k=0;k<w;k+=2) g.fillRect(cx+dx+k,cb+dy-2,1,2); });
  for(let k=-22;k<22;k+=3) g.fillRect(cx+k,cb-16,2,2); g.fillStyle='#FFD27A'; [[cx-20,cb-18],[cx-1,cb-24],[cx+20,cb-15],[cx+6,cb-9]].forEach(q=>g.fillRect(q[0],q[1],1,1));
  // a village with a church spire
  const vx=505, vb=hillY(vx)+3; g.fillStyle=col;
  [[-40,7,6],[-30,6,5],[-18,8,6],[8,7,5],[18,6,6],[30,8,5]].forEach(([dx,w,h])=>{ g.fillRect(vx+dx,vb-h,w,h); pfill(g,[[vx+dx-1,vb-h],[vx+dx+w/2,vb-h-4],[vx+dx+w+1,vb-h]],col); });
  g.fillRect(vx-6,vb-16,6,16); pfill(g,[[vx-7,vb-16],[vx-3,vb-30],[vx+1,vb-16]],col); g.fillRect(vx-4,vb-33,1,4); g.fillRect(vx-5,vb-32,3,1);
  g.fillStyle='#FFD27A'; [[vx-38,vb-3],[vx-16,vb-4],[vx+10,vb-3],[vx+32,vb-4],[vx-4,vb-10]].forEach(q=>g.fillRect(q[0],q[1],1,1));
  // cypresses and a far windmill
  g.fillStyle=M[1]; [[262,12],[270,9],[278,14],[372,10],[380,13]].forEach(([x,h])=>{ const b=hillY(x)+4; for(let y=0;y<h;y++){ const w=Math.max(1,Math.round(2*Math.sin(Math.PI*Math.min(1,(y+2)/h)))); g.fillRect(x-(w>>1),b-y,w,1); } });
  const mx=600, mb=hillY(mx)+3; g.fillStyle=col; pfill(g,[[mx-4,mb],[mx-2,mb-12],[mx+2,mb-12],[mx+4,mb]],col); [[1,1],[1,-1],[-1,1],[-1,-1]].forEach(([a,b])=>{ for(let k=0;k<9;k++) g.fillRect(mx+a*k,mb-13+b*k,1,1); });
}
// roadside objects, all silhouettes with a rim of light, matching the desert ones
const TITLE_OBJ={
  acacia:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const h=(0.7+h2(o.seed,1)*0.35)*s, cw=(0.9+h2(o.seed,2)*0.5)*s, ty=y-h, tw=Math.max(1,0.05*s);
    tln(g,x,y,x-0.04*s,y-h*0.55,tw,sil); tln(g,x-0.04*s,y-h*0.55,x-0.24*s,ty+0.06*s,Math.max(1,tw*0.6),sil); tln(g,x-0.04*s,y-h*0.55,x+0.2*s,ty+0.05*s,Math.max(1,tw*0.6),sil);
    tP(g,[[x-cw/2,ty+0.06*s],[x-cw*0.42,ty-0.04*s],[x-cw*0.18,ty-0.1*s],[x+cw*0.24,ty-0.11*s],[x+cw*0.46,ty-0.03*s],[x+cw/2,ty+0.05*s],[x+cw*0.28,ty+0.1*s],[x-cw*0.3,ty+0.1*s]],sil);
    if(near) tln(g,x+lit*cw*0.05,ty-0.11*s,x+lit*cw*0.44,ty-0.03*s,1,rim); },
  baobab:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const h=(1.1+h2(o.seed,1)*0.3)*s, bw=0.42*s, tw=0.26*s, ty=y-h;
    tP(g,[[x-bw/2,y],[x-tw/2,ty+0.2*s],[x-tw*0.4,ty],[x+tw*0.4,ty],[x+tw/2,ty+0.2*s],[x+bw/2,y]],sil);
    for(let b=0;b<7;b++){ const a=-Math.PI/2+(b-3)*0.32, L=(0.22+h2(o.seed,b+3)*0.18)*s, ex=x+Math.cos(a)*L*1.6, ey=ty+Math.sin(a)*L; tln(g,x+(b-3)*tw*0.12,ty+2,ex,ey,Math.max(1,0.03*s),sil); disc(g,Math.round(ex),Math.round(ey),Math.max(1,Math.round(0.05*s)),sil); }
    tR(g,lit>0?x+bw/2-1:x-bw/2,y-h*0.7,1,h*0.68,rim); if(near) for(let k=1;k<4;k++) tR(g,x-bw*0.3+k*bw*0.15,ty+0.25*s,1,h*0.6,mid); },
  mound:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const h=(0.45+h2(o.seed,1)*0.35)*s, w=0.32*s; tP(g,[[x-w/2,y],[x-w*0.22,y-h*0.6],[x-w*0.08,y-h],[x+w*0.06,y-h*0.92],[x+w*0.2,y-h*0.55],[x+w/2,y]],sil); tln(g,x+lit*w*0.07,y-h*0.95,x+lit*w*0.45,y-1,1,rim); },
  tuft:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const n=5+Math.floor(h2(o.seed,1)*4); for(let k=0;k<n;k++){ const dx=(k-n/2)*0.04*s, hh=(0.12+h2(o.seed,k+2)*0.14)*s; tln(g,x+dx,y,x+dx+(k-n/2)*0.02*s,y-hh,1,k%3?sil:rim); } },
  rondavel:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const w=0.7*s, wh=0.32*s, rh=0.42*s; tR(g,x-w/2,y-wh,w,wh,sil); tP(g,[[x-w*0.62,y-wh],[x,y-wh-rh],[x+w*0.62,y-wh]],sil); tR(g,x-0.06*s,y-0.22*s,0.12*s,0.22*s,mid); tln(g,x,y-wh-rh,x+lit*w*0.62,y-wh,1,rim); if(near) tR(g,x+0.14*s,y-0.2*s,Math.max(1,0.05*s),Math.max(1,0.05*s),'#E8A040'); },
  giraffe:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const sw=Math.sin(TT*0.8+o.seed)*0.04*s, bx=x-0.3*s, bh=0.25*s, by=y-0.75*s;
    [0,0.08,0.42,0.5].forEach(d=>tln(g,bx+d*s,by+bh*0.5,bx+d*s+0.02*s,y,Math.max(1,0.03*s),sil)); tP(g,[[bx-0.04*s,by+bh*0.6],[bx,by],[bx+0.56*s,by-0.06*s],[bx+0.6*s,by+bh*0.5]],sil);
    tln(g,bx+0.52*s,by,bx+0.72*s+sw,by-0.62*s,Math.max(1,0.06*s),sil); tP(g,[[bx+0.68*s+sw,by-0.66*s],[bx+0.86*s+sw,by-0.6*s],[bx+0.84*s+sw,by-0.55*s],[bx+0.7*s+sw,by-0.56*s]],sil); tln(g,bx+0.72*s+sw,by-0.66*s,bx+0.72*s+sw,by-0.74*s,1,sil);
    if(near) tln(g,bx+0.54*s,by-0.02*s,bx+0.72*s+sw,by-0.62*s,1,rim); },
  kmpost:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const h=0.32*s, w=Math.max(2,0.09*s); tR(g,x-w/2,y-h,w,h,sil); tR(g,x-w/2,y-h,w,Math.max(1,0.06*s),'#C8301A'); tR(g,lit>0?x+w/2-1:x-w/2,y-h,1,h,rim); },
  cypress:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const h=(1.1+h2(o.seed,1)*0.5)*s, w=0.17*s, pts=[]; for(let k=0;k<=10;k++){ const u=k/10, ww=w*Math.sin(Math.PI*Math.min(1,0.15+u*0.95)); pts.push([x-ww/2,y-u*h]); } for(let k=10;k>=0;k--){ const u=k/10, ww=w*Math.sin(Math.PI*Math.min(1,0.15+u*0.95)); pts.push([x+ww/2,y-u*h]); }
    tP(g,pts,sil); if(near) tln(g,x+lit*w*0.3,y-h*0.85,x+lit*w*0.45,y-h*0.2,1,rim); },
  oak:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const h=(0.75+h2(o.seed,1)*0.3)*s, r=(0.32+h2(o.seed,2)*0.12)*s; tln(g,x,y,x,y-h*0.6,Math.max(1,0.07*s),sil);
    [[0,-h,r],[-r*0.7,-h+r*0.35,r*0.75],[r*0.7,-h+r*0.3,r*0.8],[0,-h+r*0.6,r*0.7]].forEach(q=>disc(g,Math.round(x+q[0]),Math.round(y+q[1]),Math.max(1,Math.round(q[2])),sil)); if(near) tln(g,x+lit*r*0.3,y-h-r*0.92,x+lit*r*1.3,y-h+r*0.1,1,rim); },
  wall:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const w=(1.1+h2(o.seed,1)*0.6)*s, h=0.14*s; tR(g,x-w/2,y-h,w,h,sil); tR(g,x-w/2,y-h,w,1,rim); if(near) for(let k=0;k<w;k+=0.18*s) tR(g,x-w/2+k,y-h+((k/(0.18*s))%2?h*0.5:0),1,h*0.5,mid); },
  bale:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const r=Math.max(2,Math.round(0.17*s)); disc(g,Math.round(x),Math.round(y-r),r,sil); if(near){ disc(g,Math.round(x+lit*r*0.25),Math.round(y-r),Math.max(1,Math.round(r*0.55)),mid); tln(g,x+lit*r*0.7,y-r*1.7,x+lit*r,y-r,1,rim); } },
  cottage:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const w=0.8*s, wh=0.36*s, rh=0.3*s; tR(g,x-w/2,y-wh,w,wh,sil); tP(g,[[x-w*0.56,y-wh],[x,y-wh-rh],[x+w*0.56,y-wh]],sil); tR(g,x+w*0.18,y-wh-rh*0.9,0.08*s,rh*0.6,sil);
    const lw=Math.max(1,Math.round(0.08*s)); tR(g,x-w*0.3,y-wh*0.7,lw,lw,'#FFD27A'); tR(g,x+w*0.12,y-wh*0.7,lw,lw,h2(o.seed,4)>0.4?'#FFD27A':mid); tln(g,x,y-wh-rh,x+lit*w*0.56,y-wh,1,rim); },
  church:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const w=0.9*s, wh=0.42*s; tR(g,x-w/2,y-wh,w,wh,sil); tP(g,[[x-w*0.54,y-wh],[x-w*0.1,y-wh-0.22*s],[x+w*0.3,y-wh]],sil);
    const tx=x+w*0.32; tR(g,tx-0.11*s,y-1.0*s,0.22*s,1.0*s,sil); tP(g,[[tx-0.13*s,y-1.0*s],[tx,y-1.45*s],[tx+0.13*s,y-1.0*s]],sil); tln(g,tx,y-1.45*s,tx,y-1.58*s,1,sil); tln(g,tx-0.05*s,y-1.53*s,tx+0.05*s,y-1.53*s,1,sil);
    const lw=Math.max(1,Math.round(0.06*s)); [-0.3,-0.12,0.06].forEach(d=>tR(g,x+d*w,y-wh*0.72,lw,Math.max(1,Math.round(lw*1.6)),'#FFD27A')); tR(g,lit>0?tx+0.11*s-1:tx-0.11*s,y-1.0*s,1,0.9*s,rim); },
  mill:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const h=1.1*s, bw=0.42*s, tw=0.24*s, ty=y-h; tP(g,[[x-bw/2,y],[x-tw/2,ty],[x+tw/2,ty],[x+bw/2,y]],sil); tP(g,[[x-tw*0.6,ty],[x,ty-0.16*s],[x+tw*0.6,ty]],sil);
    const cy=ty-0.04*s, a0=TT*0.6+o.seed; for(let b=0;b<4;b++){ const a=a0+b*Math.PI/2, ex=x+Math.cos(a)*0.7*s, ey=cy+Math.sin(a)*0.7*s; tln(g,x,cy,ex,ey,Math.max(1,0.025*s),sil); const px=-Math.sin(a), py=Math.cos(a); for(let k=3;k<=9;k++){ const u=k/10; tln(g,x+(ex-x)*u,cy+(ey-cy)*u,x+(ex-x)*u+px*0.1*s,cy+(ey-cy)*u+py*0.1*s,1,sil); } }
    tR(g,x-0.05*s,y-0.2*s,0.1*s,0.2*s,'#FFD27A'); tln(g,x+lit*tw/2,ty,x+lit*bw/2,y,1,rim); },
  mile:(g,o,K,x,y,s,lit,sil,rim,mid,near)=>{ const h=0.2*s, w=Math.max(2,0.13*s); tP(g,[[x-w/2,y],[x-w/2,y-h*0.7],[x,y-h],[x+w/2,y-h*0.7],[x+w/2,y]],sil); tln(g,x,y-h,x+lit*w/2,y-h*0.7,1,rim); }
};
