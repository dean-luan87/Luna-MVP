# -*- coding: utf-8 -*-
"""Cross-modal Vision-OCR Scene Delta candidate dry-run (no executor, no write).

Phase-CrossModal-Vision-OCR-Scene-Delta-Candidate-DryRun-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CANDIDATE_SCHEMA = "cross_modal_scene_delta_candidate_dryrun_v0"
CANDIDATES_DOC_SCHEMA = "cross_modal_scene_delta_candidates_v0"
MATRIX_SCHEMA = "cross_modal_scene_delta_mapping_matrix_v0"
GATE_STUB_SCHEMA = "cross_modal_scene_delta_gate_stub_v0"
RISK_SCHEMA = "cross_modal_scene_delta_risk_report_v0"
CHAIN_SCHEMA = "cross_modal_scene_delta_source_chain_summary_v0"
AUDIT_SCHEMA = "cross_modal_scene_delta_dryrun_audit_v0"
SUMMARY_SCHEMA = "cross_modal_scene_delta_candidate_dryrun_summary_v0"

FORBIDDEN_ACTIONS_V0: Dict[str, bool] = {
    "write_scene_delta": True,
    "write_midplatform_fact": True,
    "write_world_model": True,
    "invoke_navigation_decision": True,
    "auto_approve": True,
    "claim_confirmed_fact": True,
}

RISK_FLAGS_V0: Dict[str, bool] = {
    "scene_delta_candidate_not_write": True,
    "fusion_candidate_not_fact": True,
    "ai_interpretation_not_fact": True,
    "ocr_text_not_fact": True,
    "spatial_association_not_semantic_truth": True,
    "gate_not_evaluated": True,
    "approval_not_granted": True,
    "no_scene_delta_write": True,
    "no_midplatform_fact_write": True,
    "no_world_model_write": True,
    "no_navigation_decision": True,
}

GATE_REASON_CODES_V0: List[str] = [
    "cross_modal_candidate_requires_gate",
    "not_fact",
    "ai_interpretation_dryrun_only",
    "manual_or_policy_review_required",
]


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _file_ref(root: Path, name: str) -> Optional[str]:
    p = root / name
    return str(p.resolve()) if p.is_file() else None


def _load_fusion_by_id(root: Path) -> Dict[str, Dict[str, Any]]:
    p = root / "cross_modal_vision_ocr_fusion_candidates.json"
    if not p.is_file():
        return {}
    doc = _read_json(p)
    return {
        str(c.get("candidate_id")): c
        for c in (doc.get("candidates") or [])
        if isinstance(c, dict) and c.get("candidate_id")
    }


def _load_queue_by_fusion_id(root: Path) -> Dict[str, Dict[str, Any]]:
    p = root / "cross_modal_fusion_review_queue_candidates.json"
    if not p.is_file():
        return {}
    out: Dict[str, Dict[str, Any]] = {}
    for item in _read_json(p).get("items") or []:
        if isinstance(item, dict):
            sid = str(item.get("source_candidate_id") or "")
            if sid:
                out[sid] = item
    return out


def _load_interpretations(root: Path) -> List[Dict[str, Any]]:
    p = root / "cross_modal_ai_interpretation_candidates.json"
    if not p.is_file():
        return []
    doc = _read_json(p)
    return [i for i in (doc.get("interpretations") or []) if isinstance(i, dict)]


def build_scene_delta_candidate_v0(
    *,
    fusion_cand: Dict[str, Any],
    queue_item: Dict[str, Any],
    interpretation: Dict[str, Any],
) -> Dict[str, Any]:
    vis_ref = fusion_cand.get("vision_reference") if isinstance(fusion_cand.get("vision_reference"), dict) else {}
    spatial_ref = fusion_cand.get("spatial_reference") if isinstance(fusion_cand.get("spatial_reference"), dict) else {}
    bbox = list(vis_ref.get("bbox_in_frame") or spatial_ref.get("bbox_in_frame") or [0, 0, 0, 0])
    ocr_ref = fusion_cand.get("ocr_reference") if isinstance(fusion_cand.get("ocr_reference"), dict) else {}
    hyp = fusion_cand.get("fusion_hypothesis") if isinstance(fusion_cand.get("fusion_hypothesis"), dict) else {}
    inp = interpretation.get("input_summary") if isinstance(interpretation.get("input_summary"), dict) else {}
    body = interpretation.get("interpretation_candidate") if isinstance(interpretation.get("interpretation_candidate"), dict) else {}

    return {
        "schema_version": CANDIDATE_SCHEMA,
        "candidate_id": f"sd_cand_{uuid.uuid4().hex[:16]}",
        "candidate_scope": "dry_run_only",
        "source_type": "cross_modal_vision_ocr_fusion_candidate",
        "source_fusion_candidate_id": str(fusion_cand.get("candidate_id") or ""),
        "source_queue_item_id": str(queue_item.get("queue_item_id") or interpretation.get("source_queue_item_id") or ""),
        "source_interpretation_id": str(interpretation.get("interpretation_id") or ""),
        "scene_delta_candidate_type": "observed_text_in_visual_roi_candidate",
        "spatial_reference": {
            "frame_id": str(fusion_cand.get("frame_id") or ""),
            "roi_id": str(fusion_cand.get("roi_id") or ""),
            "roi_type": str(fusion_cand.get("roi_type") or "upper_sign_roi"),
            "bbox_in_frame": [int(v) for v in bbox],
            "coordinate_space": str(spatial_ref.get("coordinate_space") or vis_ref.get("coordinate_space") or "frame_pixel"),
        },
        "observed_evidence": {
            "ocr_text_joined": str(ocr_ref.get("text_joined") or inp.get("ocr_text_joined") or ""),
            "vision_roi_type": str(fusion_cand.get("roi_type") or inp.get("roi_type") or ""),
            "fusion_hypothesis_type": str(hyp.get("type") or inp.get("fusion_hypothesis_type") or ""),
            "ai_interpretation_summary": str(body.get("summary") or ""),
        },
        "fact_status": "not_fact",
        "write_allowed": False,
        "requires_gate_approval": True,
        "gate_status": "not_evaluated",
        "approval_status": str(queue_item.get("approval_status") or interpretation.get("approval_status") or "not_approved"),
        "review_status": str(queue_item.get("review_status") or interpretation.get("review_status") or "pending_review"),
        "forbidden_actions": dict(FORBIDDEN_ACTIONS_V0),
    }


def matrix_row_from_candidate_v0(cand: Dict[str, Any]) -> Dict[str, Any]:
    obs = cand.get("observed_evidence") if isinstance(cand.get("observed_evidence"), dict) else {}
    spatial = cand.get("spatial_reference") if isinstance(cand.get("spatial_reference"), dict) else {}
    return {
        "candidate_id": cand.get("candidate_id"),
        "source_fusion_candidate_id": cand.get("source_fusion_candidate_id"),
        "source_queue_item_id": cand.get("source_queue_item_id"),
        "source_interpretation_id": cand.get("source_interpretation_id"),
        "frame_id": spatial.get("frame_id"),
        "roi_id": spatial.get("roi_id"),
        "ocr_text_joined": obs.get("ocr_text_joined"),
        "ai_interpretation_summary": obs.get("ai_interpretation_summary"),
        "scene_delta_candidate_type": cand.get("scene_delta_candidate_type"),
        "fact_status": "not_fact",
        "write_allowed": False,
        "gate_status": "not_evaluated",
        "approval_status": cand.get("approval_status"),
    }


def build_gate_stub_v0() -> Dict[str, Any]:
    return {
        "schema_version": GATE_STUB_SCHEMA,
        "gate_required": True,
        "gate_status": "not_evaluated",
        "write_allowed": False,
        "gate_reason_codes": list(GATE_REASON_CODES_V0),
    }


def build_risk_report_v0(*, candidate_count: int) -> Dict[str, Any]:
    return {
        "schema_version": RISK_SCHEMA,
        "candidate_count": candidate_count,
        "risk_flags": dict(RISK_FLAGS_V0),
    }


def build_source_chain_summary_v0(
    *,
    fusion_root: Path,
    queue_root: Path,
    interpretation_root: Path,
) -> Dict[str, Any]:
    return {
        "schema_version": CHAIN_SCHEMA,
        "fusion_candidate_dryrun_root": str(fusion_root.resolve()),
        "review_queue_root": str(queue_root.resolve()),
        "ai_interpretation_dryrun_root": str(interpretation_root.resolve()),
        "source_chain_steps": [
            {
                "step": "fusion_candidate_dryrun",
                "root": str(fusion_root.resolve()),
                "artifacts": {
                    "fusion_candidates": _file_ref(fusion_root, "cross_modal_vision_ocr_fusion_candidates.json"),
                    "fusion_dryrun_matrix": _file_ref(fusion_root, "cross_modal_vision_ocr_fusion_dryrun_matrix.json"),
                },
            },
            {
                "step": "review_queue",
                "root": str(queue_root.resolve()),
                "artifacts": {
                    "review_queue_candidates": _file_ref(queue_root, "cross_modal_fusion_review_queue_candidates.json"),
                },
            },
            {
                "step": "ai_interpretation_dryrun",
                "root": str(interpretation_root.resolve()),
                "artifacts": {
                    "interpretation_candidates": _file_ref(
                        interpretation_root, "cross_modal_ai_interpretation_candidates.json"
                    ),
                },
            },
            {"step": "scene_delta_candidate_dryrun_build", "description": "cross_modal_scene_delta_candidate_dryrun_v0"},
        ],
    }


def build_dryrun_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_scene_delta_candidate_dryrun_executed": True,
        "dry_run_only": True,
        "scene_delta_executor_invoked": False,
        "scene_delta_written": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "ai_interpretation_committed": False,
        "rapidocr_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
    }


def run_cross_modal_scene_delta_candidate_dryrun_v0(
    *,
    fusion_candidate_dryrun_root: str,
    review_queue_root: str,
    ai_interpretation_dryrun_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    fd_root = Path(fusion_candidate_dryrun_root).resolve()
    rq_root = Path(review_queue_root).resolve()
    ai_root = Path(ai_interpretation_dryrun_root).resolve()

    fusion_by_id = _load_fusion_by_id(fd_root)
    queue_by_fusion = _load_queue_by_fusion_id(rq_root)
    interpretations = _load_interpretations(ai_root)

    if not fusion_by_id:
        errs.append(f"missing_or_empty:fusion_candidates:{fd_root}")
    if not queue_by_fusion:
        errs.append(f"missing_or_empty:review_queue:{rq_root}")
    if not interpretations:
        errs.append(f"missing_or_empty:interpretations:{ai_root}")

    candidates: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []

    for interp in interpretations:
        src_fusion_id = str(interp.get("source_candidate_id") or "")
        fc = fusion_by_id.get(src_fusion_id)
        qi = queue_by_fusion.get(src_fusion_id)
        if not fc:
            errs.append(f"fusion_candidate_not_found:{src_fusion_id}")
            continue
        if not qi:
            errs.append(f"queue_item_not_found:{src_fusion_id}")
            continue
        if qi.get("review_status") != "pending_review":
            continue
        cand = build_scene_delta_candidate_v0(
            fusion_cand=fc,
            queue_item=qi,
            interpretation=interp,
        )
        candidates.append(cand)
        matrix_rows.append(matrix_row_from_candidate_v0(cand))

    gate_stub = build_gate_stub_v0()
    risk = build_risk_report_v0(candidate_count=len(candidates))
    chain = build_source_chain_summary_v0(
        fusion_root=fd_root,
        queue_root=rq_root,
        interpretation_root=ai_root,
    )
    audit = build_dryrun_audit_v0()

    phase_verdict = "GO"
    if not candidates and not errs:
        phase_verdict = "CONDITIONAL_GO"
    if errs and not candidates:
        phase_verdict = "NO_GO"
    elif errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Candidate-DryRun-001",
        "fusion_candidate_dryrun_root": str(fd_root),
        "review_queue_root": str(rq_root),
        "ai_interpretation_dryrun_root": str(ai_root),
        "candidate_count": len(candidates),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    candidates_doc = {
        "schema_version": CANDIDATES_DOC_SCHEMA,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    matrix_doc = {
        "schema_version": MATRIX_SCHEMA,
        "row_count": len(matrix_rows),
        "rows": matrix_rows,
    }

    return summary, candidates_doc, matrix_doc, gate_stub, risk, chain, audit, errs
