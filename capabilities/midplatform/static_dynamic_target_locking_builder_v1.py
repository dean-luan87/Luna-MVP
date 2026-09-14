# -*- coding: utf-8 -*-
"""Static target locking builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.static_dynamic_target_locking_tracking_types_v1 import (
    CONTINUITY_ALLOWED,
    CONTINUITY_FREEZE,
    CONTINUITY_LOST,
    CONTINUITY_RESET,
)
from capabilities.midplatform.target_task_impact_scorer_v1 import is_static_label, score_target_task_impact


def _overlap(a: Dict[str, float], b: Dict[str, float]) -> float:
    x1 = max(a["x1"], b["x1"])
    y1 = max(a["y1"], b["y1"])
    x2 = min(a["x2"], b["x2"])
    y2 = min(a["y2"], b["y2"])
    if x2 <= x1 or y2 <= y1:
        return 0.0
    inter = (x2 - x1) * (y2 - y1)
    area_a = max((a["x2"] - a["x1"]) * (a["y2"] - a["y1"]), 1)
    return inter / area_a


def build_static_target_lock_candidates(
    *,
    previous_field_scene_summary: Dict[str, Any],
    current_field_scene_summary: Dict[str, Any],
    continuity_decision: Dict[str, Any],
    field_session_ref: str = "fsess_mock",
) -> List[Dict[str, Any]]:
    status = continuity_decision.get("continuity_status", "uncertain_need_recheck")
    if status in CONTINUITY_RESET:
        return []

    prev_entities = previous_field_scene_summary.get("entities") or []
    curr_entities = current_field_scene_summary.get("entities") or []
    locks: List[Dict[str, Any]] = []

    if status in CONTINUITY_LOST:
        for ent in prev_entities:
            if not is_static_label(ent.get("label", "")):
                continue
            locks.append(_make_lock(ent, ent, field_session_ref, current_field_scene_summary, "lock_lost", "lost", 0.2, 0.3))
        return locks

    if status in CONTINUITY_FREEZE:
        for ent in curr_entities or prev_entities:
            if not is_static_label(ent.get("label", "")):
                continue
            locks.append(_make_lock(ent, ent, field_session_ref, current_field_scene_summary, "candidate_lock", "occluded", ent.get("confidence", 0.5), 0.4))
        return locks

    if status not in CONTINUITY_ALLOWED:
        return []

    used_prev: set = set()
    for cent in curr_entities:
        label = cent.get("label", "")
        if not is_static_label(label):
            continue
        match = _find_match(cent, prev_entities, used_prev)
        conf = float(cent.get("confidence", 0.8))
        if status == "field_recovering":
            lock_st, vis = "lock_recovered", "recovered"
        elif conf < 0.4:
            lock_st, vis = "weak_locked", "visible"
        else:
            lock_st, vis = "locked", "visible"
        stability = 0.85 if status == "same_field" else 0.65
        if status == "field_shift":
            stability = 0.55
        locks.append(_make_lock(match or cent, cent, field_session_ref, current_field_scene_summary, lock_st, vis, conf, stability))
    return locks


def _find_match(curr: Dict[str, Any], prev_list: List[Dict[str, Any]], used: set) -> Optional[Dict[str, Any]]:
    best, best_ov = None, 0.0
    for p in prev_list:
        pid = p.get("entity_candidate_id")
        if pid in used:
            continue
        if p.get("label") != curr.get("label"):
            continue
        ov = _overlap(p.get("bbox", {}), curr.get("bbox", {}))
        if ov > best_ov:
            best_ov, best = ov, p
    if best and best_ov < 0.1:
        return None
    if best:
        used.add(best.get("entity_candidate_id"))
    return best


def _make_lock(
    prev_ent: Dict[str, Any], curr_ent: Dict[str, Any], session_ref: str,
    scene: Dict[str, Any], lock_status: str, visibility: str, conf: float, stability: float,
) -> Dict[str, Any]:
    impact = score_target_task_impact(
        target_ref=curr_ent.get("entity_candidate_id", "ent"),
        label=curr_ent.get("label", "unknown"),
        field_zone=curr_ent.get("field_zone", "unknown"),
        visibility_status=visibility,
        risk_hint=curr_ent.get("risk_hint"),
    )
    return {
        "lock_candidate_id": f"stl_{uuid.uuid4().hex[:12]}",
        "field_session_ref": session_ref,
        "field_scene_ref": scene.get("field_scene_id", "fs_curr"),
        "entity_candidate_ref": curr_ent.get("entity_candidate_id"),
        "label": curr_ent.get("label"),
        "bbox": curr_ent.get("bbox"),
        "pseudo_3d_position": curr_ent.get("pseudo_3d_position"),
        "field_zone": curr_ent.get("field_zone", "unknown"),
        "confidence": conf,
        "lock_status": lock_status,
        "visibility_status": visibility,
        "stability_score": stability,
        "anchor_candidate": lock_status in ("locked", "lock_recovered"),
        "task_impact_hint": impact["task_impact_hint"],
        "source_refs": ["mock_frontend"],
        "evidence_refs": [curr_ent.get("entity_candidate_id")],
        "reason_codes": [f"static_lock_{lock_status}"],
        "candidate_only": True,
    }
