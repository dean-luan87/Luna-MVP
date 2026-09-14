# -*- coding: utf-8 -*-
"""Real image set loader v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.real_frame_input_loader_v1 import load_real_frame_input_package


def load_real_frame_input_set(
    *,
    image_set_ref: str,
    frame_specs: List[Dict[str, Any]],
    work_dir: str,
    source_ref: str = "real_image_set_v1",
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[str]]:
    """Load a set of real frame fixtures. No camera / video stream."""
    frames: List[Dict[str, Any]] = []
    failure_points: List[str] = []

    for spec in frame_specs:
        case_id = spec["case_id"]
        frame_pkg, fps = load_real_frame_input_package(
            frame_input_id=f"rfi_{case_id}",
            image_path=spec.get("image_path", f"/tmp/real_frames/{case_id}.png"),
            frame_ref=spec.get("frame_ref", f"frame_{case_id}"),
            frame_width=spec.get("frame_width", 640),
            frame_height=spec.get("frame_height", 480),
            timestamp=spec.get("timestamp", "2026-06-11T10:00:00Z"),
            test_case_id=case_id,
            source_ref=source_ref,
            work_dir=work_dir,
            expected_scene_notes=spec.get("expected_scene_notes"),
        )
        if not frame_pkg:
            failure_points.extend(fps)
            failure_points.append(f"frame_load_failed_{case_id}")
            continue
        frame_pkg["fixture_type"] = spec.get("fixture_type", "local_real_image_fixture")
        frames.append(frame_pkg)
        failure_points.extend(fps)

    package = {
        "execution_input_id": f"rei_{uuid.uuid4().hex[:12]}",
        "image_set_ref": image_set_ref,
        "frame_inputs": [f["frame_input_id"] for f in frames],
        "yolo_execution_policy": "real_runner_preferred_cached_fallback",
        "depth_execution_policy": "real_adapter_preferred_explicit_fallback",
        "authorization_ref": "real_model_execution_authorization_matrix_v2",
        "dryrun_scope": "controlled_offline_execution_path_hardening",
        "candidate_only": True,
    }
    return package, frames, failure_points
