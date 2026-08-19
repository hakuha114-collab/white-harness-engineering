"""Executable graph loading, transition, and checkpoint routing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import load_json_yaml
from .status import normalize_status


def load_graph(workflow_id: str, graph_dir: str | Path = "runtime/graphs") -> dict[str, Any]:
    path = Path(graph_dir) / f"{workflow_id}.yaml"
    graph = load_json_yaml(path)
    if graph.get("id") != workflow_id:
        raise ValueError(f"graph id mismatch: expected {workflow_id}, got {graph.get('id')}")
    return graph


def next_targets(graph: dict[str, Any], node_id: str, status: str) -> list[str]:
    status = normalize_status(status)
    matches = [
        edge for edge in graph.get("edges", [])
        if edge.get("from") == node_id and edge.get("on") in {status, "*"}
    ]
    if not matches:
        return []

    edge = matches[0]
    if "fan_out" in edge:
        return list(edge["fan_out"])
    target = edge.get("to")
    return [target] if target else []


def transition_state(state: dict[str, Any], graph: dict[str, Any], status: str) -> dict[str, Any]:
    current = state.get("current_node", "start")
    targets = next_targets(graph, current, status)
    if normalize_status(status) in {"FAIL", "BLOCK"}:
        state["rollback_count"] = int(state.get("rollback_count", 0)) + 1

    max_rollbacks = int(state.get("budget", {}).get("max_rollbacks", 3))
    if state.get("rollback_count", 0) > max_rollbacks:
        state["status"] = "BLOCKED"
        state["current_node"] = "human_approval"
        return state

    if not targets:
        state["status"] = "DONE" if status == "PASS" else "BLOCKED"
        return state

    state["current_node"] = targets[0] if len(targets) == 1 else "fan_out:" + ",".join(targets)
    state["status"] = "RUNNING"
    return state
