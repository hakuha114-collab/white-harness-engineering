from __future__ import annotations

import argparse
import tempfile
import unittest
from pathlib import Path

from runtime.gates import check_spec, finalize_result
from runtime.graph import load_graph, next_targets
from runtime.router import route_task
from runtime.state import ensure_feature_memory, load_state, validate_task_state
from runtime.status import STATUS_EXIT_CODES


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


class RuntimeContractTests(unittest.TestCase):
    def test_exit_code_contract(self) -> None:
        self.assertEqual(STATUS_EXIT_CODES, {"PASS": 0, "FAIL": 1, "WARN": 2, "BLOCK": 3})

    def test_no_evidence_no_pass(self) -> None:
        result = finalize_result(
            gate="example",
            target=Path("missing"),
            status="PASS",
            checks=[],
            evidence=[],
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["exit_code"], 1)

    def test_spec_gate_passes_with_fixture_evidence(self) -> None:
        args = argparse.Namespace(target=str(FIXTURES / "SPEC_PASS.md"), output=None)
        result = check_spec(args)
        self.assertEqual(result["status"], "PASS")
        self.assertTrue(result["evidence"][0]["exists"])

    def test_router_selects_high_risk_for_side_effect(self) -> None:
        workflow = route_task({"task_type": "bug", "risk_level": "normal", "side_effects": ["prod_deploy"]})
        self.assertEqual(workflow, "high-risk")

    def test_feature_graph_fan_out(self) -> None:
        graph = load_graph("feature", ROOT / "runtime" / "graphs")
        self.assertEqual(
            next_targets(graph, "implement", "PASS"),
            ["style_gate", "security_gate", "unit_gate"],
        )

    def test_feature_memory_state_validates(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = ensure_feature_memory("FEAT-1", "demo goal", "feature", root=temp)
            state = load_state(base / "state.json")
            self.assertEqual(validate_task_state(state), [])
            self.assertTrue((base / "TECH_SPEC.md").exists())
            self.assertTrue((base / "subtasks.json").exists())


if __name__ == "__main__":
    unittest.main()
