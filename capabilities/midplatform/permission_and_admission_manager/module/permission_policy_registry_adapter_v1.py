from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_policy_lookup_v1(
    input_candidate: Mapping[str, Any],
    request_classification: Mapping[str, Any],
) -> Dict[str, Any]:
    request_type = str(input_candidate.get("request_type") or "")
    policy_snapshot = dict(input_candidate.get("policy_snapshot") or {})
    policies = dict(policy_snapshot.get("request_type_policies") or {})
    policy = policies.get(request_type)

    if policy is None:
        policy = {
            "evidence_required": True,
            "provenance_required": True,
            "consent_required": request_type
            in {"human_correction_admission", "runtime_access_admission"},
            "ownership_required": True,
            "authority_required": True,
            "allow_runtime_dispatch": False,
            "allow_fact_admission": False,
            "allow_state_write": False,
            "policy_found": False,
        }
    else:
        policy = dict(policy)
        policy["policy_found"] = True

    return {
        "schema_version": "permission_policy_registry_adapter_v1",
        "request_type": request_type,
        "policy_found": bool(policy.get("policy_found")),
        "policy": policy,
        "policy_source": "policy_snapshot"
        if policy.get("policy_found")
        else "default_fallback_candidate",
        **not_fact(),
    }
