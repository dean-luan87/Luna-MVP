from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_ownership_check_v1(
    input_candidate: Mapping[str, Any],
    policy_lookup: Mapping[str, Any],
) -> Dict[str, Any]:
    policy = dict(policy_lookup.get("policy") or {})
    ownership_required = bool(policy.get("ownership_required", True))

    owner_ref = input_candidate.get("owner_ref")
    subject_ref = input_candidate.get("subject_ref")
    ownership_unresolved = ownership_required and not owner_ref
    ownership_denied = (
        ownership_required
        and bool(owner_ref)
        and bool(subject_ref)
        and str(owner_ref) != str(subject_ref)
    )

    ownership_granted = not ownership_required or (
        not ownership_unresolved and not ownership_denied
    )
    return {
        "schema_version": "permission_ownership_checker_v1",
        "ownership_required": ownership_required,
        "ownership_unresolved": ownership_unresolved,
        "ownership_denied": ownership_denied,
        "ownership_granted": ownership_granted,
        **not_fact(),
    }
