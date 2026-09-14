"""Static-contract Verifier for the working-envelope bridge."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Iterable

VERIFIER_PATH = Path(__file__).resolve()
for _candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
        break

from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.a_working_envelope_cognitive_requirement_adapter_v1 import build_runner_result  # noqa: E402
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.a_working_envelope_cognitive_requirement_registry_v1 import (  # noqa: E402
    NEGATIVE_GUARDS,
    ROLE_A,
)


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[5]
DOC_DIR = REPO_ROOT / "docs" / "architecture" / "phase_luna_a_working_envelope_cognitive_requirement_bridge_controlled_v1"
EXPECTED_SOURCE_SET = {
    "__init__.py",
    "a_working_envelope_cognitive_requirement_adapter_v1.py",
    "a_working_envelope_cognitive_requirement_engine_v1.py",
    "a_working_envelope_cognitive_requirement_fixture_v1.py",
    "a_working_envelope_cognitive_requirement_registry_v1.py",
    "a_working_envelope_cognitive_requirement_types_v1.py",
    "run_a_working_envelope_cognitive_requirement_bridge_controlled_v1.py",
    "verify_a_working_envelope_cognitive_requirement_bridge_controlled_v1.py",
}
EXPECTED_DOC_SET = {
    "phase_contract.md",
    "implementation_overview_v1.md",
    "working_envelope_boundary_v1.md",
    "environment_change_and_impact_v1.md",
    "a_cognitive_requirement_contract_v1.md",
    "capability_requirement_bridge_v1.md",
    "observation_admission_and_evidence_return_v1.md",
    "task_experience_boundary_v1.md",
    "loop_reference_only_boundary_v1.md",
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
        return sorted((_jsonable(item) for item in value), key=lambda item: str(item))
    return value


def _case_group_ok(cases: Iterable[Dict[str, Any]], prefix: str) -> bool:
    selected = [case for case in cases if case["case_id"].startswith(prefix)]
    return bool(selected) and all(case["passed"] for case in selected)


def _docs_ok() -> bool:
    return DOC_DIR.is_dir() and {path.name for path in DOC_DIR.iterdir() if path.is_file()} == EXPECTED_DOC_SET


def _sources_ok() -> bool:
    return {path.name for path in PACKAGE_DIR.iterdir() if path.is_file() and path.suffix == ".py"} == EXPECTED_SOURCE_SET


def main() -> int:
    result = build_runner_result()
    cases = list(result["cases"])
    failed_case_ids = list(result["failed_case_ids"])
    checks: Dict[str, bool] = {
        "scenario_cases_ok": result["all_cases_passed"],
        "working_envelope_boundary_ok": _case_group_ok(cases, "WE-"),
        "environment_impact_authority_ok": _case_group_ok(cases, "EI-"),
        "a_requirement_authority_ok": _case_group_ok(cases, "NR-"),
        "capability_bridge_ok": _case_group_ok(cases, "CB-"),
        "scope_owner_ok": all(case["passed"] for case in cases if case["case_id"].startswith("CB-")),
        "resolution_owner_ok": all(case["passed"] for case in cases if case["case_id"].startswith("CB-")),
        "observation_admission_boundary_ok": _case_group_ok(cases, "OB-"),
        "evidence_return_boundary_ok": _case_group_ok(cases, "ER-"),
        "invalidation_boundary_ok": _case_group_ok(cases, "IV-"),
        "task_boundary_ok": all(NEGATIVE_GUARDS[key] is False for key in ("task_need_authority", "task_capability_selection")),
        "experience_boundary_ok": all(NEGATIVE_GUARDS[key] is False for key in ("experience_world_truth", "experience_direct_need_selection")),
        "loop_boundary_ok": all(NEGATIVE_GUARDS[key] is False for key in ("loop_requirement_creation", "loop_capability_selection", "loop_observation_request", "loop_evidence_judgment")),
        "cross_concern_isolation_ok": _case_group_ok(cases, "IS-"),
        "negative_guards_ok": all(value is True or value is False for value in NEGATIVE_GUARDS.values()),
        "source_set_ok": _sources_ok(),
        "documentation_set_ok": _docs_ok(),
    }
    failed_checks = [name for name, passed in checks.items() if not passed]
    summary = {
        "phase": result["phase"],
        "scenario_count": result["scenario_count"],
        "all_checks_passed": not failed_checks,
        "failed_case_ids": failed_case_ids,
        "failed_checks": failed_checks,
        **checks,
    }
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if not failed_checks else 1


if __name__ == "__main__":
    sys.exit(main())
