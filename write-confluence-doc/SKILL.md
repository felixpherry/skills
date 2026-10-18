---
name: write-confluence-doc
description: Writes, rewrites, or polishes a Confluence page in a skimmable style (bold-claim bullets, panels, tables, a TL;DR up top) with a skeleton per doc type (policy, runbook, system doc, bug investigation). Use when the user wants a Confluence page drafted, rewritten, or polished.
argument-hint: <topic, draft text, or existing page URL>
---

# Confluence doc

## Steps

1. **Gather facts.** Collect the source material: the user's notes, an existing page (read as HTML; see [Atlassian tools](#atlassian-tools)), tickets, code. Every rule, number, name, and time in the doc comes from that material or from the user. A fact you lack becomes an entry in the closing "Open items" panel, never a guess. Done when you can name, for each section, where its facts came from.
2. **Outline.** Pick the skeleton for the doc type (see [Skeletons](#skeletons)) and write the numbered heading list. Show it to the user when the doc is new or the structure changes. Done when the user accepts the outline, or the task is a polish of an existing page with fixed structure.
3. **Draft** the body as Confluence HTML (see [Markup](#markup)) into a file in the scratchpad. Apply [Writing rules](#writing-rules) and [Panels](#panels) as you go.
4. **Check** the draft against every item in [Pre-publish check](#pre-publish-check). Done when each item passes.
5. **File and publish.** Find where the page goes: if the workspace has a filing skill or convention for its space, use it to get the parent page and labels; otherwise ask the user. Show the user the title, destination, and a short summary, then publish only after they confirm. Updating an existing page: update it in place with a one-line version message. Print the page URL last.

## Writing rules

Shape: skimmable first
- A reader skims the bold, the bullets, and the tables before reading any paragraph. Write so the skim alone gives the point.
- Bullets by default. Each bullet holds one idea. A bullet that states a rule or a finding opens with that claim in bold as one sentence, then the detail in plain text: `<li><p><strong>Readiness decides who can be primary.</strong> A junior or newly joined engineer can be assigned once the tech lead...</p></li>`.
- Prose paragraphs are for a reason ("Why X.") or a short causal explanation. Three sentences at most.
- A paragraph carrying more than two numbers becomes bullets or a table. Counts, rates, dates, and windows that describe one thing (an error's history, a rollout) are a two-column table: fact | value.
- Inline code is for one identifier the reader might type or grep: an endpoint, an error code, a command, a column. A query, a set of bound values, a log line, or anything that would wrap goes in a `<pre><code>` block under the sentence that introduces it.
- Dates are plain text ("8 Oct 2026"). No date chips.

Voice
- Write to the person doing the work, in second person: "Watch all three channels during your shift."
- Short declarative sentences. One idea per sentence. Plain verbs (is, has, runs).
- Say who decides and how: "The tech lead answers it case by case."
- State the default explicitly: "Default: 1 primary per shift."
- Give a concrete example with numbers when a rule is easy to misread: "a Normal inquiry that lands at 10:00 should not sit until 17:00."
- Be supportive where the reader might feel blamed (asking for help, a quiet shift). One sentence of reassurance, then the rule.

Rule, then why
- State the rule first. If the reason is not obvious, follow it with a paragraph that opens with a bold lead: `<p><strong>Why not Monday morning.</strong> Issues pile up over the weekend...</p>`. The reason is part of the policy. Readers follow rules they understand and argue less about them.
- Keep the reason to what changes behaviour. Drop history ("the policy previously paged everyone") from the body; put it in a "Changes" section at the end if it matters.

Separate what gets conflated
- When one word covers several things, open the section by naming them apart: "Three different things get called escalation. Keep them apart:" followed by a bullet per meaning, each with its own subsection.

Lists
- Trigger lists say whether one or all must hold: "Call for help when any of these is true:".
- "A good handover includes:" style lists name the minimum content of an artifact.
- Bullets in a plain list of facts (the minimum content of a handover) stay unbolded; bold only the key term if one exists ("assigned in the **quarterly roadmap**").

Tables
- Use a table whenever the reader compares rows on the same attributes: roles, severities, escalation levels, sprint length vs arrangement.
- Bold the first column only when it is the lookup key. Bold the one cell value a skimmer hunts for (the SLA number), nothing else.
- Put lists inside cells as `<ul>`; never join items with " · ".

Single source of truth
- Each rule lives in exactly one section. Everywhere else links to it: "see <a href="#3.2-Secondary-on-call">§3.2 Secondary on-call</a>". A rule restated in three sections goes wrong the first time someone edits only one of them.

Evidence
- Link every source inline, right where you cite it: the Sentry issue, the PR, the ticket, the dashboard, the log search or query. The reader reaches the evidence in one click, never by asking where it is.

Punctuation and emphasis
- No em dash (—) and no en dash (–), anywhere: body, headings, table cells, title. Use a period, colon, comma, or parentheses. Ranges are "1 to 2 weeks", "09:00 to 18:00".
- Bold budget: about one bold phrase per paragraph or bullet, on the rule a skimmer must catch. Bold that lands on every line stops meaning anything.
- "Not X, but Y" only when the reader actually believes X (for example, that the SLA is a waiting period). A few per doc at most.
- Times carry the team's timezone, written out: "18:00 UTC", never a bare "18:00".
- Before finishing, run the draft prose through the `unslop` rules.

## Panels

Every panel opens with a one-sentence bold claim, then one to three sentences of reason. A panel holds paragraphs and lists only (no tables, no nested panels). At most one panel per subsection and never three in a row; a panel used on routine text dilutes the ones that matter.

| Type | Use it for | Example claim |
|---|---|---|
| `panel-info` | Exactly one, at the very top: what the doc covers and who reads it when, plus a status and review line. No owner line. Orientation only; conclusions go in the TL;DR right below it. | "Read this before your first shift." |
| `panel-note` | A boundary or clarification the reader needs to apply the rule correctly: ownership limits, a term defined precisely, an edge case, a graduation criterion. Also the closing "Open items" panel. | "Acknowledge ≠ resolve." / "Ownership stays with the change owner." |
| `panel-warning` | A behaviour the reader will get wrong by default or under pressure, plus its cost. | "These are ceilings, not waiting periods." / "Acknowledging is the primary's job." |
| `panel-error` | Rare. An action that causes irreversible damage (data loss, money moved). Most docs need none. | "Never run the backfill against prod without a snapshot." |

Skip `panel-success`, custom panels, and emoji panels.

## Skeletons

Sections are numbered `<h2>` ("4. Coverage & response SLA"), subsections numbered `<h3>` ("3.1 Primary on-call"), and an occasional unnumbered `<h4>` for a named idea inside a subsection. Sentence case. Docs with six or more sections get a `toc` macro (`maxLevel` 2) right after the info panel.

Working instruction or policy (the reference shape):
1. What is X? Definition, why it exists, and what it does not cover (link to the scope section).
2. When and how long. Mechanics, with a "Why" paragraph for any choice that looks odd.
3. Who. Roles table (role, expectation, purpose, counts as X?), then one subsection per role.
4. Expectations. SLA or targets table, then the note and warning that stop misreadings.
5. Inputs. Where the work comes from, and the single system of record.
6. Scope of responsibility. One subsection per duty; include "when to hand off or call for help" with a trigger list.
7. Escalation and exceptions.
8. Remaining policies (location, compensation), one section each.
9. Checklist table: When | Do this, with a `<ul>` per cell.
10. Changes (optional): dated rows for what changed and why.

Close with a `panel-note` that starts "**Open items to confirm:**", lists every unknown and proposed default, and states the review cadence.

Every doc, whatever its shape, opens with an unnumbered `<h2>TL;DR</h2>` directly after the info panel and before the `toc`. Three to five bullets: the conclusions and the actions a reader must take, each a bold one-sentence claim plus at most one plain sentence of detail, nothing the body does not already say. A reader who stops there has the answer.

Runbook: summary panel, When to use, Prerequisites and access, Steps (`<ol>`, one action per step, expected output after each), Verify, Rollback, Escalation, Open items.

System or architecture doc (`[Tech Docs]`, `[System Design]`, `[Tech Flow]`):
1. What is X? What the system does, what it owns, what it leaves to other services (by name).
2. How it works. The main flow as an `<ol>`, one hop per step: caller, service, endpoint or queue in `<code>`, what changes. A diagram image goes after the list, never instead of it.
3. Components and ownership. Table: component | repo | owner | notes.
4. Data model. Per table: column | type | meaning. Name who writes and who reads it.
5. States. If anything has a status, a table of status | meaning | set by | next states.
6. Integrations and config. External parties, which env vars or secrets exist and where they live. Never the values.
7. Design decisions. Each decision is a rule-then-why: what was chosen, a bold "Why X." paragraph, and the rejected option in one sentence.
8. Failure modes. Table: symptom | likely cause | what to check or which runbook.
9. Open items.

Bug investigation and fix (`[Investigation]`). Load `write-investigation` first for the voice, the earned title, and the evidence classes (observed, measured, inferred, unknown). The story decides the order of sections and the title. Paragraph shape, markup, panels, and the dash ban come from this skill: a story section is still bold-claim bullets, short paragraphs, and tables, never a run of long paragraphs. Where the two disagree (shape, dashes), this one wins. Title is `[Investigation] <earned title>`. If the space has an approved example investigation, read it before drafting one.
- Info panel: what broke and the current status in one sentence. Second line: ticket, PR, "As of" date, commit SHA.
- TL;DR: symptom, root cause in one sentence, the fix with PR link, impact, and what is still open.
- 1. Symptom. What users or alerts saw, with numbers and the first-seen time in the team's timezone. How to reproduce, or that it is intermittent and under what conditions.
- 2. Why it was hard. The first crack: which observation broke the obvious explanation. Chapter-style heading text is fine here and in 4; keep the number.
- 3. Hypotheses. Table: hypothesis | how we tested it | result | verdict. Verdict is a status lozenge: red "Ruled out", green "Confirmed", yellow "Unverified". This table is what stops the next engineer from retrying dead ends, so keep the ruled-out rows.
- 4. Root cause. The mechanism as an `<ol>`, one causal step per item, each citing `<code>repo/path/file:line</code>`. State the exact trigger conditions. The trap that hid it goes in a `panel-warning`.
- 5. Fix. What changed, why at that spot (every caller that routes through it), PR links, the rejected fix in one sentence with its reason.
- 6. Verification. Repro before and after, the test that now fails without the fix, production signal after deploy.
- 7. Impact and cleanup. Affected orders, users, or money, and whether a backfill ran (link it) or is still open.
- 8. Prevention. The alert, test, or guard that would have caught it earlier, each with an owner or a ticket.
- 9. Open items.
- Appendix: dated timeline table, then queries, commands, and raw logs, each inside `<details><summary>...</summary>...</details>` so evidence stays one click away without burying the story.

Tech doc extras: the info panel's second line carries an "As of" date (and the commit SHA when the doc was traced from code), since system docs go stale. Cite code as `<code>repo/path/file.ts:123</code>`. Put gotchas a reader will trip on (ordering, retries, idempotency, timezone) in a `panel-warning` right where the flow hits them. For a flow you still have to trace from code, trace it first (with the workspace's tracing skill if it has one), then use this skill for the writing.

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

## Pre-publish check

- [ ] `grep -n -e '—' -e '–' <draft>` returns nothing (title included).
- [ ] Use vocabularies that are easy to understand.
- [ ] 1 sentence should make 1 point only. Making more than 1 point in a sentence make the sentence difficult to understand.
- [ ] Skim test: reading only bold text, bullets, and tables gives every section's point. No paragraph over three sentences or with more than two numbers; no query or value set in inline code; no `<time>` chips.
- [ ] Exactly one `panel-info`, at the top, with a status and review line.
- [ ] Every panel opens with a bold one-sentence claim; no tables inside panels; no three panels in a row.
- [ ] Every rule appears in one section; repeats are links.
- [ ] Every cited source (Sentry issue, PR, ticket, dashboard, query) is linked inline where it's cited.
- [ ] Every same-page link is a `#anchor` that matches a heading exactly, punctuation included (`<h2>5. Fix (not chosen yet)</h2>` is `#5.-Fix-(not-chosen-yet)`). No `href="#"`.
- [ ] No sentence claims more than its table shows. If a row says "Untested", the text does not say every option works.
- [ ] A hypotheses table lists candidate causes only. Rejected fixes go in the fix section's options table.
- [ ] Every non-obvious rule has its "Why" paragraph; every role or decision names who decides.
- [ ] Unknowns and proposed defaults are in the closing "Open items to confirm" panel, with the review cadence.
- [ ] `<h2>TL;DR</h2>` sits directly after the info panel, with three to five bold-claim bullets and no new facts.
- [ ] Unslop pass done: no "not just X, but Y", generic closers, forced triads, or decorative bold.
