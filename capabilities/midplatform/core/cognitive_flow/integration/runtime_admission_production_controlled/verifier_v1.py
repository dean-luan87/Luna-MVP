"""Independent static/controlled checks for Runtime Admission production."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from capabilities.midplatform.core.cognitive_flow.integration.governed_capability_execution_record_production_controlled.producer_v1 import (
    RUNTIME_ADMISSION_PRODUCTION_MARKER,
    RUNTIME_ADMISSION_PRODUCTION_RELATIVE,
)
from capabilities.midplatform.core.cognitive_flow.integration.governed_capability_execution_record_production_controlled.yolo11n_producer_entry_v1 import (
    produce_yolo11n_governed_execution_records_v1,
)

from .runner_v1 import run_runtime_admission_production_v1


def verify_runtime_admission_production_v1(repo_root: Path) -> Dict[str, Any]:
    result = produce_yolo11n_governed_execution_records_v1(repo_root)
    source_file = repo_root / RUNTIME_ADMISSION_PRODUCTION_RELATIVE / "producer_v1.py"
    source_text = source_file.read_text(encoding="utf-8") if source_file.is_file() else ""
    bundle = result.bundle
    checks = {
        "runtime_admission_owner_ok": "Runtime Admission" in source_text and result.inventory.runtime_admission_source_found,
        "repository_backed_inputs_ok": bool(bundle and bundle.source_refs and all((repo_root / ref).is_file() for ref in bundle.source_refs)),
        "executable_candidate_condition_ok": bool(bundle and bundle.runtime_admission_assessment and bundle.runtime_admission_assessment.admission_status == "READY_FOR_EXECUTABLE_CANDIDATE" and bundle.executable_capability),
        "capability_binding_preserved": bool(bundle and bundle.capability_model_binding and bundle.capability_model_binding.authority_owner == "Capability Governance"),
        "model_identity_preserved": bool(bundle and bundle.capability_model_binding and bundle.model_provider_binding and bundle.capability_model_binding.model_asset_ref == bundle.model_provider_binding.model_asset_ref),
        "provider_binding_preserved": bool(bundle and bundle.model_provider_binding and bundle.model_provider_binding.authority_owner == "Provider Governance"),
        "version_lineage_ok": bool(bundle and bundle.source_version_refs and bundle.capability_model_binding and bundle.model_provider_binding and bundle.runtime_admission_version),
        "invalidation_ok": bool(bundle and not bundle.invalidation_refs),
        "grant_permission_safety_resource_constraints_ok": bool(bundle and bundle.grant_refs and bundle.constraint_refs),
        "no_provider_admission": bool(bundle and not bundle.provider_invocation_executed),
        "no_model_loading": bool(bundle and not bundle.model_loading_executed),
        "no_provider_invocation": bool(bundle and not bundle.provider_invocation_executed),
        "no_observation_execution": bool(bundle and not bundle.observation_execution_executed),
        "no_action_execution": bool(bundle and not bundle.action_execution_executed),
        "no_source_mutation": bool(bundle and not bundle.source_mutation_executed),
        "no_world_truth": bool(bundle and not bundle.world_truth_declared),
        "no_success_synthesis": result.no_success_synthesized and RUNTIME_ADMISSION_PRODUCTION_MARKER in source_text,
        "positive_and_fail_closed_cases_pass": run_runtime_admission_production_v1(repo_root)["all_cases_passed"],
    }
    return {
        "phase": "Phase-P1-Midplatform-Runtime-Admission-Production-Source-v1-001",
        "production_status": result.status,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "record_bundle_produced": bundle is not None,
        "missing_declarations": list(result.missing_declarations),
        "runtime_executed": False,
        "model_loaded": False,
        "provider_invoked": False,
        "observation_executed": False,
        "action_executed": False,
    }


__all__ = ["verify_runtime_admission_production_v1"]


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[6]
    print(json.dumps(verify_runtime_admission_production_v1(root), ensure_ascii=False, indent=2))
