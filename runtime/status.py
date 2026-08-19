"""Gate status and exit-code contract."""

from __future__ import annotations

STATUS_EXIT_CODES = {
    "PASS": 0,
    "FAIL": 1,
    "WARN": 2,
    "BLOCK": 3,
}

EXIT_CODE_STATUS = {value: key for key, value in STATUS_EXIT_CODES.items()}


def normalize_status(status: str) -> str:
    value = status.upper()
    if value not in STATUS_EXIT_CODES:
        raise ValueError(f"unknown gate status: {status}")
    return value


def worst_status(statuses: list[str]) -> str:
    order = {"PASS": 0, "WARN": 1, "FAIL": 2, "BLOCK": 3}
    if not statuses:
        return "PASS"
    return max((normalize_status(status) for status in statuses), key=lambda item: order[item])
