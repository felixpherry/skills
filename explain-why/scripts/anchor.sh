#!/usr/bin/env bash
set -uo pipefail

if [ $# -ne 1 ] && [ $# -ne 3 ]; then
  echo "Usage: anchor.sh <file> [<start line> <end line>]" >&2
  echo "Prints the code anchor: last-touch commits, recent history, PR numbers, ticket keys and PR discussions." >&2
  echo "Set ANCHOR_MAX_PRS to change how many PRs are fetched (default 5)." >&2
  exit 2
fi

file=$1
max_prs=${ANCHOR_MAX_PRS:-5}

if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
  echo "anchor.sh: not inside a git repository" >&2
  exit 1
fi
if ! git ls-files --error-unmatch -- "$file" >/dev/null 2>&1; then
  echo "anchor.sh: git does not track $file" >&2
  exit 1
fi

commits=""
if [ $# -eq 3 ]; then
  echo "## Last-touch commits for $file:$2-$3"
  git blame -s -L "$2,$3" -- "$file" | awk '{print $1}' | sort | uniq -c | sort -rn
  commits=$(git blame -s -L "$2,$3" -- "$file" | awk '{print $1}' | tr -d '^' | sort -u)
  echo
fi

echo "## Last 20 commits touching $file, through renames"
git log --follow --format='%h %ad %an %s' --date=short -20 -- "$file"
echo

recent=$(git log --follow --format='%h' -20 -- "$file")
messages=$(for commit in $commits $recent; do git log -1 --format='%B' "$commit"; done)

prs=$(printf '%s\n' "$messages" | grep -oE '\(#[0-9]+\)|pull request #[0-9]+' | grep -oE '[0-9]+' | awk '!seen[$0]++')
tickets=$(printf '%s\n' "$messages" | grep -oE '\b[A-Z][A-Z0-9]+-[0-9]+\b' | sort -u)

echo "## PR numbers in those commits"
printf '%s\n' "${prs:-none}"
echo
echo "## Ticket keys in those commits"
printf '%s\n' "${tickets:-none}"
echo

count=0
for pr in $prs; do
  count=$((count + 1))
  if [ "$count" -gt "$max_prs" ]; then
    echo "## PRs not fetched (over the limit of $max_prs)"
    printf '%s\n' "$prs" | tail -n +"$((max_prs + 1))"
    break
  fi
  echo "## PR #$pr"
  gh pr view "$pr" --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews 2>&1 \
    || echo "could not fetch PR #$pr with gh"
  echo
done
