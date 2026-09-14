from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    not_fact,
)


def build_navigation_evidence_state_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    vision_refs = tuple(input_candidate.get("vision_evidence_refs") or ())
    ocr_refs = tuple(input_candidate.get("ocr_evidence_refs") or ())
    map_evidence = dict(input_candidate.get("map_evidence_candidate") or {})
    map_visual_conflict = bool(map_evidence.get("map_visual_conflict", False))
    return {
        "schema_version": "navigation_manager_evidence_adapter_v1",
        "vision_evidence_refs": vision_refs,
        "ocr_evidence_refs": ocr_refs,
        "map_evidence_candidate": map_evidence,
        "vision_evidence_present": bool(vision_refs),
        "ocr_evidence_present": bool(ocr_refs),
        "map_evidence_present": bool(map_evidence),
        "map_visual_conflict": map_visual_conflict,
        **not_fact(),
    }
