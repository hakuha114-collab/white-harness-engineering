"""Machine-readable policy helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .io import load_json_yaml


def load_policies(path: str | Path = "rules/policies.yaml") -> dict[str, Any]:
    return load_json_yaml(path)


def side_effect_requires_approval(effect: str, policies: dict[str, Any]) -> bool:
    policy = policies.get("side_effect_policy", {})
    rule = policy.get(str(effect), {})
    return bool(rule.get("human_approval_required", False))


def blocked_without_approval(
    side_effects: list[str],
    approvals: list[dict[str, Any]],
    policies: dict[str, Any],
) -> list[str]:
    approved = {item.get("effect") for item in approvals if item.get("status") == "APPROVED"}
    blocked: list[str] = []
    for effect in side_effects:
        if side_effect_requires_approval(effect, policies) and effect not in approved:
            blocked.append(effect)
    return blocked
