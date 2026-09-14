# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard v1 RealVideo frame sample smoke (index only).

Phase-CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.vision_runtime.vision_frame_trace_v0 import load_video_frame_envelopes_jsonl

PHASE_ID = "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001"

SUMMARY_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_sample_summary_v0"
INDEX_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_sample_index_v0"
QUALITY_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_quality_placeholder_matrix_v0"
COVERAGE_SCHEMA = "cross_modal_vision_ocr_realvideo_case_coverage_mapping_v0"
POSTER_FACILITY_SCHEMA = "cross_modal_vision_ocr_realvideo_poster_facility_candidate_mapping_v0"
METRICS_BINDING_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_sample_metrics_binding_report_v0"
BOUNDARY_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_sample_no_write_boundary_report_v0"
SIM_CONTEXT_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_sample_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_sample_non_claims_report_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_realvideo_frame_sample_audit_v0"

POSTER_CASE_PREFIXES = ("RV_POSTER_",)
FACILITY_CASE_PREFIXES = ("RV_FACILITY_",)


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _load_traces(trace_root: Path) -> List[Dict[str, Any]]:
    path = trace_root / "vision_frame_trace.jsonl"
    rows: List[Dict[str, Any]] = []
    if not path.is_file():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if isinstance(o, dict):
            rows.append(o)
    return rows


def _governance_by_frame_id(gov_root: Path) -> Dict[str, Dict[str, Any]]:
    mx = _read_json(gov_root / "vision_frame_input_governance_matrix.json") or {}
    out: Dict[str, Dict[str, Any]] = {}
    for row in mx.get("rows") or []:
        if isinstance(row, dict) and row.get("frame_id"):
            out[str(row["frame_id"])] = row
    return out


