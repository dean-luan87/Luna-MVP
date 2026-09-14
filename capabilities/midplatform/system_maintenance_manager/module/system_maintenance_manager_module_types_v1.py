from __future__ import annotations

from typing import Any, Dict

MODULE_SCHEMA_VERSION = "system_maintenance_manager_module_v1"
CAPABILITY_ID = "luna.system_maintenance_manager"

SUPPORTED_ANOMALY_TYPES = {
    "module_integration_failure",
    "module_runtime_anomaly",
    "unexpected_module_status",
    "trace_missing",
    "replay_mismatch",
    "determinism_drift",
    "boundary_violation",
    "protocol_version_drift",
    "protocol_schema_mismatch",
    "protocol_deprecation_conflict",
    "model_asset_missing",
    "model_asset_unavailable",
    "model_admission_failure",
    "model_capability_mismatch",
    "model_resource_insufficient",
    "model_ownership_conflict",
    "dependency_unavailable",
    "baseline_behavior_drift",
    "manifest_registry_mismatch",
    "baseline_registry_mismatch",
    "unknown_anomaly",
}

SUPPORTED_RUNTIME_MODES = {"NORMAL_RUNTIME", "CALIBRATION", "REBASELINE"}

MODULE_STATUSES = {
    "invalid_input",
    "diagnostic_ready",
    "fault_localized",
    "fault_partially_localized",
    "baseline_drift_detected",
    "protocol_drift_detected",
    "model_asset_issue_detected",
    "dependency_issue_detected",
    "multiple_fault_domains_detected",
    "manual_review_required",
    "no_fault_detected",
    "insufficient_evidence",
    "internal_error",
}

FAULT_DOMAINS = {
    "input_contract",
    "module_logic",
    "status_reduction",
    "protocol_contract",
    "model_asset",
    "dependency",
    "baseline_drift",
    "registry_drift",
    "trace_replay",
    "permission_boundary",
    "resource",
    "unknown",
}

BOUNDARY_FALSE_FIELDS = (
    "module_code_modified",
    "protocol_modified",
    "model_asset_modified",
    "baseline_modified",
    "registry_modified",
    "dependency_modified",
    "task_execution_executed",
    "model_switch_executed",
    "rollback_executed",
    "runtime_recovery_executed",
    "production_action_executed",
)


def not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}
