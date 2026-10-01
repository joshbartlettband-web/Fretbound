# Fretbound

A roguelike ear-training game for guitarists. A rival plays a phrase; you answer on a touch fretboard. The whole game is one self-contained web page, `index.html`, which also ships as an Android app and on itch.io.

- `index.html`: the game (open it in a browser to play).
- `HANDOFF.md`: how every system works, version by version. Read this first.
- `tests/`: Playwright checks and the art processing scripts.
- `art/`: processed portraits, title plates, masks, castle sprite, world map.
- `android/`: a minimal WebView wrapper and `build.sh`.
- `docs/art-checklist.html`: the Gemini prompt checklist.
- `setup.sh`: installs everything the tests and build need.
