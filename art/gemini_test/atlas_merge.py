# v1.86: merge an atlas_edit.py result into the original atlas: register each edited pose to the original (a few px of drift), then take the
# edited pixels only where the edit really changed something (the guitar), despill the green key. No Gemini calls.
# usage: python3 atlas_merge.py ID OUTFILE DIR [DIR ...]   -> OUTFILE. For each pose it takes the candidate (from any DIR) that lines up best and
# really changed the guitar; when the edit moved the body too (score over WHOLE) it takes the whole edited figure instead of a merge.
import sys,json,numpy as np
from PIL import Image
from scipy import ndimage as ndi
cid,outfile,dirs=sys.argv[1],sys.argv[2],sys.argv[3:]; WHOLE=80
A=np.asarray(Image.open(f'poses_master/{cid}_atlas.png').convert('RGBA')).astype(int); M=json.load(open(f'../poses/{cid}_meta.json')); cw,ch=M['cw'],M['ch']
S=5; W,H=1664,936; res=A.copy()
cand={}
for out in dirs:
  for g in range(4):
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
            small=e[Y:Y+ch*S,X:X+cw*S].reshape(ch,S,cw,S,3).mean((1,3)); d=np.abs(small-o[:,:,:3]).sum(2); return (np.median(d[oa]),dx,dy,small)
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
        if sc>WHOLE: px,alpha=small,al&ndi.binary_opening(al,iterations=1)
        else: px=np.where(chg[...,None],small,o[:,:,:3]); alpha=np.where(chg,al,oa)&~gone
        ok=chg.sum()>150; key=(0 if ok else 1, 0 if sc<=WHOLE else 1, sc)
        if i not in cand or key<cand[i][0]: cand[i]=(key,px,alpha,out)
        print(out,i,'shift',dx,dy,'score',round(sc,1),'changed px',int(chg.sum()))
for i,(key,px,alpha,out) in sorted(cand.items()):
    x0,y0=(i%8)*cw,(i//8)*ch; res[y0:y0+ch,x0:x0+cw,:3]=px; res[y0:y0+ch,x0:x0+cw,3]=alpha*255; print('pose',i,'from',out,key)
im=res.astype(np.uint8); al=im[:,:,3]>140
q=Image.fromarray(im[:,:,:3]).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
Image.fromarray(np.dstack([np.asarray(q),(al*255).astype(np.uint8)])).save(outfile); print('saved')
