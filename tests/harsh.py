import json,time,sys,numpy as np
from playwright.sync_api import sync_playwright
JS="""async ([g,ids])=>{
  const saved={ctx,master,roomIn}, sr=48000; tr.on=false;
  try{
    const off=new OfflineAudioContext(1,sr*3,sr); ctx=off; master=off.destination; roomIn=null;
    const r=makeRig({pan:0,amp:true}); r.setGuitar(GUITAR_BY[g]); r.setPedals(ids);
    [[4,52],[3,57],[2,62],[1,66]].forEach((n,k)=>r.pluck(n[1],n[0],0.05+k*0.45)); r.pluck(69,0,1.9);
    const b=await off.startRendering(); return Array.from(b.getChannelData(0));
  } finally { ctx=saved.ctx; master=saved.master; roomIn=saved.roomIn; }
}"""
def bands(x,sr=48000):
    X=np.abs(np.fft.rfft(np.array(x)*np.hanning(len(x))))**2; f=np.fft.rfftfreq(len(x),1/sr)
    e=lambda a,b: X[(f>=a)&(f<b)].sum()+1e-20
    body=e(100,1500); rms=np.sqrt(np.mean(np.square(x)))
    return 10*np.log10(e(2000,4000)/body), 10*np.log10(e(4000,12000)/body), 20*np.log10(rms+1e-9)
if __name__=="__main__":
    CASES=[(g,s) for g in sys.argv[1].split(',') for s in [[],['goblin'],['goblin','hornet'],['iron','gate','echo','goblin','hornet']]]
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.goto("file://"+sys.argv[2]); time.sleep(0.4)
        out={}
        print(f"{'guitar':10} {'board':34} {'2-4k':>6} {'4-12k':>6} {'level':>6}")
        for g,ids in CASES:
            pr,fz,lv=bands(pg.evaluate("([g,ids])=>window.__fb.rigRender(g,ids)",[g,ids])); out[g+':'+','.join(ids)]=[pr,fz,lv]
            print(f"{g:10} {(','.join(ids) or 'clean'):34} {pr:6.1f} {fz:6.1f} {lv:6.1f}")
        json.dump(out,open(sys.argv[3],'w')); print("errors:",errs); b.close()
