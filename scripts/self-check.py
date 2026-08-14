#!/usr/bin/env python3
"""Run repository-local Harness 2.0 checks."""

from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON_FILES = [
    *sorted((ROOT / "runtime").glob("*.py")),
    *sorted((ROOT / "scripts").glob("*.py")),
    *sorted((ROOT / "scripts").glob("*/*.py")),
]


def compile_python() -> None:
    for path in PYTHON_FILES:
        py_compile.compile(str(path), doraise=True)


def run_unittest() -> None:
    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=ROOT, check=True)


def run_gate_samples() -> None:
    samples = [
        ["scripts/check-spec/check_spec.py", "tests/fixtures/SPEC_PASS.md", "--json"],
        ["scripts/check-design/check_design.py", "tests/fixtures/DESIGN_PASS.md", "--json"],
        ["scripts/check-risk/check_risk.py", "tests/fixtures/RISK_PASS.md", "--json"],
        ["scripts/check-review-pass/check_review_pass.py", "tests/fixtures/review_pass.md", "--json"],
        ["scripts/check-test-coverage/check_test_coverage.py", "tests/fixtures/coverage_pass.json", "--json"],
    ]
    for sample in samples:
        subprocess.run([sys.executable, *sample], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)


def main() -> int:
    compile_python()
    run_unittest()
    run_gate_samples()
    print("self-check PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
