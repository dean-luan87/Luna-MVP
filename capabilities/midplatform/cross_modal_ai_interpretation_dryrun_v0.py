# -*- coding: utf-8 -*-
"""Cross-modal AI interpretation dry-run (template stub only, no external LLM).

Phase-CrossModal-Vision-OCR-AI-Interpretation-DryRun-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

INTERPRETATION_SCHEMA = "cross_modal_ai_interpretation_candidate_v0"
CANDIDATES_DOC_SCHEMA = "cross_modal_ai_interpretation_candidates_v0"
MATRIX_SCHEMA = "cross_modal_ai_interpretation_matrix_v0"
RISK_SCHEMA = "cross_modal_ai_interpretation_risk_report_v0"
POLICY_SCHEMA = "cross_modal_ai_interpretation_policy_report_v0"
AUDIT_SCHEMA = "cross_modal_ai_interpretation_dryrun_audit_v0"
SUMMARY_SCHEMA = "cross_modal_ai_interpretation_dryrun_summary_v0"

FORBIDDEN_ACTIONS_V0: Dict[str, bool] = {
    "write_midplatform_fact": True,
    "write_scene_delta": True,
    "write_world_model": True,
    "invoke_navigation_decision": True,
    "auto_approve": True,
    "claim_confirmed_fact": True,
}

RISK_FLAGS_V0: Dict[str, bool] = {
    "ai_interpretation_not_fact": True,
    "template_interpretation_not_llm_truth": True,
    "ocr_text_not_fact": True,
    "visual_roi_not_fact": True,
    "fusion_candidate_not_confirmed": True,
    "no_auto_approval": True,
    "no_midplatform_fact_write": True,
    "no_scene_delta_write": True,
    "no_world_model_write": True,
    "no_navigation_decision": True,
}

TEMPLATE_SUMMARY_EN = (
    "OCR text appears spatially associated with the selected visual ROI."
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _load_fusion_candidates_by_id(fusion_dryrun_root: Path) -> Dict[str, Dict[str, Any]]:
    p = fusion_dryrun_root / "cross_modal_vision_ocr_fusion_candidates.json"
    if not p.is_file():
        return {}
    doc = _read_json(p)
    out: Dict[str, Dict[str, Any]] = {}
    for c in doc.get("candidates") or []:
        if isinstance(c, dict):
            cid = str(c.get("candidate_id") or "")
            if cid:
                out[cid] = c
    return out


def build_template_interpretation_candidate_v0(
    queue_item: Dict[str, Any],
    fusion_cand: Dict[str, Any],
) -> Dict[str, Any]:
    ocr_ref = fusion_cand.get("ocr_reference") if isinstance(fusion_cand.get("ocr_reference"), dict) else {}
    hyp = fusion_cand.get("fusion_hypothesis") if isinstance(fusion_cand.get("fusion_hypothesis"), dict) else {}
    text_joined = str(ocr_ref.get("text_joined") or "")
    hyp_type = str(hyp.get("type") or "text_in_visual_roi_candidate")
    roi_type = str(fusion_cand.get("roi_type") or queue_item.get("roi_type") or "upper_sign_roi")

    return {
        "schema_version": INTERPRETATION_SCHEMA,
        "interpretation_id": f"interp_{uuid.uuid4().hex[:16]}",
        "source_queue_item_id": str(queue_item.get("queue_item_id") or ""),
        "source_candidate_id": str(queue_item.get("source_candidate_id") or fusion_cand.get("candidate_id") or ""),
        "interpretation_scope": "dry_run_only",
        "interpretation_mode": "template_stub",
        "input_summary": {
            "ocr_text_joined": text_joined,
            "fusion_hypothesis_type": hyp_type,
            "roi_type": roi_type,
        },
        "interpretation_candidate": {
            "summary": TEMPLATE_SUMMARY_EN,
            "language": "en",
            "fact_status": "not_fact",
            "confidence": None,
            "requires_review": True,
        },
        "approval_status": str(queue_item.get("approval_status") or "not_approved"),
        "review_status": str(queue_item.get("review_status") or "pending_review"),
        "forbidden_actions": dict(FORBIDDEN_ACTIONS_V0),
    }


def matrix_row_from_interpretation_v0(interp: Dict[str, Any]) -> Dict[str, Any]:
    inp = interp.get("input_summary") if isinstance(interp.get("input_summary"), dict) else {}
    body = interp.get("interpretation_candidate") if isinstance(interp.get("interpretation_candidate"), dict) else {}
    return {
        "interpretation_id": interp.get("interpretation_id"),
        "source_queue_item_id": interp.get("source_queue_item_id"),
        "source_candidate_id": interp.get("source_candidate_id"),
        "ocr_text_joined": inp.get("ocr_text_joined"),
        "interpretation_mode": interp.get("interpretation_mode"),
        "fact_status": body.get("fact_status", "not_fact"),
        "requires_review": body.get("requires_review", True),
        "approval_status": interp.get("approval_status"),
        "review_status": interp.get("review_status"),
    }


def build_risk_report_v0(*, interpretation_count: int) -> Dict[str, Any]:
    return {
        "schema_version": RISK_SCHEMA,
        "interpretation_count": interpretation_count,
        "risk_flags": dict(RISK_FLAGS_V0),
        "notes": [
            "Template stub interpretation is not LLM output and not semantic truth.",
            "Interpretation must not alter review queue approval or review status.",
        ],
    }


def build_policy_report_v0(*, interpretation_count: int) -> Dict[str, Any]:
    return {
        "schema_version": POLICY_SCHEMA,
        "interpretation_count": interpretation_count,
        "all_interpretations_dry_run_only": interpretation_count > 0,
        "all_require_review": True,
        "auto_approve_allowed": False,
        "approval_status_unchanged": True,
        "write_actions_forbidden": True,
        "external_llm_invoked": False,
    }


def build_dryrun_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_ai_interpretation_dryrun_executed": True,
        "interpretation_mode": "template_stub",
        "external_llm_invoked": False,
        "online_ai_invoked": False,
        "ai_interpretation_committed": False,
        "approval_granted": False,
        "auto_approve_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "rapidocr_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
    }


def run_cross_modal_ai_interpretation_dryrun_v0(
    *,
    review_queue_root: str,
    fusion_candidate_dryrun_root: str,
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
    rq_root = Path(review_queue_root).resolve()
    fd_root = Path(fusion_candidate_dryrun_root).resolve()

    rq_cand_path = rq_root / "cross_modal_fusion_review_queue_candidates.json"
    if not rq_cand_path.is_file():
        errs.append(f"missing:review_queue_candidates:{rq_cand_path}")
        queue_items: List[Dict[str, Any]] = []
    else:
        rq_doc = _read_json(rq_cand_path)
        queue_items = [i for i in (rq_doc.get("items") or []) if isinstance(i, dict)]

    fusion_by_id = _load_fusion_candidates_by_id(fd_root)
    if not fusion_by_id:
        errs.append(f"missing_or_empty:fusion_candidates:{fd_root}")

    interpretations: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    skipped_non_pending = 0

    for qi in queue_items:
        if qi.get("review_status") != "pending_review":
            skipped_non_pending += 1
            continue
        src_id = str(qi.get("source_candidate_id") or "")
        fc = fusion_by_id.get(src_id)
        if not fc:
            errs.append(f"fusion_candidate_not_found:{src_id}")
            continue
        interp = build_template_interpretation_candidate_v0(qi, fc)
        interpretations.append(interp)
        matrix_rows.append(matrix_row_from_interpretation_v0(interp))

    risk = build_risk_report_v0(interpretation_count=len(interpretations))
    policy = build_policy_report_v0(interpretation_count=len(interpretations))
    audit = build_dryrun_audit_v0()

    phase_verdict = "GO"
    if not interpretations and not errs:
        phase_verdict = "CONDITIONAL_GO"
    if errs and not interpretations:
        phase_verdict = "NO_GO"
    elif errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-AI-Interpretation-DryRun-001",
        "review_queue_root": str(rq_root),
        "fusion_candidate_dryrun_root": str(fd_root),
        "interpretation_count": len(interpretations),
        "skipped_non_pending_queue_items": skipped_non_pending,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    candidates_doc = {
        "schema_version": CANDIDATES_DOC_SCHEMA,
        "interpretation_count": len(interpretations),
        "interpretations": interpretations,
    }
    matrix_doc = {
        "schema_version": MATRIX_SCHEMA,
        "row_count": len(matrix_rows),
        "rows": matrix_rows,
    }

    return summary, candidates_doc, matrix_doc, risk, policy, audit, errs
