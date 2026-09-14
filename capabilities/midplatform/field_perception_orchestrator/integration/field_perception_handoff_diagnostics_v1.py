from __future__ import annotations

from typing import Any, Dict, Mapping


def build_visual_handoff_diagnostics_v1(
    input_candidate: Mapping[str, Any],
    integration_status: str,
    deduplication_result: Mapping[str, Any],
    budget_decision: Mapping[str, Any],
    eligible_model_candidates: tuple[Mapping[str, Any], ...],
    rejected_model_candidates: tuple[Mapping[str, Any], ...],
    rejection_reasons: tuple[str, ...],
) -> Dict[str, Any]:
    return {
        "schema_version": "field_perception_handoff_diagnostics_v1",
        "handoff_request_id": input_candidate.get("handoff_request_id"),
        "integration_status": integration_status,
        "vision_required": bool(input_candidate.get("vision_required", True)),
        "deduplication_status": deduplication_result.get("deduplication_status"),
        "budget_level": (budget_decision.get("budget_decision") or {}).get(
            "budget_level"
        ),
        "eligible_model_count": len(eligible_model_candidates),
        "rejected_model_count": len(rejected_model_candidates),
        "rejection_reasons": tuple(rejection_reasons),
    }
