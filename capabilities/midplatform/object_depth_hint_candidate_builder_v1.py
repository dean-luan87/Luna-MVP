# -*- coding: utf-8 -*-
"""ObjectDepthHintCandidate builder for depth-object fusion v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.bbox_depth_sampling_policy_v1 import sample_depth_for_object_bbox, _bbox_valid
from capabilities.midplatform.depth_object_fusion_fallback_policy_v1 import apply_depth_object_fusion_fallback
from capabilities.midplatform.depth_object_fusion_types_v1 import REJECTED_ALIGNMENT_STATUSES


def build_object_depth_hint_candidate(
    aligned: Dict[str, Any],
    obj: Dict[str, Any],
    depth: Optional[Dict[str, Any]],
    *,
    sampling_method: str = "bbox_center_sample",
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    status = aligned.get("alignment_status", "")
    if status in REJECTED_ALIGNMENT_STATUSES:
        return None, {
            "aligned_candidate_ref": aligned.get("aligned_candidate_id"),
            "object_observation_ref": obj.get("observation_id"),
            "reason": "alignment_rejected_no_fusion",
            "alignment_status": status,
        }

    if not aligned.get("primary_object_observation_ref"):
        return None, {
            "aligned_candidate_ref": aligned.get("aligned_candidate_id"),
            "reason": "missing_primary_object_ref",
        }

    fw = int(obj.get("frame_width", 640))
    fh = int(obj.get("frame_height", 480))
    valid, bbox_reason = _bbox_valid(obj.get("bbox") or {}, fw, fh)
    if not valid:
        return None, {
            "aligned_candidate_ref": aligned.get("aligned_candidate_id"),
            "object_observation_ref": obj.get("observation_id"),
            "reason": bbox_reason,
        }

    sampled, sample_status, sample_warnings, sample_missing = sample_depth_for_object_bbox(
        obj, depth, method=sampling_method,
    )
    partial, ok = apply_depth_object_fusion_fallback(
        aligned=aligned, obj=obj, depth=depth,
        sampled=sampled, sample_status=sample_status,
        sample_warnings=sample_warnings, sample_missing=sample_missing,
    )
    if not ok and partial.get("reject_reason"):
        return None, {
            "aligned_candidate_ref": aligned.get("aligned_candidate_id"),
            "object_observation_ref": obj.get("observation_id"),
            "reason": partial.get("reject_reason"),
        }

    hint = {
        "object_depth_hint_id": f"odh_{uuid.uuid4().hex[:12]}",
        "aligned_candidate_ref": aligned.get("aligned_candidate_id"),
        "object_observation_ref": obj.get("observation_id"),
        "depth_observation_ref": aligned.get("depth_observation_ref") or (depth or {}).get("depth_observation_id"),
        "frame_ref": obj.get("frame_ref", aligned.get("frame_ref", "frame_0")),
        "timestamp": obj.get("timestamp", aligned.get("timestamp", "2026-06-11T00:00:00Z")),
        "label": obj.get("label", "unknown_object"),
        "bbox": dict(obj.get("bbox") or {}),
        "bbox_sampling_policy": sampling_method,
        **partial,
        "source_refs": [
            aligned.get("aligned_candidate_id"),
            obj.get("observation_id"),
        ] + ([depth.get("depth_observation_id")] if depth else []),
        "evidence_refs": list(obj.get("evidence_refs") or []) + list((depth or {}).get("evidence_refs") or []),
        "traceability_refs": [obj.get("frame_ref", "frame_0")],
        "candidate_only": True,
    }
    return hint, None


def build_object_depth_hints_from_fusion_input(
    fusion_input: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    aligned_list = fusion_input.get("aligned_candidates") or []
    objects_by_id = {o["observation_id"]: o for o in (fusion_input.get("object_observations") or [])}
    depths_by_id = {d["depth_observation_id"]: d for d in (fusion_input.get("depth_observations") or [])}

    hints: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    for aligned in aligned_list:
        obj_ref = aligned.get("primary_object_observation_ref")
        if not obj_ref:
            rejected.append({"aligned_candidate_ref": aligned.get("aligned_candidate_id"), "reason": "no_primary_object"})
            continue
        obj = objects_by_id.get(obj_ref)
        if not obj:
            rejected.append({"aligned_candidate_ref": aligned.get("aligned_candidate_id"), "reason": "object_not_found"})
            continue
        depth_ref = aligned.get("depth_observation_ref")
        depth = depths_by_id.get(depth_ref) if depth_ref else None
        if not depth and (fusion_input.get("depth_observations") or []):
            depth = (fusion_input.get("depth_observations") or [None])[0]

        hint, rej = build_object_depth_hint_candidate(aligned, obj, depth)
        if hint:
            hints.append(hint)
        if rej:
            rejected.append(rej)

    return hints, rejected
