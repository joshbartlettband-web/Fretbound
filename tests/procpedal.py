# Gemini pedal fronts -> game pedals: key the flat background (flood fill from the border, keep the biggest piece), fit into 84x120, 48-colour palette, hard alpha.
# usage: python3 tests/procpedal.py        (art/gemini_test/pedals/<id>.png -> art/pedals/<id>.png)
import glob,os,sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0,'tests')
from arttone import tone
W,H=84,120; os.makedirs('art/pedals',exist_ok=True)
def key(im):
    a=np.asarray(im.convert('RGB')).astype(int); h,w,_=a.shape
    border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]); bg=np.median(border,axis=0)
    near=np.abs(a-bg).sum(axis=2)<150
    lab,n=ndi.label(near); edge=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0)
    bgm=np.isin(lab,list(edge)); fg=~bgm
    fg=ndi.binary_opening(fg,iterations=2); lab,n=ndi.label(fg); sz=ndi.sum(fg,lab,range(1,n+1)); fg=lab==(1+int(np.argmax(sz))); fg=ndi.binary_fill_holes(fg)
    return fg
def proc(f):
    im=Image.open(f).convert('RGB'); fg=key(im); ys,xs=np.where(fg); box=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
    rgba=np.dstack([np.asarray(im),(fg*255).astype(np.uint8)]); c=Image.fromarray(rgba).crop(box)
    s=min((W-2)/c.width,(H-2)/c.height); nw,nh=max(1,round(c.width*s)),max(1,round(c.height*s))
    c=c.resize((nw,nh),Image.LANCZOS); a=np.asarray(c).copy(); al=a[:,:,3]>150; a[:,:,3]=al*255
    rgb=Image.fromarray(tone(a[:,:,:3],al)).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    out=Image.new('RGBA',(W,H),(0,0,0,0)); o=np.asarray(rgb).copy(); oa=np.dstack([o,al*255]).astype(np.uint8)
    out.paste(Image.fromarray(oa),((W-nw)//2,H-nh-1)); out.save('art/pedals/'+os.path.basename(f)[:-4]+'.png',optimize=True); return os.path.getsize('art/pedals/'+os.path.basename(f)[:-4]+'.png')
if __name__=='__main__' and '--embed' not in sys.argv:
    tot=0
    for f in sorted(glob.glob('art/gemini_test/pedals/*.jpg')): tot+=proc(f)
    print('total',tot//1024,'KB for',len(glob.glob('art/pedals/*.png')),'pedals')
def embed(path='index.html'):
    import base64,json
    src={os.path.basename(f)[:-4]:'data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode() for f in sorted(glob.glob('art/pedals/*.png'))}
    s=open(path,encoding='utf-8').read(); a=s.index('/*PEDALS:BEGIN*/'); b=s.index('/*PEDALS:END*/')+len('/*PEDALS:END*/')
    open(path,'w',encoding='utf-8').write(s[:a]+'/*PEDALS:BEGIN*/\nconst PEDAL_SRC='+json.dumps(src,separators=(',',':'))+';\n/*PEDALS:END*/'+s[b:]); print('embedded',len(src),'pedals')
if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='--embed': embed()
