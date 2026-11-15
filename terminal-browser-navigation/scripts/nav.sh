#!/usr/bin/env bash
set -uo pipefail

if [ $# -lt 2 ] || [ $# -gt 3 ]; then
  echo "Usage: nav.sh <orb pane> <url> [<tab id>]" >&2
  echo "Navigates the pane's browser tab (the active one unless a tab id is given) without opening a new tab, then checks that." >&2
  exit 2
fi
pane=$1
url=$2
wanted=${3:-}

reply=$(orb pane browser "$pane" 2>&1) || { echo "nav.sh: no single browser in pane $pane: $reply" >&2; exit 1; }
key=$(python3 -c 'import json, sys; print(json.loads(sys.argv[1])["key"])' "$reply") || { echo "nav.sh: could not read the browser key from: $reply" >&2; exit 1; }

tabs() {
  terminal-browser ls --all --json | python3 -c '
import json, sys
key, wanted = sys.argv[1], sys.argv[2]
data = json.load(sys.stdin)
browsers = data.get("browsers", []) if isinstance(data, dict) else data
browser = next((entry for entry in browsers if entry.get("key") == key), None)
if browser is None:
    sys.exit(1)
tabs = browser["tabs"]
if wanted:
    tab = next((entry for entry in tabs if str(entry["id"]) == wanted), None)
else:
    tab = next((entry for entry in tabs if entry.get("active")), None)
if tab is None:
    sys.exit(2)
print(tab["id"], tab["targetId"], len(tabs), tab["url"])
' "$key" "$1"
}

before=$(tabs "$wanted") || { echo "nav.sh: browser $key has no such tab" >&2; exit 1; }
read -r tab target count _ <<<"$before"

terminal-browser action --browser "$key" --tab "$tab" -- navigate "$url" >/dev/null
status=$?
after=$(tabs "$tab") || after=""
terminal-browser action --browser "$key" --tab "$tab" done >/dev/null 2>&1
if [ "$status" -ne 0 ]; then
  echo "nav.sh: navigate failed in browser $key tab $tab" >&2
  exit 1
fi
if [ -z "$after" ]; then
  echo "nav.sh: tab $tab is gone after navigating" >&2
  exit 1
fi
read -r _ target_after count_after landed <<<"$after"
if [ "$target_after" != "$target" ]; then
  echo "nav.sh: tab $tab now points at a different page target ($target became $target_after)" >&2
  exit 1
fi
if [ "$count_after" -ne "$count" ]; then
  echo "nav.sh: the browser had $count tabs and now has $count_after" >&2
  exit 1
fi
echo "browser=$key tab=$tab url=$landed"
