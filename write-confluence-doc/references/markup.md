# Atlassian tools and markup

## Atlassian tools

These are the Atlassian MCP v2 tools (`https://mcp.atlassian.com/v2/mcp`). Get `cloudId` once from `getAccessibleAtlassianResources`.

- **Read:** `getConfluenceContent` with `detail: "full"` and `content_format: "html"`.
- **Create:** `createConfluenceContent` with `contentType: "page"`, the parent, and `body: {format: "html", value}`.
- **Update:** `updateConfluenceContent` with the `snapshotToken` from your last read, `body: {format: "html", value}`, and a one-line `versionMessage`.
- **Space instructions:** the tools ask you to load the space's own authoring instructions first (`getConfluenceSpace` through `executeRead`). Follow them where they don't clash with this skill.
- **Anything else** (a user lookup, the format guide): find the operation with `discover`, then run it with `executeRead`.

## Markup

Write HTML. Not storage XML (`<ac:...>`), not Markdown. Run `getContentFormatGuide` (through `executeRead`, toolName `createConfluencePage`) once if you need an element not shown here.

```html
<div data-type="panel-info">
  <p>Working instruction for the ... It defines who ..., when ..., and <strong>the one thing to remember</strong>. Read this before ...</p>
  <p>As of 8 Oct 2026 · Review every quarter</p>
</div>
<h2>TL;DR</h2>
<ul><li><p><strong>Conclusion in one sentence.</strong> One sentence of detail.</p></li></ul>
<div data-type="extension" data-extension-key="toc" data-extension-type="com.atlassian.confluence.macro.core" data-parameters='{"macroParams":{"maxLevel":{"value":"2"}},"macroMetadata":{"schemaVersion":{"value":"1"},"title":"Table of Contents"}}'></div>

<h2>1. What is X?</h2>
<p>...</p>

<h3>3.1 Primary on-call</h3>
<p>Rule. <strong>Why fixed timings.</strong> Reason.</p>

<div data-type="panel-warning"><p><strong>Claim in one sentence.</strong> Why it matters.</p></div>

<table data-width="760">
  <thead><tr><th><p>When</p></th><th><p>Do this</p></th></tr></thead>
  <tbody><tr><td><p><strong>Start of shift</strong></p></td><td><ul><li><p>First action</p></li><li><p>Second action</p></li></ul></td></tr></tbody>
</table>
```

- Same-page links use the hash form `#` + heading text with spaces as hyphens: `<h3>6.5 Handover &amp; documentation</h3>` is `href="#6.5-Handover-&amp;-documentation"`. Link text carries the section: "§6.5 Handover & documentation". Never a full page URL for a link within the page.
- People: a real mention needs an Atlassian account id (find the user-lookup operation with `discover`); without one write `[@name]` as plain text.
- When editing an existing page, keep every `<span class="annotation" ...>` intact so inline comments stay anchored.
