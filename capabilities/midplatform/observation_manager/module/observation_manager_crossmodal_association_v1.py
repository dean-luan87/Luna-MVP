from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.observation_manager.module.observation_manager_module_types_v1 import (
    not_fact,
)


def build_observation_crossmodal_association_v1(
    evidence_intake: Mapping[str, Any],
) -> Dict[str, Any]:
    vision_evidence_refs = tuple(evidence_intake.get("vision_evidence_refs") or ())
    ocr_evidence_refs = tuple(evidence_intake.get("ocr_evidence_refs") or ())
    associations = []
    for idx, vref in enumerate(vision_evidence_refs):
        if idx < len(ocr_evidence_refs):
            associations.append(
                {
                    "association_id": f"assoc_{idx}",
                    "vision_evidence_ref": vref,
                    "ocr_evidence_ref": ocr_evidence_refs[idx],
                    "association_type": "spatiotemporal_text_overlay_candidate",
                }
            )

    return {
        "schema_version": "observation_manager_crossmodal_association_v1",
        "crossmodal_associations": tuple(associations),
        "crossmodal_association_present": bool(associations),
        **not_fact(),
    }
