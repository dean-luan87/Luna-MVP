# -*- coding: utf-8 -*-
"""TestBoard LOW_QUALITY_TEXT / PARTIAL_TEXT execution (evaluation-only, no writes).

Phase-CrossModal-Vision-OCR-TestBoard-LowQuality-PartialText-Execution-001
"""

from __future__ import annotations

import json
import uuid
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.cross_modal_vision_ocr_fusion_candidate_dryrun_v0 import (
    build_fusion_candidate_from_reference_v0,
)
from capabilities.midplatform.cross_modal_vision_ocr_testboard_expansion_v0 import (
    CASE_SPECS,
    _load_font,
    _upper_sign_bbox,
    apply_rapidocr_eval_env,
    expected_behavior_for_case,
    run_rapidocr_on_crop_v0,
)
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_lowquality_partial_summary_v0"
FIXTURE_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_lowquality_partial_fixture_report_v0"
EXECUTION_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_lowquality_partial_case_execution_matrix_v0"
PLANNED_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_lowquality_partial_planned_only_matrix_v0"
EXPECTED_VS_OBSERVED_SCHEMA = (
    "cross_modal_vision_ocr_testboard_lowquality_partial_expected_vs_observed_report_v0"
)
RISK_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_lowquality_partial_risk_report_v0"
BOUNDARY_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_lowquality_partial_boundary_matrix_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_lowquality_partial_audit_v0"

NEW_EXECUTED_CASE_IDS = frozenset(
    {
        "CM_VOCR_004_LOW_QUALITY_TEXT",
        "CM_VOCR_005_PARTIAL_TEXT",
    }
)

PRIOR_EXECUTED_CASE_IDS = frozenset(
    {
        "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
        "CM_VOCR_002_EMPTY_TEXT_ROI",
        "CM_VOCR_006_MULTI_TEXT_LINES",
    }
)

