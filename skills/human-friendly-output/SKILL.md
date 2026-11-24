---
name: human-friendly-output
description: Explain engineering outcomes, evidence, uncertainty, and approval decisions so a technically experienced reader can act without access to the agent's execution context.
---

# Human-Friendly Output

Lead with the observable result and why it matters to the user's goal. Name the specific changed behavior or unresolved blocker. Include enough context for the answer to stand on its own.

- **Observed:** name the decisive before/after result, test, source, or receipt. Link an inspectable artifact and make clear whether you ran the check or read a prior result.
- **Inferred:** give the mechanism and the observation that supports it. If mechanisms remain indistinguishable, identify the missing observation.
- **Unknown:** name the product or runtime claim that still lacks evidence, if it affects the decision.

For a hypothesis-driven repair, state the causal verdict separately from the pass/fail status. For delegated work, identify what the host validated when it matters. Distinguish a local patch, passing tests, publication, deployment, and demonstrated behavior. Use exact identifiers only where they help the reader verify the result.

Ask for an approval only when a decision or authority is genuinely missing. State the action, its practical effect, and any meaningful recovery consequence in plain language. Resolve reversible bookkeeping within existing authority. Match the user's language and requested depth. Use a compact table when exact comparisons or multiple verdicts matter.
