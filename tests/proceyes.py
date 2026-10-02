# Eye positions for the painted players and callers, so they can blink. usage: python3 tests/proceyes.py          (writes 'eye' and 'ec' into the sprite json files)
#                                                                          python3 tests/proceyes.py --check ID,ID,...   (draws the rectangles on the painting: /tmp/fbout/eyecheck.png)
# Rectangles are in PAINTING pixels (864x1184 pictures) and are mapped to sprite pixels with the 'map' that procbody.py / proccaller.py store; 'sprite' entries are already
# in sprite pixels (the Bard was built by an older script). The lid colour 'ec' is the median skin colour around the eye in the sprite. Re-run procbody/proccaller first
# (they rewrite the json), then this, then their --embed.
import sys,json,os
import numpy as np
from PIL import Image,ImageDraw
EYES={
 'monk':[(469,207,10,10)],'hermit':[(459,229,22,13),(516,229,11,11)],'busker':[(440,207,38,18),(508,209,9,12)],'luthier':[(434,186,38,17),(494,186,8,14)],'carto':[(453,316,17,16),(498,315,17,16)],
 'tide':[(470,148,37,18)],'juke':[(417,197,19,14),(466,197,13,14)],'dunes':[(461,180,20,9),(501,178,16,12)],'sebene':[(493,201,52,28)],'azmari':[(464,187,75,66)],
 'rio':[(478,208,36,22)],'milonga':[(447,167,38,14)],'chicha':[(426,98,28,26)],'paris':[(462,183,52,22)],'frost':[(422,180,50,30),(483,193,17,13)],
 'tokyo':[(498,205,50,30)],'ghat':[(441,136,40,24)],'bali':[(470,189,28,20)],'lanai':[(477,207,46,32)],'grotto':[(435,172,32,20)],'aurora':[(437,140,32,24),(483,159,8,8)],
}
SPRITE_EYES={'bard':[(24,13,6,1)]}
EC={'bard':'#f0d49c','tide':'#f2c7b0'}   # lid colour where sampling picks up hair
def jpath(i): return f'art/sprites/{i}_body.json' if os.path.exists(f'art/sprites/{i}_body.json') else f'art/callers/{i}_body.json'
def ppath(i): return jpath(i).replace('.json','.png')
def convert(i):
    if i in SPRITE_EYES: return [list(r) for r in SPRITE_EYES[i]]
    m=json.load(open(jpath(i)))['map']; x0,y0,s=m
    return [[round((x-x0)*s,1),round((y-y0)*s,1),max(1,round(w*s,1)),max(1,round(h*s,1))] for x,y,w,h in EYES[i]]
def skin(i,rects):
    im=np.asarray(Image.open(ppath(i)).convert('RGBA')); H,W=im.shape[:2]; px=[]
    for x,y,w,h in rects:
        x0,y0,x1,y1=int(x)-2,int(y)-2,int(x+w)+3,int(y+h)+3
        for yy in range(max(0,y0),min(H,y1)):
            for xx in range(max(0,x0),min(W,x1)):
                if x0+2<=xx<x1-2 and y0+2<=yy<y1-2: continue   # the ring around the eye, not the eye
                p=im[yy,xx]
                if p[3]>200 and 0.3*p[0]+0.59*p[1]+0.11*p[2]>70: px.append(p[:3])
    if not px: return None
    c=np.median(np.array(px),axis=0); return '#%02x%02x%02x'%tuple(int(v) for v in c)
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--check':
        ids=sys.argv[2].split(','); tiles=[]; D='art/gemini_test/'
        for i in ids:
            f=D+(f'chars/{i}_body.jpg' if os.path.exists(D+f'chars/{i}_body.jpg') else f'callers/{i}_body.jpg'); a=Image.open(f).convert('RGB'); d=ImageDraw.Draw(a)
            for x,y,w,h in EYES[i]: d.rectangle([x,y,x+w,y+h],outline=(255,255,0),width=2)
            cx=sum(x+w/2 for x,y,w,h in EYES[i])/len(EYES[i]); cy=sum(y+h/2 for x,y,w,h in EYES[i])/len(EYES[i])
            c=a.crop((int(cx-85),int(cy-55),int(cx+85),int(cy+55))).resize((340,220),Image.NEAREST); ImageDraw.Draw(c).text((4,4),i,fill=(0,255,255)); tiles.append(c)
        sh=Image.new('RGB',(340*3,((len(tiles)+2)//3)*224))
        for k,t in enumerate(tiles): sh.paste(t,((k%3)*340,(k//3)*224))
        os.makedirs('/tmp/fbout',exist_ok=True); sh.save('/tmp/fbout/eyecheck.png'); print(sh.size)
    else:
        for i in list(EYES)+list(SPRITE_EYES):
            r=convert(i); ec=EC.get(i) or skin(i,r); J=json.load(open(jpath(i))); J['eye']=r; J['ec']=ec; json.dump(J,open(jpath(i),'w')); print(i,r,ec)
