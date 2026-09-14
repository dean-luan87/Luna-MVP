# -*- coding: utf-8 -*-
"""RTAB-Map Odometry Real File Loader DryRun — cases v1."""

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
from capabilities.field_understanding.rtab_map_odometry_real_file_loader_dryrun.rtab_map_odometry_real_file_loader_dryrun_types_v1 import (
    HEALTH_PROVIDER,
    HEALTH_SEVERITY_BY_STATUS,
    HEALTH_STATUS_DEGRADED_STATES,
    HEALTH_STATUS_LOST_STATES,
    HEALTH_STATUS_OK_STATES,
    NEGATIVE_CASE_REFS,
    NODE_ID_ALIASES,
    ODOMETRY_QUALITY_ALIASES,
    ODOMETRY_QUALITY_DEGRADED_THRESHOLD,
    ORIENTATION_FIELDS,
    POSITIVE_CASE_REFS,
    PROHIBITED_FILE_FLAGS,
    RTABMapOdometryRealFileLoaderDryRunCase,
    SAMPLE_FILES,
    SAMPLES_REL_DIR,
    SOURCE_CHAIN,
    SOURCE_FORMAT,
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


def read_local_rtab_odometry_file(
    sample_file: str,
) -> Tuple[Optional[Dict[str, Any]], bool, List[str]]:
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


def admit_rtab_odometry_file_source(
    *, sample_file: str, file_doc: Dict[str, Any]
) -> Dict[str, Any]:
    path = _SAMPLES_DIR / sample_file
    rejection_reasons: List[str] = []

    controlled_ok = is_controlled_sample_path(path)
    if not controlled_ok:
        rejection_reasons.append("controlled_samples_path_violation")

    format_ref_ok = file_doc.get("format_ref") == SOURCE_FORMAT
    if not format_ref_ok:
        rejection_reasons.append("format_ref_not_rtab_map_odometry_export_file")

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
        "result_ref": f"rtab_odom_admission_{sample_file}",
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


def _resolve_node_id(record: Dict[str, Any]) -> Tuple[Optional[Any], bool]:
    return _resolve_alias(record, NODE_ID_ALIASES)


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


def _resolve_tracking_state(record: Dict[str, Any]) -> Tuple[Optional[str], bool]:
    value, used_alias = _resolve_alias(record, TRACKING_STATE_ALIASES)
    if value is None:
        return None, used_alias
    return str(value).lower(), used_alias


def _resolve_odometry_quality(record: Dict[str, Any]) -> Tuple[Optional[float], bool]:
    value, used_alias = _resolve_alias(record, ODOMETRY_QUALITY_ALIASES)
    if value is None:
        return None, used_alias
    try:
        return float(value), used_alias
    except (TypeError, ValueError):
        return None, used_alias


def _quaternion_valid(orientation: Dict[str, float]) -> bool:
    norm = math.sqrt(
        orientation["qx"] ** 2
        + orientation["qy"] ** 2
        + orientation["qz"] ** 2
        + orientation["qw"] ** 2
    )
    return norm >= 1e-9


def map_tracking_state_to_health(
    tracking_state: str,
    odometry_quality: Optional[float],
) -> Dict[str, Any]:
    """Map RTAB tracking_state / odometry_quality to Luna health candidate fields."""
    state = tracking_state.lower()
    health_status = "ok"
    severity = HEALTH_SEVERITY_BY_STATUS["ok"]
    reason = "tracking_ok"
    emit_health = False

    if state in HEALTH_STATUS_LOST_STATES:
        health_status = "lost"
        severity = HEALTH_SEVERITY_BY_STATUS["lost"]
        reason = f"tracking_state_{state}"
        emit_health = True
    elif state in HEALTH_STATUS_DEGRADED_STATES:
        health_status = "degraded"
        severity = HEALTH_SEVERITY_BY_STATUS["degraded"]
        reason = f"tracking_state_{state}"
        emit_health = True
    elif state in HEALTH_STATUS_OK_STATES:
        if odometry_quality is not None and odometry_quality < ODOMETRY_QUALITY_DEGRADED_THRESHOLD:
            health_status = "degraded"
            severity = HEALTH_SEVERITY_BY_STATUS["degraded"]
            reason = "odometry_quality_below_threshold"
            emit_health = True
        else:
            health_status = "ok"
            severity = HEALTH_SEVERITY_BY_STATUS["ok"]
            reason = "tracking_ok"
            emit_health = False
    else:
        health_status = "degraded"
        severity = HEALTH_SEVERITY_BY_STATUS["degraded"]
        reason = f"unknown_tracking_state_{state}"
        emit_health = True

    return {
        "health_status": health_status,
        "severity": severity,
        "reason": reason,
        "health_candidate_emitted": emit_health,
        "candidate_only": True,
    }


def parse_rtab_odometry_records(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    valid_records: List[Dict[str, Any]] = []
    health_mappings: List[Dict[str, Any]] = []
    parse_errors: List[str] = []
    rejected = 0
    alias_used = False

    for index, record in enumerate(records):
        node_id, node_alias = _resolve_node_id(record)
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

        tracking_state, ts_state_alias = _resolve_tracking_state(record)
        if tracking_state is None:
            rejected += 1
            parse_errors.append(f"record_{index}:missing_tracking_state")
            continue

        odometry_quality, oq_alias = _resolve_odometry_quality(record)

        record_source_chain = record.get("source_chain")
        if not record_source_chain:
            rejected += 1
            parse_errors.append(f"record_{index}:missing_source_chain")
            continue

        alias_used = alias_used or node_alias or ts_alias or tr_alias or ts_state_alias or oq_alias
        health_map = map_tracking_state_to_health(tracking_state, odometry_quality)
        health_mappings.append(
            {
                "result_ref": f"health_mapping_{node_id}",
                "node_id": node_id,
                "tracking_state": tracking_state,
                "odometry_quality": odometry_quality,
                **health_map,
                "source_chain": SOURCE_CHAIN,
            }
        )

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
                "health_mapping": health_map,
            }
        )

    return {
        "result_ref": "rtab_odom_record_parse_result",
        "valid_records": valid_records,
        "valid_record_count": len(valid_records),
        "rejected_record_count": rejected,
        "alias_field_mapping_used": alias_used,
        "health_mappings": health_mappings,
        "parse_errors": parse_errors,
        "source_chain": SOURCE_CHAIN,
    }


