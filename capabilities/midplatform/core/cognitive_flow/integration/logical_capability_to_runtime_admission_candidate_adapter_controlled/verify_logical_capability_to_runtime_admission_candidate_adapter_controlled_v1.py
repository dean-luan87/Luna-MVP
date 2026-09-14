"""Static/candidate-only verifier for the Runtime Admission seam."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict


VERIFIER_PATH = Path(__file__).resolve()
PACKAGE_DIR = VERIFIER_PATH.parent
for _candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        REPO_ROOT = _candidate
        sys.path.insert(0, str(_candidate))
        break
else:  # pragma: no cover - direct entry guard
    REPO_ROOT = VERIFIER_PATH.parents[7]

from capabilities.midplatform.core.cognitive_flow.integration.logical_capability_to_runtime_admission_candidate_adapter_controlled.logical_capability_runtime_admission_fixture_v1 import (  # noqa: E402
    build_runtime_admission_run_v1,
)


EXPECTED_SOURCE_SET = {
    "__init__.py",
    "logical_capability_runtime_admission_types_v1.py",
    "logical_capability_runtime_admission_adapter_v1.py",
    "logical_capability_runtime_admission_fixture_v1.py",
    "run_logical_capability_to_runtime_admission_candidate_adapter_controlled_v1.py",
    "verify_logical_capability_to_runtime_admission_candidate_adapter_controlled_v1.py",
}
DOC_DIR = REPO_ROOT / "docs" / "architecture" / "phase_luna_logical_capability_to_runtime_admission_candidate_adapter_controlled_v1"
EXPECTED_DOC_SET = {
    "phase_contract.md",
    "implementation_overview_v1.md",
    "logical_resolution_input_boundary_v1.md",
    "runtime_admission_candidate_mapping_v1.md",
    "executable_capability_candidate_boundary_v1.md",
    "readiness_evidence_reuse_v1.md",
    "provider_admission_handoff_boundary_v1.md",
    "terminal_trial_compatibility_mapping_v1.md",
    "scenario_mapping_v1.json",
    "negative_guards_v1.md",
    "change_manifest.md",
}


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


def _check(check_id: str, passed: bool, actual: Any = None, expected: Any = True) -> Dict[str, Any]:
    return {"check_id": check_id, "passed": bool(passed), "actual": actual, "expected": expected}


def build_verification_summary_v1() -> Dict[str, Any]:
    run = build_runtime_admission_run_v1()
    cases = run["cases"]
    source_set = {item.name for item in PACKAGE_DIR.iterdir() if item.is_file() and item.suffix == ".py"}
    documentation_set = {item.name for item in DOC_DIR.iterdir() if item.is_file()} if DOC_DIR.is_dir() else set()
    checks = [
        _check("scenario_cases_ok", run["all_cases_passed"], run["failed_case_ids"], []),
        _check("logical_resolution_boundary_ok", all(case["logical_resolution_status"] != "READY_CANDIDATE" or case["assessment_status"] != "UNAVAILABLE_CANDIDATE" for case in cases), True),
        _check("runtime_admission_boundary_ok", run["key_guards"]["runtime_admission_required"], True),
        _check("model_manager_boundary_ok", all(case["candidate_only"] for case in cases), True),
        _check("diagnostics_evidence_boundary_ok", run["key_guards"]["no_runtime_probe"], True),
        _check("integrity_boundary_ok", run["key_guards"]["no_runtime_probe"], True),
        _check("permission_resource_safety_boundary_ok", run["key_guards"]["existing_owners_preserved"], True),
        _check("executable_candidate_boundary_ok", all(not case["executable_created"] or case["assessment_status"] == "READY_FOR_EXECUTABLE_CANDIDATE" for case in cases), True),
        _check("provider_boundary_ok", all(not case["provider_invocation_authorized"] for case in cases), True),
        _check("staleness_boundary_ok", all(case["assessment_status"] != "READY_FOR_EXECUTABLE_CANDIDATE" for case in cases if case["kind"] in {"logical_stale", "integrity_stale", "source_stale", "dependency_stale", "governance_stale", "state_isolation"}), True),
        _check("cross_capability_isolation_ok", all(case["passed"] for case in cases if case["kind"] in {"resolution_isolation", "model_isolation", "state_isolation"}), True),
        _check("negative_guards_ok", all(run["key_guards"].values()), True),
        _check("source_set_ok", source_set == EXPECTED_SOURCE_SET, sorted(source_set), sorted(EXPECTED_SOURCE_SET)),
        _check("documentation_set_ok", documentation_set == EXPECTED_DOC_SET, sorted(documentation_set), sorted(EXPECTED_DOC_SET)),
    ]
    failed_checks = [item["check_id"] for item in checks if not item["passed"]]
    return {
        "phase": run["phase"],
        "scenario_count": run["scenario_count"],
        "checks": checks,
        "failed_checks": failed_checks,
        "all_checks_passed": not failed_checks,
        "source_set_diagnostic": {"actual": sorted(source_set), "expected": sorted(EXPECTED_SOURCE_SET)},
        "documentation_set_diagnostic": {"actual": sorted(documentation_set), "expected": sorted(EXPECTED_DOC_SET)},
    }


def main() -> int:
    summary = build_verification_summary_v1()
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
