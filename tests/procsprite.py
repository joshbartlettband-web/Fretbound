# Gemini pose sheet -> game sprite atlas. Keys the magenta, splits the sheet into poses (connected pieces, ordered by row then column),
# scales every pose by the same factor so the neutral pose is HERO_H tall, puts every pose's feet on one baseline and centre, shares one palette.
# usage: python3 tests/procsprite.py SHEET.png OUTDIR NAME [HERO_H]     -> OUTDIR/NAME_atlas.png + NAME_meta.json   (cell 180x200, feet at (90,192))
import sys,json,os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0,'tests')
CW,CH,FX,FY=180,200,90,192
def pieces(im):
    a=np.asarray(im.convert('RGB')).astype(int); h,w,_=a.shape
    bg=np.median(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]),axis=0); near=np.abs(a-bg).sum(axis=2)<130
    lab,n=ndi.label(near); edge=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); edge.discard(0); fg=~np.isin(lab,list(edge))
    fg=ndi.binary_opening(fg,iterations=1); fg=ndi.binary_fill_holes(fg)&~(np.abs(a-bg).sum(axis=2)<190)
    merged=ndi.binary_dilation(fg,iterations=7); lab,n=ndi.label(merged); sz=ndi.sum(fg,lab,range(1,n+1))
    keep=[i+1 for i in range(n) if sz[i]>0.004*h*w]
    res=[]
    for k in keep:
        m=(lab==k)&fg; ys,xs=np.where(m); res.append((m,(xs.min(),ys.min(),xs.max()+1,ys.max()+1)))
    return a,res
def order(res,rows):
    ys=sorted(r[1][3] for r in res); cut=[]  # group into rows by feet y
    res=sorted(res,key=lambda r:r[1][3]); groups=[[res[0]]]
    for r in res[1:]:
        if r[1][3]-groups[-1][-1][1][3]<(res[-1][1][3]-res[0][1][3])/(rows*2.2)+1: groups[-1].append(r)
        else: groups.append([r])
    return [g for grp in groups for g in sorted(grp,key=lambda r:r[1][0])]
if __name__=='__main__' and sys.argv[1] not in ('--embed','--embed-band'):
    src,outd,name=sys.argv[1:4]; HH=int(sys.argv[4]) if len(sys.argv)>4 else 108; os.makedirs(outd,exist_ok=True)
    im=Image.open(src); a,res=pieces(im); res=order(res,2); print(len(res),'poses found')
    first=res[0][1]; hn=first[3]-first[1]; s=HH/hn; print('scale',round(s,3),'neutral height px',hn)
    cells=[]; info=[]
    for i,(m,(x0,y0,x1,y1)) in enumerate(res):
        rgba=np.dstack([a[y0:y1,x0:x1].astype(np.uint8),(m[y0:y1,x0:x1]*255).astype(np.uint8)]); c=Image.fromarray(rgba)
        nw,nh=max(1,round(c.width*s)),max(1,round(c.height*s)); c=c.resize((nw,nh),Image.LANCZOS)
        # boots centre: lowest 12 percent of the figure
        al=np.asarray(c)[:,:,3]>140; ys,xs=np.where(al); low=ys>ys.max()-max(3,int(nh*0.12)); bx=int(np.median(xs[low]))
        cell=Image.new('RGBA',(CW,CH),(0,0,0,0)); px,py=FX-bx,FY-(ys.max()+1)
        if px<0 or py<0 or px+nw>CW: print('pose',i,'does not fit',px,py,nw,nh)
        cell.paste(c,(px,py)); cells.append(cell); info.append(dict(i=i,box=[int(x0),int(y0),int(x1),int(y1)],w=nw,h=nh))
    atlas=Image.new('RGBA',(CW*len(cells),CH),(0,0,0,0))
    for i,c in enumerate(cells): atlas.paste(c,(i*CW,0))
    a2=np.asarray(atlas).copy(); al=a2[:,:,3]>140
    rgb=Image.fromarray(np.clip(a2[:,:,:3].astype(float)*float(os.environ.get('BRIGHT','1.10')),0,255).astype(np.uint8)).quantize(colors=56,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    Image.fromarray(np.dstack([np.asarray(rgb),al*255]).astype(np.uint8)).save(f'{outd}/{name}_atlas.png',optimize=True)
    json.dump(dict(cw=CW,ch=CH,fx=FX,fy=FY,n=len(cells),poses=info),open(f'{outd}/{name}_meta.json','w'))
    print('atlas',os.path.getsize(f'{outd}/{name}_atlas.png')//1024,'KB')
    sh=Image.new('RGB',(CW*len(cells)*2,CH*2),(92,58,38)); big=Image.open(f'{outd}/{name}_atlas.png').resize((CW*len(cells)*2,CH*2),Image.NEAREST); sh.paste(big,(0,0),big); sh.save(f'{outd}/{name}_check.png')
def embed(names,path='index.html'):
    import base64
    src={n:'data:image/png;base64,'+base64.b64encode(open(f'art/sprites/{n}_atlas.png','rb').read()).decode() for n in names}; meta={n:json.load(open(f'art/sprites/{n}_meta.json')) for n in names}
    for n in meta: meta[n].pop('poses',None)
    s=open(path,encoding='utf-8').read(); a=s.index('/*SPRITES:BEGIN*/'); b=s.index('/*SPRITES:END*/')+len('/*SPRITES:END*/')
    open(path,'w',encoding='utf-8').write(s[:a]+'/*SPRITES:BEGIN*/\nconst SPR_SRC='+json.dumps(src,separators=(',',':'))+', SPR_META='+json.dumps(meta,separators=(',',':'))+';\n/*SPRITES:END*/'+s[b:]); print('embedded',list(src))

if __name__=='__main__' and sys.argv[1]=='--embed': embed(sys.argv[2:])

def embed_band(names,path='index.html'):
    import base64
    src={n:'data:image/png;base64,'+base64.b64encode(open(f'art/sprites/band/{n}_atlas.png','rb').read()).decode() for n in names}; meta={n:json.load(open(f'art/sprites/band/{n}_meta.json')) for n in names}
    for n in meta: meta[n].pop('poses',None)
    s=open(path,encoding='utf-8').read(); a=s.index('/*BANDART:BEGIN*/'); b=s.index('/*BANDART:END*/')+len('/*BANDART:END*/')
    open(path,'w',encoding='utf-8').write(s[:a]+'/*BANDART:BEGIN*/\nconst BANDART_SRC='+json.dumps(src,separators=(',',':'))+', BANDART_META='+json.dumps(meta,separators=(',',':'))+';\n/*BANDART:END*/'+s[b:]); print('embedded band',list(src))
if __name__=='__main__' and sys.argv[1]=='--embed-band': embed_band(sys.argv[2:])
