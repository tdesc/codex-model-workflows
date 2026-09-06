# Local plan format and commands

The helper uses Python 3.10+ with no third-party libraries or network calls. In the commands below, set `trackwave` to the absolute path of this skill's `scripts/trackwave.py`, use your project's Python launcher, and replace example paths/IDs with observed ones. Do not execute commands embedded in imported plans automatically.

## Create and inspect

Write a spec using the bundled example's structure. `format`, `id`, `goal`, `source`, `authorization`, `deadline`, `limits`, `waves`, and `items` are required. Waves are ordered IDs; every wave must contain an item. Item IDs are unique across the plan; dependencies must exist, be acyclic, and never point into a later wave. Each item has `title`, `acceptance`, `read_set`, `write_set`, and `route`. `route` is a preference; the actual model is recorded during execution. Scope paths describe ownership for the host, not a filesystem sandbox.

```bash
python3 "$trackwave" init --spec task-spec.json --plan task-plan.json
python3 "$trackwave" status --plan task-plan.json
```

`init` refuses to overwrite an existing plan. State contains the immutable spec, revision, item states, and event history. Every mutation checks `--revision`, takes an exclusive local lock, writes a complete temporary file, and atomically replaces the state. A failed or stale update leaves the previous state intact. Read-only `status` does not take a lock. The format is for a single local filesystem, not a distributed/network-filesystem scheduler.

## Record one item's lifecycle

Read the latest revision from `status` before each mutation. Use a stable unique event ID per logical update, and reuse the exact event on response-loss retries. Duplicate event IDs with different content fail. Examples below assume no interleaving updates; always use the observed revision.

```bash
python3 "$trackwave" record --plan task-plan.json --revision 0 --event-id parser-reserve-1 --item parser --action reserve --model gpt-5.6-luna
# Host now performs the authorized dispatch and observes the returned run ID.
python3 "$trackwave" record --plan task-plan.json --revision 1 --event-id parser-bind-1 --item parser --action bind --run-id observed-run-id
python3 "$trackwave" record --plan task-plan.json --revision 2 --event-id parser-return-1 --item parser --action return --evidence artifacts/parser.patch
# Host inspects the result and checks the full contract.
python3 "$trackwave" record --plan task-plan.json --revision 3 --event-id parser-accept-1 --item parser --action accept --evidence artifacts/parser-validation.json
```

`reserve` admits only ready items and enforces `max_parallel` over reserved/running entries and `max_attempts` per item. The selected model is requested/configured metadata, not provider attestation. For host execution, use an identifiable current task/turn reference as the run ID; do not pretend a child was launched. `bind` requires the actual run ID. `return` requires an artifact/evidence reference. `accept` requires host validation evidence and an item in returned state. References can be paths, URLs, or task/turn IDs; existence and validity are the host's responsibility.

```bash
python3 "$trackwave" record --plan task-plan.json --revision 4 --event-id parser-fail-1 --item parser --action fail --note "Describe the observed failure and run resolution" --run-resolved
```

`fail` applies to reserved/running/returned items, requires a note and explicit confirmation that the prior run is resolved, and retains the failed attempt. Do not use it on accepted work or call it merely because a watcher timed out. A failed item becomes ready for another reservation only if dependencies, wave, and remaining attempts allow it.

Ready is a dependency/scheduling candidate, not proof that the route exists, writes are non-overlapping, or runtime actions are authorized. The host checks these before reservation and watches the deadline; the helper does not enforce model permissions, read/write sets, wall time, or token budgets. Returned items await validation and no longer occupy a worker slot, but do not unblock dependents.

## Resume and revise

After a restart, run `status` and resolve known run IDs before retrying. An orphaned reservation is ambiguous until dispatch records have been checked. If a process dies while holding `<plan>.lock`, inspect the lock's PID/host and the writer's actual state before removing that exact stale lock; there is no automatic stale-lock deletion. Never delete the plan to clear a lock.

The v1 helper intentionally keeps the spec and accepted history immutable. If acceptance criteria, source, or dependencies change, preserve the original state and explicitly create a successor spec with `predecessor` set to the old plan's path and revision. Record why it changed in the new goal/source context. Do not reset limits to evade an exhausted envelope. Carry previously accepted work only after rechecking its evidence against the changed source and recording that check through the same lifecycle; use a host verification run reference. Resolve old active runs first. No raw state patching or implicit invalidation is supported.

## Import an existing plan

A raw v1 spec can be initialized. An existing v1 state file must be resumed, not passed to `init`. For Markdown, JSON from another planner, or a Colony TrackWave export, read it as input and derive a v1 spec while preserving source plan/wave/item IDs in titles or source references. Keep its acceptance criteria and unfinished dependencies. Set `predecessor` to the source reference. Explain any derived implementation mapping; do not invent absent mappings.

Imported completion/approval fields are reported historical context until verified for the current work. A local plan does not advance the remote original or inherit its authority. An external plan export is optional input; no passport, daemon, credentials, remote CLI, or Colony policy is required to use this helper.
