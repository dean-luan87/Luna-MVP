from __future__ import annotations

from typing import Any, Dict, Mapping


def resolve_protocol_manager_module_status_v1(
    input_candidate: Mapping[str, Any],
    registry_lookup: Mapping[str, Any],
    lifecycle_candidate: Mapping[str, Any],
    compatibility_candidate: Mapping[str, Any],
    admission_candidate: Mapping[str, Any],
    change_control: Mapping[str, Any],
    boundary_report: Mapping[str, Any],
    error_namespace_report: Mapping[str, Any],
) -> str:
    operation = str(input_candidate.get("operation") or "query")
    protocol_id = str(input_candidate.get("protocol_id") or "")

    if not input_candidate.get("operation_supported") or not input_candidate.get(
        "protocol_request_id"
    ):
        return "invalid_input"
    if not protocol_id:
        return "invalid_input"
    if boundary_report.get("boundary_violation"):
        return "boundary_violation"
    if error_namespace_report.get("error_namespace_conflict"):
        return "error_namespace_conflict"
    if operation == "register_candidate":
        return "protocol_candidate_registered"
    if not registry_lookup.get("protocol_exists") and operation != "register_candidate":
        return "protocol_not_found"
    if not lifecycle_candidate.get("lifecycle_transition_valid"):
        return "invalid_input"

    compat = str(compatibility_candidate.get("compatibility_result") or "unknown")
    if compat == "incompatible":
        return "protocol_incompatible"
    if not admission_candidate.get("admitted"):
        return "admission_rejected"
    if operation == "deprecate_candidate":
        return "deprecation_candidate"
    if operation == "impact_analysis":
        return "impact_analysis_ready"
    if operation == "diagnose":
        return "diagnostic_only"
    if operation == "change_review":
        if change_control.get("change_review_required"):
            return "change_review_required"
        if change_control.get("change_allowed_candidate"):
            return "change_allowed_candidate"
    if operation in {"validate", "compatibility_check", "admission_check"}:
        return "protocol_valid"
    if operation == "query":
        return "no_change"
    return "protocol_valid"


def build_protocol_manager_result_summary_v1(
    *,
    input_candidate: Mapping[str, Any],
    module_status: str,
    compatibility_candidate: Mapping[str, Any],
    admission_candidate: Mapping[str, Any],
    change_control: Mapping[str, Any],
    impact_analysis: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "protocol_manager_result_summary_v1",
        "protocol_request_id": input_candidate.get("protocol_request_id"),
        "operation": input_candidate.get("operation"),
        "protocol_id": input_candidate.get("protocol_id"),
        "module_status": module_status,
        "compatibility_result": compatibility_candidate.get("compatibility_result"),
        "admitted": admission_candidate.get("admitted"),
        "change_review_required": change_control.get("change_review_required"),
        "breaking_change_candidate": impact_analysis.get("breaking_change_candidate"),
        "migration_required": impact_analysis.get("migration_required"),
        "candidate_only": True,
    }
