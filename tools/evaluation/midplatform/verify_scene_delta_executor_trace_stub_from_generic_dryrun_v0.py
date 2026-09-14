#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for generic Scene Delta executor trace stub from dry-run smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

TRACE_GENERIC_SCHEMA = "scene_delta_executor_trace_stub_generic_v0"
SUMMARY_SCHEMA_VERSION = "scene_delta_executor_trace_stub_generic_summary_v0"
FORBIDDEN_STATUSES = frozenset({"executed_write", "committed", "approved"})
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    sum_p = root / "scene_delta_executor_trace_stub_generic_summary.json"
    tr_p = root / "scene_delta_executor_trace_stub_generic.json"
    mat_p = root / "scene_delta_executor_planned_step_matrix_generic.json"
    comp_p = root / "scene_delta_executor_input_compatibility_report_generic.json"
    aud_p = root / "scene_delta_executor_trace_stub_generic_audit_report.json"

    for label, p in (
        ("trace_stub_generic_summary", sum_p),
        ("trace_stub_generic", tr_p),
        ("planned_step_matrix_generic", mat_p),
        ("input_compatibility_generic", comp_p),
        ("trace_stub_generic_audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "scene_delta_executor_trace_stub_generic_verifier_report_v0",
            "phase": "Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "scene_delta_executor_trace_stub_generic_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    summ: Dict[str, Any] = _read_json(sum_p)
    tr: Dict[str, Any] = _read_json(tr_p)
    aud: Dict[str, Any] = _read_json(aud_p)
    mat: Dict[str, Any] = _read_json(mat_p)
    comp: Dict[str, Any] = _read_json(comp_p)

    if str(summ.get("schema_version") or "") != SUMMARY_SCHEMA_VERSION:
        blockers.append("summary_schema_version_mismatch")

    if str(tr.get("schema_version") or "") != TRACE_GENERIC_SCHEMA:
        blockers.append("trace_stub_schema_mismatch")
    if str(tr.get("source_type") or "") not in SUPPORTED_SOURCE_TYPES:
        blockers.append("source_type_must_be_ocr_or_vision")
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
    else:
        for step in ps:
            if not isinstance(step, dict):
                continue
            st = str(step.get("status") or "")
            if st in FORBIDDEN_STATUSES:
                blockers.append(f"forbidden_trace_step_status:{step.get('step')}:{st}")

    rows = mat.get("rows")
    if not isinstance(rows, list) or not rows:
        blockers.append("planned_step_matrix_rows_missing")
    else:
        for row in rows:
            if not isinstance(row, dict):
                continue
            st = str(row.get("status") or "")
            if st in FORBIDDEN_STATUSES:
                blockers.append(f"forbidden_matrix_step_status:{row.get('step')}:{st}")

    if str(tr.get("gate_status") or "") != "not_evaluated":
        blockers.append("gate_status_must_be_not_evaluated")

    rc = tr.get("risk_codes")
    if not isinstance(rc, list) or len(rc) < 1:
        blockers.append("risk_codes_must_be_non_empty")

    for k, must in (
        ("executor_trace_stub_generated", True),
        ("scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("database_write_invoked", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("real_vision_provider_invoked", False),
        ("yolo_invoked", False),
        ("supervision_mainline_invoked", False),
        ("vlm_invoked", False),
        ("ocr_provider_invoked", False),
        ("ocr_routing_changed", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if not isinstance(comp, dict) or not comp:
        blockers.append("input_compatibility_report_empty")
    elif comp.get("overall_compatible") is not True:
        blockers.append("input_compatibility_overall_not_compatible")

    if not blockers:
        verdict = "GO"
        if isinstance(rows, list) and len(rows) < 8:
            verdict = "CONDITIONAL_GO"
            soft.append("planned_step_matrix_row_count_lt_8")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "scene_delta_executor_trace_stub_generic_verifier_report_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "trace_id": tr.get("trace_id"),
        "source_type": tr.get("source_type"),
    }
    _write_json(root / "scene_delta_executor_trace_stub_generic_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