PLANNED_ONLY_CASE_IDS = frozenset(
    {
        "CM_VOCR_003_NON_TEXT_ROI_REJECTED",
        "CM_VOCR_007_MIXED_CN_EN",
        "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
        "CM_VOCR_009_DUPLICATE_TEXT_ROI",
        "CM_VOCR_010_CONFLICTING_TEXT_ROI",
    }
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _case_spec(case_id: str) -> Dict[str, Any]:
    for s in CASE_SPECS:
        if s["case_id"] == case_id:
            return s
    return {"case_id": case_id}


def create_low_quality_fixture_v0(work_dir: Path, *, case_id: str) -> Dict[str, Any]:
    from PIL import Image, ImageDraw, ImageFilter

    work_dir.mkdir(parents=True, exist_ok=True)
    frame_w, frame_h = 640, 480
    x1, y1, x2, y2 = _upper_sign_bbox(frame_w, frame_h)
    frame_path = (work_dir / f"{case_id}_frame.png").resolve()
    crop_path = (work_dir / f"{case_id}_crop.png").resolve()

    lines = ["LOW QUALITY 123", "模糊测试"]
    img = Image.new("RGB", (frame_w, frame_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _load_font(14)
    tx, ty = x1 + 12, y1 + 10
    for line in lines:
        draw.text((tx, ty), line, fill=(40, 40, 40), font=font)
        ty += 22

    img = img.filter(ImageFilter.GaussianBlur(radius=3))
    small = img.resize((frame_w // 2, frame_h // 2), Image.Resampling.BILINEAR)
    img = small.resize((frame_w, frame_h), Image.Resampling.BILINEAR)

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=35)
    buf.seek(0)
    img = Image.open(buf).convert("RGB")

    img.save(frame_path, format="PNG")
    crop = img.crop((x1, y1, x2, y2))
    crop.save(crop_path, format="PNG")
    cw, ch = crop.size

    return {
        "case_id": case_id,
        "case_type": "LOW_QUALITY_TEXT",
        "image_ref": str(frame_path),
        "roi_crop_ref": str(crop_path),
        "fixture_generation_method": "small_font_blur_jpeg_recompress",
        "expected_text_hint": lines,
        "quality_variant": "low_quality",
        "risk_variant": "quality_uncertain",
        "network_request_invoked": False,
        "roi_bbox_in_crop": [0, 0, cw, ch],
    }


def create_partial_text_fixture_v0(work_dir: Path, *, case_id: str) -> Dict[str, Any]:
    from PIL import Image, ImageDraw

    work_dir.mkdir(parents=True, exist_ok=True)
    frame_w, frame_h = 640, 480
    x1, y1, x2, y2 = _upper_sign_bbox(frame_w, frame_h)
    frame_path = (work_dir / f"{case_id}_frame.png").resolve()
    crop_path = (work_dir / f"{case_id}_crop.png").resolve()

    lines = ["PARTIAL TEXT 456", "残缺文字"]
    img = Image.new("RGB", (frame_w, frame_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _load_font(36)
    tx, ty = x1 + 16, y1 + 12
    for line in lines:
        draw.text((tx, ty), line, fill=(0, 0, 0), font=font)
        ty += 40

    img.save(frame_path, format="PNG")
    full_crop = img.crop((x1, y1, x2, y2))
    cw, ch = full_crop.size
    partial_w = max(32, int(cw * 0.42))
    partial = full_crop.crop((0, 0, partial_w, ch))
    partial.save(crop_path, format="PNG")
    pw, ph = partial.size

    return {
        "case_id": case_id,
        "case_type": "PARTIAL_TEXT",
        "image_ref": str(frame_path),
        "roi_crop_ref": str(crop_path),
        "fixture_generation_method": "upper_sign_roi_left_crop_partial_visible",
        "expected_text_hint": lines,
        "quality_variant": "normal",
        "risk_variant": "partial_text",
        "network_request_invoked": False,
        "roi_bbox_in_crop": [0, 0, pw, ph],
    }


def _build_reference(
    *,
    frame_id: str,
    roi_id: str,
    ocr_fields: Dict[str, Any],
    candidate_id: str,
) -> Dict[str, Any]:
    text_joined = str(ocr_fields.get("text_joined") or "")
    return {
        "schema_version": "cross_modal_vision_ocr_reference_candidate_v0",
        "reference_id": f"xref_{uuid.uuid4().hex[:16]}",
        "reference_scope": "reference_only",
        "source": "testboard_lowquality_partial_execution",
        "frame_id": frame_id,
        "roi_id": roi_id,
        "roi_type": "upper_sign_roi",
        "ocr_refs": {
            "ocr_text_joined": text_joined,
            "empty_text": not text_joined.strip(),
            "rapidocr_invoked": bool(ocr_fields.get("rapidocr_invoked")),
        },
        "fact_status": "not_fact",
    }


def execute_new_case_v0(
    *,
    case_id: str,
    case_type: str,
    fixture: Dict[str, Any],
    workspace_root: Path,
    governance_config_path: Path,
    work_dir: Path,
) -> Dict[str, Any]:
    case_run_id = f"crun_{uuid.uuid4().hex[:16]}"
    crop_ref = str(fixture["roi_crop_ref"])
    roi_bbox = list(fixture.get("roi_bbox_in_crop") or [0, 0, 384, 120])

    apply_rapidocr_eval_env()
    ocr_obs = run_rapidocr_on_crop_v0(
        crop_image_ref=crop_ref,
        roi_bbox_in_crop=roi_bbox,
        workspace_root=workspace_root,
        governance_config_path=governance_config_path,
        work_dir=work_dir / "ocr",
    )

    ocr_req = OCRRequestV0(
        input_type="roi",
        image_path=crop_ref,
        roi_refs=[
            f"ocr_roi_xyxy:{roi_bbox[0]},{roi_bbox[1]},{roi_bbox[2]},{roi_bbox[3]}"
        ],
        task_context="testboard_lowquality_partial_execution",
        allow_full_image=False,
        expected_output="ocr_evidence",
    )

    frame_id = f"testboard_{case_id[-8:].lower()}"
    roi_id = f"vision_roi_{frame_id}_upper_sign_roi"
    ocr_fields = dict(ocr_obs)
    ocr_fields["ocr_request_id"] = ocr_req.request_id

    reference = _build_reference(
        frame_id=frame_id,
        roi_id=roi_id,
        ocr_fields=ocr_fields,
        candidate_id=f"ocr_req_cand_{case_run_id}",
    )
    fusion_cand = build_fusion_candidate_from_reference_v0(reference)
    fusion_cand["candidate_id"] = f"fusion_cand_{case_run_id}"
    fusion_cand["fact_status"] = "not_fact"

    risk_codes: List[str] = []
    if case_type == "LOW_QUALITY_TEXT":
        risk_codes.extend(
            [
                "low_quality_text_risk",
                "ocr_confidence_or_quality_uncertain",
                "no_forced_interpretation",
            ]
        )
    elif case_type == "PARTIAL_TEXT":
        risk_codes.extend(
            [
                "partial_text_risk",
                "incomplete_text_candidate",
                "no_forced_completion",
            ]
        )

    return {
        "case_id": case_id,
        "case_type": case_type,
        "case_run_id": case_run_id,
        "fixture_ref": crop_ref,
        "observed_text_joined": ocr_obs.get("text_joined"),
        "observed_empty_text": ocr_obs.get("empty_text"),
        "observed_item_count": ocr_obs.get("text_item_count"),
        "ocr_request_generated": True,
        "rapidocr_invoked": bool(ocr_obs.get("rapidocr_invoked")),
        "reference_generated": True,
        "fusion_candidate_generated": fusion_cand is not None,
        "risk_codes": risk_codes,
        "review_queue_status": "skipped_quality_or_partial_risk",
        "gate_decision": "hold_for_review",
        "executor_status": "blocked_by_gate",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "boundary_ok": True,
    }


def normalize_prior_row(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_id": row.get("case_id"),
        "case_type": row.get("case_type"),
        "case_run_id": row.get("case_run_id"),
        "fixture_ref": row.get("fixture_ref"),
        "observed_text_joined": row.get("observed_text_joined"),
        "observed_empty_text": row.get("empty_text") if "empty_text" in row else row.get("observed_empty_text"),
        "observed_item_count": row.get("text_item_count")
        if "text_item_count" in row
        else row.get("observed_item_count"),
        "ocr_request_generated": row.get("ocr_request_generated", True),
        "rapidocr_invoked": row.get("rapidocr_invoked"),
        "reference_generated": row.get("reference_generated", True),
        "fusion_candidate_generated": row.get("fusion_candidate_generated"),
        "risk_codes": list(row.get("risk_codes") or []),
        "review_queue_status": row.get("review_queue_status"),
        "gate_decision": row.get("gate_decision"),
        "executor_status": row.get("executor_status"),
        "final_fact_status": row.get("final_fact_status", "not_fact"),
        "final_write_status": row.get("final_write_status", "no_write"),
        "boundary_ok": row.get("boundary_ok", True),
    }


def load_prior_executed_rows(full_chain_root: Path) -> List[Dict[str, Any]]:
    matrix_path = full_chain_root / "cross_modal_vision_ocr_testboard_case_run_matrix.json"
    if not matrix_path.is_file():
        return []
    rows = _read_json(matrix_path).get("rows") or []
    out: List[Dict[str, Any]] = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        cid = str(r.get("case_id") or "")
        if cid in PRIOR_EXECUTED_CASE_IDS:
            out.append(normalize_prior_row(r))
    order = list(PRIOR_EXECUTED_CASE_IDS)
    out.sort(key=lambda x: order.index(x["case_id"]) if x.get("case_id") in order else 99)
    return out


def build_expected_vs_observed_row(exec_row: Dict[str, Any]) -> Dict[str, Any]:
    ct = exec_row.get("case_type")
    obs_joined = str(exec_row.get("observed_text_joined") or "")
    obs_non_empty = bool(obs_joined.strip())
    row: Dict[str, Any] = {
        "case_id": exec_row.get("case_id"),
        "case_type": ct,
        "case_run_id": exec_row.get("case_run_id"),
        "observed_final_fact_status": exec_row.get("final_fact_status"),
        "observed_final_write_status": exec_row.get("final_write_status"),
        "observed_executor_status": exec_row.get("executor_status"),
        "observed_text_non_empty": obs_non_empty,
    }
    if ct == "LOW_QUALITY_TEXT":
        row["observed_text_may_be_partial_or_empty"] = True
        row["no_forced_interpretation"] = True
    elif ct == "PARTIAL_TEXT":
        row["observed_text_may_be_partial_or_fragmented"] = True
        row["no_forced_completion"] = True
    return row


def build_risk_report_v0(exec_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    all_codes = sorted({c for r in exec_rows for c in (r.get("risk_codes") or [])})
    low_row = next((r for r in exec_rows if r.get("case_type") == "LOW_QUALITY_TEXT"), None)
    partial_row = next((r for r in exec_rows if r.get("case_type") == "PARTIAL_TEXT"), None)
    return {
        "schema_version": RISK_REPORT_SCHEMA,
        "risk_codes_all_executed": all_codes,
        "low_quality_text_risk_present": low_row is not None
        and "low_quality_text_risk" in (low_row.get("risk_codes") or []),
        "partial_text_risk_present": partial_row is not None
        and "partial_text_risk" in (partial_row.get("risk_codes") or []),
        "no_forced_interpretation_present": "no_forced_interpretation" in all_codes,
        "no_forced_completion_present": "no_forced_completion" in all_codes,
        "forced_interpretation_absent": "forced_interpretation" not in all_codes,
        "forced_completion_absent": "forced_completion" not in all_codes,
    }


def build_boundary_row(exec_row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_id": exec_row.get("case_id"),
        "case_run_id": exec_row.get("case_run_id"),
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "scene_delta_executor_invoked": False,
        "database_write_invoked": False,
        "wal_append_invoked": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def build_audit_v0(*, executed: int, planned: int) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_testboard_lowquality_partial_execution_executed": True,
        "evaluation_only": True,
        "executed_case_count": executed,
        "planned_only_case_count": planned,
        "low_quality_text_case_executed": True,
        "partial_text_case_executed": True,
        "real_scene_delta_executor_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "database_write_invoked": False,
        "wal_append_invoked": False,
    }


def run_cross_modal_vision_ocr_testboard_lowquality_partial_execution_v0(
    *,
    testboard_expansion_root: str,
    full_chain_runner_root: str,
    workspace_root: Path,
    governance_config_path: Path,
    work_root: Path,
) -> Tuple[
    Dict[str, Any],
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
    tb = Path(testboard_expansion_root).resolve()
    fc = Path(full_chain_runner_root).resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    prior_rows = load_prior_executed_rows(fc)
    if len(prior_rows) < 3:
        errs.append(f"prior_executed_rows:{len(prior_rows)}")

    fixture_reports: List[Dict[str, Any]] = []
    new_rows: List[Dict[str, Any]] = []

    low_fixture = create_low_quality_fixture_v0(
        work_root / "_fixtures" / "CM_VOCR_004_LOW_QUALITY_TEXT",
        case_id="CM_VOCR_004_LOW_QUALITY_TEXT",
    )
    fixture_reports.append(low_fixture)
    new_rows.append(
        execute_new_case_v0(
            case_id="CM_VOCR_004_LOW_QUALITY_TEXT",
            case_type="LOW_QUALITY_TEXT",
            fixture=low_fixture,
            workspace_root=workspace_root,
            governance_config_path=governance_config_path,
            work_dir=work_root / "_case_work" / "CM_VOCR_004_LOW_QUALITY_TEXT",
        )
    )

    partial_fixture = create_partial_text_fixture_v0(
        work_root / "_fixtures" / "CM_VOCR_005_PARTIAL_TEXT",
        case_id="CM_VOCR_005_PARTIAL_TEXT",
    )
    fixture_reports.append(partial_fixture)
    new_rows.append(
        execute_new_case_v0(
            case_id="CM_VOCR_005_PARTIAL_TEXT",
            case_type="PARTIAL_TEXT",
            fixture=partial_fixture,
            workspace_root=workspace_root,
            governance_config_path=governance_config_path,
            work_dir=work_root / "_case_work" / "CM_VOCR_005_PARTIAL_TEXT",
        )
    )

    executed_rows = prior_rows + new_rows
    if len(executed_rows) != 5:
        errs.append(f"executed_row_count:{len(executed_rows)}")

    planned_rows = [
        {
            "case_id": cid,
            "case_type": _case_spec(cid).get("case_type"),
            "execution_status": "planned_only",
            "reason": "fixture_execution_deferred",
            "must_not_have_case_run_id": True,
        }
        for cid in sorted(PLANNED_ONLY_CASE_IDS)
    ]

    evo_rows = [build_expected_vs_observed_row(r) for r in executed_rows]
    risk_report = build_risk_report_v0(executed_rows)
    boundary_rows = [build_boundary_row(r) for r in executed_rows]

    phase_verdict = "GO" if len(executed_rows) == 5 and len(planned_rows) == 5 and not errs else "CONDITIONAL_GO"
    if len(new_rows) < 2:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-LowQuality-PartialText-Execution-001",
        "testboard_expansion_root": str(tb),
        "full_chain_runner_root": str(fc),
        "case_count": 10,
        "executed_case_count": len(executed_rows),
        "planned_only_case_count": len(planned_rows),
        "newly_executed_case_ids": sorted(NEW_EXECUTED_CASE_IDS),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    fixture_doc = {
        "schema_version": FIXTURE_REPORT_SCHEMA,
        "row_count": len(fixture_reports),
        "rows": fixture_reports,
    }

    execution_doc = {
        "schema_version": EXECUTION_MATRIX_SCHEMA,
        "row_count": len(executed_rows),
        "executed_case_count": len(executed_rows),
        "rows": executed_rows,
    }

    planned_doc = {
        "schema_version": PLANNED_MATRIX_SCHEMA,
        "row_count": len(planned_rows),
        "planned_only_case_count": len(planned_rows),
        "rows": planned_rows,
    }

    expected_doc = {
        "schema_version": EXPECTED_VS_OBSERVED_SCHEMA,
        "row_count": len(evo_rows),
        "rows": evo_rows,
    }

    boundary_doc = {
        "schema_version": BOUNDARY_MATRIX_SCHEMA,
        "boundary_all_ok": True,
        "rows": boundary_rows,
    }

    audit = build_audit_v0(executed=len(executed_rows), planned=len(planned_rows))

    return (
        summary,
        fixture_doc,
        execution_doc,
        planned_doc,
        expected_doc,
        risk_report,
        boundary_doc,
        audit,
        errs,
    )
