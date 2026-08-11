# Workflow and gates

Use this reference when entering a phase, evaluating its exit gate, or deciding how far to backtrack.

## Global transition rule

Advance only when the exit conditions are supported by the graph. An unresolved critical unknown that affects the gate blocks advancement unless the user explicitly accepts the risk. Record accepted risk as a decision with its scope and rationale.

Do not infer completion from the amount of text produced. A session may move backward.

## FRAME

Purpose: turn an aspiration into a strategic problem.

Capture only what materially shapes the search:

- desired outcome and success conditions;
- target metric, baseline, and time horizon where relevant;
- resources and stakeholders;
- hard constraints and preferences;
- material unknowns.

Clarify ambiguous terms such as “net,” “effective,” “fast,” or “safe.” Do not demand a mechanically SMART goal. Ask for user validation before stabilizing the frame.

Exit when the outcome is precise enough for backcasting and no critical ambiguity blocks it.

## BACKCAST

Purpose: determine what must be true in the desired future.

Recursively ask “What needs to be true for this outcome?” Add necessary conditions and concise causal links. Decompose useful equations, such as revenue = volume × contribution. Keep mechanisms and tasks out of this phase.

Exit when the important necessary conditions and their material causal assumptions are explicit.

## DIAGNOSE

Purpose: compare necessary future conditions with current reality.

For each condition, record what exists, partially exists, or does not exist and the evidence for that conclusion. Convert deficiencies to gaps. Ask why material gaps exist and model obstacles. Convert obstacles into intermediate objectives without mistaking a user constraint for a systemic bottleneck.

Exit when material gaps, obstacles, intermediate objectives, and evidence quality are understood well enough to explore mechanisms.

## DIVERGE

Purpose: produce genuinely different ways to satisfy intermediate objectives.

Generate mechanisms before assembling coherent strategies. Seek differences in causal mechanism, resource use, reversibility, risk, timing, or upside—not superficial variants. Use morphological dimensions when several choices combine into architectures. Use contradiction operators only to expand the feasible search space, never to ignore a hard constraint.

Exit when the option space is broad enough that convergence is not anchored on the first plausible answer and each candidate is coherent enough to evaluate.

## EVALUATE

Purpose: find admissible and attractive strategies.

1. Test every candidate against every relevant hard constraint.
2. Reject each violation unless the user changes the constraint.
3. Compare survivors on criteria derived from the actual decision.
4. Keep attractiveness and evidence confidence separate.
5. Run a lightweight sensitivity check when rankings are close.

If no strategy survives, return to `DIVERGE`, request a consequential target/constraint decision, or diagnose infeasibility.

Exit when admissibility is explicit, comparison is explainable, and unresolved critical unknowns are routed to validation.

## VALIDATE

Purpose: avoid committing to a long plan based on weak assumptions.

Prioritize assumptions by impact × uncertainty × cost of being wrong. Use the cheapest reliable resolution method: existing evidence, repository inspection, calculation, current documentation, external research, interview, prototype, technical spike, or small experiment.

Every experiment must define:

- the claim tested;
- procedure and responsible party;
- success threshold;
- failure threshold;
- time/cost bound;
- graph nodes affected by either result.

Exit when critical assumptions have sufficient evidence for commitment. If not, produce an experiment plan and remain in `VALIDATE`.

## COMMIT

Purpose: turn exploration into an intentional decision.

Present the recommendation, strongest material alternative, trade-offs, evidence confidence, and remaining assumptions. Perform a lightweight future-reality check for negative second-order effects. Do not silently select a consequential path without explicit delegation.

Exit when the decision is recorded, the chosen strategy is marked `selected`, material rejections have reasons, and no unaccepted critical unknown blocks decomposition.

## DECOMPOSE

Purpose: transform the selected strategy into executable work.

Use the hierarchy `goal → strategy → strategic outcome → initiative → deliverable → work package → task → action`, omitting unnecessary levels. Ensure every task has an incoming traceability path to the selected strategy and goal.

Exit when work is specific, owned or assignable, dependency-aware, testable by a definition of done, and free of orphan tasks.

## READY

Purpose: produce `plan.md` as a projection of the graph.

Include objective, current reality, constraints, decision, rationale, evidence/confidence, outcomes, roadmap, deliverables, actions, metrics, remaining risks/unknowns, replanning triggers, and first review point.

Exit when the plan is internally consistent with the current graph revision. Describe it as the best supported model, not a guarantee.

## Backtracking map

- Goal or success definition changes: return to `FRAME`.
- Necessary condition or causal model fails: return to `BACKCAST`.
- Current-state evidence changes materially: return to `DIAGNOSE`.
- Candidate mechanism fails but the structure remains sound: return to `DIVERGE`.
- Preference, constraint, or evaluation evidence changes: return to `EVALUATE`.
- Assumption test fails: normally return to `EVALUATE` or `DIVERGE`; return earlier if the causal model itself fails.
- Selected strategy changes: return to `COMMIT` before decomposition.
