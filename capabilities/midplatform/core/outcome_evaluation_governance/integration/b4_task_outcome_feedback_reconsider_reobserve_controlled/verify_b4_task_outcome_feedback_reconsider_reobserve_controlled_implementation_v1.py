"""Deterministic static/governance verifier for B4 controlled integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[5]
if __package__ in {None, ""} and str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.outcome_evaluation_governance.integration.b4_task_outcome_feedback_reconsider_reobserve_controlled.run_b4_task_outcome_feedback_reconsider_reobserve_controlled_implementation_v1 import (  # noqa: E402
    build_runner_result,
)


EXPECTED_IMPLEMENTATION_FILES = {
    "__init__.py",
    "b4_task_outcome_feedback_reconsider_reobserve_types_v1.py",
    "b4_task_outcome_feedback_reconsider_reobserve_adapter_v1.py",
    "b4_task_outcome_feedback_reconsider_reobserve_fixture_v1.py",
    "run_b4_task_outcome_feedback_reconsider_reobserve_controlled_implementation_v1.py",
    "verify_b4_task_outcome_feedback_reconsider_reobserve_controlled_implementation_v1.py",
}

EXPECTED_DOCUMENTATION_FILES = {
    "overview.json",
    "implementation_mapping.json",
    "b3_input_adapter_contract.json",
    "task_action_boundary.json",
    "controlled_runtime_result_contract.json",
    "outcome_input_mapping.json",
    "outcome_evaluation_contract.json",
    "task_feedback_contract.json",
    "cognitive_reconsideration_contract.json",
    "reobserve_observation_need_boundary.json",
    "retry_recovery_boundary.json",
    "safety_resource_permission_boundary.json",
    "trace_provenance.json",
    "differential_validation.json",
    "negative_guards.json",
    "scenario_mapping.json",
    "change_manifest.json",
    "implementation_summary.md",
    "phase_contract.json",
    "verifier.json",
}


def _regular_source_names(path: Path) -> set[str]:
    return {
        item.name
        for item in path.iterdir()
        if item.is_file() and item.suffix == ".py"
    }


def _regular_doc_names(path: Path) -> set[str]:
    return {
        item.name
        for item in path.iterdir()
        if item.is_file() and item.suffix in {".json", ".md"}
    }


def build_verifier_result() -> dict:
    summary = build_runner_result()
    doc_dir = REPO_ROOT / "docs/architecture/luna_brain_b4_task_outcome_feedback_reconsider_reobserve_controlled_implementation_v1"
    actual_implementation = _regular_source_names(PACKAGE_DIR)
    actual_docs = _regular_doc_names(doc_dir)
    checks = {
        "exact_implementation_file_set": actual_implementation == EXPECTED_IMPLEMENTATION_FILES,
        "exact_documentation_file_set": actual_docs == EXPECTED_DOCUMENTATION_FILES,
        "scenario_suite_passed": summary["b4_scenario_count"] == 28 and summary["all_cases_passed"] and not summary["failed_case_ids"],
        "synthetic_regression_preserved": summary["synthetic_regression_preserved"],
        "real_b3_input_only_real_component": summary["real_components"] == ["REAL_B3_TASK_DECISION_INPUT"],
        "task_manager_owner_preserved": summary["task_lifecycle_owner_preserved"],
        "controlled_runtime_fixture": summary["runtime_result_is_fixture"] and summary["controlled_runtime_result_created"],
        "no_action_execution": summary["action_execution"] is False,
        "no_runtime_execution": summary["runtime_execution"] is False,
        "no_provider_invocation": summary["provider_invocation"] is False,
        "outcome_candidate_only": summary["outcome_world_truth"] is False and summary["candidate_only"] is True,
        "external_success_not_verified": summary["external_success_verified"] is False,
        "reconsideration_and_reobserve_candidate_only": summary["reconsideration_candidate_created"] and summary["reobserve_candidate_created"],
        "no_automatic_retry": summary["automatic_retry"] is False,
        "no_memory_or_learning": not summary["memory_write"] and not summary["experience_learning"] and not summary["online_learning"],
        "no_semantic_compression": summary["semantic_compression"] is False,
        "no_dynamic_cognitive_function": summary["dynamic_cognitive_function_execution"] is False,
        "differential_validation_passed": summary["differential_validation_passed"],
        "lineage_preserved": summary["provenance_chain_complete"] and summary["temporal_refs_preserved"] and summary["uncertainty_refs_preserved"],
    }
    failures = [name for name, passed in checks.items() if not passed]
    return {
        "phase": summary["phase"],
        "mode": "CONTROLLED_B4_VERIFIER",
        "checks": checks,
        "failed_check_names": failures,
        "failed_check_count": len(failures),
        "blocker_count": len(failures),
        "expected_implementation_files": sorted(EXPECTED_IMPLEMENTATION_FILES),
        "actual_implementation_files": sorted(actual_implementation),
        "expected_documentation_files": sorted(EXPECTED_DOCUMENTATION_FILES),
        "actual_documentation_files": sorted(actual_docs),
        "business_logic_execution": False,
    }


if __name__ == "__main__":
    print(json.dumps(build_verifier_result(), indent=2, sort_keys=True))

