# -*- coding: utf-8 -*-
"""Motion candidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def _bbox_delta(bbox_seq: List[Dict[str, Any]]) -> Optional[Dict[str, float]]:
    if len(bbox_seq) < 2:
        return None
    b0 = bbox_seq[0].get("bbox") or bbox_seq[0]
    b1 = bbox_seq[-1].get("bbox") or bbox_seq[-1]
    if not isinstance(b0, (list, tuple)) or not isinstance(b1, (list, tuple)):
        return None
    if len(b0) < 2 or len(b1) < 2:
        return None
    return {"dx": float(b1[0]) - float(b0[0]), "dy": float(b1[1]) - float(b0[1])}


def _infer_motion_type(delta: Optional[Dict[str, float]], flow: Optional[Dict[str, Any]]) -> str:
    if flow and isinstance(flow.get("mean_magnitude"), (int, float)) and flow["mean_magnitude"] > 0.1:
        return "moving"
    if not delta:
        return "unknown"
    mag = abs(delta.get("dx", 0)) + abs(delta.get("dy", 0))
    if mag < 1.0:
        return "static"
    if delta.get("dy", 0) > 2:
        return "approaching"
    if delta.get("dy", 0) < -2:
        return "receding"
    if abs(delta.get("dx", 0)) > abs(delta.get("dy", 0)):
        return "crossing"
    return "moving"


def _relative_motion_hint(motion_type: str) -> str:
    mapping = {
        "approaching": "toward_user",
        "receding": "away_from_user",
        "crossing": "lateral_crossing",
        "static": "stationary",
    }
    return mapping.get(motion_type, "unknown")


def build_motion_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    tracks: List[Dict[str, Any]],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Build MotionCandidate from bbox delta and optical flow summary."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return []

    results: List[Dict[str, Any]] = []
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    raw_ref = raw_output.get("raw_output_id")
    frames = adapter_input.get("_frame_packages") or []
    frame_refs = [f.get("frame_ref") for f in frames]

    raw_motion = raw_output.get("raw_motion_payload")
    raw_flow = raw_output.get("raw_flow_payload")
    inspect_subtype = raw_output.get("_inspect_subtype", "tracking")

    if inspect_subtype == "optical_flow" or raw_flow or raw_motion:
        motion_type = _infer_motion_type(None, raw_flow)
        motion_conf = "medium" if execution_mode == "local_real_model" else "low"
        if execution_mode in ("cached_output", "adapter_stub"):
            motion_conf = "low"
        motion_id = f"mc_{uuid.uuid4().hex[:12]}"
        results.append({
            "motion_candidate_id": motion_id,
            "source_raw_output_ref": raw_ref,
            "source_track_ref": None,
            "frame_refs": frame_refs,
            "timestamp_range": raw_output.get("timestamp_range") or {},
            "motion_type": motion_type,
            "bbox_delta": None,
            "motion_vector_summary": raw_motion,
            "optical_flow_summary": raw_flow,
            "relative_motion_hint": _relative_motion_hint(motion_type),
            "motion_confidence": motion_conf,
            "risk_relevance_hint": "dynamic_obstacle_evidence" if motion_type != "static" else None,
            "warning_codes": ["from_cached_flow_not_real_run"] if execution_mode == "cached_output" else [],
            "missing_information": [],
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "evidence_refs": [adapter_input.get("model_ref")],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [motion_id],
            "candidate_only": True,
        })

    if overrides.get("force_bbox_delta") or (tracks and not results):
        for track in tracks:
            bbox_seq = track.get("bbox_sequence") or []
            delta = _bbox_delta(bbox_seq)
            if not delta and not overrides.get("force_bbox_delta"):
                continue
            if overrides.get("force_bbox_delta") and not delta:
                delta = {"dx": 2.0, "dy": 1.0}
            motion_type = overrides.get("motion_type") or _infer_motion_type(delta, None)
            motion_conf = "low"
            if execution_mode == "local_real_model":
                motion_conf = "medium"
            motion_id = f"mc_{uuid.uuid4().hex[:12]}"
            results.append({
                "motion_candidate_id": motion_id,
                "source_raw_output_ref": raw_ref,
                "source_track_ref": track.get("object_track_candidate_id"),
                "frame_refs": frame_refs,
                "timestamp_range": track.get("timestamp_range") or {},
                "motion_type": motion_type,
                "bbox_delta": delta,
                "motion_vector_summary": None,
                "optical_flow_summary": None,
                "relative_motion_hint": _relative_motion_hint(motion_type),
                "motion_confidence": motion_conf,
                "risk_relevance_hint": "moving_object_evidence" if motion_type != "static" else None,
                "warning_codes": list(track.get("warning_codes") or []),
                "missing_information": [],
                "source_refs": [track.get("object_track_candidate_id"), raw_ref],
                "evidence_refs": [adapter_input.get("model_ref")],
                "traceability_refs": list(track.get("traceability_refs") or []) + [motion_id],
                "candidate_only": True,
            })
    return results
