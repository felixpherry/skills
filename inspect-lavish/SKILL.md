---
name: inspect-lavish
description: Reads and scrolls an already-open Lavish report in terminal-browser. Use to read below the fold, jump to a heading, or when eval or a full-page screenshot misses the report's content.
---

# Inspect Lavish

Read an open Lavish report by jumping to the part you need. The report sits in a sandboxed frame inside the review page.

Get the browser key (`orb pane browser <pane>` in orb) and the tab id (`terminal-browser ls --all --json`), and pass both on every action. Don't move the user's focus.

## Read and scroll

1. **Enter the report:** `scripts/frame.sh enter <browser key> <tab id>`, from this skill's folder. It selects the report's frame, saves a full snapshot to a file, and prints the file's path and the first headings. If the headings belong to the review page and not the report, something is off: stop and look at the frames.
2. **Find the target** in the snapshot file and copy its reference (`@eNN`). If the target has none, use the nearest heading or control that does.
3. **Scroll and look:**

```sh
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- scrollintoview @eNN
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- screenshot /tmp/lavish-section.png
```

Open the image to confirm the section is visible; a scroll that succeeded proves nothing.

4. **Leave:** `scripts/frame.sh leave <browser key> <tab id>`, also after an error. It returns to the outer page and releases the browser.

**References die on a reload, a report update or a frame change.** Run `enter` again for new ones. Scroll by reference, never by repeated PageDown.

## What doesn't work

- **`eval` still runs in the outer review page,** even with the report's frame selected. A lookup for a report element returns null there. Compare `eval 'location.href'` with the frame's address to see which document answered.
- **The sandbox stays.** It gives the report its own origin, so the outer page can't read it. Don't remove it, add `allow-same-origin`, or change browser security settings.
- **A full-page screenshot holds the review page and only the visible part of the report.** Don't call it a whole-report capture. Screenshot the sections you need and label them as sections.
