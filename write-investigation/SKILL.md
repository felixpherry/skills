---
name: write-investigation
description: Writes or revises an engineering investigation as a story, with a strange title that makes sense by the end, bold claims backed by evidence, plain explanations, and a little humor. Use when drafting a report from research notes, rewriting an investigation or proposal, suggesting titles or headings, or critiquing a draft, especially when there's a question to answer, competing explanations, or a surprising measurement. Not for release notes, runbooks, API docs, or incident updates.
metadata:
  author: Felix
  version: "1.0"
---

# Investigative Engineering Storytelling

**Write like a novelist. Investigate like a scientist.**

The desired effect: a reader sees a strange title, becomes curious, follows an investigation, encounters evidence that changes the initial interpretation, and finishes knowing *why that title was chosen*. The result must still work as an engineering document: an impatient teammate can extract the conclusion, the trade-offs, and the next action without reading every experiment.

This is an editorial skill, **not** permission to invent discoveries, conceal inconvenient results, or manufacture suspense. The evidence determines the story; the writer decides how to tell it.

## When to use

Use this skill for technical investigations and proposals with a question, an assumption to test, competing explanations, surprising measurements, rejected approaches, or a decision worth defending. It can draft from research notes, rewrite an existing report, suggest titles/headings, or critique a draft.

Do not force a mystery onto release notes, API references, runbooks, straightforward tutorials, or incident communications where speed and literal clarity outweigh narrative. For urgent security, privacy, or safety findings, surface the finding and required action immediately; storytelling comes second.

## The voice

- **Poetic title, ruthless argument.** The headline may be grandiose, cryptic, paradoxical, or slightly clickbaity. The paragraphs underneath should be plain English.
- **Bold claim, narrow proof.** State the strongest conclusion the evidence *actually* warrants. Distinguish “our replay found no improvement” from “this can never improve performance.”
- **Smart, not performatively sophisticated.** Explain mechanisms so an engineer unfamiliar with the subsystem can follow the argument. Use jargon when it is more precise, then explain it.
- **Concise, not shallow.** Cut repetitive setup and decoration, not essential caveats, measurements, or reasoning.
- **Confident enough to challenge the premise.** The original ticket, hypothesis, benchmark, and your own first explanation are all fair game.
- **Funny because it's true.** Prefer the inherent absurdity of an actual system—seven links causing millions of renders—over inserted jokes. Dry understatement and an occasional conversational aside are welcome.
- **Personal, not synthetic.** Natural contractions and occasional informal phrasing are fine. Never inject slang or swear words merely to imitate a personality.

Avoid corporate filler (“leverage,” “robust solution,” “key takeaways”), TED-talk declarations, generic AI cadence (“But here's the twist,” “The real problem?”, “This wasn't just X—it was Y”), forced three-part slogans, relentless em dashes, and inspirational endings. A genuinely good contradiction needs no hype.

## Titles that reveal their meaning later

The reference feeling is **“The 25% That Wasn't”**: short, memorable, somewhat impossible on first reading, and completely justified after the investigation. Think of a title whose full meaning is unlocked retrospectively—not a headline that merely summarizes a table.

Look for a title in the *actual* evidence:

1. **A measured contradiction:** “The 3 KB That Wasn't” — only if the seemingly 3 KB response truly incurred more transfer by a clearly explained measurement.
2. **The overlooked world:** “The Page Beyond the Page” — the nominal document was only part of what a visit downloaded.
3. **An innocent culprit:** “Seven Links, Five Million Renders” — ordinary-looking behavior had disproportionate effects.
4. **An incomplete premise:** “What the HTML Couldn't Explain” — the initial investigation's boundary missed the larger phenomenon.
5. **A reversal or failed fix:** “The Optimization That Added Bytes” — only if a real experiment demonstrates this outcome.

These are *patterns, not title templates*. Do not compulsively generate more “The X That Wasn't” titles. Prefer a specific and earned title over an enigmatic title that the report cannot pay off. If the title needs an explanatory subtitle for discoverability, add one; do not spoil every interesting detail in it.

**Title test:** Does it create one genuine question? Is it accurate? Does a concrete discovery eventually answer that question? Would the reader appreciate it more after finishing?

