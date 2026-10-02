# "Dust-off" grade for every embedded Gemini picture: Gemini art comes out flat, slightly soft, with yellowed whites.
# Per picture: (1) take half the yellow out of the whites (bright, low-saturation pixels only, painted colour is left alone),
# (2) raise contrast toward the portraits' level (std of brightness 56), at most +20%, (3) lift the whites about 20% on a soft shoulder (no clipping),
# (4) a light unsharp mask for edge, (5) back to the picture's own colour count so it stays pixel art. Alpha is never touched.
# It grades the embedded data URIs in index.html (blocks below) from ungraded originals kept in art/_ungraded/<BLOCK>/<key>.png,
# so running it again never compounds. New art (re-processed and re-embedded) is detected by hash and becomes the new original.
# Repo files that were byte-identical to an original are overwritten with the graded picture too.
# usage: python3 tests/grade.py [--dry OUTDIR]   (--dry writes before/after sheets per block to OUTDIR and changes nothing)
import re,os,sys,io,json,base64,hashlib,glob
import numpy as np
from PIL import Image,ImageFilter
from scipy import ndimage as ndi
BLOCKS=['PEDAL_SRC','GUITAR_SRC','BODY_SRC','PORTRAIT_ART','CALLER_SRC','BANDART_SRC','VSP_SRC','STAGE_PLATE_SRC','TITLE_PLATES','CASTLE_SRC','WORLDMAP_SRC','VANART_SRC','RIVAL_PORT','MEMBER_PORT']
WIDE={'VSP_SRC','STAGE_PLATE_SRC','TITLE_PLATES','WORLDMAP_SRC'}     # big painted scenes: a softer unsharp
ORIG='art/_ungraded'; MAN=ORIG+'/manifest.json'
P=dict(target=56.0,kmax=1.20,lift=0.45,neutral=0.5)   # lift 0.45 brightens a 180 white about 20%
def lum(a): return a@np.array([0.299,0.587,0.114])
def grade(im,wide=False):
    im=im.convert('RGBA'); a=np.asarray(im).astype(float); al=a[:,:,3]; m=al>128; rgb=a[:,:,:3].copy()
    if m.sum()<20: return im
    L=lum(rgb); sat=(rgb.max(2)-rgb.min(2))/np.maximum(1,rgb.max(2))
    w=np.clip((L-140)/60,0,1)*np.clip(1-(sat-0.2)/0.25,0,1)                       # how much a pixel is a "white"
    cast=(rgb[:,:,0]+rgb[:,:,1])/2-rgb[:,:,2]; d=np.clip(cast,0,None)*P['neutral']*w   # yellow out of the whites
    rgb[:,:,0]-=d/3; rgb[:,:,1]-=d/3; rgb[:,:,2]+=d*2/3
    L=lum(rgb); mu=L[m].mean(); k=float(np.clip(P['target']/max(1,L[m].std()),1.0,P['kmax']))
    rgb=(rgb-mu)*k+mu                                                             # contrast about the picture's own mean
    rgb=np.clip(rgb,0,255); rgb=255-(255-rgb)*(1-P['lift']*w[...,None])          # whites up on a soft shoulder: brighter, never clipped flat
    rgb=np.clip(rgb,0,255)
    # edge: unsharp mask, with transparent pixels filled from their nearest opaque neighbour so outlines do not glow
    if (~m).any():
        idx=ndi.distance_transform_edt(~m,return_distances=False,return_indices=True); rgb=rgb[idx[0],idx[1]]
    sh=Image.fromarray(rgb.astype(np.uint8)).filter(ImageFilter.UnsharpMask(radius=1,percent=35 if wide else 55,threshold=2))
    n0=len(np.unique(np.asarray(im.convert('RGB'))[m].reshape(-1,3),axis=0))
    q=sh.quantize(colors=int(np.clip(n0,32,256)),method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGB')
    out=np.dstack([np.asarray(q),al.astype(np.uint8)]); return Image.fromarray(out.astype(np.uint8),'RGBA')
def stats(im):
    a=np.asarray(im.convert('RGBA')).astype(float); m=a[:,:,3]>128; p=a[:,:,:3][m]; L=lum(p); sat=(p.max(1)-p.min(1))/np.maximum(1,p.max(1))
    hi=p[(L>150)&(sat<0.38)]; hi=hi if len(hi)>=12 else p[L>=np.percentile(L,97)]
    return ((hi[:,0]+hi[:,1])/2-hi[:,2]).mean(), lum(hi).mean(), L.std()
def entries(s,block):
    i=s.index('const '+block+'='); j=s.find('\nconst ',i+5); j=len(s) if j<0 else j
    for n,m in enumerate(re.finditer(r'''(?:["']?([A-Za-z0-9_]+)["']?\s*:\s*)?(["'])data:image/(png|jpeg);base64,([A-Za-z0-9+/=]+)\2''',s[i:j])):
        yield (m.group(1) or str(n)), m.group(3), m.group(4)
def encode(im,fmt):
    b=io.BytesIO(); (im.convert('RGB').save(b,'JPEG',quality=88) if fmt=='jpeg' else im.save(b,'PNG',optimize=True)); return b.getvalue()
if __name__=='__main__':
    dry=sys.argv[2] if len(sys.argv)>2 and sys.argv[1]=='--dry' else None
    s=open('index.html',encoding='utf-8').read(); man=json.load(open(MAN)) if os.path.exists(MAN) else {}
    files={}
    for f in glob.glob('art/**/*.*',recursive=True):
        if '/_ungraded/' in f or '/gemini_test/' in f or not f.endswith(('.png','.jpg')): continue
        files.setdefault(hashlib.sha1(open(f,'rb').read()).hexdigest(),[]).append(f)
    rep=[]; tot=0
    for block in BLOCKS:
        if 'const '+block+'=' not in s: continue
        before=[]; after=[]
        for key,fmt,b64 in list(entries(s,block)):
            raw=base64.b64decode(b64); h=hashlib.sha1(raw).hexdigest(); mk=block+'/'+key; of=f'{ORIG}/{block}/{key}.'+('jpg' if fmt=='jpeg' else 'png')
            if man.get(mk,{}).get('graded')==h and os.path.exists(of): orig=open(of,'rb').read()        # already graded: start again from the original
            else: orig=raw                                                                               # new art: this is the original
            oim=Image.open(io.BytesIO(orig)); gim=grade(oim,block in WIDE); new=encode(gim,fmt)
            c0,w0,k0=stats(oim); c1,w1,k1=stats(Image.open(io.BytesIO(new))); rep.append((block,key,c0,c1,w0,w1,k0,k1))
            if dry: before.append(oim.convert('RGBA')); after.append(Image.open(io.BytesIO(new)).convert('RGBA')); continue
            os.makedirs(os.path.dirname(of),exist_ok=True); open(of,'wb').write(orig)
            nb=base64.b64encode(new).decode(); assert s.count(b64)==1,(mk,s.count(b64)); s=s.replace(b64,nb); tot+=1
            for f in files.get(hashlib.sha1(orig).hexdigest(),[])+([] if h==hashlib.sha1(orig).hexdigest() else files.get(h,[])): open(f,'wb').write(new)
            man[mk]={'graded':hashlib.sha1(new).hexdigest()}
        if dry and before:
            Z=1 if block in WIDE else 2; ims=list(zip(before,after))[:8 if block not in WIDE else 3]
            W=sum(b.width*Z+6 for b,_ in ims) if block not in WIDE else max(b.width for b,_ in ims)*2+6; H=(max(b.height for b,_ in ims)*Z+6)*2 if block not in WIDE else sum(b.height+6 for b,_ in ims)
            sh=Image.new('RGBA',(W,H),(42,22,20,255)); x=y=0
            for b,g in ims:
                if block in WIDE: sh.alpha_composite(b,(0,y)); sh.alpha_composite(g,(b.width+6,y)); y+=b.height+6
                else:
                    bb=b.resize((b.width*Z,b.height*Z),Image.NEAREST); gg=g.resize((g.width*Z,g.height*Z),Image.NEAREST); sh.alpha_composite(bb,(x,0)); sh.alpha_composite(gg,(x,H//2)); x+=bb.width+6
            os.makedirs(dry,exist_ok=True); sh.convert('RGB').save(f'{dry}/grade_{block}.png')
    for block in BLOCKS:
        r=[x for x in rep if x[0]==block]
        if r: print(f"{block:16s} {len(r):2d}  white cast {np.mean([x[2] for x in r]):4.0f} -> {np.mean([x[3] for x in r]):4.0f}   whites {np.mean([x[4] for x in r]):4.0f} -> {np.mean([x[5] for x in r]):4.0f}   contrast {np.mean([x[6] for x in r]):3.0f} -> {np.mean([x[7] for x in r]):3.0f}")
    if not dry: open('index.html','w',encoding='utf-8').write(s); json.dump(man,open(MAN,'w'),indent=0); print('graded',tot,'pictures')
