"""Static/governance verifier for candidate-only grant mechanics."""

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

from capabilities.midplatform.core.cognitive_flow.integration.authority_grant_mechanical_command_controlled.authority_grant_mechanical_command_adapter_v1 import (  # noqa: E402
    PHASE,
    build_authority_grant_run_v1,
)


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[5]
DOC_DIR = REPO_ROOT / "docs" / "architecture" / "phase_luna_cognitive_capability_authority_grant_controlled_implementation_v1"

EXPECTED_IMPLEMENTATION_FILES = {
    "__init__.py",
    "authority_grant_mechanical_command_types_v1.py",
    "authority_grant_mechanical_command_registry_v1.py",
    "authority_grant_mechanical_command_engine_v1.py",
    "authority_grant_mechanical_command_fixture_v1.py",
    "authority_grant_mechanical_command_adapter_v1.py",
    "run_candidate_only_authority_grant_and_mechanical_command_adapter_v1.py",
    "verify_candidate_only_authority_grant_and_mechanical_command_adapter_v1.py",
}

EXPECTED_DOCUMENTATION_FILES = {
    "phase_contract.md",
    "implementation_overview_v1.md",
    "authority_grant_runtime_boundary_v1.md",
    "loop_mechanical_validation_v1.md",
    "derived_b_grant_v1.md",
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
    return {
        "check_id": check_id,
        "actual": actual,
        "expected": expected,
        "passed": actual == expected,
    }


def build_verification_summary_v1() -> dict[str, object]:
    payload = build_authority_grant_run_v1()
    summary = payload["summary"]
    cases = payload["cases"]
    guards = summary["negative_guards"]
    checks = [
        _check("phase", summary["phase"], PHASE),
        _check("scenario_count", summary["scenario_count"], 36),
        _check("scenario_cases_ok", summary["all_cases_passed"], True),
        _check("authority_boundary_ok", summary["capability_boundary_violation_count"] >= 4, True),
        _check("grant_scope_ok", summary["rejected_grant_count"] >= 5, True),
        _check("mechanical_command_boundary_ok", summary["accepted_mechanical_command_count"] >= 8 and summary["rejected_mechanical_command_count"] >= 1, True),
        _check("derived_b_grant_ok", summary["derived_b_grant_count"] == 1, True),
        _check("revocation_expiry_ok", summary["revoked_grant_count"] == 1 and summary["expired_grant_count"] == 1, True),
        _check("responsibility_binding_ok", all(item["passed"] for item in cases if item["scenario_id"].startswith("RB-")), True),
        _check("negative_guards_ok", all(value is False for value in guards.values()), True),
        _check("candidate_only", summary["key_guards"]["candidate_only"], True),
        _check("synthetic_only", summary["key_guards"]["synthetic_only"], True),
        _check("loop_no_semantic_authority", summary["key_guards"]["loop_has_no_semantic_authority"], True),
        _check("source_set_ok", _source_names(), EXPECTED_IMPLEMENTATION_FILES),
        _check("documentation_set_ok", _doc_names(), EXPECTED_DOCUMENTATION_FILES),
    ]
    failed_checks = [item["check_id"] for item in checks if not item["passed"]]
    failed_case_ids = sorted({item["scenario_id"] for item in cases if not item["passed"]})
    return {
        "phase": PHASE,
        "all_checks_passed": not failed_checks,
        "failed_case_ids": failed_case_ids,
        "failed_checks": failed_checks,
        "scenario_cases_ok": next(item["passed"] for item in checks if item["check_id"] == "scenario_cases_ok"),
        "authority_boundary_ok": next(item["passed"] for item in checks if item["check_id"] == "authority_boundary_ok"),
        "grant_scope_ok": next(item["passed"] for item in checks if item["check_id"] == "grant_scope_ok"),
        "mechanical_command_boundary_ok": next(item["passed"] for item in checks if item["check_id"] == "mechanical_command_boundary_ok"),
        "derived_b_grant_ok": next(item["passed"] for item in checks if item["check_id"] == "derived_b_grant_ok"),
        "revocation_expiry_ok": next(item["passed"] for item in checks if item["check_id"] == "revocation_expiry_ok"),
        "responsibility_binding_ok": next(item["passed"] for item in checks if item["check_id"] == "responsibility_binding_ok"),
        "negative_guards_ok": next(item["passed"] for item in checks if item["check_id"] == "negative_guards_ok"),
        "source_set_ok": next(item["passed"] for item in checks if item["check_id"] == "source_set_ok"),
        "documentation_set_ok": next(item["passed"] for item in checks if item["check_id"] == "documentation_set_ok"),
        "scenario_count": summary["scenario_count"],
        "checks": checks,
    }


def main() -> int:
    summary = build_verification_summary_v1()
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["build_verification_summary_v1", "main"]
