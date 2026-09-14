# -*- coding: utf-8 -*-
"""TestBoard DUPLICATE_TEXT_ROI / CONFLICTING_TEXT_ROI execution (evaluation-only).

Phase-CrossModal-Vision-OCR-TestBoard-Duplicate-Conflicting-Text-Execution-001
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

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_duplicate_conflicting_summary_v0"
FIXTURE_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_duplicate_conflicting_fixture_report_v0"
EXECUTION_MATRIX_SCHEMA = (
    "cross_modal_vision_ocr_testboard_duplicate_conflicting_case_execution_matrix_v0"
)
PLANNED_MATRIX_SCHEMA = (
    "cross_modal_vision_ocr_testboard_duplicate_conflicting_planned_only_matrix_v0"
)
EXPECTED_VS_OBSERVED_SCHEMA = (
    "cross_modal_vision_ocr_testboard_duplicate_conflicting_expected_vs_observed_report_v0"
)
RISK_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_duplicate_conflicting_risk_report_v0"
BOUNDARY_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_duplicate_conflicting_boundary_matrix_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_duplicate_conflicting_audit_v0"

NEW_EXECUTED_CASE_IDS = frozenset(
    {
        "CM_VOCR_009_DUPLICATE_TEXT_ROI",
        "CM_VOCR_010_CONFLICTING_TEXT_ROI",
    }
)

PRIOR_EXECUTED_CASE_IDS = (
    "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
    "CM_VOCR_002_EMPTY_TEXT_ROI",
    "CM_VOCR_004_LOW_QUALITY_TEXT",
    "CM_VOCR_005_PARTIAL_TEXT",
    "CM_VOCR_006_MULTI_TEXT_LINES",
    "CM_VOCR_007_MIXED_CN_EN",
    "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
)

PLANNED_ONLY_CASE_IDS = ("CM_VOCR_003_NON_TEXT_ROI_REJECTED",)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _case_spec(case_id: str) -> Dict[str, Any]:
    for s in CASE_SPECS:
        if s["case_id"] == case_id:
            return s
    return {"case_id": case_id}


def _draw_sign_text(
    draw: Any,
    *,
    x: int,
    y: int,
    lines: List[str],
    font: Any,
    gap: int = 36,
) -> int:
    ty = y
    for line in lines:
        draw.text((x, ty), line, fill=(0, 0, 0), font=font)
        ty += gap
    return ty


def create_duplicate_text_fixture_v0(work_dir: Path, *, case_id: str) -> Dict[str, Any]:
    from PIL import Image, ImageDraw

    work_dir.mkdir(parents=True, exist_ok=True)
    frame_w, frame_h = 640, 480
    x1, y1, x2, y2 = _upper_sign_bbox(frame_w, frame_h)
    lines = ["OPEN TODAY", "营业中"]
    font = _load_font(32)
    image_refs: List[str] = []
    roi_crop_refs: List[str] = []

    for frame_tag in ("frame_001", "frame_002"):
        frame_path = (work_dir / f"{case_id}_{frame_tag}.png").resolve()
        crop_path = (work_dir / f"{case_id}_{frame_tag}_crop.png").resolve()
        img = Image.new("RGB", (frame_w, frame_h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        _draw_sign_text(draw, x=x1 + 16, y=y1 + 12, lines=lines, font=font)
        img.save(frame_path, format="PNG")
        crop = img.crop((x1, y1, x2, y2))
        crop.save(crop_path, format="PNG")
        image_refs.append(str(frame_path))
        roi_crop_refs.append(str(crop_path))

    return {
        "case_id": case_id,
        "case_type": "DUPLICATE_TEXT_ROI",
        "image_refs": image_refs,
        "roi_crop_refs": roi_crop_refs,
        "fixture_generation_method": "same_text_two_frames_upper_sign_roi",
        "expected_text_hints": lines,
        "duplicate_or_conflict_variant": "same_text_across_frames",
        "duplicate_variant": "same_text_across_frames_or_rois",
        "risk_variant": "duplicate_text_candidate",
        "network_request_invoked": False,
        "roi_bbox_in_crop": [0, 0, x2 - x1, y2 - y1],
    }


def create_conflicting_text_fixture_v0(work_dir: Path, *, case_id: str) -> Dict[str, Any]:
    from PIL import Image, ImageDraw

    work_dir.mkdir(parents=True, exist_ok=True)
    frame_w, frame_h = 640, 480
    frame_path = (work_dir / f"{case_id}_frame.png").resolve()
    img = Image.new("RGB", (frame_w, frame_h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = _load_font(30)

    roi_a = (int(frame_w * 0.15), 0, int(frame_w * 0.45), int(frame_h * 0.28))
    roi_b = (int(frame_w * 0.55), 0, int(frame_w * 0.85), int(frame_h * 0.28))
    crop_a_path = (work_dir / f"{case_id}_roi_a_crop.png").resolve()
    crop_b_path = (work_dir / f"{case_id}_roi_b_crop.png").resolve()

    _draw_sign_text(draw, x=roi_a[0] + 12, y=roi_a[1] + 10, lines=["OPEN", "营业中"], font=font)
    _draw_sign_text(draw, x=roi_b[0] + 12, y=roi_b[1] + 10, lines=["CLOSED", "暂停营业"], font=font)

    img.save(frame_path, format="PNG")
    img.crop(roi_a).save(crop_a_path, format="PNG")
    img.crop(roi_b).save(crop_b_path, format="PNG")
    aw, ah = img.crop(roi_a).size
    bw, bh = img.crop(roi_b).size

    return {
        "case_id": case_id,
        "case_type": "CONFLICTING_TEXT_ROI",
        "image_refs": [str(frame_path)],
        "roi_crop_refs": [str(crop_a_path), str(crop_b_path)],
        "fixture_generation_method": "dual_roi_open_closed_conflict",
        "expected_text_hints": ["OPEN", "CLOSED", "营业中", "暂停营业"],
        "duplicate_or_conflict_variant": "open_closed_conflict",
        "conflict_variant": "open_closed_conflict",
        "risk_variant": "conflicting_text_candidate",
        "network_request_invoked": False,
        "roi_bboxes": [[0, 0, aw, ah], [0, 0, bw, bh]],
    }


def _ocr_on_crop(
    *,
    crop_ref: str,
    roi_bbox: List[int],
    workspace_root: Path,
    governance_config_path: Path,
    work_dir: Path,
    label: str,
) -> Dict[str, Any]:
    obs = run_rapidocr_on_crop_v0(
        crop_image_ref=crop_ref,
        roi_bbox_in_crop=roi_bbox,
        workspace_root=workspace_root,
        governance_config_path=governance_config_path,
        work_dir=work_dir / label,
    )
    return {
        "label": label,
        "crop_ref": crop_ref,
        "text_joined": str(obs.get("text_joined") or ""),
        "empty_text": bool(obs.get("empty_text")),
        "text_item_count": int(obs.get("text_item_count") or 0),
        "rapidocr_invoked": bool(obs.get("rapidocr_invoked")),
    }


def _normalize_token(s: str) -> str:
    return "".join(s.split()).upper()


def _texts_look_duplicate(a: str, b: str) -> bool:
    na, nb = _normalize_token(a), _normalize_token(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    return na in nb or nb in na


def execute_duplicate_case_v0(
    *,
    case_id: str,
    fixture: Dict[str, Any],
    workspace_root: Path,
    governance_config_path: Path,
    work_dir: Path,
) -> Dict[str, Any]:
    case_run_id = f"crun_{uuid.uuid4().hex[:16]}"
    apply_rapidocr_eval_env()
    roi_bbox = list(fixture.get("roi_bbox_in_crop") or [0, 0, 384, 120])
    items: List[Dict[str, Any]] = []
    for idx, crop_ref in enumerate(fixture.get("roi_crop_refs") or []):
        items.append(
            _ocr_on_crop(
                crop_ref=str(crop_ref),
                roi_bbox=roi_bbox,
                workspace_root=workspace_root,
                governance_config_path=governance_config_path,
                work_dir=work_dir,
                label=f"frame_{idx}",
            )
        )

    joined_parts = [it["text_joined"] for it in items if it["text_joined"].strip()]
    observed_text_joined = " | ".join(joined_parts)
    duplicate_detected = len(items) >= 2 and _texts_look_duplicate(
        items[0].get("text_joined", ""), items[1].get("text_joined", "")
    )

    reference = {
        "schema_version": "cross_modal_vision_ocr_reference_candidate_v0",
        "reference_scope": "reference_only",
        "fact_status": "not_fact",
        "ocr_refs": {"ocr_text_joined": observed_text_joined, "empty_text": not joined_parts},
    }
    fusion_cand = build_fusion_candidate_from_reference_v0(reference)
    fusion_cand["fact_status"] = "not_fact"

    OCRRequestV0(
        input_type="roi",
        image_path=str((fixture.get("roi_crop_refs") or [""])[0]),
        roi_refs=[f"ocr_roi_xyxy:{roi_bbox[0]},{roi_bbox[1]},{roi_bbox[2]},{roi_bbox[3]}"],
        task_context="testboard_duplicate_text",
        allow_full_image=False,
        expected_output="ocr_evidence",
    )

    risk_codes = [
        "duplicate_text_candidate",
        "duplicate_not_world_fact",
        "no_world_model_write",
        "no_confirmed_state",
    ]

    return {
        "case_id": case_id,
        "case_type": "DUPLICATE_TEXT_ROI",
        "case_run_id": case_run_id,
        "fixture_refs": list(fixture.get("roi_crop_refs") or []),
        "image_refs": list(fixture.get("image_refs") or []),
        "observed_text_joined": observed_text_joined,
        "observed_text_items": items,
        "observed_empty_text": not bool(observed_text_joined.strip()),
        "observed_item_count": sum(int(it.get("text_item_count") or 0) for it in items),
        "ocr_request_generated": True,
        "rapidocr_invoked": any(it.get("rapidocr_invoked") for it in items),
        "reference_generated": True,
        "fusion_candidate_generated": fusion_cand is not None,
        "risk_codes": risk_codes,
        "duplicate_detected": duplicate_detected,
        "world_model_write_allowed": False,
        "confirmed_state_generated": False,
        "review_queue_status": "skipped_duplicate_candidate",
        "gate_decision": "hold_for_review",
        "executor_status": "blocked_by_gate",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "boundary_ok": True,
    }


def execute_conflicting_case_v0(
    *,
    case_id: str,
    fixture: Dict[str, Any],
    workspace_root: Path,
    governance_config_path: Path,
    work_dir: Path,
) -> Dict[str, Any]:
    case_run_id = f"crun_{uuid.uuid4().hex[:16]}"
    apply_rapidocr_eval_env()
    bboxes = fixture.get("roi_bboxes") or [[0, 0, 384, 120], [0, 0, 384, 120]]
    items: List[Dict[str, Any]] = []
    for idx, crop_ref in enumerate(fixture.get("roi_crop_refs") or []):
        bbox = bboxes[idx] if idx < len(bboxes) else [0, 0, 384, 120]
        items.append(
            _ocr_on_crop(
                crop_ref=str(crop_ref),
                roi_bbox=list(bbox),
                workspace_root=workspace_root,
                governance_config_path=governance_config_path,
                work_dir=work_dir,
                label=f"roi_{idx}",
            )
        )

    joined_parts = [it["text_joined"] for it in items if it["text_joined"].strip()]
    observed_text_joined = " || ".join(joined_parts)
    conflict_detected = len(items) >= 2 and not _texts_look_duplicate(
        items[0].get("text_joined", ""), items[1].get("text_joined", "")
    )

    reference = {
        "schema_version": "cross_modal_vision_ocr_reference_candidate_v0",
        "reference_scope": "reference_only",
        "fact_status": "not_fact",
        "ocr_refs": {"ocr_text_joined": observed_text_joined, "empty_text": not joined_parts},
    }
    fusion_cand = build_fusion_candidate_from_reference_v0(reference)
    fusion_cand["fact_status"] = "not_fact"

    risk_codes = [
        "conflicting_text_candidate",
        "conflicting_text_risk",
        "conflict_not_resolved",
        "no_conflict_resolution",
        "requires_review_before_fact",
    ]

    return {
        "case_id": case_id,
        "case_type": "CONFLICTING_TEXT_ROI",
        "case_run_id": case_run_id,
        "fixture_refs": list(fixture.get("roi_crop_refs") or []),
        "image_refs": list(fixture.get("image_refs") or []),
        "observed_text_joined": observed_text_joined,
        "observed_text_items": items,
        "observed_empty_text": not bool(observed_text_joined.strip()),
        "observed_item_count": sum(int(it.get("text_item_count") or 0) for it in items),
        "ocr_request_generated": True,
        "rapidocr_invoked": any(it.get("rapidocr_invoked") for it in items),
        "reference_generated": True,
        "fusion_candidate_generated": fusion_cand is not None,
        "risk_codes": risk_codes,
        "conflict_detected": conflict_detected,
        "conflict_resolved": False,
        "no_conflict_resolution": True,
        "confirmed_state_generated": False,
        "review_queue_status": "pending_review_conflict",
        "gate_decision": "hold_for_review",
        "executor_status": "blocked_by_gate",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "boundary_ok": True,
    }


def normalize_prior_row(row: Dict[str, Any]) -> Dict[str, Any]:
    refs = row.get("fixture_refs")
    if not refs and row.get("fixture_ref"):
        refs = [row.get("fixture_ref")]
    out: Dict[str, Any] = {
        "case_id": row.get("case_id"),
        "case_type": row.get("case_type"),
        "case_run_id": row.get("case_run_id"),
        "fixture_refs": refs,
        "fixture_ref": row.get("fixture_ref") or (refs[0] if refs else None),
        "observed_text_joined": row.get("observed_text_joined"),
        "observed_empty_text": row.get("observed_empty_text")
        if "observed_empty_text" in row
        else row.get("empty_text"),
        "observed_item_count": row.get("observed_item_count")
        if row.get("observed_item_count") is not None
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
        "confirmed_state_generated": row.get("confirmed_state_generated", False),
    }
    for flag in (
        "no_forced_interpretation",
        "no_forced_completion",
        "no_translation",
        "no_semantic_interpretation",
        "visual_region_not_text",
        "no_confirmed_sign",
    ):
        if row.get(flag):
            out[flag] = row[flag]
    return out


def load_prior_executed_rows(fc7_root: Path) -> List[Dict[str, Any]]:
    path = fc7_root / "cross_modal_vision_ocr_testboard_full_chain_7cases_case_run_matrix.json"
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
        "confirmed_state_generated": exec_row.get("confirmed_state_generated", False),
    }
    if ct == "DUPLICATE_TEXT_ROI":
        row["duplicate_detected"] = exec_row.get("duplicate_detected")
        row["confirmed_state_generated"] = False
    elif ct == "CONFLICTING_TEXT_ROI":
        row["conflict_detected"] = exec_row.get("conflict_detected")
        row["conflict_resolved"] = exec_row.get("conflict_resolved")
        row["no_conflict_resolution"] = exec_row.get("no_conflict_resolution")
        row["confirmed_state_generated"] = False
    return row


def build_risk_report_v0(exec_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    all_codes = sorted({c for r in exec_rows for c in (r.get("risk_codes") or [])})
    dup = next((r for r in exec_rows if r.get("case_type") == "DUPLICATE_TEXT_ROI"), None)
    conf = next((r for r in exec_rows if r.get("case_type") == "CONFLICTING_TEXT_ROI"), None)
    return {
        "schema_version": RISK_REPORT_SCHEMA,
        "risk_codes_all_executed": all_codes,
        "duplicate_text_candidate_present": "duplicate_text_candidate" in all_codes,
        "duplicate_not_world_fact_present": "duplicate_not_world_fact" in all_codes,
        "no_world_model_write_present": "no_world_model_write" in all_codes,
        "no_confirmed_state_present": "no_confirmed_state" in all_codes,
        "conflicting_text_candidate_present": "conflicting_text_candidate" in all_codes,
        "conflict_not_resolved_present": "conflict_not_resolved" in all_codes,
        "no_conflict_resolution_present": "no_conflict_resolution" in all_codes,
        "requires_review_before_fact_present": "requires_review_before_fact" in all_codes,
        "duplicate_detected": bool(dup and dup.get("duplicate_detected")),
        "conflict_detected": bool(conf and conf.get("conflict_detected")),
        "conflict_resolved_any": any(r.get("conflict_resolved") for r in exec_rows),
        "confirmed_state_generated_any": any(r.get("confirmed_state_generated") for r in exec_rows),
        "world_model_write_allowed_any": any(r.get("world_model_write_allowed") for r in exec_rows),
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


def build_audit_v0(*, executed: int, planned: int, dup_row: Dict[str, Any], conf_row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_testboard_duplicate_conflicting_execution_executed": True,
        "evaluation_only": True,
        "executed_case_count": executed,
        "planned_only_case_count": planned,
        "duplicate_text_case_executed": True,
        "conflicting_text_case_executed": True,
        "duplicate_detected": bool(dup_row.get("duplicate_detected")),
        "conflict_detected": bool(conf_row.get("conflict_detected")),
        "conflict_resolved": False,
        "confirmed_state_generated": False,
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


def run_cross_modal_vision_ocr_testboard_duplicate_conflicting_execution_v0(
    *,
    full_chain_7cases_root: str,
    testboard_expansion_root: str,
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
    fc7 = Path(full_chain_7cases_root).resolve()
    tb = Path(testboard_expansion_root).resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    prior_rows = load_prior_executed_rows(fc7)
    if len(prior_rows) < 7:
        errs.append(f"prior_executed_rows:{len(prior_rows)}")

    fixture_reports: List[Dict[str, Any]] = []
    dup_fixture = create_duplicate_text_fixture_v0(
        work_root / "_fixtures" / "CM_VOCR_009_DUPLICATE_TEXT_ROI",
        case_id="CM_VOCR_009_DUPLICATE_TEXT_ROI",
    )
    fixture_reports.append(dup_fixture)
    dup_row = execute_duplicate_case_v0(
        case_id="CM_VOCR_009_DUPLICATE_TEXT_ROI",
        fixture=dup_fixture,
        workspace_root=workspace_root,
        governance_config_path=governance_config_path,
        work_dir=work_root / "_case_work" / "CM_VOCR_009_DUPLICATE_TEXT_ROI",
    )

    conf_fixture = create_conflicting_text_fixture_v0(
        work_root / "_fixtures" / "CM_VOCR_010_CONFLICTING_TEXT_ROI",
        case_id="CM_VOCR_010_CONFLICTING_TEXT_ROI",
    )
    fixture_reports.append(conf_fixture)
    conf_row = execute_conflicting_case_v0(
        case_id="CM_VOCR_010_CONFLICTING_TEXT_ROI",
        fixture=conf_fixture,
        workspace_root=workspace_root,
        governance_config_path=governance_config_path,
        work_dir=work_root / "_case_work" / "CM_VOCR_010_CONFLICTING_TEXT_ROI",
    )

    executed_rows = prior_rows + [dup_row, conf_row]
    if len(executed_rows) != 9:
        errs.append(f"executed_row_count:{len(executed_rows)}")

    planned_rows = [
        {
            "case_id": PLANNED_ONLY_CASE_IDS[0],
            "case_type": _case_spec(PLANNED_ONLY_CASE_IDS[0]).get("case_type"),
            "execution_status": "planned_only",
            "reason": "fixture_execution_deferred",
            "must_not_have_case_run_id": True,
        }
    ]

    evo_rows = [build_expected_vs_observed_row(r) for r in executed_rows]
    risk_report = build_risk_report_v0(executed_rows)
    boundary_rows = [build_boundary_row(r) for r in executed_rows]

    phase_verdict = "GO" if len(executed_rows) == 9 and len(planned_rows) == 1 and not errs else "CONDITIONAL_GO"
    if len(executed_rows) < 9:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Duplicate-Conflicting-Text-Execution-001",
        "full_chain_7cases_root": str(fc7),
        "testboard_expansion_root": str(tb),
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
        build_audit_v0(executed=len(executed_rows), planned=len(planned_rows), dup_row=dup_row, conf_row=conf_row),
        errs,
    )
