# In-between poses for leaning into a call (v1.97). Josh: while a caller plays, the jump between poses looks almost doubled over.
# The caller swaps between lean_in (head and shoulders forward) and the upright strum, blink and idle poses many times a call. Three
# new cells per character, made by tests/tween.py's optical flow from the GRADED atlases the game embeds (art/poses/*_atlas.png), so
# they need no grade of their own (POSE_TW_SRC is not in grade.py's BLOCKS):
#   16 lean_half  halfway from idle to lean_in, shown going into and out of the lean
#   17 lean_down  halfway from lean_in to strum_down: strumming while leaning, the head stays forward
#   18 lean_up    halfway from lean_in to strum_up
# usage: python3 tests/posetween.py [--embed] [OUT_DIR]   -> OUT_DIR/<id>_tw.png (three cells in a row), --embed writes POSE_TW_SRC
import sys,os,json,glob,base64,io
import numpy as np
from PIL import Image
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tween import tween
import outlinefix
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args=[a for a in sys.argv[1:] if not a.startswith('--')]; OUT=args[0] if args else os.path.join(ROOT,'art','poses_tw'); os.makedirs(OUT,exist_ok=True)
PAIRS=[('idle','lean_in'),('lean_in','strum_down'),('lean_in','strum_up')]
src={}
for mf in sorted(glob.glob(os.path.join(ROOT,'art','poses','*_meta.json'))):
    cid=os.path.basename(mf)[:-10]; m=json.load(open(mf)); cw,ch=m['cw'],m['ch']; a=np.asarray(Image.open(mf.replace('_meta.json','_atlas.png')).convert('RGBA'))
    C=[a[(i//8)*ch:(i//8)*ch+ch,(i%8)*cw:(i%8)*cw+cw].copy() for i in range(16)]
    allpx=np.concatenate([c[c[:,:,3]>140][:,:3] for c in C]); pal=np.unique(allpx,axis=0).astype(float)
    strip=Image.new('RGBA',(cw*3,ch),(0,0,0,0))
    for k,(pa,pb) in enumerate(PAIRS):
        f=tween(C[m['names'].index(pa)],C[m['names'].index(pb)],0.5,pal); f=outlinefix.fix_cell(f)
        strip.paste(Image.fromarray(f.astype(np.uint8),'RGBA'),(k*cw,0))
    p=os.path.join(OUT,cid+'_tw.png'); strip.save(p,optimize=True); src[cid]=p; print(cid,cw,ch,flush=True)
if '--embed' in sys.argv:
    H=os.path.join(ROOT,'index.html'); s=open(H,encoding='utf-8').read()
    blk='/*POSETW:BEGIN*/const POSE_TW_SRC='+json.dumps({k:'data:image/png;base64,'+base64.b64encode(open(v,'rb').read()).decode() for k,v in src.items()},separators=(',',':'))+';/*POSETW:END*/'
    if '/*POSETW:BEGIN*/' in s:
        i=s.index('/*POSETW:BEGIN*/'); j=s.index('/*POSETW:END*/')+len('/*POSETW:END*/'); s=s[:i]+blk+s[j:]
    else:
        a='const POSE_IMG={}, POSE_IMG_L={};'; assert s.count(a)==1; s=s.replace(a,blk+'\n'+a)
    open(H,'w',encoding='utf-8').write(s); print('embedded',len(src),len(blk),'bytes')
