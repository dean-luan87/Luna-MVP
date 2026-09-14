# -*- coding: utf-8 -*-
"""In-memory mock Scene Delta executor handshake from generic trace stub.

Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

MOCK_REQUEST_GENERIC_SCHEMA = "scene_delta_mock_executor_request_generic_v0"
MOCK_ACK_GENERIC_SCHEMA = "scene_delta_mock_executor_ack_generic_v0"
COMPAT_REPORT_GENERIC_SCHEMA = "scene_delta_mock_handshake_compatibility_report_generic_v0"
MOCK_HANDSHAKE_AUDIT_GENERIC_SCHEMA = "scene_delta_mock_handshake_audit_generic_v0"
TRACE_STUB_GENERIC_SCHEMA = "scene_delta_executor_trace_stub_generic_v0"

SUPPORTED_SOURCE_TYPES = frozenset({"ocr_evidence", "vision_recognition_evidence"})
FORBIDDEN_STEP_STATUSES = frozenset({"executed_write", "committed", "approved"})

HANDSHAKE_TRACE_EVENTS = (
    "mock_request_created",
    "mock_executor_received",
    "generic_trace_shape_validated",
    "synthetic_ack_emitted",
    "no_write_confirmed",
)


def _utc_ts() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_mock_executor_request_generic_v0(
    *,
    trace_stub: Dict[str, Any],
    candidate_payload_ref: str,
    planned_matrix_path: str,
    compatibility_path: str,
) -> Dict[str, Any]:
    return {
        "schema_version": MOCK_REQUEST_GENERIC_SCHEMA,
        "request_id": f"mock_req_generic_{uuid.uuid4().hex}",
        "source_trace_id": str(trace_stub.get("trace_id") or ""),
        "source_dry_run_id": str(trace_stub.get("source_dry_run_id") or ""),
        "source_candidate_id": str(trace_stub.get("source_candidate_id") or ""),
        "source_type": str(trace_stub.get("source_type") or ""),
        "executor_mode": "mock_handshake_only",
        "write_allowed": False,
        "candidate_payload_ref": str(candidate_payload_ref),
        "planned_step_matrix_ref": str(planned_matrix_path),
        "input_compatibility_ref": str(compatibility_path),
        "request_scope": "no_write_handshake",
    }


def build_mock_executor_ack_generic_v0(
    *,
    request: Dict[str, Any],
    trace_stub: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": MOCK_ACK_GENERIC_SCHEMA,
        "ack_id": f"mock_ack_generic_{uuid.uuid4().hex}",
        "request_id": str(request.get("request_id") or ""),
        "source_trace_id": str(trace_stub.get("trace_id") or ""),
        "source_type": str(trace_stub.get("source_type") or ""),
        "ack_status": "accepted_for_shape_only",
        "executor_invoked": False,
        "real_executor_invoked": False,
        "write_attempted": False,
        "write_committed": False,
        "reason_codes": [
            "mock_handshake_only",
            "no_write_allowed",
            "gate_not_evaluated",
            "generic_trace_stub_accepted",
        ],
    }


def build_handshake_trace_lines_generic_v0(
    *,
    request_id: str,
    trace_id: str,
    source_type: str,
) -> List[Dict[str, Any]]:
    ts = _utc_ts()
    base = {
        "ts": ts,
        "request_id": request_id,
        "source_trace_id": trace_id,
        "source_type": source_type,
    }
    return [{**base, "event": ev} for ev in HANDSHAKE_TRACE_EVENTS]


def build_mock_handshake_compatibility_report_generic_v0(
    *,
    trace_stub: Dict[str, Any],
    request: Dict[str, Any],
    planned_matrix: Dict[str, Any],
    compatibility_input: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    issues: List[str] = []
    source_type = str(trace_stub.get("source_type") or "")

    if not bool(str(trace_stub.get("trace_id") or "").strip()):
        issues.append("source_trace_id_missing")
    if not bool(str(trace_stub.get("source_candidate_id") or "").strip()):
        issues.append("source_candidate_id_missing")
    if not bool(str(trace_stub.get("source_dry_run_id") or "").strip()):
        issues.append("source_dry_run_id_missing")
    if source_type not in SUPPORTED_SOURCE_TYPES:
        issues.append("source_type_not_supported")

    src_mode = str(trace_stub.get("executor_mode") or "")
    if src_mode != "trace_stub_only":
        issues.append("source_trace_executor_mode_not_trace_stub_only")

    if trace_stub.get("no_write_guarantee") is not True:
        issues.append("no_write_guarantee_not_true")

    if str(request.get("request_scope") or "") != "no_write_handshake":
        issues.append("request_scope_invalid")
    if request.get("write_allowed") is not False:
        issues.append("request_write_allowed_not_false")

    rows = planned_matrix.get("rows") if isinstance(planned_matrix.get("rows"), list) else []
    for row in rows:
        if not isinstance(row, dict):
            continue
        st = str(row.get("status") or "")
        if st in FORBIDDEN_STEP_STATUSES:
            issues.append(f"forbidden_planned_status:{row.get('step')}:{st}")

    overall_compat = False
    if isinstance(compatibility_input, dict):
        overall_compat = compatibility_input.get("overall_compatible") is True
        if not compatibility_input.get("schema"):
            issues.append("input_compatibility_schema_missing")
    else:
        issues.append("input_compatibility_report_missing")

    if not overall_compat:
        issues.append("input_compatibility_overall_compatible_not_true")

    report = {
        "schema": COMPAT_REPORT_GENERIC_SCHEMA,
        "generic_trace_stub_exists": True,
        "source_type": source_type,
        "source_type_supported": source_type in SUPPORTED_SOURCE_TYPES,
        "source_trace_id_present": bool(str(trace_stub.get("trace_id") or "").strip()),
        "source_candidate_id_present": bool(str(trace_stub.get("source_candidate_id") or "").strip()),
        "source_dry_run_id_present": bool(str(trace_stub.get("source_dry_run_id") or "").strip()),
        "source_executor_mode": src_mode,
        "source_executor_mode_ok": src_mode == "trace_stub_only",
        "request_scope_ok": str(request.get("request_scope") or "") == "no_write_handshake",
        "write_allowed_false": request.get("write_allowed") is False,
        "no_write_guarantee_true": trace_stub.get("no_write_guarantee") is True,
        "planned_matrix_forbidden_status_scan_ok": len([i for i in issues if i.startswith("forbidden_planned_status")]) == 0,
        "input_compatibility_overall_compatible": overall_compat,
        "issues": list(issues),
        "overall_ok": len(issues) == 0,
    }
    return report, issues


def build_mock_handshake_audit_generic_v0() -> Dict[str, Any]:
    return {
        "schema": MOCK_HANDSHAKE_AUDIT_GENERIC_SCHEMA,
        "generic_mock_handshake_executed": True,
        "mock_executor_request_created": True,
        "synthetic_ack_emitted": True,
        "real_scene_delta_executor_invoked": False,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "database_write_invoked": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_routing_changed": False,
        "real_vision_provider_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "rehearsal_log_written": False,
        "wal_append_invoked": False,
    }


def run_mock_handshake_generic_v0(
    *,
    trace_stub: Dict[str, Any],
    planned_matrix: Dict[str, Any],
    compatibility_input: Dict[str, Any],
    trace_stub_audit: Dict[str, Any],
    candidate_payload_ref: str,
    planned_matrix_path: str,
    compatibility_path: str,
    generic_trace_root: str,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any], List[str]]:
    """
    In-memory generic handshake. ``trace_stub_audit`` is read for lineage only.

    Returns (summary, request, ack, trace_lines, compat_report, audit, blocking_errors).
    """
    _ = trace_stub_audit

    blocking: List[str] = []
    if str(trace_stub.get("schema_version") or "") != TRACE_STUB_GENERIC_SCHEMA:
        blocking.append("invalid_generic_trace_stub_schema")

    source_type = str(trace_stub.get("source_type") or "")
    if source_type not in SUPPORTED_SOURCE_TYPES:
        blocking.append("unsupported_source_type")

    req = build_mock_executor_request_generic_v0(
        trace_stub=trace_stub,
        candidate_payload_ref=candidate_payload_ref,
        planned_matrix_path=planned_matrix_path,
        compatibility_path=compatibility_path,
    )
    ack = build_mock_executor_ack_generic_v0(request=req, trace_stub=trace_stub)
    lines = build_handshake_trace_lines_generic_v0(
        request_id=str(req.get("request_id") or ""),
        trace_id=str(trace_stub.get("trace_id") or ""),
        source_type=source_type,
    )
    compat, issues = build_mock_handshake_compatibility_report_generic_v0(
        trace_stub=trace_stub,
        request=req,
        planned_matrix=planned_matrix,
        compatibility_input=compatibility_input,
    )
    audit = build_mock_handshake_audit_generic_v0()

    summary = {
        "schema_version": "scene_delta_executor_mock_handshake_generic_summary_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001",
        "input_generic_trace_root": generic_trace_root,
        "request_id": req.get("request_id"),
        "ack_id": ack.get("ack_id"),
        "source_trace_id": trace_stub.get("trace_id"),
        "source_dry_run_id": trace_stub.get("source_dry_run_id"),
        "source_candidate_id": trace_stub.get("source_candidate_id"),
        "source_type": source_type,
        "ack_status": ack.get("ack_status"),
        "compatibility_overall_ok": compat.get("overall_ok"),
        "compatibility_issues": list(issues),
        "blocking_errors": list(blocking),
    }

    return summary, req, ack, lines, compat, audit, blocking
