from __future__ import annotations

from typing import Any, Dict, Mapping


def build_protocol_manager_diagnostics_v1(
    input_candidate: Mapping[str, Any],
    registry_lookup: Mapping[str, Any],
    compatibility_candidate: Mapping[str, Any],
    admission_candidate: Mapping[str, Any],
    change_control: Mapping[str, Any],
    boundary_report: Mapping[str, Any],
    error_namespace_report: Mapping[str, Any],
    impact_analysis: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "protocol_manager_diagnostics_v1",
        "operation": input_candidate.get("operation"),
        "protocol_exists": bool(registry_lookup.get("protocol_exists")),
        "compatibility_result": compatibility_candidate.get("compatibility_result"),
        "admitted": bool(admission_candidate.get("admitted")),
        "change_review_required": bool(change_control.get("change_review_required")),
        "boundary_violation": bool(boundary_report.get("boundary_violation")),
        "error_namespace_conflict": bool(
            error_namespace_report.get("error_namespace_conflict")
        ),
        "impact_analysis_ready": True,
        "diagnostic_only": str(input_candidate.get("operation")) == "diagnose",
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
