# -*- coding: utf-8 -*-
"""Depth-Object fusion result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.depth_object_fusion_types_v1 import NON_EXECUTION_FLAGS


def assemble_depth_object_fusion_result(
    *,
    object_depth_hint_candidates: List[Dict[str, Any]],
    rejected_fusion_items: List[Dict[str, Any]],
    alignment_result_ref: str | None = None,
) -> Dict[str, Any]:
    missing_count = sum(
        1 for h in object_depth_hint_candidates
        if h.get("object_depth_hint") is None or h.get("depth_bucket") == "unknown"
    )
    unreliable_count = sum(
        1 for h in object_depth_hint_candidates
        if h.get("fusion_confidence") == "low" and h.get("object_depth_hint") is not None
    )
    all_warnings = [w for h in object_depth_hint_candidates for w in (h.get("warning_codes") or [])]
    all_conflicts = [c for h in object_depth_hint_candidates for c in (h.get("conflict_refs") or [])]
    all_missing = []
    for h in object_depth_hint_candidates:
        all_missing.extend(h.get("missing_information") or [])

    valid_hints = [
        h for h in object_depth_hint_candidates
        if h.get("object_depth_hint") is not None and h.get("depth_bucket") != "unknown"
    ]
    readiness = (
        len(valid_hints) > 0
        and all(h.get("candidate_only") is True for h in object_depth_hint_candidates)
        and all(h.get("depth_error_expected") is True for h in object_depth_hint_candidates)
    )

    return {
        "fusion_result_id": f"dof_{uuid.uuid4().hex[:12]}",
        "input_alignment_result_ref": alignment_result_ref,
        "object_depth_hint_candidates": object_depth_hint_candidates,
        "accepted_fusion_count": len(object_depth_hint_candidates),
        "rejected_fusion_count": len(rejected_fusion_items),
        "missing_depth_count": missing_count,
        "unreliable_depth_count": unreliable_count,
        "warning_summary": {"warnings": all_warnings, "warning_count": len(all_warnings)},
        "conflict_summary": {"conflicts": all_conflicts, "conflict_count": len(all_conflicts)},
        "missing_information": sorted(set(all_missing)),
        "readiness_for_field_geometry": readiness,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "candidate_only": True,
    }
