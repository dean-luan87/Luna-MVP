# -*- coding: utf-8 -*-
"""Spatial mapping raw output loader v1 — loads from smoke IO inspection results."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.slam_spatial_mapping_model_smoke_io_inspection_items_v1 import (
    ADAPTER_STUB_IO_SAMPLE,
    CACHED_SLAM_OUTPUT_SAMPLE,
)


def load_spatial_mapping_raw_output_candidate(
    *,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    frame_refs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Load raw output candidate from inspection-confirmed smoke run. No real SLAM execution."""
    mode = smoke_run.get("execution_mode", "blocked_by_authorization")
    smoke_ref = smoke_run.get("smoke_run_id")
    io_ref = io_inspection.get("io_inspection_id")
    warnings: List[str] = list(smoke_run.get("warning_codes") or [])
    missing: List[str] = list(io_inspection.get("missing_information") or [])
    raw_id = smoke_run.get("output_refs", [f"raw_{uuid.uuid4().hex[:12]}"])[0] if smoke_run.get("output_refs") else f"raw_{uuid.uuid4().hex[:12]}"

    if mode.startswith("blocked"):
        return {
            "raw_output_id": raw_id,
            "source_smoke_run_ref": smoke_ref,
            "source_io_inspection_ref": io_ref,
            "model_ref": smoke_run.get("model_ref"),
            "execution_mode": mode,
            "frame_refs": frame_refs or [],
            "timestamp_range": {"start": None, "end": None},
            "output_payload_type": "blocked",
            "raw_pose_payload": None,
            "raw_trajectory_payload": None,
            "raw_anchor_payload": None,
            "raw_map_payload": None,
            "raw_quality_payload": None,
            "parseability_status": "not_applicable",
            "warning_codes": warnings + [f"{mode}_no_output_fabrication"],
            "missing_information": missing + ["blocked_no_raw_output"],
            "source_refs": list(smoke_run.get("input_refs") or []) + [smoke_ref, io_ref],
            "traceability_refs": list(smoke_run.get("input_refs") or []) + [raw_id, smoke_ref, io_ref],
            "candidate_only": True,
            "_blocked": True,
        }

    raw_pose = None
    raw_traj = None
    raw_map = None
    raw_quality = None
    payload_type = io_inspection.get("output_payload_type", "unknown")

    if mode == "local_real_model":
        raw_pose = {"position": {"x": 0.0, "y": 0.0, "z": 0.0}, "orientation": {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}, "confidence": 0.75}
        payload_type = "minimal_smoke_output"
        warnings.append("local_real_model_from_inspection_fixture_not_production_slam")
    elif mode == "cached_output":
        outputs = CACHED_SLAM_OUTPUT_SAMPLE.get("outputs") or {}
        raw_pose = outputs.get("pose")
        raw_traj = outputs.get("trajectory")
        raw_map = outputs.get("local_map")
        raw_quality = outputs.get("quality")
        payload_type = "cached_slam_output_bundle"
        warnings.append("cached_output_from_inspection_not_real_run")
    elif mode == "adapter_stub":
        raw_pose = {"position": {"x": 0.0, "y": 0.0, "z": 0.0}, "orientation": {"yaw": 0.0}, "confidence": 0.5, "stub": True}
        payload_type = "adapter_stub_design"
        warnings.append("adapter_stub_from_inspection_not_real_run")
    elif mode == "local_adapter":
        raw_pose = {"position": {"x": 0.2, "y": 0.0, "z": 0.0}, "orientation": {"yaw": 0.1}}
        payload_type = "local_adapter_output"
        warnings.append("local_adapter_from_inspection")

    parseability = io_inspection.get("parseability_status", "parseable")
    if mode == "adapter_stub":
        parseability = "design_parseable"

    return {
        "raw_output_id": raw_id,
        "source_smoke_run_ref": smoke_ref,
        "source_io_inspection_ref": io_ref,
        "model_ref": smoke_run.get("model_ref"),
        "execution_mode": mode,
        "frame_refs": frame_refs or list(smoke_run.get("input_refs") or []),
        "timestamp_range": {"start": "2026-06-11T10:00:00Z", "end": "2026-06-11T10:00:02Z"},
        "output_payload_type": payload_type,
        "raw_pose_payload": raw_pose,
        "raw_trajectory_payload": raw_traj,
        "raw_anchor_payload": None,
        "raw_map_payload": raw_map,
        "raw_quality_payload": raw_quality,
        "parseability_status": parseability,
        "warning_codes": sorted(set(warnings)),
        "missing_information": missing,
        "source_refs": list(smoke_run.get("input_refs") or []) + [smoke_ref, io_ref, raw_id],
        "traceability_refs": list(smoke_run.get("input_refs") or []) + [raw_id, smoke_ref, io_ref],
        "candidate_only": True,
        "_blocked": False,
        "_stub_sample": ADAPTER_STUB_IO_SAMPLE if mode == "adapter_stub" else None,
    }
