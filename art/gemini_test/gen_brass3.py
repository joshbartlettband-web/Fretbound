# The Brass Tacks are three horn players. The fedora trumpet player is band/brass_sheet.jpg; these are the other two, matched to it.
# usage: python3 gen_brass3.py [brassb brassc]
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
BASE=("Pixel-art game sprite sheet on a solid flat pure magenta (#FF00FF) background, crisp pixels, thick dark brown outline, warm hand-painted palette, no shadows, no text, no watermark. "
 "The person is one of the musicians in the reference portrait of a horn section. Mustard-gold suit jacket, brown trousers, brown shoes. BAREHEADED: no hat, no cap, the hair is visible. "
 "ONE person only, full body with legs and shoes, flat side view facing RIGHT. TWO poses side by side in one row, identical size and scale, on the same baseline, with a wide empty magenta gap between them. ")
P={
'brassb':"A slim young man with dark brown skin and short black hair, bareheaded, the musician on the LEFT of the portrait (not the man in the fedora), playing a brass trumpet. Pose 1: playing, trumpet held level pointing right. Pose 2: the SAME dark-skinned man (same dark brown skin, same face and hair), trumpet raised high, pointing up and to the right, leaning back.",
'brassc':"A slim young man with fair skin, short wavy brown hair and a brown bow tie, bareheaded, the musician on the RIGHT of the portrait (not the man in the fedora), playing a brass trombone. Pose 1: playing, trombone held level pointing right, slide pulled in. Pose 2: slide pushed far out and the trombone tilted up to the right, leaning back.",
}
def gen(i):
    r=subprocess.run(["python3","gen_img.py",f"band/{i}_sheet.png",BASE+P[i],"3:2","band/brass_port_big.png"],capture_output=True,text=True); return i,(r.stdout+r.stderr).strip()[-50:]
ids=sys.argv[1:] or list(P)
with ThreadPoolExecutor(2) as ex:
    for r in ex.map(gen,ids): print(*r)
