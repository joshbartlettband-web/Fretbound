# Every character that gets a painted 16-pose set: reference picture, instrument, look, and the game height of its sprite.  kinds: guitar | drums | keys | sing | horn
import json,os,re
R='/home/user/Fretbound/art/'
G=json.load(open('/tmp/fbout/callergt.json')) if os.path.exists('/tmp/fbout/callergt.json') else {}
CH={}
def guitar(cid,ref,gid,gdesc,who,h):
    CH[cid]=dict(kind='guitar',ref=ref,guitar=R+f'guitars/{gid}.png',gdesc=gdesc,who=who,height=h)
HEX={'#E8A83A':'golden yellow','#5ACAB4':'turquoise'}
GN={'single':'electric guitar (Stratocaster style)','humbucker':'electric guitar (Les Paul style, humbucker pickups)','nylon':'acoustic classical guitar','resonator':'resonator guitar with a round metal cone in the body','twelve':'twelve-string acoustic guitar','baritone':'long-necked baritone electric guitar'}
# players
for cid,gid,gd,who in [
 ('monk','humbucker','a golden-yellow goldtop Les Paul style electric guitar (the same guitar as REFERENCE 3)','the Metronome Monk: a calm man in a yellow knitted beanie, saffron-orange and crimson monk robes wrapped over one shoulder, wooden prayer beads, bare feet or simple sandals'),
 ('hermit','nylon','a brown acoustic classical guitar','the Hermit: an old man in a brown hooded robe with a long white beard, worn and patched, rope belt, simple shoes'),
 ('busker','resonator','a silver resonator guitar with a round metal cone','the Busker: a young woman in a grey newsboy cap, curly dark hair, a denim jacket covered in pins, a red scarf, dark trousers and boots'),
 ('luthier','twelve','a honey-brown twelve-string acoustic guitar','the Luthier: a young woman with red hair in a long braid and goggles on her head, a brown leather apron over a cream shirt with a black bow tie, dark trousers, brown boots'),
 ('carto','baritone','a dark brown baritone electric guitar with a long neck','the Cartographer: a young man in a brown tricorn hat and round glasses, a teal-green long coat, burgundy waistcoat, white cravat, brown breeches and boots')]:
    guitar(cid,R+f'gemini_test/chars/{cid}_body.jpg',gid,gd,who,104)
LOOK={
'spur':'the Twang Knight: an armoured knight in silver plate armour with a white cowboy hat on its helmet and a red tabard with a white heart',
'tide':'the Reverb Siren: a mermaid with long teal hair and a small crown, a seashell top and a green fish tail instead of legs (NO legs and NO feet: the tail curls on the floor and is the same in every pose)',
'juke':'Mister Midnight, a moon spirit: a tall slender figure whose whole head is a softly glowing pale cream full moon with gentle grey craters and a calm kind face (soft half-closed eyes, small closed-mouth smile, no teeth), a black top hat with a magenta band, a deep purple suit jacket, white shirt with a black string tie, dark trousers, black shoes and white gloves',
'dunes':'the Dune Looper: a faceless sand spirit in a blue-purple hooded cloak with a sand-brown body, hood up, tan boots',
'sebene':'the Sebene Peacock: an anthropomorphic peacock with a blue head and a huge fan of green eyed tail feathers behind it, a pink jacket, navy trousers',
'azmari':'the Qenet Scholar: a big brown owl with a round owl head, a long white robe with gold trim, feathered feet',
'rio':'the Velvet Jaguar: an upright jaguar with spotted fur, in a cream suit',
'milonga':'the Nocturne: a tango vampire with pale lavender skin, slicked black hair, a black suit under a black cape with red lining and a high collar',
'chicha':'the Neon Condor: a man with a red featherless condor head, a white feather ruff collar, a black suit and tie',
'paris':'the Gargoyle of Montmartre: a grey stone gargoyle with a dragon-like head and bat wings, a white shirt with rolled sleeves, brown trousers, clawed feet',
'cave':'the Duende: a living flame spirit, a human-shaped body made of orange and yellow fire with a flaming head, wearing a dark jacket',
'frost':'the Frost Lich: an undead ice king with pale blue skin, a crown of ice spikes, a black leather jacket with spikes, black trousers and boots',
'tokyo':'the Kitsune: an upright fox in a black leather jacket with white stars and blue jeans, with nine fluffy orange tails',
'bali':'the Bronze Warden: a golden bronze statue-man with a golden crown, bare chest, gold ornaments and gold greaves',
'lanai':'the Slack-Key Honu: an old sea turtle in a straw hat and a red aloha shirt with white flowers, a green shell on its back, green legs',
'outback':'the Drop Bear: a koala with big round ears in a blue work shirt, grey legs',
'grotto':'the Glowworm Queen: a woman with pale blue skin, long teal hair, a small gold crown and a long teal gown with sparkles',
'mess':'the Emperor: an emperor penguin standing upright, black back, white belly, yellow-orange neck patch, flippers instead of arms (the flippers hold the guitar)',
'aurora':'the Aurora: a woman with blue skin and flowing green and purple hair, a midnight-blue dress with stars that fades into green legs',
'pole':'the Silence: a figure in a big white hooded parka, face hidden in shadow, white boots'}
for cid,who in LOOK.items():
    if cid=='ghat': continue
    g=G.get(cid,{'gt':'single','body':'#E8A83A'}); h=json.load(open(R+f'callers/{cid}_body.json'))['h']
    guitar(cid,R+f'gemini_test/callers/{cid}_body.jpg',g['gt'],f"a {GN.get(g['gt'],'guitar')} with a {g['body']} coloured body",who,h)
