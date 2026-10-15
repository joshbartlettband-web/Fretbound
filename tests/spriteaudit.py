# Audit of the painted pose sets: colour consistency from pose to pose, guitar colour against the game's guitar, sprite against its portrait.
# usage (repo root): python3 tests/spriteaudit.py [id ...]      reads art/gemini_test/poses_master/<id>_atlas.png (ungraded), art/poses/<id>_meta.json, index.html (portraits)
import sys,os,json,re,base64,io,colorsys
import numpy as np
from PIL import Image
sys.path.insert(0,'art/gemini_test/sheets')
import chars
MASTER='art/gemini_test/poses_master'
def hist(rgb,a):                     # 12 hues x 3 saturations x 3 values over opaque, non-outline pixels (outline = very dark)
    r,g,b=[rgb[...,i]/255. for i in range(3)]; mx=np.maximum(np.maximum(r,g),b); mn=np.minimum(np.minimum(r,g),b); v=mx; s=np.where(mx>0,(mx-mn)/np.maximum(mx,1e-6),0)
    d=mx-mn+1e-9; h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))/6.
    m=(a>0)&(v>0.22)
    hb=np.minimum(11,(h*12).astype(int)); sb=np.minimum(2,(s*3).astype(int)); vb=np.minimum(2,(v*3).astype(int))
    H=np.zeros((12,3,3)); np.add.at(H,(hb[m],sb[m],vb[m]),1); return H/max(1,H.sum())
def inter(a,b): return float(np.minimum(a,b).sum())
def cells(path,meta):
    im=np.asarray(Image.open(path).convert('RGBA')); cw,ch=meta['cw'],meta['ch']; out=[]
    for i in range(meta['n']): r,c=divmod(i,8); out.append(im[r*ch:(r+1)*ch,c*cw:(c+1)*cw])
    return out
def guitar_cols(path):               # the guitar sprite's body colours: the commonest colours that are not outline or near-black
    im=Image.open(path).convert('RGBA'); a=np.asarray(im).reshape(-1,4); a=a[a[:,3]>0][:,:3]; a=a[a.max(axis=1)>70]
    q=(a//24)*24+12; u,c=np.unique(q,axis=0,return_counts=True); k=np.argsort(-c)[:4]; return [(u[i],c[i]/len(a)) for i in k]
def has_col(cell,col,tol=44):
    px=cell[cell[...,3]>0][:,:3].astype(int); return float((np.abs(px-col).sum(axis=1)<tol).mean()) if len(px) else 0
def lines(cell):                      # stray straight lines left from the sheet (a row or column of opaque pixels far longer than any limb)
    a=cell[...,3]>0; ch,cw=a.shape; rows=a.sum(axis=1); cols=a.sum(axis=0)
    hr=[y for y in range(ch) if rows[y]>=0.8*cw and a[y].sum()>0 and rows[max(0,y-6)]<0.8*cw]
    vc=[x for x in range(cw) if cols[x]>=0.6*ch and cols[max(0,x-4)]<0.3*ch and cols[min(cw-1,x+4)]<0.3*ch]
    return hr,vc
def feet_y(cell):
    a=cell[...,3]>0; ys=np.where(a.any(axis=1))[0]; return int(ys.max())
def portraits():
    s=open('index.html',encoding='utf-8').read(); P={}
    for name in ('RIVAL_PORT','MEMBER_PORT','PORTRAIT_ART'):
        for m in re.finditer(r'const '+name+r'=(\{.*?\});\n',s,re.S):
            try: d=json.loads(m.group(1)); P.update({k:v for k,v in d.items() if isinstance(v,str) and v.startswith('data:')})
            except Exception: pass
    return P
def main(ids):
    P=portraits(); rows=[]
    for cid in ids:
        mp=f'art/poses/{cid}_meta.json'; ap=f'{MASTER}/{cid}_atlas.png'
        if not (os.path.exists(mp) and os.path.exists(ap)): continue
        meta=json.load(open(mp)); C=cells(ap,meta); H=[hist(c[...,:3].astype(int),c[...,3]) for c in C]
        idle=H[0]; d=[1-inter(h,idle) for h in H]; A=np.mean(H[:8],axis=0); B=np.mean(H[8:],axis=0); dAB=1-inter(A,B)
        worst=int(np.argmax(d)); r=dict(id=cid,dAB=dAB,worst=meta['names'][worst],worstd=d[worst])
        fy=[feet_y(c) for c in C]; r['float']=[(meta['names'][i],fy[i]-fy[0]) for i in range(len(C)) if abs(fy[i]-fy[0])>=2 and meta['names'][i] not in ('slump','big_hit','cheer','flinch','showoff','lean_in')]
        r['lines']=[(meta['names'][i],)+tuple(lines(C[i])) for i in range(len(C)) if any(lines(C[i]))]
        g=chars.CH.get(cid,{}).get('guitar')
        if g and os.path.exists(g):
            gc=guitar_cols(g); r['gtr']=[min(has_col(C[i],c) for c,_ in gc[:2]) for i in range(len(C))]; r['gtrmin']=min(r['gtr']); r['gtrmax']=max(r['gtr'])
            r['gtrA']=float(np.mean(r['gtr'][:8])); r['gtrB']=float(np.mean(r['gtr'][8:]))
        if cid in P:
            pi=Image.open(io.BytesIO(base64.b64decode(P[cid].split(',')[1]))).convert('RGBA'); pa=np.asarray(pi); r['port']=inter(hist(pa[...,:3].astype(int),pa[...,3]),idle)
        rows.append(r)
    print(f"{'id':9s} {'A~B':>5s} {'worst pose':>14s} {'drift':>6s} {'gtr A':>6s} {'gtr B':>6s} {'portrait':>8s}")
    for r in rows: print(f"{r['id']:9s} {r['dAB']:5.2f} {r['worst']:>14s} {r['worstd']:6.2f} {r.get('gtrA',float('nan')):6.2f} {r.get('gtrB',float('nan')):6.2f} {r.get('port',float('nan')):8.2f}")
    print('\nstray lines:',[(r['id'],r['lines']) for r in rows if r['lines'] and r['id'] not in ('jo','lou','rosa','hale','brass')] or 'none')
    print('feet off the idle baseline (calm poses, 2 px or more):',[(r['id'],r['float']) for r in rows if r['float']] or 'none')
    return rows
if __name__=='__main__': main(sys.argv[1:] or sorted(chars.CH))
