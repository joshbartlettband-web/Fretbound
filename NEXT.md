# Fretbound: open items for the next session

Updated 2026-10-02 after v1.45. v1.43 is merged to main; v1.44 and v1.45 (stage lights, painted roadside objects for all continents, castle and Luthier fixes) are on branch `claude/serene-curie-omhjrg` with a pull request open.
Read this first, then the START HERE section of `HANDOFF.md`.

## 1. The APK
- v1.43, v1.44 and v1.45 APKs were built in cloud sessions with a throwaway key (`FRETBOUND_KEYSTORE_B64` in the environment settings was a 24-character placeholder, not a keystore). Josh's phone has the throwaway-key build; later builds from the same container install over it, a fresh container makes a new key and needs one uninstall.
- To make builds update over each other for good: set `FRETBOUND_KEYSTORE_B64=<output of base64 -w0 fretbound.keystore>` (and `FRETBOUND_KEYSTORE_PASS` only if it is not "fretbound") in the environment settings, then `bash setup.sh` and `bash android/build.sh`. The phone gets one uninstall when it moves to the real key.
- Security note: the old keystore is still in the git history (file `fretbound-keystore-base64.txt`, removed in commit e1dce1f). If the repo is ever shared, clean the history or make a new key. Do not try to read the key out of git history yourself; the session safety check blocks it.
- The phone may save a downloaded APK as `.zip`; rename it to `.apk` instead of extracting.

## 2. Questions Josh has not answered yet
(Answered 2026-10-02: crowd height is fine, colours are fine, stage lights on the Spur look terrific, North America's painted title works. Done in v1.45: painted roadside sets for all seven continents with the animations kept (windmill wheel, mill sails, giraffe, flag, kangaroo, llama), the Europe plate's windmill removed, the castle's jitter fixed, the Luthier's guitar reshaped. To check on the phone: the castle approach in portrait, the Luthier's twelve-string, and whether any painted object looks too big or too small next to its neighbours (sizes are the numbers in `tests/procroadside.py`, then re-run it and `grade.py` is not needed for these). Still code-drawn on the title: rocks, scrub, tufts, fences, walls, bales, mile and km posts, the pumpjack and a few small kinds.)
2. **Clouds over the painted title skies.** The code-drawn grey clouds drift over every painted sky and look heavy on the bright ones (Africa). Drop them on painted skies, or lighten them?
5. **How it runs on his phone**: smoothness of a full-band duel, the title screen, the Hollow Pine lights-out, the castle approach on the Europe title.
6. **Shallow stages with a full band** (the mess hall, the Ghat) are crowded, and the keyboard player tends to stand right behind the caller. Fine, or should the band thin out or shift on those stages?
7. **Depth scaling for the band.** Musicians further back could be drawn a little smaller on deep stages. Held off because scaling pixel art blurs it; the band is now a fixed size smaller than the fighters instead.
8. From an earlier session, still open: Josh reported a critical error with the Monk (strings, pedals and player vanished). It was never reproduced. Ask for the device, browser, which night, and whether it was a resumed save.

## 3. Known problems not yet fixed
- Stage lights (v1.44) are generic (`stageLights`): check on the phone that the pools and cones read as light and not as a stain. Amounts are the numbers in `stageLights`. The older code-stage fallbacks still aim cones at x 156 and 472 (only used if a plate fails to load).
- **Some frame spikes remain**: about 10 frames over 33 ms per 400 at 4x CPU throttle, the worst about 50 to 60 ms (was 17 and 76). Ideas: warm more poses in the background, or build the first pose of each character before the night starts. Check on the real phone first.
- **Painted callers and players never blink or change expression.** The rough arms noted in HANDOFF are also still there: the owl's pale arm blocks, Sebene's pink sleeves over the tail, Azmari's pale arms on the white robe, and the penguin's and Pole's dark arm bars.
- **The band has only two painted poses** per member; cut-out motion carries the rest. Tam's strum pose has a faint blur.

## 4. Not painted yet (still code-drawn)
- Title roadside objects (see question 1). A painted ground beside the road was tried and backed out (it hides in the haze; see HANDOFF).
- The crowd silhouettes, the seated band and player on the Van screen, the merch room, the backstage doors, the Green Room, and the panel frames.

## 5. Housekeeping
- v1.44 is on `claude/serene-curie-omhjrg`, not merged to `main`. Ask Josh whether to open a PR.
- `tests/gplay.py` was fixed (the neck could run off short screens). The older tests write PNGs into the repo root; they are in `.gitignore`.
- After re-processing any Gemini art, run `python3 tests/grade.py`, and check that a second run leaves `index.html` byte-identical.
