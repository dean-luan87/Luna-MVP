# -*- coding: utf-8 -*-
"""RealVideo ROI-to-OCR reference-only (no OCR submit, no evidence).

Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.vision_runtime.vision_roi_to_ocr_request_bridge_v0 import _should_trigger_ocr_v0

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary_v0"
CANDIDATE_SCHEMA = "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_candidate_v0"
FRAME_ROI_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix_v0"
OCR_REF_SCHEMA = "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix_v0"
CASE_MAP_SCHEMA = "cross_modal_vision_ocr_realvideo_case_to_reference_mapping_v0"
GOV_REF_SCHEMA = "cross_modal_vision_ocr_realvideo_poster_facility_governance_reference_report_v0"
RISK_SCHEMA = "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_risk_report_v0"
METRICS_SCHEMA = "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_metrics_binding_report_v0"
BOUNDARY_SCHEMA = "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_no_write_boundary_report_v0"
SIM_SCHEMA = "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_non_claims_report_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_audit_v0"

POSTER_PREFIXES = ("RV_POSTER_",)
FACILITY_PREFIXES = ("RV_FACILITY_",)
DUPLICATE_CONFLICT_IDS = ("RV_DUPLICATE_TEXT_ACROSS_FRAMES", "RV_CONFLICTING_TEXT_ACROSS_REGIONS")


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _sample_by_frame_id(samples: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(s.get("frame_id") or ""): s for s in samples if isinstance(s, dict) and s.get("frame_id")}


def build_frame_to_roi_reference_matrix(
    *,
    samples: List[Dict[str, Any]],
    roi_items: List[Dict[str, Any]],
) -> Dict[str, Any]:
    by_frame = _sample_by_frame_id(samples)
    rows: List[Dict[str, Any]] = []
    for roi in roi_items:
        if not isinstance(roi, dict):
            continue
        fid = str(roi.get("source_frame_id") or "")
        sample = by_frame.get(fid) or {}
        roi_type = str(roi.get("roi_type") or "")
        trigger, _reason = _should_trigger_ocr_v0(roi)
        eligible = bool(trigger)
        ocr_expected = eligible
        context_only = not eligible and roi_type in ("ground_roi", "left_roi", "right_roi", "center_roi")
        ref_id = f"rvref_{sample.get('sample_id', 'unknown')}_{roi_type}"
        rows.append(
            {
                "reference_id": ref_id,
                "sample_id": sample.get("sample_id"),
                "frame_id": fid,
                "stream_id": sample.get("stream_id") or "",
                "frame_index": sample.get("frame_index"),
                "image_ref": sample.get("image_ref") or roi.get("source_image_ref"),
                "roi_id": str(roi.get("roi_id") or ""),
                "roi_type": roi_type,
                "task_hint": str(roi.get("task_hint") or ""),
                "bbox": list(roi.get("bbox_in_frame") or []),
                "eligible_for_ocr_reference": eligible,
                "ocr_candidate_expected": ocr_expected,
                "non_text_context_only": context_only,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {"schema_version": FRAME_ROI_SCHEMA, "row_count": len(rows), "rows": rows}


def build_ocr_request_reference_matrix(
    bridge_root: Path,
    candidates_doc: Dict[str, Any],
) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for cand in candidates_doc.get("candidates") or []:
        if not isinstance(cand, dict):
            continue
        ocr_req = cand.get("ocr_request") if isinstance(cand.get("ocr_request"), dict) else {}
        cid = str(cand.get("candidate_id") or "")
        rows.append(
            {
                "reference_id": f"ocr_ref_{cid}",
                "ocr_request_candidate_id": cid,
                "ocr_request_id": str(ocr_req.get("request_id") or ocr_req.get("ocr_request_id") or ""),
                "source_frame_id": str(cand.get("source_frame_id") or ""),
                "source_roi_id": str(cand.get("roi_id") or ""),
                "roi_type": str(cand.get("roi_type") or ""),
                "input_type": "roi",
                "allow_full_image": False,
                "candidate_status": str(cand.get("candidate_status") or "not_submitted"),
                "submission_status": "not_submitted",
                "ocr_invoked": False,
                "rapidocr_invoked": False,
                "evidence_generated": False,
                "fact_status": "not_fact",
                "write_allowed": False,
                "bridge_root_ref": str(bridge_root),
            }
        )
    return {"schema_version": OCR_REF_SCHEMA, "row_count": len(rows), "rows": rows}


def _refs_for_poster_or_text(
    frame_roi_rows: List[Dict[str, Any]],
) -> Tuple[List[str], List[str], List[str]]:
    sample_ids: List[str] = []
    roi_refs: List[str] = []
    ocr_refs: List[str] = []
    seen_samples: set = set()
    for row in frame_roi_rows:
        if not isinstance(row, dict):
            continue
        if row.get("eligible_for_ocr_reference"):
            sid = row.get("sample_id")
            if sid and sid not in seen_samples:
                sample_ids.append(str(sid))
                seen_samples.add(sid)
            roi_refs.append(str(row.get("reference_id") or ""))
    return sample_ids, roi_refs, ocr_refs


def build_case_to_reference_mapping(
    *,
    registry: Dict[str, Any],
    frame_roi_rows: List[Dict[str, Any]],
    ocr_ref_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ocr_ref_ids = [str(r.get("reference_id") or "") for r in ocr_ref_rows if isinstance(r, dict)]
    upper_roi_refs = [
        str(r.get("reference_id") or "")
        for r in frame_roi_rows
        if isinstance(r, dict) and r.get("roi_type") == "upper_sign_roi"
    ]
    text_samples, text_roi_refs, _ = _refs_for_poster_or_text(frame_roi_rows)

    rows: List[Dict[str, Any]] = []
    for c in registry.get("cases") or []:
        if not isinstance(c, dict):
            continue
        cid = str(c.get("case_id") or "")
        ctype = str(c.get("case_type") or "")
        if cid in DUPLICATE_CONFLICT_IDS:
            mapping_status = "requires_multi_frame_reference_later"
            mapped_samples: List[str] = []
            mapped_roi = []
            mapped_ocr = []
            expected = "Multi-frame-reference-then-ROI-to-OCR-Reference"
        elif any(cid.startswith(p) for p in FACILITY_PREFIXES):
            mapping_status = "requires_future_facility_specific_video"
            mapped_samples = []
            mapped_roi = []
            mapped_ocr = []
            expected = "PublicFacility-Semantic-Correction-runtime-later"
        elif any(cid.startswith(p) for p in POSTER_PREFIXES):
            mapping_status = "candidate_reference_mapping"
            mapped_samples = text_samples[:3] if text_samples else []
            mapped_roi = upper_roi_refs[:3] if upper_roi_refs else text_roi_refs[:3]
            mapped_ocr = ocr_ref_ids[:3]
            expected = "Poster-Track-B-governance-then-RealVideo-ROI-to-OCR-Reference"
        else:
            mapping_status = "candidate_reference_mapping"
            mapped_samples = text_samples
            mapped_roi = [r for r in upper_roi_refs if r] or text_roi_refs
            mapped_ocr = ocr_ref_ids
            expected = "RealVideo-ROI-to-OCR-Reference-execution-later"

        rows.append(
            {
                "case_id": cid,
                "case_type": ctype,
                "mapped_frame_samples": mapped_samples,
                "mapped_roi_refs": mapped_roi,
                "mapped_ocr_request_refs": mapped_ocr,
                "mapping_status": mapping_status,
                "execution_status": "reference_mapping_only",
                "expected_future_stage": expected,
                "should_submit_ocr_later": mapping_status == "candidate_reference_mapping",
                "should_generate_fusion_later": False,
                "should_write_fact": False,
                "should_invoke_navigation": False,
            }
        )
    return {"schema_version": CASE_MAP_SCHEMA, "case_count": len(rows), "rows": rows}


def build_poster_facility_governance_reference_report(
    *,
    poster_closure_root: Path,
    public_facility_root: Path,
) -> Dict[str, Any]:
    closure_sm = _read_json(poster_closure_root / "poster_testboard_track_b_closure_summary.json") or {}
    facility_available = (
        _read_json(public_facility_root / "public_facility_semantic_correction_governance_summary.json")
        is not None
        or public_facility_root.is_dir()
    )
    return {
        "schema_version": GOV_REF_SCHEMA,
        "poster_track_b_closed": closure_sm.get("track_status") == "closed_for_evaluation",
        "poster_reference_only_available": True,
        "poster_ocr_execution_allowed": False,
        "poster_visual_symbol_registry_invoked": False,
        "public_facility_governance_available": bool(facility_available),
        "facility_detection_invoked": False,
        "facility_semantic_candidate_generated": False,
        "facility_cases_deferred_to_future_runtime": True,
        "poster_track_b_closure_root": str(poster_closure_root),
        "public_facility_governance_root": str(public_facility_root),
    }


def build_risk_report() -> Dict[str, Any]:
    return {
        "schema_version": RISK_SCHEMA,
        "risk_flags": [
            "realvideo_reference_only_not_fact",
            "ocr_request_not_submitted",
            "ocr_evidence_not_generated",
            "frame_roi_reference_not_recognition",
            "poster_case_requires_poster_governance",
            "facility_case_requires_semantic_governance",
            "duplicate_conflict_requires_multi_frame_later",
            "no_fusion",
            "no_scene_delta_candidate",
            "no_world_model_write",
            "no_navigation_decision",
        ],
    }


def build_metrics_binding_report(
    *,
    registry: Dict[str, Any],
    ocr_ref_count: int,
    poster_closure_root: Path,
    metrics_collector_root: Path,
) -> Dict[str, Any]:
    poster_snap = _read_json(poster_closure_root / "poster_testboard_track_b_metrics_snapshot_report.json") or {}
    poster_metrics = poster_snap.get("metrics") if isinstance(poster_snap.get("metrics"), dict) else {}
    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    return {
        "schema_version": METRICS_SCHEMA,
        "metrics_collector_root": str(metrics_collector_root),
        "reference_candidate_count": 1,
        "case_count": len(cases),
        "ocr_request_reference_count": ocr_ref_count,
        "executed_case_count": None,
        "planned_only_case_count": len(cases),
        "ocr_empty_text_count": None,
        "ocr_non_empty_text_count": None,
        "provider_distribution": None,
        "no_write_boundary_pass_rate": 1.0,
        "poster_metrics": poster_metrics,
        "public_facility_future_metrics_placeholder": {
            "facility_semantic_candidate_count": None,
        },
        "performance_metrics_available": False,
        "per_case_latency_ms": None,
        "per_provider_latency_ms": None,
        "missing_metric_behavior": "placeholder_or_future_update_required",
    }


def build_no_write_boundary_report() -> Dict[str, Any]:
    return {
        "schema_version": BOUNDARY_SCHEMA,
        "boundary_ok": True,
        "violations": [],
        "ocr_request_submitted": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
    }


def build_simulation_context_report(sim_root: Path, output_root: Path) -> Dict[str, Any]:
    sm = _read_json(sim_root / "simulation_summary.json") or {}
    return {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sm.get("simulation_profile_id"),
        "simulation_output_root": sm.get("simulation_output_root") or str(sim_root),
        "run_model": sm.get("run_model"),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
        "simulation_context_ref": str((output_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_simulation_context_report.json").resolve()),
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "claims_denied": [
            "no_realvideo_ocr_completed_claim",
            "no_ocr_request_submitted_claim",
            "no_rapidocr_run_claim",
            "no_ocr_evidence_generated_claim",
            "no_fusion_completed_claim",
            "no_scene_delta_candidate_completed_claim",
            "no_poster_detection_completed_claim",
            "no_facility_detection_completed_claim",
            "no_benchmark_claim",
            "no_fact_write_claim",
            "no_navigation_claim",
        ],
        "no_realvideo_ocr_claim": True,
        "no_ocr_evidence_claim": True,
        "no_benchmark_claim": True,
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "realvideo_roi_to_ocr_reference_executed": True,
        "reference_only": True,
        "ocr_request_submitted": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "poster_ocr_execution_invoked": False,
        "poster_visual_symbol_registry_invoked": False,
        "facility_detection_invoked": False,
        "facility_semantic_candidate_generated": False,
        "fusion_invoked": False,
        "semantic_join_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }


def build_reference_candidate(
    *,
    frame_sample_root: Path,
    registry_root: Path,
    roi_root: Path,
    bridge_root: Path,
    poster_closure_root: Path,
    metrics_root: Path,
    rapidocr_ref_root: Path,
    sim_root: Path,
    output_root: Path,
    frame_sample_refs: List[str],
    roi_refs: List[str],
    ocr_refs: List[str],
) -> Dict[str, Any]:
    return {
        "schema_version": CANDIDATE_SCHEMA,
        "reference_scope": "reference_only",
        "frame_sample_refs": frame_sample_refs,
        "roi_refs": roi_refs,
        "ocr_request_candidate_refs": ocr_refs,
        "case_registry_refs": [str((registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json").resolve())],
        "poster_track_b_closure_ref": str(poster_closure_root.resolve()),
        "metrics_collector_ref": str(metrics_root.resolve()),
        "rapidocr_reference_only_ref": str(rapidocr_ref_root.resolve()) if rapidocr_ref_root.is_dir() else None,
        "simulation_context_ref": str(
            (output_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_simulation_context_report.json").resolve()
        ),
        "fact_status": "not_fact",
        "write_allowed": False,
        "ocr_submission_status": "not_submitted",
        "fusion_status": "not_fused",
        "scene_delta_status": "not_generated",
        "frame_sample_root": str(frame_sample_root),
        "roi_proposal_root": str(roi_root),
        "ocr_bridge_root": str(bridge_root),
    }


def build_summary(
    *,
    frame_sample_root: Path,
    registry_root: Path,
    roi_root: Path,
    bridge_root: Path,
    poster_closure_root: Path,
    metrics_root: Path,
    sim_root: Path,
    simulation_attached: bool,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "reference_scope": "reference_only",
        "based_on_frame_sample": frame_sample_root.is_dir(),
        "based_on_case_registry": (registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json").is_file(),
        "based_on_roi_proposal": (roi_root / "vision_roi_proposal_candidate.json").is_file(),
        "based_on_ocr_bridge": (bridge_root / "vision_roi_to_ocr_request_candidates.json").is_file(),
        "based_on_poster_track_b_closure": poster_closure_root.is_dir(),
        "simulation_context_attached": simulation_attached,
        "ocr_request_submitted": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_v0(
    *,
    frame_sample_root: str,
    realvideo_registry_root: str,
    vision_roi_proposal_root: str,
    vision_roi_to_ocr_bridge_root: str,
    cross_modal_rapidocr_reference_root: str,
    poster_track_b_closure_root: str,
    metrics_collector_root: str,
    simulation_lab_harness_root: str,
    public_facility_governance_root: str,
    output_root: str,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
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
    fs_root = Path(frame_sample_root).resolve()
    reg_root = Path(realvideo_registry_root).resolve()
    roi_root = Path(vision_roi_proposal_root).resolve()
    bridge_root = Path(vision_roi_to_ocr_bridge_root).resolve()
    rapidocr_root = Path(cross_modal_rapidocr_reference_root).resolve()
    poster_root = Path(poster_track_b_closure_root).resolve()
    metrics_root = Path(metrics_collector_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    facility_root = Path(public_facility_governance_root).resolve()
    out_root = Path(output_root).resolve()

    index_doc = _read_json(fs_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json")
    registry = _read_json(reg_root / "cross_modal_vision_ocr_realvideo_case_registry.json")
    roi_doc = _read_json(roi_root / "vision_roi_proposal_candidate.json")
    candidates_doc = _read_json(bridge_root / "vision_roi_to_ocr_request_candidates.json")

    if not isinstance(index_doc, dict):
        errs.append("missing_frame_sample_index")
    if not isinstance(registry, dict):
        errs.append("missing_case_registry")
    if not isinstance(roi_doc, dict):
        errs.append("missing_roi_proposal_candidate")
    if not isinstance(candidates_doc, dict):
        errs.append("missing_ocr_bridge_candidates")

    samples = index_doc.get("samples") if isinstance(index_doc, dict) else []
    roi_items = roi_doc.get("roi_items") if isinstance(roi_doc, dict) else []

    frame_roi = build_frame_to_roi_reference_matrix(samples=samples, roi_items=roi_items)
    frame_roi_rows = frame_roi.get("rows") or []
    if len(frame_roi_rows) < 1:
        errs.append("frame_to_roi_row_count_lt_1")

    ocr_matrix = build_ocr_request_reference_matrix(bridge_root, candidates_doc or {})
    ocr_rows = ocr_matrix.get("rows") or []
    for row in ocr_rows:
        if isinstance(row, dict) and row.get("submission_status") != "not_submitted":
            errs.append("ocr_submission_status_not_not_submitted")

    sample_refs = [str(s.get("sample_id")) for s in samples if isinstance(s, dict) and s.get("sample_id")]
    roi_refs = [str(r.get("reference_id")) for r in frame_roi_rows if isinstance(r, dict)]
    ocr_refs = [str(r.get("reference_id")) for r in ocr_rows if isinstance(r, dict)]

    candidate = build_reference_candidate(
        frame_sample_root=fs_root,
        registry_root=reg_root,
        roi_root=roi_root,
        bridge_root=bridge_root,
        poster_closure_root=poster_root,
        metrics_root=metrics_root,
        rapidocr_ref_root=rapidocr_root,
        sim_root=sim_root,
        output_root=out_root,
        frame_sample_refs=sample_refs,
        roi_refs=roi_refs,
        ocr_refs=ocr_refs,
    )

    case_map = build_case_to_reference_mapping(
        registry=registry or {"cases": []},
        frame_roi_rows=frame_roi_rows,
        ocr_ref_rows=ocr_rows,
    )
    for row in case_map.get("rows") or []:
        if isinstance(row, dict) and row.get("execution_status") != "reference_mapping_only":
            errs.append(f"case_execution_status_wrong:{row.get('case_id')}")
        if isinstance(row, dict) and row.get("should_write_fact") is not False:
            errs.append(f"case_should_write_fact:{row.get('case_id')}")

    gov_report = build_poster_facility_governance_reference_report(
        poster_closure_root=poster_root,
        public_facility_root=facility_root,
    )
    if not gov_report.get("poster_track_b_closed"):
        errs.append("poster_track_b_not_closed")

    risk = build_risk_report()
    metrics = build_metrics_binding_report(
        registry=registry or {"cases": []},
        ocr_ref_count=len(ocr_rows),
        poster_closure_root=poster_root,
        metrics_collector_root=metrics_root,
    )
    boundary = build_no_write_boundary_report()
    sim_report = build_simulation_context_report(sim_root, out_root)
    if sim_report.get("simulation_profile_id") != "developer_full":
        errs.append("simulation_profile_id_not_developer_full")

    non_claims = build_non_claims_report()
    audit = build_audit()
    summary = build_summary(
        frame_sample_root=fs_root,
        registry_root=reg_root,
        roi_root=roi_root,
        bridge_root=bridge_root,
        poster_closure_root=poster_root,
        metrics_root=metrics_root,
        sim_root=sim_root,
        simulation_attached=_read_json(sim_root / "simulation_summary.json") is not None,
    )

    return (
        summary,
        candidate,
        frame_roi,
        ocr_matrix,
        case_map,
        gov_report,
        risk,
        metrics,
        boundary,
        sim_report,
        non_claims,
        audit,
        errs,
    )
