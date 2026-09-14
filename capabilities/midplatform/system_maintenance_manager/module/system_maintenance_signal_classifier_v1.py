from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    not_fact,
)


def build_system_maintenance_signal_classification_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    anomaly_type = str(input_candidate.get("anomaly_type") or "")
    domain_map = {
        "trace_missing": "trace_replay",
        "replay_mismatch": "trace_replay",
        "determinism_drift": "trace_replay",
        "boundary_violation": "permission_boundary",
        "protocol_version_drift": "protocol_contract",
        "protocol_schema_mismatch": "protocol_contract",
        "protocol_deprecation_conflict": "protocol_contract",
        "model_asset_missing": "model_asset",
        "model_asset_unavailable": "model_asset",
        "model_admission_failure": "model_asset",
        "model_capability_mismatch": "model_asset",
        "model_resource_insufficient": "resource",
        "model_ownership_conflict": "model_asset",
        "dependency_unavailable": "dependency",
        "baseline_behavior_drift": "baseline_drift",
        "manifest_registry_mismatch": "registry_drift",
        "baseline_registry_mismatch": "registry_drift",
        "module_integration_failure": "module_logic",
        "module_runtime_anomaly": "module_logic",
        "unexpected_module_status": "status_reduction",
        "unknown_anomaly": "unknown",
    }
    severity = "medium"
    if anomaly_type in {
        "boundary_violation",
        "protocol_schema_mismatch",
        "model_asset_missing",
        "model_asset_unavailable",
    }:
        severity = "high"
    return {
        "schema_version": "system_maintenance_signal_classifier_v1",
        "anomaly_type": anomaly_type,
        "fault_domain_hint": domain_map.get(anomaly_type, "unknown"),
        "severity_hint": severity,
        "insufficient_evidence": not bool(input_candidate.get("diagnostics")),
        **not_fact(),
    }
