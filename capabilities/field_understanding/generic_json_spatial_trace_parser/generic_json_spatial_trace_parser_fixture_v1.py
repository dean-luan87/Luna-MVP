# -*- coding: utf-8 -*-
"""Generic JSON Spatial Trace Parser — minimal fixture v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    SOURCE_CHAIN,
)

FIXTURE_REF = "generic_json_spatial_trace_fixture_v1"
_CHAIN = (SOURCE_CHAIN, FIXTURE_REF)


def build_fixture_trace_items_v1() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "trace_id": "fixture_pose_motion_001",
            "source_chain": list(_CHAIN) + ["fixture_pose_motion_001"],
            "timestamp_ms": 1000,
            "confidence": 0.92,
            "candidate_type": "pose",
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "payload": {
                "position_m": [0.1, 0.2, 0.0],
                "orientation_quat": [0.0, 0.0, 0.0, 1.0],
                "companion_candidate_types": ["motion"],
                "motion": {"velocity_mps": [0.05, 0.01, 0.0]},
            },
            "candidate_only": True,
        },
        {
            "trace_id": "fixture_anchor_local_map_002",
            "source_chain": list(_CHAIN) + ["fixture_anchor_local_map_002"],
            "time_window_ms": [2000, 2500],
            "confidence": 0.88,
            "candidate_type": "anchor",
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "payload": {
                "anchor_ref": "anchor_room_a",
                "companion_candidate_types": ["local_map"],
                "local_map": {"map_ref": "local_map_room_a", "cell_count": 128},
            },
            "candidate_only": True,
        },
        {
            "trace_id": "fixture_health_degraded_003",
            "source_chain": list(_CHAIN) + ["fixture_health_degraded_003"],
            "timestamp_ms": 3000,
            "confidence": 0.61,
            "candidate_type": "health",
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "payload": {
                "health_status": "degraded",
                "tracking_quality": 0.55,
                "degradation_reason": "feature_poor_lighting",
            },
            "candidate_only": True,
        },
        {
            "trace_id": "fixture_drift_high_004",
            "source_chain": list(_CHAIN) + ["fixture_drift_high_004"],
            "timestamp_ms": 4000,
            "confidence": 0.73,
            "candidate_type": "drift",
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "payload": {
                "drift_level": "high",
                "drift_metric_m": 0.42,
                "map_segment_ref": "segment_b",
            },
            "candidate_only": True,
        },
        {
            "trace_id": "fixture_relocalization_005",
            "source_chain": list(_CHAIN) + ["fixture_relocalization_005"],
            "timestamp_ms": 5000,
            "confidence": 0.84,
            "candidate_type": "relocalization",
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "payload": {
                "relocalization_status": "candidate",
                "matched_map_ref": "map_session_01",
                "match_score": 0.79,
            },
            "candidate_only": True,
        },
    )


def build_negative_fixture_items_v1() -> Dict[str, Dict[str, Any]]:
    return {
        "unsupported_candidate_type": {
            "trace_id": "negative_unsupported_type",
            "source_chain": list(_CHAIN) + ["negative_unsupported_type"],
            "timestamp_ms": 9000,
            "confidence": 0.5,
            "candidate_type": "unsupported_xyz",
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "payload": {},
            "candidate_only": True,
        },
        "missing_source_chain": {
            "trace_id": "negative_missing_source_chain",
            "source_chain": [],
            "timestamp_ms": 9100,
            "confidence": 0.5,
            "candidate_type": "pose",
            "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
            "payload": {},
            "candidate_only": True,
        },
    }


def build_fixture_document_v1() -> Dict[str, Any]:
    return {
        "fixture_ref": FIXTURE_REF,
        "format_ref": "generic_json_spatial_trace",
        "fixture_count": len(build_fixture_trace_items_v1()),
        "trace_items": list(build_fixture_trace_items_v1()),
    }
