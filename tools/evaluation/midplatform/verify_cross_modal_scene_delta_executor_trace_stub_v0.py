#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Scene Delta executor trace stub."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

FORBIDDEN_MATRIX_STATUSES = (
    "executed_write",
    "committed",
    "approved",
    "scene_delta_written",
)

BLOCKED_FLAG_KEYS = (
    "gate_decision_hold_for_review",
    "write_allowed_false",
    "approval_not_granted",
    "candidate_not_fact",
    "review_required_before_write",
    "scene_delta_executor_must_not_run",
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

    paths = {
        "trace_stub": root / "cross_modal_scene_delta_executor_trace_stub.json",
        "matrix": root / "cross_modal_scene_delta_executor_planned_step_matrix.json",
        "blocked": root / "cross_modal_scene_delta_executor_blocked_reason_report.json",
        "compat": root / "cross_modal_scene_delta_executor_input_compatibility_report.json",
        "audit": root / "cross_modal_scene_delta_executor_trace_stub_audit_report.json",
        "summary": root / "cross_modal_scene_delta_executor_trace_stub_summary.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_scene_delta_executor_trace_stub_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Executor-Trace-Stub-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_scene_delta_executor_trace_stub_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    traces_doc = _read_json(paths["trace_stub"])
    matrix = _read_json(paths["matrix"])
    blocked = _read_json(paths["blocked"])
    compat_doc = _read_json(paths["compat"])
    aud = _read_json(paths["audit"])

    traces = traces_doc.get("traces") if isinstance(traces_doc.get("traces"), list) else []
    trace_count = int(traces_doc.get("trace_count") or len(traces))

    if not traces:
        soft.append("trace_count_zero")

    for i, tr in enumerate(traces):
        if not isinstance(tr, dict):
            blockers.append(f"trace_invalid:{i}")
            continue
        prefix = f"trace[{i}]"
        if tr.get("executor_mode") != "trace_stub_only":
            blockers.append(f"{prefix}:executor_mode_not_trace_stub_only")
        if tr.get("gate_status") != "evaluated_dry_run":
            blockers.append(f"{prefix}:gate_status_not_evaluated_dry_run")
        if tr.get("gate_decision") != "hold_for_review":
            blockers.append(f"{prefix}:gate_decision_not_hold_for_review")
        if tr.get("write_allowed") is not False:
            blockers.append(f"{prefix}:write_allowed_not_false")
        if tr.get("execution_status") != "blocked_by_gate":
            blockers.append(f"{prefix}:execution_status_not_blocked_by_gate")
        if tr.get("no_write_guarantee") is not True:
            blockers.append(f"{prefix}:no_write_guarantee_not_true")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if trace_count > 0 and not rows:
        blockers.append("planned_step_matrix_empty")

    for row in rows:
        if not isinstance(row, dict):
            continue
        status = str(row.get("status") or "")
        if status in FORBIDDEN_MATRIX_STATUSES:
            blockers.append(f"matrix:forbidden_status:{status}")

    flags = blocked.get("blocked_reason_flags") if isinstance(blocked.get("blocked_reason_flags"), dict) else {}
    for key in BLOCKED_FLAG_KEYS:
        if flags.get(key) is not True:
            blockers.append(f"blocked_flags:{key}")

    reports = compat_doc.get("reports") if isinstance(compat_doc.get("reports"), list) else []
    if trace_count > 0 and not reports:
        blockers.append("input_compatibility_reports_empty")
    for i, rep in enumerate(reports):
        if not isinstance(rep, dict):
            continue
        prefix = f"compat[{i}]"
        if rep.get("candidate_id_present") is not True:
            blockers.append(f"{prefix}:candidate_id_present_not_true")
        if rep.get("gate_eval_id_present") is not True:
            blockers.append(f"{prefix}:gate_eval_id_present_not_true")
        if rep.get("gate_status_evaluated_dry_run") is not True:
            blockers.append(f"{prefix}:gate_status_evaluated_dry_run_not_true")
        if rep.get("write_allowed_false") is not True:
            blockers.append(f"{prefix}:write_allowed_false_not_true")
        if rep.get("approval_granted_false") is not True:
            blockers.append(f"{prefix}:approval_granted_false_not_true")
        if rep.get("fact_status_not_fact") is not True:
            blockers.append(f"{prefix}:fact_status_not_fact_not_true")
        if rep.get("no_write_guarantee") is not True:
            blockers.append(f"{prefix}:no_write_guarantee_not_true")

    boundary = [
        ("real_scene_delta_executor_invoked", False),
        ("scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("database_write_invoked", False),
        ("wal_append_invoked", False),
        ("approval_granted", False),
        ("auto_approve_invoked", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("cross_modal_scene_delta_executor_trace_stub_generated") is not True:
        blockers.append("audit:cross_modal_scene_delta_executor_trace_stub_generated")
    if aud.get("executor_trace_stub_only") is not True:
        blockers.append("audit:executor_trace_stub_only")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif trace_count <= 0:
        verdict = "CONDITIONAL_GO"

    rep_out: Dict[str, Any] = {
        "schema": "cross_modal_scene_delta_executor_trace_stub_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Executor-Trace-Stub-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "trace_count": trace_count,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_scene_delta_executor_trace_stub_verifier_report.json", rep_out)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
