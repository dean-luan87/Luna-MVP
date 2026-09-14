"""Runner for candidate-only Loop lifecycle closure scenarios."""

from __future__ import annotations

import json
import sys
from pathlib import Path


RUNNER_PATH = Path(__file__).resolve()
for _candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_lifecycle_closure_adapter_v1 import (  # noqa: E402
    build_lifecycle_closure_run_v1,
)


def main() -> int:
    summary = build_lifecycle_closure_run_v1()
    compact_summary = {
        key: summary[key]
        for key in (
            "phase",
            "scenario_count",
            "all_cases_passed",
            "failed_case_ids",
            "key_guards",
            "lifecycle_closure_ok",
            "final_state_integrity_ok",
            "brain_assimilation_boundary_ok",
            "loop_package_boundary_ok",
            "negative_guards_ok",
        )
    }
    print(json.dumps(compact_summary, ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_cases_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["main"]
