#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for generic Scene Delta executor mock handshake smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

REQ_SCHEMA = "scene_delta_mock_executor_request_generic_v0"
ACK_SCHEMA = "scene_delta_mock_executor_ack_generic_v0"
SUPPORTED_SOURCE_TYPES = frozenset({"ocr_evidence", "vision_recognition_evidence"})
REQUIRED_TRACE_EVENTS = frozenset(
    {
        "mock_request_created",
        "mock_executor_received",
        "generic_trace_shape_validated",
        "synthetic_ack_emitted",
        "no_write_confirmed",
    }
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    sum_p = root / "scene_delta_executor_mock_handshake_generic_summary.json"
    req_p = root / "scene_delta_mock_executor_request_generic.json"
    ack_p = root / "scene_delta_mock_executor_ack_generic.json"
    tr_p = root / "scene_delta_mock_handshake_trace_generic.jsonl"
    comp_p = root / "scene_delta_mock_handshake_compatibility_report_generic.json"
    aud_p = root / "scene_delta_mock_handshake_audit_report_generic.json"

    for label, p in (
        ("summary", sum_p),
        ("mock_request", req_p),
        ("mock_ack", ack_p),
        ("handshake_trace", tr_p),
        ("compatibility", comp_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "scene_delta_mock_handshake_generic_verifier_report_v0",
            "phase": "Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "scene_delta_mock_handshake_generic_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    req: Dict[str, Any] = _read_json(req_p)
    ack: Dict[str, Any] = _read_json(ack_p)
    aud: Dict[str, Any] = _read_json(aud_p)
    comp: Dict[str, Any] = _read_json(comp_p)

    if str(req.get("schema_version") or "") != REQ_SCHEMA:
        blockers.append("mock_request_schema_mismatch")
    if str(ack.get("schema_version") or "") != ACK_SCHEMA:
        blockers.append("mock_ack_schema_mismatch")

    st = str(req.get("source_type") or ack.get("source_type") or "")
    if st not in SUPPORTED_SOURCE_TYPES:
        blockers.append("source_type_must_be_ocr_or_vision")

    if str(req.get("request_scope") or "") != "no_write_handshake":
        blockers.append("request_scope_must_be_no_write_handshake")

    if str(ack.get("ack_status") or "") != "accepted_for_shape_only":
        blockers.append("ack_status_must_be_accepted_for_shape_only")

    if ack.get("executor_invoked") is not False:
        blockers.append("ack_executor_invoked_must_be_false")
    if ack.get("real_executor_invoked") is not False:
        blockers.append("ack_real_executor_invoked_must_be_false")
    if ack.get("write_attempted") is not False:
        blockers.append("write_attempted_must_be_false")
    if ack.get("write_committed") is not False:
        blockers.append("write_committed_must_be_false")

    rc = ack.get("reason_codes")
    if not isinstance(rc, list):
        blockers.append("reason_codes_must_be_list")
    else:
        rset = {str(x) for x in rc}
        for need in ("mock_handshake_only", "no_write_allowed", "generic_trace_stub_accepted"):
            if need not in rset:
                blockers.append(f"reason_codes_missing_{need}")

    try:
        lines = [ln.strip() for ln in tr_p.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if not lines:
            blockers.append("handshake_trace_empty")
        else:
            events = set()
            for ln in lines:
                row = json.loads(ln)
                ev = str(row.get("event") or "")
                if ev:
                    events.add(ev)
                if not str(row.get("source_type") or "").strip():
                    blockers.append("handshake_trace_line_missing_source_type")
                    break
            if not REQUIRED_TRACE_EVENTS.issubset(events):
                blockers.append("handshake_trace_missing_required_events")
    except Exception:
        blockers.append("handshake_trace_invalid_jsonl")

    if comp.get("overall_ok") is not True:
        blockers.append("compatibility_overall_ok_must_be_true")

    for k, must in (
        ("generic_mock_handshake_executed", True),
        ("mock_executor_request_created", True),
        ("synthetic_ack_emitted", True),
        ("real_scene_delta_executor_invoked", False),
        ("scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("database_write_invoked", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("ocr_provider_invoked", False),
        ("ocr_routing_changed", False),
        ("real_vision_provider_invoked", False),
        ("yolo_invoked", False),
        ("supervision_mainline_invoked", False),
        ("vlm_invoked", False),
        ("rehearsal_log_written", False),
        ("wal_append_invoked", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if not blockers:
        verdict = "GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "scene_delta_mock_handshake_generic_verifier_report_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Mock-Handshake-Generic-Trace-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "request_id": req.get("request_id"),
        "ack_id": ack.get("ack_id"),
        "source_type": st,
    }
    _write_json(root / "scene_delta_mock_handshake_generic_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
