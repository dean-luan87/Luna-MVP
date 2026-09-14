# -*- coding: utf-8 -*-
"""Multi-Model alignment signal scoring v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.multi_model_alignment_types_v1 import (
    TIMESTAMP_REJECT_GAP_SEC,
    TIMESTAMP_STRONG_GAP_SEC,
    TIMESTAMP_WEAK_GAP_SEC,
)


def _parse_ts_sec(ts: str) -> float:
    try:
        parts = ts.replace("Z", "").split("T")
        if len(parts) != 2:
            return 0.0
        h, m, s = parts[1].split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    except (ValueError, IndexError):
        return 0.0


def score_frame_ref_alignment(obj_frame: str, other_frame: str) -> Tuple[str, str]:
    if obj_frame == other_frame:
        return "strong", "same_frame_ref"
    return "rejected", "frame_ref_mismatch"


def score_timestamp_alignment(obj_ts: str, other_ts: str) -> Tuple[str, str, List[str]]:
    gap = abs(_parse_ts_sec(obj_ts) - _parse_ts_sec(other_ts))
    warnings: List[str] = []
    if gap <= TIMESTAMP_STRONG_GAP_SEC:
        return "strong", "timestamp_aligned", warnings
    if gap <= TIMESTAMP_WEAK_GAP_SEC:
        warnings.append("timestamp_small_gap")
        return "medium", "timestamp_small_gap_weak", warnings
    if gap <= TIMESTAMP_REJECT_GAP_SEC:
        warnings.append("timestamp_gap_degraded")
        return "weak", "timestamp_gap_degraded", warnings
    warnings.append("timestamp_large_gap_rejected")
    return "rejected", "rejected_timestamp_gap", warnings


def score_camera_ref_alignment(
    obj_cam: Optional[str], other_cam: Optional[str],
) -> Tuple[str, str, List[str]]:
    warnings: List[str] = []
    if not obj_cam and not other_cam:
        return "strong", "camera_ref_both_absent", warnings
    if not obj_cam or not other_cam:
        return "medium", "camera_ref_partial_missing", warnings
    if obj_cam == other_cam:
        return "strong", "same_camera_ref", warnings
    warnings.append("camera_ref_mismatch")
    return "weak", "camera_ref_mismatch_degraded", warnings


def score_frame_size_alignment(
    obj_w: int, obj_h: int, other_w: int, other_h: int,
) -> Tuple[str, str, List[str]]:
    warnings: List[str] = []
    if obj_w == other_w and obj_h == other_h:
        return "strong", "frame_size_match", warnings
    warnings.append("frame_size_mismatch")
    return "weak", "frame_size_mismatch_warning", warnings


def score_model_role_presence(
    *,
    has_object: bool,
    has_depth: bool,
    has_optional: bool,
) -> Tuple[List[str], List[str]]:
    aligned_roles: List[str] = []
    missing_roles: List[str] = []
    if has_object:
        aligned_roles.append("detector_yolo")
    else:
        missing_roles.append("detector_yolo")
    if has_depth:
        aligned_roles.append("depth_model")
    else:
        missing_roles.append("depth_model")
    if has_optional:
        aligned_roles.append("optional_model")
    return aligned_roles, missing_roles


def compute_alignment_signal(
    obj: Dict[str, Any],
    depth: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    warnings: List[str] = []
    degradation: List[str] = []
    conflicts: List[str] = []
    rejected: List[Dict[str, Any]] = []

    if not depth:
        roles, missing = score_model_role_presence(has_object=True, has_depth=False, has_optional=False)
        return {
            "signal_id": f"sig_{obj.get('observation_id', 'obj')}_no_depth",
            "frame_ref_score": "strong",
            "timestamp_score": "strong",
            "camera_ref_score": "medium",
            "frame_size_score": "strong",
            "model_role_presence": "depth_missing",
            "overall_strength": "medium",
            "alignment_status": "aligned_degraded",
            "alignment_confidence": "medium",
            "aligned_model_roles": roles,
            "missing_model_roles": missing,
            "rejected_model_outputs": rejected,
            "conflict_refs": conflicts,
            "warning_codes": ["missing_depth_keeps_object"],
            "degradation_reason_codes": ["depth_model_output_missing"],
        }

    frame_score, frame_reason = score_frame_ref_alignment(
        obj.get("frame_ref", "frame_0"), depth.get("frame_ref", "frame_0"),
    )
    if frame_score == "rejected":
        rejected.append({"model_role": "depth_model", "reason": frame_reason, "ref": depth.get("depth_observation_id")})
        conflicts.append(f"frame_mismatch:{obj.get('frame_ref')}:{depth.get('frame_ref')}")
        return {
            "signal_id": f"sig_{obj.get('observation_id')}_frame_reject",
            "frame_ref_score": frame_score,
            "timestamp_score": "rejected",
            "camera_ref_score": "rejected",
            "frame_size_score": "rejected",
            "model_role_presence": "frame_mismatch",
            "overall_strength": "rejected",
            "alignment_status": "rejected_frame_mismatch",
            "alignment_confidence": "rejected",
            "aligned_model_roles": ["detector_yolo"],
            "missing_model_roles": ["depth_model"],
            "rejected_model_outputs": rejected,
            "conflict_refs": conflicts,
            "warning_codes": ["frame_ref_mismatch_rejected"],
            "degradation_reason_codes": degradation,
        }

    ts_score, ts_reason, ts_warn = score_timestamp_alignment(
        obj.get("timestamp", "2026-06-11T00:00:00Z"),
        depth.get("timestamp", "2026-06-11T00:00:00Z"),
    )
    warnings.extend(ts_warn)
    if ts_score == "rejected":
        rejected.append({"model_role": "depth_model", "reason": ts_reason, "ref": depth.get("depth_observation_id")})
        conflicts.append(f"timestamp_gap:{ts_reason}")
        return {
            "signal_id": f"sig_{obj.get('observation_id')}_ts_reject",
            "frame_ref_score": frame_score,
            "timestamp_score": ts_score,
            "camera_ref_score": "rejected",
            "frame_size_score": "rejected",
            "model_role_presence": "timestamp_reject",
            "overall_strength": "rejected",
            "alignment_status": "rejected_timestamp_gap",
            "alignment_confidence": "rejected",
            "aligned_model_roles": ["detector_yolo"],
            "missing_model_roles": ["depth_model"],
            "rejected_model_outputs": rejected,
            "conflict_refs": conflicts,
            "warning_codes": warnings,
            "degradation_reason_codes": degradation,
        }

    cam_score, cam_reason, cam_warn = score_camera_ref_alignment(
        obj.get("camera_ref"), depth.get("camera_ref"),
    )
    warnings.extend(cam_warn)
    if cam_score == "weak":
        degradation.append(cam_reason)

    size_score, size_reason, size_warn = score_frame_size_alignment(
        int(obj.get("frame_width", 640)), int(obj.get("frame_height", 480)),
        int(depth.get("frame_width", 640)), int(depth.get("frame_height", 480)),
    )
    warnings.extend(size_warn)
    if size_score == "weak":
        degradation.append(size_reason)

    roles, missing = score_model_role_presence(has_object=True, has_depth=True, has_optional=False)
    scores = [frame_score, ts_score, cam_score, size_score]
    if "rejected" in scores:
        overall = "rejected"
        status = "rejected_camera_mismatch" if cam_score == "rejected" else "rejected_timestamp_gap"
        conf = "rejected"
    elif "weak" in scores:
        overall = "weak"
        status = "aligned_weak" if ts_score in ("medium", "weak") else "aligned_degraded"
        conf = "low"
    elif "medium" in scores:
        overall = "medium"
        status = "aligned_weak"
        conf = "medium"
    else:
        overall = "strong"
        status = "aligned_strong"
        conf = "high"

    return {
        "signal_id": f"sig_{obj.get('observation_id', 'obj')}_{depth.get('depth_observation_id', 'depth')}",
        "frame_ref_score": frame_score,
        "timestamp_score": ts_score,
        "camera_ref_score": cam_score,
        "frame_size_score": size_score,
        "model_role_presence": "both_present",
        "overall_strength": overall,
        "alignment_status": status,
        "alignment_confidence": conf,
        "aligned_model_roles": roles,
        "missing_model_roles": missing,
        "rejected_model_outputs": rejected,
        "conflict_refs": conflicts,
        "warning_codes": warnings,
        "degradation_reason_codes": degradation,
    }


def compute_depth_only_signal(depth: Dict[str, Any]) -> Dict[str, Any]:
    roles, missing = score_model_role_presence(has_object=False, has_depth=True, has_optional=False)
    return {
        "signal_id": f"sig_depth_only_{depth.get('depth_observation_id', 'depth')}",
        "frame_ref_score": "strong",
        "timestamp_score": "strong",
        "camera_ref_score": "medium",
        "frame_size_score": "strong",
        "model_role_presence": "depth_without_object",
        "overall_strength": "weak",
        "alignment_status": "insufficient_alignment",
        "alignment_confidence": "low",
        "aligned_model_roles": roles,
        "missing_model_roles": missing,
        "rejected_model_outputs": [],
        "conflict_refs": ["depth_without_object_no_entity_alignment"],
        "warning_codes": ["depth_without_object_insufficient_alignment"],
        "degradation_reason_codes": ["no_primary_object_anchor"],
    }
