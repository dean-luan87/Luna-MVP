# -*- coding: utf-8 -*-
"""Multi-Model alignment builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.multi_model_alignment_signal_scoring_v1 import (
    compute_alignment_signal,
    compute_depth_only_signal,
)


def build_multi_model_aligned_observation_candidates(
    *,
    object_observations: List[Dict[str, Any]],
    depth_observation: Optional[Dict[str, Any]] = None,
    optional_observations: Optional[List[Dict[str, Any]]] = None,
    alignment_group_id: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    optional_observations = optional_observations or []
    group_id = alignment_group_id or f"ag_{uuid.uuid4().hex[:12]}"
    aligned: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    optional_by_frame = {}
    for opt in optional_observations:
        fr = opt.get("frame_ref", "frame_0")
        optional_by_frame.setdefault(fr, []).append(opt)

    if not object_observations and depth_observation:
        signal = compute_depth_only_signal(depth_observation)
        aligned.append({
            "aligned_candidate_id": f"mac_{uuid.uuid4().hex[:12]}",
            "alignment_group_id": group_id,
            "frame_ref": depth_observation.get("frame_ref", "frame_0"),
            "timestamp": depth_observation.get("timestamp", "2026-06-11T00:00:00Z"),
            "camera_ref": depth_observation.get("camera_ref"),
            "primary_object_observation_ref": None,
            "depth_observation_ref": depth_observation.get("depth_observation_id"),
            "optional_observation_refs": [],
            "alignment_status": signal["alignment_status"],
            "alignment_confidence": signal["alignment_confidence"],
            "alignment_strength": signal["overall_strength"],
            "aligned_model_roles": signal["aligned_model_roles"],
            "missing_model_roles": signal["missing_model_roles"],
            "rejected_model_outputs": signal["rejected_model_outputs"],
            "conflict_refs": signal["conflict_refs"],
            "warning_codes": signal["warning_codes"],
            "degradation_reason_codes": signal["degradation_reason_codes"],
            "source_refs": [depth_observation.get("depth_observation_id", "depth_unknown")],
            "evidence_refs": list(depth_observation.get("evidence_refs") or []),
            "traceability_refs": [depth_observation.get("frame_ref", "frame_0")],
            "candidate_only": True,
        })
        return aligned, rejected

    for obj in object_observations:
        signal = compute_alignment_signal(obj, depth_observation)
        frame_ref = obj.get("frame_ref", "frame_0")
        opt_refs = [o.get("optional_observation_id") for o in optional_by_frame.get(frame_ref, [])]
        opt_roles = signal["aligned_model_roles"][:]
        if opt_refs:
            if "optional_model" not in opt_roles:
                opt_roles.append("optional_model")
            if "optional_model" in signal["missing_model_roles"]:
                signal["missing_model_roles"] = [r for r in signal["missing_model_roles"] if r != "optional_model"]

        if signal["overall_strength"] == "rejected":
            rejected.append({
                "object_observation_ref": obj.get("observation_id"),
                "depth_observation_ref": depth_observation.get("depth_observation_id") if depth_observation else None,
                "reason": signal["alignment_status"],
                "conflict_refs": signal["conflict_refs"],
                "warning_codes": signal["warning_codes"],
            })
            continue

        depth_ref = None
        if depth_observation and signal["alignment_status"] not in (
            "rejected_frame_mismatch", "rejected_timestamp_gap",
        ):
            depth_ref = depth_observation.get("depth_observation_id")

        aligned.append({
            "aligned_candidate_id": f"mac_{uuid.uuid4().hex[:12]}",
            "alignment_group_id": group_id,
            "frame_ref": frame_ref,
            "timestamp": obj.get("timestamp", "2026-06-11T00:00:00Z"),
            "camera_ref": obj.get("camera_ref") or (depth_observation or {}).get("camera_ref"),
            "primary_object_observation_ref": obj.get("observation_id"),
            "depth_observation_ref": depth_ref,
            "optional_observation_refs": opt_refs,
            "alignment_status": signal["alignment_status"],
            "alignment_confidence": signal["alignment_confidence"],
            "alignment_strength": signal["overall_strength"],
            "aligned_model_roles": opt_roles,
            "missing_model_roles": signal["missing_model_roles"],
            "rejected_model_outputs": signal["rejected_model_outputs"],
            "conflict_refs": signal["conflict_refs"],
            "warning_codes": signal["warning_codes"],
            "degradation_reason_codes": signal["degradation_reason_codes"],
            "source_refs": [obj.get("observation_id")] + ([depth_ref] if depth_ref else []) + opt_refs,
            "evidence_refs": list(obj.get("evidence_refs") or []) + list((depth_observation or {}).get("evidence_refs") or []),
            "traceability_refs": [frame_ref],
            "candidate_only": True,
        })

    return aligned, rejected
