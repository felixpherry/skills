---
name: explain-how
description: "Explains how code works: architecture, runtime flow, and where things live, at the level of a senior engineer onboarding onto a subsystem. Use for 'how does X work', a walkthrough before changing something, or placement questions ('where should this live', 'which package owns this', 'is this the right layer'). For why it was built that way, use explain-why."
metadata:
  based-on: "how from pstack by Lauren Tan, via michael-denyer/pstack-claude (MIT)"
---

# Explain how

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Every spawn is a general-purpose subagent on the model you run on, told to read only and never edit. If you can't spawn subagents, do the same steps yourself in order.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Spawn all explorers in a single message, each with `references/explorer-prompt.md` and its angle filled in.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

If the user's own instructions (CLAUDE.md, AGENTS.md) set a writing style, reshape the output to follow it without changing what it says. If they say to show long or visual explanations as a page, do that.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
