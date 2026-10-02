# Remove unwanted objects from the title plate originals (art/plates/orig), keeping the dithered pixel texture.
#  oc: the dark trees and spinifex along the horizon -> each masked pixel takes a random sky pixel from the same row nearby
#  sa: the chapel on the terraces -> exemplar copy, mountain slope from the right and terrace from below-left, then a seam pass
# usage: python3 tests/dev/plateclean.py   then python3 tests/shiftplates.py, python3 tests/procmask.py oc / sa, re-embed masks (see HANDOFF)
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
rng=np.random.default_rng(7)
def rowfill(a,m,span=40,bad=None):
    out=a.copy(); H,W,_=a.shape; bad=m if bad is None else (m|bad)
    for y in range(H):
        xs=np.where(m[y])[0]
        for x in xs:
            lo,hi=max(0,x-span),min(W,x+span); ok=np.where(~bad[y,lo:hi])[0]
            if len(ok): out[y,x]=a[y,lo+rng.choice(ok)]
    return out
# Oceania
a=np.asarray(Image.open('art/plates/orig/oc.png').convert('RGB')).astype(int); L=a@[0.299,0.587,0.114]
out=np.ones(L.shape,bool); out[:,183:463]=False
med=np.array([np.median(L[y][out[y]]) for y in range(L.shape[0])])[:,None]
m=(np.abs(L-med)>22)|(L<95); m[:140]=False; m&=out; m=ndi.binary_dilation(m,iterations=2); m[:140]=False; m&=out
m|=ndi.binary_dilation((L<120)&(np.abs(a[:,:,0]-a[:,:,2])<90),iterations=1)&(np.arange(640)[None,:]>=150)&(np.arange(640)[None,:]<183)&(np.arange(224)[:,None]>=196)
Image.fromarray(rowfill(a,m,60,~out).astype(np.uint8)).save('art/plates/orig/oc.png'); print('oc removed',m.sum(),'px')
# South America: chapel box
b=np.asarray(Image.open('art/plates/orig/sa.png').convert('RGB')).astype(int); o=b.copy()
x0,x1,y0,y1=158,210,157,194
for y in range(y0,y1):
    for x in range(x0,x1):
        g=b[y,x]; 
        # source: same row 55 px to the right while that is mountain (not green), else 50 px to the left (terrace)
        src=b[y,x+55]; green=src[1]>src[0]+10
        o[y,x]=src if not green and y<186 else b[y,x-50] if not (b[y,x-50][1]>b[y,x-50][0]+10)==False else b[min(223,y+3),x-50]
Image.fromarray(o.astype(np.uint8)).save('art/plates/orig/sa.png'); print('sa chapel replaced')
# NOTE: the South America exemplar copy above left a visible seam; the chapel was instead removed by a Gemini edit of a 96x64 patch
# (x4, kept as art/gemini_test/plates/sa_chapel_removed_patch.png), snapped to the plate palette and pasted into x156-214, y154-198.
