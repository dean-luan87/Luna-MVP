# -*- coding: utf-8 -*-
"""Tracking / Optical Flow raw output loader v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.tracking_opticalflow_model_smoke_io_inspection_items_v1 import (
    ADAPTER_STUB_IO_SAMPLE,
    CACHED_FLOW_OUTPUT_SAMPLE,
    CACHED_TRACKING_OUTPUT_SAMPLE,
)


def load_tracking_opticalflow_raw_output_candidate(
    *,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    frame_refs: Optional[List[str]] = None,
    inspect_subtype: str = "tracking",
) -> Dict[str, Any]:
    """Load raw output from inspection-confirmed smoke run. No real tracker/flow execution."""
    mode = smoke_run.get("execution_mode", "blocked_by_authorization")
    smoke_ref = smoke_run.get("smoke_run_id")
    io_ref = io_inspection.get("io_inspection_id")
    warnings: List[str] = list(smoke_run.get("warning_codes") or [])
    missing: List[str] = list(io_inspection.get("missing_information") or [])
    raw_id = (
        smoke_run.get("output_refs", [f"raw_{uuid.uuid4().hex[:12]}"])[0]
        if smoke_run.get("output_refs")
        else f"raw_{uuid.uuid4().hex[:12]}"
    )

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
            "raw_track_payload": None,
            "raw_bbox_sequence_payload": None,
            "raw_motion_payload": None,
            "raw_flow_payload": None,
            "raw_quality_payload": None,
            "parseability_status": "not_applicable",
            "warning_codes": warnings + [f"{mode}_no_output_fabrication"],
            "missing_information": missing + ["blocked_no_raw_output"],
            "source_refs": list(smoke_run.get("input_refs") or []) + [smoke_ref, io_ref],
            "traceability_refs": list(smoke_run.get("input_refs") or []) + [raw_id, smoke_ref, io_ref],
            "candidate_only": True,
            "_blocked": True,
            "_inspect_subtype": inspect_subtype,
        }

    raw_track = None
    raw_bbox = None
    raw_motion = None
    raw_flow = None
    raw_quality = None
    payload_type = io_inspection.get("output_payload_type", "unknown")

    if mode == "local_real_model":
        raw_track = {
            "track_id": "trk_smoke_fixture_001",
            "bbox_sequence": [{"frame": 0, "bbox": [10, 20, 50, 80]}],
            "track_confidence": 0.7,
            "lifecycle_status": "active",
        }
        raw_bbox = raw_track.get("bbox_sequence")
        payload_type = "minimal_smoke_output"
        warnings.append("local_real_model_from_inspection_fixture_not_production_tracker")
    elif mode == "cached_output":
        if inspect_subtype == "optical_flow":
            outputs = CACHED_FLOW_OUTPUT_SAMPLE.get("outputs") or {}
            raw_motion = outputs.get("motion_vector")
            raw_flow = outputs.get("flow_map_summary")
            payload_type = "cached_optical_flow_output_bundle"
            warnings.append("cached_output_from_inspection_not_real_run")
        else:
            outputs = CACHED_TRACKING_OUTPUT_SAMPLE.get("outputs") or {}
            raw_track = outputs
            raw_bbox = outputs.get("bbox_sequence")
            raw_quality = {
                "track_confidence": outputs.get("track_confidence"),
                "lifecycle_status": outputs.get("lifecycle_status"),
            }
            payload_type = "cached_tracking_output_bundle"
            warnings.append("cached_output_from_inspection_not_real_run")
    elif mode == "adapter_stub":
        raw_track = {
            "track_id": "trk_stub_001",
            "bbox_sequence": [{"frame": 0, "bbox": [5, 10, 40, 70]}],
            "track_confidence": 0.5,
            "lifecycle_status": "tentative",
            "stub": True,
        }
        raw_bbox = raw_track.get("bbox_sequence")
        payload_type = "adapter_stub_design"
        warnings.append("adapter_stub_from_inspection_not_real_run")
    elif mode == "local_adapter":
        raw_track = {"track_id": "trk_local_adapter_001", "bbox_sequence": [], "track_confidence": 0.55}
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
        "raw_track_payload": raw_track,
        "raw_bbox_sequence_payload": raw_bbox,
        "raw_motion_payload": raw_motion,
        "raw_flow_payload": raw_flow,
        "raw_quality_payload": raw_quality,
        "parseability_status": parseability,
        "warning_codes": sorted(set(warnings)),
        "missing_information": missing,
        "source_refs": list(smoke_run.get("input_refs") or []) + [smoke_ref, io_ref, raw_id],
        "traceability_refs": list(smoke_run.get("input_refs") or []) + [raw_id, smoke_ref, io_ref],
        "candidate_only": True,
        "_blocked": False,
        "_inspect_subtype": inspect_subtype,
        "_stub_sample": ADAPTER_STUB_IO_SAMPLE if mode == "adapter_stub" else None,
    }
