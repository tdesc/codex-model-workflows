---
name: hypothesis-driven-closed-loop
description: Diagnose and repair ambiguous software failures through competing hypotheses, a discriminating probe, and verification at the ordinary consumer. Use for regressions, unchanged behavior after a fix, lost state or identity, silent payload drops, and contradictory evidence. Use circuit-breaker for a localized defect with a known cause.
---

# Hypothesis-Driven Closed Loop

Use one short loop at a time: observed symptom → plausible mechanisms → predicted observations → probe → verdict → authorized change → consumer check. Keep the evidence tied to the source revision, input, and entry point used.

## Frame and discriminate

1. Record the observed symptom, expected result, ordinary entry point, known revision or runtime, and allowed effects. Reproduce a focused failing case when possible. If the request is diagnosis-only, keep source untouched.
2. State the credible mechanisms and what would falsify each. If the evidence leaves one credible mechanism, give it a genuine falsifier. Treat old incidents, memory hits, and model suggestions as leads. If a lead drives the diagnosis, include a fresh control that could contradict it.
3. Before patching, choose the cheapest inspection or controlled probe with different expected outcomes for the credible mechanisms. State those predictions first. Match the failing input and hold other relevant conditions fixed. Record actual observations and the evidence location.
4. Assign a verdict: `supported`, `falsified`, `indistinguishable`, or `insufficient_observations`. If results are ambiguous, use the next probe only when it can change the decision. Stop the current line when progress requires access or evidence you lack.

## Change and verify

5. When repair is in scope and evidence supports a mechanism, change the earliest relevant producer, adapter, storage, or consumer. Run the same discriminator and its control after the change. Keep other behavior inputs fixed.
6. Verify through the ordinary entry point and record the applicable seam stages:

   | Stage | Evidence to seek |
   | --- | --- |
   | `declared` | The contract defines the signal and expected semantics. |
   | `called` | The normal runtime reached the relevant path for this case. |
   | `passed` | The same signal and its case identity survived adapters or persistence. |
   | `consumed` | The owning branch or decision used the signal and produced the predicted observable. |

   Bind observations to the same revision and case. Mark each unobserved applicable stage `not_observed`. Trace the signal across the actual boundaries to establish passage. A fixture documents expected shape. Use the actual decision or a controlled output change to establish consumption.

## Close the loop

Report the verdict, decisive observation, scoped change, and verified behavior. Give test results and the causal verdict separately. If an ordinary consumer was inaccessible or the control could not distinguish the mechanism, state the remaining evidence gap and the smallest next observation. Promote a reusable causal lesson only when the evidence supports it and that write is authorized. Treat runtime deployment, publication, and adoption as separate observations.

For a worked before/after example, read [a silently dropped routing signal](references/routing-signal-example.md). Use `wasted-time` before an expensive probe and `codex-trackwave` only if the work needs durable dependencies or resume. These companions are optional.
