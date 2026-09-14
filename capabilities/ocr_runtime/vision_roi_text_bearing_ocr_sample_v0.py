# -*- coding: utf-8 -*-
"""Text-bearing Vision ROI end-to-end OCR sample (RapidOCR via bridge only).

Phase-Vision-ROI-Text-Bearing-Sample-For-OCR-001
"""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0
from capabilities.ocr_runtime.rapidocr_submission_from_vision_roi_v0 import _bridge_row_fields

SAMPLE_REPORT_SCHEMA = "vision_roi_text_bearing_sample_report_v0"
OCR_CANDIDATE_SCHEMA = "vision_roi_to_ocr_request_candidate_v0"
SUBMISSION_RESULT_SCHEMA = "vision_roi_text_bearing_rapidocr_submission_result_v0"
CONSUMER_VIEW_SCHEMA = "vision_triggered_rapidocr_evidence_readonly_consumer_view_v0"
REFERENCE_SCHEMA = "cross_modal_vision_ocr_reference_candidate_v0"
AUDIT_SCHEMA = "vision_roi_text_bearing_ocr_sample_audit_v0"
SUMMARY_SCHEMA = "vision_roi_text_bearing_ocr_sample_summary_v0"

FRAME_ID = "stream_text_bearing_smoke_f000000"
STREAM_ID = "stream_text_bearing_smoke"
ROI_TYPE = "upper_sign_roi"

FORBIDDEN_ACTIONS_V0: Dict[str, bool] = {
    "write_midplatform_fact": True,
    "write_scene_delta": True,
    "write_world_model": True,
    "invoke_ai_interpretation": True,
    "invoke_navigation_decision": True,
    "claim_fused_fact": True,
}


def _env_true(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).strip().lower() in ("1", "true", "yes", "on")


def _write_json(p: Path, obj: object) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _roi_id_for_frame(frame_id: str, roi_type: str) -> str:
    safe = frame_id.replace("-", "_")
    return f"vision_roi_{safe}_{roi_type}"


