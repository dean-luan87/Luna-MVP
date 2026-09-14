from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.model_manager.module.model_manager_module_api_v1 import (
    run_model_manager_module_api_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_model_asset_result_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    anomaly_type = str(input_candidate.get("anomaly_type") or "")
    check_expected = anomaly_type in {
        "model_asset_missing",
        "model_asset_unavailable",
        "model_admission_failure",
        "model_capability_mismatch",
        "model_resource_insufficient",
        "model_ownership_conflict",
    }
    if not bool(input_candidate.get("model_asset_check_allowed")):
        return {
            "schema_version": "system_maintenance_model_asset_adapter_v1",
            "model_asset_result": {
                "check_expected": check_expected,
                "model_check_executed": False,
                "model_identity_exists": None,
                "model_admitted": None,
                "model_available": None,
                "capability_match": None,
                "resource_fit": None,
                "ownership_valid": None,
                "fallback_available": None,
                "lifecycle_status": None,
                "result_status": "model_asset_healthy",
            },
            **not_fact(),
        }

    payload = {
        "request_id": f"model_chk_{input_candidate.get('maintenance_request_id')}",
        "requested_capability": "maintenance.analysis",
        "task_ref": input_candidate.get("maintenance_request_id"),
        "device_ref": "maintenance_device",
        "region_ref": "maintenance_region",
        "resource_snapshot": {"memory_mb": 4096, "cpu_cores": 4},
        "version_snapshot": input_candidate.get("source_module_version")
        or {"target": "v1"},
        "trace_context": {
            "source_capability_id": input_candidate.get("source_capability_id")
        },
    }
    mm = run_model_manager_module_api_v1(payload)
    status = str(mm.get("module_status") or "")
    ownership = dict(mm.get("ownership_decision") or {})
    resources = dict(mm.get("resource_evaluation") or {})
    selected = dict(mm.get("selected_model_candidate") or {})
    fallback = tuple(mm.get("fallback_candidates") or ())

    if anomaly_type == "model_asset_missing":
        result_status = "model_asset_unavailable"
    elif anomaly_type == "model_capability_mismatch":
        result_status = "model_asset_mismatch"
    elif anomaly_type == "model_ownership_conflict":
        result_status = "model_asset_ownership_conflict"
    elif anomaly_type == "model_resource_insufficient":
        result_status = "model_asset_degraded"
    elif anomaly_type in {"model_asset_unavailable", "model_admission_failure"}:
        result_status = "model_asset_unavailable"
    elif not selected and fallback:
        result_status = "model_fallback_candidate"
    else:
        result_status = "model_asset_healthy"

    return {
        "schema_version": "system_maintenance_model_asset_adapter_v1",
        "model_asset_result": {
            "check_expected": check_expected,
            "model_check_executed": True,
            "model_identity_exists": bool(selected) or bool(fallback),
            "model_admitted": status not in {"admission_rejected", "invalid_input"},
            "model_available": status not in {"unavailable", "invalid_input"},
            "capability_match": anomaly_type != "model_capability_mismatch",
            "resource_fit": bool(resources.get("resource_ok", True)),
            "ownership_valid": bool(ownership.get("ownership_ok", True)),
            "fallback_available": bool(fallback),
            "lifecycle_status": str(
                (mm.get("lifecycle_plan") or {}).get("availability_state") or "unknown"
            ),
            "result_status": result_status,
            "model_manager_module_status": status,
        },
        **not_fact(),
    }
