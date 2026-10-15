# "Hanging out" sheets (no instruments) -> one 8-cell atlas per character for the Van screen.
# usage: python3 tests/prochang.py [id ...]         art/gemini_test/sheets/out/hang_<id>_<n>.png -> art/hang/<id>_hang.png + <id>_meta.json (masters in art/gemini_test/hang_master)
#        python3 tests/prochang.py --embed          writes HANG_SRC / HANG_META into index.html (before the pedal block)
import sys,os,json,base64,glob,re
sys.path.insert(0,'tests'); sys.path.insert(0,'art/gemini_test/sheets')
import numpy as np
from PIL import Image
import procposes as PP
import gen_sheet as GS
IDS='bard monk hermit busker luthier carto smith wizard herald journey lou rosa dee jo hale tam brass brassb brassc'.split()
MASTER='art/gemini_test/hang_master'
def build(cid,n=1):
    im,fg,masks=PP.split(f'art/gemini_test/sheets/out/hang_{cid}_{n}.png')
    if masks is None: return None,'could not find 8 figures'
    a=np.asarray(im); sp=[]
    for m in masks:
        ys,xs=np.where(m); x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
        rgba=np.dstack([a,(m*255).astype(np.uint8)])[y0:y1,x0:x1]; low=ys>ys.max()-max(4,int((y1-y0)*0.04)); sp.append((Image.fromarray(rgba),float(np.median(xs[low])-x0)))
    H=GS.CH[cid]['height']; ref=float(np.median([s.height for i,(s,_) in enumerate(sp) if i!=7])); k=H/ref
    sc=[(s.resize((max(1,round(s.width*k)),max(1,round(s.height*k))),Image.LANCZOS),fx*k) for s,fx in sp]
    left=max(fx for _,fx in sc); right=max(s.width-fx for s,fx in sc); cw=int(left+right)+6; ch=max(s.height for s,_ in sc)+4; fx0=int(left)+3
    out=Image.new('RGBA',(cw*8,ch),(0,0,0,0))
    for i,(s,fx) in enumerate(sc):
        arr=np.asarray(s).copy(); arr[:,:,3]=(arr[:,:,3]>150)*255; out.paste(Image.fromarray(arr),(i*cw+fx0-int(round(fx)),ch-2-s.height))
    arr=np.asarray(out); al=arr[:,:,3]>0
    q=Image.fromarray(arr[:,:,:3]).quantize(colors=64,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    if os.environ.get('POSE_NEAREST'):   # as in procposes: a near-grey pixel that came out strongly coloured keeps its own grey (the Journeyman's beard)
        sa=arr[:,:,:3].astype(int); qa=np.asarray(q).copy(); sch=sa.max(axis=2)-sa.min(axis=2); bad=(sch<40)&((qa.astype(int).max(axis=2)-qa.astype(int).min(axis=2))>sch+20)
        qa[bad]=((sa//16)*16+8).clip(0,255).astype(np.uint8)[bad]; q=Image.fromarray(qa)
    o=np.dstack([np.asarray(q),(al*255).astype(np.uint8)])
    return Image.fromarray(o),dict(cw=cw,ch=ch,fx=fx0,fy=ch-2,n=8,h=H)
def embed(path='index.html'):
    src={}; meta={}
    for cid in IDS:
        f=f'art/hang/{cid}_hang.png'
        if os.path.exists(f): src[cid]='data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode(); meta[cid]=json.load(open(f'art/hang/{cid}_meta.json'))
    block='/*HANG:BEGIN*/\nconst HANG_SRC='+json.dumps(src,separators=(',',':'))+';\nconst HANG_META='+json.dumps(meta,separators=(',',':'))+';\n/*HANG:END*/'
    s=open(path,encoding='utf-8').read()
    if '/*HANG:BEGIN*/' in s: a=s.index('/*HANG:BEGIN*/'); b=s.index('/*HANG:END*/')+len('/*HANG:END*/'); s=s[:a]+block+s[b:]
    else: m='/*PEDALS:BEGIN*/'; assert s.count(m)==1; s=s.replace(m,block+'\n'+m)
    open(path,'w',encoding='utf-8').write(s); print('embedded',len(src),'hang sets')
if __name__=='__main__':
    if '--embed' in sys.argv:
        os.makedirs('art/hang',exist_ok=True)
        for cid in IDS:                                  # masters are ungraded; art/hang gets a copy so the grade never compounds
            f=f'{MASTER}/{cid}_hang.png'
            if os.path.exists(f): open(f'art/hang/{cid}_hang.png','wb').write(open(f,'rb').read())
        embed()
    else:
        os.makedirs('art/hang',exist_ok=True); os.makedirs(MASTER,exist_ok=True)
        for cid in (sys.argv[1:] or IDS):
            ns=sorted(int(re.search(r'_(\d+)\.png',f).group(1)) for f in glob.glob(f'art/gemini_test/sheets/out/hang_{cid}_*.png'))
            if not ns: continue
            n=ns[-1] if os.environ.get('N') is None else int(os.environ['N'])
            r,meta=build(cid,n)
            if r is None: print(cid,'FAILED',meta); continue
            r.save(f'{MASTER}/{cid}_hang.png',optimize=True); json.dump(meta,open(f'art/hang/{cid}_meta.json','w')); print(cid,n,meta)
