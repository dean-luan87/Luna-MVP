# -*- coding: utf-8 -*-
"""Real model execution authorization resolver v1."""

from __future__ import annotations

import copy
import uuid
from typing import Any, Dict, List, Tuple


def resolve_real_model_execution_authorization(
    *,
    matrix: Dict[str, Any],
    case_overrides: Dict[str, Any] | None = None,
) -> Tuple[Dict[str, Any], Dict[str, Any], List[str]]:
    """Resolve authorization candidate and runtime policy. No implicit downloads."""
    overrides = case_overrides or {}
    auth = copy.deepcopy(matrix)
    auth.update({k: v for k, v in overrides.items() if k in auth or k.endswith("_allowed") or k.endswith("_available")})

    blocked_reasons: List[str] = []
    yolo_real = bool(auth.get("yolo_local_runner_available") and auth.get("yolo_path") == "real_runner")
    yolo_cached = auth.get("yolo_path") in ("cached_output", "cached_output_preferred", "real_runner")
    depth_path = auth.get("depth_path", "mock_adapter_with_real_frame_alignment")

    candidate = {
        "authorization_id": f"auth_{uuid.uuid4().hex[:12]}",
        "yolo_real_runner_allowed": bool(auth.get("yolo_local_runner_available")),
        "yolo_cached_output_allowed": yolo_cached,
        "depth_real_adapter_allowed": depth_path == "local_depth_adapter" and auth.get("local_depth_adapter_available"),
        "depth_authorized_model_allowed": depth_path == "authorized_depth_model" and auth.get("depth_model_download_authorized"),
        "depth_stub_allowed": depth_path == "local_depth_adapter" and not auth.get("local_depth_adapter_available", False),
        "depth_mock_fallback_allowed": depth_path == "mock_adapter_with_real_frame_alignment",
        "model_download_allowed": False,
        "weight_download_allowed": False,
        "camera_runtime_allowed": False,
        "video_stream_allowed": False,
        "candidate_only": True,
    }

    if depth_path == "blocked":
        blocked_reasons.append("blocked_by_authorization_depth")
    if not yolo_real and not yolo_cached:
        blocked_reasons.append("blocked_yolo_runner_missing")
    if auth.get("no_unauthorized_download") is not True:
        blocked_reasons.append("unauthorized_download_policy_violation")

    resolved = {
        "resolved_id": f"auth_resolved_{uuid.uuid4().hex[:12]}",
        "matrix_id": auth.get("matrix_id", "real_model_execution_authorization_matrix_v2"),
        "yolo_path": "real_runner" if yolo_real else ("cached_output" if yolo_cached else "blocked"),
        "depth_path": depth_path,
        "blocked_reasons": blocked_reasons,
        "no_unauthorized_download": True,
        "candidate_only": True,
    }
    return candidate, resolved, blocked_reasons
