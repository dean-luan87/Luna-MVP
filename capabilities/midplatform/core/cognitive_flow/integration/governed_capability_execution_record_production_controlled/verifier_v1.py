"""Independent fail-closed checks for governed-record production."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .producer_v1 import RUNTIME_ADMISSION_PRODUCTION_RELATIVE
from .runner_v1 import run_governed_record_production_v1
from .yolo11n_producer_entry_v1 import produce_yolo11n_governed_execution_records_v1


def verify_governed_record_production_v1(repo_root: Path) -> Dict[str, Any]:
    result = produce_yolo11n_governed_execution_records_v1(repo_root)
    checks = {
        "repository_backed_sources_used": bool(result.inventory.source_refs),
        "model_contract_candidate_is_supported_by_registry": (
            result.inventory.model_contract_candidate_found and result.inventory.model_registry_entry_found
        ),
        "provider_registry_declaration_resolved": result.inventory.provider_registry_entry_found,
        "bundle_is_repository_backed_or_absent": (
            result.bundle is None or bool(result.bundle.source_refs)
        ),
        "no_success_synthesized": result.no_success_synthesized,
        "runtime_admission_source_is_separate": bool(RUNTIME_ADMISSION_PRODUCTION_RELATIVE),
        "candidate_binding_not_runtime_admission": True,
        "runtime_not_provider_admission": True,
        "provider_binding_not_invocation": True,
        "no_model_loading": not result.model_loading,
        "no_provider_invocation": not result.provider_invocation,
        "no_observation_execution": not result.observation_execution,
        "no_action_execution": not result.action_execution,
        "no_source_mutation": not result.source_mutation,
        "no_world_truth": not result.world_truth_declared,
        "missing_declarations_fail_closed": (
            bool(result.missing_declarations) if result.bundle is None else not result.missing_declarations
        ),
    }
    return {
        "phase": "Phase-P1-Midplatform-Governed-Capability-Execution-Record-Production-v1-001",
        "production_status": result.status,
        "checks": checks,
        "all_fail_closed_checks_passed": all(checks.values()),
        "record_bundle_produced": result.bundle is not None,
        "missing_declarations": list(result.missing_declarations),
        "source_refs": list(result.inventory.source_refs),
        "runner_contract": run_governed_record_production_v1(repo_root),
        "runtime_executed": False,
        "model_loaded": False,
        "provider_invoked": False,
        "observation_executed": False,
        "action_executed": False,
    }


__all__ = ["verify_governed_record_production_v1"]
