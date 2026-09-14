from __future__ import annotations

from typing import Any, Dict, Mapping


def resolve_permission_admission_eligibility_v1(
    input_candidate: Mapping[str, Any],
    subject_candidate: Mapping[str, Any],
    resource_candidate: Mapping[str, Any],
    request_classification: Mapping[str, Any],
    policy_lookup: Mapping[str, Any],
    evidence_validation: Mapping[str, Any],
    consent_check: Mapping[str, Any],
    ownership_check: Mapping[str, Any],
    authority_check: Mapping[str, Any],
    risk_check: Mapping[str, Any],
    conflict_check: Mapping[str, Any],
    revocation_check: Mapping[str, Any],
) -> Dict[str, Any]:
    reasons = []
    request_id = str(input_candidate.get("request_id") or "")
    request_type = str(input_candidate.get("request_type") or "")

    if not request_id or not request_type:
        reasons.append("invalid_input")
    elif not request_classification.get("request_type_supported"):
        reasons.append("invalid_input")

    if not subject_candidate.get("subject_present"):
        reasons.append("invalid_input")
    if not resource_candidate.get("resource_present"):
        reasons.append("invalid_input")

    if not policy_lookup.get("policy_found"):
        reasons.append("policy_not_found")
    if not evidence_validation.get("evidence_sufficient"):
        reasons.append("evidence_insufficient")
    if not evidence_validation.get("provenance_valid"):
        reasons.append("provenance_invalid")

    if (
        consent_check.get("consent_required")
        and consent_check.get("consent_status") == "missing"
    ):
        reasons.append("consent_required")
    if consent_check.get("consent_denied"):
        reasons.append("consent_denied")

    if ownership_check.get("ownership_unresolved"):
        reasons.append("ownership_unresolved")
    if ownership_check.get("ownership_denied"):
        reasons.append("ownership_denied")

    if authority_check.get("authority_insufficient"):
        reasons.append("authority_insufficient")
    if authority_check.get("boundary_blocked"):
        reasons.append("boundary_blocked")
    if risk_check.get("risk_blocked"):
        reasons.append("risk_blocked")
    if conflict_check.get("conflict_unresolved"):
        reasons.append("conflict_unresolved")
    if revocation_check.get("revoked"):
        reasons.append("revoked")
    elif revocation_check.get("expired"):
        reasons.append("expired")

    if reasons:
        status = reasons[0]
    else:
        policy = dict(policy_lookup.get("policy") or {})
        if policy.get("decision_mode") == "reject":
            status = "admission_rejected"
        elif policy.get("decision_mode") == "defer":
            status = "admission_deferred"
        elif risk_check.get("review_required"):
            status = "review_required"
        else:
            status = "admission_candidate_ready"

    return {
        "schema_version": "permission_admission_eligibility_resolver_v1",
        "admission_status": status,
        "eligible": status == "admission_candidate_ready",
        "rejection_reasons": reasons,
        "review_required": status == "review_required",
    }
