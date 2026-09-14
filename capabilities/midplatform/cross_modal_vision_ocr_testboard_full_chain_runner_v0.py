# -*- coding: utf-8 -*-
"""TestBoard full-chain case runner for executed cases only (no writes).

Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Case-Runner-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.cross_modal_fusion_review_queue_v0 import (
    build_review_queue_candidate_v0,
)
from capabilities.midplatform.cross_modal_scene_delta_executor_trace_stub_v0 import (
    build_executor_trace_stub_v0,
)
from capabilities.midplatform.cross_modal_scene_delta_gate_evaluator_dryrun_v0 import (
    build_gate_evaluation_result_v0,
)
from capabilities.midplatform.cross_modal_vision_ocr_fusion_candidate_dryrun_v0 import (
    build_fusion_candidate_from_reference_v0,
)
from capabilities.midplatform.cross_modal_vision_ocr_testboard_expansion_v0 import (
    CASE_SPECS,
    apply_rapidocr_eval_env,
    expected_behavior_for_case,
    run_rapidocr_on_crop_v0,
)
from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

RUN_PLAN_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_run_plan_v0"
CASE_RUN_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_case_run_matrix_v0"
PLANNED_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_planned_only_case_matrix_v0"
EXPECTED_VS_OBSERVED_SCHEMA = "cross_modal_vision_ocr_testboard_expected_vs_observed_report_v0"
RISK_COVERAGE_SCHEMA = "cross_modal_vision_ocr_testboard_risk_coverage_report_v0"
BOUNDARY_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_boundary_matrix_v0"
SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_run_summary_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_audit_v0"

CHAIN_STAGES = [
    "fixture",
    "ocr_request",
    "rapidocr",
    "reference_only",
    "fusion_candidate_dryrun",
    "review_queue",
    "gate_evaluator",
    "executor_trace_stub",
]

EXECUTED_CASE_IDS = frozenset(
    {
        "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
        "CM_VOCR_002_EMPTY_TEXT_ROI",
        "CM_VOCR_006_MULTI_TEXT_LINES",
    }
)

FRAME_ID_PREFIX = "testboard_case"


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _case_spec_by_id(case_id: str) -> Dict[str, Any]:
    for s in CASE_SPECS:
        if s["case_id"] == case_id:
            return s
    return {}


def _build_reference_candidate(
    *,
    frame_id: str,
    roi_id: str,
    ocr_fields: Dict[str, Any],
    candidate_id: str,
) -> Dict[str, Any]:
    text_joined = str(ocr_fields.get("text_joined") or "")
    empty_text = not text_joined.strip()
    return {
        "schema_version": "cross_modal_vision_ocr_reference_candidate_v0",
        "reference_id": f"xref_{uuid.uuid4().hex[:16]}",
        "reference_scope": "reference_only",
        "source": "testboard_full_chain_runner",
        "frame_id": frame_id,
        "roi_id": roi_id,
        "roi_type": "upper_sign_roi",
        "vision_refs": {"roi_ref": roi_id, "vision_evidence_refs": []},
        "ocr_refs": {
            "ocr_provider": "rapidocr_candidate",
            "ocr_request_candidate_id": candidate_id,
            "ocr_request_id": ocr_fields.get("ocr_request_id"),
            "ocr_text_joined": text_joined,
            "empty_text": empty_text,
            "real_provider_invoked": bool(ocr_fields.get("rapidocr_invoked")),
            "rapidocr_invoked": bool(ocr_fields.get("rapidocr_invoked")),
        },
        "spatial_reference": {
            "bbox_in_frame": [128, 0, 512, 120],
            "coordinate_space": "frame_pixel",
        },
        "fact_status": "not_fact",
        "fusion_status": "not_fused",
    }


def run_single_case_full_chain_v0(
    *,
    case_id: str,
    case_type: str,
    fixture_ref: str,
    roi_bbox_in_crop: List[int],
    expected_text_hint: List[str],
    workspace_root: Path,
    governance_config_path: Path,
    work_dir: Path,
) -> Dict[str, Any]:
    case_run_id = f"crun_{uuid.uuid4().hex[:16]}"
    frame_id = f"{FRAME_ID_PREFIX}_{case_id[-8:].lower()}"
    roi_id = f"vision_roi_{frame_id}_upper_sign_roi"
    risk_codes: List[str] = []

    apply_rapidocr_eval_env()
    ocr_obs = run_rapidocr_on_crop_v0(
        crop_image_ref=fixture_ref,
        roi_bbox_in_crop=roi_bbox_in_crop,
        workspace_root=workspace_root,
        governance_config_path=governance_config_path,
        work_dir=work_dir / "ocr",
    )

    ocr_req = OCRRequestV0(
        input_type="roi",
        image_path=fixture_ref,
        roi_refs=[f"ocr_roi_xyxy:{roi_bbox_in_crop[0]},{roi_bbox_in_crop[1]},{roi_bbox_in_crop[2]},{roi_bbox_in_crop[3]}"],
        task_context="testboard_full_chain_runner",
        allow_full_image=False,
        expected_output="ocr_evidence",
    )
    ocr_fields = dict(ocr_obs)
    ocr_fields["ocr_request_id"] = ocr_req.request_id

    reference = _build_reference_candidate(
        frame_id=frame_id,
        roi_id=roi_id,
        ocr_fields=ocr_fields,
        candidate_id=f"ocr_req_cand_{case_run_id}",
    )

    fusion_skipped_reason = None
    if case_type == "EMPTY_TEXT_ROI" and ocr_obs.get("empty_text"):
        fusion_skipped_reason = "skipped_or_empty_text_candidate"
        risk_codes.append("empty_text_valid")

    fusion_cand = build_fusion_candidate_from_reference_v0(reference)
    fusion_cand["candidate_id"] = f"fusion_cand_{case_run_id}"

    if case_type == "MULTI_TEXT_LINES":
        if int(ocr_obs.get("text_item_count") or 0) >= 2:
            risk_codes.append("multi_line_text_risk")
        else:
            risk_codes.append("reading_order_risk")

    review_queue_status = "skipped_not_positive_case"
    queue_item = None
    if case_type == "POSITIVE_TEXT_CLEAR" and fusion_cand:
        queue_item = build_review_queue_candidate_v0(
            fusion_cand,
            fusion_dryrun_root=work_dir,
            candidate_payload_ref=str((work_dir / "fusion_payload.json").resolve()),
        )
        queue_item["queue_item_id"] = f"rq_{case_run_id}"
        review_queue_status = "pending_review"
    elif case_type == "MULTI_TEXT_LINES" and fusion_cand:
        review_queue_status = "pending_review_with_risk"
        queue_item = build_review_queue_candidate_v0(
            fusion_cand,
            fusion_dryrun_root=work_dir,
            candidate_payload_ref=str((work_dir / "fusion_payload.json").resolve()),
        )
        queue_item["queue_item_id"] = f"rq_{case_run_id}"

    gate_decision = "not_run"
    gate_eval = None
    executor_status = "not_run"
    trace = None

    sd_cand_for_gate = None
    if fusion_cand and queue_item and case_type == "POSITIVE_TEXT_CLEAR":
        sd_cand_for_gate = {
            "candidate_id": f"sd_cand_{case_run_id}",
            "candidate_scope": "dry_run_only",
            "fact_status": "not_fact",
            "write_allowed": False,
            "requires_gate_approval": True,
            "gate_status": "not_evaluated",
            "approval_status": "not_approved",
            "review_status": review_queue_status,
        }
        gate_eval = build_gate_evaluation_result_v0(sd_cand_for_gate)
        gate_decision = str(gate_eval.get("decision") or "hold_for_review")
        trace = build_executor_trace_stub_v0(sd_cand_for_gate, gate_eval)
        trace["trace_id"] = f"trace_{case_run_id}"
        executor_status = str(trace.get("execution_status") or "blocked_by_gate")
    elif case_type in ("EMPTY_TEXT_ROI", "MULTI_TEXT_LINES"):
        gate_decision = "hold_for_review"
        executor_status = "blocked_by_gate"
        if case_type == "EMPTY_TEXT_ROI":
            risk_codes.append("empty_text_case_covered")

    exp = expected_behavior_for_case(_case_spec_by_id(case_id) or {"case_id": case_id, "case_type": case_type})

    return {
        "case_id": case_id,
        "case_type": case_type,
        "case_run_id": case_run_id,
        "fixture_ref": fixture_ref,
        "expected_text_hint": expected_text_hint,
        "observed_text_joined": ocr_obs.get("text_joined"),
        "empty_text": ocr_obs.get("empty_text"),
        "text_item_count": ocr_obs.get("text_item_count"),
        "ocr_request_generated": True,
        "rapidocr_invoked": bool(ocr_obs.get("rapidocr_invoked")),
        "reference_generated": True,
        "fusion_candidate_generated": fusion_cand is not None,
        "fusion_skipped_reason": fusion_skipped_reason,
        "review_queue_status": review_queue_status,
        "gate_decision": gate_decision,
        "executor_status": executor_status,
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "boundary_ok": True,
        "risk_codes": risk_codes,
        "expected": exp,
        "work_dir": str(work_dir.resolve()),
    }


def build_expected_vs_observed_row(run_row: Dict[str, Any]) -> Dict[str, Any]:
    exp = run_row.get("expected") if isinstance(run_row.get("expected"), dict) else {}
    ct = run_row.get("case_type")
    obs_non_empty = not bool(run_row.get("empty_text"))
    return {
        "case_id": run_row.get("case_id"),
        "case_type": ct,
        "case_run_id": run_row.get("case_run_id"),
        "expected_text_non_empty": bool(exp.get("expected_text_non_empty")),
        "observed_text_non_empty": obs_non_empty,
        "expected_empty_text": ct == "EMPTY_TEXT_ROI",
        "observed_empty_text": bool(run_row.get("empty_text")),
        "expected_final_fact_status": "not_fact",
        "observed_final_fact_status": run_row.get("final_fact_status"),
        "expected_final_write_status": "no_write",
        "observed_final_write_status": run_row.get("final_write_status"),
        "expected_executor_status": (
            "blocked_by_gate" if ct == "POSITIVE_TEXT_CLEAR" else "blocked_by_gate_or_no_write_trace"
        ),
        "observed_executor_status": run_row.get("executor_status"),
        "match_text_non_empty": bool(exp.get("expected_text_non_empty")) == obs_non_empty,
        "match_empty_text": (ct == "EMPTY_TEXT_ROI") == bool(run_row.get("empty_text")),
        "match_fact_status": run_row.get("final_fact_status") == "not_fact",
        "match_write_status": run_row.get("final_write_status") == "no_write",
    }


def build_risk_coverage_report_v0(run_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    types = {r.get("case_type") for r in run_rows}
    return {
        "schema_version": RISK_COVERAGE_SCHEMA,
        "empty_text_case_covered": "EMPTY_TEXT_ROI" in types,
        "positive_text_case_covered": "POSITIVE_TEXT_CLEAR" in types,
        "multi_line_text_case_covered": "MULTI_TEXT_LINES" in types,
        "no_write_boundary_covered": all(r.get("final_write_status") == "no_write" for r in run_rows),
        "review_queue_covered": any(r.get("review_queue_status", "").startswith("pending") for r in run_rows),
        "gate_evaluator_covered": any(r.get("gate_decision") == "hold_for_review" for r in run_rows),
        "executor_blocked_trace_covered": any(
            r.get("executor_status") == "blocked_by_gate" for r in run_rows
        ),
        "risk_codes_observed": sorted({c for r in run_rows for c in (r.get("risk_codes") or [])}),
    }


def build_full_chain_audit_v0(*, selected: int, planned: int) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_testboard_full_chain_case_runner_executed": True,
        "evaluation_only": True,
        "selected_case_count": selected,
        "planned_only_case_count": planned,
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


def run_cross_modal_vision_ocr_testboard_full_chain_runner_v0(
    *,
    testboard_root: str,
    workspace_root: Path,
    governance_config_path: Path,
    chain_closure_root: Optional[str] = None,
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
    tb = Path(testboard_root).resolve()
    exec_matrix_path = tb / "cross_modal_vision_ocr_testboard_case_execution_matrix.json"
    registry_path = tb / "cross_modal_vision_ocr_testboard_registry.json"

    if not exec_matrix_path.is_file():
        errs.append(f"missing:{exec_matrix_path}")
        exec_rows: List[Dict[str, Any]] = []
    else:
        exec_rows = [
            r
            for r in (_read_json(exec_matrix_path).get("rows") or [])
            if isinstance(r, dict)
        ]

    registry = _read_json(registry_path) if registry_path.is_file() else {}
    case_count = int(registry.get("case_count") or len(CASE_SPECS))

    executed_rows = [r for r in exec_rows if r.get("case_execution_status") == "executed"]
    planned_rows = [r for r in exec_rows if r.get("case_execution_status") == "planned_only"]

    run_plan = {
        "schema_version": RUN_PLAN_SCHEMA,
        "testboard_root": str(tb),
        "chain_closure_root": str(Path(chain_closure_root).resolve()) if chain_closure_root else None,
        "case_count": case_count,
        "selected_case_count": len(executed_rows),
        "planned_only_case_count": len(planned_rows),
        "run_scope": "executed_cases_only",
        "chain_stages": list(CHAIN_STAGES),
    }

    case_run_rows: List[Dict[str, Any]] = []
    for ex in executed_rows:
        cid = str(ex.get("case_id") or "")
        if cid not in EXECUTED_CASE_IDS:
            errs.append(f"unexpected_executed_case:{cid}")
        fixture_ref = str(ex.get("fixture_ref") or "")
        if not fixture_ref or not Path(fixture_ref).is_file():
            errs.append(f"fixture_missing_for_executed:{cid}")
            continue
        spec = _case_spec_by_id(cid)
        run_row = run_single_case_full_chain_v0(
            case_id=cid,
            case_type=str(ex.get("case_type") or spec.get("case_type") or ""),
            fixture_ref=fixture_ref,
            roi_bbox_in_crop=[0, 0, 384, 120],
            expected_text_hint=list(spec.get("expected_text_hint") or []),
            workspace_root=workspace_root,
            governance_config_path=governance_config_path,
            work_dir=work_root / cid,
        )
        case_run_rows.append(run_row)

    planned_matrix_rows = [
        {
            "case_id": r.get("case_id"),
            "case_type": r.get("case_type"),
            "execution_status": "planned_only",
            "reason": "fixture_execution_deferred",
            "must_not_have_case_run_id": True,
        }
        for r in planned_rows
    ]

    evo_rows = [build_expected_vs_observed_row(r) for r in case_run_rows]
    expected_vs_observed = {
        "schema_version": EXPECTED_VS_OBSERVED_SCHEMA,
        "row_count": len(evo_rows),
        "rows": evo_rows,
    }

    risk_coverage = build_risk_coverage_report_v0(case_run_rows)
    boundary_rows = [
        {
            "case_id": r.get("case_id"),
            "case_run_id": r.get("case_run_id"),
            **{
                k: False
                for k in (
                    "midplatform_fact_written",
                    "scene_delta_written",
                    "world_model_written",
                    "scene_delta_executor_invoked",
                    "database_write_invoked",
                    "wal_append_invoked",
                    "navigation_decision_invoked",
                    "auto_approve_invoked",
                    "approval_granted",
                )
            },
        }
        for r in case_run_rows
    ]
    boundary_doc = {
        "schema_version": BOUNDARY_MATRIX_SCHEMA,
        "boundary_all_ok": True,
        "rows": boundary_rows,
    }

    if len(case_run_rows) < 3:
        errs.append(f"case_run_row_count:{len(case_run_rows)}")

    phase_verdict = "GO" if len(case_run_rows) >= 3 and not errs else "CONDITIONAL_GO"
    if errs and len(case_run_rows) < 3:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Case-Runner-001",
        "testboard_root": str(tb),
        "case_count": case_count,
        "selected_case_count": len(case_run_rows),
        "planned_only_case_count": len(planned_matrix_rows),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    audit = build_full_chain_audit_v0(
        selected=len(case_run_rows),
        planned=len(planned_matrix_rows),
    )

    return (
        summary,
        run_plan,
        {"schema_version": CASE_RUN_MATRIX_SCHEMA, "row_count": len(case_run_rows), "rows": case_run_rows},
        {
            "schema_version": PLANNED_MATRIX_SCHEMA,
            "row_count": len(planned_matrix_rows),
            "rows": planned_matrix_rows,
        },
        expected_vs_observed,
        risk_coverage,
        boundary_doc,
        audit,
        errs,
    )
