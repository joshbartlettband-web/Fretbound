# v1.63 room art -> game sizes.  usage: python3 tests/procrooms.py            (art/gemini_test/rooms/*.png -> art/gemini_test/rooms_master/*.png, art/plates/stage_green.png)
#                                        python3 tests/procrooms.py --embed    writes ROOM_SRC into index.html and the Green Room plate into STAGE_PLATE_SRC
# Masters stay ungraded (tests/grade.py only grades the copies inside index.html), so re-embedding never compounds the grade.
import sys,os,json,base64,glob
sys.path.insert(0,'tests')
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
SRC='art/gemini_test/rooms'; M='art/gemini_test/rooms_master'
def q(im,n): return im.quantize(colors=n,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
def key(im):
    a=np.asarray(im.convert('RGB')).astype(int); bg=np.median(np.concatenate([a[:4].reshape(-1,3),a[-4:].reshape(-1,3),a[:,:4].reshape(-1,3),a[:,-4:].reshape(-1,3)]),axis=0)
    fg=np.abs(a-bg).sum(axis=2)>120; fg=ndi.binary_opening(fg,iterations=2); lab,n=ndi.label(fg); sz=ndi.sum(fg,lab,range(1,n+1)); fg=lab==(1+int(np.argmax(sz))); return ndi.binary_fill_holes(fg)
def door(k,W=88,H=152):
    im=Image.open(f'{SRC}/{k}.png').convert('RGB'); fg=key(im); ys,xs=np.where(fg); box=(xs.min(),ys.min(),xs.max()+1,ys.max()+1)
    c=Image.fromarray(np.dstack([np.asarray(im),(fg*255).astype(np.uint8)])).crop(box); s=min((W-2)/c.width,(H-1)/c.height); w,h=round(c.width*s),round(c.height*s)
    c=c.resize((w,h),Image.LANCZOS); a=np.asarray(c).copy(); al=a[:,:,3]>140; rgb=q(Image.fromarray(a[:,:,:3]),48)
    out=Image.new('RGBA',(W,H),(0,0,0,0)); out.paste(Image.fromarray(np.dstack([np.asarray(rgb),(al*255).astype(np.uint8)])),((W-w)//2,H-h)); out.save(f'{M}/{k}.png',optimize=True)
def main():
    os.makedirs(M,exist_ok=True)
    import procstage; procstage.proc(f'{SRC}/green.png','art/plates/stage_green.png')
    im=Image.open(f'{SRC}/merch.png').convert('RGB'); w,h=im.size; m=int(min(w,h)*0.045); im=im.crop((m,m,w-m,h-m))
    s=max(640/im.width,360/im.height); im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS); x=(im.width-640)//2; y=(im.height-360)//2; q(im.crop((x,y,x+640,y+360)),64).save(f'{M}/merch.png',optimize=True)
    q(Image.open(f'{SRC}/wall.png').convert('RGB').resize((256,256),Image.LANCZOS),48).save(f'{M}/wall.png',optimize=True)
    for k in ('door_green','door_ear','door_roster'): door(k)
    print('ok',sorted(os.listdir(M)))
def embed(path='index.html'):
    s=open(path,encoding='utf-8').read(); b64=lambda f:'data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode()
    src={os.path.basename(f)[:-4]:b64(f) for f in sorted(glob.glob(f'{M}/*.png'))}
    blk='/*ROOMS:BEGIN*/\nconst ROOM_SRC='+json.dumps(src,separators=(',',':'))+';\n/*ROOMS:END*/'
    if '/*ROOMS:BEGIN*/' in s: a=s.index('/*ROOMS:BEGIN*/'); b=s.index('/*ROOMS:END*/')+len('/*ROOMS:END*/'); s=s[:a]+blk+s[b:]
    else: mk='/*PEDALS:BEGIN*/'; assert s.count(mk)==1; s=s.replace(mk,blk+'\n'+mk)
    a=s.index('const STAGE_PLATE_SRC=')+len('const STAGE_PLATE_SRC='); b=s.index(';\n',a); P=json.loads(s[a:b]); P['green']=b64('art/plates/stage_green.png'); s=s[:a]+json.dumps(P,separators=(',',':'))+s[b:]
    open(path,'w',encoding='utf-8').write(s); print('embedded',list(src),'+ green plate')
if __name__=='__main__': embed() if '--embed' in sys.argv else main()
