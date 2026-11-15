---
name: write-investigation
description: Writes or revises an engineering investigation as a story, with a strange title that makes sense by the end, bold claims backed by evidence, plain explanations, and a little humor. Use when drafting a report from research notes, rewriting an investigation or proposal, suggesting titles or headings, or critiquing a draft, especially when there's a question to answer, competing explanations, or a surprising measurement. Not for release notes, runbooks, API docs, or incident updates.
---

# Investigative engineering storytelling

**Write like a novelist. Investigate like a scientist.**

A reader sees a strange title, follows the investigation, meets evidence that changes the first reading, and finishes knowing why the title was chosen. An impatient teammate can still pull out the conclusion, the trade-offs and the next action without reading every experiment.

The evidence decides the story. Never invent a number, experiment, quote, source or discovery, hide an inconvenient result, or build suspense the facts don't hold. An urgent security, privacy or safety finding goes first, with the action it needs; the story comes second.

## The voice

- **Poetic title, ruthless argument.** The headline may be grand, cryptic or paradoxical. The paragraphs under it are plain English.
- **Bold claim, narrow proof.** State the strongest conclusion the evidence warrants. "Our replay found no improvement" is not "this can never improve performance."
- **Explain the mechanism** so an engineer new to the subsystem can follow. Use jargon when it's more precise, then explain it.
- **Cut setup and decoration,** never caveats, measurements or reasoning.
- **Challenge the premise.** The ticket, the hypothesis, the benchmark and your own first explanation are all fair game.
- **Funny because it's true.** Seven links causing millions of renders beats an inserted joke. A dry line comes after a discovery's evidence, never before it, never at the cost of users or a colleague, and one per document beats one per section.
- **Personal, not synthetic.** Contractions are fine. No slang or swearing to fake a personality.

Avoid corporate filler ("leverage", "robust solution", "key takeaways"), TED-talk lines ("But here's the twist", "The real problem?"), forced triads, em dashes and inspirational endings.

## Titles that pay off later

The reference feeling is **"The 25% That Wasn't"**: short, slightly impossible on first reading, justified by the end. Find the title in the evidence:

1. **A measured contradiction.** "The 3 KB That Wasn't", only if the 3 KB response did cost more by a measurement you explain.
2. **The overlooked world.** "The Page Beyond the Page": the document was only part of what a visit downloaded.
3. **An innocent culprit.** "Seven Links, Five Million Renders."
4. **An incomplete premise.** "What the HTML Couldn't Explain."
5. **A reversal or failed fix.** "The Optimization That Added Bytes", only if a real experiment shows it.

These are patterns, not templates; don't keep producing "The X That Wasn't". An earned, specific title beats an enigmatic one the report can't pay off. Add a plain subtitle if the page needs to be findable.

**Title test:** it raises one real question, it's accurate, and a concrete discovery answers it.

## Tell the investigation, not the diary

Build a causal narrative, not a log of commands. Skip any beat that didn't happen:

1. **The premise.** What the ticket, team or dashboard said, and why it mattered.
2. **The first crack.** The one measurement that didn't fit.
3. **The competing explanations,** presented fairly, including why the obvious fix looked sensible.
4. **The experiment.** What you measured or changed, and what result would have supported each explanation.
5. **The reversal.** What survived and what failed. If the first hypothesis survived, tell that story.
6. **The consequences.** The effect in numbers, the costs and risks, the next step.
7. **The payoff.** End on the insight that makes the title click. No moral, no "and that's why the title is".

## Headings

A heading asks a question, announces a discovery, or helps the reader find an operational answer. Avoid buckets like "Analysis" and "Findings". For a report on expensive page loads:

- **Seven Innocent Links**: a large source of background traffic.
- **The Fix That Looked Bigger on Paper**: the obvious optimization has a hidden cost.
- **What Actually Moves the Needle**: the switch from story to decisions.
- **How We Counted**: the appendix. Reproducibility is never cryptic.

Mix a few chapter titles with plain, searchable headings for decisions, methods, security and appendices. Each section ends on the limit or implication that makes the next one necessary. If two sections can swap places, the report has become a list of findings.

## The opening

Open with a concrete contradiction in plain language, then the stakes:

> We went looking for oversized HTML. The browser was downloading pages nobody had asked to open.

For a work document, a **TL;DR** follows the hook: the conclusion, the largest supported numbers, the proposed work and the main caveat. Never hold back a decision to protect a reveal. Use one striking number at a time, with its unit and what it's out of (per response, per visit, per week).

## Evidence classes

Before drafting, sort each important statement:

- **Observed:** what telemetry, traces, browser captures, code or logs showed.
- **Measured:** the experiment's design, environment, result, repeats and variation.
- **Estimated:** the assumptions, the method, the likely range, and what wasn't measured.
- **Inferred:** a reasonable reading, not presented as proven cause.
- **Proposed:** a change, its expected benefit, owner, dependency and risk.
- **Unknown:** the test or fact that would settle it.

Keep exact units and populations. Don't mix compressed with decoded bytes, edge-sent with browser-delivered, correlation with cause, median with mean, or a simulated phone with a field measurement. Don't add overlapping savings as if they were independent. Put each caveat next to its claim, and link each source at the claim it supports.

## Default shape

Adapt it; several parts collapse in a short piece, and if the material holds no arc, write a plain memo.

1. Title, with an optional plain subtitle.
2. An opening of two to four sentences: premise and first contradiction.
3. TL;DR and decisions.
4. The investigation. Each section brings a question, a piece of evidence and the new understanding. Keep the failed hypotheses: a dead end shows honesty and often sets up the next discovery.
5. What survives measurement: proposals compared, estimates and overlaps marked.
6. What we will do, won't do, and still don't know.
7. A short ending that earns the title, only if it adds something the TL;DR didn't say.
8. Methods, definitions and sources in a plainly named appendix.

Tables compare options and measurements; say why a table matters before it and read its main result after it.

## By request

- **From notes:** find the central question, list claim, evidence and uncertainty, find the real surprise, build the arc, then write the title. Never pick the twist first.
- **From a draft:** keep the technical claims and the author's own turns of phrase. Reorder, rename headings selectively, tighten, and move detail to tables or the appendix instead of deleting evidence. Report factual inconsistencies separately; don't quietly correct a measurement.
- **Titles:** offer different mechanisms, not variants of one formula. For each, say its payoff and whether the evidence earns it.
- **Critique:** judge separately (1) accuracy and calibration, (2) central question and continuity, (3) title and ending payoff, (4) readability, (5) humor and voice. Quote passages and suggest targeted repairs.

## Final reads

- **As a skeptical engineer:** can I reproduce the decisive result? Are strong claims scoped to the experiment? Could a number or chart mislead?
- **As a busy teammate:** can I find the conclusion, impact, next action, risks and owners within a minute?
- **As a storyteller:** what question pulls me on? Does each section change my understanding? Does the title mean more at the end?

Then run the `unslop` rules over the draft.
