from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_evidence_quality_v1(
    input_candidate: Mapping[str, Any],
    evidence_intake: Mapping[str, Any],
    crossmodal: Mapping[str, Any],
) -> Dict[str, Any]:
    vision_count = len(evidence_intake.get("vision_evidence_refs") or ())
    ocr_count = len(evidence_intake.get("ocr_evidence_refs") or ())
    assoc_count = len(crossmodal.get("crossmodal_associations") or ())

    source_constraints = dict(input_candidate.get("source_constraints") or {})
    if source_constraints.get("force_low_quality", False):
        score = 0.3
    else:
        score = min(1.0, 0.2 + 0.2 * vision_count + 0.2 * ocr_count + 0.1 * assoc_count)

    return {
        "schema_version": "observation_manager_evidence_quality_v1",
        "quality_score": round(score, 3),
        "confidence_candidate": round(max(0.0, score - 0.1), 3),
        "quality_level": "high"
        if score >= 0.8
        else ("medium" if score >= 0.5 else "low"),
        **not_fact(),
    }
