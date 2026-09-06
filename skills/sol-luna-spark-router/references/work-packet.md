# Worker packet and integration record

Use a compact structured prompt or artifact, not a new mandatory runtime schema. When project policy defines a ContextPacket, use that schema and bind these meanings to it instead of creating a rival format.

## Before dispatch

Include the fields that apply, with unavailable observations explicit:

```text
Identity: task/lane ID, attempt ID, parent/run reference, packet revision.
Goal: exact bounded outcome and why it is needed.
Source: repository/cwd, base SHA or artifact revision, relevant files/ranges.
Input: complete required schema, invariants, constraints, sample edge cases.
Dependencies: accepted upstream output IDs/digests; no assumed parent memory.
Scope: allowed reads/writes/tools, forbidden effects, proposal-only or edit mode.
Route: selected model/effort/transport, admission evidence, fallback eligibility.
Limits: remaining deadline/attempt/resource allowance and stopping condition.
Validation: host acceptance command or rubric and who may execute it.
Return: artifact/patch or evidence refs, checks actually run, residuals/status.
TrackWave (if present): project, plan, revision, wave and work-item mapping.
```

An accessible source pointer can replace copying a large file only if the child has permission and tools to read it. For a context-read-only route, send the necessary source in the packet. Do not write “follow the original schema” without delivering that schema. If context exceeds the limit, reduce the lane or shard at a valid contract boundary; do not silently truncate the definition of success. Exclude secrets, private reasoning, and unrelated transcripts.

Nested delegation is disabled unless the host explicitly admits a coordinator lane with child scope, total concurrency, budget, permitted routes, and join criteria. No child may mint its own authority or increase the parent envelope.

## Validate the actual output

First verify lineage, scope, and shape. Then validate semantics with the assigned tests or evidence rubric; for code, inspect the patch and exercise the relevant behavior when authorized. A syntactically valid JSON answer is not semantic correctness. A worker's “passed” is a report until the host observes a usable check receipt or reproduces the check.

At the final join, compare the implementation and test coverage to the full declared contract, not just the existing grader's assertions. Check declared input abstractions and edge cases: a contract accepting a mapping is not necessarily satisfied by code that only handles a built-in dictionary. A maximum grader score proves that suite passed, not complete correctness. Add a focused missing-contract check when authorized; if it exposes a defect, keep the original grader result and the new failure visible rather than silently redefining the earlier score. Apply the same coverage review after repairs, since a fix can introduce a different regression.

For non-executable work, use inspectable sources and an explicit acceptance rubric. Do not fabricate an executable validator to satisfy a policy; if policy requires one, that lane cannot be admitted without it. Review may establish a narrower accepted result than runtime testing.

Review integration changes against the original acceptance criteria. A correct proposal can become incorrect during reconciliation. Record changes applied by the host separately; do not attribute the integrated result entirely to a worker whose output was edited.

## Preserve enough evidence to resume

Keep a compact record in the task or an authorized artifact location:

`lane | dependencies | packet_revision | requested/configured_model | transport | child/run_id | attempt | status | artifact | validation | integration | elapsed | residual`

Store start/end and per-attempt outcomes when available, including failure and repair. Use declared dependencies to identify what must be redone after input drift. Do not sum overlapping durations as wall time or cumulative usage snapshots as token consumption.

On interruption, first inspect known run IDs and existing outputs. Resume from observed accepted artifacts, not the latest narrative summary. Keep `planned`, `dispatched`, `returned`, `validated`, and `integrated` distinct. Git publication and live deployment are separate, independently authorized and observed states.

If a scratch path disappeared, check referenced repository reports or saved output artifacts before declaring evidence lost. Distinguish a preserved historical report, a recovered implementation, and a freshly reproduced check; none automatically establishes the others.
