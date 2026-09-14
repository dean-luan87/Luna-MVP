from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_landmark_assessment_v1(
    input_candidate: Mapping[str, Any], evidence_state: Mapping[str, Any]
) -> Dict[str, Any]:
    landmarks = tuple(input_candidate.get("landmark_candidates") or ())
    detected = bool(landmarks)
    confidence = (
        0.8
        if detected
        else (0.5 if evidence_state.get("ocr_evidence_present") else 0.3)
    )
    return {
        "schema_version": "navigation_manager_landmark_resolver_v1",
        "landmark_assessment": {
            "landmark_detected": detected,
            "landmark_candidates": landmarks,
            "confidence_candidate": round(confidence, 3),
        },
        **not_fact(),
    }
