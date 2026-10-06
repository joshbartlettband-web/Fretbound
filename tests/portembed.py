# Portrait art: art/gemini_test/chars/<id>_port.png (Gemini, magenta background) -> <id>_card.png 176px and <id>_tile.png 96px, embedded in PORTRAIT_ART
# (replacing any entry already there). Run tests/grade.py afterwards.   usage: python3 tests/portembed.py ID ...
import sys,base64,numpy as np
from PIL import Image
from scipy import ndimage as ndi
def make(k):
    a=np.asarray(Image.open(f'art/gemini_test/chars/{k}_port.png').convert('RGB')).astype(int)
    bg=np.median(np.concatenate([a[:6].reshape(-1,3),a[:,:6].reshape(-1,3),a[:,-6:].reshape(-1,3)]),axis=0)
    near=np.abs(a-bg).sum(axis=2)<140; lab,n=ndi.label(near); edge=set(lab[0])|set(lab[:,0])|set(lab[:,-1])|set(lab[-1]); edge.discard(0); bgm=np.isin(lab,list(edge))
    bgm|=((a[:,:,0]-a[:,:,1]>70)&(a[:,:,2]-a[:,:,1]>50))
    rgba=Image.fromarray(np.dstack([a.astype(np.uint8),((~bgm)*255).astype(np.uint8)])); out={}
    for kind,sz in (('card',176),('tile',96)):
        o=np.asarray(rgba.resize((sz,sz),Image.LANCZOS)).copy(); al=o[:,:,3]>140
        r,g,b=[o[:,:,i].astype(int) for i in range(3)]; al&=~((r-g>60)&(b-g>40)&(b>90))
        q=Image.fromarray(o[:,:,:3]).quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
        f=f'art/gemini_test/chars/{k}_{kind}.png'; Image.fromarray(np.dstack([np.asarray(q),(al*255).astype(np.uint8)])).save(f,optimize=True)
        out[kind]='data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode()
    return k+":{card:'"+out['card']+"',tile:'"+out['tile']+"'}"
s=open('index.html',encoding='utf-8').read(); a="const PORTRAIT_ART={"; assert s.count(a)==1
for k in sys.argv[1:]:
    st=s.index(a); end=s.index('};',st)
    i=s.find(k+":{card:'data:",st,end)
    if i>=0: j=s.index("'}",i)+2; s=s[:i]+s[j+(1 if s[j]==',' else 0):]
    s=s.replace(a,a+make(k)+",",1); print('embedded',k)
open('index.html','w',encoding='utf-8').write(s)
