# -*- coding: utf-8 -*-
"""Tracking / Optical Flow output normalizer v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple


def normalize_tracking_opticalflow_output_to_candidates(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[str], List[str]]:
    """Normalize inspection-confirmed raw output into ObjectTrackCandidate and TrackingQualityCandidate."""
    warnings: List[str] = list(raw_output.get("warning_codes") or [])
    failure_points: List[str] = []
    overrides = case_overrides or {}
    frames = adapter_input.get("_frame_packages") or []
    observations = adapter_input.get("_object_observations") or []
    session_ref = adapter_input.get("session_ref", "session_unknown")
    execution_mode = adapter_input.get("execution_mode", "adapter_stub")
    raw_ref = raw_output.get("raw_output_id")

    if raw_output.get("_blocked") or execution_mode.startswith("blocked"):
        failure_points.append(execution_mode)
        warnings.append("blocked_no_candidate_fabrication")
        return [], [], warnings, failure_points

    tracks: List[Dict[str, Any]] = []
    qualities: List[Dict[str, Any]] = []

    raw_track = raw_output.get("raw_track_payload")
    raw_bbox = raw_output.get("raw_bbox_sequence_payload") or (raw_track or {}).get("bbox_sequence")
    lifecycle = overrides.get("lifecycle_status", (raw_track or {}).get("lifecycle_status", "active"))
    identity_switch_risk = overrides.get("identity_switch_risk", "low")
    occlusion_risk = overrides.get("occlusion_risk", "low")

    if raw_track and not overrides.get("no_track"):
        track_conf = overrides.get("track_confidence", (raw_track or {}).get("track_confidence", 0.5))
        if isinstance(track_conf, (int, float)):
            conf_label = "high" if track_conf >= 0.85 else ("medium" if track_conf >= 0.6 else "low")
        else:
            conf_label = str(track_conf)
        if execution_mode in ("cached_output", "adapter_stub") and conf_label == "high":
            conf_label = "medium"
            warnings.append(f"{execution_mode}_caps_track_confidence")

        mode_warnings: List[str] = []
        if execution_mode == "cached_output":
            mode_warnings.append("from_cached_output_not_real_run")
        if execution_mode == "adapter_stub":
            mode_warnings.append("from_adapter_stub_not_real_run")

        track_id = f"otc_{uuid.uuid4().hex[:12]}"
        obs_refs = [o.get("object_observation_id") or o.get("observation_id") for o in observations if o]
        tracks.append({
            "object_track_candidate_id": track_id,
            "source_raw_output_ref": raw_ref,
            "track_id": (raw_track or {}).get("track_id", f"trk_{uuid.uuid4().hex[:8]}"),
            "source_object_observation_refs": [r for r in obs_refs if r],
            "frame_refs": [f.get("frame_ref") for f in frames],
            "timestamp_range": raw_output.get("timestamp_range") or {},
            "bbox_sequence": raw_bbox or [],
            "label_hint": overrides.get("label_hint", observations[0].get("label") if observations else None),
            "track_confidence": conf_label,
            "lifecycle_status": lifecycle,
            "lost_frame_count": overrides.get("lost_frame_count", 0 if lifecycle != "lost" else 3),
            "warning_codes": mode_warnings,
            "missing_information": list(raw_output.get("missing_information") or []),
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref] + obs_refs,
            "evidence_refs": [adapter_input.get("model_ref"), adapter_input.get("smoke_run_ref")],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [track_id, raw_ref],
            "candidate_only": True,
            "_identity_switch_risk": identity_switch_risk,
        })

        quality_status = overrides.get("quality_status", "usable")
        if lifecycle == "lost":
            quality_status = "degraded"
        if identity_switch_risk in ("high", "severe"):
            quality_status = "degraded"
        if execution_mode in ("cached_output", "adapter_stub"):
            quality_status = "usable" if quality_status == "strong" else quality_status

        qualities.append({
            "tracking_quality_candidate_id": f"tqc_{uuid.uuid4().hex[:12]}",
            "source_raw_output_ref": raw_ref,
            "track_quality": conf_label,
            "flow_quality": overrides.get("flow_quality", "unknown"),
            "continuity_quality": "degraded" if lifecycle == "lost" else "usable",
            "frame_alignment_quality": overrides.get("frame_alignment_quality", "usable"),
            "identity_switch_risk": identity_switch_risk,
            "occlusion_risk": occlusion_risk,
            "quality_status": quality_status,
            "blockers": [],
            "warnings": mode_warnings,
            "source_refs": [adapter_input.get("adapter_input_id"), raw_ref],
            "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [raw_ref],
            "candidate_only": True,
        })

    if execution_mode in ("cached_output", "adapter_stub", "local_real_model"):
        warnings.append(f"normalized_from_{execution_mode}_inspection_result")

    return tracks, qualities, warnings, failure_points
