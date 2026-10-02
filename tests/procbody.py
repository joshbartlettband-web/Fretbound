# Armless painted body -> rig body sprite. The hand-erased body (art/gemini_test/chars/<name>_armless_body.png, 864x1184 source crop, see art/gemini_test/armless.py)
# is keyed, scaled so the figure is HEIGHT px tall, brightened (default +10%), quantized, and saved with the feet point and the two shoulder points.
# usage: python3 tests/procbody.py NAME [HEIGHT] [BRIGHT]    -> art/sprites/<name>_body.png + <name>_body.json ; add --embed NAME... to write the block in index.html
import sys,json,os,base64
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
OX,OY=200,330   # crop origin used by armless.py
# shoulder points in ORIGINAL image coordinates: fretting arm (front, right) and picking arm (back, left)
SH={'bard':dict(front=(530,418),back=(352,452)),'monk':dict(front=(470,400),back=(372,400)),'busker':dict(front=(490,420),back=(375,420)),'hermit':dict(front=(470,430),back=(372,440)),'luthier':dict(front=(510,450),back=(368,430)),'carto':dict(front=(490,450),back=(368,450))}   # back shoulders moved inside the torso when the hanging arms were cut away (armless2.py)
def build(name,HEIGHT=104,BRIGHT=1.10):
    im=Image.open(f'art/gemini_test/chars/{name}_armless_body.png').convert('RGBA'); ox,oy=(0,0) if im.size==(864,1184) else (OX,OY)
    full=Image.open(f'art/gemini_test/chars/{name}_body.jpg' if os.path.exists(f'art/gemini_test/chars/{name}_body.jpg') else f'art/gemini_test/chars/{name}_body.png').convert('RGBA')
    full.paste(im,(ox,oy)) if ox or oy else full.paste(im,(0,0)); f=np.asarray(full).astype(int)
    if (np.asarray(im)[0,:,3]==0).mean()>0.9:   # the eraser already wrote a clean transparent background
        fg=f[:,:,3]>0
    else:
        bg=np.median(np.concatenate([f[0],f[-1],f[:,0],f[:,-1]])[:,:3],axis=0); near=np.abs(f[:,:,:3]-bg).sum(axis=2)<150
        lab,n=ndi.label(near); edge=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0); fg=~np.isin(lab,list(edge))&(f[:,:,3]>0)
    fg=ndi.binary_opening(fg,iterations=2); lab,n=ndi.label(fg); sz=ndi.sum(fg,lab,range(1,n+1)); fg=lab==(1+int(np.argmax(sz))); fg=ndi.binary_fill_holes(fg)
    ys,xs=np.where(fg); x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1; s=HEIGHT/(y1-y0)
    rgba=np.dstack([f[:,:,:3].astype(np.uint8),(fg*255).astype(np.uint8)]); c=Image.fromarray(rgba).crop((x0,y0,x1,y1)); nw,nh=max(1,round(c.width*s)),HEIGHT
    c=c.resize((nw,nh),Image.LANCZOS); b=np.asarray(c).copy(); al=b[:,:,3]>140
    rgb=np.clip(b[:,:,:3].astype(float)*BRIGHT,0,255).astype(np.uint8)
    q=Image.fromarray(rgb).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    out=Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8)); os.makedirs('art/sprites',exist_ok=True); out.save(f'art/sprites/{name}_body.png',optimize=True)
    ysl,xsl=np.where(al); low=ysl>ysl.max()-max(3,int(nh*0.1)); fx=int(np.median(xsl[low])); fy=int(ysl.max()+1)
    P=lambda p:[round((p[0]-x0)*s,1),round((p[1]-y0)*s,1)]
    meta=dict(w=nw,h=nh,fx=fx,fy=fy,s1=P(SH[name]['front']),s2=P(SH[name]['back'])); json.dump(meta,open(f'art/sprites/{name}_body.json','w')); print(name,meta,os.path.getsize(f'art/sprites/{name}_body.png')//1024,'KB'); return out,meta
def embed(names,path='index.html'):
    src={n:'data:image/png;base64,'+base64.b64encode(open(f'art/sprites/{n}_body.png','rb').read()).decode() for n in names}; meta={n:json.load(open(f'art/sprites/{n}_body.json')) for n in names}
    s=open(path,encoding='utf-8').read(); a=s.index('/*BODIES:BEGIN*/'); b=s.index('/*BODIES:END*/')+len('/*BODIES:END*/')
    open(path,'w',encoding='utf-8').write(s[:a]+'/*BODIES:BEGIN*/\nconst BODY_SRC='+json.dumps(src,separators=(',',':'))+', BODY_META='+json.dumps(meta,separators=(',',':'))+';\n/*BODIES:END*/'+s[b:]); print('embedded',list(src))
if __name__=='__main__':
    if sys.argv[1]=='--embed': embed(sys.argv[2:])
    else: build(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 104,float(sys.argv[3]) if len(sys.argv)>3 else 1.10)
