# Twelve new pedal fronts (v1.56). usage: python3 gen_pedals2.py [id ...]   writes pedals/<id>.jpg
import subprocess,sys,os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
D={ # id: (emblem, enclosure colour, knobs, knob, finish)
'harpy':('a screeching harpy, half woman half bird, wings spread wide, beak open','bright turquoise',2,'black','a hammered-metal finish'),
'fairy':('a ring of little red toadstool mushrooms with white spots and a tiny glowing fairy','mossy forest green',2,'cream','a fine sandy powder-coat grit finish'),
'pixie':('a tiny pixie with dragonfly wings sprinkling sparkles','bright magenta pink',3,'silver','a metallic flake sparkle finish'),
'centaur':('a galloping centaur silhouette with a bow, seen from the side','rich chestnut wood-brown, clearly brown and not orange',2,'gold','a fine sandy powder-coat grit finish'),
'mermaid':('a mermaid tail rising from blue waves with a shell','deep sea blue-green',2,'clear','a metallic flake sparkle finish'),
'leprechaun':('a pot of gold coins under a small rainbow with a green top hat','shamrock green',2,'gold','a hammered-metal finish'),
'wizard':('a wizard hat with stars and a crescent moon, with a swirling spark trail','royal indigo blue',3,'silver','a metallic flake sparkle finish'),
'hydra':('a three-headed hydra, three green snake heads on one body','swamp teal',3,'black','a fine sandy powder-coat grit finish'),
'phoenix':('a firebird phoenix with spread wings rising out of flames','blazing orange-gold',3,'gold','a hammered-metal finish'),
'gnome':('a gnome with a big white beard and a tall pointed red hat','sunny yellow',1,'black','a fine sandy powder-coat grit finish'),
'kraken':('a giant kraken with tentacles curling around a sunken ship mast','dark navy blue-black',3,'silver','a hammered-metal finish'),
'gremlin':('a small furry dark grey gremlin with huge pointed bat ears, glowing red eyes and a cheeky toothy grin, little yellow sparks around it, definitely not green','neon lime and black',2,'black','a metallic flake sparkle finish')}
def prompt(i):
    e,c,k,kn,fin=D[i]; BG='bright green (#00FF00)' if i in ('leprechaun','hydra','gremlin') else 'magenta (#FF00FF)'
    return (f"Pixel-art game asset: a guitar effects pedal seen straight from the front, upright, filling most of the frame, on a solid flat pure {BG} background. Crisp pixels, thick dark brown outline, warm hand-painted palette, chunky and slightly worn like a beloved road-case pedal. "
     f"The whole enclosure is {c} (NOT orange unless stated), with {fin}. Exactly {k} {kn} knob{'s' if k>1 else ''} in a row across the top, a small round red LED in the middle between the knobs and the emblem, "
     f"a rectangular inset label window in the centre showing the emblem: {e}, and a single chrome footswitch at the bottom. Four small screws in the corners. "
     "Absolutely no text, no letters, no numbers, no logo, no watermark, no cast shadow on the background.")
def gen(i):
    out=f"pedals/{i}.png"; r=subprocess.run(["python3","gen_img.py",out,prompt(i),"2:3","pedals/dragon.jpg" if False else "pedals/ogre.jpg"],capture_output=True,text=True)
    if os.path.exists(out): Image.open(out).convert('RGB').save(f"pedals/{i}.jpg",quality=90); os.remove(out)
    return i,(r.stdout+r.stderr).strip()[:100]
ids=sys.argv[1:] or list(D)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(gen,ids): print(*r)
