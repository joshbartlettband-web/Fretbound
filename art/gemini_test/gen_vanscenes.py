# Seven painted Van-screen scenes (the lodging for each continent). usage: python3 gen_vanscenes.py [id ...]
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
BASE=("Pixel-art painted game backdrop, very wide panorama, side-on flat view, crisp pixels, warm hand-painted palette with dark outlines, 64-colour feel. "
 "COMPOSITION: the horizon sits at about 55 percent of the image height; the bottom 40 percent is a flat, empty, level parking lot or yard (plain ground, nothing on it) with the left third completely empty so a vehicle can be added there; the lodging building stands in the middle and right on the horizon. "
 "FULL-BLEED artwork that fills the entire image edge to edge: no border, no frame, no letterbox bars. No vehicles, no people, no animals, no readable text or letters, no logos, no watermark. Scene: ")
S={
'na':"A lonely desert roadside motel at dawn: a long low motel with teal doors and lit amber windows, a tall roadside pylon with a glowing neon arrow (no letters), distant purple mesas, a pink and orange dawn sky with fading stars, cracked asphalt lot.",
'af':"A safari lodge at golden dusk in Africa: a cluster of round thatched-roof huts and a long thatched lodge with glowing lanterns and warm windows, a distant flat-topped acacia tree on the horizon, a huge orange sky, packed red earth yard.",
'sa':"A colourful colonial posada in the Andes at dusk: a long white-and-ochre building with arches, terracotta roof, bougainvillea, lit windows and string lights, snowy Andes peaks behind in violet, cobbled courtyard.",
'eu':"A cosy half-timbered countryside inn in Europe at twilight: a stone and timber inn with warm glowing windows, a chimney with smoke, rolling hills behind, a deep blue and pink sky with the first stars, cobbled yard with a lantern post.",
'as':"A traditional Japanese ryokan guesthouse at dusk: a low wooden building with paper lanterns and glowing shoji windows, a small torii gate, misty mountains and cherry trees behind, a purple and pink sky, a gravel and stone-path yard.",
'oc':"An Australian outback roadhouse at sunset: a corrugated-iron-roofed roadhouse with a wide veranda, lit windows, a windmill and water tank, a huge orange and gold sky, flat red dirt yard, distant low hills.",
'an':"A polar research station hut village in Antarctica at twilight: a few small orange and white prefab huts with warm lit windows on a snow field, a radio mast, ice cliffs in the distance, a dark blue sky with green aurora ribbons and stars, packed snow ground.",
}
def gen(i):
    r=subprocess.run(["python3","gen_img.py",f"vanscenes/{i}.png",BASE+S[i],"21:9"],capture_output=True,text=True); return i,(r.stdout+r.stderr).strip()[-40:]
ids=sys.argv[1:] or list(S)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(gen,ids): print(*r)
