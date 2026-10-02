# Fretbound: open items for the next session

Written at the end of the 2026-10-02 art session (v1.43 on branch `claude/epic-ramanujan-r64nhk`, not merged to main, no PR).
Read this first, then the START HERE section of `HANDOFF.md`.

## 1. Build the v1.43 APK (Josh wants to test on his phone)
- Everything is committed: the game says v1.43, `android/AndroidManifest.xml` is versionCode 53 / versionName 1.43, and HANDOFF has the dated line.
- Run `bash setup.sh`, then `bash android/build.sh`, and send Josh the APK (`android/bin/fretbound.apk`).
- Signing: if `FRETBOUND_KEYSTORE_B64` is set in the environment, the APK installs over his old one and keeps his save. If it is not set, the build makes a temporary key, and Josh must uninstall the old app first, which loses his save. He was fine with that ("let's move past this").
- The environment variable box in the settings takes `.env` lines: `FRETBOUND_KEYSTORE_B64=<base64 of the keystore>` and, only if the password is not "fretbound", `FRETBOUND_KEYSTORE_PASS=<password>`. His first try had the two names on one line with no values.
- Security note for Josh: the old keystore is still in the git history (file `fretbound-keystore-base64.txt`, removed in commit e1dce1f). If the repo is ever shared, clean the history or make a new key (a new key means one uninstall).
- Do not try to read the key out of git history yourself; the session safety check blocks it.

## 2. Questions Josh has not answered yet
1. **Painted title roadside objects.** Pilot North America's set (saguaro, Joshua tree, billboard, windmill, shack) as painted silhouettes, drawn through `ladderAt` like the Europe castle so they do not shimmer as they grow? Recommended; waiting on a yes.
2. **Clouds over the painted title skies.** The code-drawn grey clouds drift over every painted sky and look heavy on the bright ones (Africa). Drop them on painted skies, or lighten them?
3. **Crowd row height** on the play screen. It is one number (`CROWD_DROP`). Does the crowd sit right relative to the fighters' feet?
4. **Colour grade strength.** It can be pushed harder or softer per art group (`tests/grade.py`, `P` and `PSOFT`). Josh said the grade looked better; portraits were softened after he called them crisp. Anything else too strong or too weak?
5. **How it runs on his phone**: smoothness of a full-band duel, the title screen, the Hollow Pine lights-out, the castle approach on the Europe title.
6. **Shallow stages with a full band** (the mess hall, the Ghat) are crowded, and the keyboard player tends to stand right behind the caller. Fine, or should the band thin out or shift on those stages?
7. **Depth scaling for the band.** Musicians further back could be drawn a little smaller on deep stages. Held off because scaling pixel art blurs it; the band is now a fixed size smaller than the fighters instead.
8. From an earlier session, still open: Josh reported a critical error with the Monk (strings, pedals and player vanished). It was never reproduced. Ask for the device, browser, which night, and whether it was a resumed save.

## 3. Known problems not yet fixed
- **Painted light cones and spots no longer line up with the fighters.** The fighters moved from x 156 / 472 to 210 / 430 (`HERO_X`, `RIVAL_X`), but the Spur's code light cones (`lightCone2(g,156,...)` and `472` in the painted-Spur detail) and any painted spotlight pools on the plates still aim at the old spots. Re-aim the code cones; check each plate for painted pools.
- **Some frame spikes remain**: about 10 frames over 33 ms per 400 at 4x CPU throttle, the worst about 50 to 60 ms (was 17 and 76). Ideas: warm more poses in the background, or build the first pose of each character before the night starts. Check on the real phone first.
- **Painted callers and players never blink or change expression.** The rough arms noted in HANDOFF are also still there: the owl's pale arm blocks, Sebene's pink sleeves over the tail, Azmari's pale arms on the white robe, and the penguin's and Pole's dark arm bars.
- **The band has only two painted poses** per member; cut-out motion carries the rest. Tam's strum pose has a faint blur.

## 4. Not painted yet (still code-drawn)
- Title roadside objects (see question 1). A painted ground beside the road was tried and backed out (it hides in the haze; see HANDOFF).
- The crowd silhouettes, the seated band and player on the Van screen, the merch room, the backstage doors, the Green Room, and the panel frames.

## 5. Housekeeping
- The branch is far ahead of `main` and has no PR. Ask Josh whether to open one.
- `tests/gplay.py` was fixed (the neck could run off short screens). The older tests write PNGs into the repo root; they are in `.gitignore`.
- After re-processing any Gemini art, run `python3 tests/grade.py`, and check that a second run leaves `index.html` byte-identical.
