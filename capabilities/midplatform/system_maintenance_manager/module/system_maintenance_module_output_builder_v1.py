from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.system_maintenance_manager.module.system_maintenance_manager_module_types_v1 import (
    BOUNDARY_FALSE_FIELDS,
    CAPABILITY_ID,
)


def resolve_system_maintenance_module_status_v1(
    input_candidate: Mapping[str, Any],
    signal_classification: Mapping[str, Any],
    anomaly_correlation: Mapping[str, Any],
    baseline_calibration: Mapping[str, Any],
    protocol_result: Mapping[str, Any],
    model_result: Mapping[str, Any],
    dependency_impact: Mapping[str, Any],
) -> str:
    if not input_candidate.get("maintenance_request_id") or not input_candidate.get(
        "anomaly_type_supported"
    ):
        return "invalid_input"
    if signal_classification.get("insufficient_evidence") and not input_candidate.get(
        "trace_ref"
    ):
        return "insufficient_evidence"

    domains = tuple(anomaly_correlation.get("fault_domains") or ())
    baseline_result = str(
        baseline_calibration.get("baseline_calibration_result") or "baseline_match"
    )
    if baseline_result in {
        "baseline_drift_candidate",
        "baseline_version_mismatch",
        "rebaseline_candidate",
    }:
        return "baseline_drift_detected"
    if baseline_result == "baseline_missing":
        return "manual_review_required"

    proto = dict(protocol_result.get("protocol_drift_result") or {})
    if bool(proto.get("protocol_check_executed", False)) and (
        bool(proto.get("deprecation_conflict"))
        or not bool(proto.get("schema_compatible", True))
        or bool(proto.get("migration_required"))
    ):
        return "protocol_drift_detected"

    model = dict(model_result.get("model_asset_result") or {})
    if str(model.get("result_status") or "") in {
        "model_asset_degraded",
        "model_asset_unavailable",
        "model_asset_mismatch",
        "model_asset_ownership_conflict",
        "model_fallback_candidate",
    }:
        return "model_asset_issue_detected"

    if bool(
        (dependency_impact.get("dependency_impact") or {}).get(
            "dependency_unavailable", False
        )
    ):
        return "dependency_issue_detected"

    if len(domains) > 1:
        return "multiple_fault_domains_detected"

    if input_candidate.get("anomaly_type") == "unknown_anomaly":
        return "manual_review_required"
    if input_candidate.get("anomaly_type") == "module_runtime_anomaly":
        return "fault_partially_localized"
    if input_candidate.get("anomaly_type") == "unexpected_module_status":
        return "fault_localized"
    if input_candidate.get("anomaly_type") == "module_integration_failure":
        return "fault_localized"
    if input_candidate.get("anomaly_type") == "trace_missing":
        return "fault_partially_localized"
    if input_candidate.get("anomaly_type") == "replay_mismatch":
        return "fault_partially_localized"
    if input_candidate.get("anomaly_type") == "determinism_drift":
        return "fault_partially_localized"
    if input_candidate.get("anomaly_type") == "boundary_violation":
        return "fault_localized"
    if input_candidate.get("anomaly_type") == "dependency_unavailable":
        return "dependency_issue_detected"
    if input_candidate.get("anomaly_type") in {
        "protocol_version_drift",
        "protocol_schema_mismatch",
        "protocol_deprecation_conflict",
    }:
        return "protocol_drift_detected"
    if input_candidate.get("anomaly_type") in {
        "model_asset_missing",
        "model_asset_unavailable",
        "model_admission_failure",
        "model_capability_mismatch",
        "model_resource_insufficient",
        "model_ownership_conflict",
    }:
        return "model_asset_issue_detected"
    if input_candidate.get("anomaly_type") == "manifest_registry_mismatch":
        return "multiple_fault_domains_detected"
    if input_candidate.get("anomaly_type") == "baseline_registry_mismatch":
        return "fault_localized"
    if input_candidate.get("anomaly_type") == "baseline_behavior_drift":
        return "baseline_drift_detected"

    if input_candidate.get("anomaly_type") == "unknown_anomaly" and not bool(
        input_candidate.get("diagnostics")
    ):
        return "insufficient_evidence"
    if input_candidate.get("anomaly_type") == "unknown_anomaly":
        return "manual_review_required"
    return "no_fault_detected"


def build_system_maintenance_module_output_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    root_cause: Mapping[str, Any],
    protocol_result: Mapping[str, Any],
    model_result: Mapping[str, Any],
    baseline_calibration: Mapping[str, Any],
    dependency_impact: Mapping[str, Any],
    remediation: Mapping[str, Any],
    task_handoff: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
    trace_ref: str,
    replay_key: str,
) -> Dict[str, Any]:
    output = {
        "capability_id": CAPABILITY_ID,
        "maintenance_request_id": input_candidate.get("maintenance_request_id"),
        "maintenance_status": module_status,
        "primary_capability_candidate": root_cause.get("primary_capability_candidate"),
        "secondary_capability_candidates": tuple(
            root_cause.get("secondary_capability_candidates") or ()
        ),
        "fault_domain": root_cause.get("fault_domain"),
        "root_cause_candidates": tuple(root_cause.get("root_cause_candidates") or ()),
        "protocol_drift_result": protocol_result.get("protocol_drift_result"),
        "model_asset_result": model_result.get("model_asset_result"),
        "baseline_calibration_result": baseline_calibration.get(
            "baseline_calibration_result"
        ),
        "dependency_impact": dependency_impact.get("dependency_impact"),
        "remediation_candidates": tuple(
            remediation.get("remediation_candidates") or ()
        ),
        "task_handoff_candidate": task_handoff.get("task_handoff_candidate"),
        "diagnostics": diagnostics,
        "trace_ref": trace_ref,
        "replay_key": replay_key,
        "boundary_flags": {field: False for field in BOUNDARY_FALSE_FIELDS},
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
    for field in BOUNDARY_FALSE_FIELDS:
        output[field] = False
    return output
