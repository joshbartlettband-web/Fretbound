# Gemini image edit of a stage source. usage: python3 edit_stage.py ID "instruction"   (writes stages/ID_edit.png; review, then move over stages/ID.jpg)
import json,base64,subprocess,sys
from PIL import Image
import io
i,ins=sys.argv[1],sys.argv[2]
buf=io.BytesIO(); Image.open(f'stages/{i}.jpg').convert('RGB').save(buf,'PNG'); src=base64.b64encode(buf.getvalue()).decode()
prompt=("Edit this pixel-art stage backdrop. Keep everything else exactly the same: same composition, colours, lighting, pixel style, empty floor, same positions of all other objects. "+ins+" Do not add anything else.")
body=json.dumps({"contents":[{"parts":[{"text":prompt},{"inlineData":{"mimeType":"image/png","data":src}}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"21:9"}}})
open("/tmp/req_edit_"+i+".json","w").write(body)
for _ in range(3):
    r=subprocess.run(["curl","-sS","-X","POST","https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent","-H","Content-Type: application/json","-d","@/tmp/req_edit_"+i+".json"],capture_output=True,text=True)
    d=json.loads(r.stdout)
    for p in d.get('candidates',[{}])[0].get('content',{}).get('parts',[]):
        if 'inlineData' in p: open(f'stages/{i}_edit.png','wb').write(base64.b64decode(p['inlineData']['data'])); print('saved',i); sys.exit(0)
print('failed',str(d)[:300])
