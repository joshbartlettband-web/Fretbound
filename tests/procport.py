import cv2, numpy as np, json, sys
from PIL import Image
MAP={'milonga':'15563.png','azmari':'15561.png','rio':'15562.png','ghat':'15579.jpg','paris':'15565.png','juke':'15558.png','outback':'15588.jpg','grotto':'15587.jpg','chicha':'15564.png','dunes':'15559.png','bali':'15585.jpg','sebene':'15560.png','lanai':'15586.jpg','cave':'15566.png','tide':'15557.png','pole':'15590.jpg','fay':'15578.jpg','tokyo':'15580.jpg','frost':'15567.png','mess':'15589.jpg'}
OUT=128; OUTLINE=(36,16,12)
def dewatermark(bgr):
    x0,y0,x1,y1=846,846,966,966; box=bgr[y0:y1,x0:x1].astype(np.int16)
    med=cv2.medianBlur(bgr[y0-40:y1+40,x0-40:x1+40],31)[40:-40,40:-40].astype(np.int16)
    diff=np.abs(box-med).sum(2); bright=box.sum(2)>med.sum(2)+30
    m=((diff>70)&bright).astype(np.uint8)*255; m=cv2.dilate(m,np.ones((5,5),np.uint8))
    full=np.zeros(bgr.shape[:2],np.uint8); full[y0:y1,x0:x1]=m
    return cv2.inpaint(bgr,full,6,cv2.INPAINT_TELEA), int((m>0).sum())
def key(rgb):
    R,G,B=[rgb[...,i].astype(np.int16) for i in range(3)]; mag=np.minimum(R,B)-G
    cand=((mag>100)&(R>140)&(B>140)).astype(np.uint8)
    n,lab=cv2.connectedComponents(cand,connectivity=4); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bg=np.isin(lab,list(edge))|((mag>165)&(R>195)&(B>195)&(G<95))   # enclosed pockets of pure background magenta too
    fr=cv2.dilate(bg.astype(np.uint8),np.ones((3,3),np.uint8)).astype(bool)&~bg&(mag>45)   # pink fringe hugging the cut
    return ~(bg|fr)
def process(src):
    bgr=cv2.imread('/mnt/user-data/uploads/'+src,cv2.IMREAD_COLOR); bgr,wm=dewatermark(bgr); rgb=cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB); a=key(rgb)
    H,W=a.shape; band=a[:,int(W*0.2):int(W*0.72)]; rows=np.where(band.sum(1)>=6)[0]; top=int(rows[0])
    reg=a[top:top+140,int(W*0.1):int(W*0.8)]; ys,xs=np.nonzero(reg); cx=int(xs.mean())+int(W*0.1)
    S=880; t0=top-44; l0=cx-int(0.5*S)
    rgba=np.dstack([rgb,(a*255).astype(np.uint8)]); canvas=np.zeros((S,S,4),np.uint8)
    sy0,sx0=max(0,t0),max(0,l0); sy1,sx1=min(H,t0+S),min(W,l0+S); canvas[sy0-t0:sy1-t0,sx0-l0:sx1-l0]=rgba[sy0:sy1,sx0:sx1]
    col=canvas[...,:3].copy(); col[canvas[...,3]==0]=OUTLINE
    small=np.asarray(Image.fromarray(col).resize((OUT,OUT),Image.LANCZOS)); al=np.asarray(Image.fromarray(canvas[...,3]).resize((OUT,OUT),Image.BOX))>110
    q=np.asarray(Image.fromarray(small).quantize(colors=48,method=Image.Quantize.MEDIANCUT).convert('RGB'))
    out=np.zeros((OUT,OUT,4),np.uint8); out[...,:3]=q; out[...,3]=al*255
    nb=np.zeros_like(al); nb[1:]|=al[:-1]; nb[:-1]|=al[1:]; nb[:,1:]|=al[:,:-1]; nb[:,:-1]|=al[:,1:]; ol=nb&~al; out[ol]=(*OUTLINE,255)
    return Image.fromarray(out), wm, top, cx
sheet=Image.new('RGB',(5*(OUT*2+6),4*(OUT*2+6)),(58,32,22)); rep={}
for k,(vid,f) in enumerate(MAP.items()):
    im,wm,top,cx=process(f); im.save(f'newport/{vid}.png'); rep[vid]=(wm,top,cx)
    bg=Image.new('RGBA',im.size,(58,32,22,255)); bg.alpha_composite(im); sheet.paste(bg.resize((OUT*2,OUT*2),Image.NEAREST).convert('RGB'),((k%5)*(OUT*2+6),(k//5)*(OUT*2+6)))
sheet.save('newport_sheet.png'); print(rep)
