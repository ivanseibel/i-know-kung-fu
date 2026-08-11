#!/usr/bin/env python3
"""Validate a goal-to-action Strategic Graph using only Python's standard library."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


PHASES = (
    "FRAME",
    "BACKCAST",
    "DIAGNOSE",
    "DIVERGE",
    "EVALUATE",
    "VALIDATE",
    "COMMIT",
    "DECOMPOSE",
    "READY",
)
NODE_TYPES = {
    "goal",
    "success_condition",
    "fact",
    "resource",
    "hard_constraint",
    "preference",
    "unknown",
    "assumption",
    "evidence",
    "necessary_condition",
    "gap",
    "obstacle",
    "intermediate_objective",
    "mechanism",
    "strategy",
    "experiment",
    "decision",
    "strategic_outcome",
    "initiative",
    "deliverable",
    "work_package",
    "task",
    "action",
    "result",
}
EDGE_TYPES = {
    "requires",
    "supports",
    "expected_to_cause",
    "blocked_by",
    "resolves",
    "assumes",
    "evidenced_by",
    "tests",
    "violates",
    "conflicts_with",
    "depends_on",
    "decomposes_to",
    "selected_by",
}
CONFIDENCE = {"low", "medium", "high", "unknown"}
UNKNOWN_CLASSES = {"researchable", "user-decision-required", "testable", "deferred"}
MATERIALITY = {"critical", "material", "minor"}
RESOLVED_UNKNOWN_STATUSES = {"supported", "validated", "accepted_risk", "completed", "rejected"}


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        graph = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"file not found: {path}"], warnings
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read valid JSON from {path}: {exc}"], warnings

    if not isinstance(graph, dict):
        return ["graph root must be a JSON object"], warnings

    if graph.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    session = graph.get("session")
    if not isinstance(session, dict):
        errors.append("session must be an object")
        session = {}
    for field in ("id", "title", "phase", "status", "created_at", "updated_at"):
        if not isinstance(session.get(field), str):
            errors.append(f"session.{field} must be a string")
    if session.get("phase") not in PHASES:
        errors.append(f"session.phase must be one of: {', '.join(PHASES)}")
    revision = session.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        errors.append("session.revision must be a positive integer")
    for field in ("pending_prompt_id", "last_processed_operator_event_id"):
        value = session.get(field)
        if value is not None and not is_nonempty_string(value):
            errors.append(f"session.{field} must be null or a non-empty string")

    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list):
        errors.append("nodes must be an array")
        nodes = []
    if not isinstance(edges, list):
        errors.append("edges must be an array")
        edges = []

    nodes_by_id: dict[str, dict[str, Any]] = {}
    for index, node in enumerate(nodes):
        label = f"nodes[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{label} must be an object")
            continue
        node_id = node.get("id")
        if not is_nonempty_string(node_id):
            errors.append(f"{label}.id must be a non-empty string")
        elif node_id in nodes_by_id:
            errors.append(f"duplicate node id: {node_id}")
        else:
            nodes_by_id[node_id] = node
        if node.get("type") not in NODE_TYPES:
            errors.append(f"{label}.type is not supported: {node.get('type')!r}")
        if not is_nonempty_string(node.get("statement")):
            errors.append(f"{label}.statement must be a non-empty string")
        if not is_nonempty_string(node.get("status")):
            errors.append(f"{label}.status must be a non-empty string")
        if not is_nonempty_string(node.get("provenance")):
            errors.append(f"{label}.provenance must be a non-empty string")
        if node.get("confidence") not in CONFIDENCE:
            errors.append(f"{label}.confidence must be low, medium, high, or unknown")
        if not isinstance(node.get("evidence_refs"), list):
            errors.append(f"{label}.evidence_refs must be an array")
        attrs = node.get("attributes")
        if not isinstance(attrs, dict):
            errors.append(f"{label}.attributes must be an object")
            attrs = {}
        if node.get("type") == "unknown":
            if attrs.get("classification") not in UNKNOWN_CLASSES:
                errors.append(f"{label} unknown requires a valid attributes.classification")
            if attrs.get("materiality") not in MATERIALITY:
                errors.append(f"{label} unknown requires a valid attributes.materiality")
        if node.get("type") == "experiment":
            for field in ("success_threshold", "failure_threshold"):
                if not is_nonempty_string(attrs.get(field)):
                    errors.append(f"{label} experiment requires attributes.{field}")

    edge_ids: set[str] = set()
    incoming_decomposition: dict[str, list[str]] = defaultdict(list)
    strategy_decisions: dict[str, list[str]] = defaultdict(list)
    selected_strategy_ids: set[str] = {
        node_id
        for node_id, node in nodes_by_id.items()
        if node.get("type") == "strategy" and node.get("status") == "selected"
    }
    goal_ids = {node_id for node_id, node in nodes_by_id.items() if node.get("type") == "goal"}

    for index, edge in enumerate(edges):
        label = f"edges[{index}]"
        if not isinstance(edge, dict):
            errors.append(f"{label} must be an object")
            continue
        edge_id = edge.get("id")
        if not is_nonempty_string(edge_id):
            errors.append(f"{label}.id must be a non-empty string")
        elif edge_id in edge_ids:
            errors.append(f"duplicate edge id: {edge_id}")
        else:
            edge_ids.add(edge_id)
        if edge.get("type") not in EDGE_TYPES:
            errors.append(f"{label}.type is not supported: {edge.get('type')!r}")
        source = edge.get("from")
        target = edge.get("to")
        if source not in nodes_by_id:
            errors.append(f"{label}.from references missing node: {source!r}")
        if target not in nodes_by_id:
            errors.append(f"{label}.to references missing node: {target!r}")
        if not is_nonempty_string(edge.get("status")):
            errors.append(f"{label}.status must be a non-empty string")
        if edge.get("confidence") not in CONFIDENCE:
            errors.append(f"{label}.confidence must be low, medium, high, or unknown")
        if not isinstance(edge.get("evidence_refs"), list):
            errors.append(f"{label}.evidence_refs must be an array")
        if not isinstance(edge.get("attributes"), dict):
            errors.append(f"{label}.attributes must be an object")
        if edge.get("type") == "decomposes_to" and source in nodes_by_id and target in nodes_by_id:
            incoming_decomposition[target].append(source)
        if (
            edge.get("type") == "selected_by"
            and source in selected_strategy_ids
            and nodes_by_id.get(target, {}).get("type") == "decision"
        ):
            strategy_decisions[source].append(target)
        if (
            edge.get("type") == "violates"
            and source in selected_strategy_ids
            and nodes_by_id.get(target, {}).get("type") == "hard_constraint"
        ):
            errors.append(f"selected strategy {source} violates hard constraint {target}")

    phase = session.get("phase")
    if phase in {"COMMIT", "DECOMPOSE", "READY"}:
        for node_id, node in nodes_by_id.items():
            attrs = node.get("attributes", {})
            if (
                node.get("type") == "unknown"
                and attrs.get("materiality") == "critical"
                and node.get("status") not in RESOLVED_UNKNOWN_STATUSES
            ):
                errors.append(f"open critical unknown {node_id} blocks phase {phase}")

    if phase in {"DECOMPOSE", "READY"} and not selected_strategy_ids:
        errors.append(f"phase {phase} requires at least one selected strategy")
    if phase in {"DECOMPOSE", "READY"}:
        for strategy_id in selected_strategy_ids:
            if not strategy_decisions.get(strategy_id):
                errors.append(f"selected strategy {strategy_id} requires a selected_by decision before {phase}")

    def has_decomposition_ancestor(start: str, targets: set[str]) -> bool:
        queue = deque([start])
        seen = {start}
        while queue:
            current = queue.popleft()
            for parent in incoming_decomposition.get(current, []):
                if parent in targets:
                    return True
                if parent not in seen:
                    seen.add(parent)
                    queue.append(parent)
        return False

    if selected_strategy_ids and goal_ids:
        for strategy_id in selected_strategy_ids:
            if not has_decomposition_ancestor(strategy_id, goal_ids):
                warnings.append(f"selected strategy {strategy_id} has no decomposes_to path from a goal")

    for node_id, node in nodes_by_id.items():
        if node.get("type") in {"task", "action"}:
            if not selected_strategy_ids:
                errors.append(f"{node.get('type')} {node_id} exists without a selected strategy")
            elif not has_decomposition_ancestor(node_id, selected_strategy_ids):
                errors.append(f"{node.get('type')} {node_id} is not traceable to a selected strategy")
            if goal_ids and not has_decomposition_ancestor(node_id, goal_ids):
                errors.append(f"{node.get('type')} {node_id} is not traceable to a goal")

    if nodes and not goal_ids:
        warnings.append("graph has nodes but no goal node")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path, help="path to graph.json")
    args = parser.parse_args()

    errors, warnings = validate(args.graph)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"INVALID: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"VALID: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
