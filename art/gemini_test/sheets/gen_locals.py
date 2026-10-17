# v1.94: the people you meet on the road. One 4x2 sheet of 8 relaxed poses per local (same poses and layout as gen_hang.py, so the road scene's
# talk/listen/react slots work), from a text description only (no reference picture) plus the house style sheet. Pro model, 2K, logged in spend.log.
# usage: python3 gen_locals.py [id ...] [--n N]   -> out/hang_<id>_<n>.png ; LOCALS below also gives each local's sprite height
import sys,os,json,base64,subprocess,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from concurrent.futures import ThreadPoolExecutor
import gen_sheet as GS
from gen_hang import POSES
WORLD=("The world is our modern world with a little lazy, casual magic in it: people are ordinary, a bit scruffy and kind, never epic. ")
LOCALS={
 'gerald':(92,"Gerald, a soft, scruffy, slightly round middle-aged unicorn standing on four legs: off-white shaggy coat, a faded pastel rainbow mane and tail, a short blunt golden horn, a long hand-knitted red-and-yellow scarf, kind sleepy eyes. He was the host of a 1990s public-television counting show. He is a real four-legged horse-shaped unicorn: he stands on ALL FOUR HOOVES in every pose, he has hooves, never hands, and never stands up on two legs. Instead of hand gestures he tilts his head, lifts one front hoof, swishes his tail; for 'sipping' he sips from a paper cup held in his mouth; for 'stretching' he does a big yawning stretch like a cat, front legs forward."),
 'owner':(102,"a pawn shop owner in his sixties: bald on top with grey side hair, round glasses on a chain, a cardigan with a pocket full of guitar picks, a jeweller's loupe on a cord, slippers."),
 'fan':(98,"a superfan in her twenties: a homemade white T-shirt with a hand-drawn guitarist's face on it, a lanyard with backstage-pass-style badges, a bucket hat, sneakers, a tote bag with a cat face on it."),
 'radiohost':(100,"a small-town morning radio host: big over-ear headphones around the neck, a colourful knitted sweater, a mug of coffee, cheerful, curly hair."),
 'producer':(104,"a record producer in a cosy studio: a worn denim jacket, a baseball cap, a beard, a pencil behind one ear, comfortable boots."),
 'teahost':(104,"a Tuareg musician from the Sahara who hosts tea: an indigo tagelmust headscarf wrapped around the head and face showing kind eyes, a long flowing pale blue robe, leather sandals, warm and welcoming."),
 'tailor':(102,"a sharp-dressed Kinshasa tailor in the sapeur style: a perfectly cut bright lemon-yellow suit (NOT pink, NOT purple), a patterned teal silk tie, a pocket square, two-tone shoes, a tape measure around the neck, a proud, stylish posture."),
 'coffeehost':(98,"an Ethiopian woman hosting a coffee ceremony: a white habesha kemis dress with a colourful woven border, a netela shawl, her hair in braids, gentle and generous."),
 'drummer':(104,"a samba school drummer from Rio: a bright yellow-and-green T-shirt, white shorts, sneakers, a wide grin, drumsticks tucked in a back pocket (no drum)."),
 'teacher':(102,"a tango teacher from Buenos Aires in her fifties: a black fitted dress, a red shawl, her hair in a neat bun, elegant dance shoes, very upright posture."),
 'seller':(100,"a market stall seller in Lima: a patterned knitted vest over a shirt, a flat cap, a cash pouch on a strap, relaxed and amused."),
 'violinist':(102,"a Paris Metro busker violinist: a long striped scarf, a beret, a worn wool coat, fingerless gloves, a violin case on a strap over the back (no violin in hand)."),
 'singer':(102,"a flamenco singer from Andalusia, late at night: a crisp white shirt open at the collar, a black waistcoat, dark trousers, slicked-back grey hair, a strong expressive face."),
 'deckhand':(104,"a Norwegian ferry deckhand: an orange waterproof jacket, a knitted beanie, a thick beard, rubber boots, rosy cheeks, cheerful in the cold."),
 'chaiseller':(100,"an elderly chai seller by the river steps in Varanasi: a white kurta and dhoti, a shawl, a grey moustache, a small kettle in one hand, calm and smiling."),
 'leader':(100,"a Balinese gamelan leader: a white udeng head cloth, a white shirt, a patterned sarong, bare feet, calm and patient, a pair of small wooden mallets tucked in the sash."),
 'bonfireplayer':(102,"a Hawaiian musician at a beach bonfire: a faded aloha shirt with flowers, shorts, bare feet, a flower lei, long dark hair, relaxed and smiling."),
 'quizmaster':(102,"a New Zealand pub quizmaster: a teal shirt with a bold white polka-dot pattern (the same shirt in every pose), a sparkly gold bow tie, a clipboard, reading glasses on the head, big friendly grin."),
 'partyhost':(100,"a student hosting a garage show in Dunedin: a band T-shirt (no text), a flannel shirt tied around the waist, ripped jeans, messy hair, a slightly worried but excited look."),
}
def prompt(cid):
    lst='\n'.join(f'{i+1}. {n}: {d}' for i,(n,d) in enumerate(POSES))
    return (f"Make ONE pixel-art sprite sheet of a single game character in 8 relaxed poses, on a flat solid pure magenta (#FF00FF) background that fills the whole image edge to edge (not white, no shadows), crisp chunky pixel art (not smooth cartoon art), thick dark brown outline, warm hand-painted palette, no text, no labels, no numbers, no watermark.\n"
     f"{WORLD}The character: {LOCALS[cid][1]} Keep the exact same face, body, clothes, colours and proportions in every pose.\n"
     "The character holds no musical instrument. Full body from head to feet in every pose, both feet fully painted.\n"
     "REFERENCE 1 shows the art style and scale to match (a finished sprite sheet of another character).\n"
     "Layout: 4 columns by 2 rows, one pose per cell, numbered left to right, top to bottom. Every figure faces RIGHT (side or three-quarter view), is the SAME size and stands on the SAME baseline in its row, centered in its own cell, with wide empty magenta gaps so nothing touches or overlaps.\nThe 8 poses:\n"+lst)
def gen(cid,n):
    M='gemini-3-pro-image'; out=f'out/hang_{cid}_{n}.png'
    body=json.dumps({"contents":[{"parts":[{"text":prompt(cid)},GS.img_part(GS.STYLE)]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9","imageSize":"2K"}}})
    rq=f'/tmp/req_local_{cid}_{n}.json'; open(rq,'w').write(body); d={}
    for t in range(3):
        r=subprocess.run(["curl","-sS","-X","POST",f"https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent","-H","Content-Type: application/json","-d","@"+rq],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except Exception: continue
        if 'spending cap' in str(d): return cid,'CAP'
        for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]):
            if 'inlineData' in p:
                open(out,'wb').write(base64.b64decode(p['inlineData']['data']))
                open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','spend.log'),'a').write(time.strftime('%Y-%m-%d %H:%M')+'\t'+M+'\t0.134\t'+os.path.basename(out)+'\n')
                return cid,'saved '+out
    return cid,'FAILED '+str(d)[:200]
if __name__=='__main__':
    os.makedirs('out',exist_ok=True); a=sys.argv[1:]; n=1
    if '--n' in a: i=a.index('--n'); n=int(a[i+1]); a=a[:i]+a[i+2:]
    ids=a or list(LOCALS)
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(lambda c:gen(c,n),ids): print(*r,flush=True)
