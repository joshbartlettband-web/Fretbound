# Painted pose sheets -> a 16-pose atlas per character, with consistency checks.
# usage: python3 tests/procposes.py ID HEIGHT [A_n B_n]    -> art/poses/<id>_atlas.png + <id>_meta.json (+ a check sheet and report)
#        python3 tests/procposes.py --embed ID ...         -> writes POSE_SRC / POSE_META in index.html
# Sheets come from art/gemini_test/sheets/gen_sheet.py (out/<id>_A_<n>.png, out/<id>_B_<n>.png: 4x2 poses each, flat magenta).  Every pose of a character is scaled by ONE factor
# (set so the idle pose is HEIGHT px tall), put on a common baseline with the feet at the cell's centre line, and the atlas shares one 48-colour palette.
import sys,os,json,base64
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0,'art/gemini_test/sheets')
import poses as P
NAMES=[n for n,_ in P.A]+[n for n,_ in P.B]
def key(im):
    a=np.asarray(im.convert('RGB')).astype(int); bg=np.median(np.concatenate([a[:6].reshape(-1,3),a[-6:].reshape(-1,3),a[:,:6].reshape(-1,3),a[:,-6:].reshape(-1,3)]),axis=0)
    d=np.abs(a-bg).sum(axis=2); fg=d>150                                              # every pixel near the background colour goes, enclosed gaps included
    fg&=~((a[:,:,0]-a[:,:,1]>60)&(a[:,:,2]-a[:,:,1]>40)&(a[:,:,0]>120))              # and any magenta-tinted fringe
    fg=ndi.binary_opening(fg,iterations=1); return fg
def split(path):
    im=Image.open(path).convert('RGB'); fg=key(im); H,W=fg.shape
    lab,n=ndi.label(ndi.binary_dilation(fg,iterations=14)); lab=lab*fg                  # dilate to join a tail or a raised fist to its body, then keep only real pixels
    sz=ndi.sum(fg,lab,range(1,n+1)); keep=[i+1 for i in np.argsort(sz)[::-1][:8]] if n>=8 else None
    if keep is None or sz[np.array(keep)-1].min()<0.05*sz.max(): return im,fg,None
    objs=ndi.find_objects(lab); cells=[]
    for k in keep:
        sl=objs[k-1]; cy=(sl[0].start+sl[0].stop)/2; cx=(sl[1].start+sl[1].stop)/2; cells.append((int(cy>H/2),cx,k))
    cells.sort(); out=[]
    for r in (0,1):
        row=sorted([c for c in cells if c[0]==r],key=lambda c:c[1]); out+= [c[2] for c in row]
    if len(out)!=8: return im,fg,None
    return im,fg,[(lab==k) for k in out]
def build(cid,HEIGHT,an=1,bn=1,K=None):
    D='art/gemini_test/sheets/out/'; sprites=[]; report={'id':cid,'issues':[]}
    for which,n in (('A',an),('B',bn)):
        im,fg,masks=split(f'{D}{cid}_{which}_{n}.png')
        if masks is None: report['issues'].append(f'sheet {which}: could not find 8 separate figures'); return None,report
        a=np.asarray(im)
        for m in masks:
            ys,xs=np.where(m); x0,y0,x1,y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
            rgba=np.dstack([a,(m*255).astype(np.uint8)])[y0:y1,x0:x1]; low=ys>ys.max()-max(4,int((y1-y0)*0.04)); fx=float(np.median(xs[low])-x0)
            sprites.append((Image.fromarray(rgba),fx))
    idle=sprites[0][0]; s=HEIGHT/idle.height; cw=0; ch=0; sc=[]
    for im,fx in sprites:
        w,h=max(1,round(im.width*s)),max(1,round(im.height*s)); r=im.resize((w,h),Image.LANCZOS); sc.append((r,fx*s)); 
    cw=int(max(max(r.width for r,_ in sc),0))+8; left=max(fx for _,fx in sc); right=max(r.width-fx for r,fx in sc); cw=int(left+right)+6; ch=max(r.height for r,_ in sc)+4
    FX=int(left)+3; FY=ch-2; atlas=Image.new('RGBA',(cw*8,ch*2),(0,0,0,0)); hts=[]
    for i,(r,fx) in enumerate(sc):
        ox=(i%8)*cw+FX-int(round(fx)); oy=(i//8)*ch+FY-r.height; atlas.alpha_composite(r,(ox,oy)); hts.append(r.height)
    # one palette for the whole atlas
    arr=np.asarray(atlas).copy(); al=arr[:,:,3]>140
    q=Image.fromarray(arr[:,:,:3]).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    out=Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8))
    # --- checks: the figures should be one size, nothing cut off, nothing missing
    ih=hts[0]
    for k in (1,2,3,4,5,6,7): 
        if abs(hts[k]-ih)/ih>0.10: report['issues'].append(f'{NAMES[k]}: {hts[k]}px tall vs idle {ih}px')
    for i,(r,fx) in enumerate(sc):
        wd=r.width; 
        if wd>cw-4: report['issues'].append(f'{NAMES[i]}: wider than its cell')
    report['heights']=dict(zip(NAMES,hts)); report['cell']=[cw,ch]; report['scale']=round(s,3)
    return (out,dict(cw=cw,ch=ch,fx=FX,fy=FY,n=16,names=NAMES,h=HEIGHT)),report
def sheet_png(cid,out):
    cw=out[1]['cw']; ch=out[1]['ch']; im=out[0]; bg=Image.new('RGBA',im.size,(90,60,50,255)); bg.alpha_composite(im); return bg.convert('RGB')
def embed(ids):
    s=open('index.html',encoding='utf-8').read(); src={}; meta={}
    for f in sorted(os.listdir('art/poses')):
        if f.endswith('_atlas.png'):
            i=f[:-10]; src[i]='data:image/png;base64,'+base64.b64encode(open('art/poses/'+f,'rb').read()).decode(); meta[i]=json.load(open(f'art/poses/{i}_meta.json'))
    B,E='/*POSES:BEGIN*/','/*POSES:END*/'; blk=B+'\nconst POSE_SRC='+json.dumps(src,separators=(',',':'))+', POSE_META='+json.dumps(meta,separators=(',',':'))+';\n'+E
    if B in s: a=s.index(B); b=s.index(E)+len(E); s=s[:a]+blk+s[b:]
    else:
        m='/*SPRITES:BEGIN*/'; assert s.count(m)==1; s=s.replace(m,blk+'\n'+m)
    open('index.html','w',encoding='utf-8').write(s); print('embedded',list(src))
if __name__=='__main__':
    if sys.argv[1]=='--embed': embed(sys.argv[2:])
    else:
        cid,H=sys.argv[1],int(sys.argv[2]); an=int(sys.argv[3]) if len(sys.argv)>3 else 1; bn=int(sys.argv[4]) if len(sys.argv)>4 else 1
        res,rep=build(cid,H,an,bn)
        if res is None: print(rep); sys.exit(1)
        os.makedirs('art/poses',exist_ok=True); out,meta=res; out.save(f'art/poses/{cid}_atlas.png',optimize=True); json.dump(meta,open(f'art/poses/{cid}_meta.json','w'))
        sheet_png(cid,res).save(f'/tmp/fbout/atlas_{cid}.png'); print(json.dumps(rep)); print(os.path.getsize(f'art/poses/{cid}_atlas.png')//1024,'KB',out.size)
