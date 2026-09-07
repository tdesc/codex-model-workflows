# Codex Model Workflows

Four portable skills for standalone Codex:

- `codex-trackwave` creates and resumes local wave plans, checks dependencies, and records attempts and acceptance evidence.
- `sol-luna-spark-router` assigns ready work to suitable available models and validates the combined result.
- `wasted-time` bounds expensive work with a stop contract, a canary, and an explicit scale/repair/stop decision.
- `human-friendly-output` turns agent findings into concise, independently understandable engineering reports.

The bundle needs Codex and Python 3.10+ (standard library only). It contains no MCP server, network client, or service credentials. Model access comes from the user's existing Codex setup. The planner records work; Codex launches and supervises it through available tools.

Install this directory as a Codex plugin, or copy the desired folders under `skills/` into your configured Codex skills directory. The skills in this repository are standalone and require only Codex; they do not depend on a server or external service credentials.

Example requests:

```text
Use $codex-trackwave to plan this change in local waves. Plan only.

Use $sol-luna-spark-router to execute task-plan.json within this task's limits.

Resume task-plan.json, inspect unresolved runs, and continue ready work.
```

The bundled example spec illustrates the format. Replace its goal, paths, acceptance criteria, source, and authorization with the actual task before initializing it. The helper never executes strings found in a plan.

Run the standalone helper tests with:

```bash
python3 -B tests/test_trackwave.py
```

Plans are ordinary local JSON files with revision checks and atomic writes. They retain failed and accepted attempts for resume. Evidence references are host-recorded and require inspection; the helper does not prove correctness, enforce path permissions or deadlines, or terminate model calls.
