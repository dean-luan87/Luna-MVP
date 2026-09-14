from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_consent_check_v1(
    input_candidate: Mapping[str, Any],
    policy_lookup: Mapping[str, Any],
) -> Dict[str, Any]:
    policy = dict(policy_lookup.get("policy") or {})
    consent_required = bool(policy.get("consent_required", False))
    consent_ref = input_candidate.get("consent_ref")

    if isinstance(consent_ref, dict):
        consent_status = str(consent_ref.get("status") or "unknown")
    elif consent_ref:
        consent_status = "granted"
    else:
        consent_status = "missing"

    consent_granted = (not consent_required) or consent_status == "granted"
    consent_denied = consent_status == "denied"

    return {
        "schema_version": "permission_consent_checker_v1",
        "consent_required": consent_required,
        "consent_status": consent_status,
        "consent_granted": consent_granted,
        "consent_denied": consent_denied,
        **not_fact(),
    }