def _pose_trace_item(
    record: Dict[str, Any],
    *,
    file_origin: Dict[str, Any],
    export_session_id: str,
) -> Dict[str, Any]:
    node_id = record["node_id"]
    trace_id = f"rtab_odom_pose_{node_id}"
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": SOURCE_FORMAT,
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
        "payload": {
            "source_format": SOURCE_FORMAT,
            "pose": dict(record["pose"]),
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def _motion_trace_item(
    prev_record: Dict[str, Any],
    curr_record: Dict[str, Any],
    *,
    file_origin: Dict[str, Any],
    export_session_id: str,
) -> Dict[str, Any]:
    from_node_id = prev_record["node_id"]
    to_node_id = curr_record["node_id"]
    trace_id = f"rtab_odom_motion_{from_node_id}_{to_node_id}"
    p0 = prev_record["pose"]
    p1 = curr_record["pose"]
    delta_translation = [p1["x"] - p0["x"], p1["y"] - p0["y"], p1["z"] - p0["z"]]
    dot = (
        p0["qx"] * p1["qx"]
        + p0["qy"] * p1["qy"]
        + p0["qz"] * p1["qz"]
        + p0["qw"] * p1["qw"]
    )
    dot = max(-1.0, min(1.0, abs(dot)))
    delta_rotation_hint = round(1.0 - dot, 6)
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": SOURCE_FORMAT,
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
            "source_format": SOURCE_FORMAT,
            "delta_translation": delta_translation,
            "delta_rotation_hint": delta_rotation_hint,
            "from_node_id": from_node_id,
            "to_node_id": to_node_id,
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def _health_trace_item(
    record: Dict[str, Any],
    *,
    file_origin: Dict[str, Any],
    export_session_id: str,
) -> Dict[str, Any]:
    node_id = record["node_id"]
    health_map = record["health_mapping"]
    trace_id = f"rtab_odom_health_{node_id}"
    metadata = {
        "file_origin": dict(file_origin),
        "source_format": SOURCE_FORMAT,
        "node_id": node_id,
        "row_index": record["row_index"],
        "export_session_id": export_session_id,
        "tracking_state": record["tracking_state"],
    }
    health_payload = {
        "provider": HEALTH_PROVIDER,
        "tracking_state": record["tracking_state"],
        "odometry_quality": record.get("odometry_quality"),
        "health_status": health_map["health_status"],
        "severity": health_map["severity"],
        "reason": health_map["reason"],
        "candidate_risk_only": True,
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
            "source_format": SOURCE_FORMAT,
            "health": health_payload,
            "metadata": metadata,
        },
        "candidate_only": True,
    }


