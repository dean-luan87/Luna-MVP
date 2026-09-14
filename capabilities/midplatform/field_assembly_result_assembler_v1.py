# -*- coding: utf-8 -*-
"""Field assembly result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.field_assembly_types_v1 import NON_EXECUTION_FLAGS


def assemble_field_assembly_result(
    *,
    enhanced_field_scene: Dict[str, Any],
    enhanced_entities: List[Dict[str, Any]],
    rejected_items: List[Dict[str, Any]],
    alignment_result_ref: str | None = None,
    fusion_result_ref: str | None = None,
    geometry_result_ref: str | None = None,
) -> Dict[str, Any]:
    geom_enhanced = sum(1 for e in enhanced_entities if e.get("entity_status") == "entity_geometry_enhanced")
    geom_unknown = sum(1 for e in enhanced_entities if e.get("entity_status") == "entity_geometry_unknown")
    zone_summary = enhanced_field_scene.get("zone_summary") or {}

    scene_ready = enhanced_field_scene.get("readiness_for_core_pipeline") is True
    has_estimated = any(
        e.get("entity_status") in ("entity_geometry_enhanced", "entity_degraded")
        and e.get("depth_error_expected") is True
        for e in enhanced_entities
    )
    readiness_core = scene_ready and len(enhanced_entities) > 0
    readiness_real_path = readiness_core and has_estimated and geom_enhanced >= 1

    return {
        "assembly_result_id": f"far_{uuid.uuid4().hex[:12]}",
        "input_alignment_result_ref": alignment_result_ref,
        "input_fusion_result_ref": fusion_result_ref,
        "input_geometry_result_ref": geometry_result_ref,
        "enhanced_field_scene_candidate": enhanced_field_scene,
        "enhanced_entity_candidates": enhanced_entities,
        "accepted_entity_count": len(enhanced_entities),
        "rejected_entity_count": len(rejected_items),
        "geometry_enhanced_count": geom_enhanced,
        "geometry_unknown_count": geom_unknown,
        "zone_summary": zone_summary,
        "warning_summary": enhanced_field_scene.get("warning_summary") or {},
        "conflict_summary": enhanced_field_scene.get("conflict_summary") or {},
        "missing_information": enhanced_field_scene.get("missing_information") or [],
        "readiness_for_field_first_core": readiness_core,
        "readiness_for_real_model_success_path": readiness_real_path,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "candidate_only": True,
    }
