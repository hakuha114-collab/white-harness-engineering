#!/usr/bin/env python3
"""CLI for White Harness 2.0 runtime operations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from runtime.graph import load_graph, next_targets
from runtime.router import route_task
from runtime.state import checkpoint, ensure_feature_memory, load_state, save_state, validate_task_state
from runtime.trace import replay


def cmd_init(args: argparse.Namespace) -> int:
    base = ensure_feature_memory(
        args.task_id,
        args.goal,
        args.workflow,
        root=args.root,
        risk_level=args.risk_level,
    )
    print(json.dumps({"feature_dir": str(base), "state": str(base / "state.json")}, ensure_ascii=False, indent=2))
    return 0


def cmd_route(args: argparse.Namespace) -> int:
    workflow = route_task({
        "task_type": args.task_type,
        "risk_level": args.risk_level,
        "changed_files": args.changed_files,
        "side_effects": args.side_effect,
    })
    print(json.dumps({"workflow": workflow}, ensure_ascii=False, indent=2))
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    graph = load_graph(args.workflow)
    targets = next_targets(graph, args.node, args.status)
    print(json.dumps({"workflow": args.workflow, "from": args.node, "status": args.status, "next": targets}, indent=2))
    return 0


def cmd_validate_state(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    errors = validate_task_state(state)
    print(json.dumps({"state": args.state, "valid": not errors, "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def cmd_checkpoint(args: argparse.Namespace) -> int:
    target = checkpoint(args.state, name=args.name)
    print(json.dumps({"checkpoint": str(target)}, ensure_ascii=False, indent=2))
    return 0


def cmd_set_node(args: argparse.Namespace) -> int:
    state = load_state(args.state)
    state["current_node"] = args.node
    state["status"] = args.status
    save_state(args.state, state)
    print(json.dumps({"state": args.state, "current_node": args.node, "status": args.status}, indent=2))
    return 0


def cmd_replay(args: argparse.Namespace) -> int:
    print(json.dumps(replay(args.timeline), ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="White Harness 2.0 runtime CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create feature-level task memory")
    init.add_argument("--task-id", required=True)
    init.add_argument("--goal", required=True)
    init.add_argument("--workflow", default="normal")
    init.add_argument("--risk-level", default="normal")
    init.add_argument("--root", default=".harness")
    init.set_defaults(func=cmd_init)

    route = sub.add_parser("route", help="choose trivial/normal/feature/high-risk graph")
    route.add_argument("--task-type", default="normal")
    route.add_argument("--risk-level", default="normal")
    route.add_argument("--changed-files", type=int, default=0)
    route.add_argument("--side-effect", action="append", default=[])
    route.set_defaults(func=cmd_route)

    nxt = sub.add_parser("next", help="show next node(s) for a graph transition")
    nxt.add_argument("--workflow", required=True)
    nxt.add_argument("--node", required=True)
    nxt.add_argument("--status", required=True, choices=["PASS", "WARN", "FAIL", "BLOCK"])
    nxt.set_defaults(func=cmd_next)

    validate = sub.add_parser("validate-state", help="validate a TaskState file")
    validate.add_argument("state")
    validate.set_defaults(func=cmd_validate_state)

    cp = sub.add_parser("checkpoint", help="create a state checkpoint")
    cp.add_argument("state")
    cp.add_argument("--name")
    cp.set_defaults(func=cmd_checkpoint)

    set_node = sub.add_parser("set-node", help="update current node and status")
    set_node.add_argument("state")
    set_node.add_argument("--node", required=True)
    set_node.add_argument("--status", default="RUNNING")
    set_node.set_defaults(func=cmd_set_node)

    replay_cmd = sub.add_parser("replay", help="summarize a timeline.ndjson trace")
    replay_cmd.add_argument("timeline")
    replay_cmd.set_defaults(func=cmd_replay)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
