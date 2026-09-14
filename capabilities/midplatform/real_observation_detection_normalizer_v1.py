# -*- coding: utf-8 -*-
"""Real observation detection normalizer v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple


def _xyxy_to_luna_bbox(xyxy: Dict[str, float]) -> Dict[str, float]:
    return {"x1": float(xyxy["x1"]), "y1": float(xyxy["y1"]), "x2": float(xyxy["x2"]), "y2": float(xyxy["y2"])}


def _bbox_valid(bbox: Dict[str, float]) -> bool:
    return bbox["x2"] > bbox["x1"] and bbox["y2"] > bbox["y1"] and bbox["x1"] >= 0 and bbox["y1"] >= 0


def _clip_bbox_to_frame(bbox: Dict[str, float], fw: int, fh: int) -> Tuple[Dict[str, float], List[str]]:
    warnings: List[str] = []
    x1, y1, x2, y2 = bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]
    if x2 > fw or y2 > fh or x1 < 0 or y1 < 0:
        warnings.append("bbox_out_of_frame_clipped")
    clipped = {
        "x1": max(0.0, min(x1, fw)),
        "y1": max(0.0, min(y1, fh)),
        "x2": max(0.0, min(x2, fw)),
        "y2": max(0.0, min(y2, fh)),
    }
    return clipped, warnings


def normalize_detector_output_to_luna_detection(
    detector_output: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str]]:
    """Return normalized detections, rejected detections, global warnings."""
    normalized: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []
    global_warnings: List[str] = []
    fw = int(detector_output.get("frame_width", 640))
    fh = int(detector_output.get("frame_height", 480))
    frame_ref = detector_output.get("frame_ref", "frame_0")
    timestamp = detector_output.get("timestamp", "2026-06-11T00:00:00Z")
    source_id = detector_output.get("detector_output_id", "det_unknown")

    for idx, det in enumerate(detector_output.get("detections") or []):
        xyxy_raw = det.get("bbox_xyxy") or det.get("xyxy") or {}
        if not all(k in xyxy_raw for k in ("x1", "y1", "x2", "y2")):
            rejected.append({"detection_index": idx, "reason": "missing_bbox_xyxy", "raw": det})
            continue
        bbox = _xyxy_to_luna_bbox(xyxy_raw)
        if not _bbox_valid(bbox):
            rejected.append({"detection_index": idx, "reason": "invalid_bbox", "raw": det})
            continue
        norm_warnings: List[str] = []
        if bbox["x2"] > fw or bbox["y2"] > fh or bbox["x1"] < 0 or bbox["y1"] < 0:
            bbox, clip_warns = _clip_bbox_to_frame(bbox, fw, fh)
            norm_warnings.extend(clip_warns)
            if not _bbox_valid(bbox):
                rejected.append({"detection_index": idx, "reason": "invalid_bbox_after_clip", "raw": det})
                continue
        label = det.get("class_name") or det.get("label")
        if not label:
            label = "unknown_object" if det.get("class_id") is not None else "unknown_object"
            norm_warnings.append("unknown_class_label_fallback")
        normalized.append({
            "normalized_detection_id": f"nd_{uuid.uuid4().hex[:12]}",
            "source_detector_output_ref": source_id,
            "frame_ref": frame_ref,
            "timestamp": timestamp,
            "xyxy": bbox,
            "label": label,
            "confidence": float(det.get("confidence", 0.0)),
            "class_id": det.get("class_id"),
            "tracker_hint_id": det.get("tracker_hint_id"),
            "normalization_warnings": norm_warnings,
            "candidate_only": True,
        })
    return normalized, rejected, global_warnings
