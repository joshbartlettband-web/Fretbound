# Gemini backdrops -> title plates: find the horizon, scale to 640 wide, align the horizon to the game's (y=224), 64 colours, crisp edges
import numpy as np
from PIL import Image
MAP={'na':'15677','af':'15679','sa':'15681','eu':'15689','as':'15683','oc':'15684','an':'15685'}
HZ=224
for cid,f in MAP.items():
    im=Image.open(f'/mnt/user-data/uploads/{f}.jpg').convert('RGB'); a=np.asarray(im).astype(float); H,W,_=a.shape
    lum=a.mean(axis=2); rowm=lum.mean(axis=1); rows=lum.std(axis=1)
    ground=rowm[-60:].mean(); thr=ground+10
    hz=None
    if cid=='na': hz=579
    if cid=='eu': hz=540
    for y in ([] if hz else range(int(H*0.45),H-12)):
        if all(rowm[y+k]<thr for k in range(10)) and rowm[y-2]>thr+4: hz=y; break
    s=640/W; h=round(H*s); im2=im.resize((640,h),Image.LANCZOS); hz2=round(hz*s); off=HZ-hz2
    plate=Image.new('RGB',(640,HZ)); plate.paste(im2,(0,off))
    if off>0:
        top=im2.crop((0,0,640,1)).resize((640,off)); plate.paste(top,(0,0))
    q=plate.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    q.save(f'/home/claude/plates/{cid}.png',optimize=True)
    import os; print(cid,'horizon at',hz,'of',H,f'({hz/H:.0%})','-> shifted',off,'px |',os.path.getsize(f'/home/claude/plates/{cid}.png')//1024,'KB')
ims=[Image.open(f'/home/claude/plates/{c}.png') for c in MAP]
S=Image.new('RGB',(2*644,4*228),'black')
for i,im in enumerate(ims): S.paste(im,((i%2)*644,(i//2)*228))
S.save('/home/claude/plates/plates_sheet.png')
