"""Builds the landing page's pictures from the raw screens made by shots.py.

  python3 tools/landing/make_landing.py        (reads $RAW, default /tmp/fretbound-shots)

Writes to landing/:
  screen-<name>.png   the screens, 390x844, 256-colour PNGs
  card.png            1200x630 link preview (og:image), drawn as HTML and photographed by Chromium
  more/fretbound.gif  240 px wide animated tour of five screens, 1.2 s a frame, looping
  fonts/*.woff2       the game's own fonts, copied out of index.html (so the redrawn Pixelify Sans digits match)
Needs Pillow, fontTools with brotli (pip install brotli) and Playwright.
"""
import base64, io, os, re
from PIL import Image

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
RAW = os.environ.get('RAW', '/tmp/fretbound-shots')
OUT = os.path.join(REPO, 'landing')
os.makedirs(os.path.join(OUT, 'more'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'fonts'), exist_ok=True)

SCREENS = ['title', 'chars', 'soundcheck', 'venue', 'duel', 'backstage', 'van']
GIF = ['title', 'chars', 'venue', 'duel', 'backstage']

# 1. fonts, straight out of the game
FONTS = {('Jacquard 24', '400'): 'jacquard24.woff2', ('Jersey 10', '400'): 'jersey10.woff2',
         ('Pixelify Sans', '400'): 'pixelify-400.woff2', ('Pixelify Sans', '700'): 'pixelify-700.woff2'}
html = open(os.path.join(REPO, 'index.html'), encoding='utf-8').read()
for m in re.finditer(r"@font-face\{font-family:'([^']*)'([^}]*?)url\(data:font/woff2;base64,([A-Za-z0-9+/=]*)\)([^}]*)\}", html):
    w = re.search(r'font-weight:(\d+)', m.group(2) + m.group(4))
    key = (m.group(1), w.group(1) if w else '400')
    if key in FONTS:
        open(os.path.join(OUT, 'fonts', FONTS[key]), 'wb').write(base64.b64decode(m.group(3)))
        print('font', FONTS[key])

# 2. screens
def q256(im):
    return im.convert('RGB').quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)

raw = {n: Image.open(os.path.join(RAW, n + '.png')).convert('RGB') for n in SCREENS}
for n, im in raw.items():
    q256(im).save(os.path.join(OUT, 'screen-%s.png' % n), optimize=True)

# 3. the animated GIF: one shared palette so frames do not flicker
W = 240
frames = [raw[n].resize((W, round(raw[n].height * W / raw[n].width)), Image.LANCZOS) for n in GIF]
strip = Image.new('RGB', (W, frames[0].height * len(frames)))
for i, f in enumerate(frames):
    strip.paste(f, (0, i * f.height))
pal = strip.quantize(255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
gf = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
gf[0].save(os.path.join(OUT, 'more', 'fretbound.gif'), save_all=True, append_images=gf[1:],
           duration=1200, loop=0, optimize=True, disposal=1)

# 4. the link card, 1200x630
CARD = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:'Jacquard 24';src:url(fonts/jacquard24.woff2) format('woff2')}
@font-face{font-family:'Jersey 10';src:url(fonts/jersey10.woff2) format('woff2')}
@font-face{font-family:'Pixelify Sans';src:url(fonts/pixelify-400.woff2) format('woff2')}
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{background:#1C0E0E radial-gradient(ellipse at 20% 0%,#4a2414 0,#1C0E0E 70%);color:#FFF0D0;font-family:'Pixelify Sans',monospace;position:relative}
.edge{position:absolute;inset:14px;border:3px solid #D9A441;box-shadow:0 0 0 3px #0E0404,inset 0 0 0 3px #0E0404}
.txt{position:absolute;left:70px;top:120px;width:560px}
h1{font-family:'Jacquard 24',serif;font-weight:400;font-size:150px;line-height:.9;margin:0 0 26px;color:#FFC857;text-shadow:5px 5px 0 #A8261C,10px 10px 0 #1A0606}
p{font-size:34px;line-height:1.25;margin:0 0 30px;color:#FFE3A6}
.tag{display:inline-block;font-family:'Jersey 10',monospace;font-size:36px;padding:8px 22px 10px;background:#E0A030;color:#2A1206;border:3px solid #D9A441;box-shadow:0 0 0 3px #0E0404,0 6px 0 3px #0E0404}
.ph{position:absolute;top:46px;height:538px;border:3px solid #D9A441;box-shadow:0 0 0 3px #0E0404,0 10px 30px rgba(0,0,0,.6);image-rendering:pixelated}
</style></head><body><div class="edge"></div>
<div class="txt"><h1>Fretbound</h1><p>A roguelike ear-training game for guitarists. Hear the phrase, play it back.</p><span class="tag">PLAY IN YOUR BROWSER</span></div>
<img class="ph" src="screen-duel.png" style="left:656px"><img class="ph" src="screen-title.png" style="left:922px">
</body></html>"""
tmp = os.path.join(OUT, '_card.html')
open(tmp, 'w').write(CARD)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1200, 'height': 630})
    pg.goto('file://' + tmp); pg.wait_for_timeout(600)
    pg.screenshot(path=os.path.join(OUT, 'card.png'))
    b.close()
os.remove(tmp)
q256(Image.open(os.path.join(OUT, 'card.png'))).save(os.path.join(OUT, 'card.png'), optimize=True)

total = 0
for root, _, files in os.walk(OUT):
    for f in sorted(files):
        if f.endswith('.html'): continue
        s = os.path.getsize(os.path.join(root, f)); total += s
        print('%-28s %7d' % (os.path.relpath(os.path.join(root, f), OUT), s))
print('total pictures and fonts: %d bytes' % total)
