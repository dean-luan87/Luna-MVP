"""Compact Runner for the synthetic A -> B-CR -> A bridge."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path


RUNNER_PATH = Path(__file__).resolve()
for _candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.a_b_contingency_reasoning_bridge_controlled.a_b_contingency_reasoning_adapter_v1 import build_a_b_contingency_run_v1  # noqa: E402


def _jsonable(value: object) -> object:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_jsonable(item) for item in value), key=str)
    return value


def main() -> int:
    payload = build_a_b_contingency_run_v1()
    summary = payload["summary"]
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main"]
