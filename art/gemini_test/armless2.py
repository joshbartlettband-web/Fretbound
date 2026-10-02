# Remove the arms of the Gemini standing bodies for the rig (which draws its own arms). Every arm here hangs OUTSIDE the torso silhouette, so each polygon is simply
# deleted (made transparent); the cut edge gets a dark painted outline so the torso still has one.  Polygons are in ORIGINAL image coordinates (864x1184).
# usage (from art/gemini_test): python3 armless2.py [name ...] [--ov]  -> chars/<name>_armless_body.png (RGBA) ; --ov writes chars/<name>_ov.png with the polygons drawn
import sys,os,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
CUT={
'hermit':[[(225,380),(343,440),(350,744),(350,830),(255,925),(225,925)],[(537,640),(580,640),(580,830),(527,830),(527,700)]],
'luthier':[[(225,300),(343,300),(343,470),(343,800),(225,800)],[(545,380),(580,380),(580,800),(522,800),(522,440)]],
'monk':[[(225,300),(336,300),(336,560),(362,600),(374,660),(374,790),(250,840),(225,840)]],
'busker':[[(225,360),(343,360),(343,690),(366,700),(368,815),(225,825)],[(522,625),(580,625),(580,810),(522,810)]],
'carto':[[(225,400),(343,400),(343,700),(358,710),(358,830),(225,830)],[(526,640),(580,640),(580,820),(526,820)]],
}
OUTLINE=(30,18,12)
def fgmask(a):
    ai=a.astype(int); bgc=np.median(np.concatenate([ai[0],ai[-1],ai[:,0],ai[:,-1]]),axis=0)
    near=np.abs(ai-bgc).sum(axis=2)<150; magenta=((ai[:,:,0]-ai[:,:,1])>110)&((ai[:,:,2]-ai[:,:,1])>50)
    lab,n=ndi.label(near|magenta); edge=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0)
    fg=~np.isin(lab,list(edge)); fg=ndi.binary_fill_holes(fg)
    soft=((ai[:,:,0]-ai[:,:,1])>70)&((ai[:,:,2]-ai[:,:,1])>35)&(ai[:,:,0]>110)
    fg=ndi.binary_opening(fg&~soft,iterations=1); lab,n=ndi.label(fg); sz=ndi.sum(fg,lab,range(1,n+1)); return lab==(1+int(np.argmax(sz)))
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
def run(name,ov=False):
    im=Image.open(f'chars/{name}_body.jpg').convert('RGB'); a=np.asarray(im); H,W,_=a.shape
    cut=np.zeros((H,W),bool)
    for P in CUT[name]:
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(P,fill=255); cut|=np.asarray(m)>0
    if ov:
        o=im.copy(); d=ImageDraw.Draw(o)
        for P in CUT[name]: d.polygon(P,outline=(255,255,0))
        o.crop((150,60,760,1180)).save(f'chars/{name}_ov.png'); return
    fg=fgmask(a); cut=cut&~backstrip(cut,fg,30)
    keep=fg&~cut
    lab,n=ndi.label(keep); sz=ndi.sum(keep,lab,range(1,n+1)); keep=lab==(1+int(np.argmax(sz)))     # drop any stray bits the cut left behind
    rim=keep&ndi.binary_dilation(fg&cut,iterations=4)                                                 # the cut edge: a dark painted outline, 4 px
    out=a.copy(); out[rim]=OUTLINE
    Image.fromarray(np.dstack([out,keep*255]).astype(np.uint8)).save(f'chars/{name}_armless_body.png'); print('saved',name,int(keep.sum()))
if __name__=='__main__':
    ov='--ov' in sys.argv; names=[n for n in sys.argv[1:] if n!='--ov'] or list(CUT)
    for n in names: run(n,ov)
