"""Deterministic verifier for scope/resolution metadata only."""

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

from capabilities.midplatform.model_manager.registries.universal_capability_slot.capability_scope_resolution_fixture_v1 import (  # noqa: E402
    build_runner_result,
)


PACKAGE_ROOT = Path(__file__).resolve().parent
DOC_ROOT = REPO_ROOT / "docs" / "architecture" / "phase_luna_official_capability_resolution_scope_and_invocation_bridge_controlled_implementation_v1"
EXPECTED_SOURCE_FILES = {
    "__init__.py",
    "universal_capability_slot_types_v1.py",
    "universal_capability_slot_governance_v1.py",
    "universal_capability_slot_resolution_v1.py",
    "universal_capability_slot_fixture_v1.py",
    "official_capability_catalog_types_v1.py",
    "official_capability_catalog_governance_v1.py",
    "official_capability_catalog_fixture_v1.py",
    "capability_scope_resolution_fixture_v1.py",
    "run_official_capability_resolution_scope_and_invocation_bridge_controlled_v1.py",
    "verify_official_capability_resolution_scope_and_invocation_bridge_controlled_v1.py",
}
EXPECTED_DOC_FILES = {
    "overview.md",
    "existing_asset_inventory.md",
    "capability_scope_contract.md",
    "capability_requirement_contract.md",
    "scope_validation_contract.md",
    "capability_gap_boundary.md",
    "capability_resolution_flow.md",
    "invocation_bridge_contract.md",
    "capability_self_scope_view.md",
    "brain_scope_boundary.md",
    "csa_scope_boundary.md",
    "reference_chain_ocr.md",
    "reference_chain_object_detection.md",
    "reference_chain_spatial_mapping.md",
    "owner_mutation_matrix.json",
    "negative_guards.json",
    "scenario_suite_v1.json",
    "scope_fixture_contract_reconciliation_v1.json",
    "scenario_mapping.md",
    "change_manifest.md",
    "phase_contract.md",
    "implementation_summary.md",
}
NEGATIVE_FALSE_FIELDS = (
    "runtime_execution", "real_provider_invocation", "provider_invocation", "model_inference", "camera_activation",
    "real_download", "real_install", "real_activation", "real_upgrade", "real_rollback",
    "brain_direct_capability_mutation", "user_direct_capability_mutation", "brain_out_of_scope_capability_request",
    "capability_scope_bypass", "capability_contract_overreach", "capability_output_authority_escalation",
    "provider_extends_module_scope", "model_metadata_extends_module_scope", "csa_extends_module_scope",
    "slot_semantic_authority", "slot_world_truth_authority", "module_world_truth_authority",
    "safety_scope_bypass", "safety_baseline_bypass", "automatic_capability_acquisition",
    "automatic_capability_uninstall", "automatic_capability_optimization", "capability_value_scoring",
    "learning_execution", "memory_mutation", "knowledge_implementation", "srsk_implementation",
    "semantic_folding_execution", "semantic_expansion_execution", "market_capability_implementation",
    "parallel_capability_registry", "parallel_capability_resolver", "parallel_model_manager",
    "parallel_capability_self_owner",
)


def verify() -> dict[str, object]:
    result = build_runner_result()
    source_files = {path.name for path in PACKAGE_ROOT.iterdir() if path.is_file()}
    doc_files = {path.name for path in DOC_ROOT.iterdir() if path.is_file()} if DOC_ROOT.exists() else set()
    source_set_ok = EXPECTED_SOURCE_FILES.issubset(source_files)
    doc_set_ok = EXPECTED_DOC_FILES.issubset(doc_files)
    guard_ok = all(result.get(field) is False for field in NEGATIVE_FALSE_FIELDS)
    structure_ok = result.get("scope_validation_before_invocation") is True and result.get("capability_gap_candidate_supported") is True
    cases_ok = bool(result.get("all_cases_passed")) and result.get("scenario_count") == 35
    return {
        "phase": result["phase"],
        "source_set_ok": source_set_ok,
        "documentation_set_ok": doc_set_ok,
        "scenario_count": result["scenario_count"],
        "scenario_cases_ok": cases_ok,
        "scope_resolution_structure_ok": structure_ok,
        "negative_guards_ok": guard_ok,
        "candidate_only": result.get("candidate_only") is True,
        "all_checks_passed": source_set_ok and doc_set_ok and cases_ok and structure_ok and guard_ok,
        "failed_case_ids": result.get("failed_case_ids", []),
        "runtime_execution": False,
        "provider_invocation": False,
        "model_inference": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
