#!/bin/bash
# Generate icons

## Getting the icon
## wget 'http://upload.wikimedia.org/wikipedia/en/f/f9/Imageshacknew.png' -O "$1/ImageShack.png"

## $1: source dir, $2: binary dir.

uudecode -o "$2/ImageShack.png" "$1/ImageShack.png.uu"

Sizes="64 48 32 24 22 16"
echo "Making:"
for x in $Sizes
do
    Dir="$2/icons/hicolor/${x}x${x}/apps"
    mkdir -p "$Dir"
    echo $x
    convert "$2/ImageShack.png" -resize ${x}x${x}\! "$Dir/ImageShack.png"
done
echo "Generated icons."
