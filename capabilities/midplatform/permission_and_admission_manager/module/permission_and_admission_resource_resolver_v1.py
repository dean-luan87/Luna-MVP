from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_and_admission_resource_candidate_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    resource_ref = input_candidate.get("resource_ref")
    resource_present = bool(resource_ref)
    return {
        "schema_version": "permission_and_admission_resource_resolver_v1",
        "resource_ref": resource_ref,
        "resource_present": resource_present,
        "resource_identity_status": "resolved" if resource_present else "missing",
        **not_fact(),
    }
