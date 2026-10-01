import sys
from PIL import Image, ImageDraw
import numpy as np
K=int(sys.argv[1]); out=sys.argv[2]
S=432; CELL=9   # the gradient is built from 9 px cells (a 48x48 grid) with ordered dithering between bands
STOPS=[(0.00,'#0C0618'),(0.14,'#2A1038'),(0.31,'#6E1E44'),(0.49,'#A83434'),(0.67,'#DC6428'),(0.84,'#F8A840'),(1.00,'#FFD880')]
hx=lambda h:tuple(int(h[i:i+2],16) for i in (1,3,5)); cols=[hx(c) for _,c in STOPS]; pos=[p for p,_ in STOPS]
B4=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])/16.0
n=S//CELL; bg=np.zeros((S,S,4),np.uint8); bg[...,3]=255
for cy in range(n):
    u=(cy+0.5)/n
    for k in range(len(pos)-1):
        if pos[k]<=u<=pos[k+1]: f=(u-pos[k])/(pos[k+1]-pos[k]); lo,hi=k,k+1; break
    f=min(1,max(0,(f-0.3)/0.4))   # a 40% dither zone between bands keeps the bands crisp
    for cx in range(n):
        c=cols[hi] if f>B4[cy%4,cx%4] else cols[lo]
        bg[cy*CELL:(cy+1)*CELL,cx*CELL:(cx+1)*CELL,:3]=c
bgI=Image.fromarray(bg)
F=Image.open('/home/claude/F_54.png').convert('RGBA'); a=np.asarray(F)[...,3]>0; ys,xs=np.nonzero(a)
crop=F.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1)); w,h=crop.size
big=crop.resize((w*K,h*K),Image.NEAREST)
fgI=Image.new('RGBA',(S,S),(0,0,0,0)); fgI.alpha_composite(big,((S-big.width)//2,(S-big.height)//2))
bgI.save(out+'_bg.png'); fgI.save(out+'_fg.png')
comp=bgI.copy(); comp.alpha_composite(fgI)
def mask(kind):
    m=Image.new('L',(S,S),0); d=ImageDraw.Draw(m); r=S*36/108
    if kind=='circle': d.ellipse((S/2-r,S/2-r,S/2+r,S/2+r),fill=255)
    else: d.rounded_rectangle((S/2-r,S/2-r,S/2+r,S/2+r),radius=r*0.42,fill=255)
    return m
sheet=Image.new('RGB',(S*3+20+200,S),(24,24,32)); sheet.paste(comp.convert('RGB'),(0,0))
for i,kind in enumerate(['circle','squircle']):
    c=Image.new('RGB',(S,S),(24,24,32)); c.paste(comp.convert('RGB'),(0,0),mask(kind)); sheet.paste(c,((i+1)*(S+10),0))
y=10
for sz in (96,64,48):
    t=Image.new('RGB',(sz,sz),(24,24,32)); t.paste(comp.convert('RGB').resize((sz,sz),Image.LANCZOS),(0,0),mask('circle').resize((sz,sz),Image.LANCZOS)); sheet.paste(t,(S*3+30,y)); y+=sz+10
sheet.thumbnail((1500,420)); sheet.save(out+'_preview.png'); print(out,'F box',big.size)
