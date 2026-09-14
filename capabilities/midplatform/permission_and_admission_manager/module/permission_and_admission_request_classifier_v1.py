from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.permission_and_admission_manager.module.permission_and_admission_manager_module_types_v1 import (
    SUPPORTED_REQUEST_TYPES,
    not_fact,
)


def build_permission_and_admission_request_classification_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    request_type = str(input_candidate.get("request_type") or "")
    classification = {
        "evidence_admission": "evidence_gate",
        "fact_admission_candidate": "fact_candidate_gate",
        "state_candidate_admission": "state_candidate_gate",
        "model_admission": "model_gate",
        "skill_admission": "skill_gate",
        "protocol_admission": "protocol_gate",
        "capability_admission": "capability_gate",
        "human_correction_admission": "human_correction_gate",
        "action_candidate_admission": "action_candidate_gate",
        "runtime_access_admission": "runtime_access_gate",
    }.get(request_type, "unknown")

    return {
        "schema_version": "permission_and_admission_request_classifier_v1",
        "request_type": request_type,
        "request_type_supported": request_type in SUPPORTED_REQUEST_TYPES,
        "classification": classification,
        **not_fact(),
    }
