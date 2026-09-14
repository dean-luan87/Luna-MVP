# -*- coding: utf-8 -*-
"""In-memory mock Scene Delta executor handshake (synthetic ACK only).

Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-001 — no real executor, no writes, no WAL.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

MOCK_REQUEST_SCHEMA = "scene_delta_mock_executor_request_v0"
MOCK_ACK_SCHEMA = "scene_delta_mock_executor_ack_v0"
COMPAT_REPORT_SCHEMA = "scene_delta_mock_handshake_compatibility_report_v0"
MOCK_HANDSHAKE_AUDIT_SCHEMA = "scene_delta_mock_handshake_audit_v0"

FORBIDDEN_STEP_STATUSES = frozenset({"executed_write", "committed", "approved"})


def _utc_ts() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_mock_executor_request_v0(
    *,
    trace_stub: Dict[str, Any],
    trace_stub_path: str,
    planned_matrix_path: str,
    compatibility_path: str,
    candidate_payload_ref: str,
) -> Dict[str, Any]:
    return {
        "schema_version": MOCK_REQUEST_SCHEMA,
        "request_id": f"mock_req_{uuid.uuid4().hex}",
        "source_trace_id": str(trace_stub.get("trace_id") or ""),
        "source_candidate_id": str(trace_stub.get("source_candidate_id") or ""),
        "executor_mode": "mock_handshake_only",
        "write_allowed": False,
        "candidate_payload_ref": str(candidate_payload_ref),
        "planned_step_matrix_ref": str(planned_matrix_path),
        "input_compatibility_ref": str(compatibility_path),
        "request_scope": "no_write_handshake",
        "source_trace_stub_ref": str(trace_stub_path),
    }


def build_mock_executor_ack_v0(
    *,
    request: Dict[str, Any],
    trace_stub: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": MOCK_ACK_SCHEMA,
        "ack_id": f"mock_ack_{uuid.uuid4().hex}",
        "request_id": str(request.get("request_id") or ""),
        "source_trace_id": str(trace_stub.get("trace_id") or ""),
        "ack_status": "accepted_for_shape_only",
        "executor_invoked": False,
        "real_executor_invoked": False,
        "write_attempted": False,
        "write_committed": False,
        "reason_codes": [
            "mock_handshake_only",
            "no_write_allowed",
            "gate_not_evaluated",
        ],
    }


def build_handshake_trace_lines_v0(
    *,
    request_id: str,
    trace_id: str,
) -> List[Dict[str, Any]]:
    ts = _utc_ts()
    base = {"ts": ts, "request_id": request_id, "source_trace_id": trace_id}
    return [
        {**base, "event": "mock_request_created"},
        {**base, "event": "mock_executor_received"},
        {**base, "event": "shape_validated"},
        {**base, "event": "synthetic_ack_emitted"},
        {**base, "event": "no_write_confirmed"},
    ]


def build_mock_handshake_compatibility_report_v0(
    *,
    trace_stub: Dict[str, Any],
    request: Dict[str, Any],
    planned_matrix: Dict[str, Any],
    compatibility_input: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    issues: List[str] = []

    tid_ok = bool(str(trace_stub.get("trace_id") or "").strip())
    if not tid_ok:
        issues.append("trace_id_missing")

    scid_ok = bool(str(trace_stub.get("source_candidate_id") or "").strip())
    if not scid_ok:
        issues.append("source_candidate_id_missing")

    src_mode = str(trace_stub.get("executor_mode") or "")
    if src_mode != "trace_stub_only":
        issues.append("source_trace_executor_mode_not_trace_stub_only")

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

    compat_ok = isinstance(compatibility_input, dict) and bool(compatibility_input.get("schema"))

    report = {
        "schema": COMPAT_REPORT_SCHEMA,
        "trace_id_present": tid_ok,
        "source_candidate_id_present": scid_ok,
        "source_executor_mode": src_mode,
        "source_executor_mode_ok": src_mode == "trace_stub_only",
        "request_scope": str(request.get("request_scope") or ""),
        "request_scope_ok": str(request.get("request_scope") or "") == "no_write_handshake",
        "write_allowed_false": request.get("write_allowed") is False,
        "planned_matrix_forbidden_status_scan_ok": len([i for i in issues if i.startswith("forbidden_planned_status")]) == 0,
        "input_compatibility_report_exists": compat_ok,
        "issues": list(issues),
        "overall_ok": len(issues) == 0,
    }
    return report, issues


def build_mock_handshake_audit_v0() -> Dict[str, Any]:
    return {
        "schema": MOCK_HANDSHAKE_AUDIT_SCHEMA,
        "mock_handshake_executed": True,
        "mock_executor_request_created": True,
        "synthetic_ack_emitted": True,
        "real_scene_delta_executor_invoked": False,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "database_write_invoked": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_routing_changed": False,
        "rehearsal_log_written": False,
        "wal_append_invoked": False,
    }


def run_mock_handshake_v0(
    *,
    trace_stub: Dict[str, Any],
    planned_matrix: Dict[str, Any],
    compatibility_input: Dict[str, Any],
    trace_stub_audit: Dict[str, Any],
    trace_stub_path: str,
    planned_matrix_path: str,
    compatibility_path: str,
    candidate_payload_ref: str,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], List[Dict[str, Any]], Dict[str, Any], Dict[str, Any], List[str]]:
    """
    In-memory handshake. ``trace_stub_audit`` is read for lineage only (not mutated).

    Returns (summary, request, ack, trace_lines, compat_report, audit, blocking_errors).
    """
    _ = trace_stub_audit  # lineage / future correlation

    blocking: List[str] = []
    if str(trace_stub.get("schema_version") or "") != "scene_delta_executor_trace_stub_v0":
        blocking.append("invalid_trace_stub_schema")

    req = build_mock_executor_request_v0(
        trace_stub=trace_stub,
        trace_stub_path=trace_stub_path,
        planned_matrix_path=planned_matrix_path,
        compatibility_path=compatibility_path,
        candidate_payload_ref=candidate_payload_ref,
    )
    ack = build_mock_executor_ack_v0(request=req, trace_stub=trace_stub)
    lines = build_handshake_trace_lines_v0(request_id=str(req.get("request_id")), trace_id=str(trace_stub.get("trace_id")))
    compat, issues = build_mock_handshake_compatibility_report_v0(
        trace_stub=trace_stub,
        request=req,
        planned_matrix=planned_matrix,
        compatibility_input=compatibility_input,
    )
    audit = build_mock_handshake_audit_v0()

    summary = {
        "schema": "scene_delta_executor_mock_handshake_summary_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-001",
        "input_trace_stub_root": None,
        "request_id": req.get("request_id"),
        "ack_id": ack.get("ack_id"),
        "source_trace_id": trace_stub.get("trace_id"),
        "source_candidate_id": trace_stub.get("source_candidate_id"),
        "ack_status": ack.get("ack_status"),
        "compatibility_overall_ok": compat.get("overall_ok"),
        "compatibility_issues": list(issues),
        "blocking_errors": list(blocking),
    }

    return summary, req, ack, lines, compat, audit, blocking
