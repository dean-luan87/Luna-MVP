# -*- coding: utf-8 -*-
"""RealVideo OCR reference-only update (parallel refs; no fusion).

Phase-RealVideo-OCR-Reference-Update-001
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "RealVideo-OCR-Reference-Update-001"
ELIGIBLE_ROI_TYPE = "upper_sign_roi"

SUMMARY_SCHEMA = "realvideo_ocr_reference_update_summary_v0"
CANDIDATE_SCHEMA = "realvideo_ocr_updated_reference_candidate_v0"
ALIGNMENT_SCHEMA = "realvideo_ocr_reference_update_alignment_matrix_v0"
REJECTED_PRESERVE_SCHEMA = "realvideo_ocr_reference_update_rejected_roi_preservation_report_v0"
EMPTY_GUARD_SCHEMA = "realvideo_ocr_reference_update_empty_text_guard_report_v0"
CASE_MAPPING_SCHEMA = "realvideo_ocr_reference_update_case_mapping_report_v0"
CHAIN_SCHEMA = "realvideo_ocr_reference_update_source_chain_report_v0"
METRICS_SCHEMA = "realvideo_ocr_reference_update_metrics_candidate_report_v0"
BENCHMARK_SCHEMA = "realvideo_ocr_reference_update_benchmark_link_report_v0"
HEALTH_SCHEMA = "realvideo_ocr_reference_update_system_health_link_report_v0"
BOUNDARY_SCHEMA = "realvideo_ocr_reference_update_no_write_boundary_report_v0"
SIM_SCHEMA = "realvideo_ocr_reference_update_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "realvideo_ocr_reference_update_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "realvideo_ocr_reference_update_open_followups_v0"
AUDIT_SCHEMA = "realvideo_ocr_reference_update_audit_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _source_ok(root: Path, summary_name: str) -> bool:
    sm = _read_json(root / summary_name) or {}
    if not sm:
        return False
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    return hint in ("GO", "CONDITIONAL_GO")


def run_realvideo_ocr_reference_update_v0(
    *,
    realvideo_roi_to_ocr_reference_root: str,
    realvideo_gated_submission_root: str,
    realvideo_readonly_consumer_root: str,
    realvideo_frame_sample_root: str,
    realvideo_case_registry_root: str,
    vision_roi_proposal_root: str,
    vision_roi_to_ocr_bridge_root: str,
    benchmark_real_values_smoke_root: str,
    system_health_governance_root: str,
    simulation_lab_harness_root: str,
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
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    roi_ref_root = Path(realvideo_roi_to_ocr_reference_root).resolve()
    sub_root = Path(realvideo_gated_submission_root).resolve()
    consumer_root = Path(realvideo_readonly_consumer_root).resolve()
    frame_root = Path(realvideo_frame_sample_root).resolve()
    registry_root = Path(realvideo_case_registry_root).resolve()
    proposal_root = Path(vision_roi_proposal_root).resolve()
    bridge_root = Path(vision_roi_to_ocr_bridge_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    if not _source_ok(roi_ref_root, "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json"):
        errs.append("roi_to_ocr_reference_not_ok")
    if not _source_ok(sub_root, "realvideo_ocr_request_gated_submission_summary.json"):
        errs.append("gated_submission_not_ok")
    if not _source_ok(consumer_root, "realvideo_ocr_evidence_readonly_consumer_summary.json"):
        errs.append("readonly_consumer_not_ok")

    frame_index_doc = _read_json(frame_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json") or {}
    frame_roi_matrix = _read_json(roi_ref_root / "cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix.json") or {}
    ocr_req_matrix = _read_json(roi_ref_root / "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json") or {}
    by_candidate = _read_json(consumer_root / "realvideo_ocr_evidence_by_candidate_index.json") or {}
    by_case_consumer = _read_json(consumer_root / "realvideo_ocr_evidence_by_case_index.json") or {}
    rejected_src = _read_json(sub_root / "realvideo_ocr_request_rejected_roi_guard_report.json") or {}
    consumer_summary = _read_json(consumer_root / "realvideo_ocr_evidence_readonly_consumer_summary.json") or {}

    roi_rows = [r for r in (frame_roi_matrix.get("rows") or []) if isinstance(r, dict)]
    ocr_req_rows = [r for r in (ocr_req_matrix.get("rows") or []) if isinstance(r, dict)]
    entries = [e for e in (by_candidate.get("entries") or []) if isinstance(e, dict)]

    frame_sample_refs = [
        {
            "sample_id": s.get("sample_id"),
            "frame_id": s.get("frame_id"),
            "image_ref": s.get("image_ref"),
        }
        for s in (frame_index_doc.get("samples") or [])
        if isinstance(s, dict)
    ]

    roi_reference_refs = [{"reference_id": r.get("reference_id"), "roi_id": r.get("roi_id"), "roi_type": r.get("roi_type")} for r in roi_rows]
    ocr_request_refs = [
        {"reference_id": r.get("reference_id"), "ocr_request_candidate_id": r.get("ocr_request_candidate_id")}
        for r in ocr_req_rows
    ]

    ocr_submission_refs = [
        {"submission_id": e.get("submission_id"), "ocr_request_candidate_id": e.get("ocr_request_candidate_id")}
        for e in entries
    ]
    ocr_evidence_refs = [
        {
            "ocr_evidence_id": e.get("ocr_evidence_id"),
            "ocr_request_candidate_id": e.get("ocr_request_candidate_id"),
            "bridge_pack_ref": e.get("bridge_pack_ref"),
        }
        for e in entries
    ]

    case_registry_doc = _read_json(registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json") or {}
    case_registry_refs = [
        {"case_id": c.get("case_id"), "case_type": c.get("case_type")}
        for c in (case_registry_doc.get("cases") or [])
        if isinstance(c, dict)
    ]

    empty_count = sum(1 for e in entries if e.get("empty_text"))
    non_empty_count = len(entries) - empty_count
    provider_counter = Counter(str(e.get("provider") or "rapidocr_candidate") for e in entries)

    alignment_rows: List[Dict[str, Any]] = []
    chain_evidence_rows: List[Dict[str, Any]] = []

    for i, ent in enumerate(entries):
        cid = str(ent.get("ocr_request_candidate_id") or "")
        alignment_rows.append(
            {
                "alignment_id": f"align_{cid}",
                "ocr_request_candidate_id": cid,
                "source_frame_id": str(ent.get("source_frame_id") or ""),
                "source_roi_id": str(ent.get("source_roi_id") or ""),
                "roi_type": str(ent.get("roi_type") or ELIGIBLE_ROI_TYPE),
                "submission_id": str(ent.get("submission_id") or ""),
                "ocr_evidence_id": str(ent.get("ocr_evidence_id") or ""),
                "bridge_pack_ref": ent.get("bridge_pack_ref"),
                "provider": str(ent.get("provider") or "rapidocr_candidate"),
                "text_joined": str(ent.get("text_joined") or ""),
                "empty_text": bool(ent.get("empty_text")),
                "alignment_status": "aligned_by_ocr_request_candidate_id",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
        chain_evidence_rows.append(
            {
                "ocr_evidence_id": ent.get("ocr_evidence_id"),
                "ocr_request_candidate_id": cid,
                "source_chain": [
                    str(frame_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json"),
                    str(roi_ref_root / "cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix.json"),
                    str(roi_ref_root / "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json"),
                    str(bridge_root / "vision_roi_to_ocr_request_candidates.json"),
                    str(sub_root / "realvideo_ocr_request_submission_collection.json"),
                    str(consumer_root / "realvideo_ocr_evidence_by_candidate_index.json"),
                    str(out / "realvideo_ocr_updated_reference_candidate.json"),
                ],
            }
        )

    if len(roi_rows) != 50:
        errs.append(f"roi_reference_count:{len(roi_rows)}")
    if len(ocr_req_rows) != 10:
        errs.append(f"ocr_request_ref_count:{len(ocr_req_rows)}")
    if len(entries) != 10:
        errs.append(f"evidence_count:{len(entries)}")

    rejected_roi_refs = [r for r in roi_rows if str(r.get("roi_type")) != ELIGIBLE_ROI_TYPE]

    updated_candidate = {
        "schema_version": CANDIDATE_SCHEMA,
        "reference_scope": "reference_only",
        "frame_sample_refs": frame_sample_refs,
        "roi_reference_refs": roi_reference_refs,
        "ocr_request_refs": ocr_request_refs,
        "ocr_submission_refs": ocr_submission_refs,
        "ocr_evidence_refs": ocr_evidence_refs,
        "case_registry_refs": case_registry_refs,
        "empty_text_guard": {
            "empty_text_is_valid_ocr_result": True,
            "empty_text_is_not_failure": True,
            "empty_text_is_not_no_text_fact": True,
        },
        "reference_status": "updated_with_real_ocr_evidence",
        "fusion_status": "not_fused",
        "semantic_join_allowed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "requires_review": True,
        "prior_roi_to_ocr_reference_ref": str(roi_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_candidate.json"),
    }

    alignment_matrix = {
        "schema_version": ALIGNMENT_SCHEMA,
        "row_count": len(alignment_rows),
        "rows": alignment_rows,
    }

    rejected_preserve = {
        "schema_version": REJECTED_PRESERVE_SCHEMA,
        "total_roi_reference_count": len(roi_rows),
        "selected_upper_sign_roi_count": sum(1 for r in roi_rows if r.get("roi_type") == ELIGIBLE_ROI_TYPE),
        "rejected_roi_count": len(rejected_roi_refs),
        "rejected_roi_refs_preserved": True,
        "rejected_roi_evidence_generated": False,
        "rejected_roi_ref_ids": [r.get("reference_id") for r in rejected_roi_refs],
        "ground_roi_submitted": rejected_src.get("ground_roi_submitted", False),
        "center_roi_submitted": rejected_src.get("center_roi_submitted", False),
        "left_roi_submitted": rejected_src.get("left_roi_submitted", False),
        "right_roi_submitted": rejected_src.get("right_roi_submitted", False),
        "full_frame_ocr_invoked": rejected_src.get("full_frame_ocr_invoked", False),
    }

    empty_guard = {
        "schema_version": EMPTY_GUARD_SCHEMA,
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "empty_text_is_valid_ocr_result": True,
        "empty_text_is_not_failure": True,
        "empty_text_is_not_no_text_fact": True,
        "no_text_fact_written": False,
        "no_scene_delta_from_empty_text": True,
        "no_navigation_decision_from_empty_text": True,
        "future_text_bearing_video_required": non_empty_count == 0,
    }

    # Build roi ref lookup for case mapping
    roi_ref_by_id = {str(r.get("roi_id")): r.get("reference_id") for r in roi_rows if r.get("roi_id")}
    ocr_ref_by_cand = {str(r.get("ocr_request_candidate_id")): r.get("reference_id") for r in ocr_req_rows}

    case_rows: List[Dict[str, Any]] = []
    for row in by_case_consumer.get("cases") or []:
        if not isinstance(row, dict):
            continue
        case_id = str(row.get("case_id") or "")
        sub_refs = row.get("related_submission_refs") if isinstance(row.get("related_submission_refs"), list) else []
        ev_refs = row.get("related_evidence_refs") if isinstance(row.get("related_evidence_refs"), list) else []
        ocr_req_refs_case: List[str] = []
        for s in sub_refs:
            sid = str(s)
            cid = sid[len("sub_") :] if sid.startswith("sub_") else sid
            ref_id = ocr_ref_by_cand.get(cid)
            if ref_id and ref_id not in ocr_req_refs_case:
                ocr_req_refs_case.append(ref_id)
        facility = row.get("requires_future_facility_specific_video") is True
        multi_later = row.get("requires_multi_frame_reference_later") is True
        notes = []
        if facility:
            notes.append("requires_future_facility_specific_video")
        if multi_later:
            notes.append("requires_multi_frame_reference_later")
        if ev_refs and not facility and not multi_later:
            notes.append("ocr_evidence_linked_not_fact_complete")
        case_rows.append(
            {
                "case_id": case_id,
                "case_type": row.get("case_type"),
                "related_roi_refs": list(row.get("mapped_roi_refs") or []) if row.get("mapped_roi_refs") else [],
                "related_ocr_request_refs": ocr_req_refs_case,
                "related_submission_refs": sub_refs,
                "related_evidence_refs": ev_refs,
                "reference_update_status": "updated_parallel_refs",
                "fact_status": "not_fact",
                "write_allowed": False,
                "requires_future_facility_specific_video": facility,
                "requires_multi_frame_reference_later": multi_later,
                "notes": "; ".join(notes) if notes else "reference_only_parallel_update",
            }
        )

    # Enrich text/poster cases with upper_sign roi refs from case mapping in roi ref root
    case_mapping_src = _read_json(roi_ref_root / "cross_modal_vision_ocr_realvideo_case_to_reference_mapping.json") or {}
    case_roi_map = {
        str(c.get("case_id")): c.get("mapped_roi_refs") if isinstance(c.get("mapped_roi_refs"), list) else []
        for c in (case_mapping_src.get("rows") or [])
        if isinstance(c, dict)
    }
    for cr in case_rows:
        if not cr.get("related_roi_refs") and case_roi_map.get(cr["case_id"]):
            cr["related_roi_refs"] = case_roi_map[cr["case_id"]]

    case_mapping_report = {
        "schema_version": CASE_MAPPING_SCHEMA,
        "case_count": len(case_rows),
        "rows": case_rows,
    }

    source_chain = {
        "schema_version": CHAIN_SCHEMA,
        "case_registry_ref": str(registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json"),
        "frame_sample_ref": str(frame_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json"),
        "roi_to_ocr_reference_ref": str(roi_ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_candidate.json"),
        "vision_roi_proposal_ref": str(proposal_root / "vision_roi_proposal_stub.json"),
        "vision_roi_to_ocr_bridge_ref": str(bridge_root / "vision_roi_to_ocr_request_candidates.json"),
        "gated_submission_ref": str(sub_root / "realvideo_ocr_request_submission_collection.json"),
        "readonly_consumer_ref": str(consumer_root / "realvideo_ocr_evidence_by_candidate_index.json"),
        "reference_update_build_step": PHASE_ID,
        "evidence_chain_rows": chain_evidence_rows,
    }

    provider_dist = dict(provider_counter) if provider_counter else {"rapidocr_candidate": len(entries)}

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "realvideo_ocr_reference_update_ready": len(entries) == 10 and not errs,
        "roi_reference_count": len(roi_rows),
        "ocr_request_reference_count": len(ocr_req_rows),
        "ocr_submission_ref_count": len(ocr_submission_refs),
        "ocr_evidence_ref_count": len(ocr_evidence_refs),
        "aligned_ocr_evidence_count": len(alignment_rows),
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "rejected_roi_count": rejected_preserve["rejected_roi_count"],
        "frame_count": len(frame_sample_refs),
        "provider_distribution": provider_dist,
        "ocr_accuracy_computed": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark_link = {
        "schema_version": BENCHMARK_SCHEMA,
        "benchmark_smoke_root": str(bench),
        "benchmark_real_values_smoke_available": bench.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "can_feed_future_t1_collector": True,
        "t2_quality_values_collected": False,
        "ground_truth_available": False,
        "ocr_accuracy_computed": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health_link = {
        "schema_version": HEALTH_SCHEMA,
        "system_health_governance_root": str(health),
        "system_health_governance_available": health.is_dir(),
        "module_health_report_generated": False,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }

    boundary = {
        "schema_version": BOUNDARY_SCHEMA,
        "boundary_ok": True,
        "violations": [],
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "full_frame_ocr_invoked": False,
        "non_text_roi_submitted": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }

    sim_sm = _read_json(sim_root / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sim_sm.get("simulation_output_root") or str(sim_root),
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_realvideo_ocr_generalization_complete": True,
        "not_ocr_accuracy": True,
        "empty_text_not_means_no_text": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "not_fusion": True,
        "not_scene_delta_candidate": True,
        "not_world_model_write_readiness": True,
        "not_navigation": True,
        "not_production_ready": True,
        "not_facility_cases_executed": True,
        "not_duplicate_conflict_resolved": True,
    }

    followups = {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": [
            "RealVideo OCR reference closure",
            "RealVideo text-bearing frame sample later",
            "RealVideo multi-frame duplicate/conflict later",
            "facility-specific real video later",
            "real video quality metrics later",
            "OCR ground truth labeling later",
            "benchmark T2 collector later",
            "provider health runtime later",
            "SystemHealthCenter dry-run later",
            "Scene Delta candidate dry-run later",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "realvideo_ocr_reference_update_executed": True,
        "reference_only_update": True,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "full_frame_ocr_invoked": False,
        "non_text_roi_submitted": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
    }

    phase_hint = "GO" if len(entries) == 10 and len(roi_rows) == 50 and not errs else "CONDITIONAL_GO" if entries and not errs else "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "reference_scope": "reference_only_update",
        "based_on_roi_to_ocr_reference": roi_ref_root.is_dir(),
        "based_on_gated_submission": sub_root.is_dir(),
        "based_on_readonly_consumer": consumer_root.is_dir(),
        "based_on_frame_sample": frame_root.is_dir(),
        "based_on_case_registry": registry_root.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "roi_reference_count": len(roi_rows),
        "ocr_request_reference_count": len(ocr_req_rows),
        "ocr_submission_ref_count": len(ocr_submission_refs),
        "ocr_evidence_ref_count": len(ocr_evidence_refs),
        "aligned_ocr_evidence_count": len(alignment_rows),
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "rejected_roi_count": rejected_preserve["rejected_roi_count"],
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": phase_hint,
        "output_root": str(out),
    }

    return (
        summary,
        updated_candidate,
        alignment_matrix,
        rejected_preserve,
        empty_guard,
        case_mapping_report,
        source_chain,
        metrics,
        benchmark_link,
        health_link,
        boundary,
        sim_report,
        non_claims,
        followups,
        audit,
        errs,
    )
