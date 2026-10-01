# landmark layer for each plate.
# The skies are horizontal bands, so each row's sky colour is carried down from the row above; a pixel that differs clearly
# from its row's sky colour is not open sky. Landmarks are the non-sky pixels joined to the horizon; the rest (sun, moon,
# painted clouds, aurora, birds) stay behind the drifting clouds.
import numpy as np, os
from PIL import Image
from collections import deque
T=26
def masks(a):
    # the sky colour is tracked per row in 40 px blocks, so skies that shade sideways (South America) work too
    H,W,_=a.shape; B=320; nb=W//B; S=np.zeros((H,nb,3))
    for k in range(nb): S[0,k]=np.median(a[0,k*B:(k+1)*B],axis=0)
    for y in range(1,H):
        for k in range(nb):
            seg=a[y,k*B:(k+1)*B]; d=np.abs(seg-S[y-1,k]).max(axis=1); c=seg[d<36]
            S[y,k]=np.median(c,axis=0) if len(c)>=0.3*B else S[y-1,k]
    xs=(np.arange(W)+0.5)/B-0.5; k0=np.clip(np.floor(xs).astype(int),0,nb-1); k1=np.clip(k0+1,0,nb-1); f=np.clip(xs-np.floor(xs),0,1)[None,:,None]
    SK=S[:,k0]*(1-f)+S[:,k1]*f
    sky=np.abs(a-SK).max(axis=2)<T
    sky[H-2:,:]=False
    fg=np.zeros((H,W),bool); q=deque()
    for x in range(W):
        if not sky[H-1,x]: fg[H-1,x]=True; q.append((H-1,x))
    while q:
        y,x=q.popleft()
        for dy,dx in ((-1,0),(0,1),(0,-1),(1,0)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and not fg[ny,nx] and not sky[ny,nx]: fg[ny,nx]=True; q.append((ny,nx))
    return sky,fg
sheet=Image.new('RGB',(2*644,4*228),'black')
for i,cid in enumerate(['na','af','sa','eu','as','oc','an']):
    im=Image.open(f'/home/claude/plates/{cid}.png').convert('RGB'); a=np.asarray(im).astype(float)
    p=np.pad(a,((2,2),(2,2),(0,0)),mode='edge'); b=sum(p[dy:dy+a.shape[0],dx:dx+a.shape[1]] for dy in range(5) for dx in range(5))/25.0
    sky,fg=masks(b)
    rgba=np.dstack([np.asarray(im),(fg*255).astype(np.uint8)]); Image.fromarray(rgba,'RGBA').save(f'/home/claude/plates/{cid}_fg.png',optimize=True)
    vis=np.asarray(im).copy(); vis[sky]=(vis[sky]*0.35+np.array([255,0,255])*0.65).astype(np.uint8); m=~sky&~fg; vis[m]=(vis[m]*0.4+np.array([0,255,255])*0.6).astype(np.uint8)
    sheet.paste(Image.fromarray(vis),((i%2)*644,(i//2)*228))
    print(cid,'sky',round(sky.mean()*100),'% | landmarks',round(fg.mean()*100),'% | sky objects',round(m.mean()*100),'% |',os.path.getsize(f'/home/claude/plates/{cid}_fg.png')//1024,'KB')
sheet.save('/home/claude/plates/mask_sheet.png')
