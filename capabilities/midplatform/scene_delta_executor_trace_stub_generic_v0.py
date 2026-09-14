# -*- coding: utf-8 -*-
"""Scene Delta executor trace stub from generic dry-run (OCR + Vision).

Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

TRACE_STUB_GENERIC_SCHEMA = "scene_delta_executor_trace_stub_generic_v0"
PLANNED_STEP_MATRIX_GENERIC_SCHEMA = "scene_delta_executor_planned_step_matrix_generic_v0"
INPUT_COMPAT_GENERIC_SCHEMA = "scene_delta_executor_input_compatibility_report_generic_v0"
TRACE_STUB_GENERIC_AUDIT_SCHEMA = "scene_delta_executor_trace_stub_generic_audit_v0"
GENERIC_SUMMARY_SCHEMA_VERSION = "scene_delta_executor_trace_stub_generic_summary_v0"

FORBIDDEN_STEP_STATUSES = frozenset({"executed_write", "committed", "approved"})

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

TRACE_PLANNED_STEPS: List[Dict[str, str]] = [
    {"step": "validate_candidate", "status": "planned_only"},
    {"step": "validate_gate", "status": "planned_only"},
    {"step": "map_evidence_to_scene_delta", "status": "planned_only"},
    {"step": "reject_write_due_to_gate_not_evaluated", "status": "planned_only"},
]

VISION_SUMMARY_FILE = "scene_delta_write_candidate_dryrun_from_vision_summary.json"
VISION_SUMMARY_SCHEMA = "scene_delta_write_candidate_dryrun_from_vision_summary_v0"
OCR_SUMMARY_FILE = "scene_delta_write_candidate_dryrun_summary.json"
OCR_SUMMARY_SCHEMA = "scene_delta_write_candidate_dryrun_summary_v0"


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


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


def resolve_dry_run_bundle(dry_run_root: Path) -> Tuple[str, Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Path, Path, Path]:
    """
    Returns (flavor, dry_summary, mapping_matrix, risk_report, no_write_audit, map_p, risk_p, nw_p).
    flavor is 'vision' or 'ocr'.
    """
    root = dry_run_root.resolve()
    v_sum_p = root / VISION_SUMMARY_FILE
    o_sum_p = root / OCR_SUMMARY_FILE

    if v_sum_p.is_file():
        dry_summary = _read_json(v_sum_p)
        if isinstance(dry_summary, dict) and str(dry_summary.get("schema_version") or "") == VISION_SUMMARY_SCHEMA:
            map_p = root / "scene_delta_write_candidate_from_vision_mapping_matrix.json"
            risk_p = root / "scene_delta_write_candidate_from_vision_risk_report.json"
            nw_p = root / "scene_delta_write_candidate_from_vision_no_write_audit_report.json"
            if not map_p.is_file() or not risk_p.is_file() or not nw_p.is_file():
                raise FileNotFoundError(f"vision dry-run companion files missing under {root}")
            return (
                "vision",
                dry_summary,
                _read_json(map_p),
                _read_json(risk_p),
                _read_json(nw_p),
                map_p,
                risk_p,
                nw_p,
            )

    if o_sum_p.is_file():
        dry_summary = _read_json(o_sum_p)
        if isinstance(dry_summary, dict) and str(dry_summary.get("schema") or "") == OCR_SUMMARY_SCHEMA:
            map_p = root / "scene_delta_write_candidate_mapping_matrix.json"
            risk_p = root / "scene_delta_write_candidate_risk_report.json"
            nw_p = root / "scene_delta_write_candidate_no_write_audit_report.json"
            if not map_p.is_file() or not risk_p.is_file() or not nw_p.is_file():
                raise FileNotFoundError(f"ocr dry-run companion files missing under {root}")
            return (
                "ocr",
                dry_summary,
                _read_json(map_p),
                _read_json(risk_p),
                _read_json(nw_p),
                map_p,
                risk_p,
                nw_p,
            )

    raise ValueError(
        f"unrecognized dry-run root {root}: need {VISION_SUMMARY_FILE} ({VISION_SUMMARY_SCHEMA}) "
        f"or {OCR_SUMMARY_FILE} ({OCR_SUMMARY_SCHEMA})"
    )


def load_write_candidate_and_gate(
    dry_summary: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    paths = dry_summary.get("paths") if isinstance(dry_summary.get("paths"), dict) else {}
    cand_s = str(paths.get("write_candidate_json") or "").strip()
    gate_s = str(paths.get("gate_stub_json") or "").strip()
    if not cand_s or not Path(cand_s).is_file():
        raise FileNotFoundError("dry-run summary paths.write_candidate_json missing or not a file")
    if not gate_s or not Path(gate_s).is_file():
        raise FileNotFoundError("dry-run summary paths.gate_stub_json missing or not a file")
    return _read_json(Path(cand_s)), _read_json(Path(gate_s))


def build_dry_run_loader_dict(
    *,
    flavor: str,
    dry_summary: Dict[str, Any],
    mapping_matrix_path: str,
    risk_report_path: str,
    no_write_audit_path: str,
    source_type: str,
) -> Dict[str, Any]:
    items = dry_summary.get("evidence_items") if isinstance(dry_summary.get("evidence_items"), list) else None
    ec = int(dry_summary.get("evidence_count") or 0)
    if ec < 1 and items is not None:
        ec = len(items)
    return {
        "dry_run_id": str(dry_summary.get("dry_run_id") or ""),
        "source_candidate_id": str(dry_summary.get("source_candidate_id") or ""),
        "source_type": source_type,
        "evidence_count": ec,
        "write_would_be_allowed": dry_summary.get("write_would_be_allowed", False),
        "executor_invoked": dry_summary.get("executor_invoked", False),
        "database_write_invoked": dry_summary.get("database_write_invoked", False),
        "mapping_matrix_path": mapping_matrix_path,
        "risk_report_path": risk_report_path,
        "no_write_audit_path": no_write_audit_path,
        "dry_run_flavor": flavor,
    }


def resolve_source_type(candidate: Dict[str, Any], flavor: str) -> str:
    st = str(candidate.get("source_type") or "").strip()
    if st in ("ocr_evidence", "vision_recognition_evidence"):
        return st
    if flavor == "vision":
        return "vision_recognition_evidence"
    if flavor == "ocr":
        return "ocr_evidence"
    return st or "unknown"


def build_executor_trace_stub_generic_v0(
    *,
    dry_run_summary: Dict[str, Any],
    risk_report: Dict[str, Any],
    gate_status: str,
    source_type: str,
) -> Dict[str, Any]:
    risk_codes = _risk_codes_from_report(risk_report)
    return {
        "schema_version": TRACE_STUB_GENERIC_SCHEMA,
        "trace_id": f"trace_sd_exec_generic_{uuid.uuid4().hex}",
        "source_dry_run_id": str(dry_run_summary.get("dry_run_id") or ""),
        "source_candidate_id": str(dry_run_summary.get("source_candidate_id") or ""),
        "source_type": source_type,
        "executor_mode": "trace_stub_only",
        "executor_invoked": False,
        "write_intent": "not_allowed",
        "write_allowed": False,
        "gate_status": str(gate_status or "not_evaluated"),
        "risk_codes": risk_codes,
        "planned_steps": [dict(x) for x in TRACE_PLANNED_STEPS],
        "no_write_guarantee": True,
    }


def build_planned_step_matrix_generic_v0() -> Dict[str, Any]:
    rows = [{"step": s, "status": st} for s, st in PLANNED_STEP_MATRIX_ROWS]
    return {"schema": PLANNED_STEP_MATRIX_GENERIC_SCHEMA, "rows": rows}


def _nw_false(nw: Dict[str, Any], key: str, default_if_missing: bool = True) -> bool:
    if key not in nw:
        return default_if_missing
    return nw.get(key) is False


def build_input_compatibility_report_generic_v0(
    *,
    flavor: str,
    candidate: Dict[str, Any],
    dry_run_summary: Dict[str, Any],
    mapping_matrix: Any,
    risk_report: Any,
    no_write_audit: Dict[str, Any],
    gate_status: str,
    source_type: str,
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
    ec = int(dry_run_summary.get("evidence_count") or len(items))

    base: Dict[str, Any] = {
        "schema": INPUT_COMPAT_GENERIC_SCHEMA,
        "candidate_id_present": bool(str(candidate.get("candidate_id") or "").strip()),
        "evidence_count_positive": ec > 0,
        "mapping_matrix_present": mm_ok,
        "risk_report_present": isinstance(risk_report, dict) and isinstance(risk_report.get("risks"), list),
        "no_write_audit_present": isinstance(no_write_audit, dict) and len(no_write_audit) > 0,
        "write_allowed_is_false": candidate.get("write_allowed") is False,
        "executor_invoked_false": dry_run_summary.get("executor_invoked") is False,
        "database_write_invoked_false": dry_run_summary.get("database_write_invoked") is False,
        "source_type_supported": source_type in ("ocr_evidence", "vision_recognition_evidence"),
        "gate_status_present": bool(str(gate_status or "").strip()),
        "fact_status_not_fact_all_evidence": fact_all_not_fact,
        "dry_run_summary_present": isinstance(dry_run_summary, dict) and bool(dry_run_summary.get("dry_run_id")),
    }

    if flavor == "vision":
        base["navigation_decision_invoked_false"] = _nw_false(no_write_audit, "navigation_decision_invoked", True)
        base["real_vision_provider_invoked_false"] = _nw_false(no_write_audit, "real_vision_provider_invoked", True)
        base["yolo_invoked_false"] = _nw_false(no_write_audit, "yolo_invoked", True)
        base["supervision_mainline_invoked_false"] = _nw_false(no_write_audit, "supervision_mainline_invoked", True)
        base["vlm_invoked_false"] = _nw_false(no_write_audit, "vlm_invoked", True)
        base["ocr_provider_invoked_false"] = True
        base["ocr_routing_changed_false"] = True
    else:
        base["navigation_decision_invoked_false"] = True
        base["real_vision_provider_invoked_false"] = True
        base["yolo_invoked_false"] = True
        base["supervision_mainline_invoked_false"] = True
        base["vlm_invoked_false"] = True
        base["ocr_provider_invoked_false"] = _nw_false(no_write_audit, "ocr_provider_invoked", True)
        base["ocr_routing_changed_false"] = _nw_false(no_write_audit, "ocr_routing_changed", True)

    overall = all(v is True for k, v in base.items() if k != "schema")
    base["overall_compatible"] = overall
    return base


def build_executor_trace_stub_generic_audit_v0() -> Dict[str, Any]:
    return {
        "schema": TRACE_STUB_GENERIC_AUDIT_SCHEMA,
        "executor_trace_stub_generated": True,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "database_write_invoked": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "real_vision_provider_invoked": False,
        "yolo_invoked": False,
        "supervision_mainline_invoked": False,
        "vlm_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_routing_changed": False,
    }


def run_executor_trace_stub_from_generic_dryrun_v0(
    *,
    dry_run_root: str,
    dry_summary: Dict[str, Any],
    flavor: str,
    mapping_matrix: Dict[str, Any],
    risk_report: Dict[str, Any],
    no_write_audit: Dict[str, Any],
    mapping_matrix_path: str,
    risk_report_path: str,
    no_write_audit_path: str,
    write_candidate: Dict[str, Any],
    gate_stub: Dict[str, Any],
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    """Returns (summary, trace_stub, step_matrix, compat_report, audit, errors)."""
    errs: List[str] = []
    gate_status = str(gate_stub.get("gate_status") or "")

    source_type = resolve_source_type(write_candidate, flavor)
    if source_type not in ("ocr_evidence", "vision_recognition_evidence"):
        errs.append("unsupported_source_type")

    loader = build_dry_run_loader_dict(
        flavor=flavor,
        dry_summary=dry_summary,
        mapping_matrix_path=mapping_matrix_path,
        risk_report_path=risk_report_path,
        no_write_audit_path=no_write_audit_path,
        source_type=source_type,
    )

    trace = build_executor_trace_stub_generic_v0(
        dry_run_summary=dry_summary,
        risk_report=risk_report,
        gate_status=gate_status,
        source_type=source_type,
    )
    matrix = build_planned_step_matrix_generic_v0()
    compat = build_input_compatibility_report_generic_v0(
        flavor=flavor,
        candidate=write_candidate,
        dry_run_summary=dry_summary,
        mapping_matrix=mapping_matrix,
        risk_report=risk_report,
        no_write_audit=no_write_audit if isinstance(no_write_audit, dict) else {},
        gate_status=gate_status,
        source_type=source_type,
    )
    audit = build_executor_trace_stub_generic_audit_v0()

    summary = {
        "schema_version": GENERIC_SUMMARY_SCHEMA_VERSION,
        "phase": "Phase-MidPlatform-Scene-Delta-Executor-Trace-Stub-From-Generic-DryRun-001",
        "input_dry_run_root": dry_run_root,
        "dry_run_flavor": flavor,
        "dry_run_loader": loader,
        "trace_id": trace.get("trace_id"),
        "source_dry_run_id": trace.get("source_dry_run_id"),
        "source_candidate_id": trace.get("source_candidate_id"),
        "source_type": source_type,
        "executor_mode": trace.get("executor_mode"),
        "validation_errors": list(errs),
    }

    return summary, trace, matrix, compat, audit, errs
