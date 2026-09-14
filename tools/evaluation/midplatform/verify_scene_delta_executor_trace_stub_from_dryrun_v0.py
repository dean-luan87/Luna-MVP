#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Scene Delta executor trace stub from dry-run smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

TRACE_SCHEMA = "scene_delta_executor_trace_stub_v0"
FORBIDDEN_STATUSES = frozenset({"executed_write", "committed", "approved"})


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

    sum_p = root / "scene_delta_executor_trace_stub_summary.json"
    tr_p = root / "scene_delta_executor_trace_stub.json"
    mat_p = root / "scene_delta_executor_planned_step_matrix.json"
    comp_p = root / "scene_delta_executor_input_compatibility_report.json"
    aud_p = root / "scene_delta_executor_trace_stub_audit_report.json"

    for label, p in (
        ("trace_stub_summary", sum_p),
        ("trace_stub", tr_p),
        ("planned_step_matrix", mat_p),
        ("input_compatibility", comp_p),
        ("trace_stub_audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "scene_delta_executor_trace_stub_verifier_report_v0",
            "phase": "Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "scene_delta_executor_trace_stub_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    tr: Dict[str, Any] = _read_json(tr_p)
    aud: Dict[str, Any] = _read_json(aud_p)
    mat: Dict[str, Any] = _read_json(mat_p)
    comp: Dict[str, Any] = _read_json(comp_p)

    if str(tr.get("schema_version") or "") != TRACE_SCHEMA:
        blockers.append("trace_stub_schema_mismatch")
    if str(tr.get("executor_mode") or "") != "trace_stub_only":
        blockers.append("executor_mode_must_be_trace_stub_only")
    if tr.get("executor_invoked") is not False:
        blockers.append("executor_invoked_must_be_false")
    if tr.get("write_allowed") is not False:
        blockers.append("write_allowed_must_be_false")
    if tr.get("no_write_guarantee") is not True:
        blockers.append("no_write_guarantee_must_be_true")

    ps = tr.get("planned_steps")
    if not isinstance(ps, list) or not ps:
        blockers.append("planned_steps_must_exist")

    rows = mat.get("rows")
    if not isinstance(rows, list) or not rows:
        blockers.append("planned_step_matrix_rows_missing")

    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        st = str(row.get("status") or "")
        if st in FORBIDDEN_STATUSES:
            blockers.append(f"forbidden_step_status:{row.get('step')}:{st}")

    if str(tr.get("gate_status") or "") != "not_evaluated":
        blockers.append("gate_status_must_be_not_evaluated")

    rc = tr.get("risk_codes")
    if not isinstance(rc, list) or "gate_not_evaluated" not in rc:
        blockers.append("risk_codes_must_include_gate_not_evaluated")

    for k, must in (
        ("scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("database_write_invoked", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("ocr_provider_invoked", False),
        ("ocr_routing_changed", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if aud.get("executor_trace_stub_generated") is not True:
        blockers.append("executor_trace_stub_generated_must_be_true")

    if not isinstance(comp, dict) or not comp:
        blockers.append("input_compatibility_report_empty")

    if not blockers:
        verdict = "GO"
        if isinstance(rows, list) and len(rows) < 8:
            verdict = "CONDITIONAL_GO"
            soft.append("planned_step_matrix_optional_steps_incomplete")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "scene_delta_executor_trace_stub_verifier_report_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "trace_id": tr.get("trace_id"),
    }
    _write_json(root / "scene_delta_executor_trace_stub_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
