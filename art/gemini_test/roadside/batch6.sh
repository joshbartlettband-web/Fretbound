g(){ bash gen_all.sh "$@" >/dev/null 2>&1 & }
gc(){ python3 ../gen_img.py "$1.jpg" "Pixel art game sprite in a warm 16-bit style with a dark brown outline, full colour with soft shading, lit from the right by a low warm sun. Single object, centered, entire object visible with margin around it, flat solid pure magenta (#FF00FF) background edge to edge: no sun, no sky, no stripes, no gradient, no border, no frame, no ground, no shadow, no text, no other objects. Subject: $2" "${3:-1:1}" >/dev/null 2>&1 & }
# Oceania
g emu "an emu standing seen from the side, long neck, shaggy feathers, long legs." 1:1
g kookaburra "a kookaburra bird perched on top of a wooden fence post, big head and beak." 1:1
g tinhut "a small Australian outback shack with a corrugated tin roof, a verandah and a water tank beside it, one lit window." 3:2
g banksia "a banksia tree with a gnarled trunk, serrated leaves and several cone-shaped flower spikes." 1:1
g ute "an old Australian ute pickup truck seen from the side with a tray back." 3:2
g dingo "a dingo dog standing seen from the side, alert, ears up, bushy tail." 3:2
# Antarctica (full colour)
gc seal_c "a Weddell seal lying on the snow seen from the side, grey spotted body, whiskers." 3:2
gc snowmobile_c "a red Antarctic research snowmobile on tracks with a windshield and a small sled attached, seen from the side." 3:2
gc radome_c "a white geodesic radar dome on a short cylindrical base, with a small door and a red light." 1:1
gc tent_c "an orange pyramid polar expedition tent with guy ropes pegged into the snow and a small flag on top." 1:1
gc icearch_c "a natural ice arch: a pale blue glacier ice formation shaped like a bridge with a tunnel through it, with icicles." 3:2
gc skua_c "a brown skua seabird standing on top of a wooden post, hooked beak." 1:1
wait; ls *.jpg | wc -l
