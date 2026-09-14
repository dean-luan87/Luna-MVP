# -*- coding: utf-8 -*-
"""Enhanced FieldScene assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.field_assembly_types_v1 import DEFAULT_FIELD_RADIUS_M, NON_EXECUTION_FLAGS
from capabilities.midplatform.field_quality_summary_builder_v1 import (
    build_depth_quality_summary,
    build_geometry_quality_summary,
    build_scene_quality_summary,
)
from capabilities.midplatform.field_zone_summary_builder_v1 import build_field_zone_summary


def assemble_enhanced_field_scene_candidate(
    *,
    entities: List[Dict[str, Any]],
    geometry_candidates: List[Dict[str, Any]],
    hints: List[Dict[str, Any]],
    assembly_input: Dict[str, Any],
) -> Dict[str, Any]:
    scene_id = f"efs_{uuid.uuid4().hex[:12]}"
    for ent in entities:
        ent["field_scene_ref"] = scene_id

    zone_summary = build_field_zone_summary(entities)
    depth_q = build_depth_quality_summary(entities, hints)
    geometry_q = build_geometry_quality_summary(entities, geometry_candidates)

    all_warnings = [w for e in entities for w in (e.get("warning_codes") or [])]
    all_conflicts = [c for e in entities for c in (e.get("conflict_refs") or [])]
    all_missing: List[str] = []
    for e in entities:
        all_missing.extend(e.get("missing_information") or [])

    scene_q = build_scene_quality_summary(entities, depth_q, geometry_q, all_warnings)
    active_zones = [z for z, k in (
        ("inner_zone", "inner_zone_entity_count"),
        ("working_zone", "working_zone_entity_count"),
        ("forecast_zone", "forecast_zone_entity_count"),
        ("unknown", "unknown_zone_entity_count"),
    ) if zone_summary.get(k, 0) > 0]

    has_valid = any(
        e.get("entity_status") in ("entity_geometry_enhanced", "entity_degraded")
        for e in entities
    )
    readiness = has_valid and len(entities) > 0 and all(e.get("candidate_only") is True for e in entities)

    frame_ref = assembly_input.get("frame_ref") or (entities[0].get("traceability_refs") or ["frame_0"])[0] if entities else "frame_0"
    timestamp = assembly_input.get("timestamp") or "2026-06-11T00:00:00Z"

    return {
        "field_scene_id": scene_id,
        "field_session_ref": assembly_input.get("field_session_ref"),
        "frame_ref": frame_ref,
        "timestamp": timestamp,
        "camera_ref": assembly_input.get("camera_ref"),
        "user_ref": assembly_input.get("user_ref"),
        "field_origin": "self_centered",
        "field_radius_m": assembly_input.get("field_radius_m", DEFAULT_FIELD_RADIUS_M),
        "active_zones": active_zones,
        "entity_candidates": entities,
        "geometry_candidates": geometry_candidates,
        "zone_summary": zone_summary,
        "scene_quality_summary": scene_q,
        "depth_quality_summary": depth_q,
        "geometry_quality_summary": geometry_q,
        "missing_information": sorted(set(all_missing)),
        "warning_summary": {"warnings": sorted(set(all_warnings)), "warning_count": len(set(all_warnings))},
        "conflict_summary": {"conflicts": sorted(set(all_conflicts)), "conflict_count": len(set(all_conflicts))},
        "readiness_for_core_pipeline": readiness,
        "source_refs": list(assembly_input.get("source_refs") or []) + [scene_id],
        "evidence_refs": list(assembly_input.get("evidence_refs") or []),
        "traceability_refs": [frame_ref],
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "candidate_only": True,
    }
