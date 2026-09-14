# -*- coding: utf-8 -*-
"""Read-only consumer for Vision-triggered OCR submission collection.

Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CONSUMER_VIEW_SCHEMA = "vision_triggered_ocr_evidence_readonly_consumer_view_v0"
CONSUMER_ID = "vision_triggered_ocr_readonly_consumer_v0"
MATRIX_SCHEMA = "vision_triggered_ocr_evidence_matrix_v0"
CHAIN_SCHEMA = "vision_triggered_ocr_source_chain_summary_v0"
AUDIT_SCHEMA = "vision_triggered_ocr_evidence_readonly_consumer_audit_v0"
SUMMARY_SCHEMA = "vision_triggered_ocr_evidence_readonly_consumer_summary_v0"


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _provider_from_result(entry: Dict[str, Any]) -> str:
    ev = entry.get("ocr_evidence") if isinstance(entry.get("ocr_evidence"), dict) else {}
    bp = entry.get("bridge_pack") if isinstance(entry.get("bridge_pack"), dict) else {}
    pt = bp.get("provider_trace") if isinstance(bp.get("provider_trace"), dict) else {}
    return str(ev.get("provider") or pt.get("provider") or "unknown")


def _text_joined_from_result(entry: Dict[str, Any]) -> str:
    ev = entry.get("ocr_evidence") if isinstance(entry.get("ocr_evidence"), dict) else {}
    bp = entry.get("bridge_pack") if isinstance(entry.get("bridge_pack"), dict) else {}
    return str(ev.get("text_joined") or bp.get("raw_text_joined") or "")


def _evidence_status_from_row(row: Dict[str, Any]) -> str:
    st = str(row.get("submission_status") or "")
    br = str(row.get("ocr_bridge_status") or "")
    if st == "submitted" and br == "success":
        return "evidence_available"
    if st == "rejected_by_gate":
        return "gate_rejected"
    if st in ("failed", "blocked_by_gate"):
        return "no_evidence"
    return "unknown"


def _canonical_evidence_entry_v0(
    *,
    candidate_id: str,
    row: Dict[str, Any],
    ocr_result: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "source_frame_id": str(row.get("source_frame_id") or ""),
        "roi_id": str(row.get("roi_id") or ocr_result.get("roi_id") or ""),
        "roi_type": str(row.get("roi_type") or ""),
        "crop_image_ref": str(row.get("crop_image_ref") or ""),
        "ocr_request_id": str(row.get("ocr_request_id") or ocr_result.get("ocr_request_id") or ""),
        "ocr_bridge_status": str(row.get("ocr_bridge_status") or ocr_result.get("ocr_bridge_status") or ""),
        "submission_status": str(row.get("submission_status") or ocr_result.get("submission_status") or ""),
        "provider": _provider_from_result(ocr_result),
        "text_joined": _text_joined_from_result(ocr_result),
        "bridge_pack_ref": str(row.get("bridge_pack_ref") or ocr_result.get("bridge_pack_ref") or ""),
        "evidence_status": _evidence_status_from_row(row),
        "fact_status": "not_fact",
        "fusion_status": "not_fused",
    }


def _resolve_vision_roi_proposal_root(plan: Dict[str, Any], submission_root: Path) -> Optional[str]:
    bridge_root = Path(str(plan.get("source_bridge_root") or ""))
    if bridge_root.is_dir():
        sum_p = bridge_root / "vision_roi_to_ocr_request_bridge_summary.json"
        if sum_p.is_file():
            doc = _read_json(sum_p)
            if isinstance(doc, dict) and doc.get("vision_roi_proposal_root"):
                return str(doc["vision_roi_proposal_root"])
    return None


def build_source_chain_summary_v0(
    *,
    vision_roi_proposal_root: Optional[str],
    chain_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "schema_version": CHAIN_SCHEMA,
        "vision_roi_proposal_root": vision_roi_proposal_root,
        "chain_row_count": len(chain_rows),
        "chains": chain_rows,
    }


def build_readonly_consumer_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "vision_triggered_ocr_readonly_consumer_executed": True,
        "ocr_submission_collection_read": True,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "cross_modal_fusion_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
    }


def run_vision_triggered_ocr_evidence_readonly_consume_v0(
    *,
    ocr_submission_from_vision_roi_root: str,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []
    root = Path(ocr_submission_from_vision_roi_root).resolve()

    coll_p = root / "ocr_submission_from_vision_roi_collection.json"
    matrix_p = root / "ocr_request_submission_result_matrix.json"
    plan_p = root / "ocr_request_submission_plan_from_vision_roi.json"
    sub_aud_p = root / "ocr_request_submission_from_vision_roi_audit_report.json"

    for label, p in (
        ("collection", coll_p),
        ("result_matrix", matrix_p),
        ("plan", plan_p),
        ("submission_audit", sub_aud_p),
    ):
        if not p.is_file():
            errs.append(f"missing:{label}")

    collection: Dict[str, Any] = _read_json(coll_p) if coll_p.is_file() else {}
    matrix_doc: Dict[str, Any] = _read_json(matrix_p) if matrix_p.is_file() else {}
    plan: Dict[str, Any] = _read_json(plan_p) if plan_p.is_file() else {}

    matrix_rows = matrix_doc.get("rows") if isinstance(matrix_doc.get("rows"), list) else []
    ocr_results = collection.get("ocr_results") if isinstance(collection.get("ocr_results"), list) else []

    result_by_candidate: Dict[str, Dict[str, Any]] = {}
    for item in ocr_results:
        if isinstance(item, dict) and item.get("candidate_id"):
            result_by_candidate[str(item["candidate_id"])] = item

    evidence_by_candidate: Dict[str, Dict[str, Any]] = {}
    evidence_by_frame: Dict[str, List[Dict[str, Any]]] = {}
    evidence_by_roi: Dict[str, List[Dict[str, Any]]] = {}
    matrix_out: List[Dict[str, Any]] = []
    chain_rows: List[Dict[str, Any]] = []
    text_counter: Counter[str] = Counter()
    providers: Counter[str] = Counter()

    vision_proposal_root = _resolve_vision_roi_proposal_root(plan, root)

    for row in matrix_rows:
        if not isinstance(row, dict):
            continue
        cid = str(row.get("candidate_id") or "")
        ocr_result = result_by_candidate.get(cid, {})
        entry = _canonical_evidence_entry_v0(candidate_id=cid, row=row, ocr_result=ocr_result)
        evidence_by_candidate[cid] = entry

        fid = entry["source_frame_id"]
        rid = entry["roi_id"]
        if fid:
            evidence_by_frame.setdefault(fid, []).append(entry)
        if rid:
            evidence_by_roi.setdefault(rid, []).append(entry)

        tj = str(entry.get("text_joined") or "")
        if tj:
            text_counter[tj] += 1
        providers[str(entry.get("provider") or "unknown")] += 1

        matrix_out.append(
            {
                "candidate_id": cid,
                "source_frame_id": entry["source_frame_id"],
                "roi_id": entry["roi_id"],
                "roi_type": entry["roi_type"],
                "crop_image_ref": entry["crop_image_ref"],
                "ocr_request_id": entry["ocr_request_id"],
                "ocr_bridge_status": entry["ocr_bridge_status"],
                "provider": entry["provider"],
                "text_joined": entry["text_joined"],
                "bridge_pack_ref": entry["bridge_pack_ref"],
                "evidence_status": entry["evidence_status"],
                "fact_status": "not_fact",
                "fusion_status": "not_fused",
            }
        )

        chain_rows.append(
            {
                "candidate_id": cid,
                "vision_roi_proposal_root": vision_proposal_root,
                "ocr_request_candidate_source_bridge_root": str(plan.get("source_bridge_root") or ""),
                "ocr_bridge_submission_status": entry["submission_status"],
                "ocr_bridge_status": entry["ocr_bridge_status"],
                "bridge_pack_ref": entry["bridge_pack_ref"],
            }
        )

    submission_count = int(collection.get("submission_count") or len(matrix_rows))
    success_count = int(collection.get("success_count") or 0)
    failed_count = int(collection.get("failed_count") or 0)
    dominant_provider = providers.most_common(1)[0][0] if providers else "unknown"

    view = {
        "schema_version": CONSUMER_VIEW_SCHEMA,
        "consumer_id": CONSUMER_ID,
        "source_submission_root": str(root),
        "submission_count": submission_count,
        "success_count": success_count,
        "failed_count": failed_count,
        "provider": dominant_provider,
        "evidence_by_candidate": evidence_by_candidate,
        "evidence_by_frame": evidence_by_frame,
        "evidence_by_roi": evidence_by_roi,
        "text_joined_summary": dict(text_counter),
        "fact_status": "not_fact",
        "fusion_status": "not_fused",
        "ai_interpretation_status": "not_invoked",
    }

    chain_summary = build_source_chain_summary_v0(
        vision_roi_proposal_root=vision_proposal_root,
        chain_rows=chain_rows,
    )

    matrix_doc_out = {
        "schema_version": MATRIX_SCHEMA,
        "row_count": len(matrix_out),
        "rows": matrix_out,
    }

    audit = build_readonly_consumer_audit_v0()

    phase_verdict = "GO"
    if success_count <= 0 and matrix_out:
        phase_verdict = "CONDITIONAL_GO"
    if errs and success_count <= 0:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001",
        "ocr_submission_from_vision_roi_root": str(root),
        "submission_count": submission_count,
        "success_count": success_count,
        "failed_count": failed_count,
        "provider": dominant_provider,
        "candidate_index_count": len(evidence_by_candidate),
        "frame_index_count": len(evidence_by_frame),
        "roi_index_count": len(evidence_by_roi),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, view, matrix_doc_out, chain_summary, audit, errs
