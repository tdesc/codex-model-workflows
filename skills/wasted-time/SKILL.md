---
name: wasted-time
description: Bound expensive tests, simulations, provider calls, and repeated retries with a representative canary and an explicit scale, repair, or stop decision. Use when the user asks to fail fast or a costly wave depends on an unverified causal path.
---

# Wasted Time

Before spending the budget, write one line:

`decision | cheapest falsifier | progress observable | wall/domain budget | trip condition | scale condition`

Choose the earliest uncertain boundary that can change the decision. Where several gates must align, inspect one representative trace or truth table to see whether they can all hold for the same case, input, source, and time. Prefer existing evidence when it exercises the same path. If no useful progress observable exists, make it observable within the task's authority before launching the expensive run.

Run the smallest representative canary and choose one action:

- **Scale** when the owning boundary produced the predicted effect and the promised acceptance conditions still apply. Use the smallest wave that meets coverage and freeze inputs for comparisons.
- **Repair** when evidence identifies a specific divergence and a changed input, source, or probe can distinguish the next mechanism. Use `hypothesis-driven-closed-loop` when several causes remain credible.
- **Stop the attempt** when its budget is exhausted, the progress signal is flat for the agreed window, or another attempt would repeat the same evidence. Preserve accepted work and continue any useful independent route already in scope.

A ready gate, green unit test, offline score, or running process can justify a probe. Scale only from evidence at the owning boundary. Keep leading indicators and terminal acceptance separate. Preserve the agreed budget and acceptance when switching routes. A timeout establishes elapsed time, so inspect the actual run state before retrying mutations. Keep wall time and the domain clock separate when they differ.

Report the decision, observed effect or first blocker, measured time, and next useful action. Claim time saved only when a larger action was avoided or a measured bottleneck improved.
