---
name: sol-luna-spark-router
description: Route Codex work with GPT-6.2 Sol as the default executor and integrator. Use for model choice, bounded delegation, or executing or resuming a Codex TrackWave plan. Luna and Spark are optional routes for narrowly specified tasks when supported.
---

# GPT-6.2 Sol Router

Start with GPT-6.2 Sol (`gpt-6.2-sol`) on the current task when the active surface supports it. The host owns the goal, acceptance criteria, coupled changes, and final verification. Keep those decisions and ordinary serial work together. Read [routing and model availability](references/routing.md) when resolving a route or launching work.

## Choose what to run

- **Plan only:** inspect inputs and describe the goal, acceptance, dependencies, and limits. Create a local plan when requested. Plan-only work leaves execution state untouched.
- **Execute or resume:** continue within the user's existing authorization. For a supplied TrackWave plan, use [the TrackWave adapter](references/trackwave.md) and preserve accepted evidence, unresolved runs, and remaining limits.
- **Ambiguous failure:** use `hypothesis-driven-closed-loop` to identify the cheapest discriminating probe before editing. Use `circuit-breaker` for a localized defect with a known cause. Use `wasted-time` before a costly run whose deciding boundary is still uncertain.

## Keep delegation conditional

Delegate only if intent, project policy, and the active surface allow it, there is a separable contract, and dispatch plus host verification is worthwhile. Prefer the smallest flat group of permitted workers. Keep tightly coupled work, shared write surfaces, and critical integration with one owner. Do not launch a worker merely to hand the only blocking step back to the host.

Use [the worker packet](references/work-packet.md) to hand off source, authority, evidence, acceptance, and remaining limits. A child does not inherit tools, context, or authority merely because it has a model label. Record the actual run ID and transport when dispatch succeeds.

If a task expressly requires GPT-6.2 Sol and the active route cannot provide it, preserve that constraint. Continue useful work that does not require that model. When Sol is a workflow preference and the current session is adequate, proceed with the available model and record its observed identity or uncertainty. Do not silently switch an explicitly requested model.

## Verify and recover

Review returned evidence and rerun the deciding check against integrated source. For causal repairs, verify the signal reaches the ordinary consumer and changes the expected behavior. A worker report, plan state, or model label alone does not establish that effect.

On failure, distinguish missing context, a semantic failure, a route failure, and source drift. Retry only when a changed packet, artifact, probe, or newly admitted route can address the specific blocker. Inspect an unresolved run before relaunching work with effects. Preserve validated independent work and report the route actually used, the acceptance observed, and the remaining gap.
