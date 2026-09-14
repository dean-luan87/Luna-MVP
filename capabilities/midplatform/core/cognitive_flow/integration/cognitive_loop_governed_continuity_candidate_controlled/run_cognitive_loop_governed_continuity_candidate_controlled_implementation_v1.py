"""Runner for the synthetic candidate-only Cognitive Loop skeleton."""

from __future__ import annotations

import json
import sys
from pathlib import Path


RUNNER_PATH = Path(__file__).resolve()
for _candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_continuity_candidate_adapter_v1 import (  # noqa: E402
    build_candidate_loop_run_v1,
)


def main() -> int:
    payload = build_candidate_loop_run_v1()
    print(json.dumps(payload["summary"], ensure_ascii=False, sort_keys=True))
    return 0 if payload["summary"]["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main"]
