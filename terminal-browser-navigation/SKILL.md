---
name: terminal-browser-navigation
description: Navigate an existing terminal-browser tab without creating another tab. Use when driving terminal-browser in orb, including a Lavish page, and changing the selected tab's URL, reloading a review page at a new URL, or staying in the original tab.
---

# Navigate the selected tab

**Use `navigate` or `goto` to stay in the selected tab.** `terminal-browser action -- open URL` creates another tab, even with an explicit tab selector. Do not use it for same-tab navigation or replace navigation with script evaluation.

## Select, navigate, verify

1. Resolve the intended browser pane with `orb pane browser PANE`. Use its returned key as `KEY`.
2. Run `terminal-browser ls --all --json`. Find the browser matching `KEY`, then choose the intended tab's `id` as `ID`. Note its URL, `targetId`, and tab count.
3. Replace `KEY`, `ID`, and `URL` below with those values and the destination. Keep both selectors on every action. Omit `--follow` so the user's selected tab stays unchanged.

```sh
terminal-browser action --browser KEY --tab ID -- navigate URL
terminal-browser ls --all --json
```

4. Confirm the selected tab has the destination URL, the same `id` and `targetId`, and no added tab. `goto URL` also supports same-tab navigation.
5. Release control when finished. `done` is a wrapper command, without the `--` separator.

```sh
terminal-browser action --browser KEY --tab ID done
```
