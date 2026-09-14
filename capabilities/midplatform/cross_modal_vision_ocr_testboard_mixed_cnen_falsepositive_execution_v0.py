# -*- coding: utf-8 -*-
"""TestBoard MIXED_CN_EN / FALSE_POSITIVE_VISUAL_ROI execution (evaluation-only).

Phase-CrossModal-Vision-OCR-TestBoard-MixedCNEN-FalsePositive-Execution-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.cross_modal_vision_ocr_fusion_candidate_dryrun_v0 import (
    build_fusion_candidate_from_reference_v0,
)
from capabilities.midplatform.cross_modal_vision_ocr_testboard_expansion_v0 import (
    CASE_SPECS,
    _load_font,
    _upper_sign_bbox,
    apply_rapidocr_eval_env,
    run_rapidocr_on_crop_v0,
)
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_summary_v0"
FIXTURE_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_fixture_report_v0"
EXECUTION_MATRIX_SCHEMA = (
    "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_case_execution_matrix_v0"
)
PLANNED_MATRIX_SCHEMA = (
    "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_planned_only_matrix_v0"
)
EXPECTED_VS_OBSERVED_SCHEMA = (
    "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_expected_vs_observed_report_v0"
)
RISK_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_risk_report_v0"
BOUNDARY_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_boundary_matrix_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_audit_v0"

NEW_EXECUTED_CASE_IDS = frozenset(
    {
        "CM_VOCR_007_MIXED_CN_EN",
        "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
    }
)

PRIOR_EXECUTED_CASE_IDS = (
    "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
    "CM_VOCR_002_EMPTY_TEXT_ROI",
    "CM_VOCR_004_LOW_QUALITY_TEXT",
    "CM_VOCR_005_PARTIAL_TEXT",
    "CM_VOCR_006_MULTI_TEXT_LINES",
)

PLANNED_ONLY_CASE_IDS = (
    "CM_VOCR_003_NON_TEXT_ROI_REJECTED",
    "CM_VOCR_009_DUPLICATE_TEXT_ROI",
    "CM_VOCR_010_CONFLICTING_TEXT_ROI",
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _case_spec(case_id: str) -> Dict[str, Any]:
    for s in CASE_SPECS:
        if s["case_id"] == case_id:
            return s
    return {"case_id": case_id}


def create_mixed_cn_en_fixture_v0(work_dir: Path, *, case_id: str) -> Dict[str, Any]:
    from PIL import Image, ImageDraw

    work_dir.mkdir(parents=True, exist_ok=True)
    frame_w, frame_h = 640, 480
    x1, y1, x2, y2 = _upper_sign_bbox(frame_w, frame_h)
    frame_path = (work_dir / f"{case_id}_frame.png").resolve()
    crop_path = (work_dir / f"{case_id}_crop.png").resolve()

    lines = ["SALE 50% OFF", "中文优惠", "LUNA A1 测试"]
    img = Image.new("RGB", (frame_w, frame_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _load_font(30)
    tx, ty = x1 + 14, y1 + 10
    for line in lines:
        draw.text((tx, ty), line, fill=(0, 0, 0), font=font)
        ty += 36

    img.save(frame_path, format="PNG")
    crop = img.crop((x1, y1, x2, y2))
    crop.save(crop_path, format="PNG")
    cw, ch = crop.size

    return {
        "case_id": case_id,
        "case_type": "MIXED_CN_EN",
        "image_ref": str(frame_path),
        "roi_crop_ref": str(crop_path),
        "fixture_generation_method": "mixed_cn_en_upper_sign_roi_text",
        "expected_text_hint": lines,
        "language_variant": "mixed_cn_en",
        "visual_variant": "normal",
        "risk_variant": "mixed_language_text",
        "network_request_invoked": False,
        "roi_bbox_in_crop": [0, 0, cw, ch],
    }


def create_false_positive_visual_roi_fixture_v0(work_dir: Path, *, case_id: str) -> Dict[str, Any]:
    from PIL import Image, ImageDraw

    work_dir.mkdir(parents=True, exist_ok=True)
    frame_w, frame_h = 640, 480
    x1, y1, x2, y2 = _upper_sign_bbox(frame_w, frame_h)
    frame_path = (work_dir / f"{case_id}_frame.png").resolve()
    crop_path = (work_dir / f"{case_id}_crop.png").resolve()

    img = Image.new("RGB", (frame_w, frame_h), (240, 240, 240))
    draw = ImageDraw.Draw(img)
    sign_x1, sign_y1 = x1 + 20, y1 + 8
    sign_x2, sign_y2 = x2 - 20, y2 - 8
    draw.rectangle([sign_x1, sign_y1, sign_x2, sign_y2], fill=(255, 200, 60), outline=(180, 120, 0), width=4)
    draw.line([(sign_x1 + 12, sign_y1 + 12), (sign_x2 - 12, sign_y2 - 12)], fill=(200, 80, 0), width=3)
    draw.ellipse(
        [(sign_x1 + sign_x2) // 2 - 18, (sign_y1 + sign_y2) // 2 - 18,
         (sign_x1 + sign_x2) // 2 + 18, (sign_y1 + sign_y2) // 2 + 18],
        outline=(120, 60, 0),
        width=2,
    )

    img.save(frame_path, format="PNG")
    crop = img.crop((x1, y1, x2, y2))
    crop.save(crop_path, format="PNG")
    cw, ch = crop.size

    return {
        "case_id": case_id,
        "case_type": "FALSE_POSITIVE_VISUAL_ROI",
        "image_ref": str(frame_path),
        "roi_crop_ref": str(crop_path),
        "fixture_generation_method": "sign_like_non_text_decorative_roi",
        "expected_text_hint": [],
        "language_variant": "none",
        "visual_variant": "sign_like_non_text",
        "risk_variant": "false_positive_visual_roi",
        "network_request_invoked": False,
        "roi_bbox_in_crop": [0, 0, cw, ch],
    }


def _build_reference(
    *,
    frame_id: str,
    text_joined: str,
    empty_text: bool,
    rapidocr_invoked: bool,
    case_run_id: str,
) -> Dict[str, Any]:
    return {
        "schema_version": "cross_modal_vision_ocr_reference_candidate_v0",
        "reference_id": f"xref_{uuid.uuid4().hex[:16]}",
        "reference_scope": "reference_only",
        "source": "testboard_mixed_cnen_falsepositive_execution",
        "frame_id": frame_id,
        "roi_type": "upper_sign_roi",
        "ocr_refs": {
            "ocr_text_joined": text_joined,
            "empty_text": empty_text,
            "rapidocr_invoked": rapidocr_invoked,
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

    OCRRequestV0(
        input_type="roi",
        image_path=crop_ref,
        roi_refs=[
            f"ocr_roi_xyxy:{roi_bbox[0]},{roi_bbox[1]},{roi_bbox[2]},{roi_bbox[3]}"
        ],
        task_context="testboard_mixed_cnen_falsepositive",
        allow_full_image=False,
        expected_output="ocr_evidence",
    )

    frame_id = f"testboard_{case_id[-8:].lower()}"
    text_joined = str(ocr_obs.get("text_joined") or "")
    reference = _build_reference(
        frame_id=frame_id,
        text_joined=text_joined,
        empty_text=bool(ocr_obs.get("empty_text")),
        rapidocr_invoked=bool(ocr_obs.get("rapidocr_invoked")),
        case_run_id=case_run_id,
    )
    fusion_cand = build_fusion_candidate_from_reference_v0(reference)
    fusion_cand["candidate_id"] = f"fusion_cand_{case_run_id}"
    fusion_cand["fact_status"] = "not_fact"

    row: Dict[str, Any] = {
        "case_id": case_id,
        "case_type": case_type,
        "case_run_id": case_run_id,
        "fixture_ref": crop_ref,
        "observed_text_joined": text_joined,
        "observed_empty_text": ocr_obs.get("empty_text"),
        "observed_item_count": ocr_obs.get("text_item_count"),
        "ocr_request_generated": True,
        "rapidocr_invoked": bool(ocr_obs.get("rapidocr_invoked")),
        "reference_generated": True,
        "fusion_candidate_generated": fusion_cand is not None,
        "review_queue_status": "skipped_mixed_or_false_positive_risk",
        "gate_decision": "hold_for_review",
        "executor_status": "blocked_by_gate",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "boundary_ok": True,
        "translation_performed": False,
        "semantic_interpretation_performed": False,
        "confirmed_sign": False,
    }

    if case_type == "MIXED_CN_EN":
        row["risk_codes"] = [
            "mixed_language_text_risk",
            "no_translation",
            "no_semantic_interpretation",
            "commercial_text_not_fact",
        ]
        row["no_translation"] = True
        row["no_semantic_interpretation"] = True
    elif case_type == "FALSE_POSITIVE_VISUAL_ROI":
        row["risk_codes"] = [
            "false_positive_visual_roi_risk",
            "visual_region_not_text",
            "no_confirmed_sign",
            "ocr_empty_or_invalid_not_failure",
        ]
        row["visual_region_not_text"] = True
        row["no_confirmed_sign"] = True
        row["confirmed_sign"] = False
    else:
        row["risk_codes"] = []

    return row


def normalize_prior_row(row: Dict[str, Any]) -> Dict[str, Any]:
    out = {
        "case_id": row.get("case_id"),
        "case_type": row.get("case_type"),
        "case_run_id": row.get("case_run_id"),
        "fixture_ref": row.get("fixture_ref"),
        "observed_text_joined": row.get("observed_text_joined"),
        "observed_empty_text": row.get("observed_empty_text")
        if "observed_empty_text" in row
        else row.get("empty_text"),
        "observed_item_count": row.get("observed_item_count")
        if "observed_item_count" in row
        else row.get("text_item_count"),
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
    if row.get("no_forced_interpretation"):
        out["no_forced_interpretation"] = True
    if row.get("no_forced_completion"):
        out["no_forced_completion"] = True
    return out


def load_prior_executed_rows(lp_root: Path) -> List[Dict[str, Any]]:
    path = lp_root / "cross_modal_vision_ocr_testboard_lowquality_partial_case_execution_matrix.json"
    if not path.is_file():
        return []
    rows = _read_json(path).get("rows") or []
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
    row: Dict[str, Any] = {
        "case_id": exec_row.get("case_id"),
        "case_type": ct,
        "case_run_id": exec_row.get("case_run_id"),
        "observed_final_fact_status": exec_row.get("final_fact_status"),
        "observed_final_write_status": exec_row.get("final_write_status"),
        "observed_executor_status": exec_row.get("executor_status"),
    }
    if ct == "MIXED_CN_EN":
        row["observed_text_may_include_cn_en"] = True
        row["translation_performed"] = False
        row["semantic_interpretation_performed"] = False
    elif ct == "FALSE_POSITIVE_VISUAL_ROI":
        row["confirmed_sign"] = False
        row["observed_empty_or_invalid_text_allowed"] = True
    return row


def build_risk_report_v0(exec_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    all_codes = sorted({c for r in exec_rows for c in (r.get("risk_codes") or [])})
    mixed = next((r for r in exec_rows if r.get("case_type") == "MIXED_CN_EN"), None)
    fp = next((r for r in exec_rows if r.get("case_type") == "FALSE_POSITIVE_VISUAL_ROI"), None)
    return {
        "schema_version": RISK_REPORT_SCHEMA,
        "risk_codes_all_executed": all_codes,
        "mixed_language_text_risk_present": mixed is not None
        and "mixed_language_text_risk" in (mixed.get("risk_codes") or []),
        "false_positive_visual_roi_risk_present": fp is not None
        and "false_positive_visual_roi_risk" in (fp.get("risk_codes") or []),
        "no_translation_present": "no_translation" in all_codes,
        "no_semantic_interpretation_present": "no_semantic_interpretation" in all_codes,
        "commercial_text_not_fact_present": "commercial_text_not_fact" in all_codes,
        "visual_region_not_text_present": "visual_region_not_text" in all_codes,
        "no_confirmed_sign_present": "no_confirmed_sign" in all_codes,
        "ocr_empty_or_invalid_not_failure_present": "ocr_empty_or_invalid_not_failure" in all_codes,
        "translation_performed_any": any(r.get("translation_performed") for r in exec_rows),
        "semantic_interpretation_performed_any": any(
            r.get("semantic_interpretation_performed") for r in exec_rows
        ),
        "confirmed_sign_any": any(r.get("confirmed_sign") for r in exec_rows),
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
        "cross_modal_testboard_mixed_cnen_falsepositive_execution_executed": True,
        "evaluation_only": True,
        "executed_case_count": executed,
        "planned_only_case_count": planned,
        "mixed_cn_en_case_executed": True,
        "false_positive_visual_roi_case_executed": True,
        "translation_performed": False,
        "semantic_interpretation_performed": False,
        "confirmed_sign_generated": False,
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


def run_cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_execution_v0(
    *,
    testboard_expansion_root: str,
    full_chain_5cases_root: str,
    lowquality_partial_root: str,
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
    fc5 = Path(full_chain_5cases_root).resolve()
    lp = Path(lowquality_partial_root).resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    prior_rows = load_prior_executed_rows(lp)
    if len(prior_rows) < 5:
        errs.append(f"prior_executed_rows:{len(prior_rows)}")

    fixture_reports: List[Dict[str, Any]] = []
    new_rows: List[Dict[str, Any]] = []

    mixed_fixture = create_mixed_cn_en_fixture_v0(
        work_root / "_fixtures" / "CM_VOCR_007_MIXED_CN_EN",
        case_id="CM_VOCR_007_MIXED_CN_EN",
    )
    fixture_reports.append(mixed_fixture)
    new_rows.append(
        execute_new_case_v0(
            case_id="CM_VOCR_007_MIXED_CN_EN",
            case_type="MIXED_CN_EN",
            fixture=mixed_fixture,
            workspace_root=workspace_root,
            governance_config_path=governance_config_path,
            work_dir=work_root / "_case_work" / "CM_VOCR_007_MIXED_CN_EN",
        )
    )

    fp_fixture = create_false_positive_visual_roi_fixture_v0(
        work_root / "_fixtures" / "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
        case_id="CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
    )
    fixture_reports.append(fp_fixture)
    new_rows.append(
        execute_new_case_v0(
            case_id="CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
            case_type="FALSE_POSITIVE_VISUAL_ROI",
            fixture=fp_fixture,
            workspace_root=workspace_root,
            governance_config_path=governance_config_path,
            work_dir=work_root / "_case_work" / "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
        )
    )

    executed_rows = prior_rows + new_rows
    if len(executed_rows) != 7:
        errs.append(f"executed_row_count:{len(executed_rows)}")

    planned_rows = [
        {
            "case_id": cid,
            "case_type": _case_spec(cid).get("case_type"),
            "execution_status": "planned_only",
            "reason": "fixture_execution_deferred",
            "must_not_have_case_run_id": True,
        }
        for cid in PLANNED_ONLY_CASE_IDS
    ]

    evo_rows = [build_expected_vs_observed_row(r) for r in executed_rows]
    risk_report = build_risk_report_v0(executed_rows)
    boundary_rows = [build_boundary_row(r) for r in executed_rows]

    phase_verdict = "GO" if len(executed_rows) == 7 and len(planned_rows) == 3 and not errs else "CONDITIONAL_GO"
    if len(new_rows) < 2:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-MixedCNEN-FalsePositive-Execution-001",
        "testboard_expansion_root": str(tb),
        "full_chain_5cases_root": str(fc5),
        "lowquality_partial_root": str(lp),
        "case_count": 10,
        "executed_case_count": len(executed_rows),
        "planned_only_case_count": len(planned_rows),
        "newly_executed_case_ids": sorted(NEW_EXECUTED_CASE_IDS),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return (
        summary,
        {"schema_version": FIXTURE_REPORT_SCHEMA, "row_count": len(fixture_reports), "rows": fixture_reports},
        {
            "schema_version": EXECUTION_MATRIX_SCHEMA,
            "row_count": len(executed_rows),
            "executed_case_count": len(executed_rows),
            "rows": executed_rows,
        },
        {
            "schema_version": PLANNED_MATRIX_SCHEMA,
            "row_count": len(planned_rows),
            "planned_only_case_count": len(planned_rows),
            "rows": planned_rows,
        },
        {"schema_version": EXPECTED_VS_OBSERVED_SCHEMA, "row_count": len(evo_rows), "rows": evo_rows},
        risk_report,
        {"schema_version": BOUNDARY_MATRIX_SCHEMA, "boundary_all_ok": True, "rows": boundary_rows},
        build_audit_v0(executed=len(executed_rows), planned=len(planned_rows)),
        errs,
    )
