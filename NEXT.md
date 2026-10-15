# Fretbound: open items for the next session

Updated 2026-10-02 after v1.55 (painted pose sets for 34 of 35 characters: painted pose sets for the Bard and the Tiger) (developer menu: five taps on the version text). v1.43 is merged to main; v1.44 to v1.55 (stage lights, painted roadside objects with doubled variety, castle, guitars, arms, power lines) are on branch `claude/serene-curie-omhjrg` with a pull request open.
Read this first, then the START HERE section of `HANDOFF.md`.

## 0. Next build (Josh, 2026-10-15): mumble speech for the characters
Josh wants characters to "talk" in a mumble voice when their lines appear, like Animal Crossing's Animalese or the UnitOfTime video "I Gave My NPCs Voices Without Recording Anything" (YouTube; its thumbnail shows a pitch contour drawn over the line "Ah greetings young one!"). No recordings: every syllable is synthesised.
Where it hooks in: `say(who,text,ms,noType)` types the dialog strip two characters every 22 ms (`typeTimer`). Speak one blip per syllable-ish chunk as the text appears, so voice and typing stay in sync; stop it in `hideDialog` and whenever `say` is called again.
A sketch to start from (all in the Web Audio graph the game already has, through the music or SFX bus so the volume sliders apply):
- **One voice per speaker.** A table keyed by caller id, band member and player: base pitch, waveform or formant pair, speed, and a wobble. Examples: the Twang Knight a nasal square with a drawl (slow, low), the Reverb Siren a sine with a long echo send, Mister Midnight low and breathy (filtered noise plus a soft triangle), the Penguin short high chirps, the Brass Tacks a muted-trumpet buzz. Fall back to a voice built from the character's id so nobody is silent.
- **Syllables from the text.** Split on vowel groups; each syllable is a 50 to 90 ms blip with a quick attack and release. Pick its pitch from the letters (a hash of the vowel, so the same word always sounds the same), plus a contour over the line: a gentle fall at a full stop, a rise on "?", a jump on "!", a pause at commas.
- **Two formants instead of a plain beep** read as speech: a source (saw or pulse) through two band-pass filters whose frequencies follow the vowel (a, e, i, o, u each have a pair). That is the cheap trick behind Animalese-style voices.
- **Stay in key.** Snap syllable pitches to the night's key, or to E minor on the title (`snapEm`), so the voices sit inside the music. Keep them short and under the band; duck the band a little (there is `cueDuck` for cues) only while a line is spoken.
- **Settings and accessibility.** A "Voices" slider (or on/off) in settings; respect reduced motion for the typewriter as today. Do not voice the rule text or the long liner notes, only spoken lines (`say` callers, road encounters, recruits).
- **Test** with an offline render like `cueTest` (an OfflineAudioContext): check the loudness is about the same for every voice and that a line of 60 characters lasts about as long as it takes to type.


**`PLAYTEST.md`** has notes from five bot playthroughs of v1.79 with a suggested order. Done so far: band depth and layout (v1.80), reward banners and confetti (v1.81). Next on that list after the mumble voices: a late-game money sink, a real Tour Complete screen, a brighter neck while answering plus colour-blind-safe pocket/groove marks, even music levels, then onboarding. Re-run the bots after gameplay changes: `OUT=/tmp/run python3 tests/dev/botrun.py pro bard greedy` (profiles pro, casual, novice; greedy or thrifty).

**Test page:** the game is over 16 MB, so build the artifact with `python3 tests/dev/artifact_split.py OUTDIR` and publish `OUTDIR/index.html` with its two `art_*.js` side files.

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
4. **Depth scaling for the band.** Done in v1.80 (pre-shrunk pose atlases keep it crisp). Does it read right on the phone?
5. **The Monk critical error** (strings, pedals and player vanished) was never reproduced. Ask for the device, browser, which night, and whether it was a resumed save. Resolved for now (2026-10-03): Josh never reproduced it; safeguards stay in place.
6. **A real signing key** so builds update over each other (section 1).

## 2b. Sound still to do (audit 2026-10-05, v1.77)
- Done in v1.78: every screen has its own music now.
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
