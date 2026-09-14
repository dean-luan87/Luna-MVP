#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Scene Delta executor contract conformance smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

SKELETON_SCHEMA = "scene_delta_executor_contract_skeleton_v0"


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

    sk_p = root / "scene_delta_executor_contract_skeleton_v0.json"
    req_p = root / "scene_delta_executor_request_conformance_matrix.json"
    ack_p = root / "scene_delta_executor_ack_conformance_matrix.json"
    gap_p = root / "scene_delta_executor_contract_gap_report.json"
    nw_p = root / "scene_delta_executor_no_write_contract_report.json"
    aud_p = root / "scene_delta_executor_contract_conformance_audit_report.json"

    for label, p in (
        ("contract_skeleton", sk_p),
        ("request_matrix", req_p),
        ("ack_matrix", ack_p),
        ("gap_report", gap_p),
        ("no_write_contract", nw_p),
        ("conformance_audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "scene_delta_executor_contract_conformance_verifier_report_v0",
            "phase": "Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "scene_delta_executor_contract_conformance_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    sk: Dict[str, Any] = _read_json(sk_p)
    req_m: Dict[str, Any] = _read_json(req_p)
    ack_m: Dict[str, Any] = _read_json(ack_p)
    gap: Dict[str, Any] = _read_json(gap_p)
    nw: Dict[str, Any] = _read_json(nw_p)
    aud: Dict[str, Any] = _read_json(aud_p)

    if str(sk.get("schema_version") or "") != SKELETON_SCHEMA:
        blockers.append("contract_skeleton_schema_mismatch")

    if not _all_checks_ok(req_m):
        blockers.append("request_required_fields_not_all_ok")
    if not _all_checks_ok(ack_m):
        blockers.append("ack_required_fields_not_all_ok")

    h_root = ""
    sum_p = root / "scene_delta_executor_contract_conformance_summary.json"
    if sum_p.is_file():
        sm = _read_json(sum_p)
        if isinstance(sm, dict):
            h_root = str(sm.get("input_mock_handshake_root") or "")

    ack_src_p = Path(h_root) / "scene_delta_mock_executor_ack.json" if h_root else None
    audit_src_p = Path(h_root) / "scene_delta_mock_handshake_audit_report.json" if h_root else None

    if ack_src_p and ack_src_p.is_file():
        ack_src: Dict[str, Any] = _read_json(ack_src_p)
        if ack_src.get("write_attempted") is not False:
            blockers.append("ack_write_attempted_must_be_false")
        if ack_src.get("write_committed") is not False:
            blockers.append("ack_write_committed_must_be_false")
        if ack_src.get("real_executor_invoked") is not False:
            blockers.append("ack_real_executor_invoked_must_be_false")
    else:
        blockers.append("cannot_reload_mock_ack_for_verification")

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
    else:
        blockers.append("cannot_reload_handshake_audit_for_verification")

    if nw.get("no_write_mode_checks_ok") is not True:
        blockers.append("no_write_contract_report_failed")

    for k, must in (
        ("contract_conformance_checked", True),
        ("real_scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("database_write_invoked", False),
        ("rehearsal_log_written", False),
        ("wal_append_invoked", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
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
        "schema": "scene_delta_executor_contract_conformance_verifier_report_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "contract_reference_mode": gap.get("contract_reference_mode"),
    }
    _write_json(root / "scene_delta_executor_contract_conformance_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
