---
name: wasted-time
description: Prevent low-information work from scaling into expensive loops. Use when a task, experiment, simulation, test wave, provider call, or repeated retry is taking too long; when the user asks to fail fast or optimize for time; or before a costly wave whose critical causal link has not yet been demonstrated. Do not use to weaken required safety, provenance, or acceptance evidence.
---

# Wasted Time

Stop the attempt that has stopped teaching you; do not abandon the user's
outcome merely because one route failed.

## Write the stop contract first

Before an expensive action, state a compact contract:

`decision sought | cheapest falsifier | progress signal | wall/domain budget | trip condition | scale condition`

- The **decision sought** is what this run can change, not the whole project.
- The **cheapest falsifier** exercises the earliest uncertain causal boundary.
- The **progress signal** must be observable during or immediately after the
  run. A process being alive, producing logs, or accumulating samples is not
  progress by itself.
- Record both wall time and the domain clock when they differ, such as
  simulator time, provider latency, queue time, or test duration.
- A trip condition ends the current attempt. It does not authorize dropping
  the requested outcome or skipping required proof.

If no observable canary can distinguish success from failure, instrument that
boundary before running the costly wave.

## Prove that the path can be active

For a path guarded by several conditions, inspect one receipt, replay, trace,
or static truth table and prove that the gates have a non-empty joint window.
Record the first blocking predicate and its time range.

Do this before collecting a large corpus or launching paired evaluations. A
model that predicts well offline but is never admitted to the owning runtime
path is unwired evidence, not a candidate worth scaling.

Check at least:

- the proposed signal reaches the actual owner of the effect;
- every independent gate can be true at the same time;
- the action is early enough to affect the measured terminal outcome;
- the receipt distinguishes requested, admitted, executed, and observed;
- source/config/checkpoint compatibility is exact.

## Run one canary, then decide

Use the smallest representative case and the shortest budget that still lets
the hypothesis succeed. Prefer an existing immutable receipt or replay before
a new live/runtime call.

After the canary, make exactly one of these decisions:

- **scale** — the effect was executed, changed the intended observable in the
  predicted direction, and stayed inside safety and provenance bounds;
- **repair** — the earliest causal divergence is localized and yields one new,
  falsifiable source hypothesis;
- **stop** — the path was silent, unwired, repeatedly blocked, or no longer
  changes the decision.

Do not launch a full wave merely because unit tests pass, a checkpoint loads,
an offline metric improves, or a gate says `eligible`. Require observed effect
at the owning boundary. After a negative canary, a retake is justified only by
a concrete change that should move the first divergent observable.

## Trip the attempt

Stop or interrupt the current attempt when any applies:

- the explicit wall/domain deadline is reached;
- the progress signal is flat for the preregistered window;
- two attempts return the same blocker without a new source-backed hypothesis;
- required gate intervals do not overlap;
- output cannot affect the target owner or terminal metric;
- source/config drift invalidates the active frozen wave;
- the user changes the objective or asks to stop.

Preserve completed receipts and partial diagnostics. Do not delete evidence to
recover time, silently extend a budget, or treat a timeout as proof that the
underlying condition is false.

## Scale only after the canary

Freeze the full manifest after the causal path works in a representative
canary and before candidate fitting or comparative evaluation. Scale in the
smallest wave that can meet the statistical or coverage requirement. Parallel
work is useful only when each lane has its own bounded question and cannot
multiply the same unverified assumption.

Keep acceptance metrics distinct from leading indicators. Faster approach,
lower prediction error, or more contacts can justify the next experiment, but
cannot substitute for a required grasp, transaction, deployment, or other
terminal result.

## Report time honestly

End with:

`attempt | decision | wall time | domain time | useful evidence | avoidable work | first blocker | next smallest action`

Call work *saved* only when a tripped canary prevented a larger action or a
measured bottleneck became shorter. Never hit a time target by weakening hard
safety, approval, provenance, family separation, rollback, or terminal
afterstate requirements.
