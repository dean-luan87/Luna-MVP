# -*- coding: utf-8 -*-
"""Real model candidate conversion v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_scene_small_range_types_v1 import bbox_center


def convert_yolo_output_to_object_observation_candidates(
    yolo_pkg: Dict[str, Any],
    frame_pkg: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    warnings: List[str] = []
    objects: List[Dict[str, Any]] = []
    for i, det in enumerate(yolo_pkg.get("detections") or []):
        bbox = dict(det.get("bbox_xyxy") or {})
        obs_id = f"obs_real_{uuid.uuid4().hex[:8]}"
        conf = float(det.get("confidence", 0.5))
        if conf < 0.5:
            warnings.append("low_confidence_detection_retained")
        objects.append({
            "observation_id": obs_id,
            "source_type": "model_detector",
            "model_ref": yolo_pkg.get("model_ref", "yolo_integrated"),
            "frame_ref": frame_pkg["frame_ref"],
            "timestamp": frame_pkg["timestamp"],
            "label": det.get("label", "unknown"),
            "confidence": conf,
            "bbox": bbox,
            "bbox_format": "xyxy",
            "frame_width": frame_pkg["frame_width"],
            "frame_height": frame_pkg["frame_height"],
            "source_refs": list(yolo_pkg.get("source_refs") or []) + [obs_id],
            "evidence_refs": [yolo_pkg.get("detector_run_id"), obs_id],
            "traceability_refs": [frame_pkg["frame_ref"], yolo_pkg.get("raw_output_ref")],
            "candidate_only": True,
        })
    return objects, warnings


def convert_depth_output_to_depth_observation_candidate(
    depth_pkg: Dict[str, Any] | None,
    frame_pkg: Dict[str, Any],
) -> Tuple[Dict[str, Any] | None, List[str]]:
    if not depth_pkg:
        return None, ["depth_observation_missing"]
    warnings: List[str] = []
    if depth_pkg.get("execution_mode") == "mock_adapter_with_real_frame_alignment":
        warnings.append("mock_depth_adapter_aligned_to_real_frame")
    did = f"depth_obs_{uuid.uuid4().hex[:8]}"
    depth = {
        "depth_observation_id": did,
        "source_type": "model_depth_estimator",
        "model_ref": depth_pkg.get("model_ref"),
        "frame_ref": frame_pkg["frame_ref"],
        "timestamp": depth_pkg.get("timestamp", frame_pkg["timestamp"]),
        "frame_width": frame_pkg["frame_width"],
        "frame_height": frame_pkg["frame_height"],
        "depth_map_ref": depth_pkg.get("depth_map_ref"),
        "depth_map_shape": depth_pkg.get("depth_map_shape", [frame_pkg["frame_height"], frame_pkg["frame_width"]]),
        "depth_map_samples": depth_pkg.get("depth_map_samples") or {},
        "depth_value_unit": depth_pkg.get("depth_value_unit", "metric"),
        "depth_source": depth_pkg.get("depth_source", "estimated"),
        "depth_confidence": depth_pkg.get("depth_confidence", "medium"),
        "depth_error_expected": True,
        "reliability_level": "medium" if depth_pkg.get("depth_confidence") == "medium" else "low",
        "source_refs": list(depth_pkg.get("source_refs") or []) + [did],
        "evidence_refs": [depth_pkg.get("depth_run_id"), did],
        "traceability_refs": [frame_pkg["frame_ref"], depth_pkg.get("raw_output_ref")],
        "candidate_only": True,
    }
    return depth, warnings
