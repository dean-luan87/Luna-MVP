from __future__ import annotations

from typing import Any, Dict

MODULE_SCHEMA_VERSION = "permission_and_admission_manager_module_v1"

SUPPORTED_REQUEST_TYPES = {
    "evidence_admission",
    "fact_admission_candidate",
    "state_candidate_admission",
    "model_admission",
    "skill_admission",
    "protocol_admission",
    "capability_admission",
    "human_correction_admission",
    "action_candidate_admission",
    "runtime_access_admission",
}

ADMISSION_STATUSES = {
    "invalid_input",
    "policy_not_found",
    "evidence_insufficient",
    "provenance_invalid",
    "consent_required",
    "consent_denied",
    "ownership_unresolved",
    "ownership_denied",
    "authority_insufficient",
    "boundary_blocked",
    "risk_blocked",
    "conflict_unresolved",
    "revoked",
    "expired",
    "admission_rejected",
    "admission_deferred",
    "review_required",
    "admission_candidate_ready",
}

BOUNDARY_FALSE_FIELDS = (
    "fact_admission_executed",
    "fact_promotion_executed",
    "state_mutation_executed",
    "state_store_write_executed",
    "model_execution_executed",
    "protocol_activation_executed",
    "skill_activation_executed",
    "capability_activation_executed",
    "action_execution_executed",
    "runtime_dispatch_executed",
    "database_write_executed",
    "external_lookup_executed",
    "production_execution",
)


def not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}
