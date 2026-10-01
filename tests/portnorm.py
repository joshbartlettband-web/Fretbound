from PIL import Image, ImageDraw
import numpy as np
# measured on the 176 cards: eye-to-chin size, eye line y, face centre x
M={'bard':(25,33,77),'monk':(20,33,58),'hermit':(20,35,61),'busker':(20,31,75),'luthier':(30,41,105),'carto':(25,40,103)}
OUT_BG=(36,16,12)
def crop_norm(n,Ft,size,eye_t=0.24,fx_t=0.47):
    im=Image.open(f'handoff/art/{n}_card.png').convert('RGBA'); F,ey,fx=M[n]
    arr=np.array(im)
    if (arr[1,:,3]>0).sum()<(arr[0,:,3]>0).sum()*0.5: arr[0,:,3]=0   # stray edge line from the original cutout
    im=Image.fromarray(arr)
    C=176*F/Ft
    if abs(C/176-1)<0.07 or C>176: C=176
    C=int(round(C)); left=int(round(fx-fx_t*C)); top=int(round(ey-eye_t*C))
    left=max(0,min(176-C,left)); top=min(176-C,top)          # padding only allowed above the head
    canvas=Image.new('RGBA',(176,176+64),(0,0,0,0)); canvas.paste(im,(0,64))
    cr=canvas.crop((left,top+64,left+C,top+64+C))
    if C==size: return cr
    a=np.asarray(cr).astype(np.float32); rgb=a[...,:3].copy(); al=a[...,3]
    rgb[al<128]=OUT_BG
    big=Image.fromarray(rgb.astype(np.uint8)).resize((C*4,C*4),Image.NEAREST).resize((size,size),Image.BOX)
    m=Image.fromarray(((al>=128)*255).astype(np.uint8)).resize((C*4,C*4),Image.NEAREST).resize((size,size),Image.BOX)
    q=np.asarray(big.quantize(colors=48,method=Image.Quantize.MEDIANCUT).convert('RGB'))
    mk=np.asarray(m)>110
    out=np.zeros((size,size,4),np.uint8); out[...,:3]=q; out[...,3]=mk*255
    return Image.fromarray(out)
names=list(M)
cards={n:crop_norm(n,27,176) for n in names}; tiles={n:crop_norm(n,30,96,eye_t=0.26) for n in names}
for n in names: cards[n].save(f'port/{n}_card.png'); tiles[n].save(f'port/{n}_tile.png')
def on_bg(im,sz): b=Image.new('RGBA',im.size,(26,12,10,255)); b.alpha_composite(im); return b.resize((sz,sz),Image.NEAREST).convert('RGB')
sheet=Image.new('RGB',(6*186,186*3+10),'black')
for k,n in enumerate(names):
    sheet.paste(on_bg(Image.open(f'handoff/art/{n}_card.png').convert('RGBA'),176),(k*186,0))
    sheet.paste(on_bg(cards[n],176),(k*186,186))
    sheet.paste(on_bg(Image.open(f'handoff/art/{n}_tile.png').convert('RGBA'),88),(k*186,372+5)); sheet.paste(on_bg(tiles[n],88),(k*186+92,372+5))
sheet.save('port_cmp.png'); print(sheet.size)
