from __future__ import annotations

from typing import Any, Dict, Mapping


def build_permission_and_admission_diagnostics_v1(
    input_candidate: Mapping[str, Any],
    eligibility: Mapping[str, Any],
    evidence_validation: Mapping[str, Any],
    consent_check: Mapping[str, Any],
    ownership_check: Mapping[str, Any],
    authority_check: Mapping[str, Any],
    risk_check: Mapping[str, Any],
    conflict_check: Mapping[str, Any],
    revocation_check: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "permission_and_admission_diagnostics_v1",
        "request_id": input_candidate.get("request_id"),
        "request_type": input_candidate.get("request_type"),
        "admission_status": eligibility.get("admission_status"),
        "rejection_reason_count": len(eligibility.get("rejection_reasons") or ()),
        "evidence_sufficient": bool(evidence_validation.get("evidence_sufficient")),
        "provenance_valid": bool(evidence_validation.get("provenance_valid")),
        "consent_status": consent_check.get("consent_status"),
        "ownership_unresolved": bool(ownership_check.get("ownership_unresolved")),
        "ownership_denied": bool(ownership_check.get("ownership_denied")),
        "authority_insufficient": bool(authority_check.get("authority_insufficient")),
        "boundary_blocked": bool(authority_check.get("boundary_blocked")),
        "risk_blocked": bool(risk_check.get("risk_blocked")),
        "conflict_unresolved": bool(conflict_check.get("conflict_unresolved")),
        "revoked": bool(revocation_check.get("revoked")),
        "expired": bool(revocation_check.get("expired")),
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
