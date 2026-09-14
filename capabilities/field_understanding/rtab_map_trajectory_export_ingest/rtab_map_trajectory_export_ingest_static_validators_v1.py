# -*- coding: utf-8 -*-
"""RTAB-Map Trajectory Export Ingest — static validators + convert v1."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.rtab_map_trajectory_export_ingest.rtab_map_trajectory_export_ingest_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    INPUT_EXPORT_KIND,
    INPUT_FORMAT_REF,
    INTERNAL_STANDARD_FORMAT,
    INGEST_REF,
    TARGET_FORMAT_REF,
    TRAJECTORY_RECORD_REQUIRED_FIELDS,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_trajectory_record_required_fields",
    "rule_02_source_chain_required",
    "rule_03_node_id_required",
    "rule_04_quaternion_normalizable",
    "rule_05_pose_json_trace_mapping",
    "rule_06_motion_json_trace_mapping",
    "rule_07_missing_source_chain_rejected",
    "rule_08_bad_quaternion_rejected",
    "rule_09_missing_node_id_rejected",
    "rule_10_direct_candidate_bundle_bypass_rejected",
)


def _quaternion_norm(qx: float, qy: float, qz: float, qw: float) -> float:
    return math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)


def validate_trajectory_record(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{field}" for field in TRAJECTORY_RECORD_REQUIRED_FIELDS if field not in record]

    if not record.get("source_chain"):
        issues.append("source_chain_required")
    if not record.get("node_id"):
        issues.append("node_id_required")

    try:
        qx = float(record["qx"])
        qy = float(record["qy"])
        qz = float(record["qz"])
        qw = float(record["qw"])
    except (KeyError, TypeError, ValueError):
        return False, issues + ["quaternion_fields_invalid"]

    norm = _quaternion_norm(qx, qy, qz, qw)
    if norm < 1e-9:
        issues.append("bad_quaternion_all_zero")

    confidence = record.get("confidence")
    if not isinstance(confidence, (int, float)) or not (0.0 <= float(confidence) <= 1.0):
        issues.append("confidence_out_of_range")

    return len(issues) == 0, issues


def parse_trajectory_record(record: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    ok, issues = validate_trajectory_record(record)
    if not ok:
        return None, issues

    qx = float(record["qx"])
    qy = float(record["qy"])
    qz = float(record["qz"])
    qw = float(record["qw"])
    norm = _quaternion_norm(qx, qy, qz, qw)
    qx, qy, qz, qw = qx / norm, qy / norm, qz / norm, qw / norm

    return {
        "node_id": str(record["node_id"]),
        "timestamp_ms": int(record["timestamp_ms"]),
        "confidence": float(record["confidence"]),
        "source_chain": list(record["source_chain"]),
        "pose": {
            "tx": float(record["tx"]),
            "ty": float(record["ty"]),
            "tz": float(record["tz"]),
            "qx": qx,
            "qy": qy,
            "qz": qz,
            "qw": qw,
        },
    }, []


def validate_trajectory_record_negative(
    record: Dict[str, Any],
    *,
    expect_issue: str,
) -> Tuple[bool, List[str]]:
    _, issues = validate_trajectory_record(record)
    if expect_issue == "missing_source_chain":
        return any(issue == "source_chain_required" for issue in issues), issues
    if expect_issue == "bad_quaternion":
        return any(issue == "bad_quaternion_all_zero" for issue in issues), issues
    if expect_issue == "missing_node_id":
        return any(issue == "node_id_required" for issue in issues), issues
    return False, issues


def validate_direct_candidate_bundle_bypass(bypass_bundle: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if bypass_bundle.get("ingest_pipeline_bypass") is True:
        issues.append("ingest_pipeline_bypass_forbidden")
    if bypass_bundle.get("generic_json_spatial_trace_bypass") is True:
        issues.append("generic_json_spatial_trace_bypass_forbidden")
    if bypass_bundle.get("input_format_ref") != INTERNAL_STANDARD_FORMAT:
        issues.append("direct_bundle_must_not_skip_internal_standard_format")
    if bypass_bundle.get("field_synthesis_entrypoint") != FIELD_SYNTHESIS_ENTRYPOINT:
        issues.append("field_synthesis_entrypoint_bypass_forbidden")
    if bypass_bundle.get("runtime_activation_allowed") is True:
        issues.append("runtime_activation_allowed_forbidden")
    if bypass_bundle.get("commercial_runtime_approved") is True:
        issues.append("commercial_runtime_approved_forbidden")
    return len(issues) > 0, issues


def _delta_translation(prev: Dict[str, Any], curr: Dict[str, Any]) -> List[float]:
    p0 = prev["pose"]
    p1 = curr["pose"]
    return [p1["tx"] - p0["tx"], p1["ty"] - p0["ty"], p1["tz"] - p0["tz"]]


def _delta_rotation_hint(prev: Dict[str, Any], curr: Dict[str, Any]) -> float:
    q0 = prev["pose"]
    q1 = curr["pose"]
    dot = (
        q0["qx"] * q1["qx"]
        + q0["qy"] * q1["qy"]
        + q0["qz"] * q1["qz"]
        + q0["qw"] * q1["qw"]
    )
    dot = max(-1.0, min(1.0, abs(dot)))
    return round(1.0 - dot, 6)


def _pose_json_trace_item(parsed: Dict[str, Any]) -> Dict[str, Any]:
    node_id = parsed["node_id"]
    trace_id = f"rtab_map_pose_{node_id}"
    return {
        "trace_id": trace_id,
        "source_chain": list(parsed["source_chain"]) + [trace_id],
        "timestamp_ms": parsed["timestamp_ms"],
        "confidence": parsed["confidence"],
        "candidate_type": "pose",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "payload": {
            "input_format": INPUT_FORMAT_REF,
            "ingest_ref": INGEST_REF,
            "target_format": TARGET_FORMAT_REF,
            "pose": dict(parsed["pose"]),
            "metadata": {
                "source_export_kind": INPUT_EXPORT_KIND,
                "node_id": node_id,
            },
        },
        "candidate_only": True,
    }


def _motion_json_trace_item(prev: Dict[str, Any], curr: Dict[str, Any]) -> Dict[str, Any]:
    from_node = prev["node_id"]
    to_node = curr["node_id"]
    trace_id = f"rtab_map_motion_{from_node}_{to_node}"
    return {
        "trace_id": trace_id,
        "source_chain": list(curr["source_chain"]) + [trace_id],
        "time_window_ms": [prev["timestamp_ms"], curr["timestamp_ms"]],
        "confidence": min(prev["confidence"], curr["confidence"]),
        "candidate_type": "motion",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "payload": {
            "input_format": INPUT_FORMAT_REF,
            "ingest_ref": INGEST_REF,
            "target_format": TARGET_FORMAT_REF,
            "motion": {
                "delta_translation": _delta_translation(prev, curr),
                "delta_rotation_hint": _delta_rotation_hint(prev, curr),
            },
            "metadata": {
                "source_export_kind": INPUT_EXPORT_KIND,
                "from_node_id": from_node,
                "to_node_id": to_node,
            },
        },
        "candidate_only": True,
    }


def convert_trajectory_records_to_json_spatial_trace_items(
    records: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    issues: List[str] = []
    parsed_records: List[Dict[str, Any]] = []

    for index, record in enumerate(records):
        parsed, record_issues = parse_trajectory_record(record)
        if parsed is None:
            issues.extend([f"record_{index}:{err}" for err in record_issues])
            continue
        parsed_records.append(parsed)

    if issues:
        return [], issues

    json_items: List[Dict[str, Any]] = []
    for parsed in parsed_records:
        json_items.append(_pose_json_trace_item(parsed))

    for prev, curr in zip(parsed_records, parsed_records[1:]):
        json_items.append(_motion_json_trace_item(prev, curr))

    return json_items, []


def summarize_json_trace_items(json_items: List[Dict[str, Any]]) -> Dict[str, int]:
    pose_count = sum(1 for item in json_items if item.get("candidate_type") == "pose")
    motion_count = sum(1 for item in json_items if item.get("candidate_type") == "motion")
    return {
        "json_trace_item_count": len(json_items),
        "pose_item_count": pose_count,
        "motion_item_count": motion_count,
    }
