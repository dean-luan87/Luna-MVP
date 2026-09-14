# -*- coding: utf-8 -*-
"""Cross-modal Scene Delta executor trace stub (blocked_by_gate, no real executor).

Phase-CrossModal-Vision-OCR-Scene-Delta-Executor-Trace-Stub-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TRACE_SCHEMA = "cross_modal_scene_delta_executor_trace_stub_v0"
TRACES_DOC_SCHEMA = "cross_modal_scene_delta_executor_traces_v0"
STEP_MATRIX_SCHEMA = "cross_modal_scene_delta_executor_planned_step_matrix_v0"
BLOCKED_SCHEMA = "cross_modal_scene_delta_executor_blocked_reason_report_v0"
COMPAT_SCHEMA = "cross_modal_scene_delta_executor_input_compatibility_report_v0"
AUDIT_SCHEMA = "cross_modal_scene_delta_executor_trace_stub_audit_v0"
SUMMARY_SCHEMA = "cross_modal_scene_delta_executor_trace_stub_summary_v0"

FORBIDDEN_STEP_STATUSES = frozenset(
    {"executed_write", "committed", "approved", "scene_delta_written"}
)

PLANNED_STEPS_V0: List[Dict[str, str]] = [
    {"step": "validate_candidate", "status": "planned_only"},
    {"step": "validate_gate", "status": "planned_only"},
    {"step": "map_candidate_to_executor_payload", "status": "skipped_due_to_gate"},
    {"step": "block_write_due_to_gate", "status": "blocked_by_gate"},
    {"step": "emit_no_write_audit", "status": "planned_only"},
]

BLOCKED_REASON_FLAGS_V0: Dict[str, bool] = {
    "gate_decision_hold_for_review": True,
    "write_allowed_false": True,
    "approval_not_granted": True,
    "candidate_not_fact": True,
    "review_required_before_write": True,
    "scene_delta_executor_must_not_run": True,
}


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _load_scene_delta_candidates(root: Path) -> List[Dict[str, Any]]:
    p = root / "cross_modal_scene_delta_candidates.json"
    if not p.is_file():
        return []
    doc = _read_json(p)
    return [c for c in (doc.get("candidates") or []) if isinstance(c, dict)]


def _load_gate_results_by_candidate(root: Path) -> Dict[str, Dict[str, Any]]:
    p = root / "cross_modal_scene_delta_gate_evaluation_result.json"
    if not p.is_file():
        return {}
    doc = _read_json(p)
    out: Dict[str, Dict[str, Any]] = {}
    for r in doc.get("results") or []:
        if isinstance(r, dict):
            cid = str(r.get("source_candidate_id") or "")
            if cid:
                out[cid] = r
    return out


def build_executor_trace_stub_v0(
    sd_cand: Dict[str, Any],
    gate_eval: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": TRACE_SCHEMA,
        "trace_id": f"trace_{uuid.uuid4().hex[:16]}",
        "source_candidate_id": str(sd_cand.get("candidate_id") or ""),
        "source_gate_eval_id": str(gate_eval.get("gate_eval_id") or ""),
        "executor_mode": "trace_stub_only",
        "gate_status": str(gate_eval.get("gate_status") or ""),
        "gate_decision": str(gate_eval.get("decision") or ""),
        "write_allowed": False,
        "execution_status": "blocked_by_gate",
        "no_write_guarantee": True,
        "planned_steps": [
            {"step": "validate_candidate", "status": "planned_only"},
            {"step": "validate_gate", "status": "planned_only"},
            {"step": "block_write_due_to_gate", "status": "blocked_by_gate"},
            {"step": "emit_no_write_audit", "status": "planned_only"},
        ],
    }


def build_planned_step_matrix_rows_v0(
    trace: Dict[str, Any],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in PLANNED_STEPS_V0:
        rows.append(
            {
                "trace_id": trace.get("trace_id"),
                "source_candidate_id": trace.get("source_candidate_id"),
                "source_gate_eval_id": trace.get("source_gate_eval_id"),
                "step": spec["step"],
                "status": spec["status"],
            }
        )
    return rows


def build_blocked_reason_report_v0(*, trace_count: int) -> Dict[str, Any]:
    return {
        "schema_version": BLOCKED_SCHEMA,
        "trace_count": trace_count,
        "execution_status": "blocked_by_gate",
        "blocked_reason_flags": dict(BLOCKED_REASON_FLAGS_V0),
        "notes": [
            "Gate decision hold_for_review; write_allowed=false.",
            "Real Scene Delta executor must not run in this phase.",
        ],
    }


def build_input_compatibility_report_v0(
    sd_cand: Dict[str, Any],
    gate_eval: Dict[str, Any],
) -> Dict[str, Any]:
    candidate_id = str(sd_cand.get("candidate_id") or "")
    gate_eval_id = str(gate_eval.get("gate_eval_id") or "")
    return {
        "schema_version": COMPAT_SCHEMA,
        "source_candidate_id": candidate_id,
        "source_gate_eval_id": gate_eval_id,
        "candidate_id_present": bool(candidate_id),
        "gate_eval_id_present": bool(gate_eval_id),
        "gate_status": str(gate_eval.get("gate_status") or ""),
        "gate_status_evaluated_dry_run": gate_eval.get("gate_status") == "evaluated_dry_run",
        "write_allowed": bool(gate_eval.get("write_allowed")),
        "write_allowed_false": gate_eval.get("write_allowed") is False,
        "approval_granted": bool(gate_eval.get("approval_granted")),
        "approval_granted_false": gate_eval.get("approval_granted") is False,
        "fact_status": str(sd_cand.get("fact_status") or gate_eval.get("fact_status") or ""),
        "fact_status_not_fact": (
            sd_cand.get("fact_status") == "not_fact" and gate_eval.get("fact_status") == "not_fact"
        ),
        "no_write_guarantee": True,
        "compatible_for_trace_stub": (
            bool(candidate_id)
            and bool(gate_eval_id)
            and gate_eval.get("gate_status") == "evaluated_dry_run"
            and gate_eval.get("write_allowed") is False
            and gate_eval.get("approval_granted") is False
            and sd_cand.get("fact_status") == "not_fact"
        ),
    }


def build_trace_stub_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_scene_delta_executor_trace_stub_generated": True,
        "executor_trace_stub_only": True,
        "real_scene_delta_executor_invoked": False,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "database_write_invoked": False,
        "wal_append_invoked": False,
    }


def run_cross_modal_scene_delta_executor_trace_stub_v0(
    *,
    scene_delta_candidate_dryrun_root: str,
    gate_evaluator_dryrun_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[Dict[str, Any]],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    sd_root = Path(scene_delta_candidate_dryrun_root).resolve()
    gate_root = Path(gate_evaluator_dryrun_root).resolve()

    sd_candidates = _load_scene_delta_candidates(sd_root)
    gate_by_cand = _load_gate_results_by_candidate(gate_root)

    if not sd_candidates:
        errs.append(f"missing_or_empty:scene_delta_candidates:{sd_root}")
    if not gate_by_cand:
        errs.append(f"missing_or_empty:gate_evaluation_results:{gate_root}")

    traces: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    compat_reports: List[Dict[str, Any]] = []

    for sd in sd_candidates:
        cid = str(sd.get("candidate_id") or "")
        gate_eval = gate_by_cand.get(cid)
        if not gate_eval:
            errs.append(f"gate_eval_not_found:{cid}")
            continue
        if gate_eval.get("write_allowed") is not False:
            errs.append(f"gate_write_allowed_not_false:{cid}")
            continue
        trace = build_executor_trace_stub_v0(sd, gate_eval)
        traces.append(trace)
        matrix_rows.extend(build_planned_step_matrix_rows_v0(trace))
        compat_reports.append(build_input_compatibility_report_v0(sd, gate_eval))

    blocked = build_blocked_reason_report_v0(trace_count=len(traces))
    audit = build_trace_stub_audit_v0()

    phase_verdict = "GO"
    if not traces and not errs:
        phase_verdict = "CONDITIONAL_GO"
    if errs and not traces:
        phase_verdict = "NO_GO"
    elif errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Executor-Trace-Stub-001",
        "scene_delta_candidate_dryrun_root": str(sd_root),
        "gate_evaluator_dryrun_root": str(gate_root),
        "trace_count": len(traces),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    traces_doc = {
        "schema_version": TRACES_DOC_SCHEMA,
        "trace_count": len(traces),
        "traces": traces,
    }
    matrix_doc = {
        "schema_version": STEP_MATRIX_SCHEMA,
        "row_count": len(matrix_rows),
        "rows": matrix_rows,
    }

    compat_doc = {
        "schema_version": "cross_modal_scene_delta_executor_input_compatibility_reports_v0",
        "report_count": len(compat_reports),
        "reports": compat_reports,
    }

    return summary, traces_doc, matrix_doc, blocked, compat_doc, audit, errs


def matrix_has_forbidden_status(matrix_doc: Dict[str, Any]) -> List[str]:
    violations: List[str] = []
    for row in matrix_doc.get("rows") or []:
        if not isinstance(row, dict):
            continue
        status = str(row.get("status") or "")
        if status in FORBIDDEN_STEP_STATUSES:
            violations.append(f"forbidden_status:{status}")
    return violations
