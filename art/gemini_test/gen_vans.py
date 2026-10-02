# Painted vehicles for the three Bigger Van levels: side view (Van screen, front facing RIGHT) and rear three-quarter view (title screen). usage: python3 gen_vans.py [name ...]
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
BASE=("Pixel-art game sprite on a solid flat pure magenta (#FF00FF) background, crisp pixels, thick dark brown outline, warm hand-painted palette, no shadow on the background, no text, no letters, no logos, no watermark. "
 "Livery for all three vehicles: cream white upper half, a thick red lower half with a white pinstripe between them, chrome bumpers, round red tail lights. ")
V={
'v0':"A small beat-up 1970s camper van, short and boxy, two square windows, a roof rack carrying one guitar amp and a couple of cases, a spare tire cover on the back door.",
'v1':"A long fifteen-passenger touring van (like a Ford Econoline or Mercedes Sprinter extended), tall roof, four rows of side windows, double rear doors, a ladder at the back, a big roof rack loaded with guitar cases, an amp and a drum case, a rear-mounted cargo box.",
'v2':"A full-size rock tour bus (a big coach like a Prevost), very long, with a row of large dark tinted windows, a luggage bay door below, roof air-conditioning units, three axles with six wheels, a satellite dish on the roof, a big rear engine bay, the same cream and red livery sweeping along the length.",
}
VIEW={'side':"Exactly side view, flat 2D, the vehicle's FRONT (windshield) at the RIGHT, wheels on the ground, whole vehicle in frame with margin.",
 'rear':"Rear three-quarter view from behind and slightly to the left, so the rear face and the left side are both visible, whole vehicle in frame with margin, wheels on the ground."}
def gen(job):
    k,view=job; refs=['vans/ref_side.png'] if view=='side' else []
    pr=BASE+V[k]+" "+VIEW[view]+(" Match the livery and style of the reference image." if refs else "")
    r=subprocess.run(["python3","gen_img.py",f"vans/{k}_{view}.png",pr,"3:2"]+refs,capture_output=True,text=True); return k,view,(r.stdout+r.stderr).strip()[-40:]
jobs=[(k,v) for k in V for v in ('side','rear')]
if len(sys.argv)>1: jobs=[tuple(a.split('_')) for a in sys.argv[1:]]
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(gen,jobs): print(*r)
