---
name: inspect-lavish
description: Inspects and scrolls already-open Lavish reports in terminal-browser using fresh frame-owned snapshot references. Use to read sections below the fold, jump to a report heading, troubleshoot frame-selected eval that still sees the outer page, or check whether a full-page screenshot includes the nested artifact.
---

# Inspect Lavish

Read a Lavish artifact without repeated PageDown calls. Keep its sandbox unchanged.

## Start with the intended browser

Use the terminal-browser skill for browser commands and the orb skill for pane targeting when inside orb. Start with an already-open Lavish review. Get its browser key and tab ID, then pass both on every action. Do not rely on the active browser or move the user's focus.

In the examples, replace `BROWSER_KEY` and `TAB_ID` with those observed values.

## Find the artifact, then take fresh references

1. Return to the outer page and inspect its frames:

```sh
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- frame main
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- eval 'Array.from(document.querySelectorAll("iframe"), f => ({src: f.getAttribute("src"), sandbox: f.getAttribute("sandbox")}))'
```

2. Select the artifact iframe, not a helper iframe. Current Lavish reviews use an artifact URL containing `/artifact/`. Confirm that in the output before using this selector; use the observed artifact selector if it differs.

```sh
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- frame 'iframe[src*="/artifact/"]'
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- snapshot
```

3. Read the full snapshot and find the target heading, text, or control. Do not use an interactive-only snapshot when looking for a heading. Confirm the snapshot contains the artifact, not the review shell.

4. Copy the target's reference from that snapshot. Replace `@eNN` below with that reference, then scroll and check a viewport screenshot:

```sh
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- scrollintoview @eNN
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- screenshot /tmp/lavish-section.png
```

Open the image and confirm the intended section is visible. A successful scroll command alone is not proof. If the reference is stale or points at the wrong content, select the artifact frame again, take a new full snapshot, and retry with the new reference.

**Refresh references after reloads, artifact updates, and frame changes.** Never reuse an example reference or assume a previous reference still belongs to the same element. If the target has no reference, choose a nearby referenced heading or control. Do not replace this workflow with PageDown loops.

## Why frame-selected eval misses the content

**Selecting a frame scopes locator actions, not JavaScript evaluation in the observed tooling.** Even after selecting the artifact frame, `eval` still runs in the outer review page. An artifact-only element lookup can return null and `scrollIntoView()` can fail with `Cannot read properties of null`.

To check this, compare `eval 'location.href'` with the artifact frame's URL and inspect a fresh frame snapshot. A null lookup alone does not prove which document ran the script. Use `scrollintoview` on a fresh frame-owned reference instead of evaluating a DOM scroll.

The artifact's sandbox gives it a separate origin. Reading its DOM through the outer page does not bypass that boundary. Do not remove the sandbox, add `allow-same-origin`, or change browser security settings.

## What a full-page screenshot covers

**A successful full-page capture may contain only the outer review shell and the artifact's current viewport.** It does not prove that content below the fold inside the nested artifact was captured.

If checking this limit, return to `frame main`, take `screenshot /tmp/lavish-shell-full.png --full`, and open the image. Check for both the artifact's first and last sections. Do not call it a whole-report capture unless the image shows the whole report. Use fresh references and viewport screenshots for the sections you need; label them as section captures.

## Finish

Return to the outer frame and release browser control, including after an error:

```sh
terminal-browser action --browser BROWSER_KEY --tab TAB_ID -- frame main
terminal-browser action --browser BROWSER_KEY --tab TAB_ID done
```
