# One 4x2 sheet of 8 relaxed "hanging out by the van" poses per character, with NO instrument.  usage: python3 gen_hang.py ID [candidate-number]   -> out/hang_<id>_<n>.png (2K, magenta)
import sys,os,io,json,base64,subprocess
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import gen_sheet as GS
CH=GS.CH
POSES=[('chatting','talking with a small hand gesture, mouth open, friendly'),('laughing','head tipped back a little, a big grin, one hand on the belly'),
 ('listening','arms crossed, weight on one hip, relaxed, a small smile'),('hands in pockets','both hands in the pockets, shoulders relaxed, looking ahead and smiling'),
 ('sipping','sipping from a small paper coffee cup held in one hand, the other hand relaxed'),('explaining','pointing off ahead with one hand and explaining something, the other hand on the hip'),
 ('shrugging','shrugging with both palms up and a cheeky smile'),('stretching','both arms stretched up overhead, a big yawn, after a long drive')]
def prompt(cid):
    c=CH[cid]; lst='\n'.join(f'{i+1}. {n}: {d}' for i,(n,d) in enumerate(POSES))
    return (f"Make ONE pixel-art sprite sheet of a single game character in 8 relaxed poses, on a flat solid pure magenta (#FF00FF) background, crisp pixels, thick dark brown outline, warm hand-painted palette, no text, no labels, no numbers, no watermark.\n"
     f"REFERENCE 1 is the character: {c['who']}. Keep the exact same face, body, clothes, colours and proportions in every pose.\n"
     "IMPORTANT: the character holds NO instrument and has none anywhere: no guitar, no drum kit, no keyboard, no microphone or stand, no horn, no stage gear. Just the person, standing, hanging out with friends beside a touring van after a show, chatting and enjoying themselves. Both arms and both feet are fully painted.\n"
     "REFERENCE 2 shows the art style and scale to match (a finished sprite sheet of another character).\n"
     "Layout: 4 columns by 2 rows, one pose per cell, numbered left to right, top to bottom. Every figure faces RIGHT (side or three-quarter view), is the SAME size and stands on the SAME baseline in its row, centered in its own cell, with wide empty magenta gaps so nothing touches or overlaps.\nThe 8 poses:\n"+lst+os.environ.get('EXTRA',''))
def main():
    cid=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 1; M='gemini-3-pro-image'
    os.makedirs('out',exist_ok=True); out=f'out/hang_{cid}_{n}.png'
    parts=[{"text":prompt(cid)},GS.img_part(CH[cid]['ref']),GS.img_part(GS.STYLE)]
    body=json.dumps({"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"16:9","imageSize":os.environ.get("SHEET_SIZE","2K")}}})
    rq=f'/tmp/req_hang_{cid}_{n}.json'; open(rq,'w').write(body); d={}
    for t in range(3):
        r=subprocess.run(["curl","-sS","-X","POST",f"https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent","-H","Content-Type: application/json","-d","@"+rq],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except Exception: continue
        for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]):
            if 'inlineData' in p: open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); print('saved',out,Image.open(out).size); return
    print('FAILED',out,str(d)[:400])
if __name__=='__main__': main()
