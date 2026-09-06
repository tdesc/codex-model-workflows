# Standalone TrackWave adapter

Use the companion `codex-trackwave` skill for local JSON plans. Resolve its installed `SKILL.md` and read its command reference; use its bundled Python helper. No remote planner, project passport, MCP server, Docker service, or Colony policy is required.

## Bind the plan

Read the supplied local state and run `status`. Bind `spec.id`, the current `revision`, `active_wave`, selected item, source reference, acceptance, ownership sets, deadline, and remaining attempts/slots. Completed items keep their accepted artifact and validation references. Resolve reserved/running attempts before scheduling retries.

For a plain goal, a local plan is useful when work spans waves or needs restart recovery. Generate a spec using the companion's example and initialize a new state only when no selected state already exists. Ordinary serial work may stay in the current task.

For a Markdown plan or an export from any other planner, derive a local spec using the companion's import procedure. Preserve source IDs and acceptance criteria, label derived lane mappings, and retain historical completion as reported until rechecked. This does not synchronize or advance the external original. The export is sufficient input; do not require access to its source service.

## Route and run

Choose a dependency-ready item in the active wave. Check source freshness, route support, time remaining, and read/write hazards with other running lanes. Reserve the item before dispatch, recording the selected model. Send the complete worker packet with the plan/wave/item identity and accepted upstream outputs. Record the actual run ID through `bind`, then use the platform's wait/status tools to observe it.

The local lifecycle is:

`pending/failed → reserved → running → returned → accepted`

Reserve consumes an attempt and a worker slot. Returned results release the worker slot but remain unavailable to dependent work until acceptance. Only the host records transitions; workers must not edit plan state. Read the current revision for each update and reuse event IDs for response-loss retries.

At the join, inspect actual artifacts, check the entire contract, and reconcile results under the host's authority. Record the output with `return` and validation evidence with `accept`. The helper derives the next wave from accepted items; no approval token or remote advance command is involved. Continue automatically within the existing authorized goal and envelope; ask only at a real unresolved decision or action boundary.

## Resume and report

Re-read state after interruption. A reservation with no bound run ID may have dispatched before the response was lost; inspect the launch records before retrying. Resolve a run before recording failure, preserve attempt history, and do not exceed the plan's attempt limit by silently creating another plan.

The helper checks dependencies, wave order, attempt counts, concurrency, revisions, and evidence-reference presence. It does not check model permissions, evidence truth, source freshness, ownership conflicts, or wall-clock limits; those remain host responsibilities. If a contract or source change invalidates accepted work, preserve the original and use the companion's explicit successor-plan procedure.

Report `plan/revision | wave/item | actual model/transport/run | returned artifact | validation | integration | residual`. A completed local plan is a record of host acceptance; publication and live behavior require their own observed evidence.
