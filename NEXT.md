# Fretbound: open items for the next session

Updated 2026-10-02 after v1.55 (painted pose sets for 34 of 35 characters: painted pose sets for the Bard and the Tiger) (developer menu: five taps on the version text). v1.43 is merged to main; v1.44 to v1.55 (stage lights, painted roadside objects with doubled variety, castle, guitars, arms, power lines) are on branch `claude/serene-curie-omhjrg` with a pull request open.
Read this first, then the START HERE section of `HANDOFF.md`.

## 0. Mumble voices (v1.83, 2026-10-15)
Done: callers mumble their lines, and road-scene quotes are spoken (see HANDOFF v1.83). Still open:
- **Josh to listen on the phone.** Are any voices too loud, too long or too silly? Each voice is one line in `VOICE` (pitch `b`, speed `st`, size `fs`, breath `br`, echo `ech`, glide `gl`, wobble `wob`). After changing a voice, re-level it with `__fb.voiceTest`.
- Lines run about 2 to 2.5 s for 70 characters, longer than the typing (0.8 s). Josh may want them shorter or the typing slower.
- v1.84: the players and band talk too (character select, night start and end, perfect-call cheers, member and recruit cards, road reactions). Josh to check: are the lines in character, and is the 1.9 s player answer at the start of each night too slow?
- Not voiced yet: the road quizzes. Only 7 road lines are in quotes; more quoted speech in road stories would give the voices more to do. A band member could comment on a bad call too (only perfect calls get a cheer).
- Ideas: a little consonant click at the start of syllables (plosives), a "hm?" for question-only lines, ducking the band slightly while a caller talks.

## 00. The world and the events (Josh, 2026-10-16)
- **World:** `WORLD.md` is the draft world bible (casual, lazy magic in the modern world; players are a storybook guild of travelling musicians; callers are the spirits of a music's place; real people only in liner notes). Josh wants to spend time enriching it; its open questions are a good place to start.
- **Events as conversations (v1.91):** road events can carry `talk` lines spoken by the people in the scene (see HANDOFF v1.91). All 27 events are conversations (v1.92). Next: write more events; Josh wants an idea-jam session for them. The developer menu's EVENTS browser is the way to review them.
- **Event backgrounds:** every event still shows its continent's Van-scene plate, so the karaoke box looks like a temple and the pawn shop like a motel. Painted backdrops per event are high on Josh's list and are the natural place for the fantastic details (a haunted ice machine, Gerald's bulletin board). Estimate: one Pro image each at about $0.134, so all 27 events are about $4 plus retries; they use the same 480x200 plate format as the Van scenes. Gerald himself also needs art (a portrait and a few road poses).
- **Players to bring in line with the world:** the Journeyman and the Busker (see WORLD.md).
- **In-between frames:** `tests/tween.py` works for small moves (pilot GIFs of the Bard's strum). Next step: wire tweens into the atlases and `drawPose` for strums.

## Pinned: Brain Jam (a separate app idea, 2026-10-16)
An app for teasing out ideas by talking with an AI partner: a simple animated avatar (fun, simple graphics), powered by a large enough model to feel natural, that asks questions about an idea, leads where it helps, and writes up documentation of the ideas as you go. Josh: "I suppose I'm just describing the live chat feature of any of the LLMs, but with fun, simple graphics." Not started; pinned for later.

## 0a. Guitars
Done (v1.87, v1.88): 9 characters have their own guitar shapes on stage and in their portraits. The Bard and the Dune Looper keep Strats by choice. Gemini spend for the whole job: about $8.50 (`art/gemini_test/spend.log`).

## 0b. More distinct guitars (estimate for Josh, 2026-10-15)
12 of 31 guitar players use the single-coil (Strat-style) guitar: the Bard, the Wizard and the Journeyman, and 9 callers (Twang Knight, Reverb Siren, Dune Looper, Sebene Peacock, Neon Condor, Kitsune, Emperor, Aurora, Silence). A character's guitar lives in its 16-pose set (two sheets) and its portrait, so changing it means new sheets. Cost per character on `gemini-3-pro-image` at 2K ($0.134 an image): about 6 sheet images (2 sheets x 3 candidates) plus 2 to 3 portrait edits, so about $1.10 to $1.25. For all 12: about $15, call it $20 with retries; about 100 requests, well under the 250 a day limit. Time: one session (generation, `repick.py`, `procposes.py --embed`, grade, checks). Keeping these looks only (same sound and stats) avoids any gameplay work; new guitar TYPES with their own sound and stats would add menu icons (2 images each) and balancing.
Update (v1.86): the cheap route works. The Wizard was redone by editing his existing atlas with Flash (see HANDOFF v1.86), about $0.35 a character, so all 12 would be about $4 to $6. Flash changes colours and finishes well but not shapes (no headless guitar), so pick looks that differ by colour and finish, or use Pro for a shape change on the one or two that need it. Done: Wizard (natural blond). The Journeyman already had a butterscotch Telecaster on stage.
Suggested looks: Bard keeps the mint Strat; Journeyman a butterscotch Telecaster (matches his liner notes); Wizard a headless or extended-range guitar; Twang Knight a Telecaster with a B-bender; Reverb Siren a surf-green Jaguar; Sebene Peacock a sunburst archtop; Neon Condor a 60s teardrop guitar in neon paint; Kitsune a Mosrite (the Ventures in Japan); the Emperor a white Gretsch Falcon (tuxedo colours); the Aurora a clear acrylic guitar; the Silence a plain white SG; the Dune Looper keeps a weathered Strat.

 has notes from five bot playthroughs of v1.79 with a suggested order. Done so far: band depth and layout (v1.80), reward banners and confetti (v1.81). Next on that list after the mumble voices: a late-game money sink, a real Tour Complete screen, a brighter neck while answering plus colour-blind-safe pocket/groove marks, even music levels, then onboarding. Re-run the bots after gameplay changes: `OUT=/tmp/run python3 tests/dev/botrun.py pro bard greedy` (profiles pro, casual, novice; greedy or thrifty).

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
