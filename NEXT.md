# Fretbound: open items for the next session

Updated 2026-10-02 after v1.55 (painted pose sets for 34 of 35 characters: painted pose sets for the Bard and the Tiger) (developer menu: five taps on the version text). v1.43 is merged to main; v1.44 to v1.55 (stage lights, painted roadside objects with doubled variety, castle, guitars, arms, power lines) are on branch `claude/serene-curie-omhjrg` with a pull request open.
Read this first, then the START HERE section of `HANDOFF.md`.

## 1. The APK
- v1.43 to v1.55 APKs were built in cloud sessions with a throwaway key (`FRETBOUND_KEYSTORE_B64` in the environment settings was a 24-character placeholder, not a keystore). Josh's phone has the throwaway-key build; later builds from the same container install over it, a fresh container makes a new key and needs one uninstall.
- To make builds update over each other for good: set `FRETBOUND_KEYSTORE_B64=<output of base64 -w0 fretbound.keystore>` (and `FRETBOUND_KEYSTORE_PASS` only if it is not "fretbound") in the environment settings, then `bash setup.sh` and `bash android/build.sh`. The phone gets one uninstall when it moves to the real key.
- Security note: the old keystore is still in the git history (file `fretbound-keystore-base64.txt`, removed in commit e1dce1f). If the repo is ever shared, clean the history or make a new key. Do not try to read the key out of git history yourself; the session safety check blocks it.
- The phone may save a downloaded APK as `.zip`; rename it to `.apk` instead of extracting.

## 2. Questions for Josh
0. **New players (v1.74, v1.75).** Are the Blacksmith, Wizard, Herald and Journeyman balanced? The Wizard and the Journeyman were each toned down once in testing. Read the Herald's liner notes. The Herald and the Journeyman show the stock humbucker and single-coil icons on their cards, not their own white and butterscotch guitars; worth painting?
1. **Clouds over the painted title skies.** The code-drawn grey clouds drift over every painted sky and look heavy on the bright ones (Africa). Drop them on painted skies, or lighten them?
2. **How it runs on his phone:** a full-band duel, the title screen, the Hollow Pine lights-out, the castle approach on the Europe title (portrait), the Luthier's and Hermit's guitars, whether the light pools read as light, and whether any painted roadside object looks too big or small (sizes are in `tests/procroadside.py`).
3. **Crowded stages** (mess hall, Ghat) now show at most four band members a side (v1.47). Does that read better?
4. **Depth scaling for the band.** Musicians further back could be drawn a little smaller on deep stages. Held off because scaling pixel art blurs it.
5. **The Monk critical error** (strings, pedals and player vanished) was never reproduced. Ask for the device, browser, which night, and whether it was a resumed save. Resolved for now (2026-10-03): Josh never reproduced it; safeguards stay in place.
6. **A real signing key** so builds update over each other (section 1).

## 2b. Sound still to do (audit 2026-10-05, v1.77)
- No music at all: the Van, Backstage, the Roster, the Ear Report, the Green Room setup, the Results screen after its jingle.
- The soundcheck and the shop share one generic 8-step menu loop (`JAM`/`LEAD` in `schedStep`).
- UI sounds are mostly one square-wave `blip`. Candidates: buying and selling, a passport stamp, a recruit joining, drag-and-drop on the board, the tour map.
- Encounter backdrops are the 480x200 Van-screen plate of each continent; painted scenes per encounter would be much sharper (about $0.134 each at 2K).

## 3. Known problems not yet fixed
- Stage lights (v1.44) are generic (`stageLights`): check on the phone that the pools and cones read as light and not as a stain. Amounts are the numbers in `stageLights`. The older code-stage fallbacks still aim cones at x 156 and 472 (only used if a plate fails to load).
- **Some frame spikes remain**: about 10 frames over 33 ms per 400 at 4x CPU throttle, the worst about 50 to 60 ms (was 17 and 76). Ideas: warm more poses in the background, or build the first pose of each character before the night starts. Check on the real phone first.
- **Painted callers and players never blink or change expression.** The hanging arms are gone (v1.46); a few fill seams may remain (owl, turtle, koala: check).
- **The band has only two painted poses** per member; cut-out motion carries the rest. Tam's strum pose was sharpened in v1.47.
- **Blinking (WIP, not released):** eye rectangles for 26 characters are in `tests/proceyes.py` (painting coordinates, `--check` draws them), stored as `eye`/`ec` in the sprite metadata, and `warpSprite` paints a skin-coloured lid when `blink` is set. Wired and tests pass, but a blink was not visibly confirmed at game size. If the sprites move to painted pose sheets (see below), a closed-eyes pose replaces this.

## 4. Not painted yet (still code-drawn)
- Title roadside: rocks, scrub, tufts, fences, walls, bales, mile and km posts, the pumpjack and a few small kinds. A painted ground beside the road was tried and backed out (see HANDOFF).
- Done in v1.61 to v1.63: the Van screen crowd, merch room, backstage wall and doors, Green Room and the Guitar Tech. Still code by choice: the panel frames (guitar strings), the backstage lamps, flyers and floor. Josh agreed (2026-10-03): the string frames stay.

## 5. Housekeeping
- PR [#3](https://github.com/joshbartlettband-web/Fretbound/pull/3) (v1.44 to v1.55) is open against `main`.
- `tests/gplay.py` was fixed (the neck could run off short screens). The older tests write PNGs into the repo root; they are in `.gitignore`.
- After re-processing any Gemini art, run `python3 tests/grade.py`, and check that a second run leaves `index.html` byte-identical.

## 6. Painted pose sets
- All 35 characters are painted (v1.54). Check on the phone: size consistency while posing, whether any character still lacks its instrument in a pose, jerkiness of the weakest sets (cave, lou, paris, brassb, brass, rosa), crispness of the 2K sets next to the 4K Bard and Tiger. The big_hit pose is still not wired to a trigger. Menus (character card, roster, venue card) still use the portraits.

## 7. Floating sprites
- Resolved (Josh, 2026-10-03): no longer seen after v1.53 to v1.62.
