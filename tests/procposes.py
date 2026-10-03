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
CALM_X,CALM_Y=4,4
MASTER='art/gemini_test/poses_master'   # UNGRADED atlases (tests/grade.py never touches art/gemini_test); --embed copies them to art/poses and embeds those, so grading can never compound   # playing poses: the head may drift this many pixels from idle
def key(im):
    a=np.asarray(im.convert('RGB')).astype(int); bg=np.median(np.concatenate([a[:6].reshape(-1,3),a[-6:].reshape(-1,3),a[:,:6].reshape(-1,3),a[:,-6:].reshape(-1,3)]),axis=0)
    d=np.abs(a-bg).sum(axis=2); fg=d>150                                              # every pixel near the background colour goes, enclosed gaps included
    near=ndi.binary_dilation(~fg,iterations=3)                                        # a magenta-tinted fringe goes too, but only next to the background (cream fur and white cloth inside a figure picks up a pink cast)
    fg&=~((a[:,:,0]-a[:,:,1]>60)&(a[:,:,2]-a[:,:,1]>40)&(a[:,:,0]>120)&near)
    fg=ndi.binary_opening(fg,iterations=max(1,round(a.shape[1]/2752))); return fg
def grid_split(fg):
    """Figures touch (a peacock's tail fan, a wide stance): cut the 4x2 grid along the quietest vertical gutters and the quietest horizontal gutter, then take each cell's own figure."""
    H,W=fg.shape; col=fg.sum(axis=0).astype(float); row=fg.sum(axis=1).astype(float)
    def quiet(v,c,span):
        lo,hi=max(1,int(c-span)),min(len(v)-1,int(c+span)); w=np.convolve(v,np.ones(9)/9,mode='same'); return int(lo+np.argmin(w[lo:hi]))
    xs=[0]+[quiet(col,W*k/4,W*0.07) for k in (1,2,3)]+[W]; ym=quiet(row,H/2,H*0.08); ys=[0,ym,H]
    masks=[]
    for r in (0,1):
        for c in range(4):
            m=np.zeros_like(fg); sub=fg[ys[r]:ys[r+1],xs[c]:xs[c+1]]
            lab,n=ndi.label(ndi.binary_dilation(sub,iterations=max(4,round(10*W/2752)))); lab=lab*sub
            if n==0: return None
            sz=ndi.sum(sub,lab,range(1,n+1)); big=[i+1 for i in range(n) if sz[i]>=0.12*sz.max()]
            m[ys[r]:ys[r+1],xs[c]:xs[c+1]]=np.isin(lab,big); masks.append(m)
    if any(m.sum()<400 for m in masks): return None
    return masks
