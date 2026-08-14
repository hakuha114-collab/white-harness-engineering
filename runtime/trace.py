"""Graph trace and replay support."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .io import utc_now


def append_event(timeline_path: str | Path, event: dict[str, Any]) -> None:
    target = Path(timeline_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {"timestamp": utc_now(), **event}
    with target.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def replay(timeline_path: str | Path) -> dict[str, Any]:
    source = Path(timeline_path)
    events: list[dict[str, Any]] = []
    if source.exists():
        with source.open("r", encoding="utf-8") as stream:
            for line in stream:
                line = line.strip()
                if line:
                    events.append(json.loads(line))

    gate_counts: dict[str, int] = {}
    final_status = "UNKNOWN"
    current_node = None
    for event in events:
        if event.get("type") == "gate":
            status = event.get("status", "UNKNOWN")
            gate_counts[status] = gate_counts.get(status, 0) + 1
        if "status" in event:
            final_status = event["status"]
        if "node" in event:
            current_node = event["node"]

    return {
        "timeline": str(source),
        "event_count": len(events),
        "current_node": current_node,
        "final_status": final_status,
        "gate_counts": gate_counts,
        "events": events,
    }
