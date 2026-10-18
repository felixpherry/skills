---
name: run-arena
description: "Runs several agents at the same task in parallel, picks the strongest attempt as a base, and grafts the best parts of the others into it. Use for 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
metadata:
  based-on: "arena from pstack by Lauren Tan, via michael-denyer/pstack-claude (MIT)"
---

# Arena

Track the six phases (Frame, Fan out, Cross-judge, Pick, Graft, Verify) as a todo list, if you have one, before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick the runners. Default to three subagents on your current model, or the models the caller names. If the `Agent` tool rejects a model, use the closest valid one from its error message and say so. Spawn more runners when the arena covers several design directions; if the task is ambiguous, turn each reading into its own direction instead of stopping to ask. Use the same model N times when the work is generation-bound rather than judgment-sensitive.
4. Give each candidate its own output location: a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`. Never let two candidates write to the same file, branch, or folder. In orb, a candidate that needs its own running app or a long session can run in its own orb session through the hand-off skill instead of as a subagent, reporting back to your pane.

## Phase B: Fan out

Spawn all N subagents in one message with `run_in_background: true`, each with the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all Phase B candidates complete, spawn one read-only judge subagent. Use a different model from yours when the caller named one or one is available; otherwise your own. It sees the rubric and the candidates by path label, scores each criterion, and recommends a base with rationale. It runs in parallel with your reading in Phase D. Don't spawn it while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API: the smallest shape that solves the problem.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, as if the base had been designed with it from the start, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact against the real thing: run it, read the actual output, inspect the diff. A candidate's or the judge's report is not proof. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
