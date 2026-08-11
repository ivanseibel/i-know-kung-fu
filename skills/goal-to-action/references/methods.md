# Method router

Load only the section needed for the current phase. Methods are reasoning operators, not mandatory artifacts.

## Default backbone: Backcasting and Theory of Change

Use in `BACKCAST` to reason from the desired state to necessary prior conditions. Express only concise causal claims and assumptions in the graph.

## Means-Ends Analysis

Use in `DIAGNOSE` to compare a necessary future condition with current reality. Convert meaningful differences to gaps and then to intermediate objectives.

## Theory of Constraints

- **Prerequisite Tree:** use when obstacles must become intermediate objectives and dependencies.
- **Current Reality Tree:** use when several current problems may share root causes.
- **Evaporating Cloud:** use when a real contradiction or apparently unavoidable trade-off blocks progress.
- **Future Reality Tree:** use before `COMMIT` to inspect negative branches and second-order effects.
- **Transition Tree:** use in `DECOMPOSE` when actions must cause a tightly ordered sequence of state changes.

Do not produce TOC diagrams when ordinary graph relationships are already clear.

## Morphological Analysis

Use in `DIVERGE` when strategies combine several dimensions, such as audience × channel × offer × pricing × delivery. Generate coherent combinations and prune impossible ones; do not rank isolated dimension values as if they were complete strategies.

## TRIZ, Ideal Final Result, and “Can if”

Use in `DIVERGE` when constraints create path dependence or an apparent contradiction. Ask what an ideal result would accomplish without the costly mechanism, then generate ways the goal can be achieved if a blocking condition changes. Never use creativity language to waive a hard constraint.

## Double Diamond

Use as a meta-rule: separate expansion from convergence. Avoid scoring ideas while the option space is still materially narrow.

## Strategy Choice Cascade

Use for genuinely competitive strategy involving where to play, how to win, required capabilities, and management systems. Skip for ordinary personal or implementation-adjacent decisions.

## Impact Mapping

Use when success depends on actors changing behavior:

`WHY (goal) → WHO (actor) → HOW (behavior/impact) → WHAT (deliverable)`

Ensure deliverables remain linked to the actor change they are meant to cause.

## MCDA

Use in `EVALUATE` when several admissible candidates merit explicit comparison.

1. Derive criteria from constraints, preferences, success conditions, and resources.
2. Apply hard constraints before scoring.
3. Use a small ordinal scale and explicit weights only when they clarify judgment.
4. Report evidence confidence separately.
5. Test whether reasonable weight changes reverse the result.

Treat scores as decision support, not objective truth.

## Lean experimentation

Use in `VALIDATE` to convert a high-impact uncertain assumption into a bounded test. Define success and failure thresholds before observing results. Prefer the cheapest test that can change the decision.

## Logical Framework and OGSM

Use selectively to make inputs → activities → outputs → outcomes → goal and associated measures explicit. Do not add framework fields that do not improve traceability or verification.

## WBS and HTN

Use only after `COMMIT`. Decompose deliverables and recursively break work down until tasks are executable, owned or assignable, dependency-aware, and testable by a definition of done.

## Tree-style search

Use internally to branch candidate paths, compare, prune, and backtrack. Persist candidates, evidence, assumptions, decisions, and concise rationales only. Never request or store private chain-of-thought.
