# Generate and pick pose sets for many characters.  usage (repo root): python3 art/gemini_test/sheets/run_all.py [id ...]     (default: everyone in chars.CH that has no art/poses/<id>_atlas.png)
# Per character: A1 first (it becomes the idle reference), then A2 A3 B1 B2 B3 in parallel; candidates are scored (split must find 8 figures, head drift in the playing poses = calm_score);
# if no candidate is clean it asks for two more of each, up to 5.  Resumable (existing out/<id>_<sheet>_<n>.png are reused).  Log: art/gemini_test/sheets/run.log, choices: art/poses/choice.json
import sys,os,json,subprocess,threading,time
from concurrent.futures import ThreadPoolExecutor
HERE=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.abspath(os.path.join(HERE,'..','..','..')); os.chdir(REPO)
sys.path.insert(0,'tests'); sys.path.insert(0,HERE)
import chars,procposes as PP
STOP=threading.Event(); SEM=threading.Semaphore(3); LOG=open(HERE+'/run.log','a'); LK=threading.Lock(); CHOICE_F='art/poses/choice.json'
def log(*a):
    with LK: print(time.strftime('%H:%M:%S'),*a,file=LOG,flush=True)
def gen(cid,w,n):
    if STOP.is_set(): return False
    f=f'{HERE}/out/{cid}_{w}_{n}.png'
    if os.path.exists(f): return True
    wait=20
    for t in range(8):
        with SEM: r=subprocess.run(['python3',HERE+'/gen_sheet.py',cid,w,str(n)],cwd=HERE,capture_output=True,text=True)
        if os.path.exists(f): return True
        msg=(r.stdout+r.stderr).strip(); low=msg.lower()
        if 'spending cap' in low or 'spend cap' in low:
            log('SPENDING CAP: stopping the whole run (raise the monthly spend cap at https://ai.studio/spend, then run this again; it resumes)'); STOP.set(); return False
        if '402' in msg or 'prepayment' in low or 'credits are depleted' in low:
            log('CREDITS DEPLETED: stopping the whole run (top up at https://ai.studio/projects, then run this again; it resumes)'); STOP.set(); return False
        if '429' in msg or 'rate' in low or 'exhausted' in low or 'overloaded' in low or '503' in msg:
            log(cid,w,n,'rate limited, waiting',wait,'s'); time.sleep(wait); wait=min(wait*2,240); continue
        log(cid,w,n,'gen failed:',msg[-220:]); time.sleep(5)
    return False
def valid(cid,w,n):
    try:
        im,fg,m=PP.split(f'{HERE}/out/{cid}_{w}_{n}.png'); return m is not None
    except Exception as e: log(cid,w,n,'split error',e); return False
def one(cid):
    if STOP.is_set(): return
    H=chars.CH[cid]['height']; done=os.path.exists(f'art/poses/{cid}_atlas.png')
    if done: return
    if not gen(cid,'A',1): return
    LEAN=os.environ.get('LEAN')=='1'      # LEAN=1: two candidates per sheet (A1 A2, B1 B2) instead of three; set SHEET_SIZE=2K for the cheap size
    ns=[2] if LEAN else [2,3]
    for rnd in range(3):
        if STOP.is_set(): return
        with ThreadPoolExecutor(3) as ex: list(ex.map(lambda a:gen(cid,*a),[('A',n) for n in ns]+[('B',n) for n in (([1]+ns) if rnd==0 else ns)]))
        As=[n for n in [1]+list(range(2,max(ns)+1)) if os.path.exists(f'{HERE}/out/{cid}_A_{n}.png') and valid(cid,'A',n)]
        Bs=[n for n in range(1,max(ns)+1) if os.path.exists(f'{HERE}/out/{cid}_B_{n}.png') and valid(cid,'B',n)]
        best=None
        if As and Bs:
            for a in As:
                for b in Bs:    # blink and talk come from sheet B, so the pair is judged together
                    res,rep=PP.build(cid,H,a,b)
                    if res is None: continue
                    sc=rep['calm_score']+10*len(rep['issues'])
                    if best is None or sc<best[0]: best=(sc,a,b,res,rep)
        log(cid,'round',rnd,'As',As,'Bs',Bs,'best',None if not best else (best[1],best[2],best[0],best[4]['issues'][:2]))
        if best and not best[4]['issues']: break
        ns=[max(ns)+1] if LEAN else [max(ns)+1,max(ns)+2]
        if rnd==2: break
    if not best: log(cid,'NO USABLE CANDIDATE'); return
    sc,a,b,res,rep=best; out,meta=res; os.makedirs('art/poses',exist_ok=True); out.save(f'art/poses/{cid}_atlas.png',optimize=True); json.dump(meta,open(f'art/poses/{cid}_meta.json','w'))
    with LK:
        C=json.load(open(CHOICE_F)) if os.path.exists(CHOICE_F) else {}; C[cid]=dict(A=a,B=b,calm=rep['calm_score'],issues=rep['issues']); json.dump(C,open(CHOICE_F,'w'),indent=1)
    log(cid,'DONE A',a,'B',b,'calm',rep['calm_score'],'issues',rep['issues'])
if __name__=='__main__':
    ids=sys.argv[1:] or [c for c in chars.CH if c not in ('bard','ghat')]
    log('start',ids)
    with ThreadPoolExecutor(2) as ex: list(ex.map(one,ids))
    log('finished')
