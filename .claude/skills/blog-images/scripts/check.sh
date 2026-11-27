#!/usr/bin/env bash
# Lint SVGs and render PNG previews for visual review.
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
out="${CLAUDE_SCRATCH:-${TMPDIR:-/tmp}}/blog-image-previews"
mkdir -p "$out"
status=0
for svg in "$@"; do
  python3 -I "$here/lint.py" "$svg" || status=1
  png="$out/$(basename "$svg" .svg).png"
  if inkscape "$svg" --export-type=png --export-width=1400 --export-background='#808080' --export-filename="$png" >/dev/null 2>&1; then
    echo "preview: $png"
  else
    echo "RENDER FAILED: $svg"; status=1
  fi
done
exit $status
