---
name: circuit-breaker
description: Stop narrow implementation tasks from turning into prolonged diagnostic loops; use for a small fix, targeted validation, or explicitly requested PR.
---

# Circuit Breaker

Use when the requested outcome is small and concrete: one visual defect, one
localized bug, a focused test failure, or packaging an already-understood fix
as a PR. Do not use it for genuinely broad investigations, high-risk changes,
or when the user explicitly asks for deep research.

## Define the delivery point first

Before inspecting, name the closest requested outcome: local patch, visible
preview, commit, or open PR. Do not infer a later publication step. State no
more than three observable conditions that prove that outcome.

For a visual microfix, the default proof is:

1. The source rule causing the defect is identified.
2. One targeted before/after browser check shows the requested geometry or
   behavior.
3. The changed source has a focused syntax or diff check.

For an explicitly requested PR, add only the normal packaging proof: exact
staged paths, a focused check, current base comparison, push, and the observed
PR URL.

## Work in one hypothesis loop

- Form the smallest source hypothesis before browsing or running a suite.
- Once one observation confirms it, patch it. Do not keep gathering evidence
  that will not change the patch.
- Run one targeted validation. Run a second only when the first reveals a new,
  source-backed failure.
- For stale browser state, use one cache-busted reload or fresh page; do not
  repeatedly sample the same cached scene.
- Preserve unrelated files and stage only the intended paths. Untracked
  diagnostics need not be cleaned merely to open a scoped PR.

## Timebox and trip condition

Treat five minutes as the default budget for a focused local fix, plus ten
minutes only when the user explicitly requested commit/push/PR packaging.
These are decision boundaries, not excuses to stop early.

Trip the breaker when either condition holds:

- two validation attempts produce no new source hypothesis; or
- the budget is exceeded without a user-visible deliverable or an external
  blocker.

When tripped, stop optional searches, visual polish, agent/runtime rituals,
and broad test runs. In the same turn either deliver the best verified result
within existing authority or report the single concrete blocker and ask for the
needed decision. Say what is finished and what is not; never imply that a
local patch, a commit, a push, a PR, and a release are the same state.

## Keep process proportional

Do not turn a static-site or CSS microfix into a Colony runtime audit,
Collective call, release lane, or multi-agent task unless the request depends
on that system or a required repository gate blocks delivery. Follow mandatory
repository hooks and ownership rules once; a stale ownership claim is a
packaging blocker to resolve, not a reason to restart discovery.

For a PR, user authorization is still required for commit, push, and PR
creation. After the PR URL is observed, stop unless the user asks for checks,
review, merge, or release.
