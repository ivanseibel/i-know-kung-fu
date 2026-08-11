# Workspace, persistence, and research

Use this reference when starting/resuming a session, inspecting a repository, or gathering evidence.

## Session location

Keep the skill reusable and project-independent. Store no session state inside the installed skill.

Default to:

```text
.strategy/<session-slug>/
├── graph.json
├── brief.md
├── interaction-log.jsonl # append-only prompts and verbatim operator replies
├── sources/              # create only for material sources needing durable preservation
├── evidence.md       # create when evidence becomes material
├── history.jsonl     # create on the first meaningful mutation/event
└── plan.md           # create only after COMMIT
```

Prefer an established repository location for discovery/design artifacts when it clearly fits. Do not add artifacts to `.gitignore` or commit them unless asked.

Create the interaction log no later than the first substantive exchange. For an explicitly ephemeral session, work conversationally and warn that interruption-safe resumption and cross-agent continuity are not guaranteed.

## Resume before theory

When a session exists:

1. Load `graph.json`.
2. Read the tail of `interaction-log.jsonl`. Compare operator event IDs with `session.last_processed_operator_event_id`.
3. If a newer operator response exists, process the oldest unprocessed response before asking anything new. The journal is the recovery source for an interrupted turn; after processing, the graph is again canonical.
4. If the last event is an unanswered agent prompt, resume from that prompt instead of generating a different question.
5. Check schema version, phase, revision, open critical unknowns, selected decisions, and stale nodes.
6. Load `brief.md` and only the evidence relevant to the current gate.
7. Load method references only if the current phase needs them.
8. Reconcile other discrepancies in favor of the graph unless newer evidence clearly makes the graph stale; then update the graph explicitly.

## Relevant existing repository

Treat code as evidence of current reality, not proof of desired product behavior.

Inspect high-signal context progressively before asking questions the repository can answer:

- README and nearby project documentation;
- architecture docs and ADRs;
- package/dependency manifests;
- relevant source modules and analogous implementations;
- schemas and configuration;
- tests and existing specifications.

Use targeted search and inspection. Do not exhaustively read the repository. Record meaningful observations as facts with file/location provenance. Surface conflicts between repository evidence and user statements instead of silently choosing one.

If the goal is unrelated to the current repository, do not spend context inspecting it.

## Empty or unrelated workspace

Use conversation context, user-provided artifacts, calculations, available research, and experiments. Do not invent repository facts or create a technical framing merely because a workspace exists.

## Evidence provenance

Keep evidence classes explicit:

- `user`: supplied or confirmed by the user;
- `repository`: directly observed in workspace artifacts;
- `external`: supported by current outside sources;
- `calculation`: derived with a reproducible calculation;
- `experiment`: observed from a defined test;
- `agent-inference`: a concise interpretation that still requires support.

For external evidence, record title, publisher/author when relevant, URL or locator, access date, and the claim it supports or challenges. Prefer primary and current sources. Distinguish quotations from paraphrases.

## Research routing

When a material unknown depends on current facts and external capabilities exist, research before asking the user to guess. Describe capabilities semantically rather than requiring a named vendor tool.

If research capability is unavailable or access fails, leave the unknown unresolved with its effect on the gate. Never fill a gap with plausible-sounding claims.

Use the cheapest reliable resolution method. Do not commission expensive research when repository inspection, calculation, or a small test can answer the decision.

## Artifact update discipline

After a meaningful phase or decision:

- mutate the existing graph incrementally;
- update the phase and revision;
- regenerate the brief as a faithful concise view;
- append a high-level history event;
- add evidence without erasing prior contradictory observations;
- update `plan.md` only if `COMMIT` has occurred and the graph changed in a plan-relevant way.

For every substantive operator reply, use a stricter write-ahead order:

1. Append the verbatim reply and attachment locators to `interaction-log.jsonl` before interpreting it.
2. Apply its meaning to the graph and evidence.
3. Set `session.last_processed_operator_event_id` to that response event and clear the answered `pending_prompt_id` in the same graph update.
4. Refresh the brief and append a history event only when the strategic model materially changed.

If interrupted after step 1, resumption detects and processes the pending reply. If interrupted after step 3, the graph pointer prevents duplicate processing. Use safe append and atomic replacement capabilities when the environment provides them.
