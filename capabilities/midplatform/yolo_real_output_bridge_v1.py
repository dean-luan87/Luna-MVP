# -*- coding: utf-8 -*-
"""YOLO real output bridge v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple


def _bbox_valid(bbox: Dict[str, Any], fw: int, fh: int) -> bool:
    try:
        x1, y1 = float(bbox["x1"]), float(bbox["y1"])
        x2, y2 = float(bbox["x2"]), float(bbox["y2"])
    except (KeyError, TypeError, ValueError):
        return False
    return x2 > x1 and y2 > y1 and x1 >= 0 and y1 >= 0 and x2 <= fw and y2 <= fh


def run_or_load_yolo_real_output(
    *,
    frame_pkg: Dict[str, Any],
    authorization: Dict[str, Any],
    cached_detections: Optional[List[Dict[str, Any]]] = None,
    execution_mode_override: str | None = None,
) -> Tuple[Dict[str, Any], List[str], List[str]]:
    """Run or load YOLO output as YOLORealOutputPackage. Uses cached_output when no real runner."""
    warnings: List[str] = []
    failure_points: List[str] = []

    yolo_allowed = authorization.get("yolo_path") in (
        "cached_output", "real_runner", "cached_output_preferred",
    )
    if not yolo_allowed:
        failure_points.append("blocked_by_authorization_yolo")
        return {}, warnings, failure_points

    mode = execution_mode_override or authorization.get("yolo_path", "cached_output")
    if mode == "real_runner" and not authorization.get("yolo_local_runner_available"):
        mode = "cached_output"
        warnings.append("yolo_runner_unavailable_fallback_cached_output")

    detections_in = list(cached_detections or [])
    valid_dets: List[Dict[str, Any]] = []
    for i, det in enumerate(detections_in):
        bbox = det.get("bbox_xyxy") or det.get("bbox") or {}
        if not _bbox_valid(bbox, frame_pkg["frame_width"], frame_pkg["frame_height"]):
            warnings.append(f"invalid_bbox_rejected_index_{i}")
            failure_points.append(f"invalid_bbox_at_{i}")
            continue
        valid_dets.append({
            "bbox_xyxy": bbox,
            "label": det.get("label", "unknown"),
            "confidence": float(det.get("confidence", 0.5)),
            "class_id": det.get("class_id"),
            "source_refs": [frame_pkg["frame_input_id"], f"det_{i}"],
        })

    run_id = f"yolo_{uuid.uuid4().hex[:12]}"
    pkg = {
        "detector_run_id": run_id,
        "model_ref": authorization.get("yolo_model_ref", "yolo_integrated_cached"),
        "execution_mode": mode,
        "frame_ref": frame_pkg["frame_ref"],
        "timestamp": frame_pkg["timestamp"],
        "frame_width": frame_pkg["frame_width"],
        "frame_height": frame_pkg["frame_height"],
        "detections": valid_dets,
        "raw_output_ref": f"raw_yolo_{run_id}",
        "source_refs": [frame_pkg["source_ref"], run_id],
        "candidate_only": True,
    }
    if not valid_dets and detections_in:
        warnings.append("all_detections_invalid_bbox")
    return pkg, warnings, failure_points
