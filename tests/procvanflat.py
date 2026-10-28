# Painted vans with a flat front tire for the road's flat-tire scene (v2.07): art/gemini_test/vans/flat/v<n>_flat.png (Gemini Pro, magenta)
# -> art/vans/v<n>_flat.png, about a person's height at the hang sheets' density (2x), graded like them; --embed writes VANFLAT_SRC.
import sys,os,io,json,base64
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0,'tests'); import grade as GR
out={}
for v in ['v0','v1','v2']:
    a=np.asarray(Image.open(f'art/gemini_test/vans/flat/{v}_flat.png').convert('RGB')).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]
    key=(r>g+60)&(b>g+60)&(abs(r-b)<90)                      # magenta and its darker shadow
    m=ndi.binary_opening(~key,iterations=1); lab,n=ndi.label(m); sz=ndi.sum(m,lab,range(1,n+1)); m=np.isin(lab,[i+1 for i,s in enumerate(sz) if s>0.02*sz.max()])
    ys,xs=np.where(m); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    rgba=np.dstack([a.astype(np.uint8),(m*255).astype(np.uint8)])[y0:y1,x0:x1]; im=Image.fromarray(rgba,'RGBA')
    H=190 if v!='v2' else 210; im=im.resize((round(im.width*H/im.height),H),Image.LANCZOS)   # 2x density: about 0.9 of a person (104) for the vans, a little more for the bus
    q=np.asarray(im).copy(); q[...,3]=(q[...,3]>140)*255; im=GR.grade(Image.fromarray(q))
    im.save(f'art/vans/{v}_flat.png',optimize=True); out[v]=im.size; print(v,im.size)
if '--embed' in sys.argv:
    src={v:'data:image/png;base64,'+base64.b64encode(open(f'art/vans/{v}_flat.png','rb').read()).decode() for v in out}
    blk='/*VANFLAT:BEGIN*/\nconst VANFLAT_SRC='+json.dumps(src,separators=(',',':'))+';\n/*VANFLAT:END*/'
    s=open('index.html',encoding='utf-8').read()
    if '/*VANFLAT:BEGIN*/' in s: i=s.index('/*VANFLAT:BEGIN*/'); j=s.index('/*VANFLAT:END*/')+len('/*VANFLAT:END*/'); s=s[:i]+blk+s[j:]
    else: a='/*VANART:END*/'; assert s.count(a)==1; s=s.replace(a,a+'\n'+blk)
    open('index.html','w',encoding='utf-8').write(s); print('embedded')
