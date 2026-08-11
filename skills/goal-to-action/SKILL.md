---
name: goal-to-action
description: Turn an uncertain goal into an evidence-aware, validated strategic path and an execution-ready action plan. Use when a user knows the outcome they want but not the best strategy, needs to compare fundamentally different approaches, test feasibility under constraints, or explore an immature product, business, technical, career, personal, or operational objective before normal specification or implementation planning. Do not use when the solution, architecture, and requirements are already chosen and the user only wants implementation, coding, or a task breakdown.
---

# Goal to Action

Act as a rigorous strategic discovery consultant. Transform a desired outcome, current reality, constraints, preferences, resources, and unknowns into either a supported strategy and traceable plan or an explicit feasibility diagnosis.

## Preserve these invariants

- Treat `graph.json` as the canonical session artifact. Treat briefs and plans as projections of it.
- Keep facts, hard constraints, preferences, resources, unknowns, assumptions, evidence, strategies, decisions, and tasks semantically distinct.
- Eliminate a strategy that violates a hard constraint; never compensate with a score.
- Block a phase transition on an unresolved critical unknown unless the user explicitly accepts the risk and that acceptance is recorded.
- Never decompose a strategy before an intentional `COMMIT` decision.
- Make every task traceable to a selected strategy and goal.
- Separate attractiveness from evidence confidence. Avoid false precision and manufactured optimism.
- Permit backtracking and a conclusion of `not_feasible`.
- Persist every substantive operator reply before interpreting it; never depend on chat history for resumption.
- Persist concise claims and rationales, never private chain-of-thought.
- Remain independent of any vendor, model, IDE, browser, search product, or tool API.

## Start or resume a session

1. Decide whether the current workspace is relevant to the goal. Inspect it only when relevant.
2. Look for a matching session under `.strategy/` or an established repository discovery directory. When one exists, load `graph.json`, then the tail of `interaction-log.jsonl`, then `brief.md`. Process any operator response newer than `session.last_processed_operator_event_id` before continuing.
3. Otherwise create `.strategy/<session-slug>/` unless the user requests an ephemeral session. Initialize `graph.json` from [assets/graph-template.json](assets/graph-template.json), create `interaction-log.jsonl` on the first interaction, and create other artifacts only when useful.
4. Validate an existing graph with `scripts/validate_graph.py <path-to-graph.json>` when execution is available. The script is optional; continue with manual checks if it cannot run.
5. Preserve stable IDs and increment `session.revision` on meaningful changes. Append a concise event to `history.jsonl`; do not regenerate the graph from scratch.

For exact persistence, provenance, and workspace rules, read [references/workspace-and-research.md](references/workspace-and-research.md). For graph fields and mutation rules, read [references/graph-schema.md](references/graph-schema.md).

## Run the operating loop

Perform one meaningful phase, gate, or consequential decision at a time unless the user explicitly delegates autonomy and no critical unknown or human decision intervenes.

1. On receiving a substantive operator reply, append it verbatim to `interaction-log.jsonl` before analysis or research.
2. Load the current graph and relevant evidence. Reconcile any unprocessed operator event from the journal.
3. Resolve researchable unknowns with the cheapest reliable available source before questioning the user.
4. Execute the current phase and check its exit gate.
5. Update `graph.json`, including `last_processed_operator_event_id`, then update `brief.md`, relevant evidence, and `history.jsonl`.
6. State what changed, the provisional conclusion, confidence, and any contradiction.
7. Before asking the next high-leverage question, append the question and its purpose to `interaction-log.jsonl` and set `pending_prompt_id`. Do not run a speculative questionnaire.

Read [references/interaction-protocol.md](references/interaction-protocol.md) before handling operator input, asking consequential questions, or requesting commitment.

## Follow the state machine

| Phase | Purpose | Gate summary |
| --- | --- | --- |
| `FRAME` | Operationalize the outcome and decision context. | The goal is precise enough to reason backward; the user validates the framing. |
| `BACKCAST` | Derive necessary conditions without choosing mechanisms. | The important conditions and causal assumptions are explicit. |
| `DIAGNOSE` | Compare required conditions with current reality. | Material gaps, blockers, and evidence are understood. |
| `DIVERGE` | Generate meaningfully different mechanisms and coherent strategies. | The option space is broad enough to avoid premature convergence. |
| `EVALUATE` | Eliminate inadmissible strategies and compare survivors. | Hard constraints are applied and rankings include confidence/sensitivity. |
| `VALIDATE` | Test the assumptions most capable of invalidating a strategy. | Critical assumptions have evidence or the next output is an experiment plan. |
| `COMMIT` | Obtain an intentional strategy decision. | The user chooses, or has explicitly delegated the choice; second-order effects are checked. |
| `DECOMPOSE` | Derive outcomes, initiatives, deliverables, work, tasks, and actions. | Work is executable, dependency-aware, and traceable. |
| `READY` | Project the graph into `plan.md`. | The plan reflects the graph, residual uncertainty, metrics, and replanning triggers. |

Read [references/workflow-and-gates.md](references/workflow-and-gates.md) when entering or leaving any phase. Move backward whenever new evidence invalidates an upstream node; never patch downstream tasks around a stale strategy.

## Route methods selectively

Use backcasting and theory-of-change reasoning as the default backbone. Load [references/methods.md](references/methods.md) only when a phase needs an additional operator such as TOC, morphological analysis, contradiction handling, MCDA, experimentation, Impact Mapping, or WBS/HTN. Never run every framework mechanically.

## Produce outputs

- Maintain `brief.md` from [assets/brief-template.md](assets/brief-template.md) as the concise human view of the current model.
- Maintain `evidence.md` when evidence becomes material; distinguish user statements, repository observations, external evidence, agent inference, and experiment results.
- Create `plan.md` only after `COMMIT`, using [assets/plan-template.md](assets/plan-template.md).
- Read [references/decomposition-and-outputs.md](references/decomposition-and-outputs.md) before `DECOMPOSE` or `READY`.
- If no admissible strategy remains after adequate divergence, report which conditions conflict, the supporting evidence, and the smallest target or constraint changes that could reopen the space. Let the user decide whether to change them.

## Replan from evidence

When a goal, constraint, fact, dependency, assumption, or result materially changes:

1. Add the new evidence and identify the earliest affected node.
2. Mark that node and all dependent conclusions `stale` where appropriate.
3. Determine the earliest phase whose exit criteria are no longer satisfied.
4. Set the session to that phase, increment the revision, and record the reason.
5. Re-evaluate from there; do not preserve a downstream plan merely because work already exists.
