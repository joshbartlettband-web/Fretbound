# Working on Fretbound

The game is a single file, `index.html` (about 2.2 MB, with art embedded as base64). `HANDOFF.md` documents every system; read the relevant section before changing anything.

## Setup
Run `bash setup.sh` once per machine.

## House rules
- No menu or screen ever scrolls, on any of these sizes: 360x740, 390x844, 412x860, 740x360, 844x390. After any UI change, copy `index.html` to `test.html` and run `python3 tests/audit.py`; it must report 0 issues at every size.
- After gameplay or engine changes, run the play-through: `python3 tests/gplay.py` (expect `errors: []`).
- Many tests load `file:///home/claude/...` paths from the original workspace. Point them at this repo's `index.html` (or a copy) before running.
- Make edits with exact string replacements that assert the match count; `index.html` is large and repeated snippets are common.
- Pixel art: vector first, snapped to pixels, dark brown outline, warm palette. Title backdrops are painted Gemini plates processed by `tests/procplate.py` and masked by `tests/procfg.py`.
- Writing in the game and in replies to Josh: plain, human, few em dashes.
- The title song is in E minor. Fixed-pitch sounds are snapped to E minor while it plays (`snapEm`); keep new parts in key.

## Releasing a version
1. Bump the `Prototype vX.YY` text in `index.html`, and `versionCode`/`versionName` in `android/AndroidManifest.xml`.
2. Add a dated line for the version to `HANDOFF.md`.
3. Build the APK with `bash android/build.sh` (needs `FRETBOUND_KEYSTORE_B64` set, or the app will not update over older installs).
4. Commit with a short message naming the version.

## Tools you will need
- `bash setup.sh` once, then `bash tests/dev/pwfix.sh` (Chromium link for Playwright). Tests use repo-relative paths now.
- Art pipeline and how to test it: read the START HERE section of `HANDOFF.md` first. Gemini ignores removal instructions; erase parts yourself.
- Visual helper scripts live in `tests/dev/` (set `OUT` for their output folder). After any change run `tests/audit.py`, `tests/gplay.py` and `tests/dev/stress.py`.
