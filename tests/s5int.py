import re
p='/home/claude/fretbound.html'; t=open(p,encoding='utf-8').read(); rig=open('/home/claude/rivalrig.js').read()
assert 'function rivalFrame2' not in t
def rep(a,b):
    global t; assert t.count(a)==1,(t.count(a),a[:90]); t=t.replace(a,b,1)
rb=open('/home/claude/rivalband.js').read()
rep("\nfunction goVan(){ renderVan(); goScreen('van'); }", "\n"+rig+rb+"\nfunction goVan(){ renderVan(); goScreen('van'); }")
rep("function h2guitar(gid,C,na){\n  const G=G2[gid]||G2.single,","function h2guitar(gid,C,na){\n  const G=arguments[3]||G2[gid]||G2.single,")
rep("  g.drawImage(rivalFrame(id,'stage',f),x-(R.W-R.ox),y-R.oy);","  g.drawImage(rivalFrame2(id,rivalPose(t,st)),x-(R.W-R.ox),y-R.oy);")
rep("visQ.push({t,type:'rnote'});","visQ.push({t,type:'rnote',f:n.f});")
rep("else if(e.type==='rnote'){ anim.rStrumUntil=perfNow()+0.18;","else if(e.type==='rnote'){ anim.rStrumUntil=perfNow()+0.18; try{ rivalNote(e.f); }catch(err){}")
rep("anim.cheerUntil=perfNow()+1.6; cheer(); try{ bandTips(); }catch(e){}","anim.cheerUntil=perfNow()+1.6; cheer(); try{ bandTips(); rivalMood(-1); }catch(e){}")
rep("  if(!res.perfect){\n    const s=state.answer[res.firstWrong].s;","  if(!res.perfect){ try{ rivalMood(1); }catch(e){}\n    const s=state.answer[res.firstWrong].s;")
rep("function bandBpm(){ return hasSeat('rosa')?8:0; }","function bandBpm(){ return (hasSeat('rosa')?8:0)+(rivalHas('rosa')?6:0); }")
rep("function bandWindow(){ return hasSeat('lou')?1.3:1; }","function bandWindow(){ return (hasSeat('lou')?1.3:1)*(rivalHas('lou')?0.75:1); }")
rep("function bandHype(){ return hasSeat('tam')?-1:0; }","function bandHype(){ return (hasSeat('tam')?-1:0)+(rivalHas('tam')?-1:0); }")
rep("if(hasSeat('lou')) state.replays=Math.max(0,state.replays-1); if(hasSeat('fay')) state.replays++;","if(hasSeat('lou')) state.replays=Math.max(0,state.replays-1); if(hasSeat('fay')) state.replays++; if(rivalHas('hale')) state.replays=Math.max(0,state.replays-1);")
rep("if(phase!=='answer'&&k==='comp'&&state.screen==='duel'&&hasSeat('jo')) v=Math.max(v,0.95);","if(phase!=='answer'&&k==='comp'&&state.screen==='duel'&&(hasSeat('jo')||rivalHas('jo'))) v=Math.max(v,0.95);")
rep("const g=grooveBuses(), L=g.L, e=i%8, bar=Math.floor(i/8), r=tr.root, sw=S.swing||0.5;","const g=grooveBuses(), L=g.L, e=i%8, bar=Math.floor(i/8), r=tr.root+((state.screen==='duel'&&g.phase!=='answer'&&rivalHas('dee'))?5:0), sw=S.swing||0.5;")
rep("try{ if(n==='duel'&&VEN().rowdy) startRowdy(); else stopRowdy(); }catch(e){}","try{ if(n==='duel'&&(VEN().rowdy||rivalHas('brass'))) startRowdy(); else stopRowdy(); }catch(e){}")
rep("setTempo(V.bpm+bandBpm());\n  buildBg(V);","try{ pickRivalBand(); if(RIVAL_VEC[V.id]) rivalWarm(V.id); }catch(e){}\n  setTempo(V.bpm+bandBpm());\n  buildBg(V);")
i=t.find('function showVenueCard'); j=t.find("$('vcGo').onclick",i); assert i>0 and j>i
t=t[:j]+"try{ pickRivalBand(); const vr=$('modalCard').querySelector('.vrival'); if(vr) vr.insertAdjacentHTML('afterend',rivalBandHTML()); }catch(e){}\n    "+t[j:]
rep("function maybeRecruit(force){ if(!state.lineup) state.lineup=[]; if(state.lineup.length>=vanSeats()) return;",
    "function maybeRecruit(force){ if(!state.lineup) state.lineup=[]; if(state.lineup.length>=vanSeats()) return; const poach=(state.rivalBand||[]).filter(id=>state.lineup.indexOf(id)<0); if(poach.length) force=true;")
rep("const pool=Object.keys(MEMBERS).filter(id=>MEMBERS[id].kind==='band'&&state.lineup.indexOf(id)<0); if(!pool.length) return;",
    "const pool=poach.length?poach:Object.keys(MEMBERS).filter(id=>MEMBERS[id].kind==='band'&&state.lineup.indexOf(id)<0); if(!pool.length) return;")
rep("M.role.charAt(0)+M.role.slice(1).toLowerCase()+'. Wants to join you for the rest of this tour.</div>'",
    "(poach.length?'Played '+M.role.toLowerCase()+' for '+VEN().rival+' tonight, and liked what they heard. Wants to switch vans for the rest of this tour.':M.role.charAt(0)+M.role.slice(1).toLowerCase()+'. Wants to join you for the rest of this tour.')+'</div>'")
css="""
.vband{display:flex;flex-direction:column;gap:1px;margin:4px 0 2px;font-family:var(--body);font-size:12px;line-height:1.25;color:var(--ink)}
.vband b{font-family:var(--ui);font-weight:normal;font-size:14px;color:var(--amber)} .vband i{font-style:normal;color:var(--ink-dim)}
</style>"""
k=t.rfind('</style>'); t=t[:k]+css+t[k+len('</style>'):]
t=t.replace("window.__fb={MEMBERS,","window.__fb={rPNG:(id,q)=>rivalFrame2(id,q||{}).toDataURL(),RIVAL_VEC,pickRivalBand:()=>pickRivalBand(),MEMBERS,",1)
open(p,'w',encoding='utf-8').write(t); print('ok')
