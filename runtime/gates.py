"""Evidence-based gate engine.

Contract:
    PASS  -> exit 0
    FAIL  -> exit 1
    WARN  -> exit 2
    BLOCK -> exit 3

Principle:
    No Evidence, No Pass.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from .io import utc_now, write_json
from .status import STATUS_EXIT_CODES, normalize_status, worst_status

TEXT_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".cs", ".rb", ".php",
    ".sh", ".ps1", ".json", ".yaml", ".yml", ".toml", ".md",
}
CODE_MARKERS = ("TO" + "DO", "FIX" + "ME", "HA" + "CK")
CODE_STYLE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".cs", ".rb", ".php",
    ".sh", ".ps1",
}
EXCLUDED_DIRS = {".git", ".harness", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evidence_for_path(path: Path, *, kind: str = "file") -> dict[str, Any]:
    entry: dict[str, Any] = {"path": str(path), "kind": kind, "exists": path.exists()}
    if path.is_file():
        entry["sha256"] = file_sha256(path)
        entry["bytes"] = path.stat().st_size
    return entry


def iter_files(root: Path, extensions: set[str] = TEXT_EXTENSIONS) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix.lower() in extensions else []

    files: list[Path] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = [item for item in dirs if item not in EXCLUDED_DIRS]
        for name in names:
            path = Path(current) / name
            if path.suffix.lower() in extensions:
                files.append(path)
    return sorted(files)


def has_evidence(evidence: list[dict[str, Any]]) -> bool:
    return any(item.get("exists") for item in evidence)


def finalize_result(
    *,
    gate: str,
    target: Path,
    status: str,
    checks: list[dict[str, Any]],
    evidence: list[dict[str, Any]],
    output: Path | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    status = normalize_status(status)
    if status == "PASS" and not has_evidence(evidence):
        status = "FAIL"
        checks.append({
            "name": "evidence_required",
            "status": "FAIL",
            "message": "No Evidence, No Pass: gate cannot pass without durable evidence.",
        })

    result = {
        "schema_version": "2.0.0",
        "gate": gate,
        "target": str(target),
        "status": status,
        "exit_code": STATUS_EXIT_CODES[status],
        "timestamp": utc_now(),
        "policy": ["No Evidence, No Pass"],
        "checks": checks,
        "evidence": evidence,
        "metadata": metadata or {},
    }
    if output:
        write_json(output, result)
    return result


def print_result(result: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    print(f"[{result['gate']}] target={result['target']}")
    for check in result["checks"]:
        print(f"  [{check['status']}] {check['name']}: {check['message']}")
    print(f"[{result['gate']}] status={result['status']}")


def heading_lines(text: str) -> list[str]:
    return [line.strip().lower() for line in text.splitlines() if line.strip().startswith("#")]


def has_any(headings: list[str], keywords: list[str]) -> bool:
    lowered = [keyword.lower() for keyword in keywords]
    return any(keyword in heading for heading in headings for keyword in lowered)


def body_for(text: str, keywords: list[str]) -> str:
    lines = text.splitlines()
    capture = False
    level = 0
    buffer: list[str] = []
    lowered = [keyword.lower() for keyword in keywords]
    for line in lines:
        match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if match:
            if capture and len(match.group(1)) <= level:
                break
            if any(keyword in match.group(2).lower() for keyword in lowered):
                capture = True
                level = len(match.group(1))
                continue
        if capture:
            buffer.append(line)
    return "\n".join(buffer).strip()


def markdown_section_gate(
    gate: str,
    target: Path,
    required: dict[str, list[str]],
    recommended: dict[str, list[str]] | None = None,
) -> tuple[str, list[dict[str, Any]]]:
    text = read_text(target)
    headings = heading_lines(text)
    checks: list[dict[str, Any]] = []
    for name, keywords in required.items():
        passed = has_any(headings, keywords)
        checks.append({
            "name": name,
            "status": "PASS" if passed else "FAIL",
            "message": "section found" if passed else f"missing section keywords: {', '.join(keywords)}",
        })
    for name, keywords in (recommended or {}).items():
        passed = has_any(headings, keywords)
        checks.append({
            "name": name,
            "status": "PASS" if passed else "WARN",
            "message": "section found" if passed else f"recommended section missing: {', '.join(keywords)}",
        })
    return worst_status([check["status"] for check in checks]), checks


def check_spec(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target)
    required = {
        "overview": ["overview", "background", "需求概述", "背景"],
        "goals": ["goal", "目标", "核心目标"],
        "success_metrics": ["success", "metric", "验收指标", "成功指标"],
        "functional_scope": ["function", "feature", "功能", "范围"],
        "acceptance_criteria": ["acceptance", "验收标准"],
        "risks_assumptions": ["risk", "assumption", "风险", "假设"],
    }
    status, checks = markdown_section_gate("check-spec", target, required)
    text = read_text(target) if target.exists() else ""
    acceptance = body_for(text, ["acceptance", "验收标准"])
    quantifiable = bool(re.search(r"[%<>≥≤]|\b\d+\b|ms|second|minute|至少|不低于|不超过", acceptance))
    checks.append({
        "name": "quantifiable_acceptance",
        "status": "PASS" if quantifiable else "FAIL",
        "message": "acceptance criteria contain measurable terms"
        if quantifiable else "acceptance criteria need measurable numbers or thresholds",
    })
    ambiguous = [
        word for word in ["maybe", "roughly", "possibly", "尽量", "适当", "可能", "大概"]
        if word.lower() in text.lower()
    ]
    if ambiguous:
        checks.append({
            "name": "ambiguous_language",
            "status": "WARN",
            "message": "ambiguous terms found: " + ", ".join(sorted(set(ambiguous))),
        })
    status = worst_status([status] + [check["status"] for check in checks])
    return finalize_result(
        gate="check-spec",
        target=target,
        status=status,
        checks=checks,
        evidence=[evidence_for_path(target)],
        output=args.output,
    )


def check_design(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target)
    required = {
        "architecture": ["architecture", "system design", "架构", "系统设计"],
        "module_boundaries": ["module", "component", "模块", "组件"],
        "data_or_api_contract": ["api", "contract", "data", "接口", "数据", "契约"],
        "rollback_compatibility": ["rollback", "compatibility", "回滚", "兼容"],
    }
    recommended = {
        "tradeoffs": ["tradeoff", "alternative", "权衡", "备选"],
        "test_strategy": ["test", "validation", "测试", "验证"],
    }
    status, checks = markdown_section_gate("check-design", target, required, recommended)
    evidence = [evidence_for_path(target)]
    if args.spec:
        evidence.append(evidence_for_path(Path(args.spec)))
    return finalize_result(
        gate="check-design",
        target=target,
        status=status,
        checks=checks,
        evidence=evidence,
        output=args.output,
    )


def check_risk(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target)
    required = {
        "risk_inventory": ["risk", "风险"],
        "mitigation": ["mitigation", "control", "应对", "缓解", "控制"],
        "decision": ["decision", "conclusion", "结论", "准入"],
    }
    status, checks = markdown_section_gate("check-risk", target, required)
    text = read_text(target) if target.exists() else ""
    unresolved_l0 = re.search(r"\bL0\b|\bcritical\b|高危|严重", text, re.IGNORECASE)
    mitigated = re.search(r"mitigated|accepted|approved|已缓解|已审批|已接受|有应对", text, re.IGNORECASE)
    if unresolved_l0 and not mitigated:
        checks.append({
            "name": "l0_unresolved",
            "status": "BLOCK",
            "message": "L0/critical risk appears without mitigation or explicit approval.",
        })
    status = worst_status([status] + [check["status"] for check in checks])
    return finalize_result(
        gate="check-risk",
        target=target,
        status=status,
        checks=checks,
        evidence=[evidence_for_path(target)],
        output=args.output,
    )


def run_git_diff_check(root: Path) -> tuple[str, str]:
    try:
        completed = subprocess.run(
            ["git", "diff", "--check"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return "WARN", str(exc)
    if completed.returncode == 0:
        return "PASS", completed.stdout.strip()
    return "FAIL", (completed.stdout + completed.stderr).strip()


def check_code_style(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target)
    files = iter_files(target, CODE_STYLE_EXTENSIONS)
    checks: list[dict[str, Any]] = []
    evidence = [evidence_for_path(path) for path in files[:50]]
    if target.exists() and target.is_dir():
        git_status, git_message = run_git_diff_check(target)
        checks.append({
            "name": "git_diff_check",
            "status": git_status,
            "message": git_message or "no whitespace errors in git diff",
        })

    trailing = []
    long_lines = []
    todos = []
    missing_newline = []
    for path in files:
        text = read_text(path)
        lines = text.splitlines()
        if text and not text.endswith("\n"):
            missing_newline.append(str(path))
        for number, line in enumerate(lines, 1):
            if line.rstrip() != line:
                trailing.append(f"{path}:{number}")
            if len(line) > 120:
                long_lines.append(f"{path}:{number}")
            marker_pattern = r"\b(" + "|".join(CODE_MARKERS) + r")\b"
            if re.search(marker_pattern, line):
                todos.append(f"{path}:{number}")

    checks.extend([
        {
            "name": "trailing_whitespace",
            "status": "PASS" if not trailing else "FAIL",
            "message": "none" if not trailing else ", ".join(trailing[:20]),
        },
        {
            "name": "line_length_120",
            "status": "PASS" if not long_lines else "WARN",
            "message": "all checked lines <= 120 chars" if not long_lines else ", ".join(long_lines[:20]),
        },
        {
            "name": "todo_markers",
            "status": "PASS" if not todos else "WARN",
            "message": "none" if not todos else ", ".join(todos[:20]),
        },
        {
            "name": "final_newline",
            "status": "PASS" if not missing_newline else "WARN",
            "message": "all checked files end with newline"
            if not missing_newline else ", ".join(missing_newline[:20]),
        },
    ])
    status = worst_status([check["status"] for check in checks])
    return finalize_result(
        gate="check-code-style",
        target=target,
        status=status,
        checks=checks,
        evidence=evidence,
        output=args.output,
        metadata={"files_checked": len(files)},
    )


SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*['\"][^'\"\s]{16,}['\"]"),
]
RISKY_PATTERNS = [
    re.compile(r"\beval\s*\("),
    re.compile(r"\bexec\s*\("),
]


def check_security(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target)
    files = iter_files(target, TEXT_EXTENSIONS)
    code_files = {path for path in iter_files(target, CODE_STYLE_EXTENSIONS)}
    evidence = [evidence_for_path(path) for path in files[:50]]
    secrets = []
    risky = []
    for path in files:
        text = read_text(path)
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                secrets.append(str(path))
                break
        if path in code_files:
            for pattern in RISKY_PATTERNS:
                if pattern.search(text):
                    risky.append(str(path))
                    break

    checks = [
        {
            "name": "hardcoded_secrets",
            "status": "BLOCK" if secrets else "PASS",
            "message": "none" if not secrets else ", ".join(secrets[:20]),
        },
        {
            "name": "dynamic_code_execution",
            "status": "FAIL" if risky else "PASS",
            "message": "none" if not risky else ", ".join(risky[:20]),
        },
    ]
    status = worst_status([check["status"] for check in checks])
    return finalize_result(
        gate="check-security",
        target=target,
        status=status,
        checks=checks,
        evidence=evidence,
        output=args.output,
        metadata={"files_checked": len(files)},
    )


def check_review_pass(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target)
    text = read_text(target) if target.exists() else ""
    lowered = text.lower()
    approved = any(term in lowered for term in ["approved: true", "status: pass", "结论: pass", "通过"])
    reviewer = any(term in lowered for term in ["reviewer", "审查人", "reviewed_by"])
    open_must = re.search(r"\bmust\b.*\b(open|fail|unresolved)\b|未解决.*must", lowered)
    checks = [
        {
            "name": "reviewer_present",
            "status": "PASS" if reviewer else "FAIL",
            "message": "reviewer is recorded" if reviewer else "reviewer is missing",
        },
        {
            "name": "approval_recorded",
            "status": "PASS" if approved else "FAIL",
            "message": "approval or PASS conclusion found" if approved else "approval/PASS conclusion missing",
        },
        {
            "name": "no_open_must",
            "status": "PASS" if not open_must else "FAIL",
            "message": "no unresolved MUST item" if not open_must else "unresolved MUST item found",
        },
    ]
    return finalize_result(
        gate="check-review-pass",
        target=target,
        status=worst_status([check["status"] for check in checks]),
        checks=checks,
        evidence=[evidence_for_path(target)],
        output=args.output,
    )


def check_test_coverage(args: argparse.Namespace) -> dict[str, Any]:
    target = Path(args.target)
    checks: list[dict[str, Any]] = []
    thresholds = {
        "lines": float(args.lines),
        "branches": float(args.branches),
        "functions": float(args.functions),
    }
    try:
        data = json.loads(read_text(target))
    except (OSError, json.JSONDecodeError) as exc:
        checks.append({"name": "coverage_json_parse", "status": "FAIL", "message": str(exc)})
        return finalize_result(
            gate="check-test-coverage",
            target=target,
            status="FAIL",
            checks=checks,
            evidence=[evidence_for_path(target)],
            output=args.output,
        )

    coverage = data.get("coverage", data)
    for metric, threshold in thresholds.items():
        actual = float(coverage.get(metric, -1))
        checks.append({
            "name": f"{metric}_coverage",
            "status": "PASS" if actual >= threshold else "FAIL",
            "message": f"{actual:g}% >= {threshold:g}%" if actual >= threshold
            else f"{actual:g}% < {threshold:g}%",
        })
    return finalize_result(
        gate="check-test-coverage",
        target=target,
        status=worst_status([check["status"] for check in checks]),
        checks=checks,
        evidence=[evidence_for_path(target)],
        output=args.output,
    )


GATES: dict[str, Callable[[argparse.Namespace], dict[str, Any]]] = {
    "check-spec": check_spec,
    "check-design": check_design,
    "check-risk": check_risk,
    "check-code-style": check_code_style,
    "check-security": check_security,
    "check-review-pass": check_review_pass,
    "check-test-coverage": check_test_coverage,
}


def build_parser(default_gate: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="White Harness evidence-based gate runner")
    if default_gate:
        parser.set_defaults(gate=default_gate)
    else:
        parser.add_argument("gate", choices=sorted(GATES))
    parser.add_argument("target", help="file or directory to check")
    parser.add_argument("--json", action="store_true", help="print JSON result")
    parser.add_argument("--output", type=Path, help="write JSON result to this file")
    parser.add_argument("--spec", help="optional SPEC path for design traceability evidence")
    parser.add_argument("--lines", type=float, default=80)
    parser.add_argument("--branches", type=float, default=70)
    parser.add_argument("--functions", type=float, default=80)
    return parser


def gate_cli(default_gate: str | None = None, argv: list[str] | None = None) -> int:
    args = build_parser(default_gate).parse_args(argv)
    result = GATES[args.gate](args)
    print_result(result, args.json)
    return int(result["exit_code"])


def main() -> None:
    sys.exit(gate_cli())


if __name__ == "__main__":
    main()
