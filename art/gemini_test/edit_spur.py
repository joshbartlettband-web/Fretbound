import json,base64,subprocess,sys
src=base64.b64encode(open(sys.argv[1],'rb').read()).decode()
prompt=("Edit this pixel-art stage backdrop. Keep everything else exactly the same: same composition, colours, pixel style, empty floor. "
"Only fix proportions: the hanging wagon wheel must be a perfect circle with evenly spaced spokes (it is currently slightly squashed), "
"and the mounted longhorn skull and any framed picture must have natural, undistorted proportions. Do not add anything new.")
body=json.dumps({"contents":[{"parts":[{"text":prompt},{"inlineData":{"mimeType":"image/png","data":src}}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"21:9"}}})
open("/tmp/req.json","w").write(body)
r=subprocess.run(["curl","-sS","-X","POST","https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent","-H","Content-Type: application/json","-d","@/tmp/req.json"],capture_output=True,text=True)
d=json.loads(r.stdout)
if 'error' in d: print(d['error']); sys.exit(1)
for p in d['candidates'][0]['content']['parts']:
    if 'inlineData' in p: open(sys.argv[2],'wb').write(base64.b64decode(p['inlineData']['data'])); print('saved',sys.argv[2])
