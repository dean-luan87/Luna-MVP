# -*- coding: utf-8 -*-
"""Cross-modal Vision + OCR fusion candidate dry-run (not fact, no-write).

Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

FUSION_CANDIDATE_SCHEMA = "cross_modal_vision_ocr_fusion_candidate_v0"
CANDIDATES_DOC_SCHEMA = "cross_modal_vision_ocr_fusion_candidates_v0"
MATRIX_SCHEMA = "cross_modal_vision_ocr_fusion_dryrun_matrix_v0"
RISK_SCHEMA = "cross_modal_vision_ocr_fusion_risk_report_v0"
CHAIN_SCHEMA = "cross_modal_vision_ocr_fusion_source_chain_summary_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_fusion_dryrun_audit_v0"
SUMMARY_SCHEMA = "cross_modal_vision_ocr_fusion_candidate_dryrun_summary_v0"

FORBIDDEN_ACTIONS_V0: Dict[str, bool] = {
    "write_midplatform_fact": True,
    "write_scene_delta": True,
    "write_world_model": True,
    "invoke_ai_interpretation": True,
    "invoke_navigation_decision": True,
    "claim_confirmed_fact": True,
}

RISK_FLAGS_V0: Dict[str, bool] = {
    "ocr_text_not_fact": True,
    "vision_roi_not_fact": True,
    "spatial_association_not_semantic_truth": True,
    "fusion_candidate_not_confirmed": True,
    "no_ai_interpretation": True,
    "no_navigation_decision": True,
    "no_midplatform_fact_write": True,
    "no_scene_delta_write": True,
    "no_world_model_write": True,
}


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _file_ref(root: Path, name: str) -> Optional[str]:
    p = root / name
    return str(p.resolve()) if p.is_file() else None


def build_fusion_candidate_from_reference_v0(
    reference: Dict[str, Any],
    *,
    source_label: str = "vision_roi_text_bearing_ocr_reference",
) -> Dict[str, Any]:
    frame_id = str(reference.get("frame_id") or "")
    roi_id = str(reference.get("roi_id") or "")
    roi_type = str(reference.get("roi_type") or "upper_sign_roi")
    spatial = reference.get("spatial_reference") if isinstance(reference.get("spatial_reference"), dict) else {}
    bbox = list(spatial.get("bbox_in_frame") or [0, 0, 0, 0])
    ocr_refs = reference.get("ocr_refs") if isinstance(reference.get("ocr_refs"), dict) else {}
    text_joined = str(ocr_refs.get("ocr_text_joined") or "")
    empty_text = bool(ocr_refs.get("empty_text")) if "empty_text" in ocr_refs else not text_joined.strip()
    text_item_count = int(ocr_refs.get("text_item_count") or 0)
    if text_item_count <= 0 and text_joined.strip():
        text_item_count = max(1, len([p for p in text_joined.split("|") if p.strip()]))

    return {
        "schema_version": FUSION_CANDIDATE_SCHEMA,
        "candidate_id": f"fusion_cand_{uuid.uuid4().hex[:16]}",
        "candidate_scope": "dry_run_only",
        "source": source_label,
        "frame_id": frame_id,
        "roi_id": roi_id,
        "roi_type": roi_type,
        "vision_reference": {
            "bbox_in_frame": [int(v) for v in bbox],
            "coordinate_space": str(spatial.get("coordinate_space") or "frame_pixel"),
            "roi_source": "vision_roi",
        },
        "ocr_reference": {
            "provider": str(ocr_refs.get("ocr_provider") or "rapidocr_candidate"),
            "text_joined": text_joined,
            "text_item_count": text_item_count,
            "empty_text": empty_text,
            "bridge_pack_ref": str(ocr_refs.get("ocr_bridge_pack_ref") or ""),
            "ocr_request_candidate_id": str(ocr_refs.get("ocr_request_candidate_id") or ""),
            "ocr_request_id": str(ocr_refs.get("ocr_request_id") or ""),
        },
        "fusion_hypothesis": {
            "type": "text_in_visual_roi_candidate",
            "summary": "OCR text is spatially associated with the selected vision ROI",
            "confidence": None,
            "fact_status": "not_fact",
            "requires_review": True,
        },
        "forbidden_actions": dict(FORBIDDEN_ACTIONS_V0),
        "reference_id": str(reference.get("reference_id") or ""),
    }


def matrix_row_from_candidate_v0(cand: Dict[str, Any]) -> Dict[str, Any]:
    ocr_ref = cand.get("ocr_reference") if isinstance(cand.get("ocr_reference"), dict) else {}
    vis_ref = cand.get("vision_reference") if isinstance(cand.get("vision_reference"), dict) else {}
    hyp = cand.get("fusion_hypothesis") if isinstance(cand.get("fusion_hypothesis"), dict) else {}
    return {
        "candidate_id": cand.get("candidate_id"),
        "frame_id": cand.get("frame_id"),
        "roi_id": cand.get("roi_id"),
        "roi_type": cand.get("roi_type"),
        "ocr_text_joined": ocr_ref.get("text_joined"),
        "bridge_pack_ref": ocr_ref.get("bridge_pack_ref"),
        "bbox_in_frame": list(vis_ref.get("bbox_in_frame") or []),
        "fusion_hypothesis_type": hyp.get("type"),
        "fact_status": "not_fact",
        "dry_run_only": True,
        "requires_review": True,
    }


def build_risk_report_v0(*, candidate_count: int, non_empty_text_count: int) -> Dict[str, Any]:
    return {
        "schema_version": RISK_SCHEMA,
        "candidate_count": candidate_count,
        "non_empty_text_candidate_count": non_empty_text_count,
        "risk_flags": dict(RISK_FLAGS_V0),
        "notes": [
            "Fusion candidates are spatial-association hypotheses only.",
            "OCR text and Vision ROI bbox do not constitute confirmed facts.",
            "Dry-run output must not be ingested as MidPlatform fact or Scene Delta.",
        ],
    }


def build_source_chain_summary_v0(
    *,
    text_bearing_root: Path,
    rapidocr_reference_root: Path,
    fusion_build_step: str,
) -> Dict[str, Any]:
    tb = text_bearing_root.resolve()
    rr = rapidocr_reference_root.resolve()
    steps: List[Dict[str, Any]] = [
        {
            "step": "text_bearing_ocr_sample",
            "root": str(tb),
            "artifacts": {
                "sample_report": _file_ref(tb, "vision_roi_text_bearing_sample_report.json"),
                "ocr_request_candidate": _file_ref(tb, "vision_roi_text_bearing_ocr_request_candidate.json"),
                "rapidocr_submission": _file_ref(tb, "vision_roi_text_bearing_rapidocr_submission_result.json"),
                "rapidocr_consumer": _file_ref(tb, "vision_roi_text_bearing_rapidocr_consumer_view.json"),
                "cross_modal_reference": _file_ref(tb, "vision_roi_text_bearing_cross_modal_reference_candidate.json"),
            },
        },
        {
            "step": "rapidocr_reference_only_smoke",
            "root": str(rr),
            "artifacts": {
                "reference_candidates": _file_ref(rr, "cross_modal_vision_ocr_reference_candidates_rapidocr.json"),
                "reference_matrix": _file_ref(rr, "cross_modal_vision_ocr_reference_matrix_rapidocr.json"),
            },
        },
        {
            "step": fusion_build_step,
            "description": "cross_modal_vision_ocr_fusion_candidate_dryrun_v0",
        },
    ]
    return {
        "schema_version": CHAIN_SCHEMA,
        "text_bearing_sample_root": str(tb),
        "rapidocr_reference_only_root": str(rr),
        "source_chain_steps": steps,
    }


def build_dryrun_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_fusion_candidate_dryrun_executed": True,
        "dry_run_only": True,
        "cross_modal_fusion_committed": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
    }


def run_cross_modal_vision_ocr_fusion_candidate_dryrun_v0(
    *,
    text_bearing_sample_root: str,
    rapidocr_reference_only_root: str,
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
    tb_root = Path(text_bearing_sample_root).resolve()
    rr_root = Path(rapidocr_reference_only_root).resolve()

    ref_path = tb_root / "vision_roi_text_bearing_cross_modal_reference_candidate.json"
    sub_path = tb_root / "vision_roi_text_bearing_rapidocr_submission_result.json"
    if not ref_path.is_file():
        errs.append(f"missing_text_bearing_reference:{ref_path}")
        reference: Dict[str, Any] = {}
    else:
        reference = _read_json(ref_path)
        if not isinstance(reference, dict):
            errs.append("text_bearing_reference_not_object")
            reference = {}

    text_item_count_hint: Optional[int] = None
    if sub_path.is_file():
        sub = _read_json(sub_path)
        if isinstance(sub, dict) and sub.get("text_item_count") is not None:
            text_item_count_hint = int(sub.get("text_item_count") or 0)

    candidates: List[Dict[str, Any]] = []
    if reference:
        cand = build_fusion_candidate_from_reference_v0(
            reference,
            source_label="vision_roi_text_bearing_ocr_reference",
        )
        if text_item_count_hint is not None and isinstance(cand.get("ocr_reference"), dict):
            cand["ocr_reference"]["text_item_count"] = text_item_count_hint
        candidates.append(cand)

    # Optional: record rapidocr reference-only lineage count (no provider re-invocation)
    rr_cand_path = rr_root / "cross_modal_vision_ocr_reference_candidates_rapidocr.json"
    rapidocr_ref_count = 0
    if rr_cand_path.is_file():
        rr_doc = _read_json(rr_cand_path)
        refs = rr_doc.get("references") if isinstance(rr_doc.get("references"), list) else []
        rapidocr_ref_count = len(refs)
    else:
        errs.append(f"missing_rapidocr_reference_candidates:{rr_cand_path}")

    matrix_rows = [matrix_row_from_candidate_v0(c) for c in candidates]
    non_empty = sum(
        1
        for c in candidates
        if not (c.get("ocr_reference") or {}).get("empty_text", True)
        and str((c.get("ocr_reference") or {}).get("text_joined") or "").strip()
    )

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
    risk = build_risk_report_v0(candidate_count=len(candidates), non_empty_text_count=non_empty)
    chain = build_source_chain_summary_v0(
        text_bearing_root=tb_root,
        rapidocr_reference_root=rr_root,
        fusion_build_step="fusion_candidate_dryrun_build",
    )
    audit = build_dryrun_audit_v0()

    phase_verdict = "GO"
    if not candidates:
        phase_verdict = "NO_GO"
    elif non_empty <= 0:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001",
        "text_bearing_sample_root": str(tb_root),
        "rapidocr_reference_only_root": str(rr_root),
        "fusion_candidate_count": len(candidates),
        "non_empty_text_candidate_count": non_empty,
        "rapidocr_reference_only_lineage_count": rapidocr_ref_count,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, candidates_doc, matrix_doc, risk, chain, audit, errs
