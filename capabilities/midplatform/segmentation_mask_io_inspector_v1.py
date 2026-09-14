# -*- coding: utf-8 -*-
"""Segmentation / Mask Model IO inspector v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List


def inspect_segmentation_mask_model_io(*, smoke_run: Dict[str, Any]) -> Dict[str, Any]:
    """Inspect observed input/output formats from smoke run."""
    raw = smoke_run.get("_raw_output") or {}
    frame = smoke_run.get("_frame_input") or {}
    obs = smoke_run.get("_object_observation") or {}
    mode = smoke_run.get("execution_mode", "blocked_by_authorization")
    subtype = smoke_run.get("_inspect_subtype", "segmentation")
    warnings: List[str] = list(smoke_run.get("warning_codes") or [])
    missing: List[str] = []

    input_format = {
        "type": "RealFrameInputPackage+ObjectObservationCandidate",
        "fields_observed": sorted(set(list(frame.keys()) + list(obs.keys()))),
        "fixture_type": frame.get("fixture_type"),
    }

    if mode == "cached_output":
        outputs = raw.get("outputs") or {}
        output_format = {"type": f"cached_{subtype}_output_bundle", "keys": sorted(outputs.keys())}
        payload_type = "structured_dict"
        if subtype == "freespace":
            schema_summary = {
                "passable_area": bool(outputs.get("passable_area")),
                "region_label": bool(outputs.get("region_label")),
                "free_space_mask": bool(outputs.get("free_space_mask")),
            }
        elif subtype == "sam":
            schema_summary = {
                "mask": bool(outputs.get("mask")),
                "bbox": bool(outputs.get("bbox")),
                "polygon": bool(outputs.get("polygon")),
                "mask_quality": bool(outputs.get("mask_quality") or outputs.get("confidence")),
            }
        else:
            schema_summary = {
                "mask_ref": bool(outputs.get("mask_ref") or outputs.get("mask")),
                "polygon": bool(outputs.get("polygon")),
                "confidence": bool(outputs.get("confidence")),
                "bbox": bool(outputs.get("bbox")),
            }
        parseability = "parseable" if any(schema_summary.values()) else "partial"
        sample_refs = [raw.get("sample_id", "cached_sample")]
    elif mode == "adapter_stub":
        output_format = {"type": raw.get("output_format", "adapter_stub_candidate_dicts")}
        payload_type = "adapter_stub_design"
        schema_summary = {"input_format": raw.get("input_format"), "output_format": raw.get("output_format")}
        parseability = "design_parseable"
        sample_refs = [raw.get("sample_id", "stub_sample")]
    elif mode == "local_real_model":
        output_format = {"type": "raw_segmentation_dict", "keys": sorted(raw.keys())}
        payload_type = "minimal_smoke_output"
        schema_summary = {
            "mask": "mask" in raw,
            "bbox": "bbox" in raw,
            "confidence": "confidence" in raw,
        }
        parseability = "parseable" if "mask" in raw else "partial"
        sample_refs = [raw.get("raw_output_id", "raw_smoke")]
    elif mode.startswith("blocked"):
        output_format = {"type": "none", "reason": mode}
        payload_type = "blocked"
        schema_summary = {}
        parseability = "not_applicable"
        sample_refs = []
        missing.append(f"output_unavailable_due_to_{mode}")
    else:
        output_format = {"type": "unknown"}
        payload_type = "failed"
        schema_summary = {}
        parseability = "unparseable"
        sample_refs = []
        missing.append("runtime_failed")

    mapping_feasibility = "feasible" if parseability in ("parseable", "design_parseable", "partial") else "blocked"

    return {
        "io_inspection_id": f"ioi_{uuid.uuid4().hex[:12]}",
        "smoke_run_ref": smoke_run.get("smoke_run_id"),
        "input_format_observed": input_format,
        "output_format_observed": output_format,
        "output_payload_type": payload_type,
        "output_schema_summary": schema_summary,
        "output_sample_refs": sample_refs,
        "parseability_status": parseability,
        "candidate_mapping_feasibility": mapping_feasibility,
        "missing_information": missing,
        "warning_codes": warnings,
        "candidate_only": True,
        "_execution_mode": mode,
        "_inspect_subtype": subtype,
    }