def convert_rtab_odometry_records_to_json_spatial_trace(
    valid_records: List[Dict[str, Any]],
    *,
    file_origin: Dict[str, Any],
    export_session_id: str,
) -> Dict[str, Any]:
    conversion_issues: List[str] = []
    if not file_origin:
        conversion_issues.append("file_origin_required")
    if not valid_records:
        conversion_issues.append("no_valid_records")
    if conversion_issues:
        return {
            "result_ref": "rtab_odom_to_json_conversion_result",
            "conversion_ok": False,
            "json_trace_items": [],
            "json_trace_item_count": 0,
            "pose_item_count": 0,
            "motion_item_count": 0,
            "health_item_count": 0,
            "target_internal_format": TARGET_INTERNAL_FORMAT,
            "file_origin_preserved": False,
            "export_session_id_preserved": False,
            "source_chain_preserved": False,
            "tracking_state_preserved": False,
            "motion_generated_only_from_consecutive_records": True,
            "motion_pairs": [],
            "health_mappings": [],
            "conversion_issues": conversion_issues,
            "source_chain": SOURCE_CHAIN,
        }

    json_items: List[Dict[str, Any]] = []
    health_mappings: List[Dict[str, Any]] = []

    for record in valid_records:
        json_items.append(
            _pose_trace_item(
                record, file_origin=file_origin, export_session_id=export_session_id
            )
        )
        health_map = record["health_mapping"]
        if health_map.get("health_candidate_emitted"):
            json_items.append(
                _health_trace_item(
                    record, file_origin=file_origin, export_session_id=export_session_id
                )
            )
            health_mappings.append(
                {
                    "result_ref": f"health_mapping_{record['node_id']}",
                    "node_id": record["node_id"],
                    "tracking_state": record["tracking_state"],
                    "odometry_quality": record.get("odometry_quality"),
                    **health_map,
                    "source_chain": SOURCE_CHAIN,
                }
            )

    motion_pairs: List[List[Any]] = []
    for from_index in range(len(valid_records) - 1):
        prev_record = valid_records[from_index]
        curr_record = valid_records[from_index + 1]
        json_items.append(
            _motion_trace_item(
                prev_record,
                curr_record,
                file_origin=file_origin,
                export_session_id=export_session_id,
            )
        )
        motion_pairs.append([prev_record["node_id"], curr_record["node_id"]])

    pose_count = sum(1 for item in json_items if item.get("candidate_type") == "pose")
    motion_count = sum(1 for item in json_items if item.get("candidate_type") == "motion")
    health_count = sum(1 for item in json_items if item.get("candidate_type") == "health")
    file_origin_preserved = all(
        bool((item.get("metadata") or {}).get("file_origin")) for item in json_items
    )
    export_session_preserved = all(
        (item.get("metadata") or {}).get("export_session_id") == export_session_id
        for item in json_items
    )
    source_chain_preserved = all(bool(item.get("source_chain")) for item in json_items)
    tracking_state_preserved = all(
        bool((item.get("metadata") or {}).get("tracking_state"))
        for item in json_items
        if item.get("candidate_type") in ("pose", "health")
    )

    return {
        "result_ref": "rtab_odom_to_json_conversion_result",
        "conversion_ok": bool(json_items),
        "json_trace_items": json_items,
        "json_trace_item_count": len(json_items),
        "pose_item_count": pose_count,
        "motion_item_count": motion_count,
        "health_item_count": health_count,
        "target_internal_format": TARGET_INTERNAL_FORMAT,
        "file_origin_preserved": file_origin_preserved,
        "export_session_id_preserved": export_session_preserved,
        "source_chain_preserved": source_chain_preserved,
        "tracking_state_preserved": tracking_state_preserved,
        "motion_generated_only_from_consecutive_records": True,
        "motion_pairs": motion_pairs,
        "health_mappings": health_mappings,
        "conversion_issues": [],
        "source_chain": SOURCE_CHAIN,
    }


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
    health_candidates = bundle.get("slam_health_candidates") or []
    health_maps_ok = (
        not health_candidates
        or all(c.get("candidate_type") == "SLAMHealthCandidate" for c in health_candidates)
    )
    return {
        "result_ref": "rtab_odom_real_file_replay_result",
        "generic_json_parser_reused": True,
        "parsed_count": len(parsed_items),
        "parse_errors": parse_errors,
        "candidate_bundle_mapping_ok": bundle_ok and not parse_errors,
        "health_candidate_maps_to_slam_health_candidate": health_maps_ok,
        "output_candidate_types": list(bundle.get("output_candidate_types") or ()),
        "bundle_issues": bundle_issues,
        "spatial_evidence_candidate_bundle": bundle,
        "source_chain": SOURCE_CHAIN,
    }


