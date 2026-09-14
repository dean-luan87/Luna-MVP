"""Static/governance Verifier for the synthetic A -> B-CR -> A bridge."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path


VERIFIER_PATH = Path(__file__).resolve()
for _candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.a_b_contingency_reasoning_bridge_controlled.a_b_contingency_reasoning_adapter_v1 import build_a_b_contingency_run_v1  # noqa: E402
from capabilities.midplatform.core.cognitive_flow.integration.a_b_contingency_reasoning_bridge_controlled.a_b_contingency_reasoning_registry_v1 import PHASE  # noqa: E402


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[5]
DOC_DIR = REPO_ROOT / "docs" / "architecture" / "phase_luna_a_b_contingency_reasoning_return_bridge_controlled_v1"
EXPECTED_IMPLEMENTATION_FILES = {
    "__init__.py", "a_b_contingency_reasoning_types_v1.py", "a_b_contingency_reasoning_registry_v1.py",
    "a_b_contingency_reasoning_engine_v1.py", "a_b_contingency_reasoning_fixture_v1.py",
    "a_b_contingency_reasoning_adapter_v1.py", "run_a_b_contingency_reasoning_return_bridge_controlled_v1.py",
    "verify_a_b_contingency_reasoning_return_bridge_controlled_v1.py",
}
EXPECTED_DOCUMENTATION_FILES = {
    "phase_contract.md", "implementation_overview_v1.md", "a_to_b_request_boundary_v1.md",
    "derived_b_scope_and_termination_v1.md", "b_to_a_result_return_v1.md", "a_b_result_evaluation_v1.md",
    "ab_concurrency_candidate_boundary_v1.md", "scenario_mapping_v1.json", "negative_guards_v1.md", "change_manifest.md",
}


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


def _check(check_id: str, actual: object, expected: object) -> dict[str, object]:
    return {"check_id": check_id, "actual": actual, "expected": expected, "passed": actual == expected}


def _source_names() -> set[str]:
    return {item.name for item in PACKAGE_DIR.iterdir() if item.is_file() and item.suffix == ".py"}


def _doc_names() -> set[str]:
    return {item.name for item in DOC_DIR.iterdir() if item.is_file() and item.suffix in {".md", ".json"}} if DOC_DIR.is_dir() else set()


def build_verification_summary_v1() -> dict[str, object]:
    payload = build_a_b_contingency_run_v1()
    summary = payload["summary"]
    cases = payload["cases"]
    guards = summary["negative_guards"]
    case = {item["scenario_id"]: item for item in cases}
    checks = [
        _check("phase", summary["phase"], PHASE),
        _check("scenario_cases_ok", summary["all_cases_passed"], True),
        _check("candidate_only", summary["key_guards"]["candidate_only"], True),
        _check("synthetic_only", summary["key_guards"]["synthetic_only"], True),
        _check("a_b_initiation_boundary_ok", all(case[item]["passed"] for item in ("AB-01", "AB-02", "AB-03", "AB-04", "AB-05", "AB-06")), True),
        _check("derived_b_grant_ok", all(case[item]["passed"] for item in ("BG-01", "BG-02", "BG-03", "BG-04", "BG-05", "BG-06")), True),
        _check("b_scope_boundary_ok", all(case[item]["passed"] for item in ("BR-01", "BR-02", "BR-03", "BR-04", "BR-05", "BR-06")), True),
        _check("b_return_boundary_ok", all(case[item]["passed"] for item in ("RT-01", "RT-02", "RT-03", "RT-04")), True),
        _check("a_result_evaluation_ok", all(case[item]["passed"] for item in ("AE-01", "AE-02", "AE-03", "AE-04", "AE-05", "AE-06")), True),
        _check("staleness_handling_ok", all(case[item]["passed"] for item in ("ST-01", "ST-02", "ST-03")), True),
        _check("ab_concurrency_candidate_ok", all(case[item]["passed"] for item in ("CC-01", "CC-02", "CC-03")), True),
        _check("b_no_loop_control_ok", case["RT-02"]["passed"] and guards["b_loop_control"] is False, True),
        _check("b_no_recursive_delegation_ok", guards["b_recursive_delegation"] is False and case["NG-01"]["passed"], True),
        _check("cross_concern_isolation_ok", case["IS-01"]["passed"], True),
        _check("negative_guards_ok", all(value is False for key, value in guards.items() if key not in {"candidate_only", "synthetic_only"}), True),
        _check("source_set_ok", _source_names(), EXPECTED_IMPLEMENTATION_FILES),
        _check("documentation_set_ok", _doc_names(), EXPECTED_DOCUMENTATION_FILES),
    ]
    failed_checks = [item["check_id"] for item in checks if not item["passed"]]
    failed_case_ids = sorted({item["scenario_id"] for item in cases if not item["passed"]})
    return {
        "phase": PHASE, "scenario_count": summary["scenario_count"], "all_checks_passed": not failed_checks,
        "failed_case_ids": failed_case_ids, "failed_checks": failed_checks,
        "scenario_cases_ok": next(item["passed"] for item in checks if item["check_id"] == "scenario_cases_ok"),
        "a_b_initiation_boundary_ok": next(item["passed"] for item in checks if item["check_id"] == "a_b_initiation_boundary_ok"),
        "derived_b_grant_ok": next(item["passed"] for item in checks if item["check_id"] == "derived_b_grant_ok"),
        "b_scope_boundary_ok": next(item["passed"] for item in checks if item["check_id"] == "b_scope_boundary_ok"),
        "b_return_boundary_ok": next(item["passed"] for item in checks if item["check_id"] == "b_return_boundary_ok"),
        "a_result_evaluation_ok": next(item["passed"] for item in checks if item["check_id"] == "a_result_evaluation_ok"),
        "staleness_handling_ok": next(item["passed"] for item in checks if item["check_id"] == "staleness_handling_ok"),
        "ab_concurrency_candidate_ok": next(item["passed"] for item in checks if item["check_id"] == "ab_concurrency_candidate_ok"),
        "b_no_loop_control_ok": next(item["passed"] for item in checks if item["check_id"] == "b_no_loop_control_ok"),
        "b_no_recursive_delegation_ok": next(item["passed"] for item in checks if item["check_id"] == "b_no_recursive_delegation_ok"),
        "cross_concern_isolation_ok": next(item["passed"] for item in checks if item["check_id"] == "cross_concern_isolation_ok"),
        "negative_guards_ok": next(item["passed"] for item in checks if item["check_id"] == "negative_guards_ok"),
        "source_set_ok": next(item["passed"] for item in checks if item["check_id"] == "source_set_ok"),
        "documentation_set_ok": next(item["passed"] for item in checks if item["check_id"] == "documentation_set_ok"),
        "checks": checks,
    }


def main() -> int:
    summary = build_verification_summary_v1()
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["build_verification_summary_v1", "main"]
