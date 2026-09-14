# -*- coding: utf-8 -*-
"""Generic TUM Trajectory Ingest — fixture v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.generic_tum_trajectory_ingest.generic_tum_trajectory_ingest_types_v1 import (
    INPUT_FORMAT_REF,
    SOURCE_CHAIN,
)

FIXTURE_REF = "generic_tum_trajectory_fixture_v1"


def build_valid_tum_fixture_lines_v1() -> Tuple[str, ...]:
    return (
        "0.000 0.000 0.000 0.000 0.000 0.000 0.000 1.000",
        "0.100 0.050 0.000 0.000 0.000 0.000 0.010 0.999",
        "0.200 0.110 0.000 0.000 0.000 0.000 0.020 0.999",
    )


def build_negative_tum_fixture_lines_v1() -> Dict[str, str]:
    return {
        "bad_column_count": "0.300 0.120 0.000 0.000",
        "bad_quaternion_all_zero": "0.300 0.120 0.000 0.000 0.000 0.000 0.000 0.000",
    }


def build_fixture_document_v1() -> Dict[str, Any]:
    lines = build_valid_tum_fixture_lines_v1()
    return {
        "fixture_ref": FIXTURE_REF,
        "input_format_ref": INPUT_FORMAT_REF,
        "source_chain_prefix": [SOURCE_CHAIN, FIXTURE_REF],
        "tum_fixture_line_count": len(lines),
        "tum_lines": list(lines),
        "expected_json_trace_item_count": 5,
        "expected_pose_item_count": 3,
        "expected_motion_item_count": 2,
    }
