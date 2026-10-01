# Generate the 24 pedal fronts. usage: python3 gen_pedals.py [id ...]   (the ogre is made first, without a reference, and anchors the style of the rest)
import json,subprocess,sys,os
from concurrent.futures import ThreadPoolExecutor
P={p['id']:p for p in json.load(open('pedals/pedals.json'))}
EMB={'ogre':'an angry green ogre face with tusks','swamp':'a crocodile eye with a slit pupil half-submerged in murky water','glass':'a faceted glowing crystal shard','echo':'a round stone wishing well with blue ripples spreading out',
'wyrm':'a coiled serpent wyrm head with open jaws','moon':'a crescent moon with a few small stars','cathedral':'a gothic pointed-arch cathedral window with tracery','dragon':'a red dragon head breathing a little fire',
'iron':'an iron anvil with a spark','goblin':'a screaming green goblin face','basilisk':'a single glowing serpent eye with a vertical slit pupil, petrifying stare','hornet':'a striped hornet seen from the front with a stinger',
'tape':'a small winged wyvern curled around a tape reel','slap':'a cowboy spur with a jingling rowel','phantom':'a friendly white ghost with a swirling tail','tremor':'a curling ocean wave with foam',
'rotary':'a spinning horn speaker with a faint spirit swirl, in a wooden cabinet','owl':'an owl face with wide open round eyes','twins':'two small faces side by side, a pair of twins singing','springtank':'a coiled metal reverb spring inside a glass tank',
'halo':'a glowing golden halo ring floating above a small star','troll':'a grumpy grey-green troll face with a big nose','looper':'a skull wearing a tattered hood with two looping arrows around it','gate':'a rusty iron graveyard gate with a small tombstone'}
COL={'ogre':'bright orange','swamp':'olive green','glass':'bright cyan-teal','echo':'bright cobalt blue','wyrm':'emerald green','moon':'pale lavender-purple','cathedral':'pale lilac-white','dragon':'crimson red','iron':'steel grey','goblin':'leaf green','basilisk':'very dark charcoal blue-black','hornet':'bright yellow','tape':'tan beige leather','slap':'brick red','phantom':'vivid orange','tremor':'deep teal','rotary':'warm brown polished wood','owl':'violet purple','twins':'rose pink','springtank':'pale sky blue','halo':'cream ivory','troll':'moss grey-olive','looper':'dark plum purple','gate':'dark slate grey'}
FIN={'grit':'a fine sandy powder-coat grit finish','hammer':'a hammered-metal finish','flake':'a metallic flake sparkle finish'}
KN={'black':'black','cream':'cream-white','clear':'clear glassy','silver':'chrome silver','gold':'brass gold'}
def prompt(i):
    p=P[i]; BG='bright green (#00FF00)' if i in ('dragon',) else 'magenta (#FF00FF)'; a=p['art']; fin=FIN.get(a['tex'],'a painted finish')
    return (f"Pixel-art game asset: a guitar effects pedal seen straight from the front, upright, filling most of the frame, on a solid flat pure {BG} background. Crisp pixels, thick dark brown outline, warm hand-painted palette, chunky and slightly worn like a beloved road-case pedal. "
     f"The whole enclosure is {COL[i]} (NOT orange unless stated), with {fin}. Exactly {a['knobs']} {KN.get(a['knob'],a['knob'])} knob{'s' if a['knobs']>1 else ''} in a row across the top, a small round red LED in the middle between the knobs and the emblem, "
     f"a rectangular inset label window in the centre showing the emblem: {EMB[i]}, and a single chrome footswitch at the bottom. Four small screws in the corners. "
     "Absolutely no text, no letters, no numbers, no logo, no watermark, no cast shadow on the background.")
def gen(i,ref=None):
    out=f"pedals/{i}.png"; cmd=["python3","gen_img.py",out,prompt(i),"2:3"]+([ref] if ref else [])
    r=subprocess.run(cmd,capture_output=True,text=True); return i,(r.stdout+r.stderr).strip()[:80]
ids=sys.argv[1:] or list(P)
if 'ogre' in ids and not os.path.exists('pedals/ogre.png'): print(gen('ogre')); ids=[i for i in ids if i!='ogre']
elif 'ogre' in ids: ids=[i for i in ids if i!='ogre']
ref=None
with ThreadPoolExecutor(5) as ex:
    for r in ex.map(lambda i:gen(i,ref),ids): print(*r)
