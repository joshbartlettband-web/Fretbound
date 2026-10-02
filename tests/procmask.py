# Land/sky mask for a title plate (same logic as tests/procfg.py, one plate at a time). usage: python3 tests/procmask.py ID [--check]
import sys,numpy as np
from collections import deque
from PIL import Image
T=26
def masks(a):
    H,W,_=a.shape; B=320; nb=W//B; S=np.zeros((H,nb,3))
    for k in range(nb): S[0,k]=np.median(a[0,k*B:(k+1)*B],axis=0)
    for y in range(1,H):
        for k in range(nb):
            seg=a[y,k*B:(k+1)*B]; d=np.abs(seg-S[y-1,k]).max(axis=1); c=seg[d<36]
            S[y,k]=np.median(c,axis=0) if len(c)>=0.3*B else S[y-1,k]
    xs=(np.arange(W)+0.5)/B-0.5; k0=np.clip(np.floor(xs).astype(int),0,nb-1); k1=np.clip(k0+1,0,nb-1); f=np.clip(xs-np.floor(xs),0,1)[None,:,None]
    SK=S[:,k0]*(1-f)+S[:,k1]*f
    sky=np.abs(a-SK).max(axis=2)<T; sky[H-2:,:]=False
    fg=np.zeros((H,W),bool); q=deque()
    for x in range(W):
        if not sky[H-1,x]: fg[H-1,x]=True; q.append((H-1,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((-1,0),(0,1),(0,-1),(1,0)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and not fg[ny,nx] and not sky[ny,nx]: fg[ny,nx]=True; q.append((ny,nx))
    return sky,fg
def mask_for(cid):
    im=Image.open(f'art/plates/{cid}.png').convert('RGB'); a=np.asarray(im).astype(float)
    p=np.pad(a,((2,2),(2,2),(0,0)),mode='edge'); b=sum(p[dy:dy+a.shape[0],dx:dx+a.shape[1]] for dy in range(5) for dx in range(5))/25.0
    return masks(b)[1]
if __name__=='__main__':
    cid=sys.argv[1]; fg=mask_for(cid)
    if '--check' in sys.argv:
        old=np.asarray(Image.open(f'art/plates/orig/{cid}_mask.png').convert('L'))>=128
        print(cid,'agreement with the existing mask (unshifted plate):',round((old==fg).mean()*100,2),'%')
    else:
        Image.fromarray((fg*255).astype(np.uint8)).convert('1').save(f'art/plates/{cid}_mask.png',optimize=True); print('wrote',cid,'mask, land',round(fg.mean()*100),'%')
