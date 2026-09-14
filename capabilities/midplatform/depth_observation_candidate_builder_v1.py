# -*- coding: utf-8 -*-
"""DepthObservationCandidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple


def _map_global_confidence(val: Any) -> str:
    if val is None:
        return "unknown"
    if isinstance(val, str):
        return val if val in ("high", "medium", "low", "unknown") else "low"
    try:
        f = float(val)
        if f >= 0.75:
            return "medium"
        if f >= 0.4:
            return "low"
        return "low"
    except (TypeError, ValueError):
        return "unknown"


def build_depth_observation_candidate(depth_output: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    warnings: List[str] = []
    missing: List[str] = []
    unit = depth_output.get("depth_value_unit", "unknown")
    if unit == "unknown":
        warnings.append("depth_value_unit_unknown")
    if not depth_output.get("depth_map_ref"):
        missing.append("depth_map_ref_missing")
        warnings.append("depth_map_missing_readiness_degraded")
    conf = _map_global_confidence(depth_output.get("global_depth_confidence"))
    if conf == "high" and unit == "relative":
        conf = "medium"
        warnings.append("relative_depth_confidence_capped")
    reliability = "degraded" if missing else ("low" if conf in ("low", "unknown") else "medium")
    candidate = {
        "depth_observation_id": f"dobs_{uuid.uuid4().hex[:12]}",
        "depth_output_ref": depth_output.get("depth_output_id", "depth_unknown"),
        "model_ref": depth_output.get("model_ref", "depth_anything_v2_placeholder"),
        "frame_ref": depth_output.get("frame_ref", "frame_0"),
        "timestamp": depth_output.get("timestamp", "2026-06-11T00:00:00Z"),
        "frame_width": int(depth_output.get("frame_width", 640)),
        "frame_height": int(depth_output.get("frame_height", 480)),
        "depth_map_ref": depth_output.get("depth_map_ref"),
        "depth_map_shape": depth_output.get("depth_map_shape"),
        "depth_value_unit": unit,
        "depth_source": depth_output.get("depth_source", "estimated"),
        "depth_confidence": conf,
        "depth_error_expected": True,
        "reliability_level": reliability,
        "missing_information": missing,
        "warning_codes": warnings,
        "source_refs": [depth_output.get("depth_output_id", "depth_unknown")],
        "evidence_refs": [depth_output.get("raw_payload_ref") or depth_output.get("depth_output_id")],
        "traceability_refs": [depth_output.get("frame_ref", "frame_0")],
        "candidate_only": True,
    }
    if depth_output.get("depth_source") == "hardware":
        warnings.append("hardware_depth_rejected_not_fact")
        candidate["depth_source"] = "estimated"
        candidate["warning_codes"] = list(candidate["warning_codes"]) + ["hardware_depth_not_allowed"]
    return candidate, warnings
