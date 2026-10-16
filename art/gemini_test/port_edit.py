# v1.86: swap the guitar in a caller's 128px menu portrait (RIVAL_PORT): upscale 8x on green, Gemini edit, back to 128 by block median, key, despill.
# usage: python3 port_edit.py ID "guitar description" [model]   -> port_edit/ID.png (ungraded) ; embed with --embed ID ...
import sys,os,json,base64,io
import numpy as np
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from atlas_edit import edit
R='/home/user/Fretbound/'
def run(cid,desc,model):
    src=Image.open(R+f'art/_ungraded/RIVAL_PORT/{cid}.png').convert('RGBA'); bg=Image.new('RGBA',src.size,(0,255,0,255)); bg.alpha_composite(src)
    big=bg.convert('RGB').resize((1024,1024),Image.NEAREST)
    prompt=("Edit this pixel-art character portrait on a flat bright green background. Keep everything else exactly the same: same character, face, clothes, colours, framing, pixel style and the flat green background. "
            f"Replace only the guitar they are holding with {desc}. It is NOT a Stratocaster: a clearly different body outline. Same hands, same angle. There must be exactly ONE guitar with exactly ONE neck and ONE headstock: the old guitar, its neck and its headstock are completely gone. Do not add anything else.")
    e=edit(big,prompt,model,'1:1',f'port_{cid}')
    if e is None: print('failed',cid); return
    os.makedirs('port_edit',exist_ok=True); e.save(f'port_edit/{cid}_big.png')
    a=np.asarray(e.resize((1024,1024),Image.LANCZOS)).astype(int).reshape(128,8,128,8,3).transpose(0,2,1,3,4).reshape(128,128,64,3)
    s=np.median(a,axis=2)
    key=(s[...,1]>150)&(s[...,0]<130)&(s[...,2]<130)
    sp=s[...,1]-np.maximum(s[...,0],s[...,2]); s[...,1]-=np.where((sp>0)&~key,sp,0)
    al=~key
    out=np.dstack([s.clip(0,255),al*255]).astype(np.uint8)
    q=Image.fromarray(out[:,:,:3]).quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    Image.fromarray(np.dstack([np.asarray(q),out[:,:,3]])).save(f'port_edit/{cid}.png'); print('saved',cid)
def embed(ids):
    s=open(R+'index.html',encoding='utf-8').read(); a=s.index('const RIVAL_PORT=')+len('const RIVAL_PORT='); b=s.index(';\n',a); P=json.loads(s[a:b])
    for cid in ids: P[cid]='data:image/png;base64,'+base64.b64encode(open(f'port_edit/{cid}.png','rb').read()).decode()
    open(R+'index.html','w',encoding='utf-8').write(s[:a]+json.dumps(P,separators=(',',':'))+s[b:]); print('embedded',ids)
if __name__=='__main__':
    if sys.argv[1]=='--embed': embed(sys.argv[2:])
    else: run(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else 'gemini-3-pro-image')
