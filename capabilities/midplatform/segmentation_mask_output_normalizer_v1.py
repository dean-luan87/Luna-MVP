# -*- coding: utf-8 -*-
"""Segmentation / Mask output normalizer v1."""

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


def normalize_segmentation_mask_output_to_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[str], List[str]]:
    """Normalize inspection-confirmed raw output into segmentation candidates."""
    warnings: List[str] = list(raw_output.get("warning_codes") or [])
    failure_points: List[str] = []
    overrides = case_overrides or {}
    frames = adapter_input.get("_frame_packages") or [{}]
    frame = frames[0]
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    raw_ref = raw_output.get("raw_output_id")
    subtype = raw_output.get("_inspect_subtype", "grounded_sam")

    if raw_output.get("_blocked") or execution_mode.startswith("blocked"):
        failure_points.append(execution_mode)
        warnings.append("blocked_no_candidate_fabrication")
        return [], [], [], warnings, failure_points

    masks: List[Dict[str, Any]] = []
    regions: List[Dict[str, Any]] = []
    qualities: List[Dict[str, Any]] = []

    mode_warnings: List[str] = []
    if execution_mode == "cached_output":
        mode_warnings.append("from_cached_output_not_real_run")
    if execution_mode == "adapter_stub":
        mode_warnings.append("from_adapter_stub_not_real_run")

    raw_mask = raw_output.get("raw_mask_payload")
    raw_region = raw_output.get("raw_region_label_payload")
    raw_quality = raw_output.get("raw_quality_payload") or {}
    obs_refs = [o.get("object_observation_id") for o in adapter_input.get("_object_observations") or [] if o]
    text_refs = [t.get("text_region_candidate_id") for t in adapter_input.get("_text_regions") or [] if t]

    if raw_mask and subtype != "freespace" and not overrides.get("no_mask"):
        conf_val = overrides.get("confidence", raw_mask.get("confidence", 0.5))
        conf_label = _conf_label(conf_val, execution_mode)
        if overrides.get("low_confidence"):
            conf_label = "low"
            warnings.append("low_confidence_mask_degraded")
        enc = "polygon" if raw_mask.get("polygon") else ("bbox_linked_mask" if raw_mask.get("bbox") else "binary_mask_ref")
        mask_id = f"moc_{uuid.uuid4().hex[:12]}"
        masks.append({
            "mask_observation_candidate_id": mask_id,
            "source_raw_output_ref": raw_ref,
            "frame_ref": frame.get("frame_ref"),
            "timestamp": frame.get("timestamp"),
            "mask_ref": raw_mask.get("mask_ref") or raw_mask.get("mask"),
            "mask_encoding_type": enc,
            "associated_object_observation_refs": obs_refs,
            "associated_text_region_refs": text_refs,
            "label_hint": raw_mask.get("label", overrides.get("label_hint")),
            "mask_confidence": conf_label,
            "mask_area_summary": overrides.get("mask_area_summary", "medium"),
            "warning_codes": mode_warnings,
            "missing_information": list(raw_output.get("missing_information") or []),
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "evidence_refs": [adapter_input.get("model_ref"), adapter_input.get("smoke_run_ref")],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [mask_id, raw_ref],
            "candidate_only": True,
        })

    if raw_region or subtype == "freespace":
        region_data = raw_region or raw_output.get("raw_freespace_payload") or {}
        reg_id = f"roc_{uuid.uuid4().hex[:12]}"
        geom_refs = [g.get("field_geometry_candidate_id") for g in adapter_input.get("_geometry_packages") or [] if g]
        regions.append({
            "region_observation_candidate_id": reg_id,
            "source_raw_output_ref": raw_ref,
            "frame_ref": frame.get("frame_ref"),
            "region_label": overrides.get("region_label", region_data.get("region_type", region_data.get("region_label", "unknown"))),
            "region_ref": region_data.get("free_space_mask"),
            "bbox": (raw_mask or {}).get("bbox"),
            "polygon": region_data.get("passable_area") or (raw_mask or {}).get("polygon"),
            "associated_geometry_refs": geom_refs,
            "region_confidence": _conf_label(region_data.get("confidence", 0.7), execution_mode),
            "region_quality": overrides.get("region_quality", "usable"),
            "warning_codes": mode_warnings,
            "missing_information": [],
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "evidence_refs": [adapter_input.get("model_ref")],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [reg_id],
            "candidate_only": True,
        })

    if raw_quality or masks or regions:
        q_conf = raw_quality.get("confidence") or (raw_mask or {}).get("confidence", 0.5)
        q_status = overrides.get("quality_status", "usable")
        prompt_risk = overrides.get("prompt_dependency_risk", "low")
        if overrides.get("low_confidence") or _conf_label(q_conf, execution_mode) == "low":
            q_status = "degraded"
        if overrides.get("prompt_dependency_high"):
            prompt_risk = "high"
            q_status = "degraded"
            warnings.append("prompt_dependency_degrades_quality")
        qualities.append({
            "mask_quality_candidate_id": f"mqc_{uuid.uuid4().hex[:12]}",
            "source_raw_output_ref": raw_ref,
            "mask_quality": _conf_label(q_conf, execution_mode),
            "boundary_quality": overrides.get("boundary_quality", "usable"),
            "freespace_quality": overrides.get("freespace_quality", "usable" if subtype == "freespace" else "unknown"),
            "region_label_quality": overrides.get("region_label_quality", "usable" if subtype == "freespace" else "unknown"),
            "occlusion_risk": overrides.get("occlusion_risk", "low"),
            "blur_risk": overrides.get("blur_risk", "low"),
            "prompt_dependency_risk": prompt_risk,
            "quality_status": q_status,
            "blockers": [],
            "warnings": mode_warnings,
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [raw_ref],
            "candidate_only": True,
        })

    if execution_mode in ("cached_output", "adapter_stub", "local_real_model"):
        warnings.append(f"normalized_from_{execution_mode}_inspection_result")

    return masks, regions, qualities, warnings, failure_points
