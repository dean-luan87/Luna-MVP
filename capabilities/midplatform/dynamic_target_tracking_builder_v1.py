# -*- coding: utf-8 -*-
"""Dynamic target tracking builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.static_dynamic_target_locking_tracking_types_v1 import (
    CONTINUITY_ALLOWED,
    CONTINUITY_FREEZE,
    CONTINUITY_LOST,
    CONTINUITY_RESET,
)
from capabilities.midplatform.target_task_impact_scorer_v1 import is_dynamic_label, score_target_task_impact


def _bbox_center(bbox: Dict[str, float]) -> Dict[str, float]:
    return {"x": (bbox["x1"] + bbox["x2"]) / 2, "y": (bbox["y1"] + bbox["y2"]) / 2}


def _motion_from_bbox(prev_bbox: Dict[str, float], curr_bbox: Dict[str, float]) -> str:
    pc, cc = _bbox_center(prev_bbox), _bbox_center(curr_bbox)
    dist = abs(pc["x"] - cc["x"]) + abs(pc["y"] - cc["y"])
    if dist > 80:
        return "moving"
    if dist > 30:
        return "likely_moving"
    return "static"


def build_dynamic_target_track_candidates(
    *,
    previous_field_scene_summary: Dict[str, Any],
    current_field_scene_summary: Dict[str, Any],
    continuity_decision: Dict[str, Any],
    field_session_ref: str = "fsess_mock",
    tracker_hint_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    status = continuity_decision.get("continuity_status", "uncertain_need_recheck")
    if status in CONTINUITY_RESET or status in CONTINUITY_FREEZE or status in CONTINUITY_LOST:
        return []
    if status not in CONTINUITY_ALLOWED:
        return []

    prev_entities = previous_field_scene_summary.get("entities") or []
    curr_entities = current_field_scene_summary.get("entities") or []
    tracks: List[Dict[str, Any]] = []
    used_prev: set = set()

    for cent in curr_entities:
        label = cent.get("label", "")
        if not is_dynamic_label(label):
            continue
        prev = _match_prev(cent, prev_entities, used_prev)
        if not prev:
            continue
        motion = _motion_from_bbox(prev.get("bbox", {}), cent.get("bbox", {}))
        lock_st = "candidate_lock" if motion in ("moving", "likely_moving") else "locked"
        if not tracker_hint_id and motion in ("moving", "likely_moving"):
            lock_st = "weak_locked"
        impact = score_target_task_impact(
            target_ref=cent.get("entity_candidate_id", "ent"),
            label=label,
            field_zone=cent.get("field_zone", "unknown"),
            motion_status=motion,
        )
        tracks.append({
            "track_candidate_id": f"dtt_{uuid.uuid4().hex[:12]}",
            "field_session_ref": field_session_ref,
            "previous_entity_candidate_ref": prev.get("entity_candidate_id"),
            "current_entity_candidate_ref": cent.get("entity_candidate_id"),
            "label": label,
            "previous_bbox": prev.get("bbox"),
            "current_bbox": cent.get("bbox"),
            "previous_pseudo_3d_position": prev.get("pseudo_3d_position"),
            "current_pseudo_3d_position": cent.get("pseudo_3d_position"),
            "visibility_status": "visible",
            "motion_status": motion,
            "lock_status": lock_st,
            "tracker_hint_id": tracker_hint_id,
            "tracker_id_is_hint_not_fact": True,
            "continuity_confidence": 0.75 if motion != "static" else 0.85,
            "task_impact_hint": impact["task_impact_hint"],
            "source_refs": ["mock_frontend"],
            "evidence_refs": [prev.get("entity_candidate_id"), cent.get("entity_candidate_id")],
            "reason_codes": [f"dynamic_track_{motion}"],
            "candidate_only": True,
        })
    return tracks


def _match_prev(curr: Dict[str, Any], prev_list: List[Dict[str, Any]], used: set) -> Optional[Dict[str, Any]]:
    for p in prev_list:
        pid = p.get("entity_candidate_id")
        if pid in used:
            continue
        if p.get("label") == curr.get("label"):
            used.add(pid)
            return p
    return None
