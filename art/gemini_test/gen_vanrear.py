# Straight rear views of the three vehicles for the title road (the old ones were three-quarter views and sat skewed on the road).
# usage: python3 gen_vanrear.py [v0 v1 v2] [tries]   -> vans/<id>_back<k>.png
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
BASE=("Pixel-art game sprite on a solid flat pure magenta (#FF00FF) background, crisp pixels, thick dark brown outline, warm hand-painted palette, no shadow on the background, no text, no letters, no logos, no number plate text, no watermark. "
 "STRAIGHT REAR VIEW: the camera is directly behind the vehicle at road level, exactly on its centre line, looking straight at its back. "
 "Perfectly symmetrical left to right. ONLY the rear face is visible: NO side panels, NO side windows, NO front, NO perspective, NO three-quarter angle. "
 "Both rear wheels visible at the bottom corners, equal size. Same livery as the reference image: cream white upper half, a thick red lower half with a white pinstripe between them, chrome bumper, round red tail lights. ")
V={
'v0':"A small beat-up 1970s camper van seen from behind: a narrow tall boxy back, one rear window with a spare tire cover mounted on the back door below it, a roof rack with one guitar amp and a couple of cases sticking up above the roof.",
'v1':"A tall fifteen-passenger touring van seen from behind: wide tall double rear doors each with a window, a ladder up one side of the doors, a big roof rack loaded with guitar cases and a drum case peeking above the roof.",
'v2':"A full-size rock tour bus seen from behind: a very wide tall flat rear with a big rear engine grille, a small rear window high up, roof air conditioning units and a satellite dish peeking above the roof, dual rear wheels.",
}
ids=[a for a in sys.argv[1:] if a in V] or list(V); tries=int(([a for a in sys.argv[1:] if a.isdigit()] or ['2'])[0])
def gen(job):
    k,t=job; r=subprocess.run(["python3","gen_img.py",f"vans/{k}_back{t}.png",BASE+V[k],"1:1",f"vans/{k}_side.jpg"],capture_output=True,text=True); return k,t,(r.stdout+r.stderr).strip()[-40:]
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(gen,[(k,t) for k in ids for t in range(tries)]): print(*r)
