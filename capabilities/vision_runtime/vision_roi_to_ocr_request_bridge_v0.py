# -*- coding: utf-8 -*-
"""Vision ROI → OCRRequest candidate bridge (no OCR invoke, no fusion).

Phase-Vision-ROI-to-OCR-Request-Bridge-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

CANDIDATE_SCHEMA = "vision_roi_to_ocr_request_candidate_v0"
CANDIDATES_DOC_SCHEMA = "vision_roi_to_ocr_request_candidates_v0"
MATRIX_SCHEMA = "vision_roi_to_ocr_request_candidate_matrix_v0"
REJECTION_SCHEMA = "vision_roi_to_ocr_rejection_matrix_v0"
AUDIT_SCHEMA = "vision_roi_to_ocr_request_bridge_audit_v0"
SUMMARY_SCHEMA = "vision_roi_to_ocr_request_bridge_summary_v0"


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _stream_id_from_frame_id(frame_id: str) -> Optional[str]:
    fid = str(frame_id or "")
    if "_f" in fid:
        return fid.rsplit("_f", 1)[0]
    return fid or None


def _roi_ref_xyxy_v0(bbox: List[int], roi_id: str) -> str:
    x1, y1, x2, y2 = (int(v) for v in bbox)
    return f"ocr_roi_xyxy:{x1},{y1},{x2},{y2}"


def _should_trigger_ocr_v0(roi_item: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    roi_type = str(roi_item.get("roi_type") or "")
    task_hint = str(roi_item.get("task_hint") or "")
    if roi_type == "upper_sign_roi":
        return True, None
    if roi_type == "center_roi" and task_hint == "sign_region":
        return True, None
    if roi_type == "center_roi":
        return False, "center_roi_not_text_candidate"
    if roi_type == "ground_roi":
        return False, "ground_roi_not_ocr_candidate"
    return False, "non_text_roi"


def _index_units_by_roi_id(pack_bundle: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    packs = pack_bundle.get("packs") if isinstance(pack_bundle.get("packs"), list) else []
    for pack in packs:
        if not isinstance(pack, dict):
            continue
        source_frame_id = str(pack.get("source_frame_id") or "")
        for unit in pack.get("input_units") or []:
            if not isinstance(unit, dict):
                continue
            rid = str(unit.get("roi_id") or "")
            if rid and rid not in out:
                out[rid] = {**unit, "source_frame_id": source_frame_id or unit.get("source_frame_id")}
    return out


def build_ocr_request_for_roi_v0(
    *,
    roi_item: Dict[str, Any],
    unit: Dict[str, Any],
) -> Dict[str, Any]:
    bbox = roi_item.get("bbox_in_frame")
    if not isinstance(bbox, list) or len(bbox) != 4:
        bbox = unit.get("bbox_in_frame") or [0, 0, 0, 0]
    bbox_i = [int(v) for v in bbox]
    crop_ref = str(unit.get("image_ref") or "")
    roi_id = str(roi_item.get("roi_id") or unit.get("roi_id") or "")

    req = OCRRequestV0(
        input_type="roi",
        image_path=crop_ref,
        roi_refs=[_roi_ref_xyxy_v0(bbox_i, roi_id)],
        source_task_id=None,
        task_context="vision_roi_to_ocr_bridge",
        latency_budget_ms=1000,
        urgency="async",
        allow_heavy_ocr=False,
        allow_remote=False,
        allow_full_image=False,
        expected_output="ocr_evidence",
    )
    ocr_dict = req.to_dict()
    ocr_dict["source_task_id"] = None
    return ocr_dict


def build_candidate_v0(
    *,
    roi_item: Dict[str, Any],
    unit: Dict[str, Any],
) -> Dict[str, Any]:
    roi_id = str(roi_item.get("roi_id") or "")
    unit_id = str(unit.get("unit_id") or "")
    source_frame_id = str(roi_item.get("source_frame_id") or unit.get("source_frame_id") or "")
    bbox = roi_item.get("bbox_in_frame")
    if not isinstance(bbox, list) or len(bbox) != 4:
        bbox = unit.get("bbox_in_frame") or [0, 0, 0, 0]

    return {
        "schema_version": CANDIDATE_SCHEMA,
        "candidate_id": f"ocr_req_cand_{uuid.uuid4().hex[:16]}",
        "source": "vision_roi_proposal",
        "source_frame_id": source_frame_id,
        "stream_id": _stream_id_from_frame_id(source_frame_id),
        "roi_id": roi_id,
        "roi_type": str(roi_item.get("roi_type") or ""),
        "unit_id": unit_id,
        "source_unit_ref": unit_id,
        "crop_image_ref": str(unit.get("image_ref") or ""),
        "bbox_in_frame": [int(v) for v in bbox],
        "ocr_request": build_ocr_request_for_roi_v0(roi_item=roi_item, unit=unit),
        "candidate_status": "not_submitted",
        "ocr_provider_invoked": False,
        "ocr_runtime_invoked": False,
        "fact_status": "not_fact",
    }


def build_bridge_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "vision_roi_to_ocr_request_bridge_executed": True,
        "ocr_request_candidates_generated": True,
        "ocr_provider_invoked": False,
        "ocr_runtime_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "yolo_invoked": False,
        "real_detector_invoked": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "database_write_invoked": False,
        "external_bus_invoked": False,
    }


def run_vision_roi_to_ocr_request_bridge_v0(
    *,
    vision_roi_proposal_root: str,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []
    root = Path(vision_roi_proposal_root).resolve()

    cand_p = root / "vision_roi_proposal_candidate.json"
    pack_p = root / "vision_provider_input_pack.json"
    audit_p = root / "vision_roi_proposal_audit_report.json"

    for label, p in (("vision_roi_proposal_candidate", cand_p), ("vision_provider_input_pack", pack_p)):
        if not p.is_file():
            errs.append(f"missing:{label}")

    roi_doc: Dict[str, Any] = {}
    pack_bundle: Dict[str, Any] = {}
    if cand_p.is_file():
        raw = _read_json(cand_p)
        if isinstance(raw, dict):
            roi_doc = raw
        else:
            errs.append("vision_roi_proposal_candidate_invalid")

    if pack_p.is_file():
        raw = _read_json(pack_p)
        if isinstance(raw, dict):
            pack_bundle = raw
        else:
            errs.append("vision_provider_input_pack_invalid")

    roi_items = roi_doc.get("roi_items") if isinstance(roi_doc.get("roi_items"), list) else []
    unit_by_roi = _index_units_by_roi_id(pack_bundle)

    candidates: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    rejections: List[Dict[str, Any]] = []

    for roi_item in roi_items:
        if not isinstance(roi_item, dict):
            continue
        roi_id = str(roi_item.get("roi_id") or "")
        trigger, reason = _should_trigger_ocr_v0(roi_item)
        unit = unit_by_roi.get(roi_id)
        if trigger:
            if unit is None:
                rejections.append(
                    {
                        "roi_id": roi_id,
                        "roi_type": roi_item.get("roi_type"),
                        "reason_code": "missing_input_unit_for_roi",
                    }
                )
                errs.append(f"missing_unit:{roi_id}")
                continue
            crop_ref = str(unit.get("image_ref") or "")
            if not crop_ref or not Path(crop_ref).is_file():
                rejections.append(
                    {
                        "roi_id": roi_id,
                        "roi_type": roi_item.get("roi_type"),
                        "reason_code": "crop_image_ref_missing",
                    }
                )
                continue
            cand = build_candidate_v0(roi_item=roi_item, unit=unit)
            candidates.append(cand)
            matrix_rows.append(
                {
                    "candidate_id": cand["candidate_id"],
                    "source_frame_id": cand["source_frame_id"],
                    "roi_id": cand["roi_id"],
                    "roi_type": cand["roi_type"],
                    "unit_id": cand["unit_id"],
                    "crop_image_ref": cand["crop_image_ref"],
                    "bbox_in_frame": cand["bbox_in_frame"],
                    "ocr_request_status": "not_submitted",
                    "ocr_provider_invoked": False,
                }
            )
        else:
            rejections.append(
                {
                    "roi_id": roi_id,
                    "roi_type": roi_item.get("roi_type"),
                    "reason_code": reason or "non_text_roi",
                }
            )

    candidates_doc = {
        "schema": CANDIDATES_DOC_SCHEMA,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }

    matrix_doc = {
        "schema": MATRIX_SCHEMA,
        "row_count": len(matrix_rows),
        "rows": matrix_rows,
    }

    rejection_doc = {
        "schema": REJECTION_SCHEMA,
        "rejection_count": len(rejections),
        "rows": rejections,
    }

    audit = build_bridge_audit_v0()

    phase_verdict = "GO"
    if not candidates:
        phase_verdict = "CONDITIONAL_GO"
    if errs and not candidates:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-Vision-ROI-to-OCR-Request-Bridge-001",
        "vision_roi_proposal_root": str(root),
        "vision_roi_proposal_audit_present": audit_p.is_file(),
        "roi_items_total": len(roi_items),
        "candidate_count": len(candidates),
        "rejection_count": len(rejections),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return summary, candidates_doc, matrix_doc, rejection_doc, audit, errs
