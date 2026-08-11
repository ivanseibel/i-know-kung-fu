#!/usr/bin/env python3
"""Behavior checks for the bundled Strategic Graph validator."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from validate_graph import validate  # noqa: E402


def node(node_id: str, node_type: str, status: str = "candidate", **attributes: str) -> dict:
    return {
        "id": node_id,
        "type": node_type,
        "statement": f"Statement for {node_id}",
        "status": status,
        "provenance": "agent-inference",
        "confidence": "medium",
        "evidence_refs": [],
        "attributes": attributes,
    }


def edge(edge_id: str, edge_type: str, source: str, target: str) -> dict:
    return {
        "id": edge_id,
        "type": edge_type,
        "from": source,
        "to": target,
        "statement": f"{source} {edge_type} {target}",
        "status": "active",
        "confidence": "medium",
        "evidence_refs": [],
        "attributes": {},
    }


def graph(phase: str, nodes: list[dict], edges: list[dict]) -> dict:
    return {
        "schema_version": 1,
        "session": {
            "id": "test",
            "title": "Test",
            "phase": phase,
            "status": "active",
            "revision": 1,
            "created_at": "",
            "updated_at": "",
        },
        "nodes": nodes,
        "edges": edges,
    }


class ValidateGraphTests(unittest.TestCase):
    def validate_data(self, data: dict) -> tuple[list[str], list[str]]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "graph.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return validate(path)

    def test_template_is_valid(self) -> None:
        errors, warnings = validate(SKILL_ROOT / "assets" / "graph-template.json")
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_interaction_pointer_must_be_string_or_null(self) -> None:
        data = graph("FRAME", [], [])
        data["session"]["last_processed_operator_event_id"] = 42
        errors, _ = self.validate_data(data)
        self.assertTrue(any("last_processed_operator_event_id" in error for error in errors))

    def test_open_critical_unknown_blocks_commit(self) -> None:
        data = graph(
            "COMMIT",
            [
                node("G1", "goal", "active"),
                node(
                    "U1",
                    "unknown",
                    "open",
                    classification="testable",
                    materiality="critical",
                ),
            ],
            [],
        )
        errors, _ = self.validate_data(data)
        self.assertTrue(any("open critical unknown U1" in error for error in errors))

    def test_selected_strategy_cannot_violate_hard_constraint(self) -> None:
        data = graph(
            "COMMIT",
            [
                node("G1", "goal", "active"),
                node("S1", "strategy", "selected"),
                node("HC1", "hard_constraint", "active"),
            ],
            [edge("E1", "violates", "S1", "HC1")],
        )
        errors, _ = self.validate_data(data)
        self.assertTrue(any("violates hard constraint" in error for error in errors))

    def test_orphan_task_is_rejected(self) -> None:
        data = graph(
            "DECOMPOSE",
            [
                node("G1", "goal", "active"),
                node("S1", "strategy", "selected"),
                node("D1", "decision", "validated"),
                node("T1", "task", "candidate"),
            ],
            [
                edge("E1", "decomposes_to", "G1", "S1"),
                edge("E2", "selected_by", "S1", "D1"),
            ],
        )
        errors, _ = self.validate_data(data)
        self.assertTrue(any("task T1 is not traceable" in error for error in errors))

    def test_traceable_task_is_valid(self) -> None:
        data = graph(
            "DECOMPOSE",
            [
                node("G1", "goal", "active"),
                node("S1", "strategy", "selected"),
                node("D1", "decision", "validated"),
                node("SO1", "strategic_outcome", "active"),
                node("T1", "task", "candidate"),
            ],
            [
                edge("E1", "decomposes_to", "G1", "S1"),
                edge("E2", "selected_by", "S1", "D1"),
                edge("E3", "decomposes_to", "S1", "SO1"),
                edge("E4", "decomposes_to", "SO1", "T1"),
            ],
        )
        errors, warnings = self.validate_data(data)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)


if __name__ == "__main__":
    unittest.main()
