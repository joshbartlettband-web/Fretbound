/* ---------- the van, between tours: a roadside motel at dawn ----------
   Drawn behind the Van menu at two screen pixels per art pixel. The ground and the van sit at the bottom,
   where the gap above the buttons shows them; the player and seated band members stand around in the lot. */
let vanSceneT=null; const vsCache={};
function vsSprite(key,build,s){ if(vsCache[key]) return vsCache[key]; return vsCache[key]=rasterLayers(build(),s,70,56,28,52); }
function drawVanScene(){
  const cv=$('vanScene'); if(!cv) return; const r=cv.getBoundingClientRect(); if(!r.width) return;
  const W=Math.max(120,Math.round(r.width/2)), H=Math.max(120,Math.round(r.height/2)); if(cv.width!==W||cv.height!==H){ cv.width=W; cv.height=H; }
  const g=cv.getContext('2d'), t=performance.now()/1000, hz=H-58;
  // dawn sky, dithered into bands
  const stops=[[0,[22,14,40]],[0.45,[70,34,78]],[0.75,[176,72,98]],[1,[240,156,92]]];
  const col=u=>{ for(let k=1;k<stops.length;k++) if(u<=stops[k][0]){ const a=stops[k-1],b=stops[k],f=(u-a[0])/(b[0]-a[0]); return a[1].map((v,i)=>Math.round(v+(b[1][i]-v)*f)); } return stops[3][1]; };
  for(let y=0;y<hz;y++){ const u=y/hz, c0=col(u), c1=col(Math.min(1,u+0.06)); for(let x=0;x<W;x++){ const c=(B8[y&7][x&7]/64<((u*16)%1))?c1:c0; g.fillStyle='rgb('+c+')'; g.fillRect(x,y,1,1); } }
  for(let i=0;i<40;i++){ const x=Math.floor(h2(i,71)*W), y=Math.floor(h2(i,72)*hz*0.45), a=(0.35+0.5*Math.sin(t*(0.3+h2(i,73)*0.5)+i))*(1-y/(hz*0.5)); if(a>0.1){ g.fillStyle='rgba(255,240,220,'+a.toFixed(2)+')'; g.fillRect(x,y,1,1); } }
  // the sun just breaking the horizon, and far mesas
  g.fillStyle='rgba(255,220,150,.35)'; g.beginPath(); g.arc(W*0.78,hz,16,Math.PI,0); g.fill(); g.fillStyle='#FFE0A0'; g.beginPath(); g.arc(W*0.78,hz,9,Math.PI,0); g.fill();
  g.fillStyle='#4A2448'; g.beginPath(); g.moveTo(0,hz); [[0,hz-10],[W*0.12,hz-10],[W*0.16,hz-4],[W*0.3,hz-4],[W*0.34,hz-14],[W*0.5,hz-14],[W*0.53,hz-6],[W*0.66,hz-6],[W*0.7,hz-11],[W*0.9,hz-11],[W*0.93,hz-3],[W,hz-3],[W,hz]].forEach(q=>g.lineTo(q[0],q[1])); g.fill();
  // the lot
  g.fillStyle='#2A2026'; g.fillRect(0,hz,W,H-hz); for(let i=0;i<120;i++){ g.fillStyle=i%3?'#342A30':'#1E181C'; g.fillRect(Math.floor(h2(i,81)*W),hz+2+Math.floor(h2(i,82)*(H-hz-2)),1,1); }
  g.fillStyle='#C8B870'; for(let k=0;k<5;k++){ const x=W*0.52+k*16; for(let y=0;y<12;y++) g.fillRect(Math.round(x-y*0.6),hz+14+y,1,1); }
  // the motel: warm windows, teal doors, and a neon sign that flickers
  const mx=Math.round(W*0.5), my=hz-26, mw=W-mx+2;
  g.fillStyle='#5A3E32'; g.fillRect(mx,my,mw,28); g.fillStyle='#3A2820'; g.fillRect(mx-2,my-3,mw+2,4); g.fillStyle='#7A5A48'; g.fillRect(mx,my+1,mw,1);
  for(let k=0;k*14<mw-8;k++){ const x=mx+4+k*14; g.fillStyle='#2A6A6A'; g.fillRect(x,my+10,5,16); g.fillStyle='#E0C070'; g.fillRect(x+3,my+17,1,1);
    const lit=h2(k,91)>0.35; g.fillStyle=lit?'#FFD27A':'#2A2230'; g.fillRect(x+7,my+11,5,5); if(lit){ g.fillStyle='rgba(255,210,120,.18)'; g.fillRect(x+6,my+26,7,3); } }
  const sx=mx-10, sy=my-30; g.fillStyle='#3A3A44'; g.fillRect(sx+6,sy+14,2,H); g.fillStyle='#1A1016'; g.fillRect(sx-4,sy,22,14); g.fillStyle='#3A2028'; g.fillRect(sx-4,sy,22,1);
  const on=Math.sin(t*23)>-0.8||Math.sin(t*1.3)>0.5, vac=((t*1.7)%4)>0.25;
  g.font="8px 'Jersey 10',monospace"; g.textBaseline='top'; g.shadowBlur=4; g.shadowColor='#FF3A4A'; g.fillStyle=on?'#FF6A70':'#6A2028'; g.fillText('MOTEL',sx-2,sy+2);
  g.shadowColor='#5AFF8A'; g.fillStyle=vac?'#8AFFA8':'#1E4A2A'; g.font="6px 'Jersey 10',monospace"; g.fillText('VACANCY',sx-3,sy+16); g.shadowBlur=0;
  // the van, side on, door open with gear inside
  const vx=Math.round(W*0.05), vy=H-40, vw=Math.min(84,Math.round(W*0.46)), vh=26;
  g.fillStyle='rgba(0,0,0,.35)'; g.fillRect(vx+2,vy+vh+3,vw,3);
  g.fillStyle='#F2E6CC'; g.fillRect(vx,vy,vw,12); g.fillStyle='#C8342C'; g.fillRect(vx,vy+12,vw,vh-12); g.fillStyle='#8A1E1A'; g.fillRect(vx,vy+vh-3,vw,3);
  g.fillStyle='#F2E6CC'; g.fillRect(vx+vw-2,vy+2,5,vh-6); g.fillStyle='#2A4A6A'; g.fillRect(vx+vw-12,vy+2,10,8); g.fillStyle='#4A7AA0'; g.fillRect(vx+vw-11,vy+3,4,2);
  g.fillStyle='#2A4A6A'; g.fillRect(vx+4,vy+2,12,7); const dx=vx+20, dw=Math.round(vw*0.36); g.fillStyle='#1A1016'; g.fillRect(dx,vy+2,dw,vh-5);
  g.fillStyle='#4A4A54'; g.fillRect(dx+2,vy+vh-14,9,11); g.fillStyle='#8A8A96'; g.fillRect(dx+3,vy+vh-13,7,4); g.fillStyle='#6A3A1A'; g.fillRect(dx+13,vy+6,5,vh-9); g.fillStyle='#8A5A2A'; g.fillRect(dx+13,vy+6,5,2);
  g.fillStyle='#3A2A22'; g.fillRect(vx+6,vy-3,vw-20,2); g.fillStyle='#6A4A2A'; g.fillRect(vx+10,vy-7,12,4); g.fillStyle='#2A4A6A'; g.fillRect(vx+24,vy-6,9,3);
  [[vx+12],[vx+vw-16]].forEach(([wx])=>{ g.fillStyle='#141014'; g.beginPath(); g.arc(wx,vy+vh,5,0,Math.PI*2); g.fill(); g.fillStyle='#8A8A96'; g.beginPath(); g.arc(wx,vy+vh,2,0,Math.PI*2); g.fill(); });
  // your player and seated band, hanging around the lot
  const who=[['p',state.char||'bard'],...(META.lineup||[]).filter(id=>BANDP[id]).map(id=>['b',id])];
  const x0=vx+vw+8, gap=Math.max(14,Math.min(22,(W-x0-6)/Math.max(1,who.length)));
  who.forEach(([k,id],i)=>{ const spr=k==='p'?vsSprite('p'+id,()=>h2frame(id,{nod:0}),0.34):vsSprite('b'+id,()=>bandLayers(id,{bare:1}),0.34);
    g.drawImage(spr,Math.round(x0+i*gap-28),Math.round(H-10-52)); });
}
function startVanScene(){ drawVanScene(); clearInterval(vanSceneT); vanSceneT=setInterval(()=>{ if(state.screen==='van') drawVanScene(); else { clearInterval(vanSceneT); vanSceneT=null; } },140); }
