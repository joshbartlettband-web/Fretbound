# Standing full-body sprites for the 21 callers, from their portraits. usage: python3 gen_callers.py [id ...]
import subprocess,sys,json
from concurrent.futures import ThreadPoolExecutor
IDS="spur tide juke dunes sebene azmari rio milonga chicha paris cave frost tokyo ghat bali lanai outback grotto mess aurora pole".split()
NOTE={'tide':'a siren with a long fish tail, shown standing upright balanced on the tail fin','cave':'a living flame spirit shaped like a person, with a body of solid painted flames in orange, red and yellow (opaque, no transparency)','aurora':'a spirit of light, shown as a solid opaque figure painted in green, blue and violet aurora colours (opaque, no transparency)','pole':'a pale figure of ice and snow, solid and opaque','mess':'a standing emperor penguin in a tuxedo, upright on two feet','lanai':'a standing sea turtle character, upright on two legs','outback':'a standing koala-headed character, upright on two legs','dunes':'a figure of swirling sand shaped like a person, solid and opaque with a clear outline','grotto':'a queen figure with softly glowing blue-green lights, solid and opaque'}
def gen(i):
    extra=NOTE.get(i,'')
    pr=("Pixel-art game sprite on a solid flat pure magenta (#FF00FF) background, crisp pixels, thick dark brown outline, warm hand-painted palette, no shadow on the background, no text, no watermark. "
        "Subject: the exact character from the reference portrait (same face, head, colours and costume)"+(", "+extra if extra else "")+", shown FULL BODY from head to feet, flat side view facing right like a 2D platformer sprite, standing relaxed and upright, both arms hanging straight down at the sides with hands relaxed, and NO guitar. Whole figure in frame with generous margin, nothing cropped.")
    r=subprocess.run(["python3","gen_img.py",f"callers/{i}_body.png",pr,"3:4",f"../portraits/{i}.png"],capture_output=True,text=True); return i,(r.stdout+r.stderr).strip()[-60:]
ids=sys.argv[1:] or IDS
with ThreadPoolExecutor(5) as ex:
    for r in ex.map(gen,ids): print(*r)
