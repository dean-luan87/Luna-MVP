# -*- coding: utf-8 -*-
"""Cross-modal Scene Delta gate evaluator dry-run (evaluate only, no write).

Phase-CrossModal-Vision-OCR-Scene-Delta-Gate-Evaluator-DryRun-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

RESULT_SCHEMA = "cross_modal_scene_delta_gate_evaluation_result_v0"
RESULTS_DOC_SCHEMA = "cross_modal_scene_delta_gate_evaluation_results_v0"
REASON_MATRIX_SCHEMA = "cross_modal_scene_delta_gate_reason_matrix_v0"
POLICY_SCHEMA = "cross_modal_scene_delta_gate_policy_report_v0"
CHAIN_SCHEMA = "cross_modal_scene_delta_gate_source_chain_summary_v0"
AUDIT_SCHEMA = "cross_modal_scene_delta_gate_evaluator_audit_v0"
SUMMARY_SCHEMA = "cross_modal_scene_delta_gate_evaluation_summary_v0"

FORBIDDEN_ACTIONS_V0: Dict[str, bool] = {
    "write_scene_delta": True,
    "write_midplatform_fact": True,
    "write_world_model": True,
    "invoke_navigation_decision": True,
    "auto_approve": True,
    "claim_confirmed_fact": True,
}

DECISION_REASON_CODES_V0: List[str] = [
    "candidate_not_fact",
    "source_ai_interpretation_dryrun_only",
    "spatial_association_not_semantic_truth",
    "manual_or_policy_review_required",
]

REASON_MATRIX_SPECS_V0: List[Dict[str, Any]] = [
    {
        "reason_code": "candidate_not_fact",
        "severity": "high",
        "blocking": True,
        "explanation": "Scene Delta candidate remains not_fact; cannot authorize write.",
    },
    {
        "reason_code": "gate_dryrun_only",
        "severity": "medium",
        "blocking": True,
        "explanation": "Gate evaluation is dry-run only; no production gate commit.",
    },
    {
        "reason_code": "ai_interpretation_not_fact",
        "severity": "high",
        "blocking": True,
        "explanation": "AI interpretation is template dry-run, not confirmed semantic truth.",
    },
    {
        "reason_code": "ocr_text_not_fact",
        "severity": "medium",
        "blocking": True,
        "explanation": "OCR text is evidence only, not a confirmed fact.",
    },
    {
        "reason_code": "spatial_association_not_semantic_truth",
        "severity": "medium",
        "blocking": True,
        "explanation": "Spatial association hypothesis is not semantic truth.",
    },
    {
        "reason_code": "review_required_before_write",
        "severity": "high",
        "blocking": True,
        "explanation": "Human or policy review required before any write path.",
    },
]


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _file_ref(root: Path, name: str) -> Optional[str]:
    p = root / name
    return str(p.resolve()) if p.is_file() else None


def build_gate_evaluation_result_v0(sd_cand: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": RESULT_SCHEMA,
        "gate_eval_id": f"gate_eval_{uuid.uuid4().hex[:16]}",
        "source_candidate_id": str(sd_cand.get("candidate_id") or ""),
        "evaluation_scope": "dry_run_only",
        "gate_status": "evaluated_dry_run",
        "write_allowed": False,
        "approval_granted": False,
        "requires_human_or_policy_review": True,
        "fact_status": "not_fact",
        "decision": "hold_for_review",
        "decision_reason_codes": list(DECISION_REASON_CODES_V0),
        "forbidden_actions": dict(FORBIDDEN_ACTIONS_V0),
    }


def build_reason_matrix_rows_v0(
    gate_eval: Dict[str, Any],
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for spec in REASON_MATRIX_SPECS_V0:
        rows.append(
            {
                "gate_eval_id": gate_eval.get("gate_eval_id"),
                "source_candidate_id": gate_eval.get("source_candidate_id"),
                "reason_code": spec["reason_code"],
                "severity": spec["severity"],
                "blocking": spec["blocking"],
                "explanation": spec["explanation"],
                "write_allowed": False,
            }
        )
    return rows


def build_gate_policy_report_v0(*, evaluation_count: int) -> Dict[str, Any]:
    return {
        "schema_version": POLICY_SCHEMA,
        "evaluation_count": evaluation_count,
        "gate_evaluated": evaluation_count > 0,
        "gate_evaluation_scope": "dry_run_only",
        "write_allowed": False,
        "approval_granted": False,
        "human_or_policy_review_required": True,
        "auto_approve_allowed": False,
        "scene_delta_executor_must_not_run": True,
    }


def build_source_chain_summary_v0(*, scene_delta_candidate_root: Path) -> Dict[str, Any]:
    root = scene_delta_candidate_root.resolve()
    return {
        "schema_version": CHAIN_SCHEMA,
        "scene_delta_candidate_dryrun_root": str(root),
        "source_chain_steps": [
            {
                "step": "scene_delta_candidate_dryrun",
                "root": str(root),
                "artifacts": {
                    "scene_delta_candidates": _file_ref(root, "cross_modal_scene_delta_candidates.json"),
                    "gate_stub": _file_ref(root, "cross_modal_scene_delta_gate_stub.json"),
                    "risk_report": _file_ref(root, "cross_modal_scene_delta_risk_report.json"),
                },
            },
            {
                "step": "gate_evaluator_dryrun_build",
                "description": "cross_modal_scene_delta_gate_evaluator_dryrun_v0",
            },
        ],
    }


def build_evaluator_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_scene_delta_gate_evaluator_dryrun_executed": True,
        "dry_run_only": True,
        "gate_evaluated": True,
        "write_allowed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "ai_interpretation_invoked": False,
        "rapidocr_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
    }


def run_cross_modal_scene_delta_gate_evaluator_dryrun_v0(
    *,
    scene_delta_candidate_dryrun_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    root = Path(scene_delta_candidate_dryrun_root).resolve()

    cand_path = root / "cross_modal_scene_delta_candidates.json"
    gate_path = root / "cross_modal_scene_delta_gate_stub.json"
    risk_path = root / "cross_modal_scene_delta_risk_report.json"

    for label, p in (
        ("scene_delta_candidates", cand_path),
        ("gate_stub", gate_path),
        ("risk_report", risk_path),
    ):
        if not p.is_file():
            errs.append(f"missing:{label}:{p}")

    sd_candidates: List[Dict[str, Any]] = []
    if cand_path.is_file():
        doc = _read_json(cand_path)
        sd_candidates = [c for c in (doc.get("candidates") or []) if isinstance(c, dict)]

    results: List[Dict[str, Any]] = []
    reason_rows: List[Dict[str, Any]] = []

    for sd in sd_candidates:
        if sd.get("candidate_scope") != "dry_run_only":
            errs.append(f"candidate_scope_not_dry_run:{sd.get('candidate_id')}")
            continue
        gate_eval = build_gate_evaluation_result_v0(sd)
        results.append(gate_eval)
        reason_rows.extend(build_reason_matrix_rows_v0(gate_eval))

    policy = build_gate_policy_report_v0(evaluation_count=len(results))
    chain = build_source_chain_summary_v0(scene_delta_candidate_root=root)
    audit = build_evaluator_audit_v0()

    phase_verdict = "GO"
    if not results and not errs:
        phase_verdict = "CONDITIONAL_GO"
    if errs and not results:
        phase_verdict = "NO_GO"
    elif errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Gate-Evaluator-DryRun-001",
        "scene_delta_candidate_dryrun_root": str(root),
        "evaluation_count": len(results),
        "reason_matrix_row_count": len(reason_rows),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    result_doc = {
        "schema_version": RESULTS_DOC_SCHEMA,
        "evaluation_count": len(results),
        "results": results,
    }
    reason_matrix_doc = {
        "schema_version": REASON_MATRIX_SCHEMA,
        "row_count": len(reason_rows),
        "rows": reason_rows,
    }

    return summary, result_doc, reason_matrix_doc, policy, chain, audit, errs
