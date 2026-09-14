# -*- coding: utf-8 -*-
"""Depth fallback policy v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.depth_observation_candidate_ingestion_types_v1 import (
    DEPTH_BUCKETS,
    FIELD_ZONE_HINTS,
)


def depth_bucket_from_value(
    value: float | None,
    depth_range: Tuple[float, float] | None = None,
) -> str:
    if value is None:
        return "unknown"
    lo, hi = depth_range or (0.0, 10.0)
    span = hi - lo if hi > lo else 1.0
    norm = (float(value) - lo) / span
    if norm < 0.33:
        return "near"
    if norm < 0.66:
        return "middle"
    return "far"


def field_zone_from_bucket(bucket: str) -> str:
    return {
        "near": "inner_zone",
        "middle": "working_zone",
        "far": "forecast_zone",
        "unknown": "unknown",
    }.get(bucket, "unknown")


def apply_depth_missing_fallback(
    *,
    object_observation_ref: str,
    label: str,
    bbox: Dict[str, Any],
    frame_ref: str,
    timestamp: str,
    depth_observation_ref: str,
) -> Dict[str, Any]:
    return {
        "object_depth_hint": None,
        "sampled_depth_value": None,
        "depth_bucket": "unknown",
        "field_zone_hint": "unknown",
        "depth_source": "unknown",
        "depth_confidence": "unknown",
        "depth_error_expected": True,
        "depth_reliability_reasons": ["depth_map_missing"],
        "missing_information": ["depth_map_ref_missing", "object_depth_hint_unknown"],
        "warning_codes": ["depth_missing_fallback_applied"],
        "bbox_sampling_policy": "center_median_sample",
        "object_observation_ref": object_observation_ref,
        "depth_observation_ref": depth_observation_ref,
        "frame_ref": frame_ref,
        "timestamp": timestamp,
        "label": label,
        "bbox": dict(bbox),
        "candidate_only": True,
    }


def apply_depth_unreliable_fallback(
    *,
    object_observation_ref: str,
    label: str,
    bbox: Dict[str, Any],
    frame_ref: str,
    timestamp: str,
    depth_observation_ref: str,
    sampled_depth_value: float | None,
    reason: str = "low_global_depth_confidence",
) -> Dict[str, Any]:
    bucket = depth_bucket_from_value(sampled_depth_value) if sampled_depth_value is not None else "unknown"
    zone = field_zone_from_bucket(bucket)
    return {
        "object_depth_hint": sampled_depth_value,
        "sampled_depth_value": sampled_depth_value,
        "depth_bucket": bucket,
        "field_zone_hint": zone,
        "depth_source": "estimated",
        "depth_confidence": "low",
        "depth_error_expected": True,
        "depth_reliability_reasons": [reason],
        "missing_information": ["depth_unreliable"],
        "warning_codes": ["depth_unreliable_confidence_downgraded"],
        "bbox_sampling_policy": "center_median_sample",
        "object_observation_ref": object_observation_ref,
        "depth_observation_ref": depth_observation_ref,
        "frame_ref": frame_ref,
        "timestamp": timestamp,
        "label": label,
        "bbox": dict(bbox),
        "candidate_only": True,
    }


def apply_depth_estimated_hint(
    *,
    object_observation_ref: str,
    label: str,
    bbox: Dict[str, Any],
    frame_ref: str,
    timestamp: str,
    depth_observation_ref: str,
    sampled_depth_value: float,
    depth_range: Tuple[float, float] | None = None,
    depth_confidence: str = "medium",
) -> Dict[str, Any]:
    bucket = depth_bucket_from_value(sampled_depth_value, depth_range)
    zone = field_zone_from_bucket(bucket)
    conf = "medium" if depth_confidence in ("high", "medium") else depth_confidence
    return {
        "object_depth_hint": sampled_depth_value,
        "sampled_depth_value": sampled_depth_value,
        "depth_bucket": bucket,
        "field_zone_hint": zone,
        "depth_source": "estimated",
        "depth_confidence": conf,
        "depth_error_expected": True,
        "depth_reliability_reasons": [],
        "missing_information": [],
        "warning_codes": [],
        "bbox_sampling_policy": "center_median_sample",
        "object_observation_ref": object_observation_ref,
        "depth_observation_ref": depth_observation_ref,
        "frame_ref": frame_ref,
        "timestamp": timestamp,
        "label": label,
        "bbox": dict(bbox),
        "candidate_only": True,
    }
