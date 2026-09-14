from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_and_admission_subject_candidate_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    subject_ref = input_candidate.get("subject_ref")
    subject_present = bool(subject_ref)
    return {
        "schema_version": "permission_and_admission_subject_resolver_v1",
        "subject_ref": subject_ref,
        "subject_present": subject_present,
        "subject_identity_status": "resolved" if subject_present else "missing",
        **not_fact(),
    }
