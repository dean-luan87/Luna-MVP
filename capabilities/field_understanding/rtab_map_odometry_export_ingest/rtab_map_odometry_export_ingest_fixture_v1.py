# -*- coding: utf-8 -*-
"""RTAB-Map Odometry Export Ingest — fixture v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from capabilities.field_understanding.rtab_map_odometry_export_ingest.rtab_map_odometry_export_ingest_types_v1 import (
    INPUT_EXPORT_KIND,
    INPUT_FORMAT_REF,
    INTERNAL_STANDARD_FORMAT,
    SOURCE_CHAIN,
)

FIXTURE_REF = "rtab_map_odometry_export_fixture_v1"
_CHAIN = (SOURCE_CHAIN, FIXTURE_REF, INPUT_EXPORT_KIND)


def build_valid_odometry_records_v1() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "node_id": "odom_201",
            "timestamp_ms": 2000,
            "tx": 0.0,
            "ty": 0.0,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.0,
            "qw": 1.0,
            "tracking_state": "ok",
            "confidence": 0.93,
            "linear_velocity": [0.05, 0.0, 0.0],
            "angular_velocity": [0.0, 0.0, 0.01],
            "covariance_placeholder": [0.01, 0.0, 0.0, 0.01],
            "source_chain": list(_CHAIN) + ["odom_201"],
        },
        {
            "node_id": "odom_202",
            "timestamp_ms": 2100,
            "tx": 0.05,
            "ty": 0.0,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.01,
            "qw": 0.99995,
            "tracking_state": "ok",
            "confidence": 0.9,
            "linear_velocity": [0.05, 0.0, 0.0],
            "angular_velocity": [0.0, 0.0, 0.01],
            "covariance_placeholder": [0.012, 0.0, 0.0, 0.012],
            "source_chain": list(_CHAIN) + ["odom_202"],
        },
        {
            "node_id": "odom_203",
            "timestamp_ms": 2200,
            "tx": 0.1,
            "ty": 0.0,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.02,
            "qw": 0.9998,
            "tracking_state": "degraded",
            "confidence": 0.58,
            "linear_velocity": [0.02, 0.0, 0.0],
            "angular_velocity": [0.0, 0.0, 0.02],
            "covariance_placeholder": [0.05, 0.0, 0.0, 0.06],
            "source_chain": list(_CHAIN) + ["odom_203"],
        },
    )


def build_negative_odometry_records_v1() -> Dict[str, Dict[str, Any]]:
    base = dict(build_valid_odometry_records_v1()[0])
    missing_chain = dict(base)
    missing_chain["source_chain"] = []
    missing_chain["node_id"] = "neg_missing_chain"

    bad_quat = dict(base)
    bad_quat.update(
        {
            "node_id": "neg_bad_quat",
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.0,
            "qw": 0.0,
        }
    )

    missing_node = dict(base)
    del missing_node["node_id"]

    return {
        "missing_source_chain": missing_chain,
        "bad_quaternion": bad_quat,
        "missing_node_id": missing_node,
    }


def build_direct_bundle_bypass_fixture_v1() -> Dict[str, Any]:
    return {
        "bundle_ref": "bypass_rtab_map_odometry_direct_bundle",
        "bundle_kind": "spatial_evidence_candidate_bundle",
        "input_format_ref": INPUT_FORMAT_REF,
        "ingest_pipeline_bypass": True,
        "generic_json_spatial_trace_bypass": True,
        "field_synthesis_entrypoint": "midplatform_synthesis_v1",
        "slam_health_candidates": [{"candidate_type": "SLAMHealthCandidate", "candidate_ref": "bypass_health"}],
        "runtime_activation_allowed": True,
        "commercial_runtime_approved": True,
    }


def build_fixture_document_v1() -> Dict[str, Any]:
    records = build_valid_odometry_records_v1()
    return {
        "fixture_ref": FIXTURE_REF,
        "input_format_ref": INPUT_FORMAT_REF,
        "source_export_kind": INPUT_EXPORT_KIND,
        "source_chain_prefix": list(_CHAIN),
        "rtab_map_odometry_fixture_count": len(records),
        "odometry_records": list(records),
        "expected_json_trace_item_count": 6,
        "expected_pose_item_count": 3,
        "expected_motion_item_count": 2,
        "expected_health_item_count": 1,
        "internal_standard_format": INTERNAL_STANDARD_FORMAT,
    }
