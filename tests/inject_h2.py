import sys
src=sys.argv[1]; dst=sys.argv[2]
s=open(src,encoding='utf-8').read(); h=open('/home/claude/hero2.js',encoding='utf-8').read()
a='// stage drawing: pick a cached frame, then add the few live details\nfunction drawHero('
assert s.count(a)==1
s=s.replace(a,h+'\n'+a,1)
b='window.__fb={heroPNG:'
assert s.count(b)==1
s=s.replace(b,"window.__fb={h2PNG:(cid,q)=>heroFrame2(cid,q||{}).toDataURL(),heroPNG:",1)
open(dst,'w',encoding='utf-8').write(s); print('injected',len(s))
