# v1.63 room art: Green Room stage plate, merch room, backstage wall, three backstage doors, the Guitar Tech's reference.
# usage: python3 gen_rooms.py [key ...]   -> rooms/<key>.png
import subprocess,sys,os
from concurrent.futures import ThreadPoolExecutor
import re
_src=open('gen_stages.py').read(); STYLE=eval(_src[_src.index('STYLE=')+6:_src.index('\nV={')])   # gen_stages.py runs on import, so read its STYLE text only
PIX="Pixel-art game asset, crisp pixels, thick dark brown outline, warm hand-painted palette, chunky and slightly worn. Absolutely no text, no letters, no numbers, no logo, no watermark. "
DOOR=PIX+"A single backstage door seen straight from the front, upright, in its wooden door frame, filling most of the frame, on a solid flat pure magenta (#FF00FF) background, no wall around it, no floor, no shadow on the background. "
J={
 'green':(STYLE+"A cozy backstage green room, the dressing room where musicians warm up: painted deep green walls, a long dressing mirror ringed with warm bulbs on the back wall, a costume rack with leather jackets and a sequined coat at the far left, a cork board with gig flyers and set lists (no readable text), a small practice amp and two guitar stands at the far right, a worn patterned rug on a wooden floor, a kettle and mugs on a side table, warm cozy lamplight.",'21:9','gemini-2.5-flash-image'),
 'merch':(PIX+"A wide painted game backdrop of a music venue's backstage merch room, side-on flat view: a warm red brick wall with a sagging string of festoon bulbs near the top, a few gig posters with simple shapes (no text), wall shelves with folded band T-shirts, a long merch table across the whole bottom fifth with a dark red table cloth, stacks of vinyl records, a cash box and a tip jar on it, an amp stack and a guitar case at the far left, a T-shirt rail at the far right. The middle of the wall is calm, darker and uncluttered because menu panels sit over it. No people.",'16:9','gemini-3-pro-image'),
 'wall':(PIX+"A seamless flat texture of a backstage corridor wall seen straight on: dark red-brown brick, a pair of old metal conduit pipes running along the very top, a few cable runs and gaffer-tape scraps, scuffs and old paint drips, warm dim light from above, no doors, no floor, no posters, no people.",'1:1','gemini-3-pro-image'),
 'door_green':(DOOR+"The GREEN ROOM door: a green painted wooden door with two raised panels, a big gold five-pointed star on the upper panel, a brass knob, a small brass kick plate.",'2:3','gemini-3-pro-image'),
 'door_ear':(DOOR+"The EAR REPORT door: a blue painted wooden door with two raised panels, a round porthole-style plaque on the upper panel showing a glowing sound wave and a small ear, a brass knob, a small brass kick plate.",'2:3','gemini-3-pro-image'),
 'door_roster':(DOOR+"The ROSTER door: a red painted wooden door with two raised panels, the upper panel covered with pinned small polaroid photos of musicians' faces and a ticket stub, a brass knob, a small brass kick plate.",'2:3','gemini-3-pro-image'),
 'tech':(PIX+"A full-body character design of a friendly backstage guitar tech (a roadie), standing facing right in side view, whole body from head to boots, on a solid flat pure magenta (#FF00FF) background: a woman in her forties with a short grey-streaked dark bob and a headlamp on a band, a black band T-shirt under a utility vest full of picks, a string winder and a small tuner, a roll of gaffer tape on her belt, cargo trousers, worn work boots, holding a cream and sunburst electric guitar (Telecaster style) across her body ready to play.",'2:3','gemini-3-pro-image'),
}
def run(k):
    p,a,m=J[k]; env=dict(os.environ,GEM=m); r=subprocess.run(["python3","gen_img.py",f"rooms/{k}.png",p,a],capture_output=True,text=True,env=env); return k,(r.stdout+r.stderr).strip()[-120:]
ids=sys.argv[1:] or list(J)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(run,ids): print(*r,flush=True)
