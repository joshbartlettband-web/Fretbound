# v1.86: merge an atlas_edit.py result into the original atlas: register each edited pose to the original (a few px of drift), then take the
# edited pixels only where the edit really changed something (the guitar), despill the green key. No Gemini calls.
# usage: python3 atlas_merge.py ID OUTFILE DIR [DIR ...]   -> OUTFILE. For each pose it takes the candidate (from any DIR) that lines up best and
# really changed the guitar; when the edit moved the body too (score over WHOLE) it takes the whole edited figure instead of a merge.
import sys,json,numpy as np
from PIL import Image
from scipy import ndimage as ndi
import os; cid,outfile,dirs=sys.argv[1],sys.argv[2],sys.argv[3:]; WHOLE=float(os.environ.get("WHOLE",80))   # WHOLE=999: never take a whole edited figure (faceless characters)
A=np.asarray(Image.open(f'poses_master/{cid}_atlas.png').convert('RGBA')).astype(int); M=json.load(open(f'../poses/{cid}_meta.json')); cw,ch=M['cw'],M['ch']
W,H=1664,936; S=min(5,W//(cw*4),H//ch); res=A.copy()   # S fits four cells on the canvas, as in atlas_edit.py
cand={}; OLDG=np.zeros(A.shape[:2],bool)
for out in dirs:
  for g in range(4):
    if not os.path.exists(f'{out}/g{g}_out.png'): continue   # a re-run of only some groups
    e=np.asarray(Image.open(f'{out}/g{g}_out.png').convert('RGB')).astype(int)
    ox,oy=(W-cw*4*S)//2,(H-ch*S)//2
    for k in range(4):
        i=g*4+k
        x0,y0=(i%8)*cw,(i//8)*ch; o=A[y0:y0+ch,x0:x0+cw]; oa=o[:,:,3]>140
        best=None
        def cands():
            for dy in range(-40,41,4):
                for dx in range(-40,41,4): yield dx,dy
        def score(dx,dy):
            X,Y=ox+(k*cw)*S+dx,oy+dy
            if X<0 or Y<0 or X+cw*S>W or Y+ch*S>H: return None
            blk=e[Y:Y+ch*S,X:X+cw*S].reshape(ch,S,cw,S,3); small=np.median(blk.transpose(0,2,1,3,4).reshape(ch,cw,S*S,3),axis=2)
            sp=small[...,1]-np.maximum(small[...,0],small[...,2]); bgk=(small[...,1]>150)&(small[...,0]<130)&(small[...,2]<130); small[...,1]-=np.where((sp>0)&~bgk,sp,0); d=np.abs(small-o[:,:,:3]).sum(2); return (np.median(d[oa]),dx,dy,small)   # median per block keeps pixel edges sharp; green spill off dark and edge pixels
        for dx,dy in cands():
            r_=score(dx,dy)
            if r_ and (best is None or r_[0]<best[0]): best=r_
        bx,by=best[1],best[2]
        for dy in range(by-3,by+4):
            for dx in range(bx-3,bx+4):
                r_=score(dx,dy)
                if r_ and r_[0]<best[0]: best=r_
        for _ in []:
            for dx in []:
                pass
        sc,dx,dy,small=best
        r,gg,b=small[...,0],small[...,1],small[...,2]; green=(gg-np.maximum(r,b)>45)
        al=~green
        d=np.abs(small-o[:,:,:3]).sum(2); chg=((d>110)&al&oa)|(al&~oa)
        chg=ndi.binary_opening(chg,iterations=1); lab,n=ndi.label(chg)
        if n: sz=ndi.sum(chg,lab,range(1,n+1)); chg=np.isin(lab,[j+1 for j,v in enumerate(sz) if v>=20])
        chg=ndi.binary_closing(chg,iterations=2)&(al|oa)
        # where the old guitar was and the edit made it background, clear it
        gone=oa&~al&ndi.binary_dilation(chg,iterations=3)
        OLDG[y0:y0+ch,x0:x0+cw]|=chg&oa   # where the old guitar was: its colours are left out of the palette snap below
        if sc>WHOLE: px,alpha=small,al&ndi.binary_opening(al,iterations=1)
        else: px=np.where(chg[...,None],small,o[:,:,:3]); alpha=np.where(chg,al,oa)&~gone
        ok=chg.sum()>150; key=(0 if ok else 1, 0 if sc<=WHOLE else 1, sc)
        if i not in cand or key<cand[i][0]: cand[i]=(key,px,alpha,out)
        print(out,i,'shift',dx,dy,'score',round(sc,1),'changed px',int(chg.sum()))
for i,(key,px,alpha,out) in sorted(cand.items()):
    x0,y0=(i%8)*cw,(i//8)*ch; res[y0:y0+ch,x0:x0+cw,:3]=px; res[y0:y0+ch,x0:x0+cw,3]=alpha*255; print('pose',i,'from',out,key)
# snap colours that are close to the character's own palette back onto it (Gemini paints blacks and skin a little differently); new guitar colours stay
pal=np.unique(A[(A[:,:,3]>140)&~ndi.binary_dilation(OLDG,iterations=1)][:,:3],axis=0).astype(float); flat=res[:,:,:3].reshape(-1,3).astype(float)
for c0 in range(0,len(flat),20000):
    blk=flat[c0:c0+20000]; d=((blk[:,None,:]-pal[None,:,:])**2).sum(2); j=d.argmin(1); near=d[np.arange(len(blk)),j]<float(os.environ.get('SNAP',38))**2
    blk[near]=pal[j[near]]
res[:,:,:3]=flat.reshape(res.shape[0],res.shape[1],3)
if os.environ.get('NOGREEN'): r_,g_,b_=res[...,0],res[...,1],res[...,2]; res[...,1]=np.minimum(g_,np.maximum(r_,b_)+4)   # characters with no green of their own: no green cast anywhere
im=res.astype(np.uint8); al=im[:,:,3]>140
q=Image.fromarray(im[:,:,:3]).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
Image.fromarray(np.dstack([np.asarray(q),(al*255).astype(np.uint8)])).save(outfile); print('saved')
