# One 4x2 pose sheet for one character, from several references, on a Nano Banana model.  usage: python3 gen_sheet.py ID A|B [candidate-number] [model]
# Output: out/<id>_<sheet>_<n>.png.  References sent: (1) the character, (2) a style anchor, (3) the guitar, (4) the stick-figure pose guide for the sheet.
import sys,os,io,json,base64,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import poses
R='/home/user/Fretbound/art/'
CH={
 'bard':dict(ref=R+'gemini_test/chars/bard_body.jpg',guitar=R+'guitars/single.png',gdesc='a teal-green electric guitar (Stratocaster style, cream pickguard, maple neck)',who='the Bard: a young man in a red feathered hat, green tunic, blue cape, brown trousers and boots'),
 'ghat':dict(ref=R+'gemini_test/callers/ghat_body.jpg',guitar=R+'guitars/nylon.png',gdesc='an acoustic guitar with an orange-brown body',who='the Tiger: an upright tiger in a white kurta and white trousers with an orange marigold garland, orange paws'),
}
STYLE=R+'gemini_test/band/dee_sheet.jpg'
def img_part(path):
    b=io.BytesIO(); im=Image.open(path).convert('RGBA'); bg=Image.new('RGB',im.size,(255,0,255)); bg.paste(im,(0,0),im); bg.save(b,'PNG'); return {"inlineData":{"mimeType":"image/png","data":base64.b64encode(b.getvalue()).decode()}}
def prompt(cid,which):
    c=CH[cid]; P=poses.A if which=='A' else poses.B
    lst='\n'.join(f'{i+1}. {n}: {d}' for i,(n,d) in enumerate(P))
    return (f"Make ONE pixel-art sprite sheet of a single game character in 8 poses, on a flat solid pure magenta (#FF00FF) background, crisp pixels, thick dark brown outline, warm hand-painted palette, no text, no labels, no watermark, no shadows.\n"
     f"REFERENCE 1 is the character: {c['who']}. Keep the exact same face, hair, clothes, colours and proportions in every pose; every pose must also show BOTH arms and the guitar fully painted in (no arm missing).\n"
     f"REFERENCE 2 shows the art style and scale to match (a finished sprite sheet of another character).\n"
     f"REFERENCE 3 is the guitar the character plays: {c['gdesc']}. The same guitar in every pose, held across the body with the neck pointing RIGHT and up a little.\n"
     f"REFERENCE 4 is a stick-figure POSE GUIDE for the layout: 4 columns by 2 rows, one pose per cell, numbered left to right, top to bottom. Follow the guide's layout and pose order exactly, but do NOT draw the guide's lines, numbers or the yellow stick; draw the real character instead.\n"
     f"Every figure faces RIGHT (side view), is the SAME size and stands on the SAME baseline in its row, centered in its own cell, with wide empty magenta gaps so nothing touches or overlaps.\nThe 8 poses:\n{lst}")
def main():
    cid,which=sys.argv[1],sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 1; M=sys.argv[4] if len(sys.argv)>4 else 'gemini-3-pro-image'
    os.makedirs('out',exist_ok=True); gp=f'out/guide_{which}.png'; poses.guide(gp,which)
    c=CH[cid]; refs=[c['ref'],STYLE,c['guitar'],gp]; idle=f'out/{cid}_idle_ref.png'
    if os.path.exists(f'out/{cid}_A_1.png'):   # the idle pose of the first sheet: head, body and feet of every playing pose must match it
        im=Image.open(f'out/{cid}_A_1.png'); W,H=im.size; im.crop((0,0,W//4,H//2)).save(idle); refs.append(idle)
    parts=[{"text":prompt(cid,which)+(' REFERENCE 5 is the exact idle pose to copy: in every pose that is supposed to match idle, the head, torso, legs and feet must sit in exactly the same place, pixel for pixel; only the parts named in the pose list may change.' if len(refs)>4 else '')}]+[img_part(p) for p in refs]
    body=json.dumps({"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9","imageSize":"2K"}}})
    rq=f'/tmp/req_{cid}_{which}_{n}.json'; open(rq,'w').write(body); out=f'out/{cid}_{which}_{n}.png'
    for t in range(3):
        r=subprocess.run(["curl","-sS","-X","POST",f"https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent","-H","Content-Type: application/json","-d","@"+rq],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except Exception: continue
        for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]):
            if 'inlineData' in p: open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); print('saved',out,Image.open(out).size); return
    print('FAILED',out,str(d)[:300])
if __name__=='__main__': main()
