# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard expansion (evaluation-only, no writes).

Phase-CrossModal-Vision-OCR-TestBoard-Expansion-001
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

REGISTRY_SCHEMA = "cross_modal_vision_ocr_testboard_registry_v0"
FIXTURE_MANIFEST_SCHEMA = "cross_modal_vision_ocr_testboard_fixture_manifest_v0"
EXPECTED_BEHAVIOR_SCHEMA = "cross_modal_vision_ocr_testboard_expected_behavior_matrix_v0"
BOUNDARY_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_boundary_matrix_v0"
EXECUTION_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_case_execution_matrix_v0"
SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_summary_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_audit_v0"

ROI_TYPE = "upper_sign_roi"
EXECUTED_CASE_TYPES = frozenset({"POSITIVE_TEXT_CLEAR", "EMPTY_TEXT_ROI", "MULTI_TEXT_LINES"})

DEFAULT_FINAL_STATUS: Dict[str, str] = {
    "fact_status": "not_fact",
    "write_status": "no_write",
    "executor_status": "blocked_by_gate",
}

CASE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
        "case_type": "POSITIVE_TEXT_CLEAR",
        "description": "Clear uppercase sign text; non-empty RapidOCR via bridge.",
        "execution_mode": "executed",
        "expected_pipeline": [
            "vision_roi",
            "ocr_request",
            "rapidocr_submission",
            "reference_only",
            "fusion_candidate_dryrun",
            "review_queue",
            "gate_evaluator",
            "executor_trace_stub",
        ],
        "expected_risk_codes": [],
    },
    {
        "case_id": "CM_VOCR_002_EMPTY_TEXT_ROI",
        "case_type": "EMPTY_TEXT_ROI",
        "description": "Upper sign ROI with no readable text.",
        "execution_mode": "executed",
        "expected_pipeline": ["vision_roi", "ocr_request", "rapidocr_submission", "reference_only"],
        "expected_risk_codes": ["empty_text_valid"],
    },
    {
        "case_id": "CM_VOCR_003_NON_TEXT_ROI_REJECTED",
        "case_type": "NON_TEXT_ROI_REJECTED",
        "description": "Non-text ROI types should not generate OCRRequest.",
        "execution_mode": "planned_only",
        "expected_pipeline": ["vision_roi", "rejection_matrix"],
        "expected_risk_codes": [],
    },
    {
        "case_id": "CM_VOCR_004_LOW_QUALITY_TEXT",
        "case_type": "LOW_QUALITY_TEXT",
        "description": "Blurry or low-res text; quality_risk required.",
        "execution_mode": "planned_only",
        "expected_pipeline": ["vision_roi", "ocr_request", "rapidocr_submission"],
        "expected_risk_codes": ["quality_risk"],
    },
    {
        "case_id": "CM_VOCR_005_PARTIAL_TEXT",
        "case_type": "PARTIAL_TEXT",
        "description": "Partially cropped text fragments.",
        "execution_mode": "planned_only",
        "expected_pipeline": ["vision_roi", "ocr_request", "rapidocr_submission", "reference_only"],
        "expected_risk_codes": ["partial_text_risk"],
    },
    {
        "case_id": "CM_VOCR_006_MULTI_TEXT_LINES",
        "case_type": "MULTI_TEXT_LINES",
        "description": "Multiple text lines in upper_sign_roi.",
        "execution_mode": "executed",
        "expected_pipeline": ["vision_roi", "ocr_request", "rapidocr_submission", "reference_only"],
        "expected_risk_codes": [],
    },
    {
        "case_id": "CM_VOCR_007_MIXED_CN_EN",
        "case_type": "MIXED_CN_EN",
        "description": "Mixed Chinese and English; no translation.",
        "execution_mode": "planned_only",
        "expected_pipeline": ["vision_roi", "ocr_request", "rapidocr_submission"],
        "expected_risk_codes": [],
    },
    {
        "case_id": "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
        "case_type": "FALSE_POSITIVE_VISUAL_ROI",
        "description": "Sign-like visuals without text.",
        "execution_mode": "planned_only",
        "expected_pipeline": ["vision_roi", "ocr_request", "rapidocr_submission"],
        "expected_risk_codes": [],
    },
    {
        "case_id": "CM_VOCR_009_DUPLICATE_TEXT_ROI",
        "case_type": "DUPLICATE_TEXT_ROI",
        "description": "Duplicate text across frames; source_chain distinguishable.",
        "execution_mode": "planned_only",
        "expected_pipeline": ["vision_roi", "ocr_request", "rapidocr_submission", "reference_only"],
        "expected_risk_codes": ["duplicate_candidate"],
    },
    {
        "case_id": "CM_VOCR_010_CONFLICTING_TEXT_ROI",
        "case_type": "CONFLICTING_TEXT_ROI",
        "description": "Conflicting ROI texts; candidate only.",
        "execution_mode": "planned_only",
        "expected_pipeline": ["vision_roi", "ocr_request", "rapidocr_submission", "reference_only"],
        "expected_risk_codes": ["conflicting_text_candidate"],
    },
)


