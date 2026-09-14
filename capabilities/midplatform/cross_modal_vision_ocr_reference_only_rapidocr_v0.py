# -*- coding: utf-8 -*-
"""Cross-modal Vision + OCR reference-only alignment using RapidOCR consumer (not fusion).

Phase-CrossModal-Vision-OCR-Reference-Only-002
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REFERENCE_SCHEMA = "cross_modal_vision_ocr_reference_candidate_v0"
CANDIDATES_DOC_SCHEMA = "cross_modal_vision_ocr_reference_candidates_rapidocr_v0"
MATRIX_SCHEMA = "cross_modal_vision_ocr_reference_matrix_rapidocr_v0"
ALIGNMENT_SCHEMA = "cross_modal_vision_ocr_alignment_summary_rapidocr_v0"
COMPARISON_SCHEMA = "cross_modal_vision_ocr_stub_vs_rapidocr_comparison_v0"
CHAIN_SCHEMA = "cross_modal_vision_ocr_source_chain_summary_rapidocr_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_reference_only_rapidocr_audit_v0"
SUMMARY_SCHEMA = "cross_modal_vision_ocr_reference_only_rapidocr_summary_v0"

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
    out: Dict[str, List[Dict[str, Any]]] = {}
    if not pack_path.is_file():
        return out
    pack = _read_json(pack_path)
    for it in pack.get("items") or []:
        if not isinstance(it, dict):
            continue
        fid = str(it.get("source_frame_id") or "")
        rid = str(it.get("roi_id") or "")
        if fid and rid:
            out.setdefault(_match_key(fid, rid), []).append(it)
    return out


def _resolve_vision_pack_path(vis_cons_root: Path, roi_root: Path) -> Optional[Path]:
    sum_p = vis_cons_root / "vision_recognition_evidence_readonly_consumer_summary.json"
    if sum_p.is_file():
        doc = _read_json(sum_p)
        if isinstance(doc, dict):
            pr = str(doc.get("vision_recognition_evidence_pack_root") or "").strip()
            if pr:
                pp = Path(pr) / "vision_recognition_evidence_pack.json"
                if pp.is_file():
                    return pp
    alt = roi_root.parent / "vision_recognition_evidence_pack_stub_smoke_v0" / "vision_recognition_evidence_pack.json"
    return alt if alt.is_file() else None


def build_rapidocr_reference_candidate_v0(
    *,
    frame_id: str,
    roi_id: str,
    roi_type: str,
    bbox_in_frame: List[int],
    vision_items: List[Dict[str, Any]],
    ocr_entry: Dict[str, Any],
    ocr_candidate_id: str,
) -> Dict[str, Any]:
    text_joined = str(ocr_entry.get("text_joined") or "")
    empty_text = bool(ocr_entry.get("empty_text")) if "empty_text" in ocr_entry else not text_joined.strip()

    return {
        "schema_version": REFERENCE_SCHEMA,
        "reference_id": f"xref_{uuid.uuid4().hex[:16]}",
        "reference_scope": "reference_only",
        "source": "vision_roi_triggered_rapidocr",
        "frame_id": frame_id,
        "roi_id": roi_id,
        "roi_type": roi_type,
        "vision_refs": {
            "roi_ref": roi_id,
            "vision_evidence_refs": [str(it.get("evidence_id") or "") for it in vision_items if it.get("evidence_id")],
        },
        "ocr_refs": {
            "ocr_provider": str(ocr_entry.get("selected_provider") or "rapidocr_candidate"),
            "provider_level": str(ocr_entry.get("provider_level") or "lightweight"),
            "ocr_request_candidate_id": ocr_candidate_id,
            "ocr_request_id": str(ocr_entry.get("ocr_request_id") or ""),
            "ocr_bridge_pack_ref": str(ocr_entry.get("bridge_pack_ref") or ""),
            "ocr_text_joined": text_joined,
            "empty_text": empty_text,
            "real_provider_invoked": bool(ocr_entry.get("real_provider_invoked")),
            "rapidocr_invoked": bool(ocr_entry.get("rapidocr_invoked")),
        },
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


def _load_stub_reference_stats(stub_ref_root: Optional[Path]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "stub_reference_root": str(stub_ref_root) if stub_ref_root else None,
        "stub_reference_count": 0,
        "stub_mock_text_count": 0,
    }
    if stub_ref_root is None or not stub_ref_root.is_dir():
        return out
    cand_p = stub_ref_root / "cross_modal_vision_ocr_reference_candidates.json"
    if not cand_p.is_file():
        return out
    doc = _read_json(cand_p)
    refs = doc.get("references") if isinstance(doc.get("references"), list) else []
    out["stub_reference_count"] = len(refs)
    mock = 0
    for r in refs:
        if not isinstance(r, dict):
            continue
        ocr = r.get("ocr_refs") if isinstance(r.get("ocr_refs"), dict) else {}
        if str(ocr.get("ocr_text_joined") or "") == "MOCK_TEXT":
            mock += 1
    out["stub_mock_text_count"] = mock
    return out


def build_stub_vs_rapidocr_comparison_v0(
    *,
    stub_stats: Dict[str, Any],
    rapidocr_reference_count: int,
    empty_text_reference_count: int,
) -> Dict[str, Any]:
    return {
        "schema_version": COMPARISON_SCHEMA,
        "stub_reference_count": int(stub_stats.get("stub_reference_count") or 0),
        "rapidocr_reference_count": rapidocr_reference_count,
        "stub_mock_text_count": int(stub_stats.get("stub_mock_text_count") or 0),
        "rapidocr_empty_text_count": empty_text_reference_count,
        "provider_changed_from_stub_to_rapidocr": True,
        "note": "rapidocr_empty_text_is_valid_real_provider_result",
        "stub_reference_root": stub_stats.get("stub_reference_root"),
    }


def build_rapidocr_reference_audit_v0(*, rapidocr_consumer_audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_rapidocr_reference_only_executed": True,
        "cross_modal_fusion_invoked": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "rapidocr_invoked_upstream": bool(rapidocr_consumer_audit.get("rapidocr_invoked_upstream")),
        "real_provider_invoked_upstream": bool(rapidocr_consumer_audit.get("real_provider_invoked_upstream")),
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "yolo_invoked": False,
        "real_detector_invoked": False,
    }


def run_cross_modal_vision_ocr_reference_only_rapidocr_v0(
    *,
    vision_roi_proposal_root: str,
    vision_recognition_readonly_consumer_root: str,
    vision_roi_to_ocr_bridge_root: str,
    rapidocr_readonly_consumer_root: str,
    stub_reference_root: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []

    roi_root = Path(vision_roi_proposal_root).resolve()
    vis_cons_root = Path(vision_recognition_readonly_consumer_root).resolve()
    bridge_root = Path(vision_roi_to_ocr_bridge_root).resolve()
    rapid_cons_root = Path(rapidocr_readonly_consumer_root).resolve()
    stub_root = Path(stub_reference_root).resolve() if stub_reference_root else None

    roi_cand_p = roi_root / "vision_roi_proposal_candidate.json"
    rapid_view_p = rapid_cons_root / "vision_triggered_rapidocr_evidence_readonly_consumer_view.json"
    bridge_mx_p = bridge_root / "vision_roi_to_ocr_request_candidate_matrix.json"
    rapid_aud_p = rapid_cons_root / "vision_triggered_rapidocr_evidence_readonly_consumer_audit_report.json"

    for label, p in (
        ("vision_roi_proposal_candidate", roi_cand_p),
        ("rapidocr_consumer_view", rapid_view_p),
    ):
        if not p.is_file():
            errs.append(f"missing:{label}")

    roi_doc = _read_json(roi_cand_p) if roi_cand_p.is_file() else {}
    roi_items = roi_doc.get("roi_items") if isinstance(roi_doc.get("roi_items"), list) else []
    roi_by_key: Dict[str, Dict[str, Any]] = {}
    for it in roi_items:
        if isinstance(it, dict):
            fid = str(it.get("source_frame_id") or "")
            rid = str(it.get("roi_id") or "")
            if fid and rid:
                roi_by_key[_match_key(fid, rid)] = it

    rapid_view = _read_json(rapid_view_p) if rapid_view_p.is_file() else {}
    ocr_by_candidate = rapid_view.get("evidence_by_candidate") if isinstance(rapid_view.get("evidence_by_candidate"), dict) else {}
    rapid_consumer_audit = _read_json(rapid_aud_p) if rapid_aud_p.is_file() else {}

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

    rapid_summary_p = rapid_cons_root / "vision_triggered_rapidocr_evidence_readonly_consumer_summary.json"
    rapid_submission_root: Optional[str] = None
    if rapid_summary_p.is_file():
        rs = _read_json(rapid_summary_p)
        if isinstance(rs, dict):
            rapid_submission_root = str(rs.get("rapidocr_submission_from_vision_roi_root") or "") or None

    references: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []
    matched_keys: Set[str] = set()
    empty_text_count = 0

    vision_proposal_root = str(roi_root)

    for cand_id, ocr_entry in ocr_by_candidate.items():
        if not isinstance(ocr_entry, dict):
            continue
        frame_id = str(ocr_entry.get("source_frame_id") or "")
        roi_id = str(ocr_entry.get("roi_id") or "")
        if not frame_id or not roi_id:
            errs.append(f"rapidocr_entry_missing_keys:{cand_id}")
            continue

        key = _match_key(frame_id, roi_id)
        roi_item = roi_by_key.get(key, {})
        bbox = bbox_by_candidate.get(str(cand_id))
        if not bbox:
            bb = roi_item.get("bbox_in_frame")
            bbox = [int(v) for v in bb] if isinstance(bb, list) and len(bb) == 4 else [0, 0, 0, 0]

        vision_items = vision_idx.get(key, [])
        ref = build_rapidocr_reference_candidate_v0(
            frame_id=frame_id,
            roi_id=roi_id,
            roi_type=str(ocr_entry.get("roi_type") or roi_item.get("roi_type") or ""),
            bbox_in_frame=bbox,
            vision_items=vision_items,
            ocr_entry=ocr_entry,
            ocr_candidate_id=str(cand_id),
        )
        references.append(ref)
        matched_keys.add(key)

        ocr_refs = ref.get("ocr_refs") if isinstance(ref.get("ocr_refs"), dict) else {}
        if ocr_refs.get("empty_text"):
            empty_text_count += 1

        matrix_rows.append(
            {
                "reference_id": ref["reference_id"],
                "frame_id": frame_id,
                "roi_id": roi_id,
                "roi_type": ref["roi_type"],
                "ocr_provider": ocr_refs.get("ocr_provider"),
                "ocr_request_candidate_id": ocr_refs.get("ocr_request_candidate_id"),
                "ocr_request_id": ocr_refs.get("ocr_request_id"),
                "ocr_text_joined": ocr_refs.get("ocr_text_joined"),
                "empty_text": ocr_refs.get("empty_text"),
                "real_provider_invoked": ocr_refs.get("real_provider_invoked"),
                "rapidocr_invoked": ocr_refs.get("rapidocr_invoked"),
                "bridge_pack_ref": ocr_refs.get("ocr_bridge_pack_ref"),
                "bbox_in_frame": ref["spatial_reference"]["bbox_in_frame"],
                "fact_status": "not_fact",
                "fusion_status": "not_fused",
                "ai_interpretation_status": "not_invoked",
            }
        )

        chain_rows.append(
            {
                "reference_id": ref["reference_id"],
                "candidate_id": cand_id,
                "frame_id": frame_id,
                "roi_id": roi_id,
                "vision_roi_proposal_root": vision_proposal_root,
                "vision_roi_to_ocr_bridge_root": str(bridge_root),
                "rapidocr_submission_root": rapid_submission_root,
                "rapidocr_readonly_consumer_root": str(rapid_cons_root),
                "bridge_pack_ref": ocr_refs.get("ocr_bridge_pack_ref"),
            }
        )

    vision_roi_count = len(roi_items)
    rapidocr_evidence_count = len(ocr_by_candidate)
    matched_reference_count = len(references)
    unmatched_vision_keys = set(roi_by_key.keys()) - matched_keys

    unmatched_vision_rows = [
        {
            "frame_id": roi_by_key[k].get("source_frame_id"),
            "roi_id": roi_by_key[k].get("roi_id"),
            "roi_type": roi_by_key[k].get("roi_type"),
            "reason_code": "no_rapidocr_evidence_for_roi",
        }
        for k in sorted(unmatched_vision_keys)
    ]

    alignment = {
        "schema_version": ALIGNMENT_SCHEMA,
        "vision_roi_count": vision_roi_count,
        "rapidocr_evidence_count": rapidocr_evidence_count,
        "matched_reference_count": matched_reference_count,
        "unmatched_vision_roi_count": len(unmatched_vision_keys),
        "unmatched_rapidocr_evidence_count": 0,
        "empty_text_reference_count": empty_text_count,
        "match_key_strategy": "frame_id + roi_id",
        "reference_only": True,
        "provider": "rapidocr_candidate",
        "unmatched_vision_roi_rows": unmatched_vision_rows,
    }

    stub_stats = _load_stub_reference_stats(stub_root)
    comparison = build_stub_vs_rapidocr_comparison_v0(
        stub_stats=stub_stats,
        rapidocr_reference_count=matched_reference_count,
        empty_text_reference_count=empty_text_count,
    )

    chain_summary = {
        "schema_version": CHAIN_SCHEMA,
        "vision_roi_proposal_root": vision_proposal_root,
        "vision_roi_to_ocr_bridge_root": str(bridge_root),
        "rapidocr_submission_root": rapid_submission_root,
        "rapidocr_readonly_consumer_root": str(rapid_cons_root),
        "reference_candidate_build_step": "cross_modal_vision_ocr_reference_only_rapidocr_v0",
        "chain_row_count": len(chain_rows),
        "chains": chain_rows,
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

    audit = build_rapidocr_reference_audit_v0(rapidocr_consumer_audit=rapid_consumer_audit)

    phase_verdict = "GO"
    if matched_reference_count <= 0:
        phase_verdict = "CONDITIONAL_GO" if not errs else "NO_GO"
    elif errs:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-Reference-Only-002",
        "vision_roi_proposal_root": vision_proposal_root,
        "vision_recognition_readonly_consumer_root": str(vis_cons_root),
        "vision_roi_to_ocr_bridge_root": str(bridge_root),
        "rapidocr_readonly_consumer_root": str(rapid_cons_root),
        "stub_reference_root": str(stub_root) if stub_root else None,
        "matched_reference_count": matched_reference_count,
        "unmatched_vision_roi_count": len(unmatched_vision_keys),
        "unmatched_rapidocr_evidence_count": 0,
        "empty_text_reference_count": empty_text_count,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, candidates_doc, matrix_doc, alignment, comparison, chain_summary, audit, errs
