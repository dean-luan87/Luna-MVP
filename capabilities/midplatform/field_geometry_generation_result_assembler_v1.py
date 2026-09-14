# -*- coding: utf-8 -*-
"""Field geometry generation result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.field_geometry_candidate_types_v1 import NON_EXECUTION_FLAGS


def assemble_field_geometry_generation_result(
    *,
    object_spatial_state_candidates: List[Dict[str, Any]],
    field_geometry_candidates: List[Dict[str, Any]],
    rejected_geometry_items: List[Dict[str, Any]],
    depth_object_fusion_result_ref: str | None = None,
) -> Dict[str, Any]:
    unknown_count = sum(
        1 for g in field_geometry_candidates
        if g.get("geometry_status") in ("geometry_unknown", "geometry_rejected")
    )
    all_warnings = [w for g in field_geometry_candidates for w in (g.get("warning_codes") or [])]
    all_missing: List[str] = []
    for s in object_spatial_state_candidates:
        all_missing.extend(s.get("missing_information") or [])

    ready_geometries = [
        g for g in field_geometry_candidates
        if g.get("geometry_status") in ("geometry_estimated", "geometry_weak_estimated")
        and g.get("candidate_only") is True
    ]
    readiness = len(ready_geometries) > 0 and all(
        g.get("depth_error_expected") is True for g in field_geometry_candidates
    )

    return {
        "geometry_generation_result_id": f"fgr_{uuid.uuid4().hex[:12]}",
        "input_depth_object_fusion_result_ref": depth_object_fusion_result_ref,
        "object_spatial_state_candidates": object_spatial_state_candidates,
        "field_geometry_candidates": field_geometry_candidates,
        "accepted_geometry_count": len(field_geometry_candidates),
        "rejected_geometry_count": len(rejected_geometry_items),
        "geometry_unknown_count": unknown_count,
        "warning_summary": {"warnings": all_warnings, "warning_count": len(all_warnings)},
        "missing_information": sorted(set(all_missing)),
        "readiness_for_field_assembly": readiness,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "candidate_only": True,
    }
