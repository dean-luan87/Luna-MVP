# -*- coding: utf-8 -*-
"""Static contract conformance for Scene Delta mock executor request / ACK.

Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-001 — local skeleton only; no real executor.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

CONTRACT_SKELETON_SCHEMA = "scene_delta_executor_contract_skeleton_v0"
CONTRACT_REFERENCE_MODE_LOCAL = "local_skeleton"

REQUEST_OPTIONAL_FIELDS = frozenset(
    {
        "candidate_payload_ref",
        "source_trace_stub_ref",
        "schema_version",
    }
)
ACK_OPTIONAL_FIELDS = frozenset(
    {
        "executor_invoked",
        "real_executor_invoked",
        "schema_version",
    }
)


def build_contract_skeleton_v0() -> Dict[str, Any]:
    return {
        "schema_version": CONTRACT_SKELETON_SCHEMA,
        "request_required_fields": [
            "request_id",
            "source_trace_id",
            "source_candidate_id",
            "executor_mode",
            "write_allowed",
            "request_scope",
            "planned_step_matrix_ref",
            "input_compatibility_ref",
        ],
        "ack_required_fields": [
            "ack_id",
            "request_id",
            "source_trace_id",
            "ack_status",
            "write_attempted",
            "write_committed",
            "reason_codes",
        ],
        "forbidden_in_no_write_mode": [
            "write_attempted:true",
            "write_committed:true",
            "real_executor_invoked:true",
        ],
    }


def _non_empty_str(val: Any) -> bool:
    return isinstance(val, str) and bool(val.strip())


def build_request_conformance_matrix_v0(
    request: Dict[str, Any],
    skeleton: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    required = list(skeleton.get("request_required_fields") or [])
    checks: Dict[str, Any] = {}
    missing: List[str] = []

    for field in required:
        val = request.get(field)
        ok = False
        detail: str | None = None

        if field == "write_allowed":
            ok = val is False
            if not ok:
                detail = f"expected_false_got_{val!r}"
        elif field == "request_scope":
            ok = str(val or "") == "no_write_handshake"
            if not ok:
                detail = f"expected_no_write_handshake_got_{val!r}"
        elif field in ("planned_step_matrix_ref", "input_compatibility_ref"):
            ok = _non_empty_str(val)
            if not ok:
                detail = "non_empty_string_required"
        elif field in ("request_id", "source_trace_id", "source_candidate_id", "executor_mode"):
            ok = _non_empty_str(val)
            if not ok:
                detail = "non_empty_string_required"
        else:
            ok = False
            detail = "unknown_required_field"

        checks[field] = {"ok": ok, "value": val, "detail": detail}
        if not ok:
            missing.append(field)

    return {"schema": "scene_delta_executor_request_conformance_matrix_v0", "checks": checks}, missing


def build_ack_conformance_matrix_v0(
    ack: Dict[str, Any],
    skeleton: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[str]]:
    required = list(skeleton.get("ack_required_fields") or [])
    checks: Dict[str, Any] = {}
    missing: List[str] = []

    for field in required:
        val = ack.get(field)
        ok = False
        detail = None
        if field == "write_attempted":
            ok = val is False
        elif field == "write_committed":
            ok = val is False
        elif field == "reason_codes":
            ok = isinstance(val, list) and len(val) > 0
        elif field == "ack_status":
            ok = _non_empty_str(val)
        else:
            ok = _non_empty_str(val)

        checks[field] = {"ok": ok, "value": val, "detail": detail}
        if not ok:
            missing.append(field)

    return {"schema": "scene_delta_executor_ack_conformance_matrix_v0", "checks": checks}, missing


def _extra_fields(obj: Dict[str, Any], required: List[str], optional: Set[str]) -> List[str]:
    req_set = set(required)
    keys = set(obj.keys())
    return sorted(k for k in keys if k not in req_set and k not in optional)


def build_contract_gap_report_v0(
    *,
    request_missing: List[str],
    ack_missing: List[str],
    request_extras: List[str],
    ack_extras: List[str],
    request_ok: bool,
    ack_ok: bool,
) -> Dict[str, Any]:
    conformance_level = "full" if request_ok and ack_ok else "partial"
    return {
        "schema": "scene_delta_executor_contract_gap_report_v0",
        "contract_reference_mode": CONTRACT_REFERENCE_MODE_LOCAL,
        "conformance_level": conformance_level,
        "missing_required_fields": {
            "request": list(request_missing),
            "ack": list(ack_missing),
        },
        "extra_fields": {
            "request": list(request_extras),
            "ack": list(ack_extras),
        },
        "disclaimer": "local_skeleton_only_not_aligned_to_production_executor_contract",
    }


def build_no_write_contract_report_v0(
    *,
    request: Dict[str, Any],
    ack: Dict[str, Any],
    handshake_audit: Dict[str, Any],
) -> Dict[str, Any]:
    violations: List[str] = []

    def viol(code: str, ok: bool) -> None:
        if not ok:
            violations.append(code)

    viol("ack_write_attempted", ack.get("write_attempted") is False)
    viol("ack_write_committed", ack.get("write_committed") is False)
    viol("ack_real_executor_invoked", ack.get("real_executor_invoked") is False)
    viol("audit_database_write", handshake_audit.get("database_write_invoked") is False)
    viol("audit_rehearsal_log", handshake_audit.get("rehearsal_log_written") is False)
    viol("audit_wal_append", handshake_audit.get("wal_append_invoked") is False)
    viol("request_write_allowed", request.get("write_allowed") is False)

    return {
        "schema": "scene_delta_executor_no_write_contract_report_v0",
        "no_write_mode_checks_ok": len(violations) == 0,
        "violations": violations,
    }


def build_contract_conformance_audit_v0() -> Dict[str, Any]:
    return {
        "schema": "scene_delta_executor_contract_conformance_audit_v0",
        "contract_conformance_checked": True,
        "real_scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "database_write_invoked": False,
        "rehearsal_log_written": False,
        "wal_append_invoked": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
    }


def run_contract_conformance_v0(
    *,
    request: Dict[str, Any],
    ack: Dict[str, Any],
    handshake_compat: Dict[str, Any],
    handshake_audit: Dict[str, Any],
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    """
    Returns skeleton, req_matrix, ack_matrix, gap, no_write_contract, audit, summary_partial, blocking_errors.
    """
    blocking: List[str] = []
    skeleton = build_contract_skeleton_v0()

    req_matrix, req_missing = build_request_conformance_matrix_v0(request, skeleton)
    ack_matrix, ack_missing = build_ack_conformance_matrix_v0(ack, skeleton)

    req_required = list(skeleton.get("request_required_fields") or [])
    ack_required = list(skeleton.get("ack_required_fields") or [])
    req_extras = _extra_fields(request, req_required, REQUEST_OPTIONAL_FIELDS)
    ack_extras = _extra_fields(ack, ack_required, ACK_OPTIONAL_FIELDS)

    request_ok = len(req_missing) == 0
    ack_ok = len(ack_missing) == 0
    if req_missing:
        blocking.append(f"request_missing_required:{req_missing}")
    if ack_missing:
        blocking.append(f"ack_missing_required:{ack_missing}")

    gap = build_contract_gap_report_v0(
        request_missing=req_missing,
        ack_missing=ack_missing,
        request_extras=req_extras,
        ack_extras=ack_extras,
        request_ok=request_ok,
        ack_ok=ack_ok,
    )
    nw = build_no_write_contract_report_v0(request=request, ack=ack, handshake_audit=handshake_audit)
    if not nw.get("no_write_mode_checks_ok"):
        blocking.append("no_write_contract_violations")

    audit = build_contract_conformance_audit_v0()

    summary = {
        "schema": "scene_delta_executor_contract_conformance_summary_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-001",
        "contract_reference_mode": CONTRACT_REFERENCE_MODE_LOCAL,
        "request_conformance_ok": request_ok,
        "ack_conformance_ok": ack_ok,
        "handshake_compatibility_overall_ok": handshake_compat.get("overall_ok"),
        "blocking_errors": list(blocking),
    }

    return skeleton, req_matrix, ack_matrix, gap, nw, audit, summary, blocking
