---
name: write-confluence-doc
description: Writes, rewrites, or polishes a Confluence page in a skimmable style (bold-claim bullets, panels, tables, a TL;DR up top) with a skeleton per doc type (policy, runbook, system doc, bug investigation). Use when the user wants a Confluence page drafted, rewritten, or polished.
argument-hint: <topic, draft text, or existing page URL>
---

# Confluence doc

## Steps

1. **Gather facts.** Collect the source material: the user's notes, an existing page (read as HTML; see [references/markup.md](references/markup.md)), tickets, code. Every rule, number, name, and time in the doc comes from that material or from the user. A fact you lack becomes an entry in the closing "Open items" panel, never a guess. Done when you can name, for each section, where its facts came from.
2. **Outline.** Pick the skeleton for the doc type from [references/skeletons.md](references/skeletons.md) and write the numbered heading list. Show it to the user when the doc is new or the structure changes. Done when the user accepts the outline, or the task is a polish of an existing page with fixed structure.
3. **Draft** the body as Confluence HTML into a file in the scratchpad. The elements and the Atlassian tools are in [references/markup.md](references/markup.md). Apply [Writing rules](#writing-rules), [Panels](#panels) and [Every doc](#every-doc). Read [references/examples.md](references/examples.md) before the first draft of a session: it shows each rule as a bad line and a good line.
4. **Check.** Run `python3 -I scripts/check_draft.py <draft> --title "<title>"` from this skill's folder and fix the draft until it prints nothing. Then pass every item in [Pre-publish check](#pre-publish-check), which covers what the script can't see.
5. **File and publish.** Find where the page goes: if the workspace has a filing skill or convention for its space, use it to get the parent page and labels; otherwise ask the user. Show the user the title, destination, and a short summary, then publish only after they confirm. Updating an existing page: update it in place with a one-line version message. Print the page URL last.

## Writing rules

Shape: skimmable first
- A reader skims the bold, the bullets, and the tables before reading any paragraph. Write so the skim alone gives the point.
- Bullets by default. Each bullet holds one idea. A bullet that states a rule or a finding opens with that claim in bold as one sentence, then the detail in plain text: `<li><p><strong>Readiness decides who can be primary.</strong> A junior or newly joined engineer can be assigned once the tech lead...</p></li>`.
- Prose paragraphs are for a reason ("Why X.") or a short causal explanation. Three sentences at most.
- A paragraph carrying more than two numbers becomes bullets or a table. Counts, rates, dates, and windows that describe one thing (an error's history, a rollout) are a two-column table: fact | value.
- Inline code is for one identifier the reader might type or grep: an endpoint, an error code, a command, a column. A query, a set of bound values, a log line, or anything that would wrap goes in a `<pre><code>` block under the sentence that introduces it.
- Dates are plain text ("8 Oct 2026"). No date chips.
- Write for every reader at once. No reader labels and no "ask X first" lines; each bullet works for anyone who reads it.
- Depth goes one page down. When a part serves only a few readers (the full method, derivations), move it to a child page and link it, so the main page stays skimmable.

Voice
- Write to the person doing the work, in second person: "Watch all three channels during your shift."
- Short declarative sentences. One idea per sentence. Plain verbs (is, has, runs).
- Say who decides and how: "The tech lead answers it case by case."
- State the default explicitly: "Default: 1 primary per shift."
- Give a concrete example with numbers when a rule is easy to misread: "a Normal inquiry that lands at 10:00 should not sit until 17:00."
- Be supportive where the reader might feel blamed (asking for help, a quiet shift). One sentence of reassurance, then the rule.
- In a findings doc, write as the engineer presenting the result. State what is true. Don't narrate how the investigation went or point at what others didn't do.
- Trust the reader. Cut mechanics a capable engineer doesn't need to act on; keep the result, and put the mechanics in the appendix or a child page.
- One plain word per concept, used everywhere. Prefer the word the team already uses over a coined one the reader has to translate.

Rule, then why
- State the rule first. If the reason is not obvious, follow it with a paragraph that opens with a bold lead: `<p><strong>Why not Monday morning.</strong> Issues pile up over the weekend...</p>`.
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
- Headers are a word or two. The explanation goes in the sentence above the table.

Numbers
- Every table adds up to the number the text quotes for it. If they differ, add the missing rows (subtotal, adjustments) until they match.
- A column header names what the number is out of.
- One unit, defined once. Use % for levels and changes, and say once near the top that changes are percentage points. No "points" or "pp" in the body.
- A cell that looks wrong explains itself in parentheses.

Stay on the question
- Every row, bullet, and open item serves the doc's question. True but off-topic findings go in a collapsed "Found along the way" in the appendix.
- Open items that hang on luck rather than on a check get cut.
- Every mechanism the TL;DR leans on gets its own section.

Single source of truth
- Each rule lives in exactly one section. Everywhere else links to it: "see <a href="#3.2-Secondary-on-call">§3.2 Secondary on-call</a>".

Evidence
- Link every source inline, right where you cite it: the Sentry issue, the PR, the ticket, the dashboard, the log search or query.
- A findings or research doc links the evidence (code, commits, queries, docs), not the work tracker. Ticket keys add nothing to a finding.

Punctuation and emphasis
- No em dash (—) and no en dash (–), anywhere: body, headings, table cells, title. Use a period, colon, comma, or parentheses. Ranges are "1 to 2 weeks", "09:00 to 18:00".
- Bold budget: about one bold phrase per paragraph or bullet, on the rule a skimmer must catch.
- "Not X, but Y" only when the reader actually believes X (for example, that the SLA is a waiting period). A few per doc at most.
- Times carry the team's timezone, written out: "18:00 UTC", never a bare "18:00".

## Panels

Every panel opens with a one-sentence bold claim, then one to three sentences of reason. A panel holds paragraphs and lists only (no tables, no nested panels). At most one panel per subsection and never three in a row.

| Type | Use it for | Example claim |
|---|---|---|
| `panel-info` | Exactly one, at the very top: what the doc covers and who reads it when, plus a status and review line. No owner line. Orientation only; conclusions go in the TL;DR right below it. In a research or findings doc it states the method instead: what data the numbers come from, the window, and why that source over the obvious one, with the key facts bold. Status, date, and earlier parts then go as bullets in a `panel-note` right below it. | "Read this before your first shift." / "Every number here comes from the raw request logs." |
| `panel-note` | A boundary or clarification the reader needs to apply the rule correctly: ownership limits, a term defined precisely, an edge case, a graduation criterion. Also the closing "Open items" panel. | "Acknowledge ≠ resolve." / "Ownership stays with the change owner." |
| `panel-warning` | A behaviour the reader will get wrong by default or under pressure, plus its cost. | "These are ceilings, not waiting periods." / "Acknowledging is the primary's job." |
| `panel-error` | Rare. An action that causes irreversible damage (data loss, money moved). Most docs need none. | "Never run the backfill against prod without a snapshot." |

Skip `panel-success`, custom panels, and emoji panels.

## Every doc

Sections are numbered `<h2>` ("4. Coverage & response SLA"), subsections numbered `<h3>` ("3.1 Primary on-call"), and an occasional unnumbered `<h4>` for a named idea inside a subsection. Sentence case. Docs with six or more sections get a `toc` macro (`maxLevel` 2) right after the info panel.

It opens with an unnumbered `<h2>TL;DR</h2>` directly after the info panel and before the `toc`. Three to five bullets: the conclusions and the actions a reader must take, each a bold one-sentence claim plus at most one plain sentence of detail, nothing the body does not already say. A reader who stops there has the answer. When the answer is a result reached through several levers, the TL;DR also says how: the result, then the levers as nested bullets, each with what it adds.

## Pre-publish check

The script covers dashes, date chips, links, panel rules and the TL;DR's place and size. These need a read:

- [ ] Skim test: reading only bold text, bullets, and tables gives every section's point. No paragraph over three sentences or with more than two numbers; no query or value set in inline code.
- [ ] Every table total matches the number the text quotes for it; every number column says what it is out of.
- [ ] No sentence claims more than its table shows. If a row says "Untested", the text does not say every option works.
- [ ] A hypotheses table lists candidate causes only. Rejected fixes go in the fix section's options table.
- [ ] Every rule appears in one section; repeats are links.
- [ ] Every cited source (Sentry issue, PR, ticket, dashboard, query) is linked inline where it's cited.
- [ ] Unknowns and proposed defaults are in the closing "Open items to confirm" panel, with the review cadence.
- [ ] The TL;DR says nothing the body doesn't.
- [ ] The prose passes the `unslop` rules.
