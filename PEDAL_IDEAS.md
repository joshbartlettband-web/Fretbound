# Twelve pedal ideas (not built yet)

Scale used: common about +10 Tone or +1 to +2 Hype with a condition; uncommon about +2 to +3 Hype or +5 to +8 Tone per trigger; rare about x1.5 or scaling; legendary x2 or run-scaling.

## Common
1. **Goblin Fuzz** (25): +12 Tone, but -1 Hype if the hand has no note above fret 7. A cheap crunchy pedal that wants low notes kept honest.
2. **Mushroom Ring** (25): +1 Hype for every note on the same string as the one before. Fairy rings grow in circles. Caps itself at +4 on a normal hand.
3. **Pixie Chorus** (30): +8 Tone for each pair of notes one fret apart. Tiny and shimmery, rewards chromatic runs.
4. **Barrel Roll** (30): First note of the hand counts twice. Dwarves rolling kegs down the stairs. About +15 Tone on an average opener.

## Uncommon
5. **Mermaid Reverb** (55): +3 Hype if the hand ends on the same note name it began with. Echoes that come back home.
6. **Dragon Hoard** (60): Gains +1 Tone permanently for every 10 gold you hold, up to +20. Rewards saving over shopping.
7. **Wizard's Whammy** (60): Once per night, the lowest-scoring note is replayed as the highest one. A little cheating from a pointy hat.
8. **Troll Toll** (55): +6 Tone per pedal you own, but costs 1 gold per night. A bridge troll taking his cut. Weak with one pedal, fair with four.

## Rare
9. **Phoenix Delay** (90): After a flop, the next hand scores x1.5 Hype. If you never flop, it does nothing. A comeback pedal, so it needs a bad night to pay.
10. **Gnome Gate** (95): Hand with three or fewer notes gets x1.5 Tone. Small hands, big result. The opposite of Thick.

## Legendary
11. **Dragon's Breath Overdrive** (160): x2 Hype on a HOT call, otherwise -2 Hype. High risk, high payoff. HOT calls already double base Tone, so this is a deliberate spike.
12. **Jester's Wild Card** (150): At the start of each hand, a random effect from your other pedals fires one extra time. Chaotic on purpose, scales with how many pedals you carry.

## Balance notes
- Goblin Fuzz and Pixie Chorus compete with Glassy and Thick on the cheap end.
- Dragon Hoard and Troll Toll pull opposite ways on gold. Pair them and the shop gets tense.
- Phoenix Delay and Dragon's Breath both need state: a flop flag and a HOT check. Everything else uses data already in `evaluate()`.
- Jester's Wild Card is the hardest to build and the easiest to break. Needs a cap on repeats and care with loop and rack boards.
