# -*- coding: utf-8 -*-
"""Trajectory builder v1 — short-term trend from dynamic track candidates."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def _pos_from_track(track: Dict[str, Any], which: str) -> Optional[Dict[str, float]]:
    key = f"{which}_pseudo_3d_position"
    pos = track.get(key)
    if pos and pos.get("x") is not None and pos.get("y") is not None and pos.get("z") is not None:
        return {"x": float(pos["x"]), "y": float(pos["y"]), "z": float(pos["z"])}
    bbox_key = f"{which}_bbox"
    bbox = track.get(bbox_key) or {}
    if "x1" in bbox and "x2" in bbox:
        return {
            "x": (bbox["x1"] + bbox["x2"]) / 2,
            "y": (bbox.get("y1", 0) + bbox.get("y2", 0)) / 2,
            "z": 0.0,
        }
    return None


def _delta(prev: Dict[str, float], curr: Dict[str, float]) -> Dict[str, float]:
    return {"dx": curr["x"] - prev["x"], "dy": curr["y"] - prev["y"], "dz": curr["z"] - prev["z"]}


def _motion_pattern_from_delta(delta: Dict[str, float], label: str) -> str:
    dx, dy, dz = delta["dx"], delta["dy"], delta["dz"]
    mag = abs(dx) + abs(dy) + abs(dz)
    if mag < 5:
        return "likely_static"
    if dz < -1.5:
        return "approaching_user"
    if dz > 1.5:
        return "moving_away"
    if abs(dx) > abs(dy) * 1.5:
        if dx > 30:
            return "crossing_user_path_candidate" if label == "vehicle" else "moving_right"
        if dx < -30:
            return "moving_left"
    if abs(dy) > abs(dx) * 1.5 and abs(dy) > 20:
        return "blocking_route_candidate"
    if mag > 50:
        return "moving_across_field"
    if dz < -0.5:
        return "approaching_user"
    return "uncertain_motion"


def _confidence_from_track(track: Dict[str, Any], depth_source: str = "estimated") -> tuple[str, List[str]]:
    reasons: List[str] = []
    if depth_source == "unknown":
        reasons.append("missing_depth")
        return "low", reasons
    if depth_source == "estimated":
        reasons.append("missing_depth")
        return "medium", reasons
    conf = track.get("continuity_confidence") or 0.5
    if conf < 0.5:
        reasons.append("low_confidence_track")
        return "low", reasons
    reasons.append("sufficient_position_delta")
    return "high" if conf >= 0.75 else "medium", reasons


def build_trajectory_candidates(
    *,
    tracking_plan: Dict[str, Any],
    depth_source: str = "estimated",
) -> List[Dict[str, Any]]:
    if tracking_plan.get("tracking_frozen") or tracking_plan.get("tracking_reset"):
        return []
    if not tracking_plan.get("tracking_allowed"):
        return []

    trajectories: List[Dict[str, Any]] = []
    for track in tracking_plan.get("dynamic_tracks") or []:
        prev = _pos_from_track(track, "previous")
        curr = _pos_from_track(track, "current")
        if not prev or not curr:
            continue
        delta = _delta(prev, curr)
        motion = _motion_pattern_from_delta(delta, track.get("label", ""))
        conf, reasons = _confidence_from_track(track, depth_source)
        if track.get("tracker_hint_id"):
            reasons.append("tracker_hint_present")
        else:
            reasons.append("tracker_hint_absent")
        trajectories.append({
            "trajectory_candidate_id": f"traj_{uuid.uuid4().hex[:12]}",
            "field_session_ref": tracking_plan.get("field_session_ref", "fsess_mock"),
            "dynamic_track_ref": track.get("track_candidate_id"),
            "target_label": track.get("label", "unknown"),
            "previous_position": prev,
            "current_position": curr,
            "position_delta": delta,
            "motion_pattern": motion,
            "trajectory_confidence": conf,
            "trajectory_reliability_reasons": reasons,
            "tracker_hint_id": track.get("tracker_hint_id"),
            "tracker_id_is_hint_not_fact": True,
            "source_refs": list(track.get("source_refs") or []),
            "evidence_refs": list(track.get("evidence_refs") or []),
            "reason_codes": [f"trajectory_{motion}"],
            "candidate_only": True,
        })
    return trajectories