def _env_true(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).strip().lower() in ("1", "true", "yes", "on")


def apply_rapidocr_eval_env() -> None:
    os.environ["LUNA_ENABLE_OCR_MAINLINE_BRIDGE_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_REAL_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_RAPIDOCR_RUNTIME_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_OCR_STUB_PROVIDER_V0"] = "true"
    os.environ["LUNA_ENABLE_PADDLEOCR_RUNTIME_PROVIDER_V0"] = "false"
    os.environ["LUNA_OCR_SUBMISSION_EVAL_ONLY"] = "true"
    os.environ.setdefault("LUNA_OCR_LIGHTWEIGHT_MAX_EDGE_PX", "512")


def _load_font(size: int = 36) -> Any:
    from PIL import ImageFont

    for fp in (
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(fp, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _upper_sign_bbox(frame_w: int, frame_h: int) -> Tuple[int, int, int, int]:
    return int(frame_w * 0.2), 0, int(frame_w * 0.8), int(frame_h * 0.25)


def create_fixture_image_v0(
    work_dir: Path,
    *,
    case_id: str,
    lines: Optional[List[str]] = None,
    frame_w: int = 640,
    frame_h: int = 480,
    blur: bool = False,
) -> Dict[str, Any]:
    from PIL import Image, ImageDraw, ImageFilter

    work_dir.mkdir(parents=True, exist_ok=True)
    x1, y1, x2, y2 = _upper_sign_bbox(frame_w, frame_h)
    frame_path = (work_dir / f"{case_id}_frame.png").resolve()
    crop_path = (work_dir / f"{case_id}_crop.png").resolve()

    img = Image.new("RGB", (frame_w, frame_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _load_font(32 if blur else 36)
    line_list = list(lines or [])
    tx, ty = x1 + 16, y1 + 12
    gap = 40
    for line in line_list:
        draw.text((tx, ty), line, fill=(0, 0, 0), font=font)
        ty += gap

    if blur:
        img = img.filter(ImageFilter.GaussianBlur(radius=2))

    img.save(frame_path, format="PNG")
    crop = img.crop((x1, y1, x2, y2))
    crop.save(crop_path, format="PNG")
    cw, ch = crop.size

    return {
        "image_ref": str(frame_path),
        "crop_image_ref": str(crop_path),
        "roi_bbox_in_crop": [0, 0, cw, ch],
        "bbox_in_frame": [x1, y1, x2, y2],
        "expected_text_hint": line_list,
        "width": frame_w,
        "height": frame_h,
    }


def run_rapidocr_on_crop_v0(
    *,
    crop_image_ref: str,
    roi_bbox_in_crop: List[int],
    workspace_root: Path,
    governance_config_path: Path,
    work_dir: Path,
) -> Dict[str, Any]:
    x1, y1, x2, y2 = roi_bbox_in_crop
    req = OCRRequestV0(
        input_type="roi",
        image_path=crop_image_ref,
        roi_refs=[f"ocr_roi_xyxy:{x1},{y1},{x2},{y2}"],
        task_context="cross_modal_testboard_expansion",
        allow_full_image=False,
        expected_output="ocr_evidence",
    )
    bridge_result = run_ocr_mainline_bridge_v0(
        req,
        governance_config_path=governance_config_path,
        workspace_root=workspace_root,
        normalization_work_dir=work_dir / "norm",
    )
    fields = _bridge_row_fields(bridge_result if isinstance(bridge_result, dict) else {})
    text_joined = str(fields.get("evidence_text_joined") or "")
    return {
        "ocr_bridge_status": bridge_result.get("status") if isinstance(bridge_result, dict) else "",
        "text_joined": text_joined,
        "empty_text": not text_joined.strip(),
        "text_item_count": int(fields.get("text_item_count") or 0),
        "rapidocr_invoked": bool(fields.get("rapidocr_invoked")),
        "real_provider_invoked": bool(fields.get("real_provider_invoked")),
    }


def expected_behavior_for_case(spec: Dict[str, Any]) -> Dict[str, Any]:
    ct = spec["case_type"]
    row: Dict[str, Any] = {
        "case_id": spec["case_id"],
        "case_type": ct,
        "should_generate_ocr_request": ct != "NON_TEXT_ROI_REJECTED",
        "should_invoke_rapidocr": ct not in ("NON_TEXT_ROI_REJECTED",),
        "expected_text_non_empty": ct in ("POSITIVE_TEXT_CLEAR", "MULTI_TEXT_LINES", "MIXED_CN_EN"),
        "should_generate_reference": ct not in ("NON_TEXT_ROI_REJECTED",),
        "should_generate_fusion_candidate": ct
        in (
            "POSITIVE_TEXT_CLEAR",
            "EMPTY_TEXT_ROI",
            "MULTI_TEXT_LINES",
            "MIXED_CN_EN",
            "PARTIAL_TEXT",
            "CONFLICTING_TEXT_ROI",
        ),
        "should_enter_review_queue": ct == "POSITIVE_TEXT_CLEAR",
        "expected_gate_decision": "hold_for_review" if ct == "POSITIVE_TEXT_CLEAR" else "not_evaluated_or_hold",
        "expected_executor_status": "blocked_by_gate" if ct == "POSITIVE_TEXT_CLEAR" else "not_applicable_or_blocked",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
    }
    if ct == "NON_TEXT_ROI_REJECTED":
        row["should_generate_ocr_request"] = False
        row["should_invoke_rapidocr"] = False
    if ct == "EMPTY_TEXT_ROI":
        row["expected_text_non_empty"] = False
    if ct in ("LOW_QUALITY_TEXT", "PARTIAL_TEXT", "FALSE_POSITIVE_VISUAL_ROI"):
        row["expected_text_non_empty"] = False
    return row


def boundary_row_for_case(case_id: str) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "ai_interpretation_committed": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def execute_case_v0(
    spec: Dict[str, Any],
    *,
    fixture_work_dir: Path,
    workspace_root: Path,
    governance_config_path: Path,
    text_bearing_root: Optional[Path],
) -> Dict[str, Any]:
    case_id = spec["case_id"]
    case_type = spec["case_type"]
    base = {
        "case_id": case_id,
        "case_type": case_type,
        "execution_mode": spec.get("execution_mode"),
        "case_execution_status": "planned_only",
        "observed_text_joined": None,
        "observed_empty_text": None,
        "observed_item_count": None,
        "observed_boundary_ok": True,
        "observed_notes": [],
    }

    if spec.get("execution_mode") != "executed":
        base["observed_notes"] = ["planned_only: fixture execution deferred"]
        return base

    work = fixture_work_dir / case_id
    fixture: Dict[str, Any] = {}

    if case_type == "POSITIVE_TEXT_CLEAR" and text_bearing_root:
        tb_crop = text_bearing_root / "_sample_work" / "text_bearing_upper_sign_roi_crop.png"
        if tb_crop.is_file():
            fixture = {
                "crop_image_ref": str(tb_crop.resolve()),
                "roi_bbox_in_crop": [0, 0, 384, 120],
                "expected_text_hint": ["LUNA TEXT 123", "中文测试"],
                "source": "reuse_text_bearing_sample",
            }
        else:
            fixture = create_fixture_image_v0(
                work, case_id=case_id, lines=["LUNA TEXT 123", "中文测试"]
            )
    elif case_type == "EMPTY_TEXT_ROI":
        fixture = create_fixture_image_v0(work, case_id=case_id, lines=[])
    elif case_type == "MULTI_TEXT_LINES":
        fixture = create_fixture_image_v0(
            work,
            case_id=case_id,
            lines=["LINE ONE", "LINE TWO", "第三行"],
        )
    else:
        base["observed_notes"] = ["unsupported executed case type"]
        return base

    if not fixture.get("crop_image_ref"):
        base["case_execution_status"] = "failed"
        base["observed_notes"].append("fixture_missing")
        return base

    apply_rapidocr_eval_env()
    ocr_obs = run_rapidocr_on_crop_v0(
        crop_image_ref=str(fixture["crop_image_ref"]),
        roi_bbox_in_crop=list(fixture.get("roi_bbox_in_crop") or [0, 0, 384, 120]),
        workspace_root=workspace_root,
        governance_config_path=governance_config_path,
        work_dir=work / "ocr_work",
    )

    base["case_execution_status"] = "executed"
    base["fixture_ref"] = fixture.get("crop_image_ref")
    base["observed_text_joined"] = ocr_obs.get("text_joined")
    base["observed_empty_text"] = ocr_obs.get("empty_text")
    base["observed_item_count"] = ocr_obs.get("text_item_count")
    base["rapidocr_invoked"] = ocr_obs.get("rapidocr_invoked")

    exp = expected_behavior_for_case(spec)
    notes: List[str] = []
    if case_type == "POSITIVE_TEXT_CLEAR":
        if ocr_obs.get("empty_text"):
            notes.append("unexpected_empty_text_for_positive")
        if not ocr_obs.get("rapidocr_invoked"):
            notes.append("rapidocr_not_invoked")
    elif case_type == "EMPTY_TEXT_ROI":
        if not ocr_obs.get("empty_text") and ocr_obs.get("rapidocr_invoked"):
            notes.append("unexpected_non_empty_for_empty_roi")
    elif case_type == "MULTI_TEXT_LINES":
        if ocr_obs.get("empty_text"):
            notes.append("unexpected_empty_text_for_multi_line")
        if int(ocr_obs.get("text_item_count") or 0) < 2:
            notes.append("text_item_count_below_2")
    if exp.get("expected_text_non_empty") and ocr_obs.get("empty_text"):
        notes.append("expected_non_empty_mismatch")
    base["observed_notes"] = notes
    base["observed_boundary_ok"] = len(notes) == 0
    return base


def build_registry_v0(testboard_id: str) -> Dict[str, Any]:
    cases = []
    for spec in CASE_SPECS:
        cases.append(
            {
                "case_id": spec["case_id"],
                "case_type": spec["case_type"],
                "description": spec["description"],
                "fixture_ref": f"fixtures/{spec['case_id']}",
                "execution_mode": spec.get("execution_mode"),
                "expected_pipeline": list(spec.get("expected_pipeline") or []),
                "expected_final_status": dict(DEFAULT_FINAL_STATUS),
                "expected_risk_codes": list(spec.get("expected_risk_codes") or []),
            }
        )
    return {
        "schema_version": REGISTRY_SCHEMA,
        "testboard_id": testboard_id,
        "scope": "evaluation_only",
        "case_count": len(cases),
        "cases": cases,
    }


def build_fixture_manifest_v0(
    registry: Dict[str, Any],
    execution_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []
    exec_by_id = {r["case_id"]: r for r in execution_rows if isinstance(r, dict)}
    for c in registry.get("cases") or []:
        if not isinstance(c, dict):
            continue
        cid = c.get("case_id")
        ex = exec_by_id.get(cid) or {}
        ct = c.get("case_type")
        lines = []
        if ct == "POSITIVE_TEXT_CLEAR":
            lines = ["LUNA TEXT 123", "中文测试"]
        elif ct == "MULTI_TEXT_LINES":
            lines = ["LINE ONE", "LINE TWO", "第三行"]
        entries.append(
            {
                "case_id": cid,
                "image_ref": ex.get("fixture_ref") or f"planned_fixtures/{cid}_frame.png",
                "roi_bbox": [128, 0, 512, 120],
                "expected_text_hint": lines,
                "quality_variant": "low_quality" if ct == "LOW_QUALITY_TEXT" else "normal",
                "language_variant": "mixed_cn_en" if ct == "MIXED_CN_EN" else "default",
                "expected_ocr_behavior": (
                    "non_empty" if c.get("case_type") in ("POSITIVE_TEXT_CLEAR", "MULTI_TEXT_LINES") else "empty_or_conditional"
                ),
                "expected_risk_codes": list(c.get("expected_risk_codes") or []),
                "fixture_status": ex.get("case_execution_status", "planned_only"),
            }
        )
    return {
        "schema_version": FIXTURE_MANIFEST_SCHEMA,
        "entry_count": len(entries),
        "entries": entries,
    }


def build_testboard_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_vision_ocr_testboard_expansion_executed": True,
        "evaluation_only": True,
        "testboard_registry_generated": True,
        "fixture_manifest_generated": True,
        "expected_behavior_matrix_generated": True,
        "real_scene_delta_executor_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "ai_interpretation_committed": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "database_write_invoked": False,
        "wal_append_invoked": False,
    }


def run_cross_modal_vision_ocr_testboard_expansion_v0(
    *,
    output_work_root: Path,
    workspace_root: Path,
    governance_config_path: Path,
    chain_closure_root: Optional[str] = None,
    text_bearing_sample_root: Optional[str] = None,
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
    testboard_id = f"tb_{uuid.uuid4().hex[:12]}"
    fixture_work = output_work_root / "_fixtures"

    tb_root = Path(text_bearing_sample_root).resolve() if text_bearing_sample_root else None

    execution_rows: List[Dict[str, Any]] = []
    for spec in CASE_SPECS:
        row = execute_case_v0(
            spec,
            fixture_work_dir=fixture_work,
            workspace_root=workspace_root,
            governance_config_path=governance_config_path,
            text_bearing_root=tb_root,
        )
        execution_rows.append(row)

    registry = build_registry_v0(testboard_id)
    fixture_manifest = build_fixture_manifest_v0(registry, execution_rows)
    expected_rows = [expected_behavior_for_case(s) for s in CASE_SPECS]
    expected_doc = {
        "schema_version": EXPECTED_BEHAVIOR_SCHEMA,
        "row_count": len(expected_rows),
        "rows": expected_rows,
    }
    boundary_rows = [boundary_row_for_case(s["case_id"]) for s in CASE_SPECS]
    boundary_doc = {
        "schema_version": BOUNDARY_MATRIX_SCHEMA,
        "boundary_all_ok": all(r.get("midplatform_fact_written") is False for r in boundary_rows),
        "rows": boundary_rows,
    }
    execution_doc = {
        "schema_version": EXECUTION_MATRIX_SCHEMA,
        "row_count": len(execution_rows),
        "rows": execution_rows,
    }

    executed_count = sum(1 for r in execution_rows if r.get("case_execution_status") == "executed")
    planned_count = sum(1 for r in execution_rows if r.get("case_execution_status") == "planned_only")

    if executed_count < 3:
        errs.append(f"executed_case_count_below_3:{executed_count}")

    phase_verdict = "GO"
    if executed_count < 3:
        phase_verdict = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Expansion-001",
        "testboard_id": testboard_id,
        "case_count": len(CASE_SPECS),
        "executed_case_count": executed_count,
        "planned_case_count": planned_count,
        "boundary_all_ok": boundary_doc.get("boundary_all_ok"),
        "write_path_invoked": False,
        "chain_closure_root": str(Path(chain_closure_root).resolve()) if chain_closure_root else None,
        "text_bearing_sample_root": str(tb_root) if tb_root else None,
        "recommended_next": "expand_case_execution_or_add_performance_metrics",
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }
    audit = build_testboard_audit_v0()

    return summary, registry, fixture_manifest, expected_doc, boundary_doc, execution_doc, audit, errs
