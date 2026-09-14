# -*- coding: utf-8 -*-
"""Field Continuity Detection — signal scoring v1."""

from __future__ import annotations

from typing import Any, Dict, List

SIGNAL_SCORERS = (
    "score_location_continuity_signal",
    "score_camera_heading_signal",
    "score_key_entity_overlap_signal",
    "score_spatial_layout_similarity_signal",
    "score_visual_quality_change_signal",
    "score_occlusion_signal",
    "score_time_gap_signal",
    "score_session_recovery_signal",
)


def _result(signal_id: str, score: float, support: str, conf: float, reasons: List[str], missing: List[str] | None = None) -> Dict[str, Any]:
    return {
        "signal_id": signal_id,
        "signal_type": signal_id.replace("_signal", ""),
        "score": score,
        "support_status": support,
        "confidence": conf,
        "reason_codes": reasons,
        "missing_information": missing or [],
        "candidate_only": True,
    }


def score_location_continuity_signal(ctx: Dict[str, Any]) -> Dict[str, Any]:
    prev, curr = ctx.get("location_prev"), ctx.get("location_curr")
    if prev is None or curr is None:
        return _result("location_continuity_signal", 0.3, "supports_uncertain", 0.3, ["location_missing"], ["location_hint"])
    if prev == curr:
        return _result("location_continuity_signal", 0.9, "supports_same_field", 0.85, ["location_close"])
    return _result("location_continuity_signal", 0.1, "supports_new_field", 0.9, ["location_jump"])


def score_camera_heading_signal(ctx: Dict[str, Any]) -> Dict[str, Any]:
    delta = abs(float(ctx.get("heading_curr", 0)) - float(ctx.get("heading_prev", 0)))
    if delta < 5:
        return _result("camera_heading_signal", 0.85, "supports_same_field", 0.8, ["heading_small_change"])
    if delta < 45:
        return _result("camera_heading_signal", 0.7, "supports_field_shift", 0.75, ["heading_medium_change"])
    if delta <= 150:
        return _result("camera_heading_signal", 0.55, "supports_field_shift", 0.7, ["heading_large_change"])
    return _result("camera_heading_signal", 0.4, "supports_uncertain", 0.6, ["heading_very_large_change"])


def score_key_entity_overlap_signal(ctx: Dict[str, Any]) -> Dict[str, Any]:
    prev = set(ctx.get("entity_labels_prev") or [])
    curr = set(ctx.get("entity_labels_curr") or [])
    if not prev and not curr:
        return _result("key_entity_overlap_signal", 0.2, "supports_uncertain", 0.3, ["no_entities"], ["entity_labels"])
    if not prev or not curr:
        return _result("key_entity_overlap_signal", 0.15, "supports_occlusion", 0.5, ["entity_count_drop"])
    overlap = len(prev & curr) / max(len(prev | curr), 1)
    if overlap >= 0.8:
        return _result("key_entity_overlap_signal", 0.9, "supports_same_field", 0.85, ["high_key_entity_overlap"])
    if overlap >= 0.3:
        return _result("key_entity_overlap_signal", 0.55, "supports_field_shift", 0.65, ["partial_overlap"])
    if overlap == 0:
        return _result("key_entity_overlap_signal", 0.1, "supports_new_field", 0.9, ["all_key_entities_replaced"])
    return _result("key_entity_overlap_signal", 0.35, "supports_uncertain", 0.5, ["low_overlap"])


def score_spatial_layout_similarity_signal(ctx: Dict[str, Any]) -> Dict[str, Any]:
    prev, curr = ctx.get("layout_hash_prev"), ctx.get("layout_hash_curr")
    if prev and curr and prev == curr:
        return _result("spatial_layout_similarity_signal", 0.9, "supports_same_field", 0.85, ["layout_similar"])
    if prev and curr and prev != curr:
        return _result("spatial_layout_similarity_signal", 0.15, "supports_new_field", 0.85, ["layout_completely_different"])
    return _result("spatial_layout_similarity_signal", 0.4, "supports_uncertain", 0.4, ["layout_unknown"], ["layout_hash"])


def score_visual_quality_change_signal(ctx: Dict[str, Any]) -> Dict[str, Any]:
    bright = ctx.get("brightness_curr", "normal")
    blur = ctx.get("blur_hint_curr", "none")
    if bright in ("very_low", "dark") or ctx.get("sudden_dark"):
        return _result("visual_quality_change_signal", 0.85, "supports_occlusion", 0.8, ["sudden_dark"])
    if blur in ("strong", "severe") or ctx.get("strong_blur"):
        return _result("visual_quality_change_signal", 0.75, "supports_occlusion", 0.75, ["strong_motion_blur"])
    return _result("visual_quality_change_signal", 0.7, "supports_same_field", 0.6, ["visual_quality_ok"])


def score_occlusion_signal(ctx: Dict[str, Any]) -> Dict[str, Any]:
    prev_c = int(ctx.get("entity_count_prev", 0))
    curr_c = int(ctx.get("entity_count_curr", 0))
    drop = prev_c - curr_c
    if curr_c == 0 and prev_c > 0:
        duration = ctx.get("occlusion_duration", "brief")
        if duration == "long":
            return _result("occlusion_signal", 0.8, "supports_lost", 0.75, ["long_occlusion"])
        return _result("occlusion_signal", 0.85, "supports_occlusion", 0.8, ["brief_occlusion"])
    if ctx.get("entity_count_drop") and ctx.get("sudden_dark"):
        return _result("occlusion_signal", 0.85, "supports_occlusion", 0.8, ["brief_occlusion"])
    return _result("occlusion_signal", 0.6, "supports_same_field", 0.5, ["no_occlusion_detected"])


def score_time_gap_signal(ctx: Dict[str, Any]) -> Dict[str, Any]:
    gap = float(ctx.get("time_gap_s", 0))
    if gap <= 5:
        return _result("time_gap_signal", 0.85, "supports_same_field", 0.8, ["short_gap"])
    if gap <= 120:
        return _result("time_gap_signal", 0.45, "supports_uncertain", 0.6, ["medium_gap"])
    return _result("time_gap_signal", 0.2, "supports_lost", 0.7, ["long_gap"])


def score_session_recovery_signal(ctx: Dict[str, Any]) -> Dict[str, Any]:
    state = ctx.get("previous_session_state", "active")
    if state in ("lost", "occluded") and ctx.get("recovery_overlap") in ("high", True):
        return _result("session_recovery_signal", 0.9, "supports_recovery", 0.85, ["recoverable"])
    if state in ("lost", "occluded"):
        return _result("session_recovery_signal", 0.3, "supports_new_field", 0.6, ["not_recoverable"])
    return _result("session_recovery_signal", 0.5, "supports_same_field", 0.5, ["no_recovery_needed"])


def score_all_signals(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        score_location_continuity_signal(ctx),
        score_camera_heading_signal(ctx),
        score_key_entity_overlap_signal(ctx),
        score_spatial_layout_similarity_signal(ctx),
        score_visual_quality_change_signal(ctx),
        score_occlusion_signal(ctx),
        score_time_gap_signal(ctx),
        score_session_recovery_signal(ctx),
    ]
