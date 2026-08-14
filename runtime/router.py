"""Dynamic workflow router."""

from __future__ import annotations

from typing import Any


HIGH_RISK_EFFECTS = {"prod_deploy", "db_migration", "secret_rotation", "delete_resource"}


def route_task(task: dict[str, Any]) -> str:
    risk = str(task.get("risk_level", "normal")).lower()
    task_type = str(task.get("task_type", "normal")).lower()
    side_effects = {str(item).lower() for item in task.get("side_effects", [])}
    changed_files = int(task.get("changed_files", 0) or 0)

    if risk in {"high", "critical", "l0", "l1"} or side_effects & HIGH_RISK_EFFECTS:
        return "high-risk"
    if task_type in {"feature", "new_feature", "migration"} or changed_files >= 6:
        return "feature"
    if task_type in {"docs", "typo", "config"} and risk in {"low", "trivial"} and changed_files <= 2:
        return "trivial"
    return "normal"
