# grid sheets of the processed stage plates (640x240 coords) with bright-blob candidates marked: python3 tests/stagegrid.py OUTDIR id id ...
import sys,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage as ndi
out=sys.argv[1]; ids=sys.argv[2:]; K=2
def blobs(a):
    lum=a.mean(axis=2); loc=ndi.uniform_filter(lum,15); m=(lum>loc+38)&(lum>150)
    lab,n=ndi.label(m); res=[]
    for i,(c,z) in enumerate(zip(ndi.center_of_mass(m,lab,range(1,n+1)),ndi.sum(m,lab,range(1,n+1)))):
        if 2<=z<=60: res.append((round(c[1]),round(c[0]),int(z)))
    return res
for k in range(0,len(ids),2):
    sheet=Image.new('RGB',(640*K+40,(240*K+24)*2),'black')
    for j,i in enumerate(ids[k:k+2]):
        im=Image.open(f'art/plates/stage_{i}.png').convert('RGB'); a=np.asarray(im).astype(float)
        big=im.resize((640*K,240*K),Image.NEAREST); d=ImageDraw.Draw(big)
        for x in range(0,640,40): d.line([(x*K,0),(x*K,240*K)],fill=(255,255,255),width=1); d.text((x*K+2,2),str(x),fill=(255,255,0))
        for y in range(0,240,40): d.line([(0,y*K),(640*K,y*K)],fill=(255,255,255),width=1); d.text((2,y*K+2),str(y),fill=(255,255,0))
        b=blobs(a)
        for x,y,z in b: d.ellipse([x*K-4,y*K-4,x*K+4,y*K+4],outline=(255,0,255))
        sheet.paste(big,(20,j*(240*K+24)+12)); print(i,len(b),'blobs')
    sheet.save(f'{out}/grid_{ids[k]}.png')
