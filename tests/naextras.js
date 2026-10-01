/* ---------- North America's venues, brought up to the newer stages: light, depth and furniture ---------- */
function stageSpots(g,xs,col){ for(const cx of xs){ for(let y=6;y<198;y++){ const f=y/198, hw=10+f*44; for(let x=Math.round(cx-hw);x<=Math.round(cx+hw);x++){ const e=1-Math.abs(x-cx)/hw; if(B8[y&7][x&7]/64<e*0.22*(0.4+f*0.6)){ g.fillStyle=col; g.fillRect(x,y,1,1); } } } } }
function stageLip(g,plank,edge){ g.fillStyle=plank; g.fillRect(0,198,640,8); g.fillStyle=edge; g.fillRect(0,198,640,1); g.fillStyle='rgba(0,0,0,.35)'; g.fillRect(0,205,640,1);
  for(let x=40;x<640;x+=80){ g.fillStyle='#1A1010'; g.fillRect(x,199,8,5); g.fillStyle='#FFD890'; g.fillRect(x+2,199,4,2); for(let k=1;k<6;k++){ g.fillStyle='rgba(255,210,140,'+(0.18-k*0.03).toFixed(2)+')'; g.fillRect(x+2-k,198-k*2,4+k*2,2); } } }
function bulbString(g,y0,sag,warm){ let px0=-4, py0=y0;
  for(let x=0;x<=640;x+=2){ const u=(x%160)/160, y=Math.round(y0+Math.sin(u*Math.PI)*sag); g.fillStyle='#1A100A'; g.fillRect(x,y,2,1);
    if(x%32===16){ g.fillStyle='#1A100A'; g.fillRect(x,y+1,1,2); g.fillStyle=warm; g.fillRect(x-1,y+3,3,3); g.fillStyle='#FFFFFF'; g.fillRect(x,y+3,1,1); for(let k=1;k<4;k++){ g.fillStyle='rgba(255,210,130,'+(0.16-k*0.04).toFixed(2)+')'; g.fillRect(x-1-k,y+3-k,3+k*2,3+k*2); } } } }
(function(){
  const spur=ART.spur, juke=ART.juke; if(!spur||!juke) return;
  const sd=spur.detail;
  spur.detail=function(g){ sd.call(this,g);
    bulbString(g,8,14,'#FFE6A0');
    const w=document.createElement('canvas'); w.width=24; w.height=24; wagonWheel(w.getContext('2d'),12); g.imageSmoothingEnabled=false; g.drawImage(w,196,26,48,48);
    // the back bar under the bottles
    g.fillStyle='#3A1E0C'; g.fillRect(66,146,86,6); g.fillStyle='#5A3218'; g.fillRect(66,146,86,1); g.fillStyle='#2A1408'; g.fillRect(70,152,78,44); for(let x=74;x<146;x+=12){ g.fillStyle='#34190A'; g.fillRect(x,154,1,40); }
    g.fillStyle='#C8963A'; g.fillRect(68,186,82,2); [[82],[112],[140]].forEach(([x])=>{ g.fillStyle='#2A1408'; g.fillRect(x-5,170,11,3); g.fillRect(x-4,173,2,24); g.fillRect(x+3,173,2,24); g.fillStyle='#8A2A1A'; g.fillRect(x-5,169,11,2); });
    // a jukebox glowing in the corner
    const jx=522, jy=122; g.fillStyle='#1A0C08'; g.fillRect(jx-1,jy+10,38,66); g.fillStyle='#5A1E14'; g.fillRect(jx,jy+12,36,62); g.fillStyle='#1A0C08'; g.beginPath(); g.arc(jx+18,jy+14,19,Math.PI,0); g.fill();
    ['#FF5A4A','#FFC040','#6AE07A','#4AB0FF'].forEach((c,k)=>{ g.fillStyle=c; g.beginPath(); g.arc(jx+18,jy+14,17-k*3,Math.PI,0); g.fill(); }); g.fillStyle='#2A1410'; g.beginPath(); g.arc(jx+18,jy+14,5,Math.PI,0); g.fill();
    g.fillStyle='#E8D8B0'; g.fillRect(jx+6,jy+22,24,10); for(let k=0;k<4;k++){ g.fillStyle='#8A6A3A'; g.fillRect(jx+8,jy+24+k*2,20,1); } g.fillStyle='#2A1410'; g.fillRect(jx+6,jy+38,24,26); for(let y=jy+40;y<jy+62;y+=3){ g.fillStyle='#4A2A1C'; g.fillRect(jx+8,y,20,1); }
    for(let k=1;k<6;k++){ g.fillStyle='rgba(255,170,90,'+(0.07).toFixed(2)+')'; g.fillRect(jx-k*3,jy+10-k*2,36+k*6,66+k*4); }
    stageSpots(g,[156,484],'rgba(255,226,160,.9)'); stageLip(g,'#6A4020','#A8743A'); };
  const jd=juke.detail;
  juke.detail=function(g){ jd.call(this,g);
    // a guitar hanging on the wall and a potbelly stove with a warm glow
    g.fillStyle='#1A0C08'; g.fillRect(118,40,2,6); g.fillStyle='#5A2A10'; g.fillRect(117,46,4,34); g.fillStyle='#C87A30'; g.beginPath(); g.ellipse(119,92,11,13,0,0,Math.PI*2); g.fill(); g.beginPath(); g.ellipse(119,76,8,9,0,0,Math.PI*2); g.fill(); g.fillStyle='#1A0804'; g.beginPath(); g.arc(119,84,3,0,Math.PI*2); g.fill(); g.fillStyle='#3A1A0A'; g.fillRect(114,98,10,2);
    const sx=76; g.fillStyle='#141414'; g.fillRect(sx+6,60,4,70); g.fillStyle='#1E1E22'; g.beginPath(); g.ellipse(sx+8,150,14,20,0,0,Math.PI*2); g.fill(); g.fillRect(sx-4,168,24,6); g.fillStyle='#FF8A30'; g.fillRect(sx+3,146,10,8); g.fillStyle='#FFD070'; g.fillRect(sx+5,148,6,4);
    for(let k=1;k<7;k++){ g.fillStyle='rgba(255,140,60,0.06)'; g.fillRect(sx+8-k*5,150-k*4,k*10,k*8); }
    // a worn red rug under the players
    g.fillStyle='#6A1414'; g.fillRect(100,192,440,8); g.fillStyle='#8A2A1E'; g.fillRect(104,193,432,1); for(let x=110;x<530;x+=14){ g.fillStyle='#C8963A'; g.fillRect(x,195,6,2); }
    stageSpots(g,[156,484],'rgba(255,214,150,.9)'); stageLip(g,'#4A2A12','#7A5028'); };
})();
