# Adaptive routing and launch surfaces

## Choose the smallest adequate route

Use this as an initial heuristic, then revise with comparable observed results. It is not a benchmark ranking.

| Work shape | Candidate | Route elsewhere when |
|---|---|---|
| Ambiguous architecture, coupled changes, contradictory evidence, difficult integration decisions | Sol | Work can be reduced to an explicit, cheaply checked contract |
| Clear bounded implementation or analysis, extraction, test specification, structured reconciliation | Luna | Essential decisions remain unresolved or failures expose a reasoning gap |
| Small code proposal, local transformation, focused test or fix with executable acceptance and compact context | Spark | Required context/tools/modality are unavailable, or repair costs exceed the saved latency |

Sol is not required to plan a trivial job. Luna is not required between Sol and Spark. Spark is not a universal first attempt. Favor local serial execution when packaging and reconciliation would cost more than the work. For uncertain but decomposable workloads, try one representative permitted lane and use its measured validation/repair cost before increasing fanout; do not turn this into a compulsory preliminary benchmark.

When Sol is the actual admitted coordinator, `Sol → {Luna, Spark} → Sol` is a useful candidate: send each worker a direct complete assignment and return both outputs to Sol for contract review and integration. This avoids an unnecessary relay but does not establish a latency, cost, or quality advantage. A successful Sol-led repair of one nested run supports trying this topology, not claiming a matched comparison already proved it. If the user asks to measure the advantage, hold workload, acceptance coverage, and resource rules comparable and retain original and repaired scores separately.

Risk, ambiguity, coupling, context completeness, validator strength, and observed failure cost matter more than line count. A short security-sensitive function can require Sol-level judgment; a large mechanical transformation can remain bounded. Model choice never substitutes for independent acceptance checks or required human authority.

Choose a supported reasoning effort appropriate to the work; do not maximize every stage. Compare expected worker time plus dispatch, validation, and likely repair cost qualitatively when data is missing. Do not invent numeric success probabilities, throughput, prices, or token savings.

## Bind names to available models

The requested family resolves to these explicit IDs when the selected surface supports them:

| Name | Model ID |
|---|---|
| Sol | `gpt-5.6-sol` |
| Luna | `gpt-5.6-luna` |
| Spark | `gpt-5.3-codex-spark` |

Verify availability and supported reasoning settings from the actual dispatch tool or current client, not from the generic API catalog alone. Never replace these with Terra, Astra, a similarly named model, or a third-party provider without applicable user authorization and policy admission. Explicit use of this skill requests this model family for the assigned work, not every model on every task.

Official [Codex model guidance](https://developers.openai.com/codex/models/) supports the broad Sol/Luna task distinction and describes Spark as a text-only, low-latency coding model. Access and surface support can change. Recheck the official page for capability questions not answered by the current tool. Do not assume that a model available in the desktop task picker is accepted by the native subagent tool, or that Spark has ordinary API access.

## Choose a permitted transport

- **Native subagents:** prefer the active task's collaboration tools for bounded subtasks when available. Follow their advertised model list, inheritance rules, concurrency, and lifecycle semantics. In clients where full-history forks disallow model overrides, use a fresh or supported bounded-history context plus the complete packet. Never claim inherited history is a clean experiment.
- **Existing desktop tasks:** continue a task only when the user placed that task in scope for continued work. Inspect its current state before sending a message, since the message can start a turn. Preserve model settings unless an authorized route change is intended.
- **New desktop tasks:** use task creation only when the user explicitly requests new user-visible tasks. A request for workers, speed, or a model cascade is not that request. Resolve the project and supported environment first, and wait for setup IDs to become usable task IDs.
- **Codex CLI or another runner:** use only when available, authorized, and admitted by project policy for that transport. Inspect its current help and model support before constructing a command. Bind cwd/base, permissions, model, packet, output destination, and process/run ID; supervise termination. A model missing from the native tool can use a separately admitted transport, but a runner must not bypass a model/policy denial, approval, or platform restriction. Do not install one or alter auth merely to make the launch possible.

If the exact route is unsupported, distinguish `model_unavailable`, `transport_unavailable`, `policy_denied`, `quota_unavailable`, and `capability_mismatch`. Continue independent admitted work when useful. For an indispensable blocked step, state the precise missing route/authority and ask for the necessary choice; do not report the entire cascade as launched.

## Bound adaptation

Use the user's limits narrowed by the effective policy. If no policy supplies limits, choose and announce a finite task-proportional wall-time, concurrency, and attempt envelope before dispatch; record these as host-selected limits, not policy facts. Do not reserve imaginary token balances. Count all nested workers and retries against the parent envelope and leave time for validation/integration.

- **Context/schema defect:** supply the missing original contract or correct the packet; increasing model size alone does not fix missing input.
- **Semantic defect:** pass the actual failed checks and relevant artifact slice through the admitted retry path. If repeated errors show a capability mismatch, propose or admit a stronger eligible route rather than repeating the same prompt indefinitely.
- **Tool/transport/quota failure:** resolve the existing attempt first. Retry or reroute only if policy and current observations allow it; an unknown result must not cause duplicate writes.
- **Base or interface drift:** invalidate only affected downstream work, refresh the packet revision, and rerun its acceptance check.
- **Uncheckable or contradictory requirement:** resolve the contract with the host or user. Do not cycle models until one asserts success.

Escalation is conditional, not a fixed Spark → Luna → Sol ladder. Stop when the applicable retry/deadline limit is reached, no new evidence supports another attempt, authority is missing, or the expected remaining cost no longer fits the envelope. Keep validated independent work.