# band: instrument kinds
def band(cid,kind,who,inst,h,ref=None):
    CH[cid]=dict(kind=kind,ref=ref or R+f'portraits/{cid}.png',who=who,inst=inst,height=h,band=True)
band('lou','drums','a drummer (a grey-haired man) seated behind a small drum kit: snare, red kick drum, hi-hat and one cymbal, the kit shown in full','drum kit',90)
band('rosa','drums','a drummer (a woman) seated behind a small drum kit: snare, red kick drum, hi-hat and one cymbal, the kit shown in full','drum kit',90)
band('dee','guitar','a bass player standing, playing a four-string electric bass guitar','bass guitar',90)
band('jo','keys','a keyboard player standing behind a keyboard on an X-shaped stand','keyboard',86)
band('hale','sing','a singer standing at a microphone on a tall stand','microphone',92)
band('tam','guitar','a guitarist playing a red double-neck electric guitar: the guitar clearly has TWO necks and TWO headstocks, one stacked above the other','double-neck guitar',90)
band('brass','horn','a horn player standing, playing a brass trumpet','trumpet',88)
band('brassb','horn','a horn player standing, playing a brass trumpet','trumpet',90,R+'gemini_test/band/brassb_sheet.jpg')
band('brassc','horn','a horn player standing, playing a brass trumpet','trumpet',88,R+'gemini_test/band/brassc_sheet.jpg')
for c in ('dee',):
    CH[c]['guitar']=R+'guitars/humbucker.png'; CH[c]['gdesc']=CH[c]['inst']
CH['tam']['guitar']=None   # a double-neck has no matching game guitar sprite: describe it in words only (a gold single-neck reference made the playing poses gold)
for c,v in list(CH.items()):
    if v.get('band') and v['kind']!='guitar': v.setdefault('guitar',None)
# the Guitar Tech, the Green Room's caller (v1.63): her own reference from gen_rooms.py; no game guitar sprite matches her Telecaster, so it is described in words
guitar('green',R+'gemini_test/rooms/tech.png','single','a Telecaster-style electric guitar with a sunburst body and a cream pickguard','the Guitar Tech: a roadie woman in her forties with a short grey-streaked dark bob, a headlamp on a band, a black T-shirt under a dark utility vest with picks and a string winder, a roll of gaffer tape and a wrench on her belt, olive cargo trousers and brown work boots',100)
CH['green']['guitar']=None

# v1.67: Mister Midnight was redrawn as a moon spirit (the old look, dark skin with white eyes and a wide grin, read as a minstrel caricature)
CH['juke']['ref']=R+'gemini_test/callers/juke_moon.png'; CH['juke']['gdesc']='a silver resonator guitar with a round metal cone'
# v1.74: three new players
guitar('smith',R+'gemini_test/chars/smith_body.png','baritone','a dark brown baritone electric guitar with a long neck','the Blacksmith: a broad friendly woman blacksmith with soot on her cheeks, a short dark undercut with a braid, a thick brown leather apron over a sleeveless black T-shirt, leather bracers and gloves, heavy brown boots, a small hammer on her belt',104)
guitar('wizard',R+'gemini_test/chars/wizard_body.png','single','a teal-green Stratocaster-style electric guitar with a cream pickguard','the Math Rock Wizard: a lanky young wizard with round glasses and a short beard, a deep blue pointed hat and long robe embroidered with small gold numbers, triangles and fractions, brown sneakers, a small abacus charm on his belt',104)
# v1.75: the King replaced by the Herald; the Journeyman added
guitar('herald',R+'gemini_test/chars/herald_body.png','humbucker','a white solid-body electric guitar with two sharp pointed horns, three pickups and gold hardware','the Herald: a joyful Black woman guitarist in her forties, small gold earrings, short sculpted 1940s curls, an elegant floor-length 1940s gown of wine-red brocade with a swirling gold pattern, short puffed sleeves, a ruffled V neckline, a wide dark velvet sash at the waist, a small gold trumpet brooch, low heels',104)
guitar('journey',R+'gemini_test/chars/journey_body.png','single','a worn butterscotch Telecaster-style electric guitar with a black pickguard','the Journeyman: a weathered kind session guitarist in his sixties with a short grey beard, reading glasses pushed up on his forehead, a brown flat cap, a worn mustard cardigan over a work shirt, brown corduroy trousers, a leather tool roll of picks and capos strapped across his chest',104)
