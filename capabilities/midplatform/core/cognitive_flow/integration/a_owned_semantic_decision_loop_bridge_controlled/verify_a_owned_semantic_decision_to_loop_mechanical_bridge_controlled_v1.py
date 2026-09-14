"""Static/governance verifier for the A semantic migration seam."""

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

from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_adapter_v1 import (  # noqa: E402
    build_a_owned_semantic_decision_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_registry_v1 import (  # noqa: E402
    PHASE,
)


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[5]
DOC_DIR = REPO_ROOT / "docs" / "architecture" / "phase_luna_a_owned_semantic_decision_to_loop_mechanical_bridge_controlled_v1"

EXPECTED_IMPLEMENTATION_FILES = {
    "__init__.py",
    "a_owned_semantic_decision_types_v1.py",
    "a_owned_semantic_decision_registry_v1.py",
    "a_owned_semantic_decision_engine_v1.py",
    "a_owned_semantic_decision_fixture_v1.py",
    "a_owned_semantic_decision_adapter_v1.py",
    "run_a_owned_semantic_decision_to_loop_mechanical_bridge_controlled_v1.py",
    "verify_a_owned_semantic_decision_to_loop_mechanical_bridge_controlled_v1.py",
}

EXPECTED_DOCUMENTATION_FILES = {
    "phase_contract.md",
    "implementation_overview_v1.md",
    "semantic_authority_migration_v1.md",
    "dynamic_flow_compatibility_wrapper_v1.md",
    "a_to_loop_mechanical_mapping_v1.md",
    "scenario_mapping_v1.json",
    "negative_guards_v1.md",
    "change_manifest.md",
}


def _jsonable(value: object) -> object:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (set, frozenset)):
        items = [_jsonable(item) for item in value]
        return sorted(items, key=lambda item: str(item))
    return value


def _source_names() -> set[str]:
    return {item.name for item in PACKAGE_DIR.iterdir() if item.is_file() and item.suffix == ".py"}


def _doc_names() -> set[str]:
    return {item.name for item in DOC_DIR.iterdir() if item.is_file() and item.suffix in {".md", ".json"}} if DOC_DIR.is_dir() else set()


def _check(check_id: str, actual: object, expected: object) -> dict[str, object]:
    return {"check_id": check_id, "actual": actual, "expected": expected, "passed": actual == expected}


def build_verification_summary_v1() -> dict[str, object]:
    payload = build_a_owned_semantic_decision_run_v1()
    summary = payload["summary"]
    cases = payload["cases"]
    negative_guards = summary["negative_guards"]
    decision_cases = [item for item in cases if any(key in item for key in ("need_decision", "sufficiency_decision", "reconsideration_decision", "next_step_decision"))]
    checks = [
        _check("phase", summary["phase"], PHASE),
        _check("scenario_count", summary["scenario_count"], 36),
        _check("scenario_cases_ok", summary["all_cases_passed"], True),
        _check("a_semantic_authority_ok", all(item.get("failure_class") is not None or item.get("a_semantic_authority", True) for item in decision_cases), True),
        _check("grant_validation_ok", all(item.get("failure_class") in {None, "AUTHORITY_NOT_GRANTED", "STALE_STATE_VERSION", "SCOPE_MISMATCH", "GRANT_REVOKED", "GRANT_EXPIRED"} and all(value in {None, "SCOPE_MISMATCH", "GRANT_REVOKED", "GRANT_EXPIRED"} for value in item.get("additional_failure_classes", [])) for item in decision_cases), True),
        _check("compatibility_mapping_ok", summary["compatibility_mapped_output_count"] == 4, True),
        _check("mechanical_bridge_ok", summary["accepted_mechanical_command_count"] >= 8, True),
        _check("loop_semantic_boundary_ok", all(item.get("loop_semantic_boundary", True) for item in cases), True),
        _check("cross_concern_isolation_ok", all(item["passed"] for item in cases if item["scenario_id"].startswith("IS-")), True),
        _check("negative_guards_ok", all(value is False for value in negative_guards.values()), True),
        _check("source_set_ok", _source_names(), EXPECTED_IMPLEMENTATION_FILES),
        _check("documentation_set_ok", _doc_names(), EXPECTED_DOCUMENTATION_FILES),
    ]
    failed_checks = [item["check_id"] for item in checks if not item["passed"]]
    failed_case_ids = sorted(item["scenario_id"] for item in cases if not item["passed"])
    return {
        "phase": PHASE,
        "scenario_count": summary["scenario_count"],
        "all_checks_passed": not failed_checks,
        "failed_case_ids": failed_case_ids,
        "failed_checks": failed_checks,
        "scenario_cases_ok": next(item["passed"] for item in checks if item["check_id"] == "scenario_cases_ok"),
        "a_semantic_authority_ok": next(item["passed"] for item in checks if item["check_id"] == "a_semantic_authority_ok"),
        "grant_validation_ok": next(item["passed"] for item in checks if item["check_id"] == "grant_validation_ok"),
        "compatibility_mapping_ok": next(item["passed"] for item in checks if item["check_id"] == "compatibility_mapping_ok"),
        "mechanical_bridge_ok": next(item["passed"] for item in checks if item["check_id"] == "mechanical_bridge_ok"),
        "loop_semantic_boundary_ok": next(item["passed"] for item in checks if item["check_id"] == "loop_semantic_boundary_ok"),
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
