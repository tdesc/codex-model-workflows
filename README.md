# Codex Model Workflows

Six portable skills for standalone Codex, centered on **GPT-6.2 Sol** (`gpt-6.2-sol`) and an evidence-driven repair loop. Select GPT-6.2 Sol in your client, or start a CLI session with `codex -m gpt-6.2-sol` where supported. The skills guide the selected session. Installing them does not change the model.

| Task | Skill | What to establish |
| --- | --- | --- |
| Ambiguous failure, silent regression, conflicting evidence | `hypothesis-driven-closed-loop` | A probe that distinguishes causes and an observed effect at the ordinary consumer |
| Small fix with a clear cause | `circuit-breaker` | The focused change and its before/after check |
| Expensive run or repeated retry | `wasted-time` | A representative canary and a decision to scale, repair, or stop the attempt |
| Work with real dependencies or a need to resume | `codex-trackwave` | Durable state, accepted evidence, and the next ready item |
| Model choice, delegation, or a supplied execution plan | `sol-luna-spark-router` | A GPT-6.2 Sol-first execution route and verified integration |
| Findings, uncertainty, or an approval decision | `human-friendly-output` | An outcome and evidence a reader can evaluate independently |

Start in the current session. Add a local plan if the work needs durable dependencies or resume. Add workers only when distinct assignments can save time after dispatch and verification costs. The original router skill name remains valid for saved prompts; Luna and Spark are optional routes.

Install this directory as a Codex plugin, or copy the desired folders from `skills/` into your configured Codex skills directory. TrackWave's helper needs Python 3.10+ and uses only the standard library. The bundle needs no MCP server, runtime service, or service credentials. Model availability comes from the active Codex client or dispatch surface. See [Codex model guidance](https://developers.openai.com/codex/models/).

```text
Use $hypothesis-driven-closed-loop to find why the route reaches the queue
but the ordinary consumer still picks the default. Run a discriminating check.

Use $codex-trackwave to plan this work in local waves. Plan only.

Use $sol-luna-spark-router to resume task-plan.json with GPT-6.2 Sol and
verify the next ready item within the existing scope.
```

Replace the bundled plan example's goal, paths, acceptance criteria, source, and authorization with the actual task. The helper records work. Codex executes authorized actions and checks the evidence. The helper never executes plan strings or launches models.

Run the standalone helper tests with:

```bash
python3 -B tests/test_trackwave.py
```

Local plans use revision checks and atomic writes and retain failed and accepted attempts for resume. Evidence references are host-recorded and require inspection. The helper does not enforce filesystem permissions or deadlines, verify evidence, or terminate model calls.
