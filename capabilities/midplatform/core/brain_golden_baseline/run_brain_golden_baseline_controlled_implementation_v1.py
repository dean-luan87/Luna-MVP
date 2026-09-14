"""Metadata-only B5 governance runner; it never runs phase suites."""

from __future__ import annotations

import json
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from capabilities.midplatform.core.brain_golden_baseline.brain_golden_baseline_fixture_v1 import build_cases
    from capabilities.midplatform.core.brain_golden_baseline.brain_golden_baseline_governance_v1 import load_baseline_snapshot, normalized_phase_index, validate_baseline
else:
    from .brain_golden_baseline_fixture_v1 import build_cases
    from .brain_golden_baseline_governance_v1 import load_baseline_snapshot, normalized_phase_index, validate_baseline


def build_runner_result() -> dict[str, object]:
    cases = build_cases()
    outcomes = {case_id: bool(check()) for case_id, check in cases.items()}
    failed = [case_id for case_id, passed in outcomes.items() if not passed]
    snapshot = load_baseline_snapshot()
    consistency_issues = validate_baseline(snapshot)
    return {
        "phase": "Phase-Luna-Brain-B5-Real-Evidence-Cognitive-Loop-Golden-Baseline-Controlled-Implementation-v1-001",
        "mode": "GOVERNANCE_ONLY",
        "owner": "Brain Golden Baseline Governance",
        "scenario_count": len(outcomes),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "baseline_id": snapshot.manifest["manifest_id"],
        "baseline_version": snapshot.manifest["baseline_version"],
        "phase_membership": snapshot.manifest["phase_set"],
        "regression_execution_requested": False,
        "business_logic_execution": False,
        "provider_invocation": False,
        "model_inference": False,
        "runtime_execution": False,
        "automatic_regression_execution": False,
        "consistency_issue_count": len(consistency_issues),
        "consistency_issues": [issue.__dict__ for issue in consistency_issues],
        "normalized_phase_boundaries": list(normalized_phase_index(snapshot)),
        "governance_cases": outcomes,
    }


if __name__ == "__main__":
    print(json.dumps(build_runner_result(), indent=2, sort_keys=True))
