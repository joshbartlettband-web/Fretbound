import json,base64,subprocess,sys
prompt="Painted pixel-art style landscape backdrop, wide 4:3, North America at sunset: flat open desert plain with a low straight horizon in the lower third, distant mesas, a lone water tower and telephone poles silhouetted, warm orange and magenta sky with soft streaky clouds, no people, no text, no road, no watermark. Warm palette, dark brown outlines on landmarks."
body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["IMAGE"]}})
r=subprocess.run(["curl","-sS","-X","POST","https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent","-H","Content-Type: application/json","-d",body],capture_output=True,text=True)
d=json.loads(r.stdout)
if 'error' in d: print(d['error']); sys.exit(1)
for p in d['candidates'][0]['content']['parts']:
    if 'inlineData' in p:
        open('na_test.png','wb').write(base64.b64decode(p['inlineData']['data'])); print('saved na_test.png')
