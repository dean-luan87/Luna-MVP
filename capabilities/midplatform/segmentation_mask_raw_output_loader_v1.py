# -*- coding: utf-8 -*-
"""Segmentation / Mask raw output loader v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.segmentation_mask_model_smoke_io_inspection_items_v1 import (
    ADAPTER_STUB_IO_SAMPLE,
    CACHED_FREESPACE_OUTPUT_SAMPLE,
    CACHED_GROUNDED_SAM_OUTPUT_SAMPLE,
    CACHED_SAM_OUTPUT_SAMPLE,
)


def load_segmentation_mask_raw_output_candidate(
    *,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    frame_refs: Optional[List[str]] = None,
    inspect_subtype: str = "grounded_sam",
) -> Dict[str, Any]:
    """Load raw output from inspection-confirmed smoke run. No real segmentation execution."""
    mode = smoke_run.get("execution_mode", "blocked_by_authorization")
    smoke_ref = smoke_run.get("smoke_run_id")
    io_ref = io_inspection.get("io_inspection_id")
    warnings: List[str] = list(smoke_run.get("warning_codes") or [])
    missing: List[str] = list(io_inspection.get("missing_information") or [])
    raw_id = (
        smoke_run.get("output_refs", [f"raw_{uuid.uuid4().hex[:12]}"])[0]
        if smoke_run.get("output_refs") else f"raw_{uuid.uuid4().hex[:12]}"
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
            "raw_mask_payload": None,
            "raw_polygon_payload": None,
            "raw_boundary_payload": None,
            "raw_freespace_payload": None,
            "raw_region_label_payload": None,
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

    raw_mask = None
    raw_polygon = None
    raw_boundary = None
    raw_freespace = None
    raw_region = None
    raw_quality = None
    payload_type = io_inspection.get("output_payload_type", "unknown")

    if mode == "local_real_model":
        raw_mask = {"mask_ref": "mask_local_fixture", "bbox": [80, 60, 320, 280], "confidence": 0.75}
        payload_type = "minimal_smoke_output"
        warnings.append("local_real_model_from_inspection_fixture_not_production_segmentation")
    elif mode == "cached_output":
        if inspect_subtype == "sam":
            sample = CACHED_SAM_OUTPUT_SAMPLE
        elif inspect_subtype == "freespace":
            sample = CACHED_FREESPACE_OUTPUT_SAMPLE
        else:
            sample = CACHED_GROUNDED_SAM_OUTPUT_SAMPLE
        outputs = sample.get("outputs") or {}
        if inspect_subtype == "freespace":
            raw_freespace = outputs
            raw_region = {"region_label": outputs.get("region_label"), "region_type": outputs.get("region_type")}
            raw_quality = {"confidence": outputs.get("confidence")}
        else:
            raw_mask = outputs
            raw_polygon = {"polygon": outputs.get("polygon"), "bbox": outputs.get("bbox")}
            raw_boundary = {"bbox": outputs.get("bbox"), "polygon": outputs.get("polygon")}
            raw_quality = {"confidence": outputs.get("confidence") or outputs.get("mask_quality")}
        payload_type = f"cached_{inspect_subtype}_output_bundle"
        warnings.append("cached_output_from_inspection_not_real_run")
    elif mode == "adapter_stub":
        raw_mask = {"mask_ref": "stub_mask", "bbox": [10, 10, 50, 50], "confidence": 0.5, "stub": True}
        payload_type = "adapter_stub_design"
        warnings.append("adapter_stub_from_inspection_not_real_run")

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
        "raw_mask_payload": raw_mask,
        "raw_polygon_payload": raw_polygon,
        "raw_boundary_payload": raw_boundary,
        "raw_freespace_payload": raw_freespace,
        "raw_region_label_payload": raw_region,
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
