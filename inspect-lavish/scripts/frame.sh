#!/usr/bin/env bash
set -uo pipefail

if [ $# -ne 3 ] || { [ "$1" != enter ] && [ "$1" != leave ]; }; then
  echo "Usage: frame.sh enter|leave <browser key> <tab id>" >&2
  echo "enter selects the Lavish report's frame and saves a full snapshot to a file; leave returns to the outer page and releases the browser." >&2
  exit 2
fi
mode=$1
key=$2
tab=$3

act() {
  terminal-browser action --browser "$key" --tab "$tab" -- "$@"
}

if [ "$mode" = leave ]; then
  act frame main >/dev/null
  terminal-browser action --browser "$key" --tab "$tab" done >/dev/null
  exit 0
fi

act frame main >/dev/null || { echo "frame.sh: browser $key tab $tab did not answer" >&2; exit 1; }
frames=$(act eval 'JSON.stringify(Array.from(document.querySelectorAll("iframe"), f => f.getAttribute("src")))')
if ! printf '%s' "$frames" | grep -q '/artifact/'; then
  echo "frame.sh: no frame with /artifact/ in its address. Frames on the page: $frames" >&2
  exit 1
fi
act frame 'iframe[src*="/artifact/"]' >/dev/null || { echo "frame.sh: could not select the report frame" >&2; exit 1; }
out="${TMPDIR:-/tmp}/lavish-snapshot-$key-$tab.txt"
act snapshot >"$out" || { echo "frame.sh: snapshot failed" >&2; exit 1; }
echo "snapshot=$out lines=$(wc -l <"$out" | tr -d ' ')"
grep -m 12 -E '^ *- heading ' "$out"
