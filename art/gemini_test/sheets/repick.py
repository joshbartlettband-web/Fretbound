# Re-pick the best A/B pair for every character from the candidate sheets already in out/, with the current checks (registration, silhouette area, head drift).
# usage (repo root): python3 art/gemini_test/sheets/repick.py [id ...]     writes art/poses/<id>_atlas.png + meta and art/poses/choice.json; log: art/gemini_test/sheets/repick.log
import sys,os,json,glob,re,time
from multiprocessing import Pool
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.abspath(os.path.join(HERE,'..','..','..')); os.chdir(REPO)
sys.path.insert(0,'tests'); sys.path.insert(0,HERE)
import chars,procposes as PP
chars.CH.setdefault('bard',dict(height=104)); chars.CH.setdefault('ghat',dict(height=109))
def cands(cid):
    A=sorted(int(re.search(r'_A_(\d+)\.png',f).group(1)) for f in glob.glob(f'{HERE}/out/{cid}_A_*.png') if re.search(r'_A_\d+\.png$',f))
    B=sorted(int(re.search(r'_B_(\d+)\.png',f).group(1)) for f in glob.glob(f'{HERE}/out/{cid}_B_*.png') if re.search(r'_B_\d+\.png$',f))
    return A,B
_MG={}
def magenta(name):   # a sheet whose background is white or pink keys cream fur and white cloth out as holes (the Kitsune's snout), so prefer magenta ones
    if name not in _MG:
        from PIL import Image
        px=Image.open(f'{HERE}/out/{name}.png').convert('RGB').getpixel((6,6)); _MG[name]=px[0]>200 and px[2]>200 and px[1]<90
    return _MG[name]
def work(cid):
    H=chars.CH[cid]['height']; A,B=cands(cid); best=None; tried=0
    for a in A:
        for b in B:
            try: res,rep=PP.build(cid,H,a,b)
            except Exception as e: continue
            if res is None: continue
            tried+=1; sc=rep['calm_score']+10*len(rep['issues'])+8*sum(1 for n in (f'{cid}_A_{a}',f'{cid}_B_{b}') if not magenta(n))
            if best is None or sc<best[0]: best=(sc,a,b,res,rep)
    if not best: return cid,None
    sc,a,b,res,rep=best; out,meta=res; os.makedirs(PP.MASTER,exist_ok=True); out.save(f'{PP.MASTER}/{cid}_atlas.png',optimize=True); json.dump(meta,open(f'art/poses/{cid}_meta.json','w'))
    return cid,dict(A=a,B=b,calm=rep['calm_score'],issues=rep['issues'],tried=tried)
if __name__=='__main__':
    ids=sys.argv[1:] or sorted(set(chars.CH)|{'bard','ghat'})
    L=open(HERE+'/repick.log','a'); C=json.load(open('art/poses/choice.json')) if os.path.exists('art/poses/choice.json') else {}
    with Pool(4) as p:
        for cid,r in p.imap_unordered(work,ids):
            print(time.strftime('%H:%M:%S'),cid,r,file=L,flush=True)
            if r: C[cid]=r
            json.dump(C,open('art/poses/choice.json','w'),indent=1)
    print('finished',file=L,flush=True)
