# Ideas: road encounters and learning note names (2026-10-04). Encounters built in v1.68, always one per leg (no choice); note names next. Josh: missing a note name may cost Tone or Hype.

## Road encounters
**How it works.** After night 1 of each leg, the road card gives a choice: take the highway (straight to the next show), or take the back road (one encounter). Each continent has a pool of 5 to 10 encounters. A run draws one per leg, never repeating within a run.

**What an encounter is.** Like the ? rooms in Slay the Spire: one painted scene, a short story in two or three lines, and two or three choices. Some choices cost money, a string or a replay. Some carry risk. Some only appear with a certain player, band member or pedal.

**Art.** Most scenes reuse what we have: the title plates, Van scene plates, stage plates and roadside objects as backgrounds, and the hang poses, caller poses and crowd sprites as the people. New Gemini art only where a scene needs something special, about one picture per continent.

### Anywhere (shared pool)
1. **Flat tire.** Pay $4. Or everyone pushes: -1 replay next night. Free with the Luthier or the Guitar Tech.
2. **Busking corner.** Play a short request for tips. The more of it you play right, the more you earn.
3. **Old friend.** A caller you have beaten is on the same road (their hang pose). Jam with them for one of their pedals, or ask for advice: their rule is softened for the next show.
4. **Pawn shop.** Trade one pedal for a random one of the next rarity up, or sell it for its full price.
5. **Rainy motel.** Rest: free restring and +1 spare. Or practise all night: the next show's first call is a HOT call, with double base Tone.
6. **Radio station.** An on-air ear quiz, three questions. Each right answer pays cash.
7. **Superfan.** They give you a pedal, but you must play their favourite call next show (it is forced HOT).
8. **Merch mix-up.** A box of the wrong T-shirts. Sell them cheap for $3 now, or carry them for $1 a night for the rest of the leg.

### North America
- **Truck stop jukebox.** Feed it $2 and pick one of three common pedals.
- **Session gig.** Play rhythm on a country record, three quick calls, for pay.
- **Mister Midnight's moonlit bet.** Double or nothing on the next night's door money.

