# Remove the hanging arms and hands from the Gemini caller paintings (the rig draws its own arms).  Run from the repo root:
#   python3 art/gemini_test/armless_callers.py [id ...] [--ov]   -> art/gemini_test/callers/<id>_armless.png (RGBA, full size 864x1184); --ov writes <id>_ov.png with the shapes drawn
# Shapes are in ORIGINAL picture coordinates.  'cut': the arm sticks out past the body, so it is made transparent (and the new edge gets a dark outline).
# 'fill': the arm lies over the body, so it is painted out from the nearest body pixels (OpenCV Telea).  Then run tests/proccaller.py <id> and --embed.
import sys,os,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
import cv2
C,F='cut','fill'
SH={
'spur':[(C,[(215,350),(330,350),(332,690),(362,700),(362,850),(215,850)])],
'tide':[(F,[(378,505),(452,505),(452,700),(378,700)])],
'juke':[(C,[(235,340),(316,340),(316,700),(342,715),(342,820),(235,820)]),(C,[(494,360),(575,360),(575,820),(488,820),(488,715),(494,700)])],
'dunes':[(C,[(285,360),(356,360),(358,690),(400,705),(400,800),(285,800)])],
'sebene':[(F,[(385,400),(480,405),(478,690),(520,700),(520,800),(405,800),(388,700)])],
'azmari':[(F,[(215,755),(455,755),(455,960),(215,960)])],
'rio':[(F,[(345,630),(425,630),(425,790),(345,790)])],
'milonga':[(F,[(293,650),(392,650),(392,835),(293,835)])],
'chicha':[(F,[(235,635),(340,635),(340,780),(235,780)]),(C,[(512,635),(600,635),(600,780),(512,780)])],
'paris':[(F,[(335,625),(440,625),(440,850),(335,850)])],
'cave':[(C,[(300,625),(345,625),(345,725),(300,725)]),(F,[(335,690),(415,690),(415,870),(335,870)])],
'frost':[(F,[(310,665),(400,665),(400,795),(310,795)]),(C,[(505,660),(580,660),(580,800),(505,800)])],
'tokyo':[(F,[(380,670),(455,670),(455,795),(380,795)]),(C,[(585,670),(660,670),(660,795),(585,795)])],
'ghat':[(F,[(240,690),(350,690),(350,860),(240,860)]),(C,[(538,690),(590,690),(590,840),(538,840)])],
'bali':[(C,[(300,380),(372,380),(374,690),(300,800)]),(F,[(360,670),(415,670),(415,790),(360,790)])],
'lanai':[(F,[(200,610),(325,610),(325,930),(200,930)]),(C,[(625,640),(710,640),(710,930),(625,930)])],
'outback':[(C,[(200,560),(300,560),(300,780),(200,780)]),(F,[(215,780),(335,780),(335,905),(215,905)]),(C,[(520,570),(610,570),(610,780),(520,780)]),(F,[(500,780),(590,780),(590,880),(500,880)])],
'grotto':[(F,[(335,650),(420,650),(420,790),(335,790)])],
'aurora':[(F,[(300,590),(375,590),(375,700),(300,700)]),(C,[(505,590),(580,590),(580,710),(505,710)])],
'pole':[(F,[(285,720),(395,720),(395,850),(285,850)])],
}
OUTLINE=(30,18,12)
def key(a):
    ai=a.astype(int); bg=np.median(np.concatenate([ai[0],ai[-1],ai[:,0],ai[:,-1]]),axis=0)
    near=np.abs(ai-bg).sum(axis=2)<150; mag=((ai[:,:,0]-ai[:,:,1])>70)&((ai[:,:,2]-ai[:,:,1])>35)&(ai[:,:,0]>110)
    lab,n=ndi.label(near|mag); edge=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0); fg=~np.isin(lab,list(edge)); fg=ndi.binary_fill_holes(fg)&~mag
    fg=ndi.binary_opening(fg,iterations=1); lab,n=ndi.label(fg); sz=ndi.sum(fg,lab,range(1,n+1)); keep=[i+1 for i in range(n) if sz[i]>0.02*sz.max()]
    return np.isin(lab,keep)
