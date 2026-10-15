# Gemini image edit. usage: python3 edit_room.py IN.png OUT.png "instruction" [model] [aspect]   (v1.85; IN may be a rooms/ key)
import json,base64,subprocess,sys,io
from PIL import Image
k,out,ins=sys.argv[1],sys.argv[2],sys.argv[3]; model=sys.argv[4] if len(sys.argv)>4 else 'gemini-3-pro-image'; asp=sys.argv[5] if len(sys.argv)>5 else '16:9'
import os; src_path=k if os.path.exists(k) else f'rooms/{k}.png'; k=os.path.basename(k).split('.')[0]
buf=io.BytesIO(); Image.open(src_path).convert('RGB').save(buf,'PNG'); src=base64.b64encode(buf.getvalue()).decode()
prompt=("Edit this pixel-art game picture. Keep everything else exactly the same: same composition, framing, colours, lighting, pixel style, and the same positions and sizes of every object. "+ins+" Do not add anything else.")
body=json.dumps({"contents":[{"parts":[{"text":prompt},{"inlineData":{"mimeType":"image/png","data":src}}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":asp}}})
req="/tmp/req_edit_"+os.path.basename(out)+".json"; open(req,"w").write(body)
for _ in range(3):
    r=subprocess.run(["curl","-sS","-X","POST",f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent","-H","Content-Type: application/json","-d","@"+req],capture_output=True,text=True)
    try: d=json.loads(r.stdout)
    except Exception: print('bad',r.stdout[:200]); continue
    for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]):
        if 'inlineData' in p: open(out,'wb').write(base64.b64decode(p['inlineData']['data'])); print('saved',out); sys.exit(0)
    print('retry',str(d)[:300])
print('failed')
