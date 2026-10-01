# Gemini standing callers -> rig body sprites. Keys the background, erases the hanging arms (OpenCV Telea inpaint inside an automatic arm area), scales the figure to the height
# of the old vector caller, brightens +10%, quantizes, and records the feet and shoulder points. Overrides per caller are in OV.
# usage: python3 tests/proccaller.py [ids]  (reads art/gemini_test/callers/<id>_body.png and /tmp/.../rival_old.json written by the hook run)  ;  --embed writes CALLER_SRC/CALLER_META in index.html
import sys,json,os,glob,base64
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import cv2
OLD=json.load(open(os.environ.get('RIVAL_OLD','/tmp/claude-0/-home-user-Fretbound/06db394c-e65b-5e2f-91cd-5e32ab269560/scratchpad/rival_old.json')))
# per-caller tweaks: sh = shoulder row as a fraction of figure height, cx = torso centre offset (fraction of height), aw = arm half width, ye = hand end row fraction, none = leave the arms (no distinct arms)
OV={'sebene':{'cx':0.15,'sh':0.34},'outback':{'sh':0.52,'ye':0.80,'aw':0.09},'lanai':{'sh':0.36,'ye':0.70},'mess':{'sh':0.36,'ye':0.62}}
def key(im):
    a=np.asarray(im.convert('RGB')).astype(int); bg=np.median(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]),axis=0)
    near=np.abs(a-bg).sum(axis=2)<150; mag=((a[:,:,0]-a[:,:,1])>70)&((a[:,:,2]-a[:,:,1])>35)&(a[:,:,0]>110)
    lab,n=ndi.label(near|mag); edge=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0); fg=~np.isin(lab,list(edge)); fg=ndi.binary_fill_holes(fg)&~mag
    fg=ndi.binary_opening(fg,iterations=1); lab,n=ndi.label(fg); sz=ndi.sum(fg,lab,range(1,n+1)); keep=[i+1 for i in range(n) if sz[i]>0.02*sz.max()]
    return np.isin(lab,keep),a.astype(np.uint8)
def build(i,bright=1.10,dump=False):
    o=OV.get(i,{}); fg,a=key(Image.open(f'art/gemini_test/callers/{i}_body.jpg')); H,W=fg.shape
    ys,xs=np.where(fg); x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1; h=y1-y0
    sy=int(y0+o.get('sh',0.30)*h); ye=int(y0+o.get('ye',0.60)*h)
    row=np.where(fg[int(y0+0.45*h)])[0]; q1,q3=np.percentile(row,[25,75]); cx=int((q1+q3)/2+o.get('cx',0)*h)
    aw=int(o.get('aw',0.075)*h); res=a.copy()
    if not o.get('none'):
        m=np.zeros((H,W),np.uint8); m[sy:ye,cx-aw:cx+aw]=255; m=cv2.dilate(m,np.ones((3,3),np.uint8))
        idx=ndi.distance_transform_edt(~fg,return_distances=False,return_indices=True); src=a[idx[0],idx[1]]
        res=cv2.inpaint(src,m,10,cv2.INPAINT_TELEA)
    th=OLD[i]['bot']-OLD[i]['top']+1; s=th/h
    rgba=np.dstack([res,(fg*255).astype(np.uint8)]); c=Image.fromarray(rgba).crop((x0,y0,x1,y1)); nw,nh=max(1,round(c.width*s)),th
    c=c.resize((nw,nh),Image.LANCZOS); b=np.asarray(c).copy(); al=b[:,:,3]>140
    rgb=np.clip(b[:,:,:3].astype(float)*bright,0,255).astype(np.uint8)
    q=Image.fromarray(rgb).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    out=Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8)); os.makedirs('art/callers',exist_ok=True); out.save(f'art/callers/{i}_body.png',optimize=True)
    yl,xl=np.where(al); low=yl>yl.max()-max(3,int(nh*0.08)); fx=int(np.median(xl[low])); fy=int(yl.max()+1)
    sh_y=round((sy-y0)*s,1); sx=round((cx-x0)*s,1); d=round(0.075*th,1)
    meta=dict(w=nw,h=nh,fx=fx,fy=fy,sy=sh_y,s1=[sx+d,sh_y],s2=[sx-d,sh_y])
    json.dump(meta,open(f'art/callers/{i}_body.json','w')); print(i,meta['w'],meta['h'],os.path.getsize(f'art/callers/{i}_body.png')//1024,'KB'); return out
def embed(path='index.html'):
    ids=sorted(os.path.basename(f)[:-5].replace('_body','') for f in glob.glob('art/callers/*_body.json'))
    src={i:'data:image/png;base64,'+base64.b64encode(open(f'art/callers/{i}_body.png','rb').read()).decode() for i in ids}; meta={i:json.load(open(f'art/callers/{i}_body.json')) for i in ids}
    s=open(path,encoding='utf-8').read(); a=s.index('/*CALLERS:BEGIN*/'); b=s.index('/*CALLERS:END*/')+len('/*CALLERS:END*/')
    open(path,'w',encoding='utf-8').write(s[:a]+'/*CALLERS:BEGIN*/\nconst CALLER_SRC='+json.dumps(src,separators=(',',':'))+', CALLER_META='+json.dumps(meta,separators=(',',':'))+';\n/*CALLERS:END*/'+s[b:]); print('embedded',len(ids))
if __name__=='__main__':
    if '--embed' in sys.argv: embed()
    else:
        for i in [x for x in sys.argv[1:]] or [os.path.basename(f)[:-9] for f in sorted(glob.glob('art/gemini_test/callers/*_body.jpg'))]: build(i)
