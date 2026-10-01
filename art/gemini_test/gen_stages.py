# Generate one painted stage plate per venue. usage: python3 gen_stages.py [id ...]
import json,base64,subprocess,sys,os
from concurrent.futures import ThreadPoolExecutor
STYLE=("Pixel-art painted game backdrop, side-on flat view like a 2D game, very wide panoramic. Warm hand-painted palette with dark outlines, crisp pixels, 64-colour feel. "
"COMPOSITION RULES: the stage floor or ground is a flat clear band across the bottom 22 percent of the image, with its back edge at about 77 percent of the image height. "
"The middle of the floor and the two areas about one quarter and three quarters across must be EMPTY and uncluttered with nothing tall standing in front, so characters can be placed there. "
"Props belong at the far left and far right edges and on the back wall. No people, no animals standing on the stage, no readable text or letters, no logos, no watermark. Scene: ")
V={
'tide':"A Southern California beach-club stage at sunset: sandy-wood plank stage, ocean horizon with a big low orange sun over the water, silhouetted palm trees at both edges, tiki torches, a string of warm bulbs, and a glowing teal glass tide-pool aquarium tank built into the back wall. Purple to orange sky.",
'juke':"A Mississippi Delta juke joint at night: weathered grey-brown plank walls, bare hanging bulbs, an old guitar hung on the wall, a glowing potbelly stove at the far left, a window showing a moonlit cotton field, worn wooden floor with a faded red rug.",
'dunes':"A Sahara desert music festival stage at dusk: a raised wooden platform on sand, huge golden dunes behind, first stars in a deep orange to indigo sky, woven rugs and hanging lanterns, nomad tents at the far edges, a small campfire at the far left.",
'sebene':"A Kinshasa dance hall: vivid painted walls in green, yellow and red with abstract murals, bright wax-print cloth banners, a ceiling fan, strings of coloured bulbs, a polished tiled floor, loudspeaker stacks at both far edges.",
'azmari':"An Addis Ababa azmari music house: a warm round interior with woven baskets on the walls, a clay coffee pot with rising incense smoke on a low table at the far left, hanging lanterns in green yellow and red glass, patterned rugs, a krar lyre on the wall.",
'rio':"A rooftop terrace in Rio de Janeiro at night: Sugarloaf mountain and the lit bay and city lights glittering in the distance, tropical palm fronds at the edges, a string of festoon lights, a tiled terrace floor, deep blue night sky with a warm glow.",
'milonga':"A Buenos Aires milonga ballroom: dim old ballroom with red velvet curtains, crystal chandeliers, tall arched windows, candles on small tables at the edges, a polished checkered wood dance floor, sepia and crimson tones.",
'chicha':"A Lima chicha psychedelic tent: a canvas tent hung with neon-bright Andean textile patterns, big pink cyan and yellow glowing neon shapes (abstract, no letters), sun and condor motifs, painted posters, a bright patterned stage floor.",
'paris':"A Paris Montmartre cabaret stage: deep red velvet curtains drawn back, a gilded proscenium with a marquee ring of bulbs, a big round window showing the Eiffel Tower and rooftops at night, a polished stage floor, a glass cat sculpture at the far right.",
'cave':"A Seville flamenco cave tablao: whitewashed rough cave walls with rounded arches, iron torches and many candles in niches, hanging copper pots, painted tiles, a raised wooden tablao floor, warm orange firelight.",
'frost':"A frozen cathedral in Bergen, Norway: tall blue ice columns and pointed gothic arches made of ice, frozen stained-glass windows glowing pale blue and violet, hanging icicles, frost on the walls, a polished ice-blue stone floor, cold moonlight.",
'tokyo':"A Tokyo neon shrine on a rainy night: a vermilion torii gate, paper lanterns, glowing pink and cyan neon shapes (abstract, no letters), wet reflective stone ground, a small shrine at the far left, dark rainy sky with city lights behind.",
'ghat':"The ghats of Varanasi at dusk: wide stone steps leading down to the river Ganges, temple spires in silhouette, many small oil lamps and marigold garlands, floating diyas on the water at the right, smoky orange and pink sky, a flat stone platform in front.",
'bali':"A moonlit open-air wooden pavilion in Ubud, Bali: carved split gate, frangipani flowers, hanging lanterns, a large full moon over terraced rice fields, bamboo and palms at the edges, gamelan gongs at the far sides, a polished wooden floor.",
'lanai':"A sunset lanai porch in Honolulu: wooden porch with the Pacific Ocean and an orange pink sunset behind, palm trees and plumeria, tiki torches, a string of bulbs, bamboo and woven walls, a plank floor.",
'outback':"The Red Centre roadhouse near Alice Springs, Australia: a corrugated tin bar with a slow ceiling fan, a glowing neon beer sign shape (no letters), a window showing red desert and a distant Uluru rock at sunset, rough timber stage, dusty red floor.",
'grotto':"The Waitomo glowworm grotto in New Zealand: a dark limestone cave, thousands of tiny glowing blue-green dots like stars on the ceiling, stalactites, a still black pool reflecting the lights at the back, a flat stone ledge in front as the stage.",
'mess':"The McMurdo Station mess hall in Antarctica: a metal-panelled canteen with long tables and benches at the far edges, paper bunting, fluorescent ceiling strips, large windows showing a whiteout blizzard and ice, a scuffed linoleum floor.",
'aurora':"A glass geodesic dome on the Polar Plateau: a triangulated glass dome with bright green and violet aurora ribbons rippling across the starry sky outside, snow field beyond, soft blue interior light, a smooth floor.",
'pole':"The geographic South Pole: a flat endless white ice plain, a striped marker pole with a shiny sphere at the far right, a ring of flags, a low pale sun, long blue shadows, pale pink and blue sky, a flat packed-snow ground band.",
}
def gen(i):
    out=f"stages/{i}.png"  # saved as PNG, then kept as q92 JPEG (see HANDOFF)
    body=json.dumps({"contents":[{"parts":[{"text":STYLE+V[i]}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"21:9"}}})
    open(f"/tmp/req_{i}.json","w").write(body)
    for attempt in range(3):
        r=subprocess.run(["curl","-sS","-X","POST","https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent","-H","Content-Type: application/json","-d",f"@/tmp/req_{i}.json"],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except Exception: continue
        for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]):
            if 'inlineData' in p: open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); return i,'ok'
    return i,'FAILED'
ids=sys.argv[1:] or list(V)
with ThreadPoolExecutor(5) as ex:
    for r in ex.map(gen,ids): print(*r)
