# Hand-erase the arms of the Gemini standing bodies. Polygons are in ORIGINAL image coordinates (864x1184), one list per arm with a fill mode:
#   right / left : continue the clothing from the nearest pixels on that side (smoothed over +-14 rows); alpha : the arm sticks out past the body, so make it transparent.
# usage: python3 armless_all.py [name ...]  -> chars/<name>_armless_body.png (full size RGBA) and, with --ov, chars/<name>_ov.png showing the polygons
import sys,json,numpy as np
from PIL import Image,ImageDraw
CFG={
'monk':[('right',[(268,345),(325,335),(332,450),(335,600),(345,680),(390,720),(390,800),(325,805),(295,760),(282,700),(270,600),(266,450)])],
'busker':[('right',[(298,385),(345,380),(350,500),(352,690),(345,720),(358,740),(360,800),(325,820),(300,780),(298,720),(296,600)]),
          ('left',[(498,390),(525,420),(530,700),(525,730),(535,790),(515,800),(498,740),(490,700),(492,500)])],
'hermit':[('right',[(240,400),(300,420),(330,500),(335,720),(335,760),(320,815),(280,815),(262,760),(250,700),(245,550)]),
          ('left',[(498,720),(518,730),(518,792),(496,792)])],
'luthier':[('right',[(282,350),(330,340),(345,420),(350,540),(352,700),(345,780),(320,800),(295,790),(290,720),(286,620),(282,500),(278,420)]),
           ('left',[(515,440),(548,455),(550,700),(532,770),(515,770)])],
'carto':[('right',[(245,400),(330,410),(330,520),(335,700),(325,760),(322,830),(265,835),(255,770),(245,730),(243,650),(245,500)]),
         ('left',[(505,440),(545,450),(550,640),(552,700),(532,790),(505,795),(505,700),(505,560)])],
}
def erase(name,ov=False):
    im=Image.open(f'chars/{name}_body.png' if __import__('os').path.exists(f'chars/{name}_body.png') else f'chars/{name}_body.jpg').convert('RGB'); a=np.asarray(im).astype(float); H,W,_=a.shape
    if ov:
        o=im.copy(); d=ImageDraw.Draw(o)
        for _,P in CFG[name]: d.polygon(P,outline=(255,255,0))
        o.crop((150,100,750,1150)).save(f'chars/{name}_ov.png'); return
    from scipy import ndimage as ndi
    import cv2
    ai=a.astype(int); bgc=np.median(np.concatenate([ai[0],ai[-1],ai[:,0],ai[:,-1]]),axis=0)
    near=np.abs(ai-bgc).sum(axis=2)<150; magenta=((ai[:,:,0]-ai[:,:,1])>110)&((ai[:,:,2]-ai[:,:,1])>50)
    lab,n=ndi.label(near|magenta); edge=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0)
    fg=~np.isin(lab,list(edge)); fg=ndi.binary_fill_holes(fg)&~(magenta&~ndi.binary_erosion(fg,iterations=0))
    soft=((ai[:,:,0]-ai[:,:,1])>70)&((ai[:,:,2]-ai[:,:,1])>35)&(ai[:,:,0]>110)
    fg=ndi.binary_opening(fg&~soft,iterations=1)
    # colour under the background = nearest body pixel, so the inpainting never drags magenta into the arm area
    idx=ndi.distance_transform_edt(~fg,return_distances=False,return_indices=True); src=a[idx[0],idx[1]].astype(np.uint8)
    mask=np.zeros((H,W),np.uint8)
    for mode,P in CFG[name]:
        m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(P,fill=255); mask|=(np.asarray(m)>0).astype(np.uint8)*255
    res=cv2.inpaint(src,mask,12,cv2.INPAINT_TELEA)
    Image.fromarray(np.dstack([res,fg*255]).astype(np.uint8)).save(f'chars/{name}_armless_body.png'); print('saved',name)
if __name__=='__main__':
    ov='--ov' in sys.argv; names=[n for n in sys.argv[1:] if n!='--ov'] or list(CFG)
    for n in names: erase(n,ov)
