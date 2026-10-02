# Replace the cotton field in the Juke's window with a layered night pine treeline (drawn on a coarse pixel grid, then scaled up to the source).
import numpy as np, random
from PIL import Image, ImageDraw
X0,Y0,X1,Y1=1046,107,1322,320; K=2.4
im=Image.open('/tmp/juke_cotton.jpg').convert('RGB')
# the old painted ridge wedge at the left of the sky: carry the clean sky rows across from x=1172
_a=np.asarray(im).copy(); _r=np.random.default_rng(3)
for _y in range(107,222):
    _ref=_a[_y,1172:1180].astype(float).mean(axis=0)
    for _x in range(X0,1172): _a[_y,_x]=np.clip(_ref+_r.normal(0,1.6,3),0,255)
im=Image.fromarray(_a)
cw,ch=round((X1-X0)/K),round((Y1-Y0)/K)
c=Image.new('RGB',(cw,ch),(0,0,0)); d=ImageDraw.Draw(c); rnd=random.Random(11)
top=42   # rows above this keep the painted sky
def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
for y in range(top,ch):
    u=(y-top)/(ch-top); d.line([(0,y),(cw,y)],fill=lerp((64,90,104),(18,32,42),min(1,u*1.6)))   # haze at the horizon fading to dark ground
def pine(cx,base,h,col,rim):
    w=max(5,int(h*0.46)); tiers=max(3,h//9)
    for t in range(tiers):
        f=t/tiers; ty=base-h+int(h*0.80*f); tw=max(1,int(w*(0.22+0.78*f))); th=int(h*0.80/tiers*2.1)
        d.polygon([(cx,ty),(cx-tw,ty+th),(cx+tw,ty+th)],fill=col)
        d.line([(cx+tw-1,ty+th-1),(cx+1,ty+1)],fill=rim)          # moonlit right edge
    d.rectangle([cx-1,base-int(h*0.2),cx,base],fill=col)
def row(base,hmin,hmax,gap,col,rim,off=0):
    x=off
    while x<cw+8:
        pine(x,base,rnd.randint(hmin,hmax),col,rim); x+=gap+rnd.randint(-2,3)
row(45+8,12,20,5,(30,50,64),(54,80,98),2)
row(45+22,20,31,8,(21,38,50),(44,68,86),5)
row(ch+4,40,56,16,(11,22,30),(38,60,78),9)
c=c.resize((c.width*1,c.height*1),Image.NEAREST).resize((X1-X0,Y1-Y0),Image.NEAREST)
out=im.copy(); sky_rows=round(top*K)
region=out.crop((X0,Y0+sky_rows,X1,Y1)); new=c.crop((0,sky_rows,X1-X0,Y1-Y0)); out.paste(new,(X0,Y0+sky_rows))
out.save('stages/juke.jpg',quality=95); out.crop((1020,90,1345,345)).save('/tmp/claude-0/-home-user-Fretbound/06db394c-e65b-5e2f-91cd-5e32ab269560/scratchpad/juke_pines.png')