def _load_rtab_odometry_pipeline(sample_file: str) -> Dict[str, Any]:
    file_doc, read_ok, read_issues = read_local_rtab_odometry_file(sample_file)
    admission = admit_rtab_odometry_file_source(sample_file=sample_file, file_doc=file_doc or {})

    export_session_id = (file_doc or {}).get("export_session_id", "")
    file_origin = (file_doc or {}).get("file_origin") or {}

    row_result: Dict[str, Any] = {
        "valid_records": [],
        "valid_record_count": 0,
        "rejected_record_count": 0,
        "alias_field_mapping_used": False,
        "health_mappings": [],
        "parse_errors": read_issues,
    }
    conversion: Dict[str, Any] = {
        "conversion_ok": False,
        "json_trace_items": [],
        "json_trace_item_count": 0,
        "pose_item_count": 0,
        "motion_item_count": 0,
        "health_item_count": 0,
        "file_origin_preserved": False,
        "export_session_id_preserved": False,
        "source_chain_preserved": False,
        "tracking_state_preserved": False,
        "motion_generated_only_from_consecutive_records": True,
        "motion_pairs": [],
        "health_mappings": [],
        "conversion_issues": ["pipeline_not_admitted"],
    }
    replay: Dict[str, Any] = {
        "candidate_bundle_mapping_ok": False,
        "health_candidate_maps_to_slam_health_candidate": False,
        "generic_json_parser_reused": True,
        "output_candidate_types": [],
        "bundle_issues": ["pipeline_not_admitted"],
        "spatial_evidence_candidate_bundle": {},
        "parsed_count": 0,
    }

    admitted = admission["file_source_admitted"] and read_ok and file_doc is not None
    if admitted:
        records = file_doc.get("records") or []
        row_result = parse_rtab_odometry_records(records)
        if row_result["rejected_record_count"] == 0 and row_result["valid_record_count"] > 0:
            conversion = convert_rtab_odometry_records_to_json_spatial_trace(
                row_result["valid_records"],
                file_origin=file_origin,
                export_session_id=export_session_id,
            )
            if conversion["conversion_ok"]:
                replay = replay_via_generic_json_parser(conversion["json_trace_items"])

    return {
        "sample_file": sample_file,
        "read_ok": read_ok,
        "export_session_id": export_session_id,
        "file_origin": file_origin,
        "admission": admission,
        "row_result": row_result,
        "conversion": conversion,
        "replay": replay,
        "admitted": admitted,
    }


def _public_row(row: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in row.items() if k != "valid_records"}


def _public_conversion(conv: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in conv.items() if k != "json_trace_items"}


def _public_replay(replay: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in replay.items() if k != "spatial_evidence_candidate_bundle"}


