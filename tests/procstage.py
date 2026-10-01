# Gemini stage plate -> game plate: scale to 640 wide, crop to 640x240 (CROP rows off the top), 64 colours, no dither
import sys,os
from PIL import Image
src,out,crop=sys.argv[1],sys.argv[2],int(sys.argv[3])
im=Image.open(src).convert('RGB'); w,h=im.size; s=640/w; h2=round(h*s)
im2=im.resize((640,h2),Image.LANCZOS).crop((0,crop,640,crop+240))
im2.quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB').save(out,optimize=True)
print(out,im2.size,os.path.getsize(out)//1024,'KB (scaled height',h2,')')
