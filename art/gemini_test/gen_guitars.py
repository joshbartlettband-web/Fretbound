# Six player guitars, side view, neck to the right, on flat magenta. usage: python3 gen_guitars.py [id ...]
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
BASE=("Pixel-art game sprite on a solid flat pure magenta (#FF00FF) background. Crisp pixels, thick dark brown outline, warm hand-painted palette, no shadow on the background, no text, no logo, no watermark. "
 "A single guitar seen exactly from the side as a flat 2D sprite, lying perfectly horizontal and straight, body at the LEFT, neck running RIGHT, headstock at the far right, strings visible as thin lines, the whole guitar in frame with generous margin. ")
G={
'single':"A Stratocaster-style electric guitar with a bright mint-green body (#7FD6B4), a cream white pickguard with three pickups, chrome bridge, a pale maple neck with a dark rosewood fingerboard and dot inlays, a maple headstock with six chrome tuners in a row.",
'humbucker':"A Les-Paul-style single-cut electric guitar with a golden yellow top (#E0B040), two humbucker pickups, a cream binding edge, a dark brown neck with an ebony fingerboard and block inlays, a black headstock with six gold tuners.",
'nylon':"A classical nylon-string acoustic guitar with a warm amber-orange wooden body (#E8A040), a round sound hole with a rosette, a wide light neck with a dark fingerboard, a slotted classical headstock with three gold tuners on each side.",
'resonator':"A metal-bodied resonator guitar with a polished silver steel body (#C8C8D2), a large round perforated metal cone cover plate in the middle of the body, a mahogany brown neck with a dark fingerboard, a small brown headstock with six tuners.",
'twelve':"A twelve-string acoustic dreadnought guitar with a bright orange painted body (#F08A28), a dark brown pickguard, a round sound hole, a brown neck, a long headstock with twelve tuners, six on each side, and doubled strings.",
'baritone':"A baritone electric guitar with a deep maroon body (#6A1E3A) with an offset double-cut shape, a black pickguard with two pickups, a very long dark brown neck with an ebony fingerboard, a long black headstock with six tuners.",
}
def gen(i): r=subprocess.run(["python3","gen_img.py",f"guitars/{i}.png",BASE+G[i],"16:9"],capture_output=True,text=True); return i,(r.stdout+r.stderr).strip()[:80]
ids=sys.argv[1:] or list(G)
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(gen,ids): print(*r)
