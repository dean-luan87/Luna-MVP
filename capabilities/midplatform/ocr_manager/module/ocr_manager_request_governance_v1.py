from __future__ import annotations

from typing import Any, Dict, Mapping


ALLOWED_REQUEST_TYPES = {
    "task_ocr_request",
    "passive_observation_ocr_request",
    "active_observation_ocr_request",
    "human_correction_request",
    "synthetic_integration_fixture",
}

ALLOWED_SCOPES = {
    "text_region",
    "poster_region",
    "sign_region",
    "layout_region",
    "line_region",
}


def run_ocr_manager_request_governance_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    request_type = str(input_candidate.get("request_type") or "")
    task_scope = str(
        (input_candidate.get("task_ocr_request") or {}).get("scope") or "text_region"
    )

    rejection_reasons = list(input_candidate.get("rejection_reasons") or [])
    if request_type not in ALLOWED_REQUEST_TYPES:
        rejection_reasons.append("unsupported_request_type")
    if task_scope not in ALLOWED_SCOPES:
        rejection_reasons.append("invalid_scope")

    passive_active = (
        "passive" if request_type == "passive_observation_ocr_request" else "active"
    )
    if request_type == "human_correction_request":
        passive_active = "human_correction"

    admitted = len(rejection_reasons) == 0
    return {
        "admitted": admitted,
        "request_type": request_type,
        "scope": task_scope,
        "task_relevant": bool(
            (input_candidate.get("task_ocr_request") or {}).get("task_id")
            or input_candidate.get("synthetic_integration_fixture")
        ),
        "passive_active": passive_active,
        "human_correction": request_type == "human_correction_request"
        or bool(input_candidate.get("human_correction_input")),
        "permission_boundary_candidate": {
            "candidate_only": True,
            "provider_runtime_allowed": False,
            "fact_promotion_allowed": False,
            "action_execution_allowed": False,
        },
        "rejection_reasons": tuple(rejection_reasons),
    }
