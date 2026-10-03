# Give every pose of every atlas the SAME one-pixel outline.  Gemini paints a thick dark outline, and rescaling poses to line them up with idle makes its thickness
# differ from pose to pose (a pixel heavier or lighter), which shows when poses swap or crossfade.  For each 320-ish px cell: peel the dark outline rings off the silhouette
# (a ring counts as outline only while it is clearly darker than the figure's interior, so a black suit is not eaten), then draw a fresh 1 px outline OUTSIDE what is left.
# usage: python3 tests/outlinefix.py [id ...]     rewrites art/poses/<id>_atlas.png (idempotent: running it twice changes nothing more);  procposes.py calls fix_cell() when it builds.
import sys,os,json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
LUM=np.array([.299,.587,.114])
def fix_cell(cell,maxpeel=4):
    a=cell[:,:,3]>0
    if a.sum()<50: return cell
    rgb=cell[:,:,:3].astype(float); L=rgb@LUM
    # interior reference: mean luminance of the rings 5..8 px in from the edge (falls back to the whole figure)
    rings=[]; cur=a.copy()
    for d in range(1,10):
        er=ndi.binary_erosion(cur); ring=cur&~er; rings.append(ring); cur=er
        if ring.sum()==0: break
    inner=np.zeros_like(a)
    for r in rings[4:8]: inner|=r
    R=L[inner].mean() if inner.sum()>30 else L[a].mean()
    body=a.copy(); peeled=np.zeros_like(a)
    for d in range(maxpeel):
        er=ndi.binary_erosion(body); ring=body&~er
        if ring.sum()==0: break
        m=L[ring].mean()
        if m<0.62*R and m<100: peeled|=ring; body=er
        else: break
    # the outline colour: the median colour of what was peeled (kept dark), else a dark brown
    if peeled.sum()>10:
        c=np.median(rgb[peeled],axis=0); 
        if c@LUM>60: c=c*(55/(c@LUM))
    else: c=np.array([42.,24.,16.])
    grown=ndi.binary_dilation(body); outl=grown&~body
    out=np.zeros_like(cell); out[:,:,:3]=np.where(body[...,None],cell[:,:,:3],0); out[outl,:3]=c.astype(np.uint8); out[:,:,3]=(grown*255).astype(np.uint8)
    return out
def fix_atlas(cid,root='art/poses'):
    f=f'{root}/{cid}_atlas.png'; M=json.load(open(f'art/poses/{cid}_meta.json')); a=np.asarray(Image.open(f).convert('RGBA')).copy(); cw,ch=M['cw'],M['ch']
    for i in range(16):
        y0,x0=(i//8)*ch,(i%8)*cw; a[y0:y0+ch,x0:x0+cw]=fix_cell(a[y0:y0+ch,x0:x0+cw])
    Image.fromarray(a).save(f,optimize=True)
if __name__=='__main__':
    ids=sys.argv[1:] or sorted(f[:-10] for f in os.listdir('art/poses') if f.endswith('_atlas.png'))
    for i in ids: fix_atlas(i); print('fixed',i)
