from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_authority_boundary_check_v1(
    input_candidate: Mapping[str, Any],
    policy_lookup: Mapping[str, Any],
) -> Dict[str, Any]:
    policy = dict(policy_lookup.get("policy") or {})
    authority_required = bool(policy.get("authority_required", True))
    requested_authority = str(input_candidate.get("requested_authority") or "")
    requested_operation = str(input_candidate.get("requested_operation") or "")

    allowed_authorities = tuple(
        policy.get("allowed_authorities") or ("read_candidate", "admission_candidate")
    )
    allowed_operations = tuple(
        policy.get("allowed_operations") or ("evaluate", "review", "candidate_decide")
    )

    authority_insufficient = (
        authority_required and requested_authority not in allowed_authorities
    )
    boundary_blocked = bool(
        input_candidate.get("risk_context", {}).get("runtime_boundary_blocked", False)
    )

    return {
        "schema_version": "permission_authority_boundary_checker_v1",
        "authority_required": authority_required,
        "requested_authority": requested_authority,
        "requested_operation": requested_operation,
        "authority_insufficient": authority_insufficient,
        "boundary_blocked": boundary_blocked
        or (
            requested_operation not in allowed_operations and bool(requested_operation)
        ),
        "allowed_authorities": allowed_authorities,
        "allowed_operations": allowed_operations,
        "runtime_allowed_now": False,
        "state_write_allowed_now": False,
        "fact_admission_allowed_now": False,
        **not_fact(),
    }
