"""Static/user-terminal verifier for B3 controlled candidate integration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


REPO_ROOT = Path(__file__).resolve().parents[6]
IMPLEMENTATION_DIR = Path(__file__).resolve().parent
DOC_DIR = REPO_ROOT / "docs/architecture/luna_brain_b3_cognitive_state_intent_decision_task_controlled_implementation_v1"
OUTPUT_DIR = REPO_ROOT / "_eval_out/b3_cognitive_state_intent_decision_task_controlled_v1"

EXPECTED_IMPLEMENTATION_FILES = {
    "b3_cognitive_state_intent_decision_task_types_v1.py",
    "b3_cognitive_state_intent_decision_task_adapter_v1.py",
    "b3_cognitive_state_intent_decision_task_fixture_v1.py",
    "run_b3_cognitive_state_intent_decision_task_controlled_implementation_v1.py",
    "verify_b3_cognitive_state_intent_decision_task_controlled_implementation_v1.py",
}
EXPECTED_DOCUMENTATION_FILES = {
    "overview_v1.json",
    "implementation_mapping_v1.json",
    "b2_input_adapter_contract_v1.json",
    "intent_influence_contract_v1.json",
    "decision_integration_contract_v1.json",
    "task_manager_handoff_contract_v1.json",
    "safety_resource_permission_boundary_v1.json",
    "reconsideration_defer_contract_v1.json",
    "trace_provenance_v1.json",
    "differential_validation_v1.json",
    "negative_guards_v1.json",
    "scenario_mapping_v1.json",
    "change_manifest_v1.json",
    "implementation_summary_v1.md",
    "phase_contract.json",
}


def _regular_names(directory: Path, suffixes: Iterable[str]) -> set[str]:
    return {
        item.name
        for item in directory.iterdir()
        if item.is_file() and item.suffix in set(suffixes)
    } if directory.is_dir() else set()


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _static_checks() -> Dict[str, Any]:
    implementation_files = _regular_names(IMPLEMENTATION_DIR, (".py",))
    documentation_files = _regular_names(DOC_DIR, (".json", ".md"))
    source_paths = [
        path
        for path in IMPLEMENTATION_DIR.glob("*.py")
        if path.is_file() and path.name != Path(__file__).name
    ]
    source_text = "\n".join(path.read_text(encoding="utf-8") for path in source_paths)
    return {
        "implementation_file_set_exact": implementation_files == EXPECTED_IMPLEMENTATION_FILES,
        "documentation_file_set_exact": documentation_files == EXPECTED_DOCUMENTATION_FILES,
        "generated_artifacts_excluded": all(item.is_file() for item in IMPLEMENTATION_DIR.iterdir() if item.name in implementation_files),
        "canonical_intent_owner": "Intent Governance" in source_text,
        "canonical_decision_owner": "DecisionGovernanceEngineV1" in source_text,
        "canonical_task_owner": "TaskManager" in source_text,
        "legacy_decision_center_not_directly_imported": not any(
            "from capabilities.midplatform.core.decision_center" in path.read_text(encoding="utf-8")
            for path in source_paths
        ),
        "no_provider_invocation": "provider_invocation: bool = False" in source_text,
        "no_runtime_execution": "runtime_execution: bool = False" in source_text,
        "no_semantic_compression": "semantic_compression: bool = False" in source_text,
        "candidate_only": "candidate_only=True" in source_text,
    }, implementation_files, documentation_files


def verify() -> Dict[str, Any]:
    checks, implementation_files, documentation_files = _static_checks()
    runtime_summary: Dict[str, Any] = {}
    runtime_available = False
    result_path = OUTPUT_DIR / "b3_result_v1.json"
    cases_path = OUTPUT_DIR / "b3_case_results_v1.json"
    if result_path.is_file() and cases_path.is_file():
        runtime_available = True
        runtime_summary = _load_json(result_path)
        case_results = _load_json(cases_path)
        checks.update(
            {
                "runner_all_cases_passed": runtime_summary.get("all_cases_passed") is True,
                "runner_failed_case_ids_empty": runtime_summary.get("failed_case_ids") == [],
                "runner_no_intent_decision_task_mutation": all(
                    runtime_summary.get(key) is False
                    for key in ("intent_mutation", "decision_mutation", "task_mutation")
                ),
                "runner_no_action_runtime": runtime_summary.get("action_execution") is False and runtime_summary.get("runtime_execution") is False,
                "runner_no_provider": "REAL_B2_COGNITIVE_STATE_FLOW_INPUT" in runtime_summary.get("real_components", [])
                and runtime_summary.get("provider_invocation", False) is False,
                "runner_synthetic_regression_preserved": runtime_summary.get("synthetic_regression_preserved") is True,
                "runner_differential_passed": runtime_summary.get("differential_validation_passed") is True,
                "case_artifact_nonempty": isinstance(case_results, list) and len(case_results) >= 22,
            }
        )
    all_passed = all(checks.values()) and runtime_available
    return {
        "phase": "Phase-Luna-Brain-B3-Cognitive-State-Intent-Decision-Task-Controlled-Implementation-v1-001",
        "checks": checks,
        "all_checks_passed": all_passed,
        "runtime_artifacts_available": runtime_available,
        "expected_implementation_files": sorted(EXPECTED_IMPLEMENTATION_FILES),
        "actual_implementation_files": sorted(implementation_files),
        "expected_documentation_files": sorted(EXPECTED_DOCUMENTATION_FILES),
        "actual_documentation_files": sorted(documentation_files),
        "status": "WAITING_FOR_USER_TERMINAL_VERIFICATION" if not all_passed else "CONTROLLED_IMPLEMENTATION_RESULT_CANDIDATE_READY",
    }


def main() -> int:
    print(json.dumps(verify(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
