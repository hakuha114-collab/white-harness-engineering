#!/usr/bin/env python3
"""Executable test-coverage gate wrapper."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.gates import gate_cli


if __name__ == "__main__":
    sys.exit(gate_cli("check-test-coverage"))
