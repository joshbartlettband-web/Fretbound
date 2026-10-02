# Colour audit of every processed Gemini asset: overall warmth, the cast of the whites (the "piss filter"), and contrast.
# usage: python3 tests/dev/coloraudit.py            prints a table per group, worst highlight cast first
# white cast = (R+G)/2 - B of the whites (bright, near-neutral pixels): 0 is neutral, above ~25 reads yellow; white level is their brightness.
# contrast = standard deviation of luminance; range = 5th to 95th percentile of luminance.
import glob,os
import numpy as np
from PIL import Image
G={'pedals':'art/pedals/*.png','guitars':'art/guitars/*.png','players':'art/sprites/*_body.png','callers':'art/callers/*_body.png',
   'band':'art/sprites/band/*_atlas.png','stages':'art/plates/stage_*.png','titles':'art/plates/[a-z][a-z].png','vans':'art/vans/*.png',
   'vanscenes':'art/vanscenes/*.png','portraits':'art/portraits/*.png'}
def stats(f):
    a=np.asarray(Image.open(f).convert('RGBA')).astype(float); m=a[:,:,3]>128; p=a[:,:,:3][m]
    if len(p)<50: return None
    L=p@[0.299,0.587,0.114]; sat=(p.max(1)-p.min(1))/np.maximum(1,p.max(1))
    hi=p[(L>150)&(sat<0.38)]          # the whites: bright and close to neutral (pickguards, strings, chrome, labels, shirts)
    if len(hi)<12: hi=p[L>=np.percentile(L,97)]
    return dict(warm=((p[:,0]+p[:,1])/2-p[:,2]).mean(), wcast=((hi[:,0]+hi[:,1])/2-hi[:,2]).mean(), wl=(hi@[0.299,0.587,0.114]).mean(),
                con=L.std(), lo=np.percentile(L,5), hi=np.percentile(L,95))
if __name__=='__main__':
    for g,pat in G.items():
        rows=[(os.path.basename(f)[:-4],stats(f)) for f in sorted(glob.glob(pat))]; rows=[r for r in rows if r[1]]
        if not rows: continue
        avg={k:np.mean([r[1][k] for r in rows]) for k in rows[0][1]}
        print(f"\n== {g} ({len(rows)})  avg: warmth {avg['warm']:.0f}  white cast {avg['wcast']:.0f}  white level {avg['wl']:.0f}  contrast {avg['con']:.0f}  range {avg['lo']:.0f}-{avg['hi']:.0f}")
        for n,s in sorted(rows,key=lambda r:-r[1]['wcast'])[:6]: print(f"   {n:24s} white cast {s['wcast']:5.0f}  white level {s['wl']:4.0f}  contrast {s['con']:4.0f}  warmth {s['warm']:4.0f}")
