---
name: sol-luna-spark-router
description: "Plan and launch work across Sol, Luna, and Spark in standalone Codex, with local Codex TrackWave plans or a plain goal. Use for adaptive orchestration and bounded execution; no Colony services are needed."
---

# Sol Luna Spark Router

Turn a goal into verifiable work, using Sol for difficult judgments, Luna for well-specified work, and Spark for focused coding iterations when those routes are admitted. These are initial routing preferences, not a mandatory three-stage chain or a claim that a model will succeed. Optimize time to an accepted result, including dispatch, validation, and repair overhead.

This standalone edition uses the current Codex tools, project instructions, and optional local `codex-trackwave` companion. It has no server, passport, quota-treasury, or Colony-policy dependency. If the project has its own policy, honor its actual scope without requiring that policy in other projects.

## Select the work mode

- **Plan only:** inspect inputs and produce assignments, dependencies, route choices, validation, and limits. Create a requested local plan artifact, but do not launch workers or advance its execution state.
- **Execute or resume:** execute the work the user authorized, preserving existing acceptance criteria, completed work, and effect boundaries. A plan is not implementation authority. Writing or reviewing this skill does not itself request a live cascade.
- **Existing TrackWave:** read [references/trackwave.md](references/trackwave.md). Resume a local plan or map the supplied external export without contacting its original service.
- **No TrackWave:** keep a simple task in the current conversation. For multi-wave work or durable resume, use `codex-trackwave` to persist the goal, dependencies, acceptance, ownership, and attempts locally. If the companion is not installed, use the same compact fields in a local document or the task; report that automatic transition checks are unavailable.

Resolve ambiguous scope from the supplied material first. Ask only for a choice or authority that actually changes execution. Announce the selected mode and topology before launching.

## Plan around the critical path

Inspect the relevant source and define acceptance before splitting work. Keep tightly coupled changes with one owner. Parallelize only independently useful lanes with non-overlapping effects and a clear join check; include read/write hazards, not just duplicate writes. Assign each expensive test surface one owner.

The current host owns scope, architecture, admission, integration, and the final claim. Do not call it Sol unless its execution metadata supports that identity. If the requested model cannot handle the host's required step through a permitted surface, report the mismatch instead of silently relabeling another model.

For routing criteria, model IDs, supported dispatch surfaces, and failure handling, read [references/routing.md](references/routing.md) before dispatch. The normal shape is a flat host with bounded workers. Use Sol → Luna → Spark nesting only when a real intermediate decision or coordination job saves work and the platform and project policy admit it. The host can dispatch Spark directly from a Luna proposal; label that actual topology honestly.

## Admit and dispatch

Before each launch, intersect user intent, project policy, platform availability, required capabilities, observed quota, and the remaining time/resource envelope. Explicit model preferences do not override a denied route. Do not edit governance or global model configuration to make a route pass.

Use the selected platform's supported models/transports and applicable project instructions. When no project routing policy exists, choose a finite host-managed envelope and record route decisions directly. Unknown quota is unknown; it does not require installing a quota service. If a configured policy requires a specific observation or denies a route, resolve that constraint before dispatch. A local plan reservation only prevents overscheduling; it does not certify model access or grant external-action authority.

Before sending work, read [references/work-packet.md](references/work-packet.md). Send a complete bounded assignment, not a reference to unspecified parent history. Children have no implicit authority to delegate further. Start only the ready lanes permitted by the envelope, while the host continues distinct useful work. Do not spawn a sidecar for the sole blocking action when the platform requires independent parallel work.

The result of planning is a candidate route. The result of dispatch is an observed child/run ID. Neither is completed work. Keep requested and configured models separate from provider-attested identity, and record transport changes.

## Validate, adapt, and close

Validate returned artifacts against the assigned acceptance check and source snapshot before integrating. Proposal-only workers must not apply changes or execute commands; the authorized host performs those steps. Under a policy permitting worker edits, enforce the assigned ownership boundary. Recheck accepted worker output after host reconciliation.

On failure, classify missing context, invalid output, semantic failure, transport/quota failure, or integration drift. Repair the failed slice, not the entire wave. Reroute only through fresh admission and within the remaining envelope; do not reinterpret a semantic retry as permission to switch providers. Keep the original failure and later repair as separate attempts.

Use the platform's wait/cancellation mechanisms with bounded waits. A parent timeout is not proof the child stopped. Resolve existing run IDs before redispatching potentially mutating work. Stop new dispatch at the deadline or exhausted budget; preserve useful results and report any still-running work accurately.

Finish with the outcome, actual topology, accepted versus rejected/unvalidated items, checks performed, elapsed wall time, and blockers. Include exact plan/wave bindings when present. Record measured usage only; do not promise savings from model labels or separate quota pools. For post-run comparison, use `agent-session-audit` when available, without requiring an audit ritual for every run.
