# -*- coding: utf-8 -*-
"""Depth real output bridge v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple


def run_or_load_depth_output(
    *,
    frame_pkg: Dict[str, Any],
    authorization: Dict[str, Any],
    depth_mode: str = "auto",
    depth_confidence: str = "medium",
    depth_value_unit: str = "metric",
    depth_samples: Optional[Dict[str, float]] = None,
    timestamp_override: str | None = None,
) -> Tuple[Optional[Dict[str, Any]], List[str], List[str]]:
    """Produce DepthRealOutputPackage per authorization matrix."""
    warnings: List[str] = []
    failure_points: List[str] = []

    if depth_mode == "missing":
        warnings.append("depth_missing_explicit")
        return None, warnings, failure_points

    depth_path = authorization.get("depth_path", "mock_adapter_with_real_frame_alignment")
    if depth_path == "blocked":
        failure_points.append("blocked_by_authorization_depth")
        return None, warnings, failure_points

    execution_mode = depth_path
    model_ref = "depth_mock_adapter_real_frame"
    if depth_path == "local_depth_adapter":
        model_ref = "local_depth_adapter_stub"
        execution_mode = "real_adapter"
    elif depth_path == "authorized_depth_model":
        model_ref = authorization.get("depth_model_ref", "authorized_depth_model_stub")
        execution_mode = "authorized_model"
    else:
        execution_mode = "mock_adapter_with_real_frame_alignment"
        model_ref = "depth_mock_adapter_real_frame"
        warnings.append("mock_depth_not_real_model")

    if depth_confidence == "low":
        warnings.append("low_depth_confidence")

    run_id = f"depth_{uuid.uuid4().hex[:12]}"
    fw, fh = frame_pkg["frame_width"], frame_pkg["frame_height"]
    samples = depth_samples or {"150_175": 2.5, "300_200": 6.0}

    pkg = {
        "depth_run_id": run_id,
        "model_ref": model_ref,
        "execution_mode": execution_mode,
        "frame_ref": frame_pkg["frame_ref"],
        "timestamp": timestamp_override or frame_pkg["timestamp"],
        "frame_width": fw,
        "frame_height": fh,
        "depth_map_ref": None,
        "depth_map_shape": [fh, fw],
        "depth_map_samples": samples,
        "depth_value_unit": depth_value_unit,
        "depth_source": "estimated",
        "depth_confidence": depth_confidence,
        "depth_error_expected": True,
        "raw_output_ref": f"raw_depth_{run_id}",
        "source_refs": [frame_pkg["source_ref"], run_id],
        "candidate_only": True,
    }
    return pkg, warnings, failure_points
