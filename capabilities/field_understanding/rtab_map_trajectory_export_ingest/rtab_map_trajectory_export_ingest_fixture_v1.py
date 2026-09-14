# -*- coding: utf-8 -*-
"""RTAB-Map Trajectory Export Ingest — fixture v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.rtab_map_trajectory_export_ingest.rtab_map_trajectory_export_ingest_types_v1 import (
    INPUT_EXPORT_KIND,
    INPUT_FORMAT_REF,
    SOURCE_CHAIN,
)

FIXTURE_REF = "rtab_map_trajectory_export_fixture_v1"
_CHAIN = (SOURCE_CHAIN, FIXTURE_REF, INPUT_EXPORT_KIND)


def build_valid_trajectory_records_v1() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "node_id": "101",
            "timestamp_ms": 1000,
            "tx": 0.0,
            "ty": 0.0,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.0,
            "qw": 1.0,
            "confidence": 0.91,
            "source_chain": list(_CHAIN) + ["node_101"],
        },
        {
            "node_id": "102",
            "timestamp_ms": 1100,
            "tx": 0.05,
            "ty": 0.0,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.01,
            "qw": 0.99995,
            "confidence": 0.89,
            "source_chain": list(_CHAIN) + ["node_102"],
        },
        {
            "node_id": "103",
            "timestamp_ms": 1200,
            "tx": 0.11,
            "ty": 0.0,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.02,
            "qw": 0.9998,
            "confidence": 0.87,
            "source_chain": list(_CHAIN) + ["node_103"],
        },
    )


def build_negative_trajectory_records_v1() -> Dict[str, Dict[str, Any]]:
    base = dict(build_valid_trajectory_records_v1()[0])
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
        "bundle_ref": "bypass_rtab_map_direct_bundle",
        "bundle_kind": "spatial_evidence_candidate_bundle",
        "input_format_ref": INPUT_FORMAT_REF,
        "ingest_pipeline_bypass": True,
        "generic_json_spatial_trace_bypass": True,
        "field_synthesis_entrypoint": "midplatform_synthesis_v1",
        "pose_candidates": [{"candidate_type": "PoseCandidate", "candidate_ref": "bypass_pose"}],
        "runtime_activation_allowed": True,
        "commercial_runtime_approved": True,
    }


def build_fixture_document_v1() -> Dict[str, Any]:
    records = build_valid_trajectory_records_v1()
    return {
        "fixture_ref": FIXTURE_REF,
        "input_format_ref": INPUT_FORMAT_REF,
        "source_export_kind": INPUT_EXPORT_KIND,
        "source_chain_prefix": list(_CHAIN),
        "rtab_map_trajectory_fixture_count": len(records),
        "trajectory_records": list(records),
        "expected_json_trace_item_count": 5,
        "expected_pose_item_count": 3,
        "expected_motion_item_count": 2,
    }