## Tell the investigation, not the diary

Construct a **causal narrative**, not a chronological log of every command you ran. Most investigations have some version of these beats, but skip beats that did not happen:

1. **The premise.** What did the ticket, team, dashboard, or conventional wisdom say? Why did the question matter?
2. **The first crack.** Which measurement failed to fit that explanation? Give the reader one concrete anomaly, not ten facts at once.
3. **The competing explanations.** Present the plausible alternatives fairly. Let the reader understand why an apparently sensible fix seemed sensible.
4. **The experiment.** Explain what you measured or changed and what result would have supported each explanation. Include enough setup to understand the result.
5. **The reversal.** Show what survived measurement, what failed, and what you learned. A negative result can be the most interesting part.
6. **The consequences.** Quantify the effect where possible, compare costs and risks, and state what should happen next.
7. **The payoff.** End on the insight that makes the title click. Do not add an artificial moral or announce “and that's why the title is…”

A reversal is optional. Sometimes the initial hypothesis survives. Tell *that* story rather than inventing a plot twist. Organize sections around changes in the reader's understanding; use a table or appendix when the material is mainly reference data.

**The tension comes from the reasoning:** What did we expect? What did we observe? Why didn't they match? Which explanation survived a test? What changed as a result?

## Headings: chapters, not filing cabinets

A heading should do one of three jobs: pose an intriguing question, announce a meaningful discovery, or help the reader find an operational answer. Favor headings that advance the argument, not generic buckets such as “Analysis,” “Findings,” or “Further Discussion.”

Possible progression for a report about unexpectedly expensive page loads:

- **The Page Beyond the Page** — document title; meaning unfolds through the report.
- **Seven Innocent Links** — an unexpectedly large source of background traffic.
- **The Page Wasn't the Expensive Part** — in-page RSC changes the accounting.
- **The Fix That Looked Bigger on Paper** — the obvious translation optimization has a hidden soft-navigation cost.
- **A 3 KB Redirect** — introduce an apparently negligible response before exposing the true delivered cost.
- **What Actually Moves the Needle** — switch deliberately from narrative to decisions.
- **How We Counted** — straightforward appendix heading. Reproducibility should never be cryptic.

Don't make *every* heading a riddle. Mix a few memorable chapter titles with searchable, unambiguous headings for decisions, methods, security concerns, and appendices. Favor short headings; avoid spelling out their punchline in the next sentence unless the audience needs it.

Between sections, **carry the question forward**. Close one section with the limitation or implication that makes the next necessary. If two sections can be swapped without changing the argument, check whether the report has become a collection of unrelated findings.

## The opening: curiosity without hiding the answer

Open with a concrete contradiction or unexpected result in ordinary language, then establish stakes. Don't begin with corporate context or a long glossary.

Example:

> We went looking for oversized HTML. The browser was downloading pages nobody had asked to open.
>
> The original plan targeted translations and Zendesk. Those bytes exist. They just weren't where most of the waste was hiding.

For a work document, follow the hook with a **TL;DR / decision brief** containing the actual conclusion, largest supported measurements, proposed work, and major caveat. Busy stakeholders should get the answer immediately. The body can still create narrative satisfaction by explaining *how* the answer was established; don't withhold a critical decision to preserve a literary reveal.

Use one striking number at a time. Establish its unit and denominator (per response, per visit, per week), then explain why it matters.

## Evidence is the plot armor

Before drafting, classify important statements:

- **Observed:** What telemetry, traces, browser captures, code, or logs showed.
- **Measured:** Experiment design, environment, result, repeats, and error or variation where relevant.
- **Estimated/modelled:** Assumptions, extrapolation method, likely range, and which part wasn't measured directly.
- **Inferred:** Reasonable interpretation of the evidence, without presenting causation as proven.
- **Proposed:** A change, expected benefit, owner, dependency, and risk.
- **Unknown:** The test or information that would settle the question.

Never fabricate a number, experiment, quotation, source, or discovery to improve the arc. Preserve exact units and population; never confuse compressed with decoded bytes, edge-sent with browser-delivered bytes, correlation with causation, median with mean, or a simulated phone with a real field measurement. Don't add overlapping estimated savings as though independent. Place consequential caveats near the corresponding claim, not only in the appendix.

