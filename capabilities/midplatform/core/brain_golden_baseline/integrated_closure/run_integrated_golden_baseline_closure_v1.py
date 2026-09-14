"""Metadata/evidence closure runner; no regression execution."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
    from capabilities.midplatform.core.brain_golden_baseline.integrated_closure.integrated_closure_fixture_v1 import build_cases
    from capabilities.midplatform.core.brain_golden_baseline.integrated_closure.integrated_closure_governance_v1 import build_closure_result
else:
    from .integrated_closure_fixture_v1 import build_cases
    from .integrated_closure_governance_v1 import build_closure_result


def build_runner_result(evidence_path: Path | None = None) -> dict[str, object]:
    result = build_closure_result(evidence_path)
    cases = {case_id: bool(check()) for case_id, check in build_cases().items()}
    result["scenario_count"] = len(cases)
    result["all_cases_passed"] = not [case_id for case_id, passed in cases.items() if not passed]
    result["failed_case_ids"] = [case_id for case_id, passed in cases.items() if not passed]
    result["closure_scenarios"] = cases
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Metadata-only integrated baseline closure")
    parser.add_argument("--evidence-file", type=Path, default=None)
    args = parser.parse_args()
    print(json.dumps(build_runner_result(args.evidence_file), indent=2, sort_keys=True))

