#!/usr/bin/env python3
"""Repository-map stale detector.

Manifest format:
{
  "entries": [
    {"source": "src/order.py", "wiki": "assets/project-wiki/modules/order.md", "sha256": "..."}
  ]
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.gates import evidence_for_path, file_sha256, finalize_result, print_result
from runtime.status import worst_status


def check_manifest(args: argparse.Namespace) -> dict:
    manifest = Path(args.manifest)
    checks = []
    evidence = [evidence_for_path(manifest)]

    if not manifest.exists():
        checks.append({
            "name": "wiki_manifest_exists",
            "status": "WARN",
            "message": "manifest is missing; create .harness/wiki-manifest.json to enable stale detection",
        })
        return finalize_result(
            gate="check-knowledge-stale",
            target=manifest,
            status="WARN",
            checks=checks,
            evidence=evidence,
            output=args.output,
        )

    data = json.loads(manifest.read_text(encoding="utf-8"))
    entries = data.get("entries", [])
    if not entries:
        checks.append({
            "name": "wiki_manifest_entries",
            "status": "WARN",
            "message": "manifest has no tracked source/wiki entries",
        })

    for entry in entries:
        source = ROOT / entry["source"]
        wiki = ROOT / entry["wiki"]
        evidence.append(evidence_for_path(source))
        evidence.append(evidence_for_path(wiki))
        if not source.exists():
            checks.append({"name": entry["source"], "status": "FAIL", "message": "source file missing"})
            continue
        if not wiki.exists():
            checks.append({"name": entry["wiki"], "status": "FAIL", "message": "wiki file missing"})
            continue
        actual = file_sha256(source)
        expected = entry.get("sha256")
        status = "PASS" if expected == actual else ("FAIL" if args.fail_on_stale else "WARN")
        checks.append({
            "name": entry["source"],
            "status": status,
            "message": "wiki is fresh" if status == "PASS" else "source hash changed; refresh wiki",
        })

    return finalize_result(
        gate="check-knowledge-stale",
        target=manifest,
        status=worst_status([check["status"] for check in checks]),
        checks=checks,
        evidence=evidence,
        output=args.output,
        metadata={"entries": len(entries)},
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check project-wiki freshness")
    parser.add_argument("manifest", nargs="?", default=".harness/wiki-manifest.json")
    parser.add_argument("--fail-on-stale", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check_manifest(args)
    print_result(result, args.json)
    return int(result["exit_code"])


if __name__ == "__main__":
    sys.exit(main())
