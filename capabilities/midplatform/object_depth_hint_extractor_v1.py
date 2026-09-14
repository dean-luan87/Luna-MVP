# -*- coding: utf-8 -*-
"""Object depth hint extractor v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.depth_fallback_policy_v1 import (
    apply_depth_estimated_hint,
    apply_depth_missing_fallback,
    apply_depth_unreliable_fallback,
)
from capabilities.midplatform.depth_observation_candidate_ingestion_types_v1 import TIMESTAMP_GAP_THRESHOLD_SEC
from capabilities.midplatform.field_scene_small_range_types_v1 import bbox_center


def _parse_ts_sec(ts: str) -> float:
    try:
        parts = ts.replace("Z", "").split("T")
        if len(parts) != 2:
            return 0.0
        h, m, s = parts[1].split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    except (ValueError, IndexError):
        return 0.0


def _bbox_valid(bbox: Dict[str, Any], fw: int, fh: int) -> Tuple[bool, str]:
    if not bbox:
        return False, "missing_bbox"
    try:
        x1, y1 = float(bbox.get("x1", 0)), float(bbox.get("y1", 0))
        x2, y2 = float(bbox.get("x2", 0)), float(bbox.get("y2", 0))
    except (TypeError, ValueError):
        return False, "invalid_bbox_coords"
    if x2 <= x1 or y2 <= y1:
        return False, "invalid_bbox_dimensions"
    if x1 < 0 or y1 < 0 or x2 > fw or y2 > fh:
        return False, "bbox_out_of_frame"
    return True, ""


def _sample_depth_at_center(
    depth_output: Dict[str, Any],
    center: Dict[str, float],
) -> float | None:
    samples = depth_output.get("depth_map_samples") or {}
    key = f"{int(center['x'])}_{int(center['y'])}"
    if key in samples:
        return float(samples[key])
    grid = depth_output.get("depth_map_grid")
    if grid and isinstance(grid, list):
        cy, cx = int(center["y"]), int(center["x"])
        if 0 <= cy < len(grid) and 0 <= cx < len(grid[cy]):
            return float(grid[cy][cx])
    dr = depth_output.get("depth_value_range")
    if dr and len(dr) >= 2:
        return (float(dr[0]) + float(dr[1])) / 2.0
    return None


def extract_object_depth_hint_candidates(
    depth_observation: Dict[str, Any],
    object_observations: List[Dict[str, Any]],
    *,
    depth_output: Dict[str, Any] | None = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    hints: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []
    global_warnings: List[str] = []
    depth_ref = depth_observation.get("depth_observation_id", "dobs_unknown")
    depth_frame = depth_observation.get("frame_ref", "frame_0")
    depth_ts = depth_observation.get("timestamp", "2026-06-11T00:00:00Z")
    fw = int(depth_observation.get("frame_width", 640))
    fh = int(depth_observation.get("frame_height", 480))
    depth_map_missing = not depth_observation.get("depth_map_ref")
    depth_conf_global = depth_observation.get("depth_confidence", "unknown")
    depth_range = None
    if depth_output and depth_output.get("depth_value_range"):
        dr = depth_output["depth_value_range"]
        depth_range = (float(dr[0]), float(dr[1]))

    for obs in object_observations:
        obs_ref = obs.get("observation_id", "obs_unknown")
        obs_frame = obs.get("frame_ref", "frame_0")
        obs_ts = obs.get("timestamp", "2026-06-11T00:00:00Z")
        bbox = obs.get("bbox") or {}
        label = obs.get("label", "unknown_object")

        if obs_frame != depth_frame:
            rejected.append({
                "object_observation_ref": obs_ref,
                "reason": "frame_ref_mismatch",
                "object_frame": obs_frame,
                "depth_frame": depth_frame,
            })
            global_warnings.append("frame_ref_mismatch_rejected")
            continue

        ts_gap = abs(_parse_ts_sec(obs_ts) - _parse_ts_sec(depth_ts))
        ts_warning = ts_gap > TIMESTAMP_GAP_THRESHOLD_SEC

        valid, reason = _bbox_valid(bbox, fw, fh)
        if not valid:
            rejected.append({"object_observation_ref": obs_ref, "reason": reason, "bbox": bbox})
            global_warnings.append("bbox_invalid_rejected_for_depth_hint")
            continue

        center = bbox_center(bbox)
        if depth_map_missing:
            partial = apply_depth_missing_fallback(
                object_observation_ref=obs_ref, label=label, bbox=bbox,
                frame_ref=obs_frame, timestamp=obs_ts, depth_observation_ref=depth_ref,
            )
        elif depth_conf_global == "low" or depth_conf_global == "unknown":
            sampled = _sample_depth_at_center(depth_output or {}, center)
            partial = apply_depth_unreliable_fallback(
                object_observation_ref=obs_ref, label=label, bbox=bbox,
                frame_ref=obs_frame, timestamp=obs_ts, depth_observation_ref=depth_ref,
                sampled_depth_value=sampled, reason="low_global_depth_confidence",
            )
        else:
            sampled = _sample_depth_at_center(depth_output or {}, center)
            if sampled is None:
                partial = apply_depth_missing_fallback(
                    object_observation_ref=obs_ref, label=label, bbox=bbox,
                    frame_ref=obs_frame, timestamp=obs_ts, depth_observation_ref=depth_ref,
                )
            else:
                partial = apply_depth_estimated_hint(
                    object_observation_ref=obs_ref, label=label, bbox=bbox,
                    frame_ref=obs_frame, timestamp=obs_ts, depth_observation_ref=depth_ref,
                    sampled_depth_value=sampled, depth_range=depth_range,
                    depth_confidence=depth_conf_global,
                )

        if ts_warning:
            partial["warning_codes"] = list(partial.get("warning_codes") or []) + ["timestamp_gap_warning"]
            partial["depth_confidence"] = "low"
            partial["depth_reliability_reasons"] = list(partial.get("depth_reliability_reasons") or []) + ["timestamp_gap"]
            global_warnings.append("timestamp_gap_warning")

        hint = {
            "object_depth_hint_id": f"odh_{uuid.uuid4().hex[:12]}",
            **partial,
            "source_refs": [obs_ref, depth_ref],
            "evidence_refs": [depth_observation.get("depth_output_ref", "depth_unknown")],
        }
        hints.append(hint)

    return hints, rejected, global_warnings
