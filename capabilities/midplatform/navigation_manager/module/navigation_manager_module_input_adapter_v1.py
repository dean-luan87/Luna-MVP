from __future__ import annotations

from typing import Any, Dict, Mapping

from capabilities.midplatform.navigation_manager.module.navigation_manager_module_types_v1 import (
    MODULE_SCHEMA_VERSION,
    SUPPORTED_NAVIGATION_MODES,
    not_fact,
)


def adapt_navigation_manager_input_v1(payload: Mapping[str, Any]) -> Dict[str, Any]:
    candidate = dict(payload)
    navigation_mode = str(candidate.get("navigation_mode") or "").strip()
    return {
        "schema_version": MODULE_SCHEMA_VERSION,
        "navigation_request_id": str(
            candidate.get("navigation_request_id") or ""
        ).strip(),
        "task_id": str(candidate.get("task_id") or "").strip(),
        "navigation_mode": navigation_mode,
        "navigation_mode_supported": navigation_mode in SUPPORTED_NAVIGATION_MODES,
        "destination_candidate": dict(candidate.get("destination_candidate") or {}),
        "route_candidate": dict(candidate.get("route_candidate") or {}),
        "route_memory_ref": str(candidate.get("route_memory_ref") or "").strip(),
        "current_position_candidate": dict(
            candidate.get("current_position_candidate") or {}
        ),
        "route_progress_candidate": dict(
            candidate.get("route_progress_candidate") or {}
        ),
        "observation_candidate": dict(candidate.get("observation_candidate") or {}),
        "vision_evidence_refs": tuple(candidate.get("vision_evidence_refs") or ()),
        "ocr_evidence_refs": tuple(candidate.get("ocr_evidence_refs") or ()),
        "map_evidence_candidate": dict(candidate.get("map_evidence_candidate") or {}),
        "landmark_candidates": tuple(candidate.get("landmark_candidates") or ()),
        "crossing_candidates": tuple(candidate.get("crossing_candidates") or ()),
        "traffic_light_candidates": tuple(
            candidate.get("traffic_light_candidates") or ()
        ),
        "obstacle_candidates": tuple(candidate.get("obstacle_candidates") or ()),
        "user_correction_candidate": dict(
            candidate.get("user_correction_candidate") or {}
        ),
        "temporal_snapshot": dict(candidate.get("temporal_snapshot") or {}),
        "permission_context": dict(candidate.get("permission_context") or {}),
        "version_snapshot": dict(candidate.get("version_snapshot") or {}),
        "trace_context": dict(candidate.get("trace_context") or {}),
        "candidate_only": True,
        **not_fact(),
    }
