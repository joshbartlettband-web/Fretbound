# v1.86: change something in a painted pose atlas without new pose sheets: four poses per Gemini edit, scaled up on magenta,
# then scaled back into the atlas cells and keyed. Every call is logged with its cost in spend.log.
# usage: python3 atlas_edit.py ID OUTDIR "instruction" [model]   (reads poses_master/ID_atlas.png + ../poses/ID_meta.json; writes OUTDIR/ID_atlas.png and group pngs)
import json,base64,subprocess,sys,io,os,time
import numpy as np
from PIL import Image
PRICE={'gemini-2.5-flash-image':0.039,'gemini-3-pro-image':0.134,'gemini-3-pro-image-preview':0.134}
def log_spend(model,what):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'spend.log'),'a') as f: f.write(f"{time.strftime('%Y-%m-%d %H:%M')}\t{model}\t{PRICE.get(model,0):.3f}\t{what}\n")
def edit(img,prompt,model,aspect,tag):
    buf=io.BytesIO(); img.save(buf,'PNG'); src=base64.b64encode(buf.getvalue()).decode()
    body=json.dumps({"contents":[{"parts":[{"text":prompt},{"inlineData":{"mimeType":"image/png","data":src}}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect}}})
    req=f"/tmp/req_atlas_{tag}.json"; open(req,"w").write(body)
    for _ in range(3):
        r=subprocess.run(["curl","-sS","-X","POST",f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent","-H","Content-Type: application/json","-d","@"+req],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except Exception: continue
        for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]):
            if 'inlineData' in p: log_spend(model,tag); return Image.open(io.BytesIO(base64.b64decode(p['inlineData']['data']))).convert('RGB')   # only a delivered image is billed and logged
        print('retry',tag,str(d)[:200])
    return None
if __name__=='__main__':
    cid,out,ins=sys.argv[1],sys.argv[2],sys.argv[3]; model=sys.argv[4] if len(sys.argv)>4 else 'gemini-2.5-flash-image'
    os.makedirs(out,exist_ok=True)
    A=Image.open(f'poses_master/{cid}_atlas.png').convert('RGBA'); M=json.load(open(f'../poses/{cid}_meta.json')); cw,ch=M['cw'],M['ch']
    W,H=1664,936; S=min(5,W//(cw*4),H//ch); MAG=(0,255,0)   # S fits four cells on the canvas (cells differ in size per character); green, not magenta: purple and pink guitars would key out
    prompt=("Edit this pixel-art sprite sheet of four poses of the same character on a flat bright green background. Keep everything else exactly the same: "
            "the same four poses, positions, sizes, body, clothes, face, hands, colours, pixel style and the flat green background. "+ins+" Change it the same way in all four poses. Do not add anything else.")
    res=np.asarray(A).copy()
    groups=[int(x) for x in os.environ.get('EDIT_GROUPS','0,1,2,3').split(',')]
    if os.path.exists(f'{out}/{cid}_atlas.png'): res=np.asarray(Image.open(f'{out}/{cid}_atlas.png').convert('RGBA')).copy()   # redo only some groups
    orig=np.asarray(A).astype(int)
    for g in groups:
        idx=[g*4+k for k in range(4)]; strip=Image.new('RGB',(cw*4,ch),MAG)
        for k,i in enumerate(idx):
            c=A.crop(((i%8)*cw,(i//8)*ch,(i%8)*cw+cw,(i//8)*ch+ch)); bg=Image.new('RGBA',c.size,MAG+(255,)); bg.alpha_composite(c); strip.paste(bg.convert('RGB'),(k*cw,0))
        big=strip.resize((cw*4*S,ch*S),Image.NEAREST); canvas=Image.new('RGB',(W,H),MAG); ox,oy=(W-big.width)//2,(H-big.height)//2; canvas.paste(big,(ox,oy)); canvas.save(f'{out}/g{g}_in.png')
        e=edit(canvas,prompt,model,'16:9',f'{cid}_g{g}')
        if e is None: print('failed group',g); sys.exit(1)
        e=e.resize((W,H),Image.LANCZOS); e.save(f'{out}/g{g}_out.png')
        small=np.asarray(e.crop((ox,oy,ox+big.width,oy+big.height)).resize((cw*4,ch),Image.BOX)).astype(int)
        r,gg,b=small[...,0],small[...,1],small[...,2]; key=(gg-r>90)&(gg-b>90)&(gg>150)
        for k,i in enumerate(idx):
            x0,y0=(i%8)*cw,(i//8)*ch; cell=small[:,k*cw:(k+1)*cw]; al=~key[:,k*cw:(k+1)*cw]
            # keep the original pixels wherever the edit did not really change them (face, robe stay crisp); take the new ones where it did (the guitar)
            o=orig[y0:y0+ch,x0:x0+cw]; oa=o[:,:,3]>140; d=np.abs(cell-o[:,:,:3]).sum(2); ch_=(d>90)|(al!=oa)
            from scipy import ndimage as ndi
            ch_=ndi.binary_opening(ch_,iterations=1); ch_=ndi.binary_dilation(ch_,iterations=1)
            lab,n=ndi.label(ch_); 
            if n: sz=ndi.sum(ch_,lab,range(1,n+1)); ch_=np.isin(lab,[i+1 for i,v in enumerate(sz) if v>=12])
            res[y0:y0+ch,x0:x0+cw,:3]=np.where(ch_[...,None],cell,o[:,:,:3]); res[y0:y0+ch,x0:x0+cw,3]=np.where(ch_,al,oa)*255
        print('group',g,'done',flush=True)
    im=Image.fromarray(res.astype(np.uint8),'RGBA'); al=np.asarray(im)[:,:,3]>140
    q=Image.fromarray(np.asarray(im)[:,:,:3]).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    Image.fromarray(np.dstack([np.asarray(q),(al*255).astype(np.uint8)])).save(f'{out}/{cid}_atlas.png',optimize=True); print('saved',f'{out}/{cid}_atlas.png')
