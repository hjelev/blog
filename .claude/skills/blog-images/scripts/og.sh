#!/usr/bin/env bash
# Generate a 1200x630 OG PNG from a header SVG: static/img/og/<name>.png
set -euo pipefail
for svg in "$@"; do
  name=$(basename "$svg" .svg)
  out="$(git -C "$(dirname "$svg")" rev-parse --show-toplevel)/static/img/og/$name.png"
  tmp=$(mktemp --suffix=.png)
  inkscape "$svg" --export-type=png --export-width=1120 --export-filename="$tmp" >/dev/null 2>&1
  magick "$tmp" -background '#14161b' -gravity center -extent 1200x630 "$out"
  rm -f "$tmp"
  echo "og: $out"
done
