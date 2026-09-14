#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for generic Scene Delta executor contract conformance smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

SKELETON_SCHEMA = "scene_delta_executor_contract_skeleton_generic_v0"
SUPPORTED_SOURCE_TYPES = frozenset({"ocr_evidence", "vision_recognition_evidence"})


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


def _all_checks_ok(matrix: Dict[str, Any]) -> bool:
    ch = matrix.get("checks")
    if not isinstance(ch, dict):
        return False
    for _k, v in ch.items():
        if not isinstance(v, dict) or v.get("ok") is not True:
            return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    sk_p = root / "scene_delta_executor_contract_skeleton_generic_v0.json"
    req_p = root / "scene_delta_executor_request_conformance_matrix_generic.json"
    ack_p = root / "scene_delta_executor_ack_conformance_matrix_generic.json"
    gap_p = root / "scene_delta_executor_contract_gap_report_generic.json"
    nw_p = root / "scene_delta_executor_no_write_contract_report_generic.json"
    aud_p = root / "scene_delta_executor_contract_conformance_audit_report_generic.json"

    for label, p in (
        ("contract_skeleton_generic", sk_p),
        ("request_matrix_generic", req_p),
        ("ack_matrix_generic", ack_p),
        ("gap_report_generic", gap_p),
        ("no_write_contract_generic", nw_p),
        ("conformance_audit_generic", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "scene_delta_executor_contract_conformance_generic_verifier_report_v0",
            "phase": "Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-Generic-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "scene_delta_executor_contract_conformance_generic_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    sk: Dict[str, Any] = _read_json(sk_p)
    req_m: Dict[str, Any] = _read_json(req_p)
    ack_m: Dict[str, Any] = _read_json(ack_p)
    gap: Dict[str, Any] = _read_json(gap_p)
    nw: Dict[str, Any] = _read_json(nw_p)
    aud: Dict[str, Any] = _read_json(aud_p)
    summ_p = root / "scene_delta_executor_contract_conformance_generic_summary.json"
    source_type = ""
    if summ_p.is_file():
        sm = _read_json(summ_p)
        if isinstance(sm, dict):
            source_type = str(sm.get("source_type") or "")

    if str(sk.get("schema_version") or "") != SKELETON_SCHEMA:
        blockers.append("contract_skeleton_schema_mismatch")
    if str(sk.get("contract_reference_mode") or "") != "local_skeleton":
        blockers.append("contract_reference_mode_must_be_local_skeleton")
    if source_type not in SUPPORTED_SOURCE_TYPES:
        blockers.append("source_type_must_be_ocr_or_vision")

    if not _all_checks_ok(req_m):
        blockers.append("request_required_fields_not_all_ok")
    if not _all_checks_ok(ack_m):
        blockers.append("ack_required_fields_not_all_ok")

    rc_check = ack_m.get("checks", {}).get("reason_codes", {}) if isinstance(ack_m.get("checks"), dict) else {}
    if rc_check.get("ok") is not True:
        blockers.append("ack_reason_codes_must_include_generic_trace_stub_accepted")

    h_root = ""
    if summ_p.is_file():
        sm = _read_json(summ_p)
        if isinstance(sm, dict):
            h_root = str(sm.get("input_generic_mock_handshake_root") or "")

    ack_src_p = Path(h_root) / "scene_delta_mock_executor_ack_generic.json" if h_root else None
    audit_src_p = Path(h_root) / "scene_delta_mock_handshake_audit_report_generic.json" if h_root else None

    if ack_src_p and ack_src_p.is_file():
        ack_src: Dict[str, Any] = _read_json(ack_src_p)
        if ack_src.get("write_attempted") is not False:
            blockers.append("ack_write_attempted_must_be_false")
        if ack_src.get("write_committed") is not False:
            blockers.append("ack_write_committed_must_be_false")
        if ack_src.get("real_executor_invoked") is not False:
            blockers.append("ack_real_executor_invoked_must_be_false")
        rc = ack_src.get("reason_codes")
        if not isinstance(rc, list) or "generic_trace_stub_accepted" not in {str(x) for x in rc}:
            blockers.append("ack_reason_codes_missing_generic_trace_stub_accepted")
    else:
        blockers.append("cannot_reload_mock_ack_generic_for_verification")

    if audit_src_p and audit_src_p.is_file():
        ha = _read_json(audit_src_p)
        if ha.get("real_scene_delta_executor_invoked") is not False:
            blockers.append("handshake_audit_real_scene_delta_executor_invoked_must_be_false")
        if ha.get("scene_delta_written") is not False:
            blockers.append("scene_delta_written_must_be_false")
        if ha.get("database_write_invoked") is not False:
            blockers.append("database_write_invoked_must_be_false")
        if ha.get("rehearsal_log_written") is not False:
            blockers.append("rehearsal_log_written_must_be_false")
        if ha.get("wal_append_invoked") is not False:
            blockers.append("wal_append_invoked_must_be_false")
        if ha.get("midplatform_fact_written") is not False:
            blockers.append("midplatform_fact_written_must_be_false")
        if ha.get("world_model_written") is not False:
            blockers.append("world_model_written_must_be_false")
        if ha.get("ai_interpretation_invoked") is not False:
            blockers.append("ai_interpretation_invoked_must_be_false")
        if ha.get("navigation_decision_invoked") is not False:
            blockers.append("navigation_decision_invoked_must_be_false")
        if ha.get("ocr_provider_invoked") is not False:
            blockers.append("ocr_provider_invoked_must_be_false")
        if ha.get("ocr_routing_changed") is not False:
            blockers.append("ocr_routing_changed_must_be_false")
        if ha.get("real_vision_provider_invoked") is not False:
            blockers.append("real_vision_provider_invoked_must_be_false")
        if ha.get("yolo_invoked") is not False:
            blockers.append("yolo_invoked_must_be_false")
        if ha.get("supervision_mainline_invoked") is not False:
            blockers.append("supervision_mainline_invoked_must_be_false")
        if ha.get("vlm_invoked") is not False:
            blockers.append("vlm_invoked_must_be_false")
    else:
        blockers.append("cannot_reload_handshake_audit_generic_for_verification")

    if nw.get("no_write_mode_checks_ok") is not True:
        blockers.append("no_write_contract_report_failed")

    for k, must in (
        ("generic_contract_conformance_checked", True),
        ("real_scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("database_write_invoked", False),
        ("rehearsal_log_written", False),
        ("wal_append_invoked", False),
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
    ):
        if aud.get(k) is not must:
            blockers.append(f"conformance_audit:{k}")

    if not blockers:
        verdict = "GO"
        if str(gap.get("contract_reference_mode") or "") == "local_skeleton":
            soft.append("contract_reference_mode_is_local_skeleton_not_production_contract")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "scene_delta_executor_contract_conformance_generic_verifier_report_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-Generic-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "contract_reference_mode": gap.get("contract_reference_mode"),
        "source_type": source_type,
    }
    _write_json(root / "scene_delta_executor_contract_conformance_generic_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
