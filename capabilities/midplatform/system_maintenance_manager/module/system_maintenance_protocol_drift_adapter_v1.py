from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.protocol_manager.module.protocol_manager_module_api_v1 import (
    run_protocol_manager_module_v1,
)
from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_protocol_drift_result_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    anomaly_type = str(input_candidate.get("anomaly_type") or "")
    check_expected = anomaly_type in {
        "protocol_version_drift",
        "protocol_schema_mismatch",
        "protocol_deprecation_conflict",
        "manifest_registry_mismatch",
    }
    if not bool(input_candidate.get("protocol_drift_check_allowed")):
        return {
            "schema_version": "system_maintenance_protocol_drift_adapter_v1",
            "protocol_drift_result": {
                "check_expected": check_expected,
                "protocol_check_executed": False,
                "protocol_exists": None,
                "protocol_version_supported": None,
                "schema_compatible": None,
                "error_namespace_valid": None,
                "deprecation_conflict": None,
                "migration_required": None,
                "runtime_boundary_valid": None,
            },
            **not_fact(),
        }

    operation = "validate"
    if anomaly_type == "protocol_deprecation_conflict":
        operation = "deprecate"
    payload = {
        "protocol_request_id": f"proto_chk_{input_candidate.get('maintenance_request_id')}",
        "operation": operation,
        "protocol_id": str(
            (input_candidate.get("protocol_refs") or ("",))[0] or "maintenance.protocol"
        ),
        "protocol_version": str(input_candidate.get("source_module_version") or "v1"),
        "consumer_capability_id": str(
            input_candidate.get("source_capability_id")
            or "luna.system_maintenance_manager"
        ),
        "provider_capability_id": "luna.protocol_manager",
        "error_namespace_ref": "maintenance.error.namespace",
    }
    pm = run_protocol_manager_module_v1(payload)
    comp = dict(pm.get("compatibility_candidate") or {})
    reg = dict(pm.get("registry_lookup") or {})
    err = dict(pm.get("error_namespace_report") or {})

    result = {
        "check_expected": check_expected,
        "protocol_check_executed": True,
        "protocol_exists": bool(reg.get("protocol_exists", False)),
        "protocol_version_supported": str(comp.get("compatibility_result") or "")
        != "version_mismatch",
        "schema_compatible": str(comp.get("compatibility_result") or "")
        != "schema_mismatch",
        "error_namespace_valid": bool(err.get("error_namespace_valid", True)),
        "deprecation_conflict": str(comp.get("compatibility_result") or "")
        == "deprecation_conflict",
        "migration_required": str(comp.get("compatibility_result") or "")
        in {"version_mismatch", "deprecation_conflict"},
        "runtime_boundary_valid": bool(
            (pm.get("boundary_report") or {}).get("boundary_preserved", True)
        ),
        "protocol_manager_module_status": str(pm.get("module_status") or ""),
    }
    return {
        "schema_version": "system_maintenance_protocol_drift_adapter_v1",
        "protocol_drift_result": result,
        **not_fact(),
    }
