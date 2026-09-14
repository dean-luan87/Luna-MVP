# -*- coding: utf-8 -*-
"""OCR / Text raw output loader v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.ocr_text_model_smoke_io_inspection_items_v1 import (
    ADAPTER_STUB_IO_SAMPLE,
    CACHED_PADDLEOCR_OUTPUT_SAMPLE,
    CACHED_RAPIDOCR_OUTPUT_SAMPLE,
    CACHED_TEXT_NORMALIZATION_SAMPLE,
    CACHED_TEXT_REGION_OUTPUT_SAMPLE,
)


def load_ocr_text_raw_output_candidate(
    *,
    smoke_run: Dict[str, Any],
    io_inspection: Dict[str, Any],
    frame_refs: Optional[List[str]] = None,
    inspect_subtype: str = "rapidocr",
) -> Dict[str, Any]:
    """Load raw output from inspection-confirmed smoke run. No real OCR execution."""
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
            "raw_text_payload": None,
            "raw_region_payload": None,
            "raw_layout_payload": None,
            "raw_normalization_payload": None,
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

    raw_text = None
    raw_region = None
    raw_layout = None
    raw_norm = None
    raw_quality = None
    payload_type = io_inspection.get("output_payload_type", "unknown")

    if mode == "local_real_model":
        raw_text = {"text": "测试文字", "bbox": [100, 50, 200, 90], "confidence": 0.7}
        payload_type = "minimal_smoke_output"
        warnings.append("local_real_model_from_inspection_fixture_not_production_ocr")
    elif mode == "cached_output":
        if inspect_subtype == "paddleocr":
            sample = CACHED_PADDLEOCR_OUTPUT_SAMPLE
        elif inspect_subtype == "text_region":
            sample = CACHED_TEXT_REGION_OUTPUT_SAMPLE
        elif inspect_subtype == "text_enhancement":
            sample = CACHED_TEXT_NORMALIZATION_SAMPLE
        else:
            sample = CACHED_RAPIDOCR_OUTPUT_SAMPLE
        outputs = sample.get("outputs") or {}
        if inspect_subtype == "text_region":
            raw_region = outputs
            raw_layout = outputs.get("layout_block")
        elif inspect_subtype == "text_enhancement":
            raw_norm = outputs
            raw_text = {"text": outputs.get("raw_text"), "normalized_text": outputs.get("normalized_text")}
        else:
            raw_text = outputs
            raw_quality = {"confidence": outputs.get("confidence")}
        payload_type = f"cached_{inspect_subtype}_output_bundle"
        warnings.append("cached_output_from_inspection_not_real_run")
    elif mode == "adapter_stub":
        raw_text = {"text": "stub_text", "bbox": [5, 10, 40, 70], "confidence": 0.5, "stub": True}
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
        "raw_text_payload": raw_text,
        "raw_region_payload": raw_region,
        "raw_layout_payload": raw_layout,
        "raw_normalization_payload": raw_norm,
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
