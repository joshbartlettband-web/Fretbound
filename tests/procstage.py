# Gemini stage plates -> game plates (640x240, 64 colours, no dither).
# usage: python3 tests/procstage.py SRC OUT [CROP_TOP]      one file (CROP_TOP rows off the top after scaling to 640 wide)
#        python3 tests/procstage.py --all                    every art/gemini_test/stages/<id>.jpg -> art/plates/stage_<id>.png
# Flat letterbox bars (near black or near white) are trimmed first; with no CROP_TOP the crop keeps the floor: two thirds of the extra height comes off the top.
import sys,os,glob
import numpy as np
from PIL import Image
def trim(im):
    a=np.asarray(im).astype(float); m=a.mean(axis=2); sd=m.std(axis=1); mu=m.mean(axis=1)
    flat=lambda y:(sd[y]<8) and (mu[y]<45 or mu[y]>245)
    t=0; b=len(mu)
    while t<b-1 and flat(t): t+=1
    while b>t+1 and flat(b-1): b-=1
    return im.crop((0,t,im.width,b))
def proc(src,out,crop=None):
    im=trim(Image.open(src).convert('RGB')); s=640/im.width; h=round(im.height*s)
    im2=im.resize((640,h),Image.LANCZOS)
    if h<240: im2=im2.resize((round(640*240/h),240),Image.LANCZOS); im2=im2.crop(((im2.width-640)//2,0,(im2.width-640)//2+640,240))
    else:
        c=crop if crop is not None else round((h-240)*0.67); im2=im2.crop((0,c,640,c+240))
    im2.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).save(out,optimize=True)
    print(os.path.basename(out),os.path.getsize(out)//1024,'KB')
if __name__=='__main__':
    if sys.argv[1]=='--all':
        for f in sorted(glob.glob('art/gemini_test/stages/*.jpg')): proc(f,'art/plates/stage_%s.png'%os.path.basename(f)[:-4])
    else: proc(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else None)