def create_text_bearing_fixture_v0(
    work_dir: Path,
    *,
    frame_w: int = 640,
    frame_h: int = 480,
) -> Dict[str, Any]:
    """Create frame + upper_sign_roi crop with readable text (local fixture only)."""
    from PIL import Image, ImageDraw, ImageFont

    work_dir.mkdir(parents=True, exist_ok=True)
    x1, y1, x2, y2 = (
        int(frame_w * 0.2),
        0,
        int(frame_w * 0.8),
        int(frame_h * 0.25),
    )

    frame_path = (work_dir / "text_bearing_frame.png").resolve()
    crop_path = (work_dir / "text_bearing_upper_sign_roi_crop.png").resolve()

    img = Image.new("RGB", (frame_w, frame_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font: Any = None
    for fp in (
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            font = ImageFont.truetype(fp, 36)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()

    lines = ("LUNA TEXT 123", "中文测试")
    tx, ty = x1 + 16, y1 + 12
    line_gap = 48 if font != ImageFont.load_default() else 18
    for line in lines:
        draw.text((tx, ty), line, fill=(0, 0, 0), font=font)
        ty += line_gap

    img.save(frame_path, format="PNG")
    crop = img.crop((x1, y1, x2, y2))
    crop.save(crop_path, format="PNG")
    cw, ch = crop.size

    roi_id = _roi_id_for_frame(FRAME_ID, ROI_TYPE)
    return {
        "image_ref": str(frame_path),
        "crop_image_ref": str(crop_path),
        "width": frame_w,
        "height": frame_h,
        "crop_width": cw,
        "crop_height": ch,
        "bbox_in_frame": [x1, y1, x2, y2],
        "roi_bbox_in_crop": [0, 0, cw, ch],
        "roi_id": roi_id,
        "source_frame_id": FRAME_ID,
        "stream_id": STREAM_ID,
        "expected_text_hint": list(lines),
    }


def build_ocr_request_candidate_v0(
    *,
    crop_image_ref: str,
    roi_bbox_in_crop: List[int],
    candidate_id: str,
) -> Dict[str, Any]:
    x1, y1, x2, y2 = roi_bbox_in_crop
    req = OCRRequestV0(
        input_type="roi",
        image_path=crop_image_ref,
        roi_refs=[f"ocr_roi_xyxy:{x1},{y1},{x2},{y2}"],
        source_task_id=None,
        task_context="vision_roi_text_bearing_sample",
        latency_budget_ms=1000,
        urgency="async",
        allow_heavy_ocr=False,
        allow_remote=False,
        allow_full_image=False,
        expected_output="ocr_evidence",
    )
    ocr_dict = req.to_dict()
    ocr_dict["source_task_id"] = None
    return {
        "schema_version": OCR_CANDIDATE_SCHEMA,
        "candidate_id": candidate_id,
        "source": "vision_roi_text_bearing_fixture",
        "source_frame_id": FRAME_ID,
        "stream_id": STREAM_ID,
        "roi_id": _roi_id_for_frame(FRAME_ID, ROI_TYPE),
        "roi_type": ROI_TYPE,
        "crop_image_ref": crop_image_ref,
        "bbox_in_frame": roi_bbox_in_crop,
        "ocr_request": ocr_dict,
        "candidate_status": "not_submitted",
        "ocr_provider_invoked": False,
        "ocr_runtime_invoked": False,
        "fact_status": "not_fact",
    }


def build_sample_audit_v0(*, submission_fields: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "text_bearing_ocr_sample_executed": True,
        "eval_only": _env_true("LUNA_OCR_SUBMISSION_EVAL_ONLY", "false"),
        "rapidocr_invoked_upstream": bool(submission_fields.get("rapidocr_invoked")),
        "real_provider_invoked_upstream": bool(submission_fields.get("real_provider_invoked")),
        "direct_rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "cross_modal_fusion_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "navigation_decision_invoked": False,
    }


def build_cross_modal_reference_v0(
    *,
    fixture: Dict[str, Any],
    candidate_id: str,
    ocr_entry: Dict[str, Any],
    bridge_pack_ref: str,
) -> Dict[str, Any]:
    text_joined = str(ocr_entry.get("evidence_text_joined") or "")
    empty_text = not text_joined.strip()
    return {
        "schema_version": REFERENCE_SCHEMA,
        "reference_id": f"xref_{uuid.uuid4().hex[:16]}",
        "reference_scope": "reference_only",
        "source": "vision_roi_triggered_rapidocr",
        "frame_id": FRAME_ID,
        "roi_id": str(fixture.get("roi_id") or ""),
        "roi_type": ROI_TYPE,
        "vision_refs": {
            "roi_ref": fixture.get("roi_id"),
            "vision_evidence_refs": [],
        },
        "ocr_refs": {
            "ocr_provider": str(ocr_entry.get("selected_provider") or "rapidocr_candidate"),
            "provider_level": str(ocr_entry.get("selected_provider_level") or "lightweight"),
            "ocr_request_candidate_id": candidate_id,
            "ocr_request_id": str(ocr_entry.get("ocr_request_id") or ""),
            "ocr_bridge_pack_ref": bridge_pack_ref,
            "ocr_text_joined": text_joined,
            "empty_text": empty_text,
            "real_provider_invoked": bool(ocr_entry.get("real_provider_invoked")),
            "rapidocr_invoked": bool(ocr_entry.get("rapidocr_invoked")),
        },
        "spatial_reference": {
            "bbox_in_frame": list(fixture.get("bbox_in_frame") or [0, 0, 0, 0]),
            "coordinate_space": "frame_pixel",
        },
        "fact_status": "not_fact",
        "fusion_status": "not_fused",
        "ai_interpretation_status": "not_invoked",
        "allowed_next_actions": ["manual_review", "future_cross_modal_fusion_candidate"],
        "forbidden_actions": dict(FORBIDDEN_ACTIONS_V0),
    }


def run_vision_roi_text_bearing_ocr_sample_v0(
    *,
    workspace_root: Path,
    governance_config_path: Path,
    sample_work_root: Path,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []
    work = sample_work_root.resolve()
    work.mkdir(parents=True, exist_ok=True)

    fixture = create_text_bearing_fixture_v0(work)
    candidate_id = f"ocr_req_cand_text_bearing_{uuid.uuid4().hex[:8]}"

    sample_report = {
        "schema_version": SAMPLE_REPORT_SCHEMA,
        "image_ref": fixture["image_ref"],
        "crop_image_ref": fixture["crop_image_ref"],
        "width": fixture["width"],
        "height": fixture["height"],
        "crop_width": fixture["crop_width"],
        "crop_height": fixture["crop_height"],
        "roi_type": ROI_TYPE,
        "source_type": "text_bearing_fixture",
        "network_request_invoked": False,
        "expected_text_hint": fixture["expected_text_hint"],
        "bbox_in_frame": fixture["bbox_in_frame"],
        "roi_id": fixture["roi_id"],
        "source_frame_id": fixture["source_frame_id"],
        "source_chain": [
            "text_bearing_fixture_generated",
            f"frame_ref:{fixture['image_ref']}",
            f"crop_ref:{fixture['crop_image_ref']}",
        ],
    }

    ocr_candidate = build_ocr_request_candidate_v0(
        crop_image_ref=str(fixture["crop_image_ref"]),
        roi_bbox_in_crop=list(fixture["roi_bbox_in_crop"]),
        candidate_id=candidate_id,
    )

    req = OCRRequestV0(
        input_type="roi",
        image_path=str(fixture["crop_image_ref"]),
        roi_refs=list(ocr_candidate["ocr_request"]["roi_refs"]),
        source_task_id=None,
        task_context="vision_roi_text_bearing_sample",
        latency_budget_ms=1000,
        urgency="async",
        allow_heavy_ocr=False,
        allow_remote=False,
        allow_full_image=False,
        expected_output="ocr_evidence",
    )

    bridge_result: Dict[str, Any] = {}
    submission_fields: Dict[str, Any] = {}
    bridge_pack_ref = ""

    if not _env_true("LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0", "false"):
        errs.append("gate_disabled:LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0")
    else:
        try:
            bridge_result = run_ocr_mainline_bridge_v0(
                req,
                governance_config_path=governance_config_path,
                workspace_root=workspace_root,
                normalization_work_dir=work / "norm",
            )
        except Exception as e:
            errs.append(f"bridge_exception:{type(e).__name__}:{e}")
            bridge_result = {"status": "error", "error": str(e)}

    bridge_path = work / "ocr_mainline_bridge_result.json"
    _write_json(bridge_path, bridge_result)
    bp = bridge_result.get("bridge_pack") if isinstance(bridge_result.get("bridge_pack"), dict) else {}
    if bp:
        bridge_pack_path = work / "ocr_bridge_pack.json"
        _write_json(bridge_pack_path, bp)
        bridge_pack_ref = str(bridge_pack_path.resolve())

    submission_fields = _bridge_row_fields(bridge_result)
    submission_fields["ocr_request_id"] = str(req.request_id)
    submission_fields["ocr_bridge_status"] = str(bridge_result.get("status") or "")
    submission_fields["submission_status"] = (
        "submitted" if submission_fields["ocr_bridge_status"] == "success" else "failed"
    )
    submission_fields["bridge_pack_ref"] = bridge_pack_ref

    submission_result = {
        "schema_version": SUBMISSION_RESULT_SCHEMA,
        "candidate_id": candidate_id,
        "source_frame_id": FRAME_ID,
        "roi_id": fixture["roi_id"],
        "roi_type": ROI_TYPE,
        "crop_image_ref": fixture["crop_image_ref"],
        **submission_fields,
        "error": bridge_result.get("error"),
    }

    text_joined = str(submission_fields.get("evidence_text_joined") or "")
    empty_text = not text_joined.strip()

    consumer_entry = {
        "candidate_id": candidate_id,
        "source_frame_id": FRAME_ID,
        "roi_id": fixture["roi_id"],
        "roi_type": ROI_TYPE,
        "crop_image_ref": fixture["crop_image_ref"],
        "ocr_request_id": req.request_id,
        "ocr_bridge_status": submission_fields["ocr_bridge_status"],
        "submission_status": submission_fields["submission_status"],
        "selected_provider": submission_fields.get("selected_provider"),
        "provider_level": submission_fields.get("selected_provider_level"),
        "real_provider_invoked": submission_fields.get("real_provider_invoked"),
        "rapidocr_invoked": submission_fields.get("rapidocr_invoked"),
        "fallback_to_stub": submission_fields.get("fallback_to_stub"),
        "text_joined": text_joined,
        "text_item_count": submission_fields.get("text_item_count"),
        "empty_text": empty_text,
        "bridge_pack_ref": bridge_pack_ref,
        "evidence_status": "evidence_available" if not empty_text else "evidence_available_empty_text",
        "fact_status": "not_fact",
        "fusion_status": "not_fused",
    }

    consumer_view = {
        "schema_version": CONSUMER_VIEW_SCHEMA,
        "consumer_id": "vision_triggered_rapidocr_readonly_consumer_v0",
        "source_submission_root": str(work),
        "submission_count": 1,
        "success_count": 1 if submission_fields["ocr_bridge_status"] == "success" else 0,
        "failed_count": 0 if submission_fields["ocr_bridge_status"] == "success" else 1,
        "provider": str(submission_fields.get("selected_provider") or "rapidocr_candidate"),
        "provider_level": str(submission_fields.get("selected_provider_level") or "lightweight"),
        "rapidocr_success_count": 1 if submission_fields.get("rapidocr_invoked") else 0,
        "stub_fallback_count": 0,
        "empty_text_count": 1 if empty_text else 0,
        "evidence_by_candidate": {candidate_id: consumer_entry},
        "evidence_by_frame": {FRAME_ID: [consumer_entry]},
        "evidence_by_roi": {fixture["roi_id"]: [consumer_entry]},
        "text_joined_summary": {text_joined: 1} if text_joined else {},
        "fact_status": "not_fact",
        "fusion_status": "not_fused",
        "ai_interpretation_status": "not_invoked",
    }

    reference = build_cross_modal_reference_v0(
        fixture=fixture,
        candidate_id=candidate_id,
        ocr_entry=submission_fields,
        bridge_pack_ref=bridge_pack_ref,
    )

    audit = build_sample_audit_v0(submission_fields=submission_fields)

    phase_verdict = "GO"
    if not text_joined.strip():
        phase_verdict = "CONDITIONAL_GO"
    if submission_fields.get("fallback_to_stub"):
        phase_verdict = "CONDITIONAL_GO"
    if errs and not text_joined.strip():
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-Vision-ROI-Text-Bearing-Sample-For-OCR-001",
        "text_bearing_sample_path": str(work),
        "text_joined": text_joined,
        "empty_text": empty_text,
        "rapidocr_invoked": bool(submission_fields.get("rapidocr_invoked")),
        "real_provider_invoked": bool(submission_fields.get("real_provider_invoked")),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return (
        summary,
        sample_report,
        ocr_candidate,
        submission_result,
        consumer_view,
        reference,
        audit,
        errs,
    )
