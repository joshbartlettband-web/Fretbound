# v1.90 pilot: in-between frames for painted pose sprites, no image model. Optical flow between two poses (both directions),
# warp each halfway toward the other, blend, then snap every pixel to the character's own palette and harden the alpha,
# so the new frame stays crisp pixel art with no new colours. Good for small moves (strums, nods, fret slides); big pose changes smear.
# usage: python3 tests/tween.py ID POSE_A POSE_B N OUTDIR   (pose names from art/poses/ID_meta.json; N in-betweens)
#        -> OUTDIR/ID_A_B.png (strip: A, the N tweens, B), OUTDIR/ID_A_B.gif (before vs after loop)
import sys,os,json
import numpy as np, cv2
from PIL import Image
def cells(cid):
    m=json.load(open(f'art/poses/{cid}_meta.json')); cw,ch=m['cw'],m['ch']; a=np.asarray(Image.open(f'art/gemini_test/poses_master/{cid}_atlas.png').convert('RGBA'))
    return m,[a[(i//8)*ch:(i//8)*ch+ch,(i%8)*cw:(i%8)*cw+cw].copy() for i in range(16)]
def flow(a,b,S):
    # flow on the upscaled grey image with the background filled from the figure's mean, so edges carry the motion
    def prep(x):
        g=cv2.cvtColor(x[:,:,:3],cv2.COLOR_RGB2GRAY).astype(np.float32); al=x[:,:,3]>140; g[~al]=0; return cv2.resize(g,None,fx=S,fy=S,interpolation=cv2.INTER_NEAREST).astype(np.uint8)
    dis=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_ULTRAFAST); dis.setFinestScale(0); dis.setPatchSize(8); dis.setPatchStride(2)
    return dis.calc(prep(a),prep(b),None)
def warp(img,fl,t,S):
    # backward warp: the pixel at p in the tween comes from p - t*flow in the source
    h,w=fl.shape[:2]; gx,gy=np.meshgrid(np.arange(w),np.arange(h)); mx=(gx-t*fl[...,0]).astype(np.float32); my=(gy-t*fl[...,1]).astype(np.float32)
    big=cv2.resize(img,None,fx=S,fy=S,interpolation=cv2.INTER_NEAREST); return cv2.remap(big,mx,my,cv2.INTER_NEAREST,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
def tween(a,b,t,pal,S=4):
    fab=flow(a,b,S); fba=flow(b,a,S)
    wa=warp(a,fab,t,S).astype(float); wb=warp(b,fba,1-t,S).astype(float)
    mix=wa*(1-t)+wb*t
    small=cv2.resize(mix.astype(np.float32),(a.shape[1],a.shape[0]),interpolation=cv2.INTER_AREA)
    al=small[:,:,3]>110
    rgb=small[:,:,:3].reshape(-1,3); d=((rgb[:,None,:]-pal[None,:,:])**2).sum(2); snap=pal[d.argmin(1)].reshape(small.shape[0],small.shape[1],3)
    out=np.dstack([snap,al*255]).astype(np.uint8)
    # keep the dark outline: any figure pixel that touches the background and is dark in either pose stays the darkest palette colour
    return out
if __name__=='__main__':
    cid,pa,pb,n,od=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),sys.argv[5]; os.makedirs(od,exist_ok=True)
    m,C=cells(cid); A=C[m['names'].index(pa)]; B=C[m['names'].index(pb)]
    allpx=np.concatenate([c[c[:,:,3]>140][:,:3] for c in C]); pal=np.unique(allpx,axis=0).astype(float)
    frames=[A]+[tween(A,B,(k+1)/(n+1),pal) for k in range(n)]+[B]
    cw,ch=A.shape[1],A.shape[0]; strip=Image.new('RGBA',(cw*len(frames),ch),(40,40,60,255))
    for k,f in enumerate(frames): strip.alpha_composite(Image.fromarray(f),(k*cw,0))
    strip.resize((strip.width*3,strip.height*3),Image.NEAREST).save(f'{od}/{cid}_{pa}_{pb}.png')
    # a loop: left the old two-frame swap, right the tweened version, both at the same speed
    seq=frames+frames[-2:0:-1]; gif=[]
    for k in range(len(seq)*2):
        im=Image.new('RGBA',(cw*2+8,ch),(40,40,60,255)); old=A if (k//len(seq))%2==0 and (k%len(seq))<len(seq)//2 else B
        im.alpha_composite(Image.fromarray(A if (k%len(seq))<len(seq)//2 else B),(0,0)); im.alpha_composite(Image.fromarray(seq[k%len(seq)]),(cw+8,0))
        gif.append(im.resize((im.width*3,im.height*3),Image.NEAREST).convert('P',palette=Image.ADAPTIVE))
    gif[0].save(f'{od}/{cid}_{pa}_{pb}.gif',save_all=True,append_images=gif[1:],duration=70,loop=0,disposal=2)
    print('saved',len(frames),'frames')
