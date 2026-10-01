# Two-pose sprite sheets for the seven band members, from their portraits. usage: python3 gen_band.py [id ...]
import subprocess,sys
from concurrent.futures import ThreadPoolExecutor
BASE=("Pixel-art game sprite sheet on a solid flat pure magenta (#FF00FF) background, crisp pixels, thick dark brown outline, warm hand-painted palette, no shadows, no text, no watermark. "
 "The exact character from the reference portrait (same face, hair, clothes and colours), full body, flat side view facing RIGHT. TWO poses side by side in one row, identical size and scale, standing on the same baseline, with a wide empty magenta gap between them so nothing touches. ")
P={
'lou':"A drummer, seated behind a small drum kit (snare, red kick drum, hi-hat and one cymbal), the kit and drummer shown in full. Pose 1: both drumsticks raised up high. Pose 2: both sticks coming down, striking the snare and hi-hat.",
'rosa':"A drummer, seated behind a small drum kit (snare, red kick drum, hi-hat and one cymbal), the kit and drummer shown in full. Pose 1: both drumsticks raised up high. Pose 2: both sticks coming down, striking the snare and hi-hat.",
'dee':"A bass player standing, playing a four-string electric bass guitar held across the body with the neck pointing right. Pose 1: relaxed groove, head up. Pose 2: plucking hard, head nodding forward.",
'jo':"A keyboard player standing behind a keyboard on an X-shaped stand, the keyboard in front of the body. Pose 1: both hands on the left half of the keys. Pose 2: both hands on the right half of the keys, head swaying.",
'hale':"A singer standing at a microphone on a tall stand. Pose 1: one hand holding the mic stand, mouth closed, listening. Pose 2: singing with an open mouth, head tilted back a little, free arm raised.",
'tam':"A guitarist standing, playing a red double-neck electric guitar. IN BOTH POSES the guitar clearly has TWO necks and TWO headstocks, one stacked above the other, like a Gibson EDS-1275. Pose 1: relaxed stance, double-neck guitar held across the body. Pose 2: strumming hard with the head nodding forward.",
'brass':"A horn player standing, playing a brass trumpet held out in front pointing right. Pose 1: playing, trumpet held level. Pose 2: trumpet raised high, pointing up and to the right, chest out.",
}
def gen(i):
    r=subprocess.run(["python3","gen_img.py",f"band/{i}_sheet.png",BASE+P[i],"3:2",f"../portraits/{i}.png"],capture_output=True,text=True); return i,(r.stdout+r.stderr).strip()[-50:]
ids=sys.argv[1:] or list(P)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(gen,ids): print(*r)