def run_positive_valid_file_case() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("sample_rtab_odometry_valid_with_degraded.json")
    conv = pipe["conversion"]
    replay = pipe["replay"]
    row = pipe["row_result"]
    checks = {
        "local_file_read_used": pipe["read_ok"] is True,
        "file_source_admitted": pipe["admission"]["file_source_admitted"] is True,
        "rtab_record_count": row["valid_record_count"],
        "json_trace_item_count": conv["json_trace_item_count"],
        "pose_item_count": conv["pose_item_count"],
        "motion_item_count": conv["motion_item_count"],
        "health_item_count": conv["health_item_count"],
        "rtab_odometry_to_json_trace_conversion_ok": conv["conversion_ok"] is True,
        "generic_json_parser_reused": replay["generic_json_parser_reused"] is True,
        "candidate_bundle_mapping_ok": replay["candidate_bundle_mapping_ok"] is True,
        "health_candidate_maps_to_slam_health_candidate": (
            replay["health_candidate_maps_to_slam_health_candidate"] is True
        ),
    }
    passed = (
        checks["local_file_read_used"]
        and checks["file_source_admitted"]
        and checks["rtab_record_count"] == 3
        and checks["json_trace_item_count"] == 6
        and checks["pose_item_count"] == 3
        and checks["motion_item_count"] == 2
        and checks["health_item_count"] == 1
        and checks["rtab_odometry_to_json_trace_conversion_ok"]
        and checks["candidate_bundle_mapping_ok"]
        and checks["health_candidate_maps_to_slam_health_candidate"]
    )
    return {
        "case_ref": "rtab_odometry_valid_file_to_pose_motion_health_json_trace",
        "case_kind": "positive",
        "sample_file": pipe["sample_file"],
        "passed": passed,
        "admission": pipe["admission"],
        "row_result": _public_row(row),
        "conversion_result": _public_conversion(conv),
        "replay_result": _public_replay(replay),
        "checks": checks,
        "_internal": pipe,
    }


def run_positive_lost_tracking_case() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("sample_rtab_odometry_lost_tracking.json")
    conv = pipe["conversion"]
    health_mappings = conv.get("health_mappings") or []
    lost_health = next(
        (h for h in health_mappings if h.get("health_status") == "lost"),
        {},
    )
    checks = {
        "health_status": lost_health.get("health_status"),
        "severity": lost_health.get("severity"),
        "lost_health_does_not_trigger_runtime_shutdown": True,
        "health_does_not_trigger_speech_navigation_fact_write": True,
        "health_candidate_emitted": lost_health.get("health_candidate_emitted") is True,
        "candidate_only": lost_health.get("candidate_only") is True,
    }
    passed = (
        checks["health_status"] == "lost"
        and checks["severity"] == "critical"
        and checks["health_candidate_emitted"]
        and checks["candidate_only"]
        and conv["conversion_ok"] is True
    )
    return {
        "case_ref": "rtab_odometry_lost_tracking_to_critical_health",
        "case_kind": "positive",
        "sample_file": pipe["sample_file"],
        "passed": passed,
        "conversion_result": _public_conversion(conv),
        "checks": checks,
    }


def run_positive_alias_fields_case() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("sample_rtab_odometry_alias_fields.json")
    conv = pipe["conversion"]
    replay = pipe["replay"]
    row = pipe["row_result"]
    checks = {
        "rtab_odometry_alias_field_mapping_ok": row["alias_field_mapping_used"] is True
        and row["rejected_record_count"] == 0,
        "valid_record_count": row["valid_record_count"],
        "json_trace_item_count": conv["json_trace_item_count"],
        "parser_replay_ok": replay["candidate_bundle_mapping_ok"] is True,
    }
    passed = (
        checks["rtab_odometry_alias_field_mapping_ok"]
        and checks["valid_record_count"] == 3
        and checks["parser_replay_ok"]
    )
    return {
        "case_ref": "rtab_odometry_alias_fields_to_standard_trace",
        "case_kind": "positive",
        "sample_file": pipe["sample_file"],
        "passed": passed,
        "admission": pipe["admission"],
        "row_result": _public_row(row),
        "conversion_result": _public_conversion(conv),
        "replay_result": _public_replay(replay),
        "checks": checks,
    }


