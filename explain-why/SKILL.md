---
name: explain-why
description: "Finds why code is the way it is. Use for 'why does X work this way', design rationale, regressions, or where a threshold came from. For how code runs, use explain-how."
metadata:
  based-on: "why from pstack by Lauren Tan, via michael-denyer/pstack-claude (MIT)"
---

# Explain why

Find the forces that led to the code's shape. explain-how covers what the code does.

Every spawn is a general-purpose subagent on the model you run on, so it keeps its MCP tools: investigators need them, and so do the synthesizer's citation spot-checks. Investigators write nothing. If you can't spawn subagents, do the same steps yourself, one source at a time.

Say what you know apart from what you infer. The confidence tiers and their phrasing are in `references/epistemics.md`.

## 1. Pin down the target and the question

The target is code, a pattern, a feature or a named decision. If it's vague ("why do we do it this way?"), take your best guess from the conversation (open files, recent edits, what was just discussed), state it in a line so the user can redirect, and go on.

## 2. Build the code anchor

Run `scripts/anchor.sh <file> [<start> <end>]` from this skill's folder, once per target file, with the repo as the working directory. It prints the last-touch commits for the range, the last 20 commits through renames, the PR numbers and ticket keys in their messages, and each PR's body, comments and reviews (five PRs at most; `ANCHOR_MAX_PRS` changes that).

Add the key symbols (functions, classes, constants). The anchor goes to every investigator and to the synthesizer.

## 3. Spawn investigators in parallel

**Default to the full search.** The goal is a complete coverage map: document a null result, don't skip the search.

List the MCP servers you can call. In Claude Code they are tools named `mcp__<server>__<tool>`, including deferred ones listed only by name; otherwise read `.mcp.json` or run `claude mcp list`. A CLI that reaches the same source counts. Map each to one category by its name, server instructions and tool names. If one fits two categories, pick its primary evidence and note the ambiguity in the coverage map.

| Category | Examples | Best at |
|---|---|---|
| Source control | git, `gh`, code comments, tests | Rationale captured at review time. Always spawn; the only guaranteed source. |
| Issue tracker | Linear, Jira, GitHub Issues | The product or business reason, when the why is outside engineering. |
| Long-form documents | Notion, Confluence, Google Docs | Design rationale written before the code. |
| Team chat | Slack, Discord, Teams | Deliberation that never reached a doc, when the paper trail is thin. |
| Infrastructure observability | Datadog, Grafana, Honeycomb | The runtime signal the code reacts to: timeouts, retries, rate limits, circuit breakers. |
| Error tracking | Sentry, Rollbar, Bugsnag | The exceptions behind catch blocks, null guards and other defenses. |
| Analytics warehouse | Databricks, Snowflake, BigQuery | Flag-gated code, experiments, data migrations, "where did this number come from". |

Spawn one investigator per category that has a source, all in one message, each owning exactly one tool or MCP. Each prompt is `references/investigator-prompt.md` filled in, plus:

- the playbook `references/sources/<source>.md` for that MCP, or one adapted from the examples in `references/source-playbook.md`;
- `references/sources/incident-postmortem.md` if the target looks defensive (null checks, retries, timeouts, rate limits, feature flags, egress guards, OOM handlers);
- the code anchor and the user's original question.

**Skipping a category needs a written reason,** which goes in Sources Consulted. Two are valid:

- **No source for it here.** A gap, not a choice: "Team chat skipped. No matching MCP, so the conversational record was not searchable."
- **Provably irrelevant,** not probably: "Error tracking skipped. The target is a build-time script with no runtime path."

You may answer inline, with no investigators, only for a single-commit target whose PR description holds the complete answer, and only after confirming each available category would add nothing. Say so. This is rare.

## 4. Synthesize

Spawn one synthesizer with `references/synthesizer-prompt.md` filled in: the investigators' findings (nulls and justified skips included), the code anchor, the question, and the framework from `references/epistemics.md`.

## 5. Present

Present the synthesizer's output. Edit lightly for clarity, but leave the confidence language as written. If the user's instructions set a writing style or ask for a page, reshape to fit, keeping the tiers and citations.

The sections are the synthesizer prompt's: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Sources Consulted has one line per category, including the empty and the skipped, with the reason.

If the question is a step toward changing this code, add a Preserve / Change / Avoid / Risk list drawn from the findings.

**Watch for recency bias.** The latest commit is rarely the whole reason; the current shape is often many earlier decisions stacked up. Trace back.
