# -*- coding: utf-8 -*-
"""Scene Delta executor trace stub from dry-run outputs (no real executor, no writes).

Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

TRACE_STUB_SCHEMA = "scene_delta_executor_trace_stub_v0"
PLANNED_STEP_MATRIX_SCHEMA = "scene_delta_executor_planned_step_matrix_v0"
INPUT_COMPAT_SCHEMA = "scene_delta_executor_input_compatibility_report_v0"
TRACE_STUB_AUDIT_SCHEMA = "scene_delta_executor_trace_stub_audit_v0"

ALLOWED_STEP_STATUSES = frozenset({"planned_only", "blocked_by_policy", "skipped_no_write"})
FORBIDDEN_STEP_STATUSES = frozenset({"executed_write", "committed", "approved"})

TRACE_STUB_PLANNED_STEPS: List[Dict[str, str]] = [
    {"step": "validate_candidate", "status": "planned_only"},
    {"step": "validate_gate", "status": "planned_only"},
    {"step": "map_ocr_evidence_to_scene_delta", "status": "planned_only"},
    {"step": "reject_write_due_to_gate_not_evaluated", "status": "planned_only"},
]

PLANNED_STEP_MATRIX_ROWS: List[Tuple[str, str]] = [
    ("validate_candidate", "planned_only"),
    ("validate_field_completeness", "planned_only"),
    ("validate_gate_status", "planned_only"),
    ("validate_fact_status_not_fact", "planned_only"),
    ("validate_no_ai_interpretation", "planned_only"),
    ("map_evidence", "planned_only"),
    ("block_write", "blocked_by_policy"),
    ("emit_audit", "skipped_no_write"),
]


def _risk_codes_from_report(risk_report: Any) -> List[str]:
    if not isinstance(risk_report, dict):
        return []
    risks = risk_report.get("risks")
    if not isinstance(risks, list):
        return []
    out: List[str] = []
    for r in risks:
        if isinstance(r, dict) and r.get("code"):
            out.append(str(r["code"]))
    return out


def build_planned_step_matrix_v0() -> Dict[str, Any]:
    rows = [{"step": s, "status": st} for s, st in PLANNED_STEP_MATRIX_ROWS]
    return {"schema": PLANNED_STEP_MATRIX_SCHEMA, "rows": rows}


def build_executor_trace_stub_v0(
    *,
    dry_run_summary: Dict[str, Any],
    risk_report: Dict[str, Any],
    gate_status: str,
) -> Dict[str, Any]:
    risk_codes = _risk_codes_from_report(risk_report)
    return {
        "schema_version": TRACE_STUB_SCHEMA,
        "trace_id": f"trace_sd_exec_{uuid.uuid4().hex}",
        "source_dry_run_id": str(dry_run_summary.get("dry_run_id") or ""),
        "source_candidate_id": str(dry_run_summary.get("source_candidate_id") or ""),
        "executor_mode": "trace_stub_only",
        "executor_invoked": False,
        "write_intent": "not_allowed",
        "write_allowed": False,
        "gate_status": str(gate_status or "not_evaluated"),
        "risk_codes": risk_codes,
        "planned_steps": list(TRACE_STUB_PLANNED_STEPS),
        "no_write_guarantee": True,
    }


def build_input_compatibility_report_v0(
    *,
    candidate: Dict[str, Any],
    dry_run_summary: Dict[str, Any],
    mapping_matrix: Any,
    risk_report: Any,
    gate_status: str,
) -> Dict[str, Any]:
    items = candidate.get("evidence_items") if isinstance(candidate.get("evidence_items"), list) else []
    fact_all_not_fact = True
    for it in items:
        if not isinstance(it, dict):
            continue
        if str(it.get("fact_status") or "") != "not_fact":
            fact_all_not_fact = False
            break

    mm_ok = isinstance(mapping_matrix, dict) and bool(mapping_matrix.get("rows"))

    return {
        "schema": INPUT_COMPAT_SCHEMA,
        "candidate_id_present": bool(str(candidate.get("candidate_id") or "").strip()),
        "evidence_items_present": len(items) > 0,
        "mapping_matrix_present": mm_ok,
        "gate_status_present": bool(str(gate_status or "").strip()),
        "risk_report_present": isinstance(risk_report, dict) and isinstance(risk_report.get("risks"), list),
        "write_allowed": bool(candidate.get("write_allowed")),
        "write_allowed_is_false": candidate.get("write_allowed") is False,
        "fact_status_not_fact_all_evidence": fact_all_not_fact,
        "dry_run_summary_present": isinstance(dry_run_summary, dict) and bool(dry_run_summary.get("dry_run_id")),
    }


def build_executor_trace_stub_audit_v0() -> Dict[str, Any]:
    return {
        "schema": TRACE_STUB_AUDIT_SCHEMA,
        "executor_trace_stub_generated": True,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "database_write_invoked": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_routing_changed": False,
    }


def run_executor_trace_stub_from_dryrun_v0(
    *,
    dry_run_summary: Dict[str, Any],
    mapping_matrix: Dict[str, Any],
    risk_report: Dict[str, Any],
    write_candidate: Dict[str, Any],
    gate_stub: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    """Returns (summary, trace_stub, step_matrix, compat_report, audit, errors)."""
    errs: List[str] = []

    if str(dry_run_summary.get("schema") or "") != "scene_delta_write_candidate_dryrun_summary_v0":
        errs.append("unexpected_dryrun_summary_schema")

    gate_status = str(gate_stub.get("gate_status") or "")

    trace = build_executor_trace_stub_v0(dry_run_summary=dry_run_summary, risk_report=risk_report, gate_status=gate_status)
    matrix = build_planned_step_matrix_v0()
    compat = build_input_compatibility_report_v0(
        candidate=write_candidate,
        dry_run_summary=dry_run_summary,
        mapping_matrix=mapping_matrix,
        risk_report=risk_report,
        gate_status=gate_status,
    )
    audit = build_executor_trace_stub_audit_v0()

    summary = {
        "schema": "scene_delta_executor_trace_stub_summary_v0",
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-DryRun-001",
        "input_dry_run_root": None,
        "trace_id": trace.get("trace_id"),
        "source_dry_run_id": trace.get("source_dry_run_id"),
        "source_candidate_id": trace.get("source_candidate_id"),
        "executor_mode": trace.get("executor_mode"),
        "validation_errors": list(errs),
    }

    return summary, trace, matrix, compat, audit, errs