### Africa
- **Tea in the desert camp.** Three glasses of tea, a Sahel and Tuareg custom: the first strong, the second sweet, the third gentle. Each glass you stay for gives a small reward and costs time (the next night's tempo goes up).
- **The Kinshasa tailor.** Pay for a sharp suit: +1 Hype on every call next show, in the spirit of La Sape.
- **Coffee ceremony.** Ethiopia's three rounds, abol, tona and baraka. Each round restores something: a string, a replay, then a blessing.

### South America
- **Samba school rehearsal.** March with the batería: the next show is faster, but every groove hit counts double.
- **Tango practica.** Practise with the dancers. A pedal of your choice is moved to slot 1 for free, and Precise calls pay +$1.
- **Mercado in Lima.** Haggle for a used pedal. The price drops each time you ask, but the stall might close.

### Europe
- **Busking in the Métro.** Two-beat pompe practice for tips.
- **The late-night peña.** Join the flamenco session: a Phrygian call is guaranteed HOT next show.
- **Fjord ferry.** Rough crossing: lose a replay, or pay for a cabin.

### Asia
- **Karaoke box.** Sing it back. This is the note-names mini-game (see below).
- **Shinkansen.** The fast train: skip the shop, but get double door money.
- **Chai stall at the ghat steps.** Sit and listen to the drone: your next call starts on its root, shown.
- **Village gamelan rehearsal.** Learn to interlock: +1 Hype per note on alternating strings next show.

### Oceania
- **Bonfire on the beach.** Slack key singalong: retune to open G for one night, for a bonus.
- **Pub trivia night.** Music questions for a pedal.
- **The flat party.** A Dunedin garage gig: play loud for Fame.

### Antarctica
- **Supply flight delay.** Wait it out: the next show has no shop.
- **Station radio.** Play for people at stations across the continent: a pure ear test, with no replays.

## Learning the note names (built into what we have)
1. **Name the first note (optional).** After a true call, three name buttons appear for a second or two. Tap the first note's name for +1 Hype. Ignore them and nothing is lost. Your ears and the names get practised together, every call.
2. **Fading names instead of a penalty.** Right now, note names on the neck cost x0.5 Tone. Instead, each cell's name fades out as the Ear Report sees you finding that cell reliably. A name stays only where you still need it, and only those cells cost Tone.
3. **Tonight's note.** Each night picks a note name, shown on the HUD (for example, "Tonight: F#"). Every F# you play scores bonus Tone, so you hunt for it all over the neck.
4. **Echo of every octave.** After a correct note, the same note glows faintly everywhere else on the neck for half a second. You learn the octave shapes without trying. Toggle in Settings.
5. **Glow, then name, then nothing.** Rules like Fading Glow could replace the glowing first note with its name ("starts on D") before taking it away entirely. That gives a three-step ladder from seeing, to reading, to hearing.
6. **Note hunt in the Green Room.** A new practice preset: the Tech says a note name and you tap every place it lives, against the clock. It logs to the Ear Map, which gains a "by note name" view of your slowest names.
7. **Name pedals.** For example, an Owl Scribe pedal: +3 Hype if you name the first note (ties into idea 1). Or a Rosetta pedal: +5 Tone for each note whose name matches tonight's note.
8. **Review in words.** The review already shows names. Add the step between them, for example "F to G#: a minor 3rd". The notes, the names and the intervals all appear together.
9. **Encounters that teach.** The karaoke box, radio station and busking corner can be short name drills, such as "play an A on every string".

## Idea jam, round one (2026-11-25, v2.03)
A starting list for the jam with Josh. Each idea follows WORLD.md: the magic is small, worn and a bit useless, and it never fixes the problem. "Art" says what the scene would need: an existing painted plate, or new Gemini pictures (about $0.13 a scene and $0.13 a local on Pro, going by `spend.log`).

**Built in v2.03** (they use the three practice scenes from v1.93, so no new art):
- **The reunion special** (TV set). Gerald's show is taping a reunion and the house band quit. Play the counting song for $4, or the theme from the feelings season (nobody remembers it but Gerald) for +2 Tone a note.
- **Wash day** (laundromat). The only free dryer is haunted by a nice ghost who dries a load in four minutes if you play it a song. Play it a slow one (+1 Hype), buy strings from the vending machine ($2), or wait for a normal dryer (+1 replay).
- **The guild hall.** Dues are $3 "since the group chat moved". Pay and get first pick of the lost and found (an uncommon pedal), or sign up for the guild photo (+1 Fame; you blink).

**Shared pool, ideas only**
1. **The weather report.** The local news covers your van as the evening weather: "light honking, chance of a show". Go on air for Fame, or hide behind the van for nothing. Art: a news van and anchor (new local), any parking-lot plate.
2. **The haunted ice machine.** The motel ice machine makes ghost-shaped cubes and is lonely. Keep it company (one fewer replay, it is a long night) and it gives you a cold pedal; or just take the ice. Art: motel plate exists; the machine could be code-drawn.
3. **The van has a grudge.** The van refuses to stop at one particular gas station chain. Push on to the next one (-$2 for the dearer gas) or make it stop (it sulks: the next night's tempo is 4 BPM slower). Art: none new, the van only honks.
4. **A wizard in a homemade robe** asks for directions to a gig across town. Give him a ride (he pays in a used pedal that only works on Tuesdays: random common) or point the way. Art: one new local.
5. **Open mic sign-up.** A coffee shop open mic with a list of 40 names. Wait it out for a small Fame bump, or leave. A choice with no cost, just time, to make the road feel lived in.
6. **The band member's cousin.** Whoever is in your van seat has a cousin in town who feeds everyone. Restring for free, and a line from that member. Art: none (uses the seated member).
7. **Lost pick.** A pick on the pavement glows faintly. Keep it (+1 Hype on the first call of each night this leg) or hand it in at the guild hall (the hall gives a cash reward). A small item that sticks around.

**Per continent, ideas only**
- **North America: a drive-in movie** with a monster movie on. The monster in the film waves at you. Play the intermission for tips.
- **Africa: a tro-tro bus** with painted slogans and a driver who programs the radio. Ride along: a call tonight is guaranteed in a key you have practised.
- **South America: a football match on the radio** in every shop. If "your" team wins (a coin flip), the crowd tonight is huge (+door money); if not, they are kind but quiet.
- **Europe: a night train** with a sleeper car. Sleep (+1 replay) or play in the corridor for the night staff ($).
- **Asia: a convenience store at 3am** where the clerk knows every enka song. Name the step in a short quiz for snacks (a small heal: a spare string pack).
- **Oceania: a ute with a broken stereo.** Fix it with a pedal from your board (lose a pedal, gain Fame) or lend them a capo.
- **Antarctica: the penguin census.** Help count the penguins. The counting song comes back (Gerald callback), and you get +1 Hype a true call.

**Questions for Josh**
- Should some events have a small chance of a rare outcome, the way the old-friend event can give a pedal?
- Do you want a recurring storyline across a run (Gerald showing up twice, or the van's grudge paying off later)?
- Which of these would you most like painted first?
