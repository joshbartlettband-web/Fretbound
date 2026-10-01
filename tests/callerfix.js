/* callers matched to their Gemini portraits: extra layers before (behind) or after (in front of) each costume */
function rvWrap(id,before,after){ const R=RIVAL_VEC[id]; if(!R) return; const ob=R.body; R.body=function(P,p){ return [...(before?before(P,p):[]),...ob.call(this,P,p),...(after?after(P,p):[])]; }; }
(function(){
  const V=RIVAL_VEC;
  // the Drop Bear: a koala in a blue work shirt with rolled sleeves
  Object.assign(V.outback.P,{sleeve:'#3A5A8A',sleeveD:'#243A5A'}); V.outback.arm={wide:true,bare:true};
  rvWrap('outback',null,(P,p)=>[{e:[-9,-95,8.6,8.2,0],c:'#8A8A92'},{e:[-9.4,-94.6,5.2,5,0],c:'#D8CCCC'},{e:[13.4,-95.6,8.4,8,0],c:'#9A9AA2'},{e:[13.6,-95,5,4.8,0],c:'#E0D4D4'},
    {e:[2.4,-87,9.6,9,0],c:'#8A8A92'},{e:[-2.6,-86,4.6,6.4,0],c:'#74747E'},{e:[5,-81.6,5.6,2.8,0],c:'#B4B0B4'},
    {e:[9.6,-86.4,3.2,3.8,0],c:'#1A1A20'},{p:[9.2,-88.4,1,1],c:'#6A6A74'},{p:[4.4,-90.6,1.2,p.blink?0.8:1.8],c:'#1A0E0A'},{p:[0.4,-90.6,1.2,p.blink?0.8:1.8],c:'#1A0E0A'},{s:'M 5 -82.4 Q 7.4 -81 9.4 -82.4',w:0.8,c:'#3A2A2A'}]);
  // the Neon Condor: bald coral head, hooked beak, white ruff, black suit, neon guitar
  V.chicha.gt=Object.assign({},V.chicha.gt,{body:['#FF3AA8','#F2F0D4']});
  rvWrap('chicha',null,(P,p)=>[{d:'M -3.6 -74 L 3.6 -74 L 0 -60 Z',c:'#F4F0E8'},{d:'M -0.9 -73 L 0.9 -73 L 1.2 -62 L 0 -60 L -1.2 -62 Z',c:'#0A080A'},
    {d:'M -10 -76 L -7 -80 L -4 -77 L -1 -81 L 2 -77 L 5 -81 L 8 -77 L 11 -80 L 12 -75 L 8 -72 L 3 -73 L -2 -72 L -7 -73 Z',c:'#F4F4EE'},{s:'M -8 -75 Q 1 -71 10 -75',w:1,c:'#C8C8C0'},
    {e:[3.4,-87.4,7.4,8.4,0],c:'#E07A6A'},{e:[-0.6,-86,4.2,6.4,0],c:'#C45E50'},{s:'M -1 -92 Q 3 -94 7 -92',w:0.8,c:'#B0544A'},
    {d:'M 8.6 -89.6 Q 15 -90 16.4 -86 Q 16.6 -83.6 15 -82.6 Q 14.8 -85 12.6 -85.6 L 8.8 -85.4 Z',c:'#E8DCB8'},{p:[15,-84,1,1.2],c:'#8A7A58'},
    {e:[6.4,-89.8,1.8,1.8,0],c:'#F4E0C8'},{p:[6.2,-90.2,1,p.blink?0.6:1.2],c:'#140A08'}]);
  // the Kitsune: nine tails fanned behind her (seven show)
  rvWrap('tokyo',(P,p)=>{ const L=[], bx=-3, by=-54, sw=(p.sway||0)*0.05;
    for(let i=0;i<7;i++){ const a=(200+i*23)*Math.PI/180+sw, dx=Math.cos(a), dy=Math.sin(a), rot=a-Math.PI/2;
      L.push({e:[bx+dx*19,by+dy*19,5.6,16,rot],c:i%2?'#D85A18':'#E8701E'},{e:[bx+dx*31,by+dy*31,4.2,5.6,rot],c:'#F4ECDC'}); }
    return L; },null);
  // the Silence: a blank pale face in a hood rimed with icicles
  rvWrap('pole',null,(P,p)=>[{e:[4.4,-86,7,8.4,0],c:'#8EA6BE'},{e:[5,-85.2,6.2,7.4,0],c:'#C4D6E6'},{e:[6.2,-83.6,3.6,4.4,0],c:'#DCE8F2'},
    ...[[-2.4,-94.6,2.4],[1.6,-96.4,3],[6,-96.2,2.4],[10,-94,3.2],[11.8,-89,2.2]].map(q=>({d:'M '+(q[0]-1.1)+' '+q[1]+' L '+(q[0]+1.1)+' '+q[1]+' L '+q[0]+' '+(q[1]+q[2])+' Z',c:'#BFE4FF'}))]);
  // the Tiger of the Ghats: a marigold garland
  rvWrap('ghat',null,(P,p)=>{ const L=[], pts=[]; for(let k=0;k<=8;k++){ const u=k/8; pts.push([-7.4+u*3.4,-76+u*20],[8.4-u*3.2,-76+u*20]); }
    pts.push([-3,-55],[0,-54],[3,-55]); pts.forEach((q,i)=>L.push({e:[q[0],q[1],2,2,0],c:i%3===0?'#FFC030':i%3===1?'#F08A1A':'#E86A10'})); return L; });
  // the Emperor: golden neck and ear patches and a black bow tie
  rvWrap('mess',null,(P,p)=>[{e:[-3.4,-83.4,2.8,4.2,0.3],c:'#F0B030'},{e:[0,-78,6.4,3.6,0],c:'#F0B030'},{e:[0.4,-76.4,5.4,2.4,0],c:'#F8D070'},
    {d:'M -3.6 -75.4 L 0 -73.8 L -3.6 -72.2 Z',c:'#10141C'},{d:'M 3.6 -75.4 L 0 -73.8 L 3.6 -72.2 Z',c:'#10141C'},{e:[0,-73.8,1.1,1.1,0],c:'#10141C'}]);
  // the Frost Lich: a spiked leather jacket
  rvWrap('frost',null,(P,p)=>[...[[-13,-72,-0.5],[-10.6,-75,-0.2],[-7.8,-76.4,0],[8.4,-76.4,0],[11.2,-75,0.2],[13.6,-72,0.5]].map(q=>({d:'M '+(q[0]-1.3)+' '+(q[1]+1)+' L '+(q[0]+1.3)+' '+(q[1]+1)+' L '+(q[0]+q[2]*3)+' '+(q[1]-3.4)+' Z',c:'#C8D0DC'})),
    ...[[-6,-66],[-6,-58],[6.6,-66],[6.6,-58]].map(q=>({p:[q[0],q[1],1,1],c:'#C8D0DC'}))]);
  // the Sebene Peacock: the deeper pink suit from the portrait
  Object.assign(V.sebene.P,{top:'#D8607A',topD:'#A83E58',topL:'#F08AA0',pants:'#D05878',pantsD:'#A03E56',sleeve:'#D8607A',sleeveD:'#A83E58'});
})();
