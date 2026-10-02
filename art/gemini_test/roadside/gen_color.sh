G=../gen_img.py
C="Pixel art game sprite in a warm 16-bit style with a dark brown outline, full colour with soft shading, lit from the right by a low warm sun. Single object, centered, entire object visible with margin around it, flat solid pure magenta (#FF00FF) background edge to edge: no sun, no sky, no stripes, no gradient, no border, no frame, no ground, no shadow, no text, no other objects."
g(){ python3 $G "$1.jpg" "$C Subject: $2" "${3:-1:1}" >/dev/null 2>&1 & }
g berg_c "a jagged Antarctic iceberg with a flat top and angular faces, pale blue and white ice, deeper blue in the shadowed faces." 3:2
g hut_c "a small red Antarctic research hut raised on stilts, pitched roof with white snow on it, three warm lit yellow windows, a ladder and a chimney pipe." 3:2
g flag_c "a tall flagpole with a small orange rectangular flag flying to the right, a base of stacked stones." 1:1
g penguin_c "an emperor penguin standing upright seen from the side, black back, white belly, yellow-orange neck patch." 1:1
g beacon_c "a tall grey Antarctic survey beacon: a slim steel mast with crossbars, guy wires, and a small glowing amber lamp at the top." 1:1
g roosign_c "a roadside kangaroo crossing warning sign: a yellow diamond-shaped sign with a black leaping kangaroo, on a thin grey post." 1:1
g vending_c "a roadside drink vending machine seen from the front, blue body, glowing white panel with colourful drink buttons, a dark dispensing slot." 1:1
wait
