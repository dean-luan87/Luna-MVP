"""Deterministic verifier for the controlled Universal Slot foundation."""

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

from capabilities.midplatform.model_manager.registries.universal_capability_slot.universal_capability_slot_fixture_v1 import (  # noqa: E402
    build_runner_result,
)


PACKAGE_ROOT = Path(__file__).resolve().parent
DOC_ROOT = REPO_ROOT / "docs" / "architecture" / "phase_luna_brain_universal_capability_slot_official_capability_foundation_controlled_implementation_v1"
EXPECTED_SOURCE_FILES = {
    "__init__.py",
    "universal_capability_slot_types_v1.py",
    "universal_capability_slot_governance_v1.py",
    "universal_capability_slot_resolution_v1.py",
    "universal_capability_slot_fixture_v1.py",
    "run_universal_capability_slot_official_capability_foundation_controlled_v1.py",
    "verify_universal_capability_slot_official_capability_foundation_controlled_v1.py",
}
EXPECTED_DOC_FILES = {
    "overview.md",
    "implementation_mapping.md",
    "universal_slot_contract.md",
    "official_module_contract.md",
    "admission_binding_contract.md",
    "resolution_invocation_contract.md",
    "capability_self_mapping.md",
    "brain_regulation_boundary.md",
    "safety_baseline_boundary.md",
    "scenario_mapping.md",
    "negative_guards.json",
    "change_manifest.md",
    "phase_contract.md",
    "implementation_summary.md",
    "verifier.md",
}
NEGATIVE_FALSE_FIELDS = (
    "runtime_execution",
    "real_provider_invocation",
    "model_inference",
    "real_download",
    "real_install",
    "real_activation",
    "real_upgrade",
    "real_rollback",
    "brain_direct_capability_mutation",
    "user_direct_capability_mutation",
    "safety_baseline_bypass",
    "slot_semantic_authority",
    "slot_world_truth_authority",
    "module_world_truth_authority",
    "parallel_capability_registry",
    "parallel_model_manager",
    "parallel_capability_self_owner",
    "specialized_universal_slot",
    "learning_execution",
    "memory_mutation",
    "knowledge_implementation",
    "srsk_implementation",
    "semantic_folding_execution",
    "semantic_expansion_execution",
    "market_capability_implementation",
    "capability_value_scoring",
    "automatic_capability_optimization",
    "automatic_capability_uninstall",
    "automatic_capability_acquisition",
)


def verify() -> dict[str, object]:
    result = build_runner_result()
    source_files = {path.name for path in PACKAGE_ROOT.iterdir() if path.is_file()}
    doc_files = {path.name for path in DOC_ROOT.iterdir() if path.is_file()} if DOC_ROOT.exists() else set()
    source_set_ok = EXPECTED_SOURCE_FILES.issubset(source_files)
    doc_set_ok = EXPECTED_DOC_FILES.issubset(doc_files)
    guard_ok = all(result.get(field) is False for field in NEGATIVE_FALSE_FIELDS)
    cases_ok = bool(result.get("all_cases_passed")) and result.get("scenario_count") == 30
    return {
        "phase": result["phase"],
        "source_set_ok": source_set_ok,
        "documentation_set_ok": doc_set_ok,
        "scenario_count": result["scenario_count"],
        "scenario_cases_ok": cases_ok,
        "negative_guards_ok": guard_ok,
        "candidate_only": result.get("candidate_only") is True,
        "all_checks_passed": source_set_ok and doc_set_ok and cases_ok and guard_ok,
        "failed_case_ids": result.get("failed_case_ids", []),
        "runtime_execution": False,
        "provider_invocation": False,
        "model_inference": False,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
