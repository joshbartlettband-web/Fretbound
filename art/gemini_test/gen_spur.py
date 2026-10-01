import json,base64,subprocess,sys
prompt=("Pixel-art painted interior of a small Western honky-tonk bar stage, side-on flat view like a 2D game backdrop, very wide panoramic. "
"Back wall of warm brown wooden planks with a long shelf of bottles on the left, a wagon wheel chandelier and string of warm bulbs, a mounted longhorn skull above the center, tweed guitar amps at far left and far right, a jukebox glowing in a corner. "
"Wooden stage floor of worn honey-colored planks across the bottom fifth of the image. The center of the stage and floor must be EMPTY and uncluttered so characters can be placed on top. "
"No people, no text, no neon words, no watermark. Warm amber lighting, dark brown outlines, 64-colour palette feel, crisp pixels.")
body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["IMAGE"],"imageConfig":{"aspectRatio":"21:9"}}})
r=subprocess.run(["curl","-sS","-X","POST","https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent","-H","Content-Type: application/json","-d",body],capture_output=True,text=True)
d=json.loads(r.stdout)
if 'error' in d: print(d['error']); sys.exit(1)
for p in d['candidates'][0]['content']['parts']:
    if 'inlineData' in p: open(sys.argv[1],'wb').write(base64.b64decode(p['inlineData']['data'])); print('saved',sys.argv[1])
