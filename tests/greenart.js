/* ---------- the Green Room: a backstage dressing room, and the tech who plays you the notes ---------- */
function buildGreenBg(g){
  // painted wall in two greens, dithered toward the light
  for(let y=0;y<96;y++){ const u=y/96; for(let x=0;x<SW;x+=2){ const dth=(B8[y&7][x&7]/64)<(u*0.9)?1:0; g.fillStyle=dth?'#2A6042':'#347048'; g.fillRect(x,y,2,1); } }
  for(let i=0;i<90;i++){ g.fillStyle=i%2?'#3C7C52':'#245238'; g.fillRect((i*47)%SW,(i*31)%60+2,i%3?2:1,1); }
  // wainscot, dado rail and skirting
  g.fillStyle='#1E4A32'; g.fillRect(0,64,SW,32); for(let x=0;x<SW;x+=26){ g.fillStyle='#173A27'; g.fillRect(x,66,1,28); g.fillStyle='#2A5C40'; g.fillRect(x+1,66,1,28); }
  g.fillStyle='#6A4A2A'; g.fillRect(0,61,SW,3); g.fillStyle='#A8783E'; g.fillRect(0,61,SW,1); g.fillStyle='#3A2412'; g.fillRect(0,63,SW,1); g.fillStyle='#3A2412'; g.fillRect(0,94,SW,2);
  // the door with the gold star, far left
  g.fillStyle='#2A1A0C'; g.fillRect(3,14,40,82); g.fillStyle='#4A7A52'; g.fillRect(5,16,36,80); g.fillStyle='#386A44'; g.fillRect(5,56,36,40);
  g.fillStyle='#2A5A36'; g.fillRect(9,20,28,30); g.fillRect(9,58,28,32); g.fillStyle='#5A9A66'; g.fillRect(9,20,28,1); g.fillRect(9,58,28,1); g.fillStyle='#1E4A2C'; g.fillRect(9,49,28,1); g.fillRect(9,89,28,1);
  const star=[[23,24],[24,24],[22,27],[23,27],[24,27],[25,27],[17,29],[18,29],[19,29],[20,29],[21,29],[22,29],[23,29],[24,29],[25,29],[26,29],[27,29],[28,29],[29,29],[19,31],[20,31],[21,31],[22,31],[23,31],[24,31],[25,31],[26,31],[27,31],[20,33],[21,33],[22,33],[23,33],[24,33],[25,33],[26,33],[20,35],[21,35],[25,35],[26,35],[19,37],[27,37]];
  star.forEach(q=>{ g.fillStyle='#FFD860'; g.fillRect(q[0],q[1],1,2); }); g.fillStyle='#FFF4B8'; g.fillRect(23,26,2,2);
  g.fillStyle='#C8963A'; g.fillRect(36,60,3,3); g.fillStyle='#8A5E1A'; g.fillRect(36,62,3,1);
  // clothing rack with stage jackets
  g.fillStyle='#8A8A96'; g.fillRect(48,26,44,2); g.fillStyle='#5A5A66'; g.fillRect(50,28,1,66); g.fillRect(89,28,1,66); g.fillStyle='#3A3A44'; g.fillRect(46,93,48,2);
  [['#C8342A',54],['#E8B030',62],['#2A6AB0',70],['#F0F0E8',78],['#7A2A8A',85]].forEach(([c,x],i)=>{ g.fillStyle='#3A3A44'; g.fillRect(x+3,28,1,3); g.fillStyle=c; g.fillRect(x,31,8,30-i%2*4); g.fillStyle='rgba(0,0,0,.25)'; g.fillRect(x+5,31,3,30-i%2*4); g.fillStyle='rgba(255,255,255,.2)'; g.fillRect(x,31,1,30-i%2*4); });
  g.fillStyle='#E8D8A0'; g.fillRect(58,22,14,3); g.fillRect(61,18,8,4); g.fillStyle='#A8783E'; g.fillRect(58,24,14,1);
  // the dressing mirror with its bulbs
  g.fillStyle='#1A1410'; g.fillRect(98,12,128,56); g.fillStyle='#3A2A1A'; g.fillRect(100,14,124,52);
  for(let y=16;y<64;y++){ const u=(y-16)/48; g.fillStyle=u<0.5?'#9ACAD0':'#7AB0BA'; g.fillRect(104,y,116,1); }
  for(let i=0;i<40;i++){ g.fillStyle='rgba(255,255,255,'+(0.06+0.05*(i%3))+')'; g.fillRect(104+(i*29)%110,17+(i*11)%44,3,1); }
  g.fillStyle='rgba(255,255,255,.35)'; for(let k=0;k<26;k++) g.fillRect(118+k,50-k,2,1); for(let k=0;k<14;k++) g.fillRect(150+k,50-k,1,1);
  // a couch reflected in the glass
  g.fillStyle='rgba(90,30,40,.55)'; g.fillRect(122,44,70,14); g.fillRect(118,38,10,20); g.fillRect(190,38,10,20); g.fillStyle='rgba(120,50,60,.5)'; g.fillRect(124,42,66,3);
  // counter under the mirror
  g.fillStyle='#4A2C16'; g.fillRect(96,70,132,5); g.fillStyle='#8A5A2E'; g.fillRect(96,70,132,1); g.fillStyle='#2A160A'; g.fillRect(96,75,132,2); g.fillStyle='#2A160A'; g.fillRect(100,77,3,17); g.fillRect(221,77,3,17);
  // the corkboard and the amp stack on the right
  g.fillStyle='#3A2412'; g.fillRect(236,18,62,46); g.fillStyle='#B8844A'; g.fillRect(238,20,58,42); for(let i=0;i<70;i++){ g.fillStyle=i%2?'#A87438':'#C8944E'; g.fillRect(238+(i*13)%58,20+(i*7)%42,1,1); }
  [[242,24,14,18,'#F0E4B8','#C8483A'],[260,22,12,16,'#9AC8E0','#2A4A8A'],[276,26,16,14,'#E8B8D8','#6A2A6A'],[246,46,12,12,'#F0E0A0','#3A7A4A'],[264,42,14,16,'#E8C8A0','#8A4A1A']].forEach(([x,y,w,h,pa,ink],i)=>{ g.fillStyle='rgba(0,0,0,.3)'; g.fillRect(x+1,y+1,w,h); g.fillStyle=pa; g.fillRect(x,y,w,h); g.fillStyle=ink; g.fillRect(x+2,y+3,w-4,(h*0.4)|0); g.fillStyle='#3A2A20'; for(let k=0;k<2;k++) g.fillRect(x+2,y+(h*0.4|0)+6+k*3,w-4-k*3,1); g.fillStyle='#C83A3A'; g.fillRect(x+(w>>1)-1,y-1,2,2); });
  g.fillStyle='#1E1E24'; g.fillRect(272,70,42,26); g.fillStyle='#2E2E38'; g.fillRect(274,72,38,22); g.fillStyle='#1A1A20'; for(let y=74;y<92;y+=2) g.fillRect(276,y,34,1); g.fillStyle='#D0B060'; g.fillRect(276,73,34,1); g.fillStyle='#8A8A96'; g.fillRect(279,71,2,1); g.fillRect(288,71,2,1); g.fillRect(297,71,2,1);
  // floor, with a worn rug
  g.fillStyle='#6E4C2E'; g.fillRect(0,96,SW,24); for(let y=96;y<120;y+=6){ g.fillStyle='#4A3018'; g.fillRect(0,y,SW,1); for(let x=((y/6)&1)*13;x<SW;x+=34) g.fillRect(x,y,1,6); }
  for(let i=0;i<260;i++){ g.fillStyle=i%3?'#8A6440':'#5A3C20'; g.fillRect((i*37)%SW,96+(i*13)%24,1,1); }
  g.fillStyle='#2A1408'; g.fillRect(60,102,200,16); g.fillStyle='#7A2A28'; g.fillRect(62,103,196,14); g.fillStyle='#D9A441'; g.fillRect(64,105,192,1); g.fillRect(64,115,192,1);
  for(let x=68;x<252;x+=12){ g.fillStyle='#2A6A6A'; g.fillRect(x,107,6,6); g.fillStyle='#E8D8A0'; g.fillRect(x+2,109,2,2); }
}
function detailGreen(g){
  // bulbs around the mirror, each with a halo
  const bulb=(x,y)=>{ for(let k=3;k>=1;k--){ g.fillStyle='rgba(255,200,120,'+(0.06*(4-k)).toFixed(2)+')'; g.fillRect(x-k*2,y-k*2,4+k*4,4+k*4); } g.fillStyle='#FFF0C8'; g.fillRect(x,y,4,4); g.fillStyle='#FFD890'; g.fillRect(x+1,y+1,2,2); g.fillStyle='#FFFFFF'; g.fillRect(x,y,1,1); };
  for(let x=196;x<=450;x+=14){ bulb(x,18); bulb(x,134); } for(let y=30;y<=122;y+=14){ bulb(194,y); bulb(450,y); }
  // the set list and a mug on the counter, and a string winder
  g.fillStyle='#F0E4C0'; g.fillRect(250,132,18,6); g.fillStyle='#3A2A20'; g.fillRect(252,133,12,1); g.fillRect(252,135,9,1);
  g.fillStyle='#E8E8E0'; g.fillRect(380,130,9,10); g.fillStyle='#B8B8B0'; g.fillRect(380,130,1,10); g.fillStyle='#7A3A1A'; g.fillRect(381,131,7,2); g.fillStyle='#E8E8E0'; g.fillRect(389,132,3,5); g.fillStyle='#1E1814'; g.fillRect(390,133,1,3);
  g.fillStyle='#8A8A96'; g.fillRect(410,135,14,3); g.fillStyle='#C83A3A'; g.fillRect(424,134,4,5);
  // a guitar case on the floor near the rack and a pair of boots
  g.fillStyle='#1E1E24'; g.fillRect(100,172,74,14); g.fillStyle='#2E2E3A'; g.fillRect(102,174,70,10); g.fillStyle='#8A8A96'; g.fillRect(100,172,74,1); g.fillRect(100,185,74,1); g.fillStyle='#D0B060'; g.fillRect(134,177,6,4);
  // the GREEN ROOM plate over the door, lit from behind
  g.fillStyle='#0E2A1A'; g.fillRect(14,2,68,12); g.fillStyle='#5AFF9A'; g.fillRect(16,4,64,8); g.fillStyle='#0E2A1A'; g.fillRect(17,5,62,6);
  g.font="bold 8px 'Silkscreen',monospace"; g.textBaseline='middle'; g.textAlign='center'; g.shadowColor='#5AFF9A'; g.shadowBlur=3; g.fillStyle='#BFFFD8'; g.fillText('GREEN ROOM',48,9); g.shadowBlur=0; g.textAlign='left';
}
ART.green={bg:buildGreenBg,detail:detailGreen,dyn:(g,t)=>{},rival:()=>{},vec:true,pbg:'#1E4A32',motes:false};
GROOVES.green={gain:0.95,swing:0.5,room:0.12,drums:[['softkick','x.......x.......'],['rim','....x.......x...'],['hat','x.o.x.o.x.o.x.o.']],bass:['electric','1.....1.1.......',1],comp:['chop','....x.......x...',0.5]};
// the tech, drawn from his portrait: olive beanie with a headlamp, grey work shirt, a lanyard pass and pliers in the pocket
RIVAL_VEC.green={s:1.0,W:124,H:118,ox:54,oy:112,gt:{id:'nylon',body:['#B86A1C','#E8A040'],wood:'rosewood'},arm:{},
  P:{skin:'#E8B88A',skinD:'#C0906A',top:'#7A7A86',topD:'#56565F',topL:'#9A9AA6',sleeve:'#7A7A86',sleeveD:'#56565F'},
  body(P,p){ return [
    {s:'M -5 -44 L -6 -7',w:8,c:'#2E3038'},{s:'M 5 -44 L 6 -7',w:8,c:'#3A3C46'},{d:'M -11 0 L -11 -7 L -1 -7 L 1 0 Z',c:'#2A1A10'},{d:'M 1 0 L 1 -7 L 11 -7 L 13 0 Z',c:'#3A2414'},
    {d:'M -12 -43 L 12 -43 L 12 -40 L -12 -40 Z',c:'#3A2A1A'},{p:[-1,-43,3,3],c:'#C8963A'},
    {d:'M -12 -74 Q 0 -78 12 -74 L 13 -43 L -13 -43 Z',c:P.top},{d:'M 6 -75 L 12 -74 L 13 -43 L 5 -43 Z',c:P.topD},{s:'M -9 -72 L -10 -48',w:1.3,c:P.topL},
    {d:'M -5 -76 L 5 -76 L 0 -66 Z',c:'#E8E0D0'},{s:'M -5 -76 L 0 -66 L 5 -76',w:1,c:P.topD},
    {d:'M -10 -62 L -4 -62 L -4 -52 L -10 -52 Z',c:P.topD},{d:'M -9 -61 L -5 -61 L -5 -53 L -9 -53 Z',c:'#6A6A76'},{p:[-9,-63,2,2],c:'#C8342A'},{p:[-6,-63,2,2],c:'#C8342A'},{p:[-8,-60,3,4],c:'#B8B8C4'},
    {s:'M -2 -75 L -3 -58 M 3 -75 L 4 -58',w:1.2,c:'#1E2A3A'},{d:'M 0 -62 L 6 -62 L 6 -54 L 0 -54 Z',c:'#E8EEF0'},{d:'M 1 -61 L 5 -61 L 5 -55 L 1 -55 Z',c:'#7AB0C0'},{p:[2,-59,2,2],c:'#3A5A6A'},
    {s:'M 0 -81 L 0 -77',w:3.6,c:P.skinD},{e:[1.4,-87,6.2,7.6,0],c:P.skin},{e:[-3.8,-86.6,1.4,2.2,0],c:P.skinD},{p:[3,-88,1.6,p.blink?0.7:2],c:'#2A1206'},{p:[6.4,-88,1.4,p.blink?0.7:2],c:'#2A1206'},{p:[2.4,-90.4,3,0.8],c:'#3A2412'},{p:[5.6,-90.4,2.6,0.8],c:'#3A2412'},
    {s:'M 3 -82.4 Q 5.4 -81 7.4 -82.6',w:0.8,c:'#8A4A30'},{p:[7.2,-85.6,1.2,1.6],c:'#D09870'},
    {d:'M -6 -91 Q -7 -99 1 -100 Q 9 -99 9 -91 L 8.4 -88.6 L -5.6 -88.6 Z',c:'#7A6E3A'},{d:'M 4 -99.6 Q 9 -98.6 9 -91 L 8 -90 L 4 -90 Z',c:'#5A5026'},{s:'M -5.6 -89.6 L 8.6 -89.6',w:1.6,c:'#2A2A32'},
    {s:'M -6.4 -90.4 L -6.4 -96 M -3 -90.4 L -3 -97 M 0.4 -90.4 L 0.4 -98 M 3.8 -90.4 L 3.8 -97.6',w:0.6,c:'#6A5E30'},
    {d:'M 6.6 -96.6 L 11.4 -96.6 L 11.4 -91.2 L 6.6 -91.2 Z',c:'#3A3A46'},{d:'M 7.4 -95.8 L 10.6 -95.8 L 10.6 -92 L 7.4 -92 Z',c:'#FFF4C8'},{p:[8.4,-95,1.2,1.2],c:'#FFFFFF'},
    {s:'M -3 -92 L -8 -84',w:1,c:'#E0A830'},{p:[-9,-84.6,2,1.2],c:'#C85A1A'}
  ]; }};
