"""TaskState schema helpers and feature-level memory layout."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .io import utc_now, write_json
from .trace import append_event


SCHEMA_VERSION = "2.0.0"
DEFAULT_BUDGET = {
    "max_tokens": 150000,
    "max_tool_calls": 100,
    "max_rollbacks": 3,
    "max_wall_minutes": 240,
}
REQUIRED_FIELDS = [
    "schema_version",
    "task_id",
    "goal",
    "workflow_id",
    "current_node",
    "status",
    "artifacts",
    "evidence",
    "subtasks",
    "rollback_count",
    "human_approvals",
    "budget",
    "audit",
]


def new_task_state(
    task_id: str,
    goal: str,
    workflow_id: str,
    *,
    risk_level: str = "normal",
    budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    now = utc_now()
    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": task_id,
        "goal": goal,
        "workflow_id": workflow_id,
        "current_node": "start",
        "status": "READY",
        "risk_level": risk_level,
        "artifacts": {},
        "evidence": {},
        "subtasks": [],
        "rollback_count": 0,
        "human_approvals": [],
        "budget": {**DEFAULT_BUDGET, **(budget or {})},
        "audit": {
            "created_at": now,
            "updated_at": now,
            "trace": "timeline.ndjson",
            "checkpoint_dir": "checkpoints",
        },
    }


def feature_dir(root: str | Path, task_id: str) -> Path:
    return Path(root) / "features" / task_id


def validate_task_state(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if field not in state:
            errors.append(f"missing required field: {field}")
    if state.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    if not isinstance(state.get("evidence", {}), dict):
        errors.append("evidence must be an object keyed by gate id")
    if not isinstance(state.get("subtasks", []), list):
        errors.append("subtasks must be a list")
    if not isinstance(state.get("budget", {}), dict):
        errors.append("budget must be an object")
    return errors


def save_state(path: str | Path, state: dict[str, Any]) -> None:
    state.setdefault("audit", {})["updated_at"] = utc_now()
    write_json(path, state)


def load_state(path: str | Path) -> dict[str, Any]:
    import json

    return json.loads(Path(path).read_text(encoding="utf-8"))


def checkpoint(state_path: str | Path, *, name: str | None = None) -> Path:
    source = Path(state_path)
    state = load_state(source)
    checkpoint_name = name or utc_now().replace(":", "").replace("-", "")
    target = source.parent / "checkpoints" / f"{checkpoint_name}.state.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    append_event(
        source.parent / "timeline.ndjson",
        {"type": "checkpoint", "state": str(source), "checkpoint": str(target), "task_id": state["task_id"]},
    )
    return target


def ensure_feature_memory(
    task_id: str,
    goal: str,
    workflow_id: str,
    *,
    root: str | Path = ".harness",
    risk_level: str = "normal",
) -> Path:
    base = feature_dir(root, task_id)
    base.mkdir(parents=True, exist_ok=True)
    for child in ["evidence", "reports", "checkpoints"]:
        (base / child).mkdir(exist_ok=True)

    tech_spec = base / "TECH_SPEC.md"
    if not tech_spec.exists():
        tech_spec.write_text(
            f"# {task_id} TECH_SPEC\n\n"
            f"## Goal\n\n{goal}\n\n"
            "## Acceptance Criteria\n\n- [ ] Replace with measurable acceptance criteria.\n\n"
            "## Architecture Notes\n\n- Capture affected modules and constraints.\n\n"
            "## Handover Notes\n\n- Keep this file sufficient for a clean-context agent to continue.\n",
            encoding="utf-8",
        )

    subtasks = base / "subtasks.json"
    if not subtasks.exists():
        write_json(subtasks, [])

    state_path = base / "state.json"
    if not state_path.exists():
        save_state(state_path, new_task_state(task_id, goal, workflow_id, risk_level=risk_level))

    timeline = base / "timeline.ndjson"
    if not timeline.exists():
        append_event(timeline, {"type": "task_created", "task_id": task_id, "workflow_id": workflow_id})
    return base
