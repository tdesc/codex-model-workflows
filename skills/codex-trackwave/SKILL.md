---
name: codex-trackwave
description: Create, inspect, or resume a local plan when work has dependent waves or needs durable progress. Use for standalone Codex scheduling, attempt history, and verifiable acceptance across interrupted sessions.
---

# Codex TrackWave

Use TrackWave for real dependency boundaries or a need to resume. Keep a single serial change in the current task unless the user requests a plan. The local JSON helper records state. The host executes authorized work and checks evidence.

## Plan or resume

For an existing `codex-trackwave/v1` state file, run `status` and preserve its IDs, attempts, and accepted evidence. For another plan format, follow [the import procedure](references/local-plans.md). If a selected state file is unreadable, investigate it before creating new state.

For a new goal, group work into waves only at actual dependency or integration boundaries. Define each item's acceptance, dependencies, read/write scope, and route preference. Add a discriminating probe before an ambiguous repair when its result determines the next item. Use [the example spec](assets/plan.example.json) and replace its illustrative values with the actual goal, source, authority, and limits. The bundled Python 3.10+ helper uses the standard library. Resolve `scripts/trackwave.py` relative to the skill and save the plan outside the installed skill.

## Execute and accept

`status` shows the earliest incomplete wave, ready items, and unresolved runs. Check source freshness, overlapping effects, route availability, and time before reservation. Prefer the current GPT-6.2 Sol session when it fits. Use `sol-luna-spark-router` when a model-selection or delegation decision actually matters. The plan's route field is a preference and its presence does not grant execution authority.

Keep one host responsible for updates. Use `reserve` before work, `bind` with an observed worker ID or current-task reference for host execution, `return` with the artifact, and `accept` after host validation. For a causal repair, record the normal-path observable and its control when applicable. For other work, record the declared acceptance check. The next wave becomes eligible once earlier items are accepted. See [the exact commands](references/local-plans.md).

## Recover and finish

On interruption, resolve `reserved`, `running`, and `returned` entries before retrying affected work. A lost launch response or timeout leaves execution uncertain. Preserve prior attempts and acceptances. On source or acceptance drift, use the explicit successor procedure in the reference.

Report accepted items, the active wave, unresolved runs, and the important evidence. Plan acceptance records host verification. Publication, runtime deployment, and product effects have their own observations.
