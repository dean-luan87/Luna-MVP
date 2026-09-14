# -*- coding: utf-8 -*-
"""RTAB-Map Graph Export Ingest — static validators + convert v1."""

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.rtab_map_graph_export_ingest.rtab_map_graph_export_ingest_types_v1 import (
    COORDINATE_SCOPES,
    EDGE_KINDS,
    FIELD_SYNTHESIS_ENTRYPOINT,
    GPS_GNSS_LINK_RESERVED_FIELDS,
    GRAPH_EDGE_REQUIRED_FIELDS,
    GRAPH_NODE_REQUIRED_FIELDS,
    INPUT_EXPORT_KIND,
    INPUT_FORMAT_REF,
    INTERNAL_STANDARD_FORMAT,
    INGEST_REF,
    TARGET_FORMAT_REF,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_graph_node_required_fields",
    "rule_02_graph_edge_required_fields",
    "rule_03_source_chain_required",
    "rule_04_node_id_required",
    "rule_05_coordinate_scope_allowed",
    "rule_06_edge_kind_allowed",
    "rule_07_quaternion_normalizable",
    "rule_08_anchor_json_trace_mapping",
    "rule_09_relocalization_json_trace_mapping",
    "rule_10_drift_json_trace_mapping",
    "rule_11_loop_closure_must_not_restore_runtime_trust",
    "rule_12_missing_source_chain_rejected",
    "rule_13_missing_node_id_rejected",
    "rule_14_loop_closure_runtime_trust_restore_rejected",
    "rule_15_direct_candidate_bundle_bypass_rejected",
    "rule_16_gps_gnss_link_metadata_candidate_only",
)


def _quaternion_norm(qx: float, qy: float, qz: float, qw: float) -> float:
    return math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)


def _has_edge_time_ref(edge: Dict[str, Any]) -> bool:
    if edge.get("timestamp_ms") is not None:
        return True
    window = edge.get("time_window_ms")
    return isinstance(window, (list, tuple)) and len(window) == 2


