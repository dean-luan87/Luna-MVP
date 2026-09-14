# -*- coding: utf-8 -*-
"""Spatial mapping output normalizer v1 — inspection-based candidate normalization."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple


def normalize_spatial_mapping_output_to_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str], List[str]]:
    """Normalize inspection-confirmed raw output into spatial candidates."""
    warnings: List[str] = list(raw_output.get("warning_codes") or [])
    failure_points: List[str] = []
    overrides = case_overrides or {}
    frames = adapter_input.get("_frame_packages") or []
    session_ref = adapter_input.get("session_ref", "session_unknown")
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    raw_ref = raw_output.get("raw_output_id")

    if raw_output.get("_blocked") or execution_mode.startswith("blocked"):
        failure_points.append(execution_mode)
        warnings.append("blocked_no_candidate_fabrication")
        return [], [], warnings, failure_points

    scale_status = overrides.get("scale_status", (raw_output.get("raw_quality_payload") or {}).get("scale_status", "scale_estimated"))
    drift_risk = overrides.get("drift_risk", (raw_output.get("raw_quality_payload") or {}).get("drift_risk", "low"))
    high_drift = drift_risk in ("high", "severe")

    poses: List[Dict[str, Any]] = []
    trajectories: List[Dict[str, Any]] = []

    raw_pose = raw_output.get("raw_pose_payload")
    if raw_pose and not overrides.get("no_pose"):
        for i, frame in enumerate(frames or [{}]):
            pose_conf = overrides.get("pose_confidence", "medium")
            if isinstance(raw_pose.get("confidence"), (int, float)):
                pose_conf = "high" if raw_pose["confidence"] >= 0.85 else ("medium" if raw_pose["confidence"] >= 0.6 else "low")
            if scale_status == "scale_unknown" and pose_conf == "high":
                pose_conf = "medium"
                warnings.append("scale_unknown_caps_pose_confidence")
            if overrides.get("no_pose") and i == 0:
                continue
            pose_id = f"cpc_{uuid.uuid4().hex[:12]}"
            pos = raw_pose.get("position") or {"x": 0.1 * i, "y": 0.0, "z": 0.0}
            orient = raw_pose.get("orientation") or {"yaw": 0.05 * i, "pitch": 0.0, "roll": 0.0}
            mode_warning = []
            if execution_mode == "cached_output":
                mode_warning.append("from_cached_output_not_real_run")
            if execution_mode == "adapter_stub":
                mode_warning.append("from_adapter_stub_not_real_run")
            poses.append({
                "camera_pose_candidate_id": pose_id,
                "source_raw_output_ref": raw_ref,
                "frame_ref": frame.get("frame_ref"),
                "timestamp": frame.get("timestamp"),
                "camera_ref": frame.get("camera_ref"),
                "session_ref": session_ref,
                "coordinate_mode": overrides.get("coordinate_mode", "session_local_candidate"),
                "position_candidate": pos,
                "orientation_candidate": orient,
                "pose_confidence": pose_conf,
                "scale_status": scale_status,
                "drift_risk": drift_risk,
                "quality_status": "degraded" if high_drift else "acceptable",
                "warning_codes": mode_warning,
                "missing_information": list(raw_output.get("missing_information") or []),
                "source_refs": [frame.get("frame_input_id"), adapter_input.get("adapter_input_id"), raw_ref],
                "evidence_refs": [adapter_input.get("model_ref"), adapter_input.get("smoke_run_ref")],
                "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [pose_id, raw_ref],
                "candidate_only": True,
            })

    raw_traj = raw_output.get("raw_trajectory_payload")
    if len(frames) > 1 and raw_traj and not overrides.get("no_trajectory"):
        traj_id = f"ctc_{uuid.uuid4().hex[:12]}"
        traj_conf = "medium" if high_drift else overrides.get("trajectory_confidence", "medium")
        trajectories.append({
            "camera_trajectory_candidate_id": traj_id,
            "source_raw_output_ref": raw_ref,
            "session_ref": session_ref,
            "frame_refs": [f.get("frame_ref") for f in frames],
            "pose_candidate_refs": [p["camera_pose_candidate_id"] for p in poses],
            "trajectory_confidence": traj_conf,
            "drift_summary": {"drift_risk": drift_risk, "high_drift": high_drift, **(raw_traj or {})},
            "scale_status": scale_status,
            "missing_information": overrides.get("missing_information") or [],
            "warning_codes": warnings[:3],
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "evidence_refs": [adapter_input.get("model_ref")],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [traj_id],
            "candidate_only": True,
        })

    if execution_mode in ("cached_output", "adapter_stub", "local_real_model"):
        warnings.append(f"normalized_from_{execution_mode}_inspection_result")

    return poses, trajectories, warnings, failure_points
