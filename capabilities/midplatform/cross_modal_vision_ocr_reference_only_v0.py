# -*- coding: utf-8 -*-
"""Cross-modal Vision + OCR reference-only alignment (not fusion).

Phase-CrossModal-Vision-OCR-Evidence-Reference-Only-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REFERENCE_SCHEMA = "cross_modal_vision_ocr_reference_candidate_v0"
CANDIDATES_DOC_SCHEMA = "cross_modal_vision_ocr_reference_candidates_v0"
MATRIX_SCHEMA = "cross_modal_vision_ocr_reference_matrix_v0"
ALIGNMENT_SCHEMA = "cross_modal_vision_ocr_alignment_summary_v0"
CHAIN_SCHEMA = "cross_modal_vision_ocr_source_chain_summary_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_reference_only_audit_v0"
SUMMARY_SCHEMA = "cross_modal_vision_ocr_reference_only_summary_v0"

FORBIDDEN_ACTIONS_V0: Dict[str, bool] = {
    "write_midplatform_fact": True,
    "write_scene_delta": True,
    "write_world_model": True,
    "invoke_ai_interpretation": True,
    "invoke_navigation_decision": True,
    "claim_fused_fact": True,
}


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _match_key(frame_id: str, roi_id: str) -> str:
    return f"{frame_id}::{roi_id}"


def _load_vision_evidence_index(pack_path: Path) -> Dict[str, List[Dict[str, Any]]]:
    """Index vision pack items by frame_id + roi_id."""
    out: Dict[str, List[Dict[str, Any]]] = {}
    if not pack_path.is_file():
        return out
    pack = _read_json(pack_path)
    items = pack.get("items") if isinstance(pack.get("items"), list) else []
    for it in items:
        if not isinstance(it, dict):
            continue
        fid = str(it.get("source_frame_id") or "")
        rid = str(it.get("roi_id") or "")
        if not fid or not rid:
            continue
        out.setdefault(_match_key(fid, rid), []).append(it)
    return out


def _resolve_vision_pack_path(
    vision_recognition_readonly_consumer_root: Path,
    vision_roi_proposal_root: Path,
) -> Optional[Path]:
    sum_p = vision_recognition_readonly_consumer_root / "vision_recognition_evidence_readonly_consumer_summary.json"
    if sum_p.is_file():
        doc = _read_json(sum_p)
        if isinstance(doc, dict):
            pr = str(doc.get("vision_recognition_evidence_pack_root") or "").strip()
            if pr:
                pp = Path(pr) / "vision_recognition_evidence_pack.json"
                if pp.is_file():
                    return pp
    alt = vision_roi_proposal_root.parent / "vision_recognition_evidence_pack_stub_smoke_v0" / "vision_recognition_evidence_pack.json"
    if alt.is_file():
        return alt
    return None


def _resolve_ocr_submission_root(ocr_consumer_root: Path) -> Optional[str]:
    view_p = ocr_consumer_root / "vision_triggered_ocr_evidence_readonly_consumer_view.json"
    if view_p.is_file():
        view = _read_json(view_p)
        if isinstance(view, dict) and view.get("source_submission_root"):
            return str(view["source_submission_root"])
    return None


def build_reference_candidate_v0(
    *,
    frame_id: str,
    roi_id: str,
    roi_type: str,
    bbox_in_frame: List[int],
    vision_items: List[Dict[str, Any]],
    ocr_entry: Dict[str, Any],
    ocr_candidate_id: str,
) -> Dict[str, Any]:
    vision_refs = {
        "roi_ref": roi_id,
        "vision_evidence_refs": [str(it.get("evidence_id") or "") for it in vision_items if it.get("evidence_id")],
    }
    ocr_refs = {
        "ocr_request_candidate_id": ocr_candidate_id,
        "ocr_request_id": str(ocr_entry.get("ocr_request_id") or ""),
        "ocr_bridge_pack_ref": str(ocr_entry.get("bridge_pack_ref") or ""),
        "ocr_text_joined": str(ocr_entry.get("text_joined") or ""),
    }
    return {
        "schema_version": REFERENCE_SCHEMA,
        "reference_id": f"xref_{uuid.uuid4().hex[:16]}",
        "reference_scope": "reference_only",
        "source": "vision_roi_triggered_ocr",
        "frame_id": frame_id,
        "roi_id": roi_id,
        "roi_type": roi_type,
        "vision_refs": vision_refs,
        "ocr_refs": ocr_refs,
        "spatial_reference": {
            "bbox_in_frame": [int(v) for v in bbox_in_frame],
            "coordinate_space": "frame_pixel",
        },
        "fact_status": "not_fact",
        "fusion_status": "not_fused",
        "ai_interpretation_status": "not_invoked",
        "allowed_next_actions": [
            "manual_review",
            "future_cross_modal_fusion_candidate",
        ],
        "forbidden_actions": dict(FORBIDDEN_ACTIONS_V0),
    }


def build_reference_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_reference_only_executed": True,
        "cross_modal_fusion_invoked": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "yolo_invoked": False,
        "real_detector_invoked": False,
    }


def run_cross_modal_vision_ocr_reference_only_v0(
    *,
    vision_roi_proposal_root: str,
    vision_recognition_readonly_consumer_root: str,
    vision_triggered_ocr_readonly_consumer_root: str,
    vision_roi_to_ocr_bridge_root: str,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []

    roi_root = Path(vision_roi_proposal_root).resolve()
    vis_cons_root = Path(vision_recognition_readonly_consumer_root).resolve()
    ocr_cons_root = Path(vision_triggered_ocr_readonly_consumer_root).resolve()
    bridge_root = Path(vision_roi_to_ocr_bridge_root).resolve()

    roi_cand_p = roi_root / "vision_roi_proposal_candidate.json"
    ocr_view_p = ocr_cons_root / "vision_triggered_ocr_evidence_readonly_consumer_view.json"
    ocr_matrix_p = ocr_cons_root / "vision_triggered_ocr_evidence_matrix.json"
    bridge_mx_p = bridge_root / "vision_roi_to_ocr_request_candidate_matrix.json"
    vis_view_p = vis_cons_root / "vision_recognition_evidence_readonly_consumer_view.json"

    for label, p in (
        ("vision_roi_proposal_candidate", roi_cand_p),
        ("ocr_consumer_view", ocr_view_p),
        ("ocr_consumer_matrix", ocr_matrix_p),
        ("vision_consumer_view", vis_view_p),
    ):
        if not p.is_file():
            errs.append(f"missing:{label}")

    roi_doc = _read_json(roi_cand_p) if roi_cand_p.is_file() else {}
    roi_items = roi_doc.get("roi_items") if isinstance(roi_doc.get("roi_items"), list) else []

    roi_by_key: Dict[str, Dict[str, Any]] = {}
    for it in roi_items:
        if not isinstance(it, dict):
            continue
        fid = str(it.get("source_frame_id") or "")
        rid = str(it.get("roi_id") or "")
        if fid and rid:
            roi_by_key[_match_key(fid, rid)] = it

    ocr_view = _read_json(ocr_view_p) if ocr_view_p.is_file() else {}
    ocr_by_candidate = ocr_view.get("evidence_by_candidate") if isinstance(ocr_view.get("evidence_by_candidate"), dict) else {}

    bridge_mx = _read_json(bridge_mx_p) if bridge_mx_p.is_file() else {}
    bridge_rows = bridge_mx.get("rows") if isinstance(bridge_mx.get("rows"), list) else []
    bbox_by_candidate: Dict[str, List[int]] = {}
    for br in bridge_rows:
        if isinstance(br, dict) and br.get("candidate_id"):
            bb = br.get("bbox_in_frame")
            if isinstance(bb, list) and len(bb) == 4:
                bbox_by_candidate[str(br["candidate_id"])] = [int(v) for v in bb]

    pack_path = _resolve_vision_pack_path(vis_cons_root, roi_root)
    vision_idx = _load_vision_evidence_index(pack_path) if pack_path else {}
    if not vision_idx:
        errs.append("vision_evidence_index_empty")

    references: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    matched_keys: Set[str] = set()

    for cand_id, ocr_entry in ocr_by_candidate.items():
        if not isinstance(ocr_entry, dict):
            continue
        frame_id = str(ocr_entry.get("source_frame_id") or "")
        roi_id = str(ocr_entry.get("roi_id") or "")
        roi_type = str(ocr_entry.get("roi_type") or "")
        if not frame_id or not roi_id:
            errs.append(f"ocr_entry_missing_keys:{cand_id}")
            continue

        key = _match_key(frame_id, roi_id)
        roi_item = roi_by_key.get(key, {})
        bbox = bbox_by_candidate.get(str(cand_id))
        if not bbox:
            bb = roi_item.get("bbox_in_frame")
            bbox = [int(v) for v in bb] if isinstance(bb, list) and len(bb) == 4 else [0, 0, 0, 0]

        vision_items = vision_idx.get(key, [])
        ref = build_reference_candidate_v0(
            frame_id=frame_id,
            roi_id=roi_id,
            roi_type=roi_type or str(roi_item.get("roi_type") or ""),
            bbox_in_frame=bbox,
            vision_items=vision_items,
            ocr_entry=ocr_entry,
            ocr_candidate_id=str(cand_id),
        )
        references.append(ref)
        matched_keys.add(key)

        ocr_refs = ref.get("ocr_refs") if isinstance(ref.get("ocr_refs"), dict) else {}
        matrix_rows.append(
            {
                "reference_id": ref["reference_id"],
                "frame_id": frame_id,
                "roi_id": roi_id,
                "roi_type": ref["roi_type"],
                "ocr_request_candidate_id": ocr_refs.get("ocr_request_candidate_id"),
                "ocr_request_id": ocr_refs.get("ocr_request_id"),
                "ocr_text_joined": ocr_refs.get("ocr_text_joined"),
                "bridge_pack_ref": ocr_refs.get("ocr_bridge_pack_ref"),
                "bbox_in_frame": ref["spatial_reference"]["bbox_in_frame"],
                "fact_status": "not_fact",
                "fusion_status": "not_fused",
                "ai_interpretation_status": "not_invoked",
            }
        )

    vision_roi_count = len(roi_items)
    ocr_evidence_count = len(ocr_by_candidate)
    matched_reference_count = len(references)
    unmatched_vision_keys = set(roi_by_key.keys()) - matched_keys
    unmatched_ocr_count = 0

    unmatched_vision_rows = [
        {
            "frame_id": roi_by_key[k].get("source_frame_id"),
            "roi_id": roi_by_key[k].get("roi_id"),
            "roi_type": roi_by_key[k].get("roi_type"),
            "reason_code": "no_ocr_evidence_for_roi",
        }
        for k in sorted(unmatched_vision_keys)
    ]

    alignment = {
        "schema_version": ALIGNMENT_SCHEMA,
        "vision_roi_count": vision_roi_count,
        "ocr_evidence_count": ocr_evidence_count,
        "matched_reference_count": matched_reference_count,
        "unmatched_vision_roi_count": len(unmatched_vision_keys),
        "unmatched_ocr_evidence_count": unmatched_ocr_count,
        "match_key_strategy": "frame_id + roi_id",
        "reference_only": True,
        "unmatched_vision_roi_rows": unmatched_vision_rows,
    }

    ocr_submission_root = _resolve_ocr_submission_root(ocr_cons_root)

    chain = {
        "schema_version": CHAIN_SCHEMA,
        "vision_roi_proposal_root": str(roi_root),
        "vision_roi_to_ocr_bridge_root": str(bridge_root),
        "ocr_submission_from_vision_roi_root": ocr_submission_root,
        "vision_triggered_ocr_readonly_consumer_root": str(ocr_cons_root),
        "vision_recognition_readonly_consumer_root": str(vis_cons_root),
        "vision_recognition_evidence_pack_path": str(pack_path) if pack_path else None,
        "reference_candidate_build_step": "cross_modal_vision_ocr_reference_only_v0",
        "matched_reference_count": matched_reference_count,
    }

    candidates_doc = {
        "schema_version": CANDIDATES_DOC_SCHEMA,
        "reference_count": len(references),
        "references": references,
    }

    matrix_doc = {
        "schema_version": MATRIX_SCHEMA,
        "row_count": len(matrix_rows),
        "rows": matrix_rows,
    }

    audit = build_reference_audit_v0()

    phase_verdict = "GO"
    if matched_reference_count <= 0:
        phase_verdict = "CONDITIONAL_GO" if not errs else "NO_GO"
    elif errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-Evidence-Reference-Only-001",
        "vision_roi_proposal_root": str(roi_root),
        "vision_recognition_readonly_consumer_root": str(vis_cons_root),
        "vision_triggered_ocr_readonly_consumer_root": str(ocr_cons_root),
        "vision_roi_to_ocr_bridge_root": str(bridge_root),
        "matched_reference_count": matched_reference_count,
        "unmatched_vision_roi_count": len(unmatched_vision_keys),
        "unmatched_ocr_evidence_count": unmatched_ocr_count,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, candidates_doc, matrix_doc, alignment, chain, audit, errs
