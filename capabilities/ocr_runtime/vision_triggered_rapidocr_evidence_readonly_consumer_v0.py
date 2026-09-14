# -*- coding: utf-8 -*-
"""Read-only consumer for Vision-triggered RapidOCR submission collection.

Phase-Vision-Triggered-OCR-RapidOCR-ReadOnly-Consumer-001
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CONSUMER_VIEW_SCHEMA = "vision_triggered_rapidocr_evidence_readonly_consumer_view_v0"
CONSUMER_ID = "vision_triggered_rapidocr_readonly_consumer_v0"
MATRIX_SCHEMA = "vision_triggered_rapidocr_evidence_matrix_v0"
COMPARISON_SCHEMA = "vision_triggered_rapidocr_provider_comparison_summary_v0"
CHAIN_SCHEMA = "vision_triggered_rapidocr_source_chain_summary_v0"
AUDIT_SCHEMA = "vision_triggered_rapidocr_evidence_readonly_consumer_audit_v0"
SUMMARY_SCHEMA = "vision_triggered_rapidocr_evidence_readonly_consumer_summary_v0"


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _text_joined_from_sources(row: Dict[str, Any], ocr_result: Dict[str, Any]) -> str:
    tj = str(row.get("evidence_text_joined") or row.get("text_joined") or "")
    if tj:
        return tj
    ev = ocr_result.get("ocr_evidence") if isinstance(ocr_result.get("ocr_evidence"), dict) else {}
    bp = ocr_result.get("bridge_pack") if isinstance(ocr_result.get("bridge_pack"), dict) else {}
    return str(ev.get("text_joined") or bp.get("raw_text_joined") or "")


def _text_item_count(row: Dict[str, Any], ocr_result: Dict[str, Any]) -> int:
    n = row.get("text_item_count")
    if isinstance(n, int):
        return n
    ev = ocr_result.get("ocr_evidence") if isinstance(ocr_result.get("ocr_evidence"), dict) else {}
    items = ev.get("text_items") if isinstance(ev.get("text_items"), list) else []
    return len(items)


def _evidence_status_v0(row: Dict[str, Any], text_joined: str) -> str:
    st = str(row.get("submission_status") or "")
    br = str(row.get("ocr_bridge_status") or "")
    if st == "submitted" and br == "success":
        if not str(text_joined).strip():
            return "evidence_available_empty_text"
        return "evidence_available"
    if st == "rejected_by_gate":
        return "gate_rejected"
    if st in ("failed", "blocked_by_gate"):
        return "no_evidence"
    return "unknown"


def _resolve_vision_roi_proposal_root(plan: Dict[str, Any]) -> Optional[str]:
    bridge_root = Path(str(plan.get("source_bridge_root") or ""))
    if bridge_root.is_dir():
        sum_p = bridge_root / "vision_roi_to_ocr_request_bridge_summary.json"
        if sum_p.is_file():
            doc = _read_json(sum_p)
            if isinstance(doc, dict) and doc.get("vision_roi_proposal_root"):
                return str(doc["vision_roi_proposal_root"])
    return None


def _load_stub_consumer_stub_text_summary(stub_consumer_root: Optional[Path]) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "stub_consumer_root": str(stub_consumer_root) if stub_consumer_root else None,
        "stub_text_count": 0,
        "stub_mock_text_rows": 0,
        "stub_provider": None,
    }
    if stub_consumer_root is None or not stub_consumer_root.is_dir():
        return out
    view_p = stub_consumer_root / "vision_triggered_ocr_evidence_readonly_consumer_view.json"
    if not view_p.is_file():
        return out
    view = _read_json(view_p)
    tj_sum = view.get("text_joined_summary") if isinstance(view.get("text_joined_summary"), dict) else {}
    mock = int(tj_sum.get("MOCK_TEXT") or 0)
    out["stub_text_count"] = sum(int(v) for v in tj_sum.values())
    out["stub_mock_text_rows"] = mock
    out["stub_provider"] = view.get("provider")
    return out


def build_provider_comparison_summary_v0(
    *,
    stub_stub_info: Dict[str, Any],
    rapidocr_empty_text_count: int,
    rapidocr_success_count: int,
    stub_fallback_count: int,
) -> Dict[str, Any]:
    return {
        "schema_version": COMPARISON_SCHEMA,
        "stub_consumer_root": stub_stub_info.get("stub_consumer_root"),
        "stub_text_count": stub_stub_info.get("stub_text_count"),
        "stub_mock_text_rows": stub_stub_info.get("stub_mock_text_rows"),
        "stub_provider": stub_stub_info.get("stub_provider"),
        "rapidocr_empty_text_count": rapidocr_empty_text_count,
        "rapidocr_real_provider_invoked": rapidocr_success_count > 0,
        "stub_fallback_count": stub_fallback_count,
        "note": "rapidocr_empty_text_is_valid_real_provider_result",
    }


def build_readonly_consumer_audit_v0(*, submission_audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "vision_triggered_rapidocr_readonly_consumer_executed": True,
        "rapidocr_submission_collection_read": True,
        "rapidocr_invoked_upstream": bool(submission_audit.get("rapidocr_invoked")),
        "real_provider_invoked_upstream": bool(submission_audit.get("real_provider_invoked")),
        "fallback_to_stub_upstream": bool(submission_audit.get("fallback_to_stub_observed")),
        "direct_rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "cross_modal_fusion_invoked": False,
    }


def run_vision_triggered_rapidocr_evidence_readonly_consume_v0(
    *,
    rapidocr_submission_from_vision_roi_root: str,
    stub_ocr_consumer_root: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []
    root = Path(rapidocr_submission_from_vision_roi_root).resolve()
    stub_root = Path(stub_ocr_consumer_root).resolve() if stub_ocr_consumer_root else None

    coll_p = root / "rapidocr_submission_from_vision_roi_collection.json"
    matrix_p = root / "rapidocr_submission_result_matrix.json"
    plan_p = root / "rapidocr_submission_plan_from_vision_roi.json"
    prov_p = root / "rapidocr_submission_provider_summary.json"
    sub_aud_p = root / "rapidocr_submission_from_vision_roi_audit_report.json"

    for label, p in (
        ("collection", coll_p),
        ("result_matrix", matrix_p),
        ("plan", plan_p),
        ("provider_summary", prov_p),
        ("submission_audit", sub_aud_p),
    ):
        if not p.is_file():
            errs.append(f"missing:{label}")

    collection: Dict[str, Any] = _read_json(coll_p) if coll_p.is_file() else {}
    matrix_doc: Dict[str, Any] = _read_json(matrix_p) if matrix_p.is_file() else {}
    plan: Dict[str, Any] = _read_json(plan_p) if plan_p.is_file() else {}
    provider_summary_in: Dict[str, Any] = _read_json(prov_p) if prov_p.is_file() else {}
    submission_audit: Dict[str, Any] = _read_json(sub_aud_p) if sub_aud_p.is_file() else {}

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

    vision_proposal_root = _resolve_vision_roi_proposal_root(plan)
    bridge_root = str(plan.get("source_bridge_root") or "")

    for row in matrix_rows:
        if not isinstance(row, dict):
            continue
        cid = str(row.get("candidate_id") or "")
        ocr_result = result_by_candidate.get(cid, {})
        text_joined = _text_joined_from_sources(row, ocr_result)
        text_item_count = _text_item_count(row, ocr_result)
        empty_text = not str(text_joined).strip()
        evidence_status = _evidence_status_v0(row, text_joined)

        entry = {
            "candidate_id": cid,
            "source_frame_id": str(row.get("source_frame_id") or ""),
            "roi_id": str(row.get("roi_id") or ""),
            "roi_type": str(row.get("roi_type") or ""),
            "crop_image_ref": str(row.get("crop_image_ref") or ""),
            "ocr_request_id": str(row.get("ocr_request_id") or ""),
            "ocr_bridge_status": str(row.get("ocr_bridge_status") or ""),
            "submission_status": str(row.get("submission_status") or ""),
            "selected_provider": str(row.get("selected_provider") or ""),
            "provider_level": str(row.get("selected_provider_level") or ""),
            "real_provider_invoked": bool(row.get("real_provider_invoked")),
            "rapidocr_invoked": bool(row.get("rapidocr_invoked")),
            "fallback_to_stub": bool(row.get("fallback_to_stub")),
            "text_joined": text_joined,
            "text_item_count": text_item_count,
            "empty_text": empty_text,
            "bridge_pack_ref": str(row.get("bridge_pack_ref") or ""),
            "evidence_status": evidence_status,
            "fact_status": "not_fact",
            "fusion_status": "not_fused",
        }
        evidence_by_candidate[cid] = entry

        fid = entry["source_frame_id"]
        rid = entry["roi_id"]
        if fid:
            evidence_by_frame.setdefault(fid, []).append(entry)
        if rid:
            evidence_by_roi.setdefault(rid, []).append(entry)

        if text_joined:
            text_counter[text_joined] += 1

        matrix_out.append(
            {
                "candidate_id": cid,
                "source_frame_id": entry["source_frame_id"],
                "roi_id": entry["roi_id"],
                "roi_type": entry["roi_type"],
                "crop_image_ref": entry["crop_image_ref"],
                "ocr_request_id": entry["ocr_request_id"],
                "ocr_bridge_status": entry["ocr_bridge_status"],
                "selected_provider": entry["selected_provider"],
                "provider_level": entry["provider_level"],
                "real_provider_invoked": entry["real_provider_invoked"],
                "rapidocr_invoked": entry["rapidocr_invoked"],
                "fallback_to_stub": entry["fallback_to_stub"],
                "text_joined": entry["text_joined"],
                "text_item_count": entry["text_item_count"],
                "bridge_pack_ref": entry["bridge_pack_ref"],
                "evidence_status": entry["evidence_status"],
                "fact_status": "not_fact",
                "fusion_status": "not_fused",
            }
        )

        chain_rows.append(
            {
                "candidate_id": cid,
                "source_frame_id": fid,
                "roi_id": rid,
                "vision_roi_proposal_root": vision_proposal_root,
                "vision_roi_to_ocr_bridge_root": bridge_root,
                "rapidocr_submission_root": str(root),
                "bridge_pack_ref": entry["bridge_pack_ref"],
                "selected_provider": entry["selected_provider"],
                "evidence_status": evidence_status,
            }
        )

    submission_count = int(collection.get("submission_count") or len(matrix_rows))
    success_count = int(collection.get("success_count") or 0)
    failed_count = int(collection.get("failed_count") or 0)
    rapidocr_success_count = int(collection.get("rapidocr_success_count") or 0)
    stub_fallback_count = int(collection.get("stub_fallback_count") or 0)
    empty_text_count = int(collection.get("empty_text_count") or sum(1 for r in matrix_out if not str(r.get("text_joined") or "").strip()))

    provider_level = "lightweight"
    if matrix_out:
        provider_level = str(matrix_out[0].get("provider_level") or "lightweight")

    view = {
        "schema_version": CONSUMER_VIEW_SCHEMA,
        "consumer_id": CONSUMER_ID,
        "source_submission_root": str(root),
        "submission_count": submission_count,
        "success_count": success_count,
        "failed_count": failed_count,
        "provider": "rapidocr_candidate",
        "provider_level": provider_level,
        "rapidocr_success_count": rapidocr_success_count,
        "stub_fallback_count": stub_fallback_count,
        "empty_text_count": empty_text_count,
        "evidence_by_candidate": evidence_by_candidate,
        "evidence_by_frame": evidence_by_frame,
        "evidence_by_roi": evidence_by_roi,
        "text_joined_summary": dict(text_counter),
        "fact_status": "not_fact",
        "fusion_status": "not_fused",
        "ai_interpretation_status": "not_invoked",
    }

    chain_summary = {
        "schema_version": CHAIN_SCHEMA,
        "vision_roi_proposal_root": vision_proposal_root,
        "vision_roi_to_ocr_bridge_root": bridge_root,
        "rapidocr_submission_root": str(root),
        "chain_row_count": len(chain_rows),
        "chains": chain_rows,
    }

    stub_info = _load_stub_consumer_stub_text_summary(stub_root)
    comparison = build_provider_comparison_summary_v0(
        stub_stub_info=stub_info,
        rapidocr_empty_text_count=empty_text_count,
        rapidocr_success_count=rapidocr_success_count,
        stub_fallback_count=stub_fallback_count,
    )

    matrix_doc_out = {
        "schema_version": MATRIX_SCHEMA,
        "row_count": len(matrix_out),
        "rows": matrix_out,
    }

    audit = build_readonly_consumer_audit_v0(submission_audit=submission_audit)

    phase_verdict = "GO"
    if success_count <= 0 and matrix_out:
        phase_verdict = "CONDITIONAL_GO"
    if errs and success_count <= 0:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-Vision-Triggered-OCR-RapidOCR-ReadOnly-Consumer-001",
        "rapidocr_submission_from_vision_roi_root": str(root),
        "stub_ocr_consumer_root": str(stub_root) if stub_root else None,
        "submission_count": submission_count,
        "success_count": success_count,
        "failed_count": failed_count,
        "provider": view["provider"],
        "provider_level": provider_level,
        "rapidocr_success_count": rapidocr_success_count,
        "stub_fallback_count": stub_fallback_count,
        "empty_text_count": empty_text_count,
        "candidate_index_count": len(evidence_by_candidate),
        "frame_index_count": len(evidence_by_frame),
        "roi_index_count": len(evidence_by_roi),
        "upstream_provider_summary": provider_summary_in,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, view, matrix_doc_out, comparison, chain_summary, audit, errs
