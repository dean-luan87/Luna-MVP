# -*- coding: utf-8 -*-
"""ObjectObservationCandidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.field_scene_small_range_static_validators_v1 import validate_object_observation


def build_object_observation_candidate(
    normalized: Dict[str, Any],
    *,
    detector_output: Dict[str, Any],
    depth_hint: float | None = None,
    depth_source: str = "unknown",
) -> Dict[str, Any]:
    fw = int(detector_output.get("frame_width", 640))
    fh = int(detector_output.get("frame_height", 480))
    conf = float(normalized.get("confidence", 0.0))
    warnings = list(normalized.get("normalization_warnings") or [])
    missing: List[str] = []
    if conf < 0.4:
        warnings.append("low_confidence_detection_retained")
    if depth_hint is None:
        missing.append("depth_hint_missing")
        depth_conf = "unknown" if depth_source == "unknown" else "low"
        depth_err = True
    else:
        depth_conf = "medium" if depth_source == "estimated" else "high"
        depth_err = depth_source in ("unknown", "estimated")
    obs = {
        "observation_id": f"obs_{uuid.uuid4().hex[:12]}",
        "source_type": "model_detector",
        "source_ref": detector_output.get("source_ref", "detector_mock"),
        "model_ref": detector_output.get("model_ref", "yolo_lightweight_placeholder"),
        "frame_ref": normalized.get("frame_ref", "frame_0"),
        "timestamp": normalized.get("timestamp", "2026-06-11T00:00:00Z"),
        "label": normalized.get("label", "unknown_object"),
        "confidence": conf,
        "bbox": dict(normalized.get("xyxy") or {}),
        "bbox_format": "xyxy",
        "frame_width": fw,
        "frame_height": fh,
        "mask_ref": None,
        "tracker_hint_id": normalized.get("tracker_hint_id"),
        "tracker_id_is_hint_not_fact": True,
        "depth_hint": depth_hint,
        "depth_source": depth_source,
        "depth_confidence": depth_conf,
        "depth_error_expected": depth_err,
        "task_relevance_hint": None,
        "risk_hint": None,
        "validation_status": "pending",
        "missing_information": missing,
        "warning_codes": warnings,
        "source_refs": [detector_output.get("detector_output_id", "det_unknown")],
        "evidence_refs": [normalized.get("normalized_detection_id")],
        "traceability_refs": [detector_output.get("frame_ref", "frame_0")],
        "candidate_only": True,
    }
    ok, issues = validate_object_observation(obs)
    obs["validation_status"] = "valid" if ok else "invalid"
    if not ok:
        obs["warning_codes"] = list(warnings) + issues
    return obs
