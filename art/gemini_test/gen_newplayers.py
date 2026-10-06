# v1.74: three new players (v1.75: the King replaced by the Herald, plus the Journeyman). usage: python3 gen_newplayers.py [id ...]  -> chars/<id>_body.png (full body reference, magenta)
import subprocess,sys,os
from concurrent.futures import ThreadPoolExecutor
BASE=("Pixel-art game character design, full body from head to boots, standing facing right in side view, on a solid flat pure magenta (#FF00FF) background, "
 "in exactly the same art style, proportions, outline and palette as REFERENCE 1 (another player character of the same game). Crisp pixels, thick dark brown outline, warm hand-painted palette, no text. Adult proportions, head about one seventh of the height. ")
D={
 'smith':BASE+"The Blacksmith: a broad, friendly woman blacksmith in her thirties with soot on her cheeks, a short dark undercut and a braid, a thick leather apron over a sleeveless black band T-shirt, leather bracers and gloves, heavy boots, a small hammer hanging from her belt. She plays a dark brown baritone electric guitar with a long neck (the same guitar as REFERENCE 2), held across her body.",
 'wizard':BASE+"The Math Rock Wizard: a young lanky wizard with round glasses and a short beard, a deep blue pointed wizard hat and robe embroidered with small gold numbers, triangles and fractions, rolled sleeves, sneakers under the robe, a little abacus charm on his belt. He plays a teal-green Stratocaster-style electric guitar (the same guitar as REFERENCE 2) held across his body, fingers tapping on the fretboard.",
 'herald':BASE+"The Herald: a joyful Black woman guitarist in her forties singing mid-song, in a 1940s gospel-stage look: short pressed curls, small gold earrings, a long deep purple choir-style robe with gold trim over a dress, a gold herald's sash across her chest with a small trumpet emblem, low heels. She plays a white solid-body electric guitar with two sharp horns, three pickups and gold hardware (body shape like REFERENCE 2 but white with two pointed horns), held across her body. An original character, not a likeness of any real person.",
 'journey':BASE+"The Journeyman: a weathered, kind session guitarist in his sixties with a short grey beard, reading glasses pushed up on his forehead and a brown flat cap, a worn mustard cardigan over a work shirt, corduroy trousers and comfortable shoes, a leather tool roll of picks, capos and a glass slide strapped across his chest like a bandolier. He plays a worn butterscotch Telecaster-style electric guitar with a black pickguard and scuffed paint (single-cut slab body, like REFERENCE 2 in size), held across his body.",
}
G={'smith':'../guitars/baritone.png','wizard':'../guitars/single.png','herald':'../guitars/humbucker.png','journey':'../guitars/single.png'}
def run(k):
    env=dict(os.environ,GEM='gemini-3-pro-image'); r=subprocess.run(["python3","gen_img.py",f"chars/{k}_body.png",D[k],"2:3","chars/bard_body.jpg",G[k]],capture_output=True,text=True,env=env); return k,(r.stdout+r.stderr).strip()[-90:]
ids=sys.argv[1:] or list(D)
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(run,ids): print(*r,flush=True)
