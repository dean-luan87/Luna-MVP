from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_evidence_provenance_validation_v1(
    input_candidate: Mapping[str, Any],
    policy_lookup: Mapping[str, Any],
) -> Dict[str, Any]:
    policy = dict(policy_lookup.get("policy") or {})
    evidence_refs = tuple(input_candidate.get("evidence_refs") or ())
    provenance_refs = tuple(input_candidate.get("provenance_refs") or ())

    evidence_required = bool(policy.get("evidence_required", True))
    provenance_required = bool(policy.get("provenance_required", True))
    evidence_sufficient = (not evidence_required) or bool(evidence_refs)

    declared_invalid = bool(
        input_candidate.get("risk_context", {}).get("provenance_invalid", False)
    )
    provenance_valid = (
        (not provenance_required) or bool(provenance_refs)
    ) and not declared_invalid

    return {
        "schema_version": "permission_evidence_provenance_validator_v1",
        "evidence_required": evidence_required,
        "provenance_required": provenance_required,
        "evidence_refs": evidence_refs,
        "provenance_refs": provenance_refs,
        "evidence_sufficient": evidence_sufficient,
        "provenance_valid": provenance_valid,
        **not_fact(),
    }
