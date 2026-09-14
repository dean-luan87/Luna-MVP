# -*- coding: utf-8 -*-
"""Generic TUM Trajectory Ingest — static validators + TUM→JSON convert v1."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.generic_tum_trajectory_ingest.generic_tum_trajectory_ingest_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    INGEST_REF,
    INPUT_FORMAT_REF,
    TARGET_FORMAT_REF,
    TUM_COLUMN_COUNT,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_tum_eight_column_required",
    "rule_02_tum_quaternion_normalizable",
    "rule_03_ingest_source_chain_required",
    "rule_04_pose_json_trace_shape",
    "rule_05_motion_json_trace_shape",
    "rule_06_bad_column_count_rejected",
    "rule_07_bad_quaternion_rejected",
    "rule_08_missing_source_chain_rejected",
)


def _quaternion_norm(qx: float, qy: float, qz: float, qw: float) -> float:
    return math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)


def parse_tum_trajectory_line(line: str, *, line_index: int) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None, [f"line_{line_index}:empty_or_comment"]

    parts = stripped.split()
    if len(parts) != TUM_COLUMN_COUNT:
        return None, [f"line_{line_index}:bad_column_count:{len(parts)}"]

    try:
        timestamp_s = float(parts[0])
        tx, ty, tz = float(parts[1]), float(parts[2]), float(parts[3])
        qx, qy, qz, qw = float(parts[4]), float(parts[5]), float(parts[6]), float(parts[7])
    except ValueError:
        return None, [f"line_{line_index}:non_numeric_values"]

    norm = _quaternion_norm(qx, qy, qz, qw)
    if norm < 1e-9:
        return None, [f"line_{line_index}:bad_quaternion_all_zero"]

    qx, qy, qz, qw = qx / norm, qy / norm, qz / norm, qw / norm

    return {
        "line_index": line_index,
        "timestamp_s": timestamp_s,
        "timestamp_ms": int(round(timestamp_s * 1000)),
        "pose": {
            "tx": tx,
            "ty": ty,
            "tz": tz,
            "qx": qx,
            "qy": qy,
            "qz": qz,
            "qw": qw,
        },
    }, []


def validate_tum_line_negative(
    line: str,
    *,
    expect_issue: str,
    line_index: int = 0,
) -> Tuple[bool, List[str]]:
    parsed, issues = parse_tum_trajectory_line(line, line_index=line_index)
    if expect_issue == "bad_column_count":
        return parsed is None and any("bad_column_count" in issue for issue in issues), issues
    if expect_issue == "bad_quaternion":
        return parsed is None and any("bad_quaternion_all_zero" in issue for issue in issues), issues
    return False, issues


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


def _pose_json_trace_item(
    parsed: Dict[str, Any],
    *,
    source_chain_prefix: List[str],
) -> Dict[str, Any]:
    line_index = parsed["line_index"]
    trace_id = f"tum_pose_line_{line_index}"
    return {
        "trace_id": trace_id,
        "source_chain": list(source_chain_prefix) + [trace_id],
        "timestamp_ms": parsed["timestamp_ms"],
        "confidence": 0.9,
        "candidate_type": "pose",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "payload": {
            "input_format": INPUT_FORMAT_REF,
            "ingest_ref": INGEST_REF,
            "pose": dict(parsed["pose"]),
        },
        "candidate_only": True,
    }


def _motion_json_trace_item(
    prev: Dict[str, Any],
    curr: Dict[str, Any],
    *,
    source_chain_prefix: List[str],
) -> Dict[str, Any]:
    pair_id = f"tum_motion_pair_{prev['line_index']}_{curr['line_index']}"
    return {
        "trace_id": pair_id,
        "source_chain": list(source_chain_prefix) + [pair_id],
        "time_window_ms": [prev["timestamp_ms"], curr["timestamp_ms"]],
        "confidence": 0.85,
        "candidate_type": "motion",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "payload": {
            "input_format": INPUT_FORMAT_REF,
            "ingest_ref": INGEST_REF,
            "target_format": TARGET_FORMAT_REF,
            "delta_translation": _delta_translation(prev, curr),
            "delta_rotation_hint": _delta_rotation_hint(prev, curr),
        },
        "candidate_only": True,
    }


def convert_tum_lines_to_json_spatial_trace_items(
    lines: List[str],
    *,
    source_chain_prefix: List[str],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    issues: List[str] = []

    if not source_chain_prefix:
        return [], ["source_chain_required"]

    parsed_lines: List[Dict[str, Any]] = []
    for index, line in enumerate(lines):
        parsed, line_issues = parse_tum_trajectory_line(line, line_index=index)
        if parsed is None:
            issues.extend(line_issues)
            continue
        parsed_lines.append(parsed)

    if issues:
        return [], issues

    json_items: List[Dict[str, Any]] = []
    for parsed in parsed_lines:
        json_items.append(_pose_json_trace_item(parsed, source_chain_prefix=source_chain_prefix))

    for prev, curr in zip(parsed_lines, parsed_lines[1:]):
        json_items.append(_motion_json_trace_item(prev, curr, source_chain_prefix=source_chain_prefix))

    return json_items, []


def summarize_json_trace_items(json_items: List[Dict[str, Any]]) -> Dict[str, int]:
    pose_count = sum(1 for item in json_items if item.get("candidate_type") == "pose")
    motion_count = sum(1 for item in json_items if item.get("candidate_type") == "motion")
    return {
        "json_trace_item_count": len(json_items),
        "pose_item_count": pose_count,
        "motion_item_count": motion_count,
    }
