# Playtest notes, v1.79 (2026-10-11)

Five full runs played by a bot through the real UI. Each bot had a skill level (pro, casual, novice: note accuracy, timing spread, how often it named the first note) and a shopping habit (greedy: buy the dearest pedal it can afford; thrifty: buy cheap pedals and keep $5 for interest). Runs: pro Bard (greedy), casual Monk (thrifty), casual Smith (thrifty, landscape), casual Wizard (greedy), novice Busker (greedy). The tool is `tests/dev/botrun.py`. I also looked at all 21 stages with full bands, all 7 title scenes in both orientations, every menu, and the duel screen through a few lenses (blur, colour blindness, motion, tap targets, reading load, music loudness).

## Runs at a glance
| Bot | How far | Ended | Money at the end |
|---|---|---|---|
| Pro Bard | Whole world, 14 nights | Won the Pole | $201 |
| Casual Monk | 13 nights | Lost at the Aurora Dome (5 wrong notes) | $112 |
| Casual Smith | 6 nights | Lost at Sugarloaf, leg 3 night 1 | $71 |
| Novice Busker | 4 nights | Lost at the Milonga (7th chords) | $80 |
| Casual Wizard | 2 nights | Lost at Hollow Pine | $9 |

No crashes or page errors in any run. The only errors logged were the bot's own click timeouts.

## What plays well
- The core loop is fast and readable: a night is 30 to 80 seconds, and 85% of a run is spent in the duel.
- Difficulty rises sensibly through the legs, and the new chord families (7ths in South America, the diminished calls) are real walls for weaker ears. The losses happened where the musical content got harder, not by chance.
- Frame times are better than in v1.43: 5 slow frames per 400 at 4x CPU throttle (was 10), the worst 46 ms (was 50 to 60).
- The painted stages with full bands read as real gigs. At game size I found no character floating or standing inside furniture.

## Perspective (Josh asked)
- **The band is not depth-scaled.** Musicians at the back of the stage are drawn at the same size as the fighters at the front, so on deep floors (Dunes, Sebene, Azmari, Paris) the back row looks slightly too big. That's the open "depth scaling" question in NEXT.md; with everyone in place it now shows more. The fix would be about 8 to 10% smaller per 20 px of depth, with ladder steps to keep the pixels crisp.
- **The caller's side is crowded in a mirror-image cluster.** Keys, drums and guitar stack behind the caller in the right third, and the keyboard often cuts across the caller's guitar (Spur, Hollow Pine, Mess Hall). Real bands spread toward the middle. The caller's band could use the centre-back more, since the middle-of-stage penalty keeps it empty.
- **The Spur has no prop footprints** (`STAGE3D.spur.props` is empty). Nobody currently stands behind the jukebox, but nothing would prevent it.
- **Road encounter scenes:** the two characters are scaled sensibly against the backdrop. The backdrop is the continent's Van-scene plate, though, so stories set somewhere specific show a different place: the karaoke box in Tokyo is a temple courtyard, the pawn shop and the truck-stop jukebox are the same motel. Not a perspective error, but it reads like one.
- **Title screen:** no errors found. The roadside objects sit on the ground plane and grow correctly, and the castle is steady.

## Things that look broken
1. **Reward banners collide with other UI.** The HEADLINER DOWN banner overlaps the results tabs on the Tour Complete screen, and in landscape it's clipped at the stage panel ("EADLINER DOW"). The passport stamp lands on top of the "Book your next leg" text. A clipped banner fragment ("CT" / "ry call t") showed over the call caption in portrait.
2. **Confetti follows you to the next screen.** A perfect night's confetti keeps falling over the road encounter that comes after it (seen at the karaoke box and the station radio).
3. **Finishing the whole world is an anticlimax.** The Tour Complete screen is the same layout as a loss, led by "Your weakest calls from this leg", with a headliner banner on top. The biggest moment in the game deserves its own screen: the passport full of stamps, the world map lit, the band.

## Design notes (taste)
- **Money stops meaning anything.** Once the board is full (5 pedals, usually by night 3), cash piles up: $201 at the end of a world tour, $70 to $110 in the runs that lost. Interest caps at $3, and nothing else costs more than $10. A late-game money sink would make wins feel like progress: a sixth board slot, a better board, paying a band member to stay, buying a replay, or swapping pedals at the pawn shop for more than $3.
- **Single calls end nights.** Several nights were cleared in one or two calls (Duende's Cave in one, Tide Pool in two) because Tone x Hype snowballs. That's fun once; when it's common the setlist stops mattering. Consider a minimum number of calls before CASH OUT, or a target that grows with the call count.
- **Losses come from one bad call.** Every losing night was one or two calls with several wrong notes. That's fair, but there's no comeback mechanic. Replays exist, but the bots used none before losing. Maybe show "use a replay?" after a botched call, or make the first miss of a night cheaper.
- **The first minute is heavy on reading:** 452 words before the first note. That's title 27, character select 68, pedal pick 84, how to play 216, venue card 57. You also pick three pedals before you know what a pedal does. Suggestion: start the first run with a fixed starter board, and teach the rules over the first night one line at a time.
- **Squint test:** blur the duel screen and the brightest things are the sunset, the green and red Tone and Hype boxes, and the pedals. The fretboard, where you actually play, is the dimmest part. During the answer phase the neck should be the brightest thing on screen (a warmer wood, a lit edge, or dimming the stage).
- **Colour blindness (deuteranopia):** Tone (green) and Hype (red) stay readable by position. Pocket (orange) and groove (yellow) marks merge, and several pedals become the same olive. Add a shape or letter to the groove marks (the P/G letters exist in the review row; use them on the neck pops too).
- **Tap targets:** the pause button is 26x30 px and REPLAY is 33 px tall. Both are under the comfortable 44 px for a thumb.
- **Music levels:** the title song is about -22 dB, the menu and road cues -33 to -42 dB, 11 to 20 dB quieter. Going from the title to the Van or Backstage, the music almost vanishes. The quiz cues (radio, station, karaoke, trivia) are the quietest at -41 dB. Even them out to within about 4 dB.
- **The stage is small on a phone:** fighters are about 60 CSS px tall in portrait and 56 in landscape. Most of the painted detail is lost at that size. Worth trying: zoom the stage toward the two fighters while a call plays, and pull back for the band and crowd moments.

## Suggested order
1. Reward banner placement and confetti carry-over (small, visible bugs).
2. A late-game money sink.
3. A real Tour Complete screen.
4. Neck brightness during the answer phase, and pocket/groove marks for colour blindness.
5. Music levels.
6. Depth scaling and spreading out the caller's band.
7. The first-minute onboarding.
