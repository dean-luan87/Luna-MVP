from __future__ import annotations

from typing import Any, Dict, Mapping


def build_navigation_manager_diagnostics_v1(
    input_candidate: Mapping[str, Any],
    module_status: str,
    evidence_state: Mapping[str, Any],
    deviation_assessment: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": "navigation_manager_diagnostics_v1",
        "navigation_request_id": input_candidate.get("navigation_request_id"),
        "navigation_mode": input_candidate.get("navigation_mode"),
        "module_status": module_status,
        "vision_evidence_count": len(evidence_state.get("vision_evidence_refs") or ()),
        "ocr_evidence_count": len(evidence_state.get("ocr_evidence_refs") or ()),
        "map_visual_conflict": bool(evidence_state.get("map_visual_conflict", False)),
        "deviation_detected": bool(
            (
                (deviation_assessment.get("deviation_assessment") or {}).get(
                    "deviation_detected", False
                )
            )
        ),
        "candidate_only": True,
        "fact_status": "not_fact",
        "write_allowed": False,
    }
