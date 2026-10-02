# generic Gemini image call. usage: python3 gen_img.py OUT "prompt" [aspect] [ref.png ...]   (model: env GEM, default gemini-2.5-flash-image)
import json,base64,subprocess,sys,os,io
from PIL import Image
out,prompt=sys.argv[1],sys.argv[2]; aspect=sys.argv[3] if len(sys.argv)>3 else '1:1'; refs=sys.argv[4:]
parts=[{"text":prompt}]
for r in refs:
    b=io.BytesIO(); Image.open(r).convert('RGB').save(b,'PNG'); parts.append({"inlineData":{"mimeType":"image/png","data":base64.b64encode(b.getvalue()).decode()}})
body=json.dumps({"contents":[{"parts":parts}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":aspect}}})
rq=f"/tmp/req_{os.path.basename(out)}.json"; open(rq,"w").write(body)
M=os.environ.get('GEM','gemini-2.5-flash-image')
for _ in range(3):
    r=subprocess.run(["curl","-sS","-X","POST",f"https://generativelanguage.googleapis.com/v1beta/models/{M}:generateContent","-H","Content-Type: application/json","-d","@"+rq],capture_output=True,text=True)
    try: d=json.loads(r.stdout)
    except Exception: continue
    for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]):
        if 'inlineData' in p: open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); print('saved',out); sys.exit(0)
print('FAILED',out,str(d)[:200])
