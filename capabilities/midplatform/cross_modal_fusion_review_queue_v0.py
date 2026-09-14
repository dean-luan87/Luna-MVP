# -*- coding: utf-8 -*-
"""Cross-modal fusion candidate review queue (pending only, no auto-approve).

Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

QUEUE_CANDIDATE_SCHEMA = "cross_modal_fusion_review_queue_candidate_v0"
QUEUE_CANDIDATES_DOC_SCHEMA = "cross_modal_fusion_review_queue_candidates_v0"
MATRIX_SCHEMA = "cross_modal_fusion_review_queue_matrix_v0"
RISK_SUMMARY_SCHEMA = "cross_modal_fusion_review_risk_summary_v0"
POLICY_SCHEMA = "cross_modal_fusion_review_queue_policy_report_v0"
AUDIT_SCHEMA = "cross_modal_fusion_review_queue_audit_v0"
SUMMARY_SCHEMA = "cross_modal_fusion_review_queue_summary_v0"

FORBIDDEN_ACTIONS_V0: Dict[str, bool] = {
    "write_midplatform_fact": True,
    "write_scene_delta": True,
    "write_world_model": True,
    "invoke_navigation_decision": True,
    "claim_confirmed_fact": True,
    "auto_approve": True,
}

ALLOWED_NEXT_ACTIONS_V0: List[str] = [
    "manual_review",
    "ai_interpretation_dryrun_later",
    "scene_delta_candidate_later",
]


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def build_review_queue_candidate_v0(
    fusion_cand: Dict[str, Any],
    *,
    fusion_dryrun_root: Path,
    candidate_payload_ref: str,
) -> Dict[str, Any]:
    source_id = str(fusion_cand.get("candidate_id") or "")
    risk_ref = str((fusion_dryrun_root / "cross_modal_vision_ocr_fusion_risk_report.json").resolve())
    chain_ref = str((fusion_dryrun_root / "cross_modal_vision_ocr_fusion_source_chain_summary.json").resolve())

    return {
        "schema_version": QUEUE_CANDIDATE_SCHEMA,
        "queue_item_id": f"rq_{uuid.uuid4().hex[:16]}",
        "source_candidate_id": source_id,
        "queue_scope": "review_queue_only",
        "review_status": "pending_review",
        "approval_status": "not_approved",
        "source_type": "cross_modal_vision_ocr_fusion_candidate",
        "candidate_payload_ref": candidate_payload_ref,
        "risk_report_ref": risk_ref,
        "source_chain_ref": chain_ref,
        "review_required": True,
        "auto_approve_allowed": False,
        "fact_status": "not_fact",
        "allowed_next_actions": list(ALLOWED_NEXT_ACTIONS_V0),
        "forbidden_actions": dict(FORBIDDEN_ACTIONS_V0),
        "frame_id": fusion_cand.get("frame_id"),
        "roi_id": fusion_cand.get("roi_id"),
        "roi_type": fusion_cand.get("roi_type"),
    }


def matrix_row_from_queue_item_v0(
    queue_item: Dict[str, Any],
    fusion_cand: Dict[str, Any],
) -> Dict[str, Any]:
    ocr_ref = fusion_cand.get("ocr_reference") if isinstance(fusion_cand.get("ocr_reference"), dict) else {}
    hyp = fusion_cand.get("fusion_hypothesis") if isinstance(fusion_cand.get("fusion_hypothesis"), dict) else {}
    return {
        "queue_item_id": queue_item.get("queue_item_id"),
        "source_candidate_id": queue_item.get("source_candidate_id"),
        "frame_id": fusion_cand.get("frame_id"),
        "roi_id": fusion_cand.get("roi_id"),
        "ocr_text_joined": ocr_ref.get("text_joined"),
        "fusion_hypothesis_type": hyp.get("type"),
        "review_status": "pending_review",
        "approval_status": "not_approved",
        "fact_status": "not_fact",
        "auto_approve_allowed": False,
        "requires_review": True,
    }


def build_review_risk_summary_v0(risk_report: Dict[str, Any]) -> Dict[str, Any]:
    upstream = risk_report.get("risk_flags") if isinstance(risk_report.get("risk_flags"), dict) else {}
    inherited = {k: bool(upstream.get(k)) for k in (
        "ocr_text_not_fact",
        "vision_roi_not_fact",
        "spatial_association_not_semantic_truth",
        "fusion_candidate_not_confirmed",
        "no_ai_interpretation",
        "no_navigation_decision",
        "no_midplatform_fact_write",
        "no_scene_delta_write",
        "no_world_model_write",
    )}
    return {
        "schema_version": RISK_SUMMARY_SCHEMA,
        "inherited_from": "cross_modal_vision_ocr_fusion_risk_report_v0",
        "risk_flags": inherited,
    }


def build_queue_policy_report_v0(*, queue_item_count: int) -> Dict[str, Any]:
    return {
        "schema_version": POLICY_SCHEMA,
        "queue_item_count": queue_item_count,
        "all_candidates_pending_review": queue_item_count > 0,
        "auto_approve_allowed": False,
        "write_actions_forbidden": True,
        "human_or_policy_gate_required": True,
        "ai_interpretation_not_invoked": True,
        "scene_delta_not_written": True,
    }


def build_review_queue_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_fusion_review_queue_generated": True,
        "review_queue_only": True,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "cross_modal_fusion_committed": False,
        "rapidocr_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
    }


def run_cross_modal_fusion_review_queue_v0(
    *,
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
    root = Path(fusion_candidate_dryrun_root).resolve()

    cand_path = root / "cross_modal_vision_ocr_fusion_candidates.json"
    risk_path = root / "cross_modal_vision_ocr_fusion_risk_report.json"
    matrix_path = root / "cross_modal_vision_ocr_fusion_dryrun_matrix.json"
    chain_path = root / "cross_modal_vision_ocr_fusion_source_chain_summary.json"
    audit_path = root / "cross_modal_vision_ocr_fusion_dryrun_audit_report.json"

    for label, p in (
        ("fusion_candidates", cand_path),
        ("risk_report", risk_path),
        ("dryrun_matrix", matrix_path),
        ("source_chain", chain_path),
        ("dryrun_audit", audit_path),
    ):
        if not p.is_file():
            errs.append(f"missing:{label}:{p}")

    fusion_cands: List[Dict[str, Any]] = []
    risk_report: Dict[str, Any] = {}
    if cand_path.is_file():
        doc = _read_json(cand_path)
        fusion_cands = [
            c for c in (doc.get("candidates") or []) if isinstance(c, dict)
        ]
    if risk_path.is_file():
        risk_report = _read_json(risk_path)
        if not isinstance(risk_report, dict):
            risk_report = {}

    candidates_doc_path = root / "cross_modal_vision_ocr_fusion_candidates.json"
    payload_ref = str(candidates_doc_path.resolve()) if candidates_doc_path.is_file() else ""

    queue_items: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    for fc in fusion_cands:
        qi = build_review_queue_candidate_v0(
            fc,
            fusion_dryrun_root=root,
            candidate_payload_ref=payload_ref,
        )
        queue_items.append(qi)
        matrix_rows.append(matrix_row_from_queue_item_v0(qi, fc))

    risk_summary = build_review_risk_summary_v0(risk_report)
    policy = build_queue_policy_report_v0(queue_item_count=len(queue_items))
    audit = build_review_queue_audit_v0()

    phase_verdict = "GO"
    if not queue_items and not errs:
        phase_verdict = "CONDITIONAL_GO"
    if errs and not queue_items:
        phase_verdict = "NO_GO"
    elif errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001",
        "fusion_candidate_dryrun_root": str(root),
        "queue_item_count": len(queue_items),
        "pending_review_count": len(queue_items),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    candidates_doc = {
        "schema_version": QUEUE_CANDIDATES_DOC_SCHEMA,
        "queue_item_count": len(queue_items),
        "items": queue_items,
    }
    matrix_doc = {
        "schema_version": MATRIX_SCHEMA,
        "row_count": len(matrix_rows),
        "rows": matrix_rows,
    }

    return summary, candidates_doc, matrix_doc, risk_summary, policy, audit, errs
