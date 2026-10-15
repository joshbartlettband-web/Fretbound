# Build the "Fretbound Stage Test" artifact from index.html when the page is over the 16 MB artifact limit.
# The game stays one file; only the published copy moves its biggest embedded-art blocks into side files (art_<name>.js) that load
# before the game script, each as `window.__ART_<NAME>={...};`, and the game's `const NAME={...}` becomes `const NAME=window.__ART_<NAME>;`.
# usage: python3 tests/dev/artifact_split.py OUTDIR [NAME ...]   (default: STAGE_PLATE_SRC POSE_SRC)   -> OUTDIR/index.html + OUTDIR/art_*.js
import os,sys,re
REPO=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
out=sys.argv[1]; names=sys.argv[2:] or ['STAGE_PLATE_SRC','POSE_SRC']; os.makedirs(out,exist_ok=True)
s=open(os.path.join(REPO,'index.html'),encoding='utf-8').read()
def literal_end(s,i):
    # i at an opening { or [: return the index just past its matching close, skipping strings
    depth=0; q=None; k=i
    while k<len(s):
        c=s[k]
        if q:
            if c=='\\': k+=2; continue
            if c==q: q=None
        elif c in '"\'`': q=c
        elif c in '{[': depth+=1
        elif c in '}]':
            depth-=1
            if depth==0: return k+1
        k+=1
    raise ValueError('unbalanced')
tags=[]
for n in names:
    m=re.search(r'\bconst '+n+r'\s*=\s*([\{\[])',s); assert m,n
    a=m.start(1); b=literal_end(s,a); lit=s[a:b]
    fn=f'art_{n.lower()}.js'; open(os.path.join(out,fn),'w',encoding='utf-8').write(f'window.__ART_{n}={lit};\n')
    s=s[:a]+f'window.__ART_{n}'+s[b:]; tags.append(f'<script src="{fn}"></script>')
    print(n,round(len(lit)/1e6,2),'MB ->',fn)
i=s.index('<script>'); s=s[:i]+'\n'.join(tags)+'\n'+s[i:]
t=re.search(r'<title>[^<]*</title>',s).group(0); s=s.replace(t,'<title>Fretbound Stage Test</title>',1)
open(os.path.join(out,'index.html'),'w',encoding='utf-8').write(s); print('page',round(len(s.encode())/1e6,2),'MB')
