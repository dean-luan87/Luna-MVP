# -*- coding: utf-8 -*-
"""Depth ingestion result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.depth_observation_candidate_ingestion_types_v1 import NON_EXECUTION_FLAGS


def assemble_depth_ingestion_result(
    *,
    depth_observation_candidate: Dict[str, Any],
    object_depth_hint_candidates: List[Dict[str, Any]],
    rejected_objects: List[Dict[str, Any]],
    warning_summary: List[str],
    missing_information: List[str],
) -> Dict[str, Any]:
    missing_count = sum(
        1 for h in object_depth_hint_candidates
        if h.get("object_depth_hint") is None or h.get("depth_bucket") == "unknown"
    )
    unreliable_count = sum(
        1 for h in object_depth_hint_candidates
        if h.get("depth_confidence") == "low" and h.get("object_depth_hint") is not None
    )
    valid_hints = [
        h for h in object_depth_hint_candidates
        if h.get("object_depth_hint") is not None and h.get("depth_bucket") != "unknown"
    ]
    readiness = (
        len(valid_hints) > 0
        and depth_observation_candidate.get("candidate_only") is True
        and all(h.get("depth_error_expected") is True for h in object_depth_hint_candidates)
        and depth_observation_candidate.get("depth_source") != "hardware"
    )
    return {
        "ingestion_result_id": f"ding_{uuid.uuid4().hex[:12]}",
        "depth_observation_candidate": depth_observation_candidate,
        "object_depth_hint_candidates": object_depth_hint_candidates,
        "accepted_object_count": len(object_depth_hint_candidates),
        "rejected_object_count": len(rejected_objects),
        "depth_missing_count": missing_count,
        "depth_unreliable_count": unreliable_count,
        "warning_summary": {
            "warnings": warning_summary,
            "warning_count": len(warning_summary),
        },
        "missing_information": sorted(set(missing_information)),
        "readiness_for_field_geometry": readiness,
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "candidate_only": True,
    }
