"""Deterministic B2 verifier for user-terminal execution."""

from __future__ import annotations

import json
import sys
from pathlib import Path


VERIFY_PATH = Path(__file__).resolve()
REPO_ROOT = next(
    candidate
    for candidate in (VERIFY_PATH, *VERIFY_PATH.parents)
    if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir()
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_state_formation.integration.b2_current_world_cognitive_state_flow_controlled.run_b2_current_world_cognitive_state_flow_controlled_implementation_v1 import (  # noqa: E402
    build_runner_result,
)


IMPLEMENTATION_DIR = VERIFY_PATH.parent
DOC_DIR = REPO_ROOT / "docs/architecture/luna_brain_b2_current_world_cognitive_state_flow_controlled_implementation_v1"
EXPECTED_IMPLEMENTATION_FILES = {
    "b2_current_world_cognitive_state_flow_types_v1.py",
    "b2_current_world_cognitive_state_flow_adapter_v1.py",
    "b2_current_world_cognitive_state_flow_fixture_v1.py",
    "run_b2_current_world_cognitive_state_flow_controlled_implementation_v1.py",
    "verify_b2_current_world_cognitive_state_flow_controlled_implementation_v1.py",
}
EXPECTED_DOC_FILES = {
    "overview_v1.json",
    "implementation_mapping_v1.json",
    "current_world_adapter_contract_v1.json",
    "cognitive_state_contract_mapping_v1.json",
    "attention_hypothesis_boundary_v1.json",
    "observation_need_bridge_v1.json",
    "cognitive_flow_transition_contract_v1.json",
    "trace_provenance_v1.json",
    "differential_validation_v1.json",
    "negative_guards_v1.json",
    "scenario_mapping_v1.json",
    "change_manifest_v1.json",
    "implementation_summary_v1.md",
    "phase_contract.json",
    "verifier_scope_v1.json",
}


def _regular_source_files(directory: Path) -> set[str]:
    return {
        path.name
        for path in directory.iterdir()
        if path.is_file() and path.suffix == ".py" and path.name != "__init__.py"
    }


def _regular_doc_files(directory: Path) -> set[str]:
    return {
        path.name
        for path in directory.iterdir()
        if path.is_file() and path.suffix in {".json", ".md"} and not path.name.startswith(".")
    }


def _check(name: str, expected, actual) -> dict:
    return {"check": name, "expected": expected, "actual": actual, "passed": expected == actual}


def verify() -> dict:
    implementation_actual = _regular_source_files(IMPLEMENTATION_DIR)
    docs_actual = _regular_doc_files(DOC_DIR)
    checks = [
        _check("implementation_file_set", sorted(EXPECTED_IMPLEMENTATION_FILES), sorted(implementation_actual)),
        _check("documentation_file_set", sorted(EXPECTED_DOC_FILES), sorted(docs_actual)),
    ]
    runner = build_runner_result()
    summary = runner["summary"]
    checks.extend([
        _check("scenario_count", 24, summary["b2_scenario_count"]),
        _check("all_cases_passed", True, summary["all_cases_passed"]),
        _check("failed_case_ids", [], summary["failed_case_ids"]),
        _check("real_component", ["REAL_B1_CURRENT_WORLD_INPUT"], summary["real_components"]),
        _check("synthetic_regression_preserved", True, summary["synthetic_regression_preserved"]),
        _check("differential_validation_passed", True, summary["differential_validation_passed"]),
        _check("provider_invocation", False, summary["provider_invocation"]),
        _check("semantic_compression", False, summary["semantic_compression"]),
        _check("dynamic_cognitive_function_execution", False, summary["dynamic_cognitive_function_execution"]),
        _check("world_truth_promoted", False, summary["world_truth_promoted"]),
        _check("hypothesis_as_fact", False, summary["hypothesis_as_fact"]),
        _check("pcn_mutation", False, summary["pcn_mutation"]),
        _check("intent_mutation", False, summary["intent_mutation"]),
        _check("decision_mutation", False, summary["decision_mutation"]),
        _check("task_mutation", False, summary["task_mutation"]),
        _check("action_execution", False, summary["action_execution"]),
        _check("current_world_read_only", True, summary["current_world_read_only"]),
        _check("current_world_direct_mutation", False, summary["current_world_direct_mutation"]),
        _check("field_state_mutation", False, summary["field_state_mutation"]),
        _check("candidate_only", True, summary["candidate_only"]),
    ])
    failed_cases = [
        item["case_id"]
        for item in runner["case_results"]
        if not item["all_checks_passed"]
    ]
    checks.append(_check("case_result_failure_scan", [], failed_cases))
    passed = all(item["passed"] for item in checks)
    result = {
        "phase": "Phase-Luna-Brain-B2-Current-World-Cognitive-State-Flow-Controlled-Implementation-v1-001",
        "failed_check_count": sum(1 for item in checks if not item["passed"]),
        "blocker_count": 0 if passed else 1,
        "all_checks_passed": passed,
        "checks": checks,
        "business_logic_changed": True,
        "provider_invocation": False,
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


if __name__ == "__main__":
    raise SystemExit(0 if verify()["all_checks_passed"] else 1)