If sources or reproducible artifacts exist, cite or link them at the claims they support and keep detailed methods available. Technical trust is what makes an ambitious title possible.

## Pace, humor, and visual rhythm

- Lead paragraphs with their point. Usually keep paragraphs short; use a single-sentence paragraph only when the emphasis earns it.
- Give the surprising observation room, then explain the mechanism. Avoid stacking five twists in one paragraph.
- Translate abstractions into concrete actions: “The footer fetched seven pages” beats “Navigation induced nontrivial request amplification.”
- Use tables to compare options, distributions, measurements, and decisions—not to replace the argument. Introduce why a table matters; interpret its most important result afterward.
- Use code snippets when a mechanism depends on a specific API, header, condition, or implementation trap.
- Allow a dry joke after a discovery, never before its evidence, and never at the expense of affected users or a colleague. One memorable line is better than jokes in every section.
- Keep rejected ideas. A well-explained dead end demonstrates intellectual honesty and often sets up the next discovery.
- Cut sentences that merely announce what the next paragraph will say. Let the paragraph say it.

## Default document shape

Adapt this to the material; it is not a mandatory fill-in-the-blanks template.

1. **Enigmatic title**, with optional informative subtitle.
2. **Two-to-four-sentence opening** that establishes the premise and first contradiction.
3. **TL;DR / decisions** for readers who will not finish the story. Include a safety-critical finding immediately if one exists.
4. **Narrative investigation:** each major section introduces a question, a meaningful piece of evidence, and the new understanding it creates. Show important failed hypotheses.
5. **What survives measurement:** compare proposals and show which findings justify which actions. Mark estimates and overlaps.
6. **What we will do / won't do / still don't know:** concrete changes, dependencies, and cheapest next experiments.
7. **Short ending that earns the title**, if a narrative ending genuinely adds something; don't duplicate the executive summary.
8. **Methods, definitions, sources, and reproducibility** in a plainly labeled appendix.

For a short article, several parts can collapse into one. For a team memo, the decision table may precede the full story. If source material does not substantiate a dramatic arc, write a clear technical memo instead.

## How to work on a draft

**If given notes or raw research:** Extract the central question; build a claim/evidence/uncertainty inventory; find the *actual* surprising result; construct the causal arc; then write the title. Never decide on the twist first and retrofit evidence to it.

**If given an existing draft:** Preserve technical claims and the author's genuine turns of phrase. Identify the report's central question and strongest discovery. Reorder for narrative continuity, replace generic headings selectively, tighten paragraphs, and move details to tables or appendix rather than deleting evidence. Flag any factual inconsistencies separately instead of silently “correcting” measurements.

**If asked for titles:** Offer distinct mechanisms (contradiction, overlooked culprit, reversal, retrospective literary image), not ten superficial variants of the same formula. For each, state its intended payoff and whether the available evidence earns it.

**If asked for critique:** Evaluate separately: (1) accuracy and epistemic calibration; (2) central question and narrative continuity; (3) title/ending payoff; (4) readability and information hierarchy; (5) authentic humor and voice. Quote concrete passages and suggest targeted repairs; don't rewrite the author's personality out of the document.

## Final editing pass

Read once as a skeptical engineer: Can I reproduce the decisive result? Are strong claims scoped to the experiment? Were alternatives represented fairly? Could any number or chart mislead?

Read once as a busy teammate: Can I find the conclusion, impact, next action, risks, and owners within a minute? Are emergency findings impossible to miss?

Read once as a storyteller: What question pulls me onward? Does each section alter my understanding? Is the title more meaningful at the end than at the beginning? Did the humor arise from facts rather than a manufactured persona?

Finally, remove obvious AI fingerprints: repeated “not X, but Y” constructions, formulaic rhetorical questions, grand conclusions unsupported by data, filler transitions, excessive bolding, and a manufactured twist at the end of every section. Keep the few lines only this investigation could have produced.

**Success criterion:** A teammate remembers the discovery, understands the proof, knows what to do, and smiles once. The writing is memorable *because the engineering was interesting*.
