"""Small IO helpers for JSON-compatible YAML runtime files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json_yaml(path: str | Path) -> Any:
    """Load a machine-readable .yaml file that is valid JSON syntax."""

    source = Path(path)
    try:
        return json.loads(source.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{source} must be JSON-compatible YAML. "
            "Use JSON object/array syntax so the runtime has no PyYAML dependency."
        ) from exc


def write_json(path: str | Path, data: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def utc_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
