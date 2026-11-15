---
name: terminal-browser-navigation
description: Visit URLs in terminal-browser without piling up tabs. Use whenever you run terminal-browser action to visit a URL, in any tab, any browser, or a loop over many URLs, including Lavish pages and review reloads.
---

# Navigate the selected tab

Run `scripts/nav.sh <orb pane> <url> [<tab id>]` from this skill's folder. It navigates the pane's browser in place (the active tab unless you name one), releases the browser, and fails if a tab was added or the tab was replaced. It prints `browser=<key> tab=<id> url=<where it landed>` and doesn't move the user's focus.

By hand, the same thing is `terminal-browser action --browser KEY --tab ID -- navigate URL`, with both selectors and no `--follow`.

- **`-- open URL` always creates another tab,** even with a tab selector. Never use it to visit a page in an existing tab.
- **Close a tab with `-- tab close`.** Plain `-- close` prints "Browser closed" and leaves the tab open.
