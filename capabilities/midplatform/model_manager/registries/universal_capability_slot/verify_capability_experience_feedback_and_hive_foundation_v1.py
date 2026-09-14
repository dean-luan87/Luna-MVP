"""Deterministic verifier for candidate-only capability feedback foundation."""

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

from capabilities.midplatform.model_manager.registries.universal_capability_slot.capability_experience_feedback_fixture_v1 import (  # noqa: E402
    build_runner_result,
)


PACKAGE_ROOT = Path(__file__).resolve().parent
DOC_ROOT = REPO_ROOT / "docs" / "architecture" / "phase_luna_capability_experience_feedback_and_hive_foundation_v1"
EXPECTED_SOURCE_FILES = {
    "universal_capability_slot_types_v1.py",
    "capability_experience_feedback_governance_v1.py",
    "capability_experience_feedback_fixture_v1.py",
    "run_capability_experience_feedback_and_hive_foundation_v1.py",
    "verify_capability_experience_feedback_and_hive_foundation_v1.py",
}
EXPECTED_DOC_FILES = {
    "overview.md",
    "existing_asset_inventory.md",
    "ownership.md",
    "usage_record_contract.md",
    "outcome_assessment_contract.md",
    "individual_experience_aggregation.md",
    "capability_weakness_and_gap.md",
    "capability_self_feedback_boundary.md",
    "hive_feedback_contract.md",
    "privacy_data_minimization_boundary.md",
    "negative_guards.json",
    "scenario_mapping.md",
    "implementation_mapping.md",
    "verification_scope.md",
    "deferred_work.md",
    "change_manifest.md",
    "phase_contract.md",
    "implementation_summary.md",
    "verifier.md",
}
NEGATIVE_FALSE_FIELDS = (
    "runtime_execution",
    "provider_invocation",
    "model_inference",
    "camera_activation",
    "real_download",
    "real_install",
    "real_activation",
    "real_upgrade",
    "real_rollback",
    "automatic_capability_acquisition",
    "automatic_capability_uninstall",
    "automatic_capability_optimization",
    "capability_value_scoring",
    "learning_execution",
    "memory_mutation",
    "semantic_expansion_execution",
    "semantic_folding_execution",
    "srsk_implementation",
    "feedback_mutates_scope",
    "feedback_mutates_lifecycle",
    "feedback_triggers_learning",
    "feedback_triggers_model_replacement",
    "feedback_triggers_provider_replacement",
    "hive_direct_individual_mutation",
    "hive_raw_personal_data_required",
    "weakness_candidate_executes_improvement",
    "gap_candidate_executes_acquisition",
)


def verify() -> dict[str, object]:
    result = build_runner_result()
    source_files = {path.name for path in PACKAGE_ROOT.iterdir() if path.is_file()}
    doc_files = {path.name for path in DOC_ROOT.iterdir() if path.is_file()} if DOC_ROOT.exists() else set()
    source_set_ok = EXPECTED_SOURCE_FILES.issubset(source_files)
    documentation_set_ok = EXPECTED_DOC_FILES.issubset(doc_files)
    negative_guards_ok = all(result.get(field) is False for field in NEGATIVE_FALSE_FIELDS)
    scenarios_ok = result.get("scenario_count") == 26 and result.get("all_cases_passed") is True
    profile_shape_ok = result.get("usage_record_count") == 10 and result.get("profile_count") == 3
    return {
        "phase": result["phase"],
        "source_set_ok": source_set_ok,
        "documentation_set_ok": documentation_set_ok,
        "scenario_count": result["scenario_count"],
        "scenario_cases_ok": scenarios_ok,
        "profile_shape_ok": profile_shape_ok,
        "negative_guards_ok": negative_guards_ok,
        "candidate_only": result.get("candidate_only") is True,
        "all_checks_passed": source_set_ok and documentation_set_ok and scenarios_ok and profile_shape_ok and negative_guards_ok,
        "failed_case_ids": result.get("failed_case_ids", []),
        "runtime_execution": False,
        "provider_invocation": False,
        "model_inference": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