def backstrip(cut,fg,W0):
    """The painted back arm hangs against the back of the torso.  Cutting all of it flattens the back, so keep a strip along the torso's edge, deepest at the shoulder and thinning to nothing by mid-arm
    (only for cuts on the back side, the left: the paintings face right)."""
    ys,xs=np.where(fg); cx=(xs.min()+xs.max())/2; keep=np.zeros_like(cut)
    rows=np.where(cut.any(axis=1))[0]
    for P in [rows]:
        pass
    lab,n=ndi.label(cut)
    for i in range(1,n+1):
        m=lab==i; yy,xx=np.where(m)
        if xx.mean()>cx: continue                      # the front side: hands in front of the body, no strip
        y0,y1=yy.min(),yy.max()
        for y in range(y0,y1+1):
            w=int(W0*max(0.0,1-(y-y0)/(0.5*(y1-y0))))
            if w<1: continue
            xr=xx[yy==y].max(); keep[y,xr-w+1:xr+1]=True
    return keep
def run(i,ov=False):
    im=Image.open(f'art/gemini_test/callers/{i}_body.jpg').convert('RGB'); a=np.asarray(im).copy(); H,W,_=a.shape
    def mask(P):
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(P,fill=255); return np.asarray(m)>0
    if ov:
        o=im.copy(); d=ImageDraw.Draw(o)
        for mode,P in SH[i]: d.polygon(P,outline=(255,255,0) if mode==C else (0,255,255))
        o.save(f'art/gemini_test/callers/{i}_ov.png'); return
    fg=key(a); cut=np.zeros((H,W),bool); fill=np.zeros((H,W),bool)
    for mode,P in SH[i]:
        if mode==C: cut|=mask(P)
        else: fill|=mask(P)
    # fill: paint from the nearest body pixel outside the shapes
    # sample only the inside of the body (3 px in from the edge), or the magenta fringe round the figure bleeds into the filled patch
    ok=ndi.binary_erosion(fg&~fill&~cut,iterations=3); idx=ndi.distance_transform_edt(~ok,return_distances=False,return_indices=True); src=a[idx[0],idx[1]]
    res=cv2.inpaint(src,(fill&fg).astype(np.uint8)*255,10,cv2.INPAINT_TELEA); a2=np.where((fill&fg)[...,None],res,a)
    cut=cut&~backstrip(cut,fg,26)
    keep=fg&~cut; lab,n=ndi.label(keep); sz=ndi.sum(keep,lab,range(1,n+1)); keep=lab==(1+int(np.argmax(sz)))
    rim=keep&ndi.binary_dilation(fg&cut,iterations=4); a2[rim]=OUTLINE
    Image.fromarray(np.dstack([a2,keep*255]).astype(np.uint8)).save(f'art/gemini_test/callers/{i}_armless.png'); print('saved',i)
    # the colour of the painted arm that was taken away (median of its lit pixels): the rig's sleeves are drawn in it, so a new forearm matches the clothes
    arm=(cut|fill)&fg&(a.sum(axis=2)>150); px=a[arm]
    if len(px)>50:
        c=np.median(px,axis=0); import json; f='art/gemini_test/callers/armcols.json'; J=json.load(open(f)) if os.path.exists(f) else {}
        J[i]=['#%02x%02x%02x'%tuple(int(v) for v in c),'#%02x%02x%02x'%tuple(int(v*0.78) for v in c)]; json.dump(J,open(f,'w'))
if __name__=='__main__':
    ov='--ov' in sys.argv; ids=[x for x in sys.argv[1:] if x!='--ov'] or list(SH)
    for i in ids: run(i,ov)
