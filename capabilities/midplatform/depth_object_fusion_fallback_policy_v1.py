# -*- coding: utf-8 -*-
"""Depth-Object fusion fallback policy v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.bbox_depth_sampling_policy_v1 import depth_bucket_and_zone
from capabilities.midplatform.depth_object_fusion_types_v1 import REJECTED_ALIGNMENT_STATUSES


def apply_depth_object_fusion_fallback(
    *,
    aligned: Dict[str, Any],
    obj: Dict[str, Any],
    depth: Optional[Dict[str, Any]],
    sampled: float | None,
    sample_status: str,
    sample_warnings: List[str],
    sample_missing: List[str],
) -> Tuple[Dict[str, Any], bool]:
    """Return partial hint fields and whether fusion was rejected."""
    status = aligned.get("alignment_status", "")
    if status in REJECTED_ALIGNMENT_STATUSES or aligned.get("alignment_strength") == "rejected":
        return {"reject_reason": "alignment_rejected", "alignment_status": status}, False

    unit = (depth or {}).get("depth_value_unit", "unknown")
    depth_conf = (depth or {}).get("depth_confidence", "unknown")
    depth_source = (depth or {}).get("depth_source", "unknown")
    align_conf = aligned.get("alignment_confidence", "unknown")

    warnings = list(sample_warnings) + list(aligned.get("warning_codes") or [])
    missing = list(sample_missing)
    reasons: List[str] = []
    conflicts = list(aligned.get("conflict_refs") or [])

    if sampled is None or sample_status in ("depth_map_missing", "depth_sample_failed"):
        bucket, zone, bw = depth_bucket_and_zone(None, unit)
        warnings.extend(bw)
        fusion_conf = "low"
        return {
            "sampled_depth_value": None,
            "object_depth_hint": None,
            "depth_value_unit": unit,
            "depth_bucket": bucket,
            "field_zone_hint": zone,
            "depth_source": "unknown",
            "depth_confidence": "unknown",
            "depth_error_expected": True,
            "depth_reliability_reasons": ["depth_missing"],
            "alignment_confidence": align_conf,
            "fusion_confidence": fusion_conf,
            "missing_information": missing + ["depth_map_missing"],
            "warning_codes": warnings,
            "conflict_refs": conflicts,
        }, True

    bucket, zone, bw = depth_bucket_and_zone(sampled, unit)
    warnings.extend(bw)
    if unit == "relative":
        reasons.append("relative_depth_not_metric")
        fusion_conf = "low"
    elif depth_conf in ("low", "unknown"):
        reasons.append("low_depth_confidence")
        fusion_conf = "low"
    elif status == "aligned_degraded" or status == "aligned_weak":
        reasons.append("alignment_degraded")
        fusion_conf = "low"
    else:
        fusion_conf = "medium" if depth_conf == "medium" else "low"

    if depth_source == "estimated":
        reasons.append("estimated_depth_not_hardware")

    return {
        "sampled_depth_value": sampled,
        "object_depth_hint": sampled,
        "depth_value_unit": unit,
        "depth_bucket": bucket,
        "field_zone_hint": zone,
        "depth_source": "estimated" if depth_source != "unknown" else "unknown",
        "depth_confidence": depth_conf if depth_conf != "high" else "medium",
        "depth_error_expected": True,
        "depth_reliability_reasons": reasons,
        "alignment_confidence": align_conf,
        "fusion_confidence": fusion_conf,
        "missing_information": missing,
        "warning_codes": warnings,
        "conflict_refs": conflicts,
    }, True