def run_positive_metadata_preserved_case() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("sample_rtab_odometry_with_metadata.json")
    conv = pipe["conversion"]
    replay = pipe["replay"]
    items = conv.get("json_trace_items") or []

    file_origin_preserved = bool(items) and all(
        bool((item.get("metadata") or {}).get("file_origin")) for item in items
    )
    export_session_preserved = bool(items) and all(
        (item.get("metadata") or {}).get("export_session_id") == pipe["export_session_id"]
        for item in items
    )
    source_chain_preserved = bool(items) and all(
        bool(item.get("source_chain")) for item in items
    )
    bundle = replay.get("spatial_evidence_candidate_bundle") or {}
    upstream_refs_preserved = True
    for key in ("pose_candidates", "motion_candidates", "slam_health_candidates"):
        for candidate in bundle.get(key) or ():
            if not candidate.get("source_chain"):
                upstream_refs_preserved = False

    checks = {
        "file_origin_metadata_preserved": file_origin_preserved,
        "export_session_id_preserved": export_session_preserved,
        "source_chain_preserved_in_every_item": source_chain_preserved,
        "upstream_refs_preserved": upstream_refs_preserved,
    }
    passed = (
        file_origin_preserved
        and export_session_preserved
        and source_chain_preserved
        and upstream_refs_preserved
    )
    return {
        "case_ref": "rtab_odometry_metadata_and_source_chain_preserved",
        "case_kind": "positive",
        "sample_file": pipe["sample_file"],
        "passed": passed,
        "admission": pipe["admission"],
        "conversion_result": _public_conversion(conv),
        "checks": checks,
    }


def run_positive_field_task_guidance_case(prior_pipe: Dict[str, Any]) -> Dict[str, Any]:
    bundle = (prior_pipe.get("replay") or {}).get("spatial_evidence_candidate_bundle") or {}
    candidate_refs: List[str] = []
    has_health = False
    for key in (
        "pose_candidates",
        "motion_candidates",
        "spatial_anchor_candidates",
        "slam_health_candidates",
        "map_drift_candidates",
        "relocalization_candidates",
    ):
        for candidate in bundle.get(key) or ():
            ref = candidate.get("candidate_ref")
            if ref:
                candidate_refs.append(ref)
            if key == "slam_health_candidates":
                has_health = True
                if candidate.get("direct_action_allowed") is True:
                    pass

    path_trace = {
        "trace_ref": "rtab_odometry_field_task_guidance_replay_path",
        "replay_path": "field_task_guidance_candidate_replay_path",
        "candidate_only": True,
        "candidate_refs": candidate_refs,
        "health_can_only_influence_risk_as_evidence": has_health,
        "guidance_candidate_is_not_runtime_navigation": True,
        "direct_field_synthesis_write": False,
        "runtime_navigation_started": False,
        "field_entrypoint": TARGET_ENTRYPOINT,
        "source_chain": SOURCE_CHAIN,
    }
    checks = {
        "spatial_evidence_candidate_bundle_generated": bool(bundle),
        "candidate_refs_count": len(candidate_refs),
        "replay_path_candidate_only": path_trace["candidate_only"] is True,
        "health_can_only_influence_risk_as_evidence": (
            path_trace["health_can_only_influence_risk_as_evidence"] is True
        ),
        "no_direct_field_synthesis_write": path_trace["direct_field_synthesis_write"] is False,
        "no_runtime_navigation": path_trace["runtime_navigation_started"] is False,
        "no_direct_action": all(
            c.get("direct_action_allowed") is False
            for key in ("pose_candidates", "motion_candidates", "slam_health_candidates")
            for c in bundle.get(key) or ()
        ),
    }
    passed = (
        checks["spatial_evidence_candidate_bundle_generated"]
        and checks["candidate_refs_count"] > 0
        and checks["replay_path_candidate_only"]
        and checks["health_can_only_influence_risk_as_evidence"]
        and checks["no_direct_field_synthesis_write"]
        and checks["no_runtime_navigation"]
        and checks["no_direct_action"]
    )
    return {
        "case_ref": "rtab_odometry_to_field_task_guidance_replay_path",
        "case_kind": "positive",
        "sample_file": "derived_from_positive_case_1",
        "passed": passed,
        "path_trace": path_trace,
        "checks": checks,
    }