def build_frame_sample_index(
    *,
    ingest_root: Path,
    trace_root: Path,
    governance_root: Path,
    output_root: Path,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    envelopes = load_video_frame_envelopes_jsonl(ingest_root / "video_frame_envelopes.jsonl")
    traces = _load_traces(trace_root)
    trace_by_fid = {str(t.get("frame_id") or ""): t for t in traces}
    gov_by_fid = _governance_by_frame_id(governance_root)

    samples: List[Dict[str, Any]] = []
    ordered = sorted(envelopes, key=lambda e: int(e.get("frame_index") or 0))
    for i, env in enumerate(ordered):
        fid = str(env.get("frame_id") or "")
        tr = trace_by_fid.get(fid) or env
        gov = gov_by_fid.get(fid) or {}
        accepted = bool(gov.get("frame_accepted", True))
        input_status = "accepted" if accepted else "rejected"
        sample_id = f"RVFS_{i:04d}"
        samples.append(
            {
                "sample_id": sample_id,
                "frame_id": fid,
                "stream_id": str(env.get("stream_id") or tr.get("stream_id") or ""),
                "source_video_ref": str(env.get("source_video_ref") or ""),
                "frame_index": int(env.get("frame_index") or 0),
                "timestamp_ms": int(env.get("timestamp_ms") or tr.get("timestamp_ms") or 0),
                "image_ref": str(env.get("image_ref") or tr.get("image_ref") or ""),
                "frame_fingerprint": str(env.get("frame_fingerprint") or tr.get("frame_fingerprint") or ""),
                "input_status": input_status,
                "eligible_for_roi_proposal": bool(gov.get("eligible_for_roi_proposal", accepted)),
                "eligible_for_recognition": False,
                "fact_status": "not_fact",
                "write_allowed": False,
                "source_chain": [
                    str((ingest_root / "video_frame_envelopes.jsonl").resolve()),
                    str((trace_root / "vision_frame_trace.jsonl").resolve()),
                    str((governance_root / "vision_frame_input_governance_matrix.json").resolve()),
                    "realvideo_frame_sample_smoke_built",
                    str(output_root.resolve()),
                ],
            }
        )

    return {
        "schema_version": INDEX_SCHEMA,
        "phase": PHASE_ID,
        "sample_count": len(samples),
        "samples": samples,
        "ingest_root": str(ingest_root),
        "trace_root": str(trace_root),
        "governance_root": str(governance_root),
    }, samples


def build_quality_placeholder_matrix(samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows = []
    for s in samples:
        rows.append(
            {
                "sample_id": s["sample_id"],
                "frame_id": s["frame_id"],
                "frame_quality_placeholder": "not_measured_smoke_v0",
                "motion_blur_score_placeholder": None,
                "lighting_score_placeholder": None,
                "reflection_glare_score_placeholder": None,
                "roi_quality_score_placeholder": None,
                "quality_metrics_available": False,
                "performance_claim_allowed": False,
            }
        )
    return {"schema_version": QUALITY_SCHEMA, "row_count": len(rows), "rows": rows}


def _expected_future_stage(case_type: str) -> str:
    if case_type.startswith("REAL_VIDEO_POSTER"):
        return "Poster-Track-B-governance-then-RealVideo-ROI-to-OCR-Reference"
    if case_type.startswith("REAL_VIDEO_FACILITY"):
        return "PublicFacility-Semantic-Correction-then-reference-only"
    return "RealVideo-ROI-to-OCR-Reference"


def build_case_coverage_mapping(
    registry: Dict[str, Any],
    samples: List[Dict[str, Any]],
) -> Dict[str, Any]:
    sample_ids = [s["sample_id"] for s in samples]
    rows: List[Dict[str, Any]] = []
    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    for c in cases:
        if not isinstance(c, dict):
            continue
        cid = str(c.get("case_id") or "")
        ctype = str(c.get("case_type") or "")
        if any(cid.startswith(p) for p in FACILITY_CASE_PREFIXES):
            mapping_status = "requires_future_real_video"
            mapped = []
        elif any(cid.startswith(p) for p in POSTER_CASE_PREFIXES):
            mapping_status = "candidate_mapping"
            mapped = list(sample_ids)
        else:
            mapping_status = "candidate_mapping"
            mapped = list(sample_ids)
        rows.append(
            {
                "case_id": cid,
                "case_type": ctype,
                "mapped_sample_ids": mapped,
                "mapping_status": mapping_status,
                "execution_status": "sample_mapping_only",
                "should_run_ocr_later": not ctype.startswith("REAL_VIDEO_FACILITY"),
                "should_run_vision_provider_later": True,
                "expected_future_stage": _expected_future_stage(ctype),
            }
        )
    return {"schema_version": COVERAGE_SCHEMA, "case_count": len(rows), "rows": rows}


def build_poster_facility_candidate_mapping(
    *,
    registry: Dict[str, Any],
    poster_closure_root: Path,
    public_facility_root: Path,
) -> Dict[str, Any]:
    cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    poster_ids = [c["case_id"] for c in cases if isinstance(c, dict) and str(c.get("case_id", "")).startswith("RV_POSTER_")]
    facility_ids = [
        c["case_id"] for c in cases if isinstance(c, dict) and str(c.get("case_id", "")).startswith("RV_FACILITY_")
    ]
    closure_sm = _read_json(poster_closure_root / "poster_testboard_track_b_closure_summary.json") or {}
    poster_closed = closure_sm.get("track_status") == "closed_for_evaluation"
    facility_sm = _read_json(
        public_facility_root / "public_facility_semantic_correction_governance_summary.json"
    )
    facility_available = facility_sm is not None or public_facility_root.is_dir()

    return {
        "schema_version": POSTER_FACILITY_SCHEMA,
        "poster_governance_available": True,
        "poster_track_b_closed": poster_closed,
        "public_facility_governance_available": bool(facility_available),
        "poster_like_detection_invoked": False,
        "facility_detection_invoked": False,
        "poster_candidate_regions_generated": False,
        "facility_semantic_candidate_generated": False,
        "poster_related_case_ids": poster_ids,
        "facility_related_case_ids": facility_ids,
        "future_expected_governance_path": {
            "poster": "poster_layout_segmentation_governance → region_ocr_plan_stub → visual_symbol_evidence → reference_only",
            "public_facility": "public_facility_semantic_correction_governance → semantic_first_reference_later",
        },
        "poster_track_b_closure_root": str(poster_closure_root),
        "public_facility_governance_root": str(public_facility_root),
    }


def build_metrics_binding_report(
    *,
    registry: Dict[str, Any],
    poster_closure_root: Path,
    metrics_collector_root: Path,
) -> Dict[str, Any]:
    reg_cases = registry.get("cases") if isinstance(registry.get("cases"), list) else []
    case_count = len(reg_cases)
    poster_snap = _read_json(poster_closure_root / "poster_testboard_track_b_metrics_snapshot_report.json") or {}
    poster_metrics = poster_snap.get("metrics") if isinstance(poster_snap.get("metrics"), dict) else {}

    return {
        "schema_version": METRICS_BINDING_SCHEMA,
        "metrics_collector_root": str(metrics_collector_root),
        "case_count": case_count,
        "executed_case_count": None,
        "planned_only_case_count": case_count,
        "ocr_empty_text_count": None,
        "ocr_non_empty_text_count": None,
        "provider_distribution": None,
        "no_write_boundary_pass_rate": 1.0,
        "poster_metrics": poster_metrics,
        "public_facility_future_metrics_placeholder": {
            "facility_semantic_candidate_count": None,
            "facility_ocr_auxiliary_only_count": None,
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
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
    }


def build_simulation_context_report(sim_root: Path) -> Dict[str, Any]:
    sm = _read_json(sim_root / "simulation_summary.json") or {}
    return {
        "schema_version": SIM_CONTEXT_SCHEMA,
        "simulation_profile_id": sm.get("simulation_profile_id"),
        "simulation_output_root": sm.get("simulation_output_root") or str(sim_root),
        "run_model": sm.get("run_model"),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "claims_denied": [
            "no_realvideo_recognition_claim",
            "no_realvideo_ocr_claim",
            "no_realvideo_cases_executed_claim",
            "no_poster_like_detection_claim",
            "no_public_facility_detection_claim",
            "no_benchmark_claim",
            "no_performance_claim",
            "no_fact_write_claim",
            "no_navigation_claim",
            "no_production_video_pipeline_claim",
        ],
        "no_realvideo_ocr_claim": True,
        "no_benchmark_claim": True,
    }


def build_audit(*, new_video_decoded: bool) -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "realvideo_frame_sample_smoke_executed": True,
        "sample_only": True,
        "new_video_decoded": new_video_decoded,
        "real_camera_invoked": False,
        "runtime_execution": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "poster_like_detection_invoked": False,
        "facility_detection_invoked": False,
        "ocr_request_generated": False,
        "cross_modal_reference_generated": False,
        "fusion_invoked": False,
        "semantic_join_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }


def build_summary(
    *,
    realvideo_registry_root: Path,
    poster_closure_root: Path,
    metrics_collector_root: Path,
    simulation_root: Path,
    trace_root: Path,
    new_video_decoded: bool,
    sample_count: int,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "sample_scope": "frame_sample_smoke_only",
        "based_on_realvideo_registry": realvideo_registry_root.is_dir(),
        "based_on_poster_track_b_closure": poster_closure_root.is_dir(),
        "based_on_metrics_collector": metrics_collector_root.is_dir(),
        "based_on_simulation_lab": simulation_root.is_dir(),
        "based_on_vision_frame_trace": (trace_root / "vision_frame_trace.jsonl").is_file(),
        "sample_count": sample_count,
        "real_camera_invoked": False,
        "new_video_decoded": new_video_decoded,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "yolo_invoked": False,
        "vlm_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_cross_modal_vision_ocr_realvideo_frame_sample_smoke_v0(
    *,
    realvideo_registry_root: str,
    poster_track_b_closure_root: str,
    metrics_collector_root: str,
    simulation_lab_harness_root: str,
    vision_ingest_root: str,
    vision_frame_trace_root: str,
    vision_frame_input_governance_root: str,
    public_facility_governance_root: str,
    output_root: str,
    new_video_decoded: bool = False,
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
    List[str],
]:
    errs: List[str] = []
    reg_root = Path(realvideo_registry_root).resolve()
    poster_root = Path(poster_track_b_closure_root).resolve()
    metrics_root = Path(metrics_collector_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    ingest_root = Path(vision_ingest_root).resolve()
    trace_root = Path(vision_frame_trace_root).resolve()
    gov_root = Path(vision_frame_input_governance_root).resolve()
    facility_root = Path(public_facility_governance_root).resolve()
    out_root = Path(output_root).resolve()

    registry = _read_json(reg_root / "cross_modal_vision_ocr_realvideo_case_registry.json")
    if not isinstance(registry, dict):
        errs.append("missing_realvideo_case_registry")

    env_path = ingest_root / "video_frame_envelopes.jsonl"
    if not env_path.is_file():
        errs.append("missing_video_frame_envelopes")
    if not (trace_root / "vision_frame_trace.jsonl").is_file():
        errs.append("missing_vision_frame_trace")
    if not (gov_root / "vision_frame_input_governance_matrix.json").is_file():
        errs.append("missing_vision_frame_input_governance_matrix")

    index_doc, samples = build_frame_sample_index(
        ingest_root=ingest_root,
        trace_root=trace_root,
        governance_root=gov_root,
        output_root=out_root,
    )
    if len(samples) < 1:
        errs.append("sample_count_below_minimum")
    quality = build_quality_placeholder_matrix(samples)
    coverage = build_case_coverage_mapping(registry or {"cases": []}, samples)
    poster_facility = build_poster_facility_candidate_mapping(
        registry=registry or {"cases": []},
        poster_closure_root=poster_root,
        public_facility_root=facility_root,
    )
    if not poster_facility.get("poster_track_b_closed"):
        errs.append("poster_track_b_not_closed")
    if not poster_facility.get("public_facility_governance_available"):
        errs.append("public_facility_governance_not_available")

    metrics_binding = build_metrics_binding_report(
        registry=registry or {"cases": []},
        poster_closure_root=poster_root,
        metrics_collector_root=metrics_root,
    )
    boundary = build_no_write_boundary_report()
    sim_report = build_simulation_context_report(sim_root)
    if sim_report.get("simulation_profile_id") != "developer_full":
        errs.append("simulation_profile_id_not_developer_full")
    if sim_report.get("run_model") is not False:
        errs.append("simulation_run_model_not_false")

    non_claims = build_non_claims_report()
    audit = build_audit(new_video_decoded=new_video_decoded)
    summary = build_summary(
        realvideo_registry_root=reg_root,
        poster_closure_root=poster_root,
        metrics_collector_root=metrics_root,
        simulation_root=sim_root,
        trace_root=trace_root,
        new_video_decoded=new_video_decoded,
        sample_count=len(samples),
    )

    reg_cases = registry.get("cases") if isinstance(registry, dict) else []
    if len(reg_cases) != 16:
        errs.append(f"registry_case_count_not_16:got_{len(reg_cases)}")

    return (
        summary,
        index_doc,
        quality,
        coverage,
        poster_facility,
        metrics_binding,
        boundary,
        sim_report,
        non_claims,
        audit,
        errs,
    )
