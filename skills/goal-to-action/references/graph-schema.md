# Strategic Graph schema

Use this reference when creating, mutating, validating, or resuming `graph.json`.

## Root object

```json
{
  "schema_version": 1,
  "session": {},
  "nodes": [],
  "edges": []
}
```

`session` contains:

- `id`: stable session slug or identifier.
- `title`: concise human title.
- `phase`: `FRAME`, `BACKCAST`, `DIAGNOSE`, `DIVERGE`, `EVALUATE`, `VALIDATE`, `COMMIT`, `DECOMPOSE`, or `READY`.
- `status`: normally `active`, `paused`, `ready`, `not_feasible`, or `closed`.
- `revision`: positive integer incremented on meaningful graph changes.
- `created_at`, `updated_at`: ISO 8601 timestamps when available.

## Nodes

Every node contains:

```json
{
  "id": "NC1",
  "type": "necessary_condition",
  "statement": "A repeatable customer acquisition mechanism exists",
  "status": "candidate",
  "provenance": "agent-inference",
  "confidence": "medium",
  "evidence_refs": [],
  "attributes": {}
}
```

Use only needed types:

`goal`, `success_condition`, `fact`, `resource`, `hard_constraint`, `preference`, `unknown`, `assumption`, `evidence`, `necessary_condition`, `gap`, `obstacle`, `intermediate_objective`, `mechanism`, `strategy`, `experiment`, `decision`, `strategic_outcome`, `initiative`, `deliverable`, `work_package`, `task`, `action`, `result`.

Recommended status vocabulary:

`candidate`, `open`, `active`, `supported`, `validated`, `selected`, `rejected`, `blocked`, `accepted_risk`, `stale`, `completed`.

Use provenance values that reveal source class, for example `user`, `repository`, `external`, `agent-inference`, `calculation`, or `experiment`. Add a locator or citation in `attributes.source` when available.

Use confidence `low`, `medium`, `high`, or `unknown`. Confidence is evidence strength, not attractiveness.

### Required attributes by semantic type

- `unknown`: `classification` = `researchable`, `user-decision-required`, `testable`, or `deferred`; `materiality` = `critical`, `material`, or `minor`; optionally `blocks_phase`.
- `hard_constraint`: define an explicit `predicate` or a concise pass/fail interpretation when useful.
- `strategy`: record rejection reason in `attributes.rejection_reason` when material.
- `experiment`: record `success_threshold`, `failure_threshold`, and affected node IDs.
- `decision`: record `decided_by`, `decided_at`, and concise `rationale` when available.
- `task`: record `owner`, `expected_output`, `definition_of_done`, dependencies, resources, effort/size, trigger, and success indicator when useful.

## Edges

Every edge contains:

```json
{
  "id": "E1",
  "type": "requires",
  "from": "G1",
  "to": "NC1",
  "statement": "The goal requires this condition",
  "status": "active",
  "confidence": "medium",
  "evidence_refs": [],
  "attributes": {}
}
```

Use these semantics consistently:

- `requires`: source cannot hold unless target holds.
- `supports`: source increases support for target.
- `expected_to_cause`: source is expected to produce or contribute to target.
- `blocked_by`: source is obstructed by target.
- `resolves`: source addresses target.
- `assumes`: source depends on target being true.
- `evidenced_by`: source claim is supported or challenged by target evidence.
- `tests`: source experiment evaluates target assumption or claim.
- `violates`: source strategy violates target hard constraint.
- `conflicts_with`: source and target cannot both hold as modeled.
- `depends_on`: source cannot proceed before target.
- `decomposes_to`: source is the strategic or work parent of target.
- `selected_by`: source strategy was selected by target decision.

Keep edge direction literal according to these definitions. Use a concise edge statement where the relationship is not self-explanatory.

## Stable IDs

Use short prefixes, such as `G`, `SC`, `F`, `R`, `HC`, `P`, `U`, `A`, `EV`, `NC`, `GAP`, `O`, `IO`, `M`, `S`, `EX`, `D`, `SO`, `I`, `DEL`, `WP`, `T`, `AC`, and `RES`. Never recycle an ID after deletion; prefer status changes over deletion when history matters.

## Traceability

Represent decomposition from parent to child with `decomposes_to`. Every `task` and `action` must be reachable backward through incoming decomposition or causal edges to a `strategy` with status `selected` and then to a `goal`.

Link assumptions to the strategies or causal edges that rely on them. This enables forward traversal from a failed assumption to all dependent work.

## Replanning mutation

On invalidating evidence:

1. Add an evidence or result node; do not overwrite the previous evidence trail.
2. Update confidence/status on the directly affected claim.
3. Traverse dependent `assumes`, `requires`, `expected_to_cause`, `depends_on`, and `decomposes_to` relationships.
4. Mark conclusions and work `stale` when they no longer have adequate support.
5. Change the session phase to the earliest invalidated gate.
6. Increment revision and append a history event.

## History events

Write one JSON object per line to `history.jsonl`:

```json
{"at":"2026-01-01T12:00:00Z","revision":2,"event":"phase_changed","from":"FRAME","to":"BACKCAST","reason":"User validated the operational goal","node_refs":["G1","D1"]}
```

Record high-level changes, phase transitions, consequential decisions, accepted risks, invalidating evidence, and feasibility conclusions—not every wording edit.
