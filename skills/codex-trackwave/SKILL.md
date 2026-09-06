---
name: codex-trackwave
description: "Create, inspect, and resume local TrackWave plans in standalone Codex, with dependency-aware waves, attempt history, and evidence for accepted work. Use for durable multi-step planning with or without Sol Luna Spark Router; no Colony runtime is required."
---

# Codex TrackWave

Plan work in ordered waves and preserve its execution state in a local JSON file. This is a standalone file format and helper, not a client for a remote planner. It works in any project with Python 3.10+ and the standard library. The helper records state; Codex performs authorized work and checks the evidence.

## Plan or resume

For an existing `codex-trackwave/v1` state file, read it and run `status`; retain its IDs, attempts, and accepted artifacts. For a supplied plan in another format, read [references/local-plans.md](references/local-plans.md) before deriving a local plan. Do not silently create a replacement for an unreadable existing plan.

For a new goal, inspect the relevant material and define checkable work items. Group them into only the waves that reflect real join points. Each item needs dependencies, acceptance criteria, read/write scope, and a candidate route; tightly coupled work stays together. A one-step job can stay in the current task without a persisted plan.

Use [assets/plan.example.json](assets/plan.example.json) as the shape, replacing its illustrative content with the actual goal and boundaries. Choose finite attempt/concurrency limits from the task and available platform capacity. Record the user's existing authorization and deadline in the spec; these fields document context and do not grant permission or enforce a clock.

Read [references/local-plans.md](references/local-plans.md) for commands and transitions. Resolve `scripts/trackwave.py` relative to this installed skill, and use the project's Python launcher when one is prescribed. Store the plan in a task-appropriate artifact directory, outside the installed skill folder.

## Execute ready work

`status` reports the earliest incomplete wave, dependency-ready items, occupied slots, and unresolved runs. The host chooses from ready items after checking route availability, source freshness, ownership hazards, and remaining time. `reserve` claims a slot before dispatch. `bind` records the actual run ID after dispatch. One host owns plan updates; workers return results to it.

Use `sol-luna-spark-router` when installed and model routing is useful. Pass plan ID/revision, wave/item ID, the full item contract, accepted dependency evidence, and remaining limits. Without that skill, perform the ready work directly using the current Codex session or an already authorized available worker surface. Model names in a plan are preferences, not availability proof. No new user-visible tasks are required.

Record returned artifacts with `return`. Verify the full contract, inspect actual output, and run appropriate checks before recording `accept` with evidence. The helper requires an evidence reference but cannot establish its truth. The next wave becomes eligible only after all items in the earlier wave are accepted. Acceptance and Git publication or deployment remain independent observations.

## Recover and finish

On interruption, inspect `reserved`, `running`, and `returned` entries first. A reserved entry may correspond to a dispatch whose response was lost; recover that attempt before launching another. A timeout does not prove termination. Record `fail` only after resolving the old run, then retry within the existing attempt limit. Keep all prior events.

For source/contract drift, stop affected work and follow the explicit successor-plan procedure in the reference. Do not overwrite accepted history or silently reset attempt limits. Only the host schedules new work; the helper does not launch models, run commands from a plan, enforce wall-clock termination, or monitor in the background.

Report accepted items/total, active wave, unresolved runs, evidence and remaining action. A completed plan means every item's acceptance was recorded by the host. State whether those checks were reproduced, inspected, or only reported.