def split(path):
    im=Image.open(path).convert('RGB'); fg=key(im); H,W=fg.shape
    lab,n=ndi.label(ndi.binary_dilation(fg,iterations=max(6,round(14*W/2752)))); lab=lab*fg                  # dilate to join a tail or a raised fist to its body, then keep only real pixels
    sz=ndi.sum(fg,lab,range(1,n+1)); keep=[i+1 for i in np.argsort(sz)[::-1][:8]] if n>=8 else None
    if keep is None or sz[np.array(keep)-1].min()<0.05*sz.max(): return im,fg,grid_split(fg)
    objs=ndi.find_objects(lab); cells=[]
    for k in keep:
        sl=objs[k-1]; cy=(sl[0].start+sl[0].stop)/2; cx=(sl[1].start+sl[1].stop)/2; cells.append((int(cy>H/2),cx,k))
    cells.sort(); out=[]
    for r in (0,1):
        row=sorted([c for c in cells if c[0]==r],key=lambda c:c[1]); out+= [c[2] for c in row]
    if len(out)!=8: return im,fg,grid_split(fg)
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
    # REGISTER every pose against idle: Gemini draws each pose of a sheet at a slightly different size and a little off to the side, so the figure would grow, shrink and slide when poses swap.
    # For each pose, search a scale (0.88 to 1.12), a sideways shift and a lift that best overlap the bottom third of idle (legs, boots, robe), and apply it. Poses whose legs really differ keep their own size.
    def band(im,fx,hb):
        a=np.asarray(im)[:,:,3]>0; return a[-hb:],fx
    raw_areas=[(np.asarray(r)[:,:,3]>0).sum() for r,_ in sc]      # measured BEFORE registration: a pose drawn without its instrument is much smaller than idle
    idle_r,idle_fx=sc[0]; hb=max(8,int(idle_r.height*0.33)); IB,IFX=band(idle_r,idle_fx,hb); reg=[(1.0,0.0,0)]; reg_report={}
    for i in range(1,len(sc)):
        r,fx=sc[i]; best=(-1,1.0,0.0,0)
        for k in np.arange(0.92,1.081,0.02):
            w2,h2=max(1,round(r.width*k)),max(1,round(r.height*k)); a=np.asarray(r.resize((w2,h2),Image.NEAREST))[:,:,3]>0; f2=fx*k
            for dy in (-2,-1,0,1,2):
                hh=min(hb,h2); rows=a[h2-hh-dy:h2-dy] if dy>=0 else a[h2-hh-dy:h2-dy] 
                if rows.shape[0]!=hh: continue
                for dx in range(-8,9):
                    # idle band columns: [0,IB.shape[1]) with anchor IFX; pose band columns shifted so its anchor sits at IFX+dx
                    off=int(round(IFX+dx-f2)); ov=np.zeros((hh,IB.shape[1]),bool); x0=max(0,off); x1=min(IB.shape[1],off+rows.shape[1])
                    if x1<=x0: continue
                    ov[:,x0:x1]=rows[:,x0-off:x1-off]; ib=IB[-hh:]; inter=(ov&ib).sum(); uni=(ov|ib).sum()
                    iou=inter/max(1,uni)
                    if iou>best[0]: best=(iou,float(k),float(dx),dy)
        if best[0]>=0.62: reg.append((best[1],best[2],best[3])); reg_report[NAMES[i]]=(round(best[1],2),round(best[2]),best[3],round(best[0],2))
        else: reg.append((1.0,0.0,0)); reg_report[NAMES[i]]=('own',round(best[0],2))
    sc2=[sc[0]]
    for i in range(1,len(sc)):
        r,fx=sc[i]; k,dx,dy=reg[i]
        if k!=1.0: r=r.resize((max(1,round(r.width*k)),max(1,round(r.height*k))),Image.LANCZOS)
        sc2.append((r,fx*k-dx))
    sc=sc2; dys=[0]+[reg[i][2] for i in range(1,len(sc))]
    left=max(fx for _,fx in sc); right=max(r.width-fx for r,fx in sc); cw=int(left+right)+6; ch=max(r.height for r in [x for x,_ in sc])+8
    FX=int(left)+3; FY=ch-4; atlas=Image.new('RGBA',(cw*8,ch*2),(0,0,0,0)); hts=[]
    for i,(r,fx) in enumerate(sc):
        ox=(i%8)*cw+FX-int(round(fx)); oy=(i//8)*ch+FY-r.height+dys[i]; atlas.alpha_composite(r,(ox,oy)); hts.append(r.height)
    # one palette for the whole atlas
    arr=np.asarray(atlas).copy(); al=arr[:,:,3]>140
    q=Image.fromarray(arr[:,:,:3]).quantize(colors=48,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    out=Image.fromarray(np.dstack([np.asarray(q),al*255]).astype(np.uint8))
    import outlinefix; oa=np.asarray(out).copy()                                  # the same one-pixel outline on every pose (tests/outlinefix.py)
    for i in range(16): y0,x0=(i//8)*ch,(i%8)*cw; oa[y0:y0+ch,x0:x0+cw]=outlinefix.fix_cell(oa[y0:y0+ch,x0:x0+cw])
    out=Image.fromarray(oa)
    # --- checks: the figures should be one size, nothing cut off, nothing missing
    ih=hts[0]
    for k in (1,2,3,4,5,6,7): 
        if abs(hts[k]-ih)/ih>0.10: report['issues'].append(f'{NAMES[k]}: {hts[k]}px tall vs idle {ih}px')
    for i,(r,fx) in enumerate(sc):
        wd=r.width; 
        if wd>cw-4: report['issues'].append(f'{NAMES[i]}: wider than its cell')
    # head drift: the head's position relative to the feet, per pose, against idle. The playing poses must keep the head within a few pixels or the figure jerks when they swap.
    a2=np.asarray(out)[:,:,3]>0; drift={}
    for i,n in enumerate(NAMES):
        c=a2[(i//8)*ch:(i//8+1)*ch,(i%8)*cw:(i%8+1)*cw]; ys,xs=np.where(c); top=ys.min(); drift[n]=(float(xs[ys<top+8].mean()-FX),float(ch-2-top))
    report['drift']={n:(round(v[0]-drift['idle'][0],1),round(v[1]-drift['idle'][1],1)) for n,v in drift.items()}
    for n in ('breath','strum_down','strum_up','fret_far','fret_mid','fret_near','blink','talk'):
        dx,dy=report['drift'][n]
        if abs(dx)>CALM_X or abs(dy)>CALM_Y: report['issues'].append(f'{n}: head moves {dx:+.0f},{dy:+.0f} px from idle')
    report['calm_score']=round(sum(abs(report['drift'][n][0])+abs(report['drift'][n][1]) for n in ('strum_down','strum_up','fret_far','fret_mid','fret_near')),1)
    for i,n in enumerate(NAMES):
        ra=raw_areas[i]/max(1,raw_areas[0])
        if i and (ra<0.87 or ra>1.3): report['issues'].append(f'{n}: silhouette is {ra:.2f} of idle before registration (instrument or limb missing, or the figure is drawn at the wrong size)')
    report['area']={n:round(raw_areas[i]/max(1,raw_areas[0]),2) for i,n in enumerate(NAMES)}; report['reg']=reg_report
    report['heights']=dict(zip(NAMES,hts)); report['cell']=[cw,ch]; report['scale']=round(s,3)
    return (out,dict(cw=cw,ch=ch,fx=FX,fy=FY,n=16,names=NAMES,h=HEIGHT)),report
def sheet_png(cid,out):
    cw=out[1]['cw']; ch=out[1]['ch']; im=out[0]; bg=Image.new('RGBA',im.size,(90,60,50,255)); bg.alpha_composite(im); return bg.convert('RGB')
def embed(ids):
    import shutil
    for f in os.listdir(MASTER):
        if f.endswith('_atlas.png'): shutil.copy(f'{MASTER}/{f}',f'art/poses/{f}')
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
        os.makedirs('art/poses',exist_ok=True); os.makedirs(MASTER,exist_ok=True); out,meta=res; out.save(f'{MASTER}/{cid}_atlas.png',optimize=True); json.dump(meta,open(f'art/poses/{cid}_meta.json','w'))
        sheet_png(cid,res).save(f'/tmp/fbout/atlas_{cid}.png'); print(json.dumps(rep)); print(os.path.getsize(f'art/poses/{cid}_atlas.png')//1024,'KB',out.size)
