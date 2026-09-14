# -*- coding: utf-8 -*-
"""Tracking / Optical Flow IO inspector v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List


def inspect_tracking_opticalflow_model_io(*, smoke_run: Dict[str, Any]) -> Dict[str, Any]:
    """Inspect observed input/output formats from smoke run."""
    raw = smoke_run.get("_raw_output") or {}
    frame = smoke_run.get("_frame_input") or {}
    obs = smoke_run.get("_object_observation") or {}
    mode = smoke_run.get("execution_mode", "blocked_by_authorization")
    subtype = smoke_run.get("_inspect_subtype", "tracking")
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
        if subtype == "optical_flow":
            schema_summary = {
                "motion_vector": bool(outputs.get("motion_vector")),
                "flow_map_summary": bool(outputs.get("flow_map_summary")),
            }
        else:
            schema_summary = {
                "track_id": bool(outputs.get("track_id")),
                "bbox_sequence": bool(outputs.get("bbox_sequence")),
                "track_confidence": bool(outputs.get("track_confidence")),
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
        output_format = {"type": "raw_track_dict", "keys": sorted(raw.keys())}
        payload_type = "minimal_smoke_output"
        schema_summary = {"track_id": "track_id" in raw}
        parseability = "parseable" if "track_id" in raw else "partial"
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
