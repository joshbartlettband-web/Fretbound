# Twelve new pedals (built in v1.56)

Prices are in dollars, the same scale as the rest of the shop. Rarity weights are unchanged (common 50, uncommon 32, rare 14, legendary 4).
Gain figures are from `python3 tests/pedalsim.py`: the average score added on top of an Iron Comp, perfect answers, random calls.

| Pedal | Rarity | $ | Effect | Fires | Gain |
|---|---|---|---|---|---|
| Harpy Shriek | common | 3 | +24 Tone. -1 Hype unless a note is at fret 8 or higher. | always | 16% |
| Fairy Ring | common | 3 | +1 Hype for each note on the same string as the note before. | 45% | 15% |
| Pixie Chorus | common | 3 | +9 Tone each time you hop to a different string. | always | 12% |
| Centaur Gallop | common | 3 | +1 Hype for each note past the second. | 48% | 17% |
| Hydra Splitter | uncommon | 4 | +6 Tone for each pedal on your board, this one too. | always | 13% with two pedals, 30% with five |
| Mermaid Reverb | uncommon | 5 | +3 Hype if you replayed the call. | when you replay | 23% on a replayed call |
| Leprechaun Comp | uncommon | 5 | +2 Tone for each dollar you hold, up to +30. | always | 22% at $10 |
| Wizard Whammy | uncommon | 5 | +3 Hype for each leap of a 4th or more between notes. | 39% | about 14% |
| Phoenix Echo | rare | 7 | +1 Hype. x1.5 Hype too on the call after a miss. | always | about 20%, more after a miss |
| Gnome Gain | rare | 7 | x1.5 Tone if the call has 3 notes or fewer. | 72% | 22% |
| Kraken Crush | legendary | 10 | x1.25 Hype. x2 instead if no two notes share a string. | always | 47% |
| Gremlin Glitch | legendary | 10 | A random other pedal of yours fires a second time. | always | depends on the board |

Notes on the pairings:
- Fairy Ring and Pixie Chorus pull opposite ways (same string against hopping).
- Mermaid Reverb and Grave Gate pull opposite ways (replay or don't).
- Leprechaun Comp wants you to save money, which fights the shop.
- Hydra Splitter gets better the more you buy. Gremlin Glitch does too.
- Gnome Gain is the opposite of Basilisk Dist (3 notes or fewer against 4 or more).
- Pedals the first draft used that clashed with an existing one were changed: Goblin Fuzz (we have Goblin Screamer), Troll Toll (Troll Boost), Dragon Hoard and Dragon's Breath (Dragon Stack), Barrel Roll (Moon Octaver already triples the first note).
