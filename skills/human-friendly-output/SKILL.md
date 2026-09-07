---
name: human-friendly-output
description: Explain engineering work, agent findings, blockers, and approval requests in language a technically experienced sponsor can evaluate without access to hidden traces, internal receipts, or agent-only context.
---

# Human-friendly output

Write for an experienced engineer who lacks the agent's private execution
context. Preserve technical substance; remove institutional shorthand and
ceremonial detail.

## Make the result independently understandable

Lead with the observable outcome and its product consequence. Then explain:

- what changed or was learned;
- why it matters to the user's goal;
- what evidence supports it;
- what remains uncertain or unfinished;
- the next action, including any decision genuinely owned by the user.

Do not require the reader to reconstruct meaning from hashes, receipt names,
agent roles, internal phase labels, or earlier commentary. Translate each
necessary internal term on first use. Keep identifiers as supporting evidence,
not as the explanation itself.

When a conclusion depends on information unavailable to the user, expose the
useful part of that information. Distinguish clearly between:

- **observed:** seen in source, diff, test output, runtime state, or an external
  system;
- **inferred:** the best explanation connecting those observations;
- **unknown:** not established by available evidence.

Link the relevant artifact, PR, file, or check when the user can inspect it.
If they cannot inspect it, summarize the decisive evidence and its provenance
instead of citing an opaque reference.

## Approval requests

Before asking for approval, state in plain language:

1. the exact action that would be taken;
2. why it is needed now;
3. what user data, code, runtime, or history it can affect;
4. the realistic downside and recovery path;
5. the recommended answer.

Do not outsource agent-internal bookkeeping to the sponsor. Resolve a stale
receipt, naming mismatch, or reversible local bookkeeping issue autonomously
when existing authority permits it. Ask only when the user's choice changes
the product outcome, risk, scope, external state, or authorization boundary.

For a low-risk request, one sentence can be enough. For example: “Git still
remembers the branch state from before the rebase. I recommend updating that
local marker to the current clean commit; this changes no code or Git history
and can be undone by restoring the previous marker. May I proceed?”

## Calibration

Assume technical literacy, not familiarity with this particular agent system.
Use precise engineering language and concrete numbers where they help. Avoid
both oversimplification and protocol dumps. Separate a code fix, a passing
test, a deployed runtime change, and demonstrated product improvement; never
present one as proof of another.

Match the user's language and requested depth. Keep the main answer compact;
offer deeper evidence only when it changes a decision or the user asks for it.
