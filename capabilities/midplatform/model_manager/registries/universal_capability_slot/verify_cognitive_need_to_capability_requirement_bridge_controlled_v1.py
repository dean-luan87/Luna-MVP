"""Deterministic verifier for the candidate-only cognitive Need bridge."""

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

from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_fixture_v1 import (  # noqa: E402
    build_runner_result,
)


PACKAGE_ROOT = Path(__file__).resolve().parent
DOC_ROOT = REPO_ROOT / "docs" / "architecture" / "phase_luna_cognitive_need_to_capability_requirement_bridge_controlled_implementation_v1"
EXPECTED_SOURCE_FILES = {
    "cognitive_need_capability_requirement_bridge_types_v1.py",
    "cognitive_need_capability_requirement_bridge_governance_v1.py",
    "cognitive_need_capability_requirement_bridge_fixture_v1.py",
    "run_cognitive_need_to_capability_requirement_bridge_controlled_v1.py",
    "verify_cognitive_need_to_capability_requirement_bridge_controlled_v1.py",
}
EXPECTED_DOC_FILES = {
    "overview.md",
    "ownership.md",
    "cognitive_need_contract.md",
    "requirement_formation_contract.md",
    "minimum_sufficient_requirement.md",
    "scope_replanning_boundary.md",
    "safety_boundary.md",
    "existing_asset_reuse.md",
    "scenario_mapping.md",
    "negative_guards.json",
    "change_manifest.md",
    "verification_instructions.md",
    "phase_contract.md",
    "implementation_summary.md",
    "verifier.md",
    "provisional_cognitive_plan_boundary.md",
    "minimum_next_requirement_boundary.md",
    "sufficiency_continuation_boundary.md",
    "state_version_reconsideration_boundary.md",
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
    "automatic_capability_optimization",
    "automatic_capability_uninstall",
    "brain_direct_capability_mutation",
    "brain_scope_bypass",
    "brain_model_selection_as_capability_identity",
    "brain_provider_selection_as_capability_identity",
    "authority_escalation",
    "world_truth_authority",
    "action_authority",
    "fallback_hallucination",
    "learning_execution",
    "memory_mutation",
    "semantic_expansion_execution",
    "semantic_folding_execution",
    "srsk_implementation",
    "plan_to_full_execution_commitment",
    "all_plan_steps_auto_materialized",
    "remaining_candidates_binding",
    "requirement_generated_after_sufficiency",
    "obsolete_requirement_forced_execution",
    "sufficiency_stop_counted_as_failure",
    "plan_completion_used_as_goal_success_proxy",
    "safety_bypasses_sufficiency",
    "new_evidence_ignored_for_decision",
)


def verify() -> dict[str, object]:
    result = build_runner_result()
    source_files = {path.name for path in PACKAGE_ROOT.iterdir() if path.is_file()}
    doc_files = {path.name for path in DOC_ROOT.iterdir() if path.is_file()} if DOC_ROOT.exists() else set()
    source_set_ok = EXPECTED_SOURCE_FILES.issubset(source_files)
    documentation_set_ok = EXPECTED_DOC_FILES.issubset(doc_files)
    negative_guards_ok = all(result.get(field) is False for field in NEGATIVE_FALSE_FIELDS)
    scenarios_ok = result.get("scenario_count") == 40 and result.get("all_cases_passed") is True
    bridge_shape_ok = result.get("scope_gate_reused") is True and result.get("resolution_owner_reused") is True
    return {
        "phase": result["phase"],
        "source_set_ok": source_set_ok,
        "documentation_set_ok": documentation_set_ok,
        "scenario_count": result["scenario_count"],
        "scenario_cases_ok": scenarios_ok,
        "bridge_shape_ok": bridge_shape_ok,
        "negative_guards_ok": negative_guards_ok,
        "candidate_only": result.get("candidate_only") is True,
        "all_checks_passed": source_set_ok and documentation_set_ok and scenarios_ok and bridge_shape_ok and negative_guards_ok,
        "failed_case_ids": result.get("failed_case_ids", []),
        "runtime_execution": False,
        "provider_invocation": False,
        "model_inference": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
