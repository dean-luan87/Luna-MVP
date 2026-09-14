from __future__ import annotations

from typing import Any, Dict

MODULE_SCHEMA_VERSION = "protocol_manager_module_v1"

SUPPORTED_OPERATIONS = {
    "register_candidate",
    "query",
    "validate",
    "compatibility_check",
    "admission_check",
    "change_review",
    "deprecate_candidate",
    "impact_analysis",
    "diagnose",
}

MODULE_STATUSES = {
    "invalid_input",
    "protocol_not_found",
    "protocol_candidate_registered",
    "protocol_valid",
    "protocol_incompatible",
    "admission_rejected",
    "change_review_required",
    "change_allowed_candidate",
    "deprecation_candidate",
    "boundary_violation",
    "error_namespace_conflict",
    "impact_analysis_ready",
    "diagnostic_only",
    "no_change",
}

LIFECYCLE_STATES = (
    "draft",
    "candidate",
    "registered",
    "active",
    "deprecated",
    "superseded",
    "revoked",
    "archived",
)

COMPATIBILITY_RESULTS = (
    "exact_match",
    "backward_compatible",
    "forward_compatible",
    "adapter_required",
    "migration_required",
    "incompatible",
    "unknown",
)


def not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}
