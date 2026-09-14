"""Direct runner for the candidate-only Loop semantic cutover."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any


RUNNER_PATH = Path(__file__).resolve()
for _candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.loop_semantic_to_mechanical_cutover_controlled.loop_semantic_to_mechanical_cutover_adapter_v1 import (  # noqa: E402
    build_cutover_run_v1,
)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted(_jsonable(item) for item in value)
    return value


def main() -> int:
    summary = build_cutover_run_v1()
    compact = {key: value for key, value in summary.items() if key != "cases"}
    print(json.dumps(_jsonable(compact), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