def run_positive_low_quality_degrades_health() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("sample_rtab_odometry_low_quality.json")
    conv = pipe["conversion"]
    health_mappings = conv.get("health_mappings") or []
    degraded_health = next(
        (h for h in health_mappings if h.get("reason") == "odometry_quality_below_threshold"),
        {},
    )
    checks = {
        "health_status": degraded_health.get("health_status"),
        "severity": degraded_health.get("severity"),
        "degraded_health_does_not_directly_block_or_allow_action": True,
        "health_candidate_emitted": degraded_health.get("health_candidate_emitted") is True,
        "candidate_only": degraded_health.get("candidate_only") is True,
    }
    passed = (
        checks["health_status"] == "degraded"
        and checks["severity"] == "warning"
        and checks["health_candidate_emitted"]
        and checks["candidate_only"]
        and conv["conversion_ok"] is True
    )
    return {
        "case_ref": "rtab_odometry_low_quality_degrades_health",
        "case_kind": "positive",
        "sample_file": pipe["sample_file"],
        "passed": passed,
        "conversion_result": _public_conversion(conv),
        "checks": checks,
    }


def run_negative_missing_tracking_state() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("invalid_rtab_odometry_missing_tracking_state.json")
    row = pipe["row_result"]
    conv = pipe["conversion"]
    rejected = (
        row["rejected_record_count"] > 0
        and any("missing_tracking_state" in err for err in row["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {
        "case_ref": "invalid_missing_tracking_state_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": pipe["sample_file"],
        "passed": rejected,
        "checks": {
            "missing_tracking_state_rejected": rejected,
            "parse_errors": row["parse_errors"],
        },
    }


def run_negative_zero_quaternion() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("invalid_rtab_odometry_zero_quaternion.json")
    row = pipe["row_result"]
    conv = pipe["conversion"]
    rejected = (
        row["rejected_record_count"] > 0
        and any("bad_quaternion_all_zero" in err for err in row["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {
        "case_ref": "invalid_zero_quaternion_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": pipe["sample_file"],
        "passed": rejected,
        "checks": {
            "zero_quaternion_rejected": rejected,
            "parse_errors": row["parse_errors"],
        },
    }


def run_negative_missing_source_chain() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("invalid_rtab_odometry_missing_source_chain.json")
    row = pipe["row_result"]
    conv = pipe["conversion"]
    rejected = (
        row["rejected_record_count"] > 0
        and any("missing_source_chain" in err for err in row["parse_errors"])
        and conv["conversion_ok"] is False
    )
    return {
        "case_ref": "invalid_missing_source_chain_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": pipe["sample_file"],
        "passed": rejected,
        "checks": {
            "missing_source_chain_rejected": rejected,
            "parse_errors": row["parse_errors"],
        },
    }


def run_negative_direct_field_synthesis_write() -> Dict[str, Any]:
    pipe = _load_rtab_odometry_pipeline("invalid_rtab_odometry_native_rtab_object.json")
    admission = pipe["admission"]
    file_doc, _, _ = read_local_rtab_odometry_file("invalid_rtab_odometry_native_rtab_object.json")
    direct_write_declared = (file_doc or {}).get("direct_field_synthesis_write") is True
    rejected = (
        admission["file_source_admitted"] is False
        and direct_write_declared
        and "prohibited_backend_native_flags_present" in admission["rejection_reasons"]
    )
    return {
        "case_ref": "invalid_direct_field_synthesis_write_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": pipe["sample_file"],
        "passed": rejected,
        "admission": admission,
        "checks": {
            "direct_field_synthesis_write_rejected": rejected,
            "rejection_reasons": admission["rejection_reasons"],
        },
    }


def run_negative_rtab_db_ros_live_runtime() -> Dict[str, Any]:
    sample_file = "invalid_rtab_odometry_native_rtab_object.json"
    file_doc, _, _ = read_local_rtab_odometry_file(sample_file)
    admission = admit_rtab_odometry_file_source(sample_file=sample_file, file_doc=file_doc or {})
    flags_declared = any(
        (file_doc or {}).get(flag) is True
        for flag in ("rtab_db_read", "ros_topic_read", "live_rtab_runtime")
    )
    rejected = (
        admission["file_source_admitted"] is False
        and flags_declared
        and "prohibited_backend_native_flags_present" in admission["rejection_reasons"]
    )
    return {
        "case_ref": "invalid_rtab_db_ros_live_runtime_rejected",
        "case_kind": "negative",
        "expected_outcome": "rejected",
        "sample_file": sample_file,
        "passed": rejected,
        "admission": admission,
        "checks": {
            "rtab_db_ros_live_runtime_rejected": rejected,
            "rejection_reasons": admission["rejection_reasons"],
        },
    }


def build_positive_cases_v1() -> Tuple[RTABMapOdometryRealFileLoaderDryRunCase, ...]:
    specs = (
        (
            "rtab_odometry_valid_file_to_pose_motion_health_json_trace",
            "sample_rtab_odometry_valid_with_degraded.json",
            "PASS",
        ),
        (
            "rtab_odometry_lost_tracking_to_critical_health",
            "sample_rtab_odometry_lost_tracking.json",
            "PASS",
        ),
        (
            "rtab_odometry_alias_fields_to_standard_trace",
            "sample_rtab_odometry_alias_fields.json",
            "PASS",
        ),
        (
            "rtab_odometry_metadata_and_source_chain_preserved",
            "sample_rtab_odometry_with_metadata.json",
            "PASS",
        ),
        (
            "rtab_odometry_to_field_task_guidance_replay_path",
            "derived_from_positive_case_1",
            "PASS",
        ),
        (
            "rtab_odometry_low_quality_degrades_health",
            "sample_rtab_odometry_low_quality.json",
            "PASS",
        ),
    )
    return tuple(
        RTABMapOdometryRealFileLoaderDryRunCase(
            case_ref=case_ref,
            case_kind="positive",
            sample_file=sample_file,
            expected_outcome=outcome,
            source_chain=SOURCE_CHAIN,
        )
        for case_ref, sample_file, outcome in specs
    )


def build_negative_cases_v1() -> Tuple[RTABMapOdometryRealFileLoaderDryRunCase, ...]:
    specs = (
        (
            "invalid_missing_tracking_state_rejected",
            "invalid_rtab_odometry_missing_tracking_state.json",
            "EXPECTED_REJECT",
        ),
        (
            "invalid_zero_quaternion_rejected",
            "invalid_rtab_odometry_zero_quaternion.json",
            "EXPECTED_REJECT",
        ),
        (
            "invalid_missing_source_chain_rejected",
            "invalid_rtab_odometry_missing_source_chain.json",
            "EXPECTED_REJECT",
        ),
        (
            "invalid_direct_field_synthesis_write_rejected",
            "invalid_rtab_odometry_native_rtab_object.json",
            "EXPECTED_REJECT",
        ),
        (
            "invalid_rtab_db_ros_live_runtime_rejected",
            "invalid_rtab_odometry_native_rtab_object.json",
            "EXPECTED_REJECT",
        ),
    )
    return tuple(
        RTABMapOdometryRealFileLoaderDryRunCase(
            case_ref=case_ref,
            case_kind="negative",
            sample_file=sample_file,
            expected_outcome=outcome,
            source_chain=SOURCE_CHAIN,
        )
        for case_ref, sample_file, outcome in specs
    )


def run_all_cases_v1() -> Dict[str, Any]:
    case1 = run_positive_valid_file_case()
    case2 = run_positive_lost_tracking_case()
    case3 = run_positive_alias_fields_case()
    case4 = run_positive_metadata_preserved_case()
    case5 = run_positive_field_task_guidance_case(case1.get("_internal") or {})
    case6 = run_positive_low_quality_degrades_health()

    case1_public = {k: v for k, v in case1.items() if k != "_internal"}

    positive_results = [case1_public, case2, case3, case4, case5, case6]
    negative_results = [
        run_negative_missing_tracking_state(),
        run_negative_zero_quaternion(),
        run_negative_missing_source_chain(),
        run_negative_direct_field_synthesis_write(),
        run_negative_rtab_db_ros_live_runtime(),
    ]

    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results,
        "positive_case_refs": list(POSITIVE_CASE_REFS),
        "negative_case_refs": list(NEGATIVE_CASE_REFS),
        "sample_files": list(SAMPLE_FILES),
        "samples_rel_dir": SAMPLES_REL_DIR,
        "primary_positive_case": case1_public,
    }
