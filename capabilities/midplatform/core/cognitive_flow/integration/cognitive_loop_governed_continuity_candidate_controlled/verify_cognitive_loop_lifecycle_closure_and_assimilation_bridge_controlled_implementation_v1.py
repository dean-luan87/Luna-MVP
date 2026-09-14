"""Verifier for candidate-only lifecycle closure and assimilation boundaries."""

from __future__ import annotations

import json
import sys
from pathlib import Path


VERIFIER_PATH = Path(__file__).resolve()
for _candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_lifecycle_closure_adapter_v1 import (  # noqa: E402
    PHASE,
    build_lifecycle_closure_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_lifecycle_closure_engine_v1 import (  # noqa: E402
    NEGATIVE_GUARDS,
)


def _check(check_id: str, actual: object, expected: object) -> dict[str, object]:
    return {
        "check_id": check_id,
        "actual": actual,
        "expected": expected,
        "passed": actual == expected,
    }


def build_verification_summary_v1() -> dict[str, object]:
    summary = build_lifecycle_closure_run_v1()
    checks = [
        _check("phase", summary["phase"], PHASE),
        _check("scenario_cases_ok", summary["all_cases_passed"], True),
        _check("lifecycle_closure_ok", summary["lifecycle_closure_ok"], True),
        _check("final_state_integrity_ok", summary["final_state_integrity_ok"], True),
        _check("brain_assimilation_boundary_ok", summary["brain_assimilation_boundary_ok"], True),
        _check("loop_package_boundary_ok", summary["loop_package_boundary_ok"], True),
        _check("negative_guards_ok", summary["negative_guards_ok"], True),
        _check("candidate_only", summary["candidate_only"], True),
        _check("synthetic_only", summary["synthetic_only"], True),
        _check("runtime_execution", summary["runtime_execution"], False),
        _check("provider_invocation", summary["provider_invocation"], False),
        _check("model_inference", summary["model_inference"], False),
        _check("source_set_ok", summary["source_set_ok"], True),
        _check("documentation_set_ok", summary["documentation_set_ok"], True),
    ]
    for guard_name in NEGATIVE_GUARDS:
        checks.append(_check(f"negative_guard:{guard_name}", summary["negative_guards"].get(guard_name), False))
    failed_checks = list(summary["failed_checks"])
    failed_checks.extend(item["check_id"] for item in checks if not item["passed"])
    failed_case_ids = sorted(set(summary["failed_case_ids"]))
    failed_case_ids.extend(
        item["check_id"].split(":", 1)[0]
        for item in checks
        if not item["passed"] and ":" in item["check_id"] and item["check_id"].split(":", 1)[0].startswith("LC-")
    )
    failed_case_ids = sorted(set(failed_case_ids))
    return {
        "phase": PHASE,
        "scenario_count": summary["scenario_count"],
        "all_checks_passed": not failed_checks,
        "failed_case_ids": failed_case_ids,
        "failed_checks": failed_checks,
        "scenario_cases_ok": summary["all_cases_passed"],
        "negative_guards_ok": summary["negative_guards_ok"] and all(item["passed"] for item in checks if item["check_id"].startswith("negative_guard:")),
        "lifecycle_closure_ok": summary["lifecycle_closure_ok"],
        "final_state_integrity_ok": summary["final_state_integrity_ok"],
        "brain_assimilation_boundary_ok": summary["brain_assimilation_boundary_ok"],
        "loop_package_boundary_ok": summary["loop_package_boundary_ok"],
        "source_set_ok": summary["source_set_ok"],
        "documentation_set_ok": summary["documentation_set_ok"],
    }


def main() -> int:
    summary = build_verification_summary_v1()
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["build_verification_summary_v1", "main"]
