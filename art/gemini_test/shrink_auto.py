# Shrink one prop in a stage source. Gemini removes the prop (clean fill); the difference to the original gives the cut-out mask; the prop is pasted back smaller.
# usage: python3 shrink_auto.py ID x0 y0 x1 y1 SCALE bottom|top "what to remove"     -> writes stages/ID_edit.png (review, then move over stages/ID.jpg)
import sys,subprocess,io,json,base64,numpy as np
from PIL import Image,ImageFilter,ImageDraw
from scipy import ndimage as ndi
i=sys.argv[1]; box=tuple(map(int,sys.argv[2:6])); sc=float(sys.argv[6]); anchor=sys.argv[7]; what=sys.argv[8]
subprocess.run(['python3','edit_stage.py',i,f"Remove {what} completely, filling that spot with the surrounding background (floor, wall or table) matching the lighting and perspective."],check=True)
orig=Image.open(f'stages/{i}.jpg').convert('RGB'); rem=Image.open(f'stages/{i}_edit.png').convert('RGB').resize(orig.size)
x0,y0,x1,y1=box; a=np.asarray(orig).astype(int); b=np.asarray(rem).astype(int)
diff=np.abs(a-b).sum(axis=2)>60; sub=np.zeros_like(diff); sub[y0:y1,x0:x1]=diff[y0:y1,x0:x1]
sub=ndi.binary_closing(sub,iterations=2); sub=ndi.binary_fill_holes(sub); lab,n=ndi.label(sub); sz=ndi.sum(sub,lab,range(1,n+1)); sub=lab==(1+int(np.argmax(sz)))
sub=ndi.binary_dilation(sub,iterations=1)
ys,xs=np.where(sub); px0,py0,px1,py1=xs.min(),ys.min(),xs.max()+1,ys.max()+1; print('prop bbox',px0,py0,px1,py1)
alpha=Image.fromarray((sub*255).astype(np.uint8)); gm=alpha.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(6))
base=Image.composite(rem,orig,gm)      # take the clean patch from the removed version, only around the prop
prop=orig.crop((px0,py0,px1,py1)); al=alpha.crop((px0,py0,px1,py1)); nw,nh=round(prop.width*sc),round(prop.height*sc)
prop=prop.resize((nw,nh),Image.LANCZOS); al=al.resize((nw,nh),Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.5))
cx=(px0+px1)//2; px=cx-nw//2; py=(py1-nh) if anchor=='bottom' else py0
base.paste(prop,(px,py),al); base.save(f'stages/{i}_edit.png'); print('saved',i)
