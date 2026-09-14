"""Static/candidate-only verifier for the Loop semantic cutover."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple


VERIFIER_PATH = Path(__file__).resolve()
for _candidate in (VERIFIER_PATH, *VERIFIER_PATH.parents):
    if (_candidate / "capabilities").is_dir() and (_candidate / "docs").is_dir():
        sys.path.insert(0, str(_candidate))
        REPOSITORY_ROOT = _candidate
        break
else:  # pragma: no cover - direct execution always finds the repository root
    REPOSITORY_ROOT = VERIFIER_PATH.parents[7]

from capabilities.midplatform.core.cognitive_flow.integration.loop_semantic_to_mechanical_cutover_controlled.loop_semantic_to_mechanical_cutover_adapter_v1 import (  # noqa: E402
    build_cutover_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.loop_semantic_to_mechanical_cutover_controlled.loop_semantic_to_mechanical_cutover_registry_v1 import (  # noqa: E402
    PHASE,
)


PACKAGE_DIR = VERIFIER_PATH.parent
DOC_DIR = REPOSITORY_ROOT / "docs" / "architecture" / "phase_luna_loop_semantic_to_mechanical_cutover_controlled_v1"
EXPECTED_SOURCES = {
    "__init__.py",
    "loop_semantic_to_mechanical_cutover_types_v1.py",
    "loop_semantic_to_mechanical_cutover_registry_v1.py",
    "loop_semantic_to_mechanical_cutover_engine_v1.py",
    "loop_semantic_to_mechanical_cutover_fixture_v1.py",
    "loop_semantic_to_mechanical_cutover_adapter_v1.py",
    "run_loop_semantic_to_mechanical_cutover_controlled_v1.py",
    "verify_loop_semantic_to_mechanical_cutover_controlled_v1.py",
}
EXPECTED_DOCS = {
    "phase_contract.md",
    "implementation_overview_v1.md",
    "resume_semantic_cutover_v1.md",
    "local_disposition_cutover_v1.md",
    "closure_reason_cutover_v1.md",
    "continuity_semantic_boundary_v1.md",
    "legacy_loop_compatibility_v1.md",
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


def _check(check_id: str, actual: bool) -> Tuple[str, bool]:
    return check_id, bool(actual)


def _source_set_ok() -> bool:
    return {item.name for item in PACKAGE_DIR.iterdir() if item.is_file()} == EXPECTED_SOURCES


def _documentation_set_ok() -> bool:
    return DOC_DIR.is_dir() and {item.name for item in DOC_DIR.iterdir() if item.is_file()} == EXPECTED_DOCS


def build_verification_summary_v1() -> Dict[str, Any]:
    run = build_cutover_run_v1()
    cases = run["cases"]
    resume = [case for case in cases if case["family"] == "RESUME"]
    local = [case for case in cases if case["family"] == "LOCAL"]
    closure = [case for case in cases if case["family"] == "CLOSURE"]
    continuity = [case for case in cases if case["family"] == "CONTINUITY"]
    isolation = [case for case in cases if case["family"] == "ISOLATION"]
    checks = dict(
        (
            _check("scenario_cases_ok", run["all_cases_passed"]),
            _check("resume_authority_boundary_ok", all(case["checks"].get("resume_authority_boundary_ok", False) for case in resume)),
            _check("local_disposition_boundary_ok", all(case["checks"].get("local_disposition_boundary_ok", False) for case in local)),
            _check("closure_reason_boundary_ok", all(case["checks"].get("closure_reason_boundary_ok", False) for case in closure)),
            _check("continuity_semantic_boundary_ok", all(case["checks"].get("continuity_semantic_boundary_ok", False) for case in continuity)),
            _check("mechanical_mapping_ok", all(case["checks"].get("mechanical_mapping_ok", True) for case in cases if "mechanical_mapping_ok" in case["checks"])),
            _check("grant_validation_ok", all(case["checks"].get("grant_validation_ok", False) for case in cases if "grant_validation_ok" in case["checks"])),
            _check("cross_concern_isolation_ok", all(case["checks"].get("cross_concern_isolation_ok", False) for case in isolation)),
            _check("legacy_compatibility_boundary_ok", all(case["checks"].get("legacy_compatibility_boundary_ok", True) for case in cases)),
            _check("negative_guards_ok", all(run["key_guards"].values()) and run["negative_guards"]["legacy_loop_semantic_authority"] is False),
            _check("source_set_ok", _source_set_ok()),
            _check("documentation_set_ok", _documentation_set_ok()),
        )
    )
    failed_checks = tuple(name for name, passed in checks.items() if not passed)
    failed_cases = tuple(case["scenario_id"] for case in cases if not case["passed"])
    return {
        "phase": PHASE,
        "scenario_count": run["scenario_count"],
        "all_checks_passed": not failed_checks and not failed_cases,
        "failed_case_ids": failed_cases,
        "failed_checks": failed_checks,
        **checks,
    }


def main() -> int:
    summary = build_verification_summary_v1()
    print(json.dumps(_jsonable(summary), ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
