#!/bin/bash
# usage: bash gen_all.sh name "subject" aspect   (one sprite) ; all sprites for the title roadside objects. flat magenta background, backlit dark silhouette
G=../gen_img.py
S="Pixel art game sprite in a warm 16-bit style with a dark brown outline, drawn as a dark silhouette that looks backlit by a low sun: the whole object is deep brown and near black, with a thin warm orange rim of light along its right edge. Single object, centered, entire object visible with margin around it, flat solid pure magenta (#FF00FF) background, no ground, no shadow, no text, no other objects. The background is ONE flat solid magenta colour edge to edge: no sun, no sky, no stripes, no gradient, no border, no frame."
gen(){ [ -f "$1.jpg" ] && [ -z "$FORCE" ] && return; python3 $G "$1.jpg" "$S Subject: $2" "${3:-1:1}" ; }
gen "$@"
