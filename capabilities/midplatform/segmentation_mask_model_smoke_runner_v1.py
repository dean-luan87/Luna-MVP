# -*- coding: utf-8 -*-
"""Segmentation / Mask Model smoke runner v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.segmentation_mask_model_availability_checker_v1 import (
    check_segmentation_mask_availability,
)
from capabilities.midplatform.segmentation_mask_model_smoke_io_inspection_items_v1 import (
    ADAPTER_STUB_IO_SAMPLE,
    CACHED_FREESPACE_OUTPUT_SAMPLE,
    CACHED_GROUNDED_SAM_OUTPUT_SAMPLE,
    CACHED_SAM_OUTPUT_SAMPLE,
)


def _mock_frame_input(case_id: str) -> Dict[str, Any]:
    return {
        "frame_input_id": f"rfi_seg_{case_id}",
        "frame_ref": f"frame_seg_{case_id}",
        "timestamp": "2026-06-11T10:00:00Z",
        "frame_width": 640,
        "frame_height": 480,
        "source_ref": "segmentation_smoke_io_fixture",
        "fixture_type": "local_real_image_fixture",
        "candidate_only": True,
    }


def _mock_object_observation(case_id: str) -> Dict[str, Any]:
    return {
        "object_observation_id": f"ooc_seg_{case_id}",
        "observation_id": f"ooc_seg_{case_id}",
        "label": "obstacle",
        "bbox": [80, 60, 320, 280],
        "confidence": 0.85,
        "candidate_only": True,
    }


def _authorization_candidate(*, mode: str, matrix: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "authorization_id": f"auth_{uuid.uuid4().hex[:12]}",
        "model_role": "segmentation_mask_model",
        "local_real_model_allowed": mode in ("local_real_model", "local_adapter"),
        "cached_output_allowed": mode == "cached_output",
        "adapter_stub_allowed": mode == "adapter_stub",
        "model_download_allowed": bool(matrix.get("model_download_authorized")),
        "weight_download_allowed": bool(matrix.get("weight_download_authorized")),
        "camera_runtime_allowed": bool(matrix.get("camera_runtime_authorized")),
        "video_stream_allowed": bool(matrix.get("video_stream_authorized")),
        "blocked_modes": (
            "blocked_by_authorization", "blocked_by_missing_dependency", "blocked_by_missing_weight",
        ),
        "candidate_only": True,
    }


def _cached_sample(subtype: str) -> Dict[str, Any]:
    if subtype == "sam":
        return dict(CACHED_SAM_OUTPUT_SAMPLE)
    if subtype == "freespace":
        return dict(CACHED_FREESPACE_OUTPUT_SAMPLE)
    return dict(CACHED_GROUNDED_SAM_OUTPUT_SAMPLE)


def run_segmentation_mask_model_smoke(
    *,
    case_id: str,
    matrix: Dict[str, Any],
    case_overrides: Optional[Dict[str, Any]] = None,
    inspect_subtype: str = "segmentation",
) -> Tuple[Dict[str, Any], Dict[str, Any], List[str], List[str]]:
    """Run minimal smoke / blocked classification. No downloads, no camera."""
    avail, mode, warnings = check_segmentation_mask_availability(
        matrix=matrix, case_overrides=case_overrides, inspect_subtype=inspect_subtype,
    )
    frame = _mock_frame_input(case_id)
    obs = _mock_object_observation(case_id)
    input_refs = [frame["frame_input_id"], obs["object_observation_id"]]
    failure_points: List[str] = []
    output_refs: List[str] = []
    raw_output: Dict[str, Any] = {}
    execution_status = "completed"
    auth = _authorization_candidate(mode=mode, matrix=avail)

    if mode == "local_real_model":
        raw_output = {
            "raw_output_id": f"raw_{uuid.uuid4().hex[:12]}",
            "mask": "mask_local_fixture_001",
            "bbox": [80, 60, 320, 280],
            "confidence": 0.78,
            "source": "minimal_local_segmentation_fixture",
        }
        output_refs = [raw_output["raw_output_id"]]
        warnings.append("minimal_smoke_fixture_only_not_production")
    elif mode == "cached_output":
        sample = _cached_sample(inspect_subtype)
        raw_output = sample
        output_refs = [sample["sample_id"]]
        warnings.append("cached_output_inspection_not_real_run")
    elif mode == "adapter_stub":
        sample = dict(ADAPTER_STUB_IO_SAMPLE)
        raw_output = sample
        output_refs = [sample["sample_id"]]
        warnings.append("adapter_stub_inspection_not_real_run")
    elif mode.startswith("blocked"):
        execution_status = "blocked"
        failure_points.append(mode)
        warnings.append(f"{mode}_no_auto_download")
    else:
        execution_status = "failed"
        failure_points.append("failed_runtime_error")
        mode = "failed_runtime_error"

    smoke_run = {
        "smoke_run_id": f"smoke_{uuid.uuid4().hex[:12]}",
        "model_role": "segmentation_mask_model",
        "model_name": avail.get("model_name", f"segmentation_mask_{inspect_subtype}"),
        "model_ref": avail.get("model_ref", "segmentation_mask_inspection_v1"),
        "execution_mode": mode,
        "input_refs": input_refs,
        "output_refs": output_refs,
        "execution_status": execution_status,
        "runtime_environment_summary": {
            "production_runtime": False,
            "camera_runtime": False,
            "video_stream": False,
            "download_attempted": False,
            "dependency_install_attempted": False,
        },
        "failure_points": failure_points,
        "warning_codes": warnings,
        "candidate_only": True,
        "_raw_output": raw_output,
        "_frame_input": frame,
        "_object_observation": obs,
        "_inspect_subtype": inspect_subtype,
        "_authorization_candidate": auth,
    }
    return smoke_run, auth, warnings, failure_points
