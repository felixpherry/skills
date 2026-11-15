# Skeletons by doc type

Heading numbering and the TL;DR rule are in SKILL.md under "Every doc".

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
