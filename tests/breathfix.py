# v1.89: the painted "breath" pose (cell 1) was a separate painting, so idle <-> breath swaps made outlines jump ("border pulse").
# Rebuild breath from idle: everything above the waist moves up one pixel (the seam row is doubled so nothing tears), feet stay put.
# usage: python3 tests/breathfix.py [ID ...]   (default: every atlas in art/gemini_test/poses_master), then procposes --embed x and grade.py
import sys,os,glob,json
import numpy as np
from PIL import Image
M='art/gemini_test/poses_master'
ids=sys.argv[1:] or [os.path.basename(f)[:-10] for f in sorted(glob.glob(f'{M}/*_atlas.png'))]
for cid in ids:
    m=json.load(open(f'art/poses/{cid}_meta.json')); cw,ch=m['cw'],m['ch']
    a=np.asarray(Image.open(f'{M}/{cid}_atlas.png').convert('RGBA')).copy()
    idle=a[0:ch,0:cw].copy(); al=idle[:,:,3]>140; ys=np.where(al.any(1))[0]
    top,bot=ys[0],ys[-1]; waist=int(round(bot-(bot-top)*0.45))       # lift the head, shoulders, arms and guitar; not the legs
    br=idle.copy(); br[top-1:waist,:]=idle[top:waist+1,:]               # rows top..waist move up by one
    a[0:ch,cw:2*cw]=br
    Image.fromarray(a).save(f'{M}/{cid}_atlas.png',optimize=True); print(cid,'breath rebuilt, waist row',waist)
