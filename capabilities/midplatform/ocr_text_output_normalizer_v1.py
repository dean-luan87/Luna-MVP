# -*- coding: utf-8 -*-
"""OCR / Text output normalizer v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple


def _conf_label(val: Any, execution_mode: str) -> str:
    if isinstance(val, (int, float)):
        label = "high" if val >= 0.85 else ("medium" if val >= 0.6 else "low")
    else:
        label = str(val)
    if execution_mode in ("cached_output", "adapter_stub") and label == "high":
        return "medium"
    return label


def normalize_ocr_text_output_to_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[str], List[str]]:
    """Normalize inspection-confirmed raw output into text candidates."""
    warnings: List[str] = list(raw_output.get("warning_codes") or [])
    failure_points: List[str] = []
    overrides = case_overrides or {}
    frames = adapter_input.get("_frame_packages") or [{}]
    frame = frames[0]
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    raw_ref = raw_output.get("raw_output_id")
    subtype = raw_output.get("_inspect_subtype", "rapidocr")

    if raw_output.get("_blocked") or execution_mode.startswith("blocked"):
        failure_points.append(execution_mode)
        warnings.append("blocked_no_candidate_fabrication")
        return [], [], [], warnings, failure_points

    observations: List[Dict[str, Any]] = []
    regions: List[Dict[str, Any]] = []
    qualities: List[Dict[str, Any]] = []

    mode_warnings: List[str] = []
    if execution_mode == "cached_output":
        mode_warnings.append("from_cached_output_not_real_run")
    if execution_mode == "adapter_stub":
        mode_warnings.append("from_adapter_stub_not_real_run")

    raw_text = raw_output.get("raw_text_payload")
    raw_region = raw_output.get("raw_region_payload")
    raw_quality = raw_output.get("raw_quality_payload") or {}

    if raw_text and subtype != "text_region" and not overrides.get("no_observation"):
        conf_val = overrides.get("confidence", raw_text.get("confidence", 0.5))
        conf_label = _conf_label(conf_val, execution_mode)
        if overrides.get("low_confidence"):
            conf_label = "low"
            warnings.append("low_confidence_text_degraded")
        obs_id = f"toc_{uuid.uuid4().hex[:12]}"
        text_type = overrides.get("text_type_hint", "storefront" if subtype == "rapidocr" else "floor_indicator")
        observations.append({
            "text_observation_candidate_id": obs_id,
            "source_raw_output_ref": raw_ref,
            "frame_ref": frame.get("frame_ref"),
            "timestamp": frame.get("timestamp"),
            "text": raw_text.get("text", ""),
            "normalized_text": raw_text.get("normalized_text"),
            "language_hint": overrides.get("language_hint", "zh"),
            "confidence": conf_label,
            "source_region_ref": None,
            "reading_order_index": raw_text.get("reading_order", 0),
            "text_type_hint": text_type,
            "warning_codes": mode_warnings,
            "missing_information": list(raw_output.get("missing_information") or []),
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "evidence_refs": [adapter_input.get("model_ref"), adapter_input.get("smoke_run_ref")],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [obs_id, raw_ref],
            "candidate_only": True,
        })

    if raw_region or subtype == "text_region":
        region_data = raw_region or {}
        reg_id = f"trc_{uuid.uuid4().hex[:12]}"
        geom_refs = [g.get("field_geometry_candidate_id") for g in adapter_input.get("_geometry_packages") or [] if g]
        obs_refs = [o.get("object_observation_id") for o in adapter_input.get("_object_observations") or [] if o]
        regions.append({
            "text_region_candidate_id": reg_id,
            "source_raw_output_ref": raw_ref,
            "frame_ref": frame.get("frame_ref"),
            "bbox": region_data.get("bbox") or (raw_text or {}).get("bbox"),
            "polygon": region_data.get("polygon") or (raw_text or {}).get("polygon"),
            "region_type": overrides.get("region_type", region_data.get("region_type", "sign_region")),
            "region_confidence": _conf_label(region_data.get("confidence", 0.7), execution_mode),
            "associated_object_observation_refs": obs_refs,
            "associated_geometry_refs": geom_refs,
            "reading_order_index": (region_data.get("layout_block") or {}).get("reading_order"),
            "warning_codes": mode_warnings,
            "missing_information": [],
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "evidence_refs": [adapter_input.get("model_ref")],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [reg_id],
            "candidate_only": True,
        })
        if observations:
            observations[0]["source_region_ref"] = reg_id

    if raw_quality or observations:
        q_conf = raw_quality.get("confidence") or (raw_text or {}).get("confidence", 0.5)
        q_status = overrides.get("quality_status", "usable")
        if overrides.get("low_confidence") or _conf_label(q_conf, execution_mode) == "low":
            q_status = "degraded"
        qualities.append({
            "text_quality_candidate_id": f"tqc_{uuid.uuid4().hex[:12]}",
            "source_raw_output_ref": raw_ref,
            "recognition_quality": _conf_label(q_conf, execution_mode),
            "region_quality": overrides.get("region_quality", "usable"),
            "layout_quality": overrides.get("layout_quality", "usable"),
            "normalization_quality": overrides.get("normalization_quality", "unknown"),
            "blur_risk": overrides.get("blur_risk", "low"),
            "occlusion_risk": overrides.get("occlusion_risk", "low"),
            "orientation_risk": overrides.get("orientation_risk", "low"),
            "quality_status": q_status,
            "blockers": [],
            "warnings": mode_warnings,
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [raw_ref],
            "candidate_only": True,
        })

    if execution_mode in ("cached_output", "adapter_stub", "local_real_model"):
        warnings.append(f"normalized_from_{execution_mode}_inspection_result")

    return observations, regions, qualities, warnings, failure_points
