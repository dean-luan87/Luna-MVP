from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    not_fact,
)


def build_permission_admission_decision_candidate_v1(
    input_candidate: Mapping[str, Any],
    eligibility: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "permission_admission_decision_builder_v1",
        "request_id": input_candidate.get("request_id"),
        "request_type": input_candidate.get("request_type"),
        "subject_ref": input_candidate.get("subject_ref"),
        "resource_ref": input_candidate.get("resource_ref"),
        "admission_status": eligibility.get("admission_status"),
        "rejection_reasons": tuple(eligibility.get("rejection_reasons") or ()),
        "review_required": bool(eligibility.get("review_required")),
        "admission_candidate_ready": eligibility.get("admission_status")
        == "admission_candidate_ready",
        "candidate_only": True,
        **not_fact(),
    }
