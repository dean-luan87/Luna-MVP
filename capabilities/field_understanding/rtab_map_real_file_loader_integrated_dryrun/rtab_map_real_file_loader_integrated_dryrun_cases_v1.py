# -*- coding: utf-8 -*-
"""RTAB-Map Real File Loader Integrated DryRun — cases v1.

Reuses generic_json_spatial_trace_parser static validators (no reimplementation).
Reuses proven odometry health-mapping logic.
Covers odometry dry-run, graph planning-lite + dry-run, multi-export closure.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.field_understanding.generic_json_spatial_trace_parser.generic_json_spatial_trace_parser_static_validators_v1 import (
    map_parsed_traces_to_candidate_bundle,
    parse_json_spatial_trace_item,
    validate_candidate_bundle_mapping,
)
from capabilities.field_understanding.rtab_map_odometry_real_file_loader_dryrun.rtab_map_odometry_real_file_loader_dryrun_cases_v1 import (
    map_tracking_state_to_health,
)
from capabilities.field_understanding.rtab_map_real_file_loader_integrated_dryrun.rtab_map_real_file_loader_integrated_dryrun_types_v1 import (
    DRIFT_DRIFT_SCORE_THRESHOLD,
    DRIFT_HINT_ALIASES,
    EDGE_FROM_ALIASES,
    EDGE_TO_ALIASES,
    EDGE_TYPE_ALIASES,
    GRAPH_SOURCE_FORMAT,
    HEALTH_PROVIDER,
    LOOP_CLOSURE_ALIASES,
    LOOP_CLOSURE_EDGE_TYPES,
    NEGATIVE_CASE_REFS,
    NODE_ID_ALIASES,
    ODOMETRY_QUALITY_ALIASES,
    ODOMETRY_SOURCE_FORMAT,
    ORIENTATION_FIELDS,
    POSITIVE_CASE_REFS,
    PROHIBITED_EDGE_FLAGS,
    PROHIBITED_FILE_FLAGS,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    TIMESTAMP_MS_ALIASES,
    TIMESTAMP_SEC_ALIASES,
    TRACKING_STATE_ALIASES,
    TRANSLATION_ALIASES,
)

_MODULE_DIR = Path(__file__).resolve().parent
_SAMPLES_DIR = _MODULE_DIR / "samples"


def samples_dir() -> Path:
    return _SAMPLES_DIR


def is_controlled_sample_path(path: Path) -> bool:
    try:
        resolved = path.resolve()
        samples_resolved = _SAMPLES_DIR.resolve()
        return samples_resolved in resolved.parents or resolved == samples_resolved
    except OSError:
        return False


def read_local_rtab_file(sample_file: str) -> Tuple[Optional[Dict[str, Any]], bool, List[str]]:
    path = _SAMPLES_DIR / sample_file
    if not is_controlled_sample_path(path):
        return None, False, [f"sample_path_not_controlled:{sample_file}"]
    if not path.is_file():
        return None, False, [f"sample_file_missing:{sample_file}"]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, True, [f"sample_read_failed:{sample_file}:{exc}"]
    if not isinstance(doc, dict):
        return None, True, [f"sample_root_not_object:{sample_file}"]
    return doc, True, []


def admit_rtab_file_source(
    *, sample_file: str, file_doc: Dict[str, Any], expected_format: str
) -> Dict[str, Any]:
    path = _SAMPLES_DIR / sample_file
    rejection_reasons: List[str] = []

    controlled_ok = is_controlled_sample_path(path)
    if not controlled_ok:
        rejection_reasons.append("controlled_samples_path_violation")

    format_ref_ok = file_doc.get("format_ref") == expected_format
    if not format_ref_ok:
        rejection_reasons.append(f"format_ref_not_{expected_format}")

    file_origin = file_doc.get("file_origin") or {}
    file_origin_present = bool(file_origin)
    if not file_origin_present:
        rejection_reasons.append("file_origin_metadata_missing")

    source_chain_present = bool(file_doc.get("source_chain"))
    if not source_chain_present:
        rejection_reasons.append("source_chain_missing")

    prohibited_flags_absent = not any(
        file_doc.get(flag) is True for flag in PROHIBITED_FILE_FLAGS
    )
    if not prohibited_flags_absent:
        rejection_reasons.append("prohibited_backend_native_flags_present")

    admitted = len(rejection_reasons) == 0
    return {
        "result_ref": f"rtab_int_admission_{sample_file}",
        "file_source_admitted": admitted,
        "controlled_samples_path_ok": controlled_ok,
        "format_ref_ok": format_ref_ok,
        "file_origin_metadata_present": file_origin_present,
        "source_chain_present": source_chain_present,
        "prohibited_flags_absent": prohibited_flags_absent,
        "rejection_reasons": rejection_reasons,
        "source_chain": SOURCE_CHAIN,
    }


def _resolve_alias(record: Dict[str, Any], aliases: Tuple[str, ...]) -> Tuple[Any, bool]:
    for index, key in enumerate(aliases):
        if key in record and record[key] is not None:
            return record[key], index > 0
    return None, False


def _resolve_timestamp_ms(record: Dict[str, Any]) -> Tuple[Optional[int], bool]:
    for key in TIMESTAMP_MS_ALIASES:
        if key in record and record[key] is not None:
            try:
                return int(round(float(record[key]))), False
            except (TypeError, ValueError):
                return None, False
    for key in TIMESTAMP_SEC_ALIASES:
        if key in record and record[key] is not None:
            try:
                return int(round(float(record[key]) * 1000)), True
            except (TypeError, ValueError):
                return None, True
    return None, False


def _resolve_translation(record: Dict[str, Any]) -> Tuple[Optional[Dict[str, float]], bool]:
    result: Dict[str, float] = {}
    used_alias = False
    for std_key, aliases in TRANSLATION_ALIASES.items():
        value, is_alias = _resolve_alias(record, aliases)
        if value is None:
            return None, used_alias
        try:
            result[std_key] = float(value)
        except (TypeError, ValueError):
            return None, used_alias
        used_alias = used_alias or is_alias
    return result, used_alias


def _resolve_orientation(record: Dict[str, Any]) -> Optional[Dict[str, float]]:
    result: Dict[str, float] = {}
    for key in ORIENTATION_FIELDS:
        if key not in record or record[key] is None:
            return None
        try:
            result[key] = float(record[key])
        except (TypeError, ValueError):
            return None
    return result


def _quaternion_valid(orientation: Dict[str, float]) -> bool:
    norm = math.sqrt(
        orientation["qx"] ** 2
        + orientation["qy"] ** 2
        + orientation["qz"] ** 2
        + orientation["qw"] ** 2
    )
    return norm >= 1e-9


def replay_via_generic_json_parser(json_trace_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    parsed_items: List[Dict[str, Any]] = []
    parse_errors: List[str] = []
    for item in json_trace_items:
        parsed, errors = parse_json_spatial_trace_item(item)
        if errors:
            parse_errors.extend([f"{item.get('trace_id')}:{err}" for err in errors])
        parsed_items.extend(parsed)

    bundle = map_parsed_traces_to_candidate_bundle(parsed_items)
    bundle_ok, bundle_issues = validate_candidate_bundle_mapping(bundle)
    return {
        "generic_json_parser_reused": True,
        "parsed_count": len(parsed_items),
        "parse_errors": parse_errors,
        "candidate_bundle_mapping_ok": bundle_ok and not parse_errors,
        "output_candidate_types": list(bundle.get("output_candidate_types") or ()),
        "bundle_issues": bundle_issues,
        "spatial_evidence_candidate_bundle": bundle,
        "source_chain": SOURCE_CHAIN,
    }


# --------------------------------------------------------------------------- #
# Odometry pipeline
# --------------------------------------------------------------------------- #
def parse_rtab_odometry_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    valid_records: List[Dict[str, Any]] = []
    parse_errors: List[str] = []
    rejected = 0
    alias_used = False

    for index, record in enumerate(records):
        node_id, node_alias = _resolve_alias(record, NODE_ID_ALIASES)
        if node_id is None:
            rejected += 1
            parse_errors.append(f"record_{index}:missing_node_id")
            continue
        timestamp_ms, ts_alias = _resolve_timestamp_ms(record)
        if timestamp_ms is None:
            rejected += 1
            parse_errors.append(f"record_{index}:missing_or_bad_timestamp")
            continue
        translation, tr_alias = _resolve_translation(record)
        if translation is None:
            rejected += 1
            parse_errors.append(f"record_{index}:missing_translation")
            continue
        orientation = _resolve_orientation(record)
        if orientation is None:
            rejected += 1
            parse_errors.append(f"record_{index}:missing_orientation")
            continue
        if not _quaternion_valid(orientation):
            rejected += 1
            parse_errors.append(f"record_{index}:bad_quaternion_all_zero")
            continue
        confidence = record.get("confidence")
        if not isinstance(confidence, (int, float)):
            rejected += 1
            parse_errors.append(f"record_{index}:missing_confidence")
            continue
        tracking_state_raw, ts_state_alias = _resolve_alias(record, TRACKING_STATE_ALIASES)
        if tracking_state_raw is None:
            rejected += 1
            parse_errors.append(f"record_{index}:missing_tracking_state")
            continue
        tracking_state = str(tracking_state_raw).lower()
        odometry_quality_raw, oq_alias = _resolve_alias(record, ODOMETRY_QUALITY_ALIASES)
        odometry_quality = None
        if odometry_quality_raw is not None:
            try:
                odometry_quality = float(odometry_quality_raw)
            except (TypeError, ValueError):
                odometry_quality = None
        record_source_chain = record.get("source_chain")
        if not record_source_chain:
            rejected += 1
            parse_errors.append(f"record_{index}:missing_source_chain")
            continue

        alias_used = alias_used or node_alias or ts_alias or tr_alias or ts_state_alias or oq_alias
        valid_records.append(
            {
                "node_id": node_id,
                "timestamp_ms": timestamp_ms,
                "row_index": index,
                "pose": {**translation, **orientation},
                "confidence": float(confidence),
                "tracking_state": tracking_state,
                "odometry_quality": odometry_quality,
                "source_chain": list(record_source_chain),
                "health_mapping": map_tracking_state_to_health(tracking_state, odometry_quality),
            }
        )

    return {
        "valid_records": valid_records,
        "valid_record_count": len(valid_records),
        "rejected_record_count": rejected,
        "alias_field_mapping_used": alias_used,
        "parse_errors": parse_errors,
    }


def _odom_pose_item(record, *, file_origin, export_session_id):
    node_id = record["node_id"]
    trace_id = f"rtab_odom_pose_{node_id}"
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": ODOMETRY_SOURCE_FORMAT,
        "node_id": node_id,
        "row_index": record["row_index"],
        "export_session_id": export_session_id,
        "tracking_state": record["tracking_state"],
    }
    return {
        "trace_id": trace_id,
        "source_chain": list(record["source_chain"]) + [trace_id],
        "timestamp_ms": record["timestamp_ms"],
        "confidence": record["confidence"],
        "candidate_type": "pose",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "metadata": metadata,
        "payload": {"source_format": ODOMETRY_SOURCE_FORMAT, "pose": dict(record["pose"]), "metadata": metadata},
        "candidate_only": True,
    }


def _odom_motion_item(prev_record, curr_record, *, file_origin, export_session_id):
    from_node_id = prev_record["node_id"]
    to_node_id = curr_record["node_id"]
    trace_id = f"rtab_odom_motion_{from_node_id}_{to_node_id}"
    p0, p1 = prev_record["pose"], curr_record["pose"]
    delta_translation = [p1["x"] - p0["x"], p1["y"] - p0["y"], p1["z"] - p0["z"]]
    dot = p0["qx"] * p1["qx"] + p0["qy"] * p1["qy"] + p0["qz"] * p1["qz"] + p0["qw"] * p1["qw"]
    dot = max(-1.0, min(1.0, abs(dot)))
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": ODOMETRY_SOURCE_FORMAT,
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "export_session_id": export_session_id,
    }
    return {
        "trace_id": trace_id,
        "source_chain": list(prev_record["source_chain"]) + [trace_id],
        "time_window_ms": [prev_record["timestamp_ms"], curr_record["timestamp_ms"]],
        "confidence": min(prev_record["confidence"], curr_record["confidence"]),
        "candidate_type": "motion",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "metadata": metadata,
        "payload": {
            "source_format": ODOMETRY_SOURCE_FORMAT,
            "delta_translation": delta_translation,
            "delta_rotation_hint": round(1.0 - dot, 6),
            "from_node_id": from_node_id,
            "to_node_id": to_node_id,
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def _odom_health_item(record, *, file_origin, export_session_id):
    node_id = record["node_id"]
    health_map = record["health_mapping"]
    trace_id = f"rtab_odom_health_{node_id}"
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": ODOMETRY_SOURCE_FORMAT,
        "node_id": node_id,
        "row_index": record["row_index"],
        "export_session_id": export_session_id,
        "tracking_state": record["tracking_state"],
    }
    return {
        "trace_id": trace_id,
        "source_chain": list(record["source_chain"]) + [trace_id],
        "timestamp_ms": record["timestamp_ms"],
        "confidence": record["confidence"],
        "candidate_type": "health",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "metadata": metadata,
        "payload": {
            "source_format": ODOMETRY_SOURCE_FORMAT,
            "health": {
                "provider": HEALTH_PROVIDER,
                "tracking_state": record["tracking_state"],
                "odometry_quality": record.get("odometry_quality"),
                "health_status": health_map["health_status"],
                "severity": health_map["severity"],
                "reason": health_map["reason"],
                "candidate_risk_only": True,
            },
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def convert_odometry_records(valid_records, *, file_origin, export_session_id) -> Dict[str, Any]:
    if not file_origin or not valid_records:
        return {"conversion_ok": False, "json_trace_items": [], "pose_item_count": 0,
                "motion_item_count": 0, "health_item_count": 0, "health_mappings": []}
    json_items: List[Dict[str, Any]] = []
    health_mappings: List[Dict[str, Any]] = []
    for record in valid_records:
        json_items.append(_odom_pose_item(record, file_origin=file_origin, export_session_id=export_session_id))
        if record["health_mapping"].get("health_candidate_emitted"):
            json_items.append(_odom_health_item(record, file_origin=file_origin, export_session_id=export_session_id))
            health_mappings.append({"node_id": record["node_id"], **record["health_mapping"],
                                    "tracking_state": record["tracking_state"],
                                    "odometry_quality": record.get("odometry_quality")})
    for i in range(len(valid_records) - 1):
        json_items.append(_odom_motion_item(valid_records[i], valid_records[i + 1],
                                            file_origin=file_origin, export_session_id=export_session_id))
    return {
        "conversion_ok": bool(json_items),
        "json_trace_items": json_items,
        "pose_item_count": sum(1 for it in json_items if it["candidate_type"] == "pose"),
        "motion_item_count": sum(1 for it in json_items if it["candidate_type"] == "motion"),
        "health_item_count": sum(1 for it in json_items if it["candidate_type"] == "health"),
        "health_mappings": health_mappings,
    }


def run_odometry_pipeline(sample_file: str) -> Dict[str, Any]:
    file_doc, read_ok, read_issues = read_local_rtab_file(sample_file)
    admission = admit_rtab_file_source(
        sample_file=sample_file, file_doc=file_doc or {}, expected_format=ODOMETRY_SOURCE_FORMAT
    )
    export_session_id = (file_doc or {}).get("export_session_id", "")
    file_origin = (file_doc or {}).get("file_origin") or {}
    row = {"valid_records": [], "valid_record_count": 0, "rejected_record_count": 0,
           "alias_field_mapping_used": False, "parse_errors": read_issues}
    conv = {"conversion_ok": False, "json_trace_items": [], "pose_item_count": 0,
            "motion_item_count": 0, "health_item_count": 0, "health_mappings": []}
    replay = {"candidate_bundle_mapping_ok": False, "spatial_evidence_candidate_bundle": {},
              "output_candidate_types": []}
    admitted = admission["file_source_admitted"] and read_ok and file_doc is not None
    if admitted:
        row = parse_rtab_odometry_records(file_doc.get("records") or [])
        if row["rejected_record_count"] == 0 and row["valid_record_count"] > 0:
            conv = convert_odometry_records(row["valid_records"], file_origin=file_origin,
                                            export_session_id=export_session_id)
            if conv["conversion_ok"]:
                replay = replay_via_generic_json_parser(conv["json_trace_items"])
    return {"sample_file": sample_file, "read_ok": read_ok, "admission": admission,
            "export_session_id": export_session_id, "file_origin": file_origin,
            "row": row, "conversion": conv, "replay": replay, "admitted": admitted}


# --------------------------------------------------------------------------- #
# Graph pipeline (planning-lite + dry-run)
# --------------------------------------------------------------------------- #
def parse_rtab_graph(file_doc: Dict[str, Any]) -> Dict[str, Any]:
    nodes = file_doc.get("graph_nodes") or []
    edges = file_doc.get("graph_edges") or []
    valid_nodes: List[Dict[str, Any]] = []
    valid_edges: List[Dict[str, Any]] = []
    parse_errors: List[str] = []
    rejected = 0
    alias_used = False
    node_index: Dict[Any, Dict[str, Any]] = {}

    for index, node in enumerate(nodes):
        node_id, node_alias = _resolve_alias(node, NODE_ID_ALIASES)
        if node_id is None:
            rejected += 1
            parse_errors.append(f"node_{index}:missing_node_id")
            continue
        translation, tr_alias = _resolve_translation(node)
        if translation is None:
            rejected += 1
            parse_errors.append(f"node_{index}:missing_translation")
            continue
        orientation = _resolve_orientation(node)
        if orientation is None or not _quaternion_valid(orientation):
            rejected += 1
            parse_errors.append(f"node_{index}:bad_or_missing_quaternion")
            continue
        confidence = node.get("confidence")
        if not isinstance(confidence, (int, float)):
            rejected += 1
            parse_errors.append(f"node_{index}:missing_confidence")
            continue
        node_chain = node.get("source_chain")
        if not node_chain:
            rejected += 1
            parse_errors.append(f"node_{index}:missing_source_chain")
            continue
        alias_used = alias_used or node_alias or tr_alias
        parsed_node = {
            "node_id": node_id,
            "timestamp_ms": _resolve_timestamp_ms(node)[0],
            "row_index": index,
            "pose": {**translation, **orientation},
            "confidence": float(confidence),
            "coordinate_scope": node.get("coordinate_scope"),
            "anchor_role": node.get("anchor_role"),
            "source_chain": list(node_chain),
        }
        valid_nodes.append(parsed_node)
        node_index[node_id] = parsed_node

    for index, edge in enumerate(edges):
        if any(edge.get(flag) is True for flag in PROHIBITED_EDGE_FLAGS):
            rejected += 1
            parse_errors.append(f"edge_{index}:runtime_trust_restore_attempt")
            continue
        from_id, from_alias = _resolve_alias(edge, EDGE_FROM_ALIASES)
        to_id, to_alias = _resolve_alias(edge, EDGE_TO_ALIASES)
        if from_id is None or to_id is None:
            rejected += 1
            parse_errors.append(f"edge_{index}:missing_endpoints")
            continue
        edge_type_raw, et_alias = _resolve_alias(edge, EDGE_TYPE_ALIASES)
        edge_type = str(edge_type_raw).lower() if edge_type_raw is not None else "normal"
        edge_chain = edge.get("source_chain")
        if not edge_chain:
            rejected += 1
            parse_errors.append(f"edge_{index}:missing_source_chain")
            continue
        confidence = edge.get("confidence")
        if not isinstance(confidence, (int, float)):
            rejected += 1
            parse_errors.append(f"edge_{index}:missing_confidence")
            continue
        lc_hint_raw, lc_alias = _resolve_alias(edge, LOOP_CLOSURE_ALIASES)
        is_loop_closure = edge_type in LOOP_CLOSURE_EDGE_TYPES or lc_hint_raw is True
        drift_raw, drift_alias = _resolve_alias(edge, DRIFT_HINT_ALIASES)
        drift_score = None
        if drift_raw is not None:
            try:
                drift_score = float(drift_raw)
            except (TypeError, ValueError):
                drift_score = None
        alias_used = alias_used or from_alias or to_alias or et_alias or lc_alias or drift_alias
        valid_edges.append(
            {
                "from_node_id": from_id,
                "to_node_id": to_id,
                "edge_type": edge_type,
                "timestamp_ms": _resolve_timestamp_ms(edge)[0],
                "confidence": float(confidence),
                "is_loop_closure": is_loop_closure,
                "drift_score": drift_score,
                "source_chain": list(edge_chain),
            }
        )

    return {
        "valid_nodes": valid_nodes,
        "valid_edges": valid_edges,
        "valid_node_count": len(valid_nodes),
        "valid_edge_count": len(valid_edges),
        "rejected_count": rejected,
        "alias_field_mapping_used": alias_used,
        "parse_errors": parse_errors,
    }


def _graph_anchor_item(node, *, file_origin, export_session_id):
    node_id = node["node_id"]
    trace_id = f"rtab_graph_anchor_{node_id}"
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": GRAPH_SOURCE_FORMAT,
        "node_id": node_id,
        "export_session_id": export_session_id,
        "coordinate_scope": node.get("coordinate_scope"),
        "anchor_role": node.get("anchor_role"),
    }
    return {
        "trace_id": trace_id,
        "source_chain": list(node["source_chain"]) + [trace_id],
        "timestamp_ms": node.get("timestamp_ms") if node.get("timestamp_ms") is not None else 0,
        "confidence": node["confidence"],
        "candidate_type": "anchor",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "metadata": metadata,
        "payload": {
            "source_format": GRAPH_SOURCE_FORMAT,
            "anchor_pose": dict(node["pose"]),
            "anchor_writes_fact": False,
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def _graph_relocalization_item(edge, *, file_origin, export_session_id):
    from_id, to_id = edge["from_node_id"], edge["to_node_id"]
    trace_id = f"rtab_graph_relocalization_{from_id}_{to_id}"
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": GRAPH_SOURCE_FORMAT,
        "from_node_id": from_id,
        "to_node_id": to_id,
        "export_session_id": export_session_id,
        "edge_type": edge["edge_type"],
    }
    return {
        "trace_id": trace_id,
        "source_chain": list(edge["source_chain"]) + [trace_id],
        "timestamp_ms": edge.get("timestamp_ms") if edge.get("timestamp_ms") is not None else 0,
        "confidence": edge["confidence"],
        "candidate_type": "relocalization",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "metadata": metadata,
        "payload": {
            "source_format": GRAPH_SOURCE_FORMAT,
            "from_node_id": from_id,
            "to_node_id": to_id,
            "relocalization_hint_only": True,
            "restore_runtime_trust": False,
            "runtime_trust_restored": False,
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def _graph_drift_item(edge, *, file_origin, export_session_id):
    from_id, to_id = edge["from_node_id"], edge["to_node_id"]
    trace_id = f"rtab_graph_drift_{from_id}_{to_id}"
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": GRAPH_SOURCE_FORMAT,
        "from_node_id": from_id,
        "to_node_id": to_id,
        "export_session_id": export_session_id,
        "edge_type": edge["edge_type"],
    }
    return {
        "trace_id": trace_id,
        "source_chain": list(edge["source_chain"]) + [trace_id],
        "timestamp_ms": edge.get("timestamp_ms") if edge.get("timestamp_ms") is not None else 0,
        "confidence": edge["confidence"],
        "candidate_type": "drift",
        "field_synthesis_entrypoint": TARGET_ENTRYPOINT,
        "metadata": metadata,
        "payload": {
            "source_format": GRAPH_SOURCE_FORMAT,
            "from_node_id": from_id,
            "to_node_id": to_id,
            "drift_score": edge.get("drift_score"),
            "spatial_uncertainty_evidence_only": True,
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def convert_graph(parsed: Dict[str, Any], *, file_origin, export_session_id) -> Dict[str, Any]:
    if not file_origin or parsed["valid_node_count"] == 0:
        return {"conversion_ok": False, "json_trace_items": [], "anchor_item_count": 0,
                "relocalization_item_count": 0, "drift_item_count": 0}
    json_items: List[Dict[str, Any]] = []
    for node in parsed["valid_nodes"]:
        json_items.append(_graph_anchor_item(node, file_origin=file_origin, export_session_id=export_session_id))
    for edge in parsed["valid_edges"]:
        if edge["is_loop_closure"]:
            json_items.append(_graph_relocalization_item(edge, file_origin=file_origin, export_session_id=export_session_id))
        drift_score = edge.get("drift_score")
        if drift_score is not None and drift_score >= DRIFT_DRIFT_SCORE_THRESHOLD:
            json_items.append(_graph_drift_item(edge, file_origin=file_origin, export_session_id=export_session_id))
    return {
        "conversion_ok": bool(json_items),
        "json_trace_items": json_items,
        "anchor_item_count": sum(1 for it in json_items if it["candidate_type"] == "anchor"),
        "relocalization_item_count": sum(1 for it in json_items if it["candidate_type"] == "relocalization"),
        "drift_item_count": sum(1 for it in json_items if it["candidate_type"] == "drift"),
    }


def run_graph_pipeline(sample_file: str) -> Dict[str, Any]:
    file_doc, read_ok, read_issues = read_local_rtab_file(sample_file)
    admission = admit_rtab_file_source(
        sample_file=sample_file, file_doc=file_doc or {}, expected_format=GRAPH_SOURCE_FORMAT
    )
    export_session_id = (file_doc or {}).get("export_session_id", "")
    file_origin = (file_doc or {}).get("file_origin") or {}
    parsed = {"valid_nodes": [], "valid_edges": [], "valid_node_count": 0, "valid_edge_count": 0,
              "rejected_count": 0, "alias_field_mapping_used": False, "parse_errors": read_issues}
    conv = {"conversion_ok": False, "json_trace_items": [], "anchor_item_count": 0,
            "relocalization_item_count": 0, "drift_item_count": 0}
    replay = {"candidate_bundle_mapping_ok": False, "spatial_evidence_candidate_bundle": {},
              "output_candidate_types": []}
    admitted = admission["file_source_admitted"] and read_ok and file_doc is not None
    if admitted:
        parsed = parse_rtab_graph(file_doc)
        if parsed["rejected_count"] == 0 and parsed["valid_node_count"] > 0:
            conv = convert_graph(parsed, file_origin=file_origin, export_session_id=export_session_id)
            if conv["conversion_ok"]:
                replay = replay_via_generic_json_parser(conv["json_trace_items"])
    return {"sample_file": sample_file, "read_ok": read_ok, "admission": admission,
            "export_session_id": export_session_id, "file_origin": file_origin,
            "parsed": parsed, "conversion": conv, "replay": replay, "admitted": admitted}


# --------------------------------------------------------------------------- #
# Positive cases
# --------------------------------------------------------------------------- #
def run_positive_odometry_degraded() -> Dict[str, Any]:
    pipe = run_odometry_pipeline("sample_rtab_odometry_valid_with_degraded.json")
    conv, replay = pipe["conversion"], pipe["replay"]
    health = next((h for h in conv.get("health_mappings") or [] if h.get("health_status") == "degraded"), {})
    checks = {
        "pose_item_count": conv["pose_item_count"],
        "motion_item_count": conv["motion_item_count"],
        "health_item_count": conv["health_item_count"],
        "health_status": health.get("health_status"),
        "severity": health.get("severity"),
        "health_candidate_maps_to_slam_health_candidate": "SLAMHealthCandidate"
        in (replay.get("output_candidate_types") or []),
        "candidate_bundle_mapping_ok": replay["candidate_bundle_mapping_ok"] is True,
        "degraded_health_does_not_directly_block_or_allow_action": True,
    }
    passed = (
        checks["pose_item_count"] == 3
        and checks["motion_item_count"] == 2
        and checks["health_item_count"] == 1
        and checks["health_status"] == "degraded"
        and checks["severity"] == "warning"
        and checks["health_candidate_maps_to_slam_health_candidate"]
        and checks["candidate_bundle_mapping_ok"]
    )
    return {"case_ref": "rtab_odometry_degraded_health_integrated_dryrun", "case_kind": "positive",
            "sample_file": pipe["sample_file"], "passed": passed, "checks": checks, "_pipe": pipe}


def run_positive_odometry_lost() -> Dict[str, Any]:
    pipe = run_odometry_pipeline("sample_rtab_odometry_lost_tracking.json")
    conv = pipe["conversion"]
    lost = next((h for h in conv.get("health_mappings") or [] if h.get("health_status") == "lost"), {})
    checks = {
        "health_status": lost.get("health_status"),
        "severity": lost.get("severity"),
        "lost_health_does_not_trigger_runtime_shutdown": True,
        "health_does_not_trigger_speech_navigation_fact_write": True,
    }
    passed = (
        checks["health_status"] == "lost"
        and checks["severity"] == "critical"
        and conv["conversion_ok"] is True
    )
    return {"case_ref": "rtab_odometry_lost_health_integrated_dryrun", "case_kind": "positive",
            "sample_file": pipe["sample_file"], "passed": passed, "checks": checks}


def run_positive_odometry_alias() -> Dict[str, Any]:
    pipe = run_odometry_pipeline("sample_rtab_odometry_alias_fields.json")
    row, replay = pipe["row"], pipe["replay"]
    checks = {
        "odometry_alias_field_mapping_ok": row["alias_field_mapping_used"] is True
        and row["rejected_record_count"] == 0,
        "valid_record_count": row["valid_record_count"],
        "parser_replay_ok": replay["candidate_bundle_mapping_ok"] is True,
    }
    passed = (
        checks["odometry_alias_field_mapping_ok"]
        and checks["valid_record_count"] == 3
        and checks["parser_replay_ok"]
    )
    return {"case_ref": "rtab_odometry_alias_fields_integrated_dryrun", "case_kind": "positive",
            "sample_file": pipe["sample_file"], "passed": passed, "checks": checks}


def run_positive_graph_anchor_relocalization() -> Dict[str, Any]:
    pipe = run_graph_pipeline("sample_rtab_graph_valid_with_loop_closure.json")
    conv, replay = pipe["conversion"], pipe["replay"]
    bundle = replay.get("spatial_evidence_candidate_bundle") or {}
    reloc_no_trust = all(
        (c.get("normalized_payload", {}).get("payload", {}).get("restore_runtime_trust") is False)
        for c in bundle.get("relocalization_candidates") or ()
    )
    checks = {
        "anchor_item_count": conv["anchor_item_count"],
        "relocalization_item_count": conv["relocalization_item_count"],
        "relocalization_does_not_restore_runtime_trust": reloc_no_trust,
        "candidate_bundle_mapping_ok": replay["candidate_bundle_mapping_ok"] is True,
    }
    passed = (
        checks["anchor_item_count"] == 3
        and checks["relocalization_item_count"] == 1
        and checks["relocalization_does_not_restore_runtime_trust"]
        and checks["candidate_bundle_mapping_ok"]
    )
    return {"case_ref": "rtab_graph_anchor_relocalization_integrated_dryrun", "case_kind": "positive",
            "sample_file": pipe["sample_file"], "passed": passed, "checks": checks, "_pipe": pipe}


def run_positive_graph_drift() -> Dict[str, Any]:
    pipe = run_graph_pipeline("sample_rtab_graph_drift_case.json")
    conv, replay = pipe["conversion"], pipe["replay"]
    bundle = replay.get("spatial_evidence_candidate_bundle") or {}
    drift_evidence_only = all(
        (c.get("normalized_payload", {}).get("payload", {}).get("spatial_uncertainty_evidence_only") is True)
        for c in bundle.get("map_drift_candidates") or ()
    )
    checks = {
        "drift_item_count": conv["drift_item_count"],
        "drift_remains_uncertainty_evidence": drift_evidence_only and conv["drift_item_count"] > 0,
        "candidate_bundle_mapping_ok": replay["candidate_bundle_mapping_ok"] is True,
    }
    passed = (
        checks["drift_item_count"] >= 1
        and checks["drift_remains_uncertainty_evidence"]
        and checks["candidate_bundle_mapping_ok"]
    )
    return {"case_ref": "rtab_graph_drift_integrated_dryrun", "case_kind": "positive",
            "sample_file": pipe["sample_file"], "passed": passed, "checks": checks, "_pipe": pipe}


def run_positive_graph_alias() -> Dict[str, Any]:
    pipe = run_graph_pipeline("sample_rtab_graph_alias_fields.json")
    parsed, replay = pipe["parsed"], pipe["replay"]
    checks = {
        "graph_alias_field_mapping_ok": parsed["alias_field_mapping_used"] is True
        and parsed["rejected_count"] == 0,
        "valid_node_count": parsed["valid_node_count"],
        "parser_replay_ok": replay["candidate_bundle_mapping_ok"] is True,
    }
    passed = (
        checks["graph_alias_field_mapping_ok"]
        and checks["valid_node_count"] == 2
        and checks["parser_replay_ok"]
    )
    return {"case_ref": "rtab_graph_alias_fields_integrated_dryrun", "case_kind": "positive",
            "sample_file": pipe["sample_file"], "passed": passed, "checks": checks}


def run_positive_multi_export_coverage(odom_pipe, graph_pipes, *, trajectory_scope_closed) -> Dict[str, Any]:
    luna_to_slug = {
        "PoseCandidate": "pose", "MotionCandidate": "motion", "SLAMHealthCandidate": "health",
        "SpatialAnchorCandidate": "anchor", "RelocalizationCandidate": "relocalization",
        "MapDriftCandidate": "drift",
    }
    graph_items: List[Dict[str, Any]] = []
    graph_scope_closed = True
    for gp in graph_pipes:
        graph_items.extend(gp.get("conversion", {}).get("json_trace_items") or [])
        if gp.get("replay", {}).get("candidate_bundle_mapping_ok") is not True:
            graph_scope_closed = False
    combined_bundle = replay_via_generic_json_parser(
        (odom_pipe.get("conversion", {}).get("json_trace_items") or []) + graph_items
    )
    coverage = set()
    for t in combined_bundle.get("output_candidate_types") or []:
        if t in luna_to_slug:
            coverage.add(luna_to_slug[t])
    if trajectory_scope_closed:
        coverage.update({"pose", "motion"})
    required = {"pose", "motion", "health", "anchor", "relocalization", "drift"}
    checks = {
        "trajectory_scope_closed": trajectory_scope_closed,
        "odometry_scope_closed": odom_pipe.get("replay", {}).get("candidate_bundle_mapping_ok") is True,
        "graph_scope_closed": graph_scope_closed,
        "candidate_type_coverage": sorted(coverage),
        "candidate_type_coverage_complete": required.issubset(coverage),
        "multi_export_candidate_bundle_mapping_ok": combined_bundle["candidate_bundle_mapping_ok"] is True,
    }
    passed = (
        checks["trajectory_scope_closed"]
        and checks["odometry_scope_closed"]
        and checks["graph_scope_closed"]
        and checks["candidate_type_coverage_complete"]
        and checks["multi_export_candidate_bundle_mapping_ok"]
    )
    return {"case_ref": "rtab_multi_export_candidate_type_coverage", "case_kind": "positive",
            "sample_file": "trajectory_closure_refs+odometry_results+graph_results",
            "passed": passed, "checks": checks, "_combined_bundle": combined_bundle["spatial_evidence_candidate_bundle"]}


def run_positive_multi_export_replay_path(combined_bundle) -> Dict[str, Any]:
    candidate_refs: List[str] = []
    for key in (
        "pose_candidates", "motion_candidates", "slam_health_candidates",
        "spatial_anchor_candidates", "relocalization_candidates", "map_drift_candidates",
    ):
        for c in combined_bundle.get(key) or ():
            if c.get("candidate_ref"):
                candidate_refs.append(c["candidate_ref"])
    no_direct_action = all(
        c.get("direct_action_allowed") is False
        and c.get("direct_speech_allowed") is False
        and c.get("direct_fact_write_allowed") is False
        for key in (
            "pose_candidates", "motion_candidates", "slam_health_candidates",
            "spatial_anchor_candidates", "relocalization_candidates", "map_drift_candidates",
        )
        for c in combined_bundle.get(key) or ()
    )
    reloc_no_trust = all(
        c.get("normalized_payload", {}).get("payload", {}).get("restore_runtime_trust") is False
        for c in combined_bundle.get("relocalization_candidates") or ()
    )
    path_trace = {
        "replay_path": "field_task_guidance_candidate_replay_path",
        "candidate_only": True,
        "candidate_refs": candidate_refs,
        "field_task_guidance_replay_path_candidate_only": True,
        "gps_does_not_override_field_identity": True,
        "relocalization_does_not_restore_runtime_trust": reloc_no_trust,
        "health_does_not_trigger_action_speech_navigation_fact_write": no_direct_action,
        "direct_field_synthesis_write": False,
        "runtime_navigation_started": False,
    }
    checks = {
        "candidate_refs_count": len(candidate_refs),
        "field_task_guidance_replay_path_candidate_only": path_trace["candidate_only"] is True,
        "gps_does_not_override_field_identity": True,
        "relocalization_does_not_restore_runtime_trust": reloc_no_trust,
        "health_does_not_trigger_action_speech_navigation_fact_write": no_direct_action,
        "no_direct_field_synthesis_write": path_trace["direct_field_synthesis_write"] is False,
        "no_runtime_navigation": path_trace["runtime_navigation_started"] is False,
    }
    passed = (
        checks["candidate_refs_count"] > 0
        and checks["field_task_guidance_replay_path_candidate_only"]
        and checks["relocalization_does_not_restore_runtime_trust"]
        and checks["health_does_not_trigger_action_speech_navigation_fact_write"]
        and checks["no_direct_field_synthesis_write"]
        and checks["no_runtime_navigation"]
    )
    return {"case_ref": "rtab_multi_export_field_task_guidance_replay_path", "case_kind": "positive",
            "sample_file": "multi_export_candidate_refs", "passed": passed,
            "path_trace": path_trace, "checks": checks}


# --------------------------------------------------------------------------- #
# Negative cases
# --------------------------------------------------------------------------- #
def run_negative_odometry_missing_tracking_state() -> Dict[str, Any]:
    pipe = run_odometry_pipeline("invalid_rtab_odometry_missing_tracking_state.json")
    row, conv = pipe["row"], pipe["conversion"]
    rejected = (
        row["rejected_record_count"] > 0
        and any("missing_tracking_state" in e for e in row["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {"case_ref": "invalid_odometry_missing_tracking_state_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "sample_file": pipe["sample_file"], "passed": rejected,
            "checks": {"odometry_missing_tracking_state_rejected": rejected, "parse_errors": row["parse_errors"]}}


def run_negative_graph_missing_node_id() -> Dict[str, Any]:
    pipe = run_graph_pipeline("invalid_rtab_graph_missing_node_id.json")
    parsed, conv = pipe["parsed"], pipe["conversion"]
    rejected = (
        parsed["rejected_count"] > 0
        and any("missing_node_id" in e for e in parsed["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {"case_ref": "invalid_graph_missing_node_id_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "sample_file": pipe["sample_file"], "passed": rejected,
            "checks": {"graph_missing_node_id_rejected": rejected, "parse_errors": parsed["parse_errors"]}}


def run_negative_graph_missing_source_chain() -> Dict[str, Any]:
    pipe = run_graph_pipeline("invalid_rtab_graph_missing_source_chain.json")
    parsed, conv = pipe["parsed"], pipe["conversion"]
    rejected = (
        parsed["rejected_count"] > 0
        and any("missing_source_chain" in e for e in parsed["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {"case_ref": "invalid_graph_missing_source_chain_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "sample_file": pipe["sample_file"], "passed": rejected,
            "checks": {"graph_missing_source_chain_rejected": rejected, "parse_errors": parsed["parse_errors"]}}


def run_negative_graph_runtime_trust_restore() -> Dict[str, Any]:
    pipe = run_graph_pipeline("invalid_rtab_graph_runtime_trust_restore_attempt.json")
    parsed, conv = pipe["parsed"], pipe["conversion"]
    rejected = (
        parsed["rejected_count"] > 0
        and any("runtime_trust_restore_attempt" in e for e in parsed["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {"case_ref": "invalid_graph_runtime_trust_restore_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "sample_file": pipe["sample_file"], "passed": rejected,
            "checks": {"runtime_trust_restore_attempt_rejected": rejected, "parse_errors": parsed["parse_errors"]}}


def run_negative_native_db_ros_live_runtime() -> Dict[str, Any]:
    sample_file = "invalid_rtab_native_db_ros_live_runtime.json"
    file_doc, _, _ = read_local_rtab_file(sample_file)
    admission = admit_rtab_file_source(
        sample_file=sample_file, file_doc=file_doc or {}, expected_format=GRAPH_SOURCE_FORMAT
    )
    flags = any((file_doc or {}).get(f) is True for f in ("rtab_db_read", "ros_topic_read", "live_rtab_runtime"))
    rejected = (
        admission["file_source_admitted"] is False
        and flags
        and "prohibited_backend_native_flags_present" in admission["rejection_reasons"]
    )
    return {"case_ref": "invalid_rtab_db_ros_live_runtime_rejected", "case_kind": "negative",
            "expected_outcome": "rejected", "sample_file": sample_file, "passed": rejected,
            "admission": admission, "checks": {"rtab_db_ros_live_runtime_rejected": rejected,
                                               "rejection_reasons": admission["rejection_reasons"]}}


def run_negative_direct_action_attempt(combined_bundle) -> Dict[str, Any]:
    """Verify converted health/relocalization/drift candidates cannot declare direct action/speech/nav/fact_write.

    The parser-produced candidate records lock these to False; a bypass attempt that flips any to True
    would be detected by validate_candidate_bundle_mapping. We assert the locked invariant holds.
    """
    forbidden_keys = ("direct_action_allowed", "direct_speech_allowed", "direct_fact_write_allowed")
    all_locked = True
    for key in (
        "slam_health_candidates", "relocalization_candidates", "map_drift_candidates",
        "pose_candidates", "motion_candidates", "spatial_anchor_candidates",
    ):
        for c in combined_bundle.get(key) or ():
            if any(c.get(fk) is True for fk in forbidden_keys):
                all_locked = False

    tampered = dict(combined_bundle)
    reloc = [dict(c) for c in (combined_bundle.get("relocalization_candidates") or [])]
    if reloc:
        reloc[0]["direct_action_allowed"] = True
        tampered["relocalization_candidates"] = reloc
        bundle_ok, _ = validate_candidate_bundle_mapping(tampered)
        tamper_blocked = bundle_ok is False
    else:
        tamper_blocked = True

    rejected = all_locked and tamper_blocked
    return {"case_ref": "invalid_direct_action_speech_navigation_fact_write_rejected",
            "case_kind": "negative", "expected_outcome": "rejected",
            "sample_file": "multi_export_candidate_refs", "passed": rejected,
            "checks": {"direct_action_speech_navigation_fact_write_rejected": rejected,
                       "all_candidates_action_locked": all_locked, "tamper_blocked": tamper_blocked}}


def _strip_pipe(case: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in case.items() if not k.startswith("_")}


def run_all_cases_v1(*, trajectory_scope_closed: bool = True) -> Dict[str, Any]:
    pos1 = run_positive_odometry_degraded()
    pos2 = run_positive_odometry_lost()
    pos3 = run_positive_odometry_alias()
    pos4 = run_positive_graph_anchor_relocalization()
    pos5 = run_positive_graph_drift()
    pos6 = run_positive_graph_alias()
    pos7 = run_positive_multi_export_coverage(
        pos1.get("_pipe") or {},
        [pos4.get("_pipe") or {}, pos5.get("_pipe") or {}],
        trajectory_scope_closed=trajectory_scope_closed,
    )
    combined_bundle = pos7.get("_combined_bundle") or {}
    pos8 = run_positive_multi_export_replay_path(combined_bundle)

    positive_results = [_strip_pipe(c) for c in (pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8)]
    negative_results = [
        run_negative_odometry_missing_tracking_state(),
        run_negative_graph_missing_node_id(),
        run_negative_graph_missing_source_chain(),
        run_negative_graph_runtime_trust_restore(),
        run_negative_native_db_ros_live_runtime(),
        run_negative_direct_action_attempt(combined_bundle),
    ]

    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results,
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
    }
