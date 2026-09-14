"""Independent verifier for declaration baseline and non-execution guards."""

from __future__ import annotations

from pathlib import Path

from capabilities.midplatform.core.cognitive_flow.integration.governed_capability_execution_record_production_controlled.producer_v1 import (
    inspect_repository_declarations_v1,
)
from capabilities.midplatform.model_manager.model_contract_repository.yolo11n_readiness.yolo11n_readiness_types_v1 import (
    YOLO11N_ASSET_ID,
    YOLO11N_CAPABILITY_ID,
)

from .validator_v1 import TARGET_PROVIDER_FAMILY, validate_declaration_baseline_v1


def verify_declaration_baseline_v1(root: Path) -> dict:
    result = validate_declaration_baseline_v1(root)
    producer_inventory = inspect_repository_declarations_v1(
        root,
        target_model_asset_id=YOLO11N_ASSET_ID,
        target_capability_contract_id=YOLO11N_CAPABILITY_ID,
        target_provider_family=TARGET_PROVIDER_FAMILY,
    )
    checks = dict(result["checks"])
    checks.update(
        {
            "no_runtime_admission_created": result["runtime_admission_created"] is False,
            "no_executable_candidate_created": result["executable_candidate_created"] is False,
            "no_model_loading": result["model_loading"] is False,
            "no_provider_invocation": result["provider_invocation"] is False,
            "no_observation_action": result["observation_execution"] is False and result["action_execution"] is False,
            "no_source_mutation": result["source_mutation"] is False,
            "no_world_truth": result["world_truth_declared"] is False,
            "producer_detects_slot_declaration": producer_inventory.capability_slot_declaration_found,
            "producer_detects_model_declaration": producer_inventory.model_registry_entry_found,
            "producer_detects_capability_model_binding": producer_inventory.capability_model_declaration_found,
            "producer_detects_provider_declaration": producer_inventory.provider_registry_entry_found,
            "producer_detects_model_provider_binding": producer_inventory.model_provider_declaration_found,
            "producer_remaining_missing_only_runtime": producer_inventory.missing_declarations == ("RUNTIME_ADMISSION_PRODUCTION_SOURCE",),
        }
    )
    return {
        "phase": result["phase"],
        "declaration_baseline_ok": all(checks.values()),
        "checks": checks,
        "remaining_missing_declaration": list(producer_inventory.missing_declarations),
        "source_refs": result["source_refs"],
        "runtime_executed": False,
        "model_loaded": False,
        "provider_invoked": False,
    }


__all__ = ["verify_declaration_baseline_v1"]
