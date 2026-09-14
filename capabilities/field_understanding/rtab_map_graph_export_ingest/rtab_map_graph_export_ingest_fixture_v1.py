# -*- coding: utf-8 -*-
"""RTAB-Map Graph Export Ingest — fixture v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from capabilities.field_understanding.rtab_map_graph_export_ingest.rtab_map_graph_export_ingest_types_v1 import (
    INPUT_EXPORT_KIND,
    INPUT_FORMAT_REF,
    INTERNAL_STANDARD_FORMAT,
    SOURCE_CHAIN,
)

FIXTURE_REF = "rtab_map_graph_export_fixture_v1"
_CHAIN = (SOURCE_CHAIN, FIXTURE_REF, INPUT_EXPORT_KIND)


def build_valid_graph_nodes_v1() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "node_id": "node_301",
            "timestamp_ms": 3000,
            "tx": 0.0,
            "ty": 0.0,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.0,
            "qw": 1.0,
            "confidence": 0.94,
            "coordinate_scope": "local",
            "anchor_role": "stable_spatial_anchor",
            "source_chain": list(_CHAIN) + ["node_301"],
        },
        {
            "node_id": "node_302",
            "timestamp_ms": 3100,
            "tx": 1.2,
            "ty": 0.0,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.05,
            "qw": 0.99875,
            "confidence": 0.91,
            "coordinate_scope": "local",
            "anchor_role": "adjacent_spatial_anchor",
            "source_chain": list(_CHAIN) + ["node_302"],
        },
        {
            "node_id": "node_303",
            "timestamp_ms": 3200,
            "tx": 2.4,
            "ty": 0.1,
            "tz": 0.0,
            "qx": 0.0,
            "qy": 0.0,
            "qz": 0.1,
            "qw": 0.995,
            "confidence": 0.82,
            "coordinate_scope": "aligned_local",
            "anchor_role": "relocalization_hint_node",
            "global_alignment_hint": "gps_gnss_link_placeholder_v1",
            "gps_anchor_ref": "gps_anchor_placeholder_block_7",
            "map_alignment_ref": "map_alignment_placeholder_session_a",
            "source_chain": list(_CHAIN) + ["node_303"],
        },
    )


def build_valid_graph_edges_v1() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "edge_id": "edge_301_302",
            "from_node_id": "node_301",
            "to_node_id": "node_302",
            "edge_kind": "normal",
            "timestamp_ms": 3150,
            "confidence": 0.9,
            "relative_translation": [1.2, 0.0, 0.0],
            "source_chain": list(_CHAIN) + ["edge_301_302"],
        },
        {
            "edge_id": "edge_303_301",
            "from_node_id": "node_303",
            "to_node_id": "node_301",
            "edge_kind": "loop_closure",
            "timestamp_ms": 3250,
            "confidence": 0.78,
            "relative_translation": [-2.35, -0.08, 0.0],
            "loop_closure_drift_metric_m": 0.18,
            "source_chain": list(_CHAIN) + ["edge_303_301"],
        },
    )


def build_negative_graph_fixtures_v1() -> Dict[str, Dict[str, Any]]:
    base_node = dict(build_valid_graph_nodes_v1()[0])
    missing_chain = dict(base_node)
    missing_chain["source_chain"] = []
    missing_chain["node_id"] = "neg_missing_chain"

    missing_node_id = dict(base_node)
    del missing_node_id["node_id"]

    loop_closure_trust_restore = dict(build_valid_graph_edges_v1()[1])
    loop_closure_trust_restore.update(
        {
            "edge_id": "neg_loop_closure_trust_restore",
            "restore_runtime_trust": True,
            "runtime_trust_restored": True,
        }
    )

    return {
        "missing_source_chain": missing_chain,
        "missing_node_id": missing_node_id,
        "loop_closure_runtime_trust_restore": loop_closure_trust_restore,
    }


def build_direct_bundle_bypass_fixture_v1() -> Dict[str, Any]:
    return {
        "bundle_ref": "bypass_rtab_map_graph_direct_bundle",
        "bundle_kind": "spatial_evidence_candidate_bundle",
        "input_format_ref": INPUT_FORMAT_REF,
        "ingest_pipeline_bypass": True,
        "generic_json_spatial_trace_bypass": True,
        "field_synthesis_entrypoint": "midplatform_synthesis_v1",
        "spatial_anchor_candidates": [
            {"candidate_type": "SpatialAnchorCandidate", "candidate_ref": "bypass_anchor"}
        ],
        "relocalization_candidates": [
            {"candidate_type": "RelocalizationCandidate", "candidate_ref": "bypass_reloc"}
        ],
        "runtime_activation_allowed": True,
        "commercial_runtime_approved": True,
        "restore_runtime_trust": True,
    }


def build_fixture_document_v1() -> Dict[str, Any]:
    nodes = build_valid_graph_nodes_v1()
    edges = build_valid_graph_edges_v1()
    return {
        "fixture_ref": FIXTURE_REF,
        "input_format_ref": INPUT_FORMAT_REF,
        "source_export_kind": INPUT_EXPORT_KIND,
        "source_chain_prefix": list(_CHAIN),
        "rtab_map_graph_node_count": len(nodes),
        "rtab_map_graph_edge_count": len(edges),
        "graph_nodes": list(nodes),
        "graph_edges": list(edges),
        "expected_json_trace_item_count_min": 5,
        "expected_anchor_item_count": 3,
        "expected_relocalization_item_count": 1,
        "expected_drift_item_count": 1,
        "gps_gnss_link_reserved_fields": [
            "global_alignment_hint",
            "gps_anchor_ref",
            "map_alignment_ref",
            "coordinate_scope",
        ],
        "internal_standard_format": INTERNAL_STANDARD_FORMAT,
    }
