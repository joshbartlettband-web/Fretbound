"""Screenshots of Fretbound for the landing page (landing/).

Plays the game in headless Chromium at a phone portrait size (390x844) and saves the raw
screens to $RAW (default /tmp/fretbound-shots). Then run make_landing.py to build the
optimised pictures, card.png and more/fretbound.gif in landing/.

  bash tests/dev/pwfix.sh        # once, if Playwright cannot find Chromium
  python3 tools/landing/shots.py
  python3 tools/landing/make_landing.py
"""
import os, time
from playwright.sync_api import sync_playwright

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
URL = 'file://' + os.path.join(REPO, 'index.html')
RAW = os.environ.get('RAW', '/tmp/fretbound-shots')
os.makedirs(RAW, exist_ok=True)
VIEW = {"width": 390, "height": 844}
OPEN = [64, 59, 55, 50, 45, 40]          # open strings, high E to low E (as in tests/gplay.py)


def wait(pg, js, tries=150):
    for _ in range(tries):
        if pg.evaluate(js):
            return True
        time.sleep(0.1)
    return False


def shot(pg, name):
    pg.screenshot(path=os.path.join(RAW, name + '.png'))
    print('saved', name)


def tap_note(pg, midi):
    """Tap one note on the neck, sliding the neck first if needed (from tests/gplay.py)."""
    for _ in range(25):
        s = pg.evaluate("({pos:window.__fb.state.pos,win:window.__fb.state.win,broken:window.__fb.state.broken,g:window.__fb.geo})")
        found = None
        for st in range(6):
            f = midi - OPEN[st]
            if not s['broken'][st] and s['pos'] <= f < s['pos'] + s['win'] and 0 <= f <= 15:
                found = (st, f); break
        if found: break
        anyf = [midi - OPEN[st] for st in range(6) if not s['broken'][st] and 0 <= midi - OPEN[st] <= 15][0]
        pg.click("#navR" if anyf >= s['pos'] + s['win'] else "#navL"); time.sleep(0.35)
    st, f = found; g = s['g']
    r = pg.evaluate("(()=>{const r=document.getElementById('neck').getBoundingClientRect();return {x:r.left,y:r.top,w:r.width,h:r.height}})()")
    cc = f - s['pos']
    x = r['x'] + ((g['bounds'][cc] + g['bounds'][cc + 1]) / 2) / g['cw'] * r['w']
    y = r['y'] + g['sy'][st] / g['ch'] * r['h']
    pg.mouse.click(x, y)


with sync_playwright() as p:
    b = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    errs = []

    # A run: title, choose a player, soundcheck, the night's caller, the duel
    pg = b.new_page(viewport=VIEW)
    pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
    pg.goto(URL); time.sleep(3.0)
    shot(pg, 'title')
    pg.click("#btnStart"); time.sleep(0.8)
    shot(pg, 'chars')
    pg.click("#btnCharGo"); time.sleep(0.8)
    for i in (0, 2, 4):
        pg.query_selector_all("#offer .ptile")[i].click(); time.sleep(0.15)
    time.sleep(0.6)
    shot(pg, 'soundcheck')
    pg.evaluate("document.getElementById('btnReady').click()"); time.sleep(0.6)
    if pg.is_visible("#mOk"):
        shot(pg, 'howto')
        pg.click("#mOk")
    wait(pg, "!!document.getElementById('vcGo') && document.getElementById('vcGo').offsetParent!==null")
    time.sleep(1.0)
    shot(pg, 'venue')
    pg.click("#vcGo")
    wait(pg, "window.__fb.state.phase=='answer'")
    time.sleep(0.8)
    notes = pg.evaluate("window.__fb.state.call.notes")
    for n in notes[:-1]:                         # play all but the last note, so the duel is mid-answer
        tap_note(pg, n['midi']); time.sleep(0.25)
    time.sleep(0.3)
    shot(pg, 'duel')
    pg.close()

    # Backstage and the Van, from a fresh title screen
    for btn, name in (("#btnBackstage", 'backstage'), ("#btnVan", 'van')):
        pg = b.new_page(viewport=VIEW)
        pg.on("pageerror", lambda e: errs.append(str(e)[:300]))
        pg.goto(URL); time.sleep(2.0)
        pg.click(btn); time.sleep(2.0)
        shot(pg, name)
        pg.close()
    b.close()
print('errors:', errs)