def validate_graph_node(node: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{field}" for field in GRAPH_NODE_REQUIRED_FIELDS if field not in node]

    if not node.get("source_chain"):
        issues.append("source_chain_required")
    if not node.get("node_id"):
        issues.append("node_id_required")

    coordinate_scope = node.get("coordinate_scope")
    if coordinate_scope not in COORDINATE_SCOPES:
        issues.append(f"unsupported_coordinate_scope:{coordinate_scope!r}")

    try:
        qx = float(node["qx"])
        qy = float(node["qy"])
        qz = float(node["qz"])
        qw = float(node["qw"])
    except (KeyError, TypeError, ValueError):
        return False, issues + ["quaternion_fields_invalid"]

    norm = _quaternion_norm(qx, qy, qz, qw)
    if norm < 1e-9:
        issues.append("bad_quaternion_all_zero")

    confidence = node.get("confidence")
    if not isinstance(confidence, (int, float)) or not (0.0 <= float(confidence) <= 1.0):
        issues.append("confidence_out_of_range")

    return len(issues) == 0, issues


def validate_graph_edge(edge: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{field}" for field in GRAPH_EDGE_REQUIRED_FIELDS if field not in edge]

    if not edge.get("source_chain"):
        issues.append("source_chain_required")
    if not _has_edge_time_ref(edge):
        issues.append("timestamp_ms_or_time_window_ms_required")

    edge_kind = edge.get("edge_kind")
    if edge_kind not in EDGE_KINDS:
        issues.append(f"unsupported_edge_kind:{edge_kind!r}")

    confidence = edge.get("confidence")
    if not isinstance(confidence, (int, float)) or not (0.0 <= float(confidence) <= 1.0):
        issues.append("confidence_out_of_range")

    if edge_kind == "loop_closure":
        if edge.get("restore_runtime_trust") is True:
            issues.append("loop_closure_restore_runtime_trust_forbidden")
        if edge.get("runtime_trust_restored") is True:
            issues.append("loop_closure_runtime_trust_restored_forbidden")

    return len(issues) == 0, issues


def parse_graph_node(node: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    ok, issues = validate_graph_node(node)
    if not ok:
        return None, issues

    qx = float(node["qx"])
    qy = float(node["qy"])
    qz = float(node["qz"])
    qw = float(node["qw"])
    norm = _quaternion_norm(qx, qy, qz, qw)
    qx, qy, qz, qw = qx / norm, qy / norm, qz / norm, qw / norm

    parsed: Dict[str, Any] = {
        "node_id": str(node["node_id"]),
        "timestamp_ms": int(node["timestamp_ms"]),
        "confidence": float(node["confidence"]),
        "coordinate_scope": str(node["coordinate_scope"]),
        "source_chain": list(node["source_chain"]),
        "anchor_role": str(node.get("anchor_role") or "spatial_anchor"),
        "pose": {
            "tx": float(node["tx"]),
            "ty": float(node["ty"]),
            "tz": float(node["tz"]),
            "qx": qx,
            "qy": qy,
            "qz": qz,
            "qw": qw,
        },
    }
    for field in GPS_GNSS_LINK_RESERVED_FIELDS:
        if field in node:
            parsed[field] = node[field]

    return parsed, []


def parse_graph_edge(edge: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], List[str]]:
    ok, issues = validate_graph_edge(edge)
    if not ok:
        return None, issues

    time_ref: Dict[str, Any]
    if edge.get("timestamp_ms") is not None:
        time_ref = {"kind": "timestamp_ms", "value": int(edge["timestamp_ms"])}
    else:
        window = edge["time_window_ms"]
        time_ref = {"kind": "time_window_ms", "value": [int(window[0]), int(window[1])]}

    return {
        "edge_id": str(edge["edge_id"]),
        "from_node_id": str(edge["from_node_id"]),
        "to_node_id": str(edge["to_node_id"]),
        "edge_kind": str(edge["edge_kind"]),
        "confidence": float(edge["confidence"]),
        "source_chain": list(edge["source_chain"]),
        "time_ref": time_ref,
        "relative_translation": list(edge.get("relative_translation") or []),
        "loop_closure_drift_metric_m": edge.get("loop_closure_drift_metric_m"),
    }, []


def validate_graph_node_negative(
    node: Dict[str, Any],
    *,
    expect_issue: str,
) -> Tuple[bool, List[str]]:
    _, issues = validate_graph_node(node)
    if expect_issue == "missing_source_chain":
        return any(issue == "source_chain_required" for issue in issues), issues
    if expect_issue == "missing_node_id":
        return any(issue == "node_id_required" for issue in issues), issues
    return False, issues


def validate_graph_edge_negative(
    edge: Dict[str, Any],
    *,
    expect_issue: str,
) -> Tuple[bool, List[str]]:
    _, issues = validate_graph_edge(edge)
    if expect_issue == "loop_closure_runtime_trust_restore":
        return any(
            issue in ("loop_closure_restore_runtime_trust_forbidden", "loop_closure_runtime_trust_restored_forbidden")
            for issue in issues
        ), issues
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
    if bypass_bundle.get("restore_runtime_trust") is True:
        issues.append("restore_runtime_trust_forbidden")
    return len(issues) > 0, issues


def _metadata_from_node(parsed: Dict[str, Any]) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {
        "source_export_kind": INPUT_EXPORT_KIND,
        "node_id": parsed["node_id"],
        "coordinate_scope": parsed["coordinate_scope"],
        "anchor_role": parsed["anchor_role"],
        "candidate_only": True,
        "field_identity_mutation_allowed": False,
        "direct_action_allowed": False,
    }
    for field in GPS_GNSS_LINK_RESERVED_FIELDS:
        if field in parsed:
            metadata[field] = parsed[field]
    return metadata


def _anchor_json_trace_item(parsed: Dict[str, Any]) -> Dict[str, Any]:
    node_id = parsed["node_id"]
    trace_id = f"rtab_map_graph_anchor_{node_id}"
    pose = parsed["pose"]
    return {
        "trace_id": trace_id,
        "source_chain": list(parsed["source_chain"]) + [trace_id],
        "timestamp_ms": parsed["timestamp_ms"],
        "confidence": parsed["confidence"],
        "candidate_type": "anchor",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "payload": {
            "input_format": INPUT_FORMAT_REF,
            "ingest_ref": INGEST_REF,
            "target_format": TARGET_FORMAT_REF,
            "anchor_ref": f"graph_node_{node_id}",
            "position_m": [pose["tx"], pose["ty"], pose["tz"]],
            "orientation_quat": [pose["qx"], pose["qy"], pose["qz"], pose["qw"]],
            "metadata": _metadata_from_node(parsed),
        },
        "candidate_only": True,
    }


def _relocalization_json_trace_item(
    edge: Dict[str, Any],
    *,
    from_node: Dict[str, Any],
    to_node: Dict[str, Any],
) -> Dict[str, Any]:
    edge_id = edge["edge_id"]
    trace_id = f"rtab_map_graph_relocalization_{edge_id}"
    time_ref = edge["time_ref"]
    item: Dict[str, Any] = {
        "trace_id": trace_id,
        "source_chain": list(edge["source_chain"]) + [trace_id],
        "confidence": edge["confidence"],
        "candidate_type": "relocalization",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "payload": {
            "input_format": INPUT_FORMAT_REF,
            "ingest_ref": INGEST_REF,
            "target_format": TARGET_FORMAT_REF,
            "relocalization_status": "candidate",
            "matched_map_ref": f"graph_closure_{to_node['node_id']}",
            "match_score": edge["confidence"],
            "from_node_id": edge["from_node_id"],
            "to_node_id": edge["to_node_id"],
            "metadata": {
                "source_export_kind": INPUT_EXPORT_KIND,
                "edge_id": edge_id,
                "edge_kind": edge["edge_kind"],
                "coordinate_scope": from_node["coordinate_scope"],
                "restore_runtime_trust": False,
                "runtime_trust_restored": False,
                "candidate_only": True,
                "field_identity_mutation_allowed": False,
                "direct_action_allowed": False,
            },
        },
        "candidate_only": True,
    }
    if time_ref["kind"] == "timestamp_ms":
        item["timestamp_ms"] = time_ref["value"]
    else:
        item["time_window_ms"] = time_ref["value"]
    return item


def _drift_json_trace_item(edge: Dict[str, Any]) -> Dict[str, Any]:
    edge_id = edge["edge_id"]
    trace_id = f"rtab_map_graph_drift_{edge_id}"
    drift_metric = float(edge.get("loop_closure_drift_metric_m") or 0.15)
    drift_level = "high" if drift_metric >= 0.3 else "moderate" if drift_metric >= 0.1 else "low"
    time_ref = edge["time_ref"]
    item: Dict[str, Any] = {
        "trace_id": trace_id,
        "source_chain": list(edge["source_chain"]) + [trace_id],
        "confidence": edge["confidence"],
        "candidate_type": "drift",
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "payload": {
            "input_format": INPUT_FORMAT_REF,
            "ingest_ref": INGEST_REF,
            "target_format": TARGET_FORMAT_REF,
            "drift_level": drift_level,
            "drift_metric_m": drift_metric,
            "drift_check_kind": "loop_closure_drift_check",
            "map_segment_ref": f"graph_segment_{edge['from_node_id']}_{edge['to_node_id']}",
            "metadata": {
                "source_export_kind": INPUT_EXPORT_KIND,
                "edge_id": edge_id,
                "edge_kind": edge["edge_kind"],
                "candidate_only": True,
                "field_identity_mutation_allowed": False,
                "direct_action_allowed": False,
            },
        },
        "candidate_only": True,
    }
    if time_ref["kind"] == "timestamp_ms":
        item["timestamp_ms"] = time_ref["value"]
    else:
        item["time_window_ms"] = time_ref["value"]
    return item


def convert_graph_export_to_json_spatial_trace_items(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], List[str]]:
    issues: List[str] = []
    parsed_nodes: Dict[str, Dict[str, Any]] = {}
    parsed_edges: List[Dict[str, Any]] = []

    for index, node in enumerate(nodes):
        parsed, node_issues = parse_graph_node(node)
        if parsed is None:
            issues.extend([f"node_{index}:{err}" for err in node_issues])
            continue
        parsed_nodes[parsed["node_id"]] = parsed

    for index, edge in enumerate(edges):
        parsed, edge_issues = parse_graph_edge(edge)
        if parsed is None:
            issues.extend([f"edge_{index}:{err}" for err in edge_issues])
            continue
        parsed_edges.append(parsed)

    if issues:
        return [], issues

    json_items: List[Dict[str, Any]] = []
    for node in nodes:
        parsed = parsed_nodes[str(node["node_id"])]
        json_items.append(_anchor_json_trace_item(parsed))

    loop_closure_edges = [edge for edge in parsed_edges if edge["edge_kind"] == "loop_closure"]
    if not loop_closure_edges:
        issues.append("loop_closure_edge_required_for_relocalization_and_drift")
        return [], issues

    for edge in loop_closure_edges:
        from_node = parsed_nodes.get(edge["from_node_id"])
        to_node = parsed_nodes.get(edge["to_node_id"])
        if from_node is None or to_node is None:
            issues.append(f"loop_closure_edge_missing_node:{edge['edge_id']}")
            continue
        json_items.append(_relocalization_json_trace_item(edge, from_node=from_node, to_node=to_node))
        json_items.append(_drift_json_trace_item(edge))

    if issues:
        return [], issues

    return json_items, []


def summarize_json_trace_items(json_items: List[Dict[str, Any]]) -> Dict[str, int]:
    return {
        "json_trace_item_count": len(json_items),
        "anchor_item_count": sum(1 for item in json_items if item.get("candidate_type") == "anchor"),
        "relocalization_item_count": sum(
            1 for item in json_items if item.get("candidate_type") == "relocalization"
        ),
        "drift_item_count": sum(1 for item in json_items if item.get("candidate_type") == "drift"),
    }


def verify_gps_gnss_link_reserved(json_items: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    aligned_anchors = [
        item
        for item in json_items
        if item.get("candidate_type") == "anchor"
        and (item.get("payload") or {}).get("metadata", {}).get("coordinate_scope") == "aligned_local"
    ]
    if not aligned_anchors:
        issues.append("aligned_local_anchor_missing")
        return False, issues

    for item in aligned_anchors:
        metadata = (item.get("payload") or {}).get("metadata") or {}
        if "global_alignment_hint" not in metadata:
            issues.append(f"missing_global_alignment_hint:{item['trace_id']}")
        if "gps_anchor_ref" not in metadata:
            issues.append(f"missing_gps_anchor_ref:{item['trace_id']}")
        if "map_alignment_ref" not in metadata:
            issues.append(f"missing_map_alignment_ref:{item['trace_id']}")
        if metadata.get("field_identity_mutation_allowed") is True:
            issues.append(f"field_identity_mutation_forbidden:{item['trace_id']}")
        if metadata.get("direct_action_allowed") is True:
            issues.append(f"direct_action_forbidden:{item['trace_id']}")

    return len(issues) == 0, issues


def verify_runtime_trust_not_restored(json_items: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for item in json_items:
        if item.get("candidate_type") != "relocalization":
            continue
        metadata = (item.get("payload") or {}).get("metadata") or {}
        if metadata.get("restore_runtime_trust") is True:
            issues.append(f"restore_runtime_trust_forbidden:{item['trace_id']}")
        if metadata.get("runtime_trust_restored") is True:
            issues.append(f"runtime_trust_restored_forbidden:{item['trace_id']}")
        if item.get("candidate_only") is not True:
            issues.append(f"relocalization_must_be_candidate_only:{item['trace_id']}")
    return len(issues) == 0, issues
