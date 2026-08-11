# Decomposition and outputs

Use this reference only after a strategy has passed `COMMIT`.

## Decomposition hierarchy

Use as many levels as add clarity:

```text
Goal
  Strategy
    Strategic outcome
      Initiative
        Deliverable
          Work package
            Task
              Action
```

Preserve parent-to-child `decomposes_to` edges. Remove orphan work that cannot be traced to a selected strategy and goal.

## Strategic outcomes

Describe observable intermediate states, not activities. A good outcome states what will be different and how it can be recognized.

## Initiatives and deliverables

Use initiatives to group coordinated change. Use deliverables for concrete outputs that enable an outcome. If actor behavior mediates success, connect deliverables through an Impact Map rather than assuming output automatically causes outcome.

## Executable tasks

Each final task should normally identify:

- owner or assignable role;
- concrete action;
- expected output;
- definition of done;
- dependencies;
- required resources;
- effort or size when useful;
- trigger/start condition;
- success indicator when useful.

“Improve positioning” is not executable. “Interview five target customers with the approved guide and summarize recurring buying objections” is executable.

Use a transition-tree sequence when operational changes have strict causal ordering. Otherwise avoid ceremony.

## Brief projection

Use [assets/brief-template.md](../assets/brief-template.md) to show only the current strategic model:

- goal and phase;
- current reality and constraints;
- active causal model and candidates/decision;
- evidence confidence;
- critical unknowns;
- next gate.

Keep it concise enough to orient a new agent. The graph remains authoritative.

## Plan projection

Create `plan.md` only after `COMMIT`, using [assets/plan-template.md](../assets/plan-template.md). Generate each section from current graph nodes and edges. Include rejected strategies only when the rejection informs execution or replanning.

The plan must include:

- operational objective;
- relevant current reality;
- hard constraints and important preferences;
- selected strategy and material rejections;
- concise rationale;
- evidence and confidence;
- strategic outcomes;
- sequenced roadmap and milestones;
- deliverables and executable work;
- metrics and means of verification;
- remaining risks and unknowns;
- replanning triggers;
- first review point.

State that it is the best currently supported model, not a guarantee.

## Experiment plan

When `VALIDATE` is blocked, the appropriate output is often an experiment plan rather than a full implementation plan. Include claim, method, owner, thresholds, bound, evidence capture, and decision branches. Keep the phase `VALIDATE`.

## Consistency check

Before declaring `READY`:

1. Verify the plan reflects the current graph revision.
2. Verify the selected strategy has an explicit decision.
3. Verify no open critical unknown blocks decomposition.
4. Verify every task has strategic traceability.
5. Verify owners, dependencies, and definitions of done are usable.
6. Verify metrics observe outcomes, not only activity.
7. Verify replanning triggers connect to assumptions or evidence.
