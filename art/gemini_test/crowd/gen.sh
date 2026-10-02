G=../gen_img.py
S="Pixel art game sprite in a warm 16-bit style: a concert audience member seen from BEHIND, cropped at the waist, as a dark silhouette in deep brown and near black with a thin warm orange rim of light along the top edges of the head and shoulders. Single figure centered with margin around it. The background is ONE flat solid pure magenta (#FF00FF) colour edge to edge: no stage, no lights, no sky, no gradient, no border, no floor, no shadow, no text."
g(){ python3 $G "$1.jpg" "$S Subject: $2" 1:1 >/dev/null 2>&1 & }
g crowd_a "short hair, broad shoulders, plain jacket."
g crowd_b "long wavy hair falling past the shoulders."
g crowd_c "hair tied in a bun on top of the head, slim shoulders."
g crowd_d "a knitted beanie hat and a hooded sweatshirt."
g crowd_hat "a wide-brimmed cowboy hat and a denim jacket."
g crowd_arms "both arms raised straight up in the air, hands open, cheering, short hair."
g crowd_arm1 "one arm raised high holding up a small glowing phone, the other arm down, ponytail."
g crowd_board "carrying a tall surfboard upright on one shoulder, short messy hair, the board sticks up above the head."
g crowd_penguin "an emperor penguin seen from behind, black back with a pale rim, small head turned slightly, no magenta on it."
wait; ls *.jpg | wc -l
