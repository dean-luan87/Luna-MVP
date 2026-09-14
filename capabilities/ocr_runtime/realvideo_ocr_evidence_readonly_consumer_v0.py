# -*- coding: utf-8 -*-
"""Read-only consumer for RealVideo OCR evidence collection.

Phase-RealVideo-OCR-Evidence-ReadOnly-Consumer-001
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "RealVideo-OCR-Evidence-ReadOnly-Consumer-001"
ELIGIBLE_ROI_TYPE = "upper_sign_roi"

SUMMARY_SCHEMA = "realvideo_ocr_evidence_readonly_consumer_summary_v0"
BY_CANDIDATE_SCHEMA = "realvideo_ocr_evidence_by_candidate_index_v0"
BY_FRAME_SCHEMA = "realvideo_ocr_evidence_by_frame_index_v0"
BY_ROI_SCHEMA = "realvideo_ocr_evidence_by_roi_index_v0"
BY_CASE_SCHEMA = "realvideo_ocr_evidence_by_case_index_v0"
EMPTY_GUARD_SCHEMA = "realvideo_ocr_empty_text_interpretation_guard_report_v0"
REJECTED_CARRYOVER_SCHEMA = "realvideo_ocr_readonly_rejected_roi_carryover_report_v0"
PROVIDER_SUMMARY_SCHEMA = "realvideo_ocr_readonly_provider_summary_report_v0"
CHAIN_SCHEMA = "realvideo_ocr_readonly_source_chain_report_v0"
METRICS_SCHEMA = "realvideo_ocr_readonly_metrics_candidate_report_v0"
BENCHMARK_SCHEMA = "realvideo_ocr_readonly_benchmark_link_report_v0"
HEALTH_SCHEMA = "realvideo_ocr_readonly_system_health_link_report_v0"
BOUNDARY_SCHEMA = "realvideo_ocr_readonly_no_write_boundary_report_v0"
SIM_SCHEMA = "realvideo_ocr_readonly_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "realvideo_ocr_readonly_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "realvideo_ocr_readonly_open_followups_v0"
AUDIT_SCHEMA = "realvideo_ocr_readonly_audit_v0"


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


def _evidence_id_for(candidate_id: str, ocr_evidence: Dict[str, Any]) -> str:
    req_id = str(ocr_evidence.get("request_id") or "")
    if req_id:
        return f"ev_rv_{req_id}"
    return f"ev_rv_{candidate_id}"


def run_realvideo_ocr_evidence_readonly_consumer_v0(
    *,
    realvideo_gated_submission_root: str,
    realvideo_roi_to_ocr_reference_root: str,
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
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    sub_root = Path(realvideo_gated_submission_root).resolve()
    ref_root = Path(realvideo_roi_to_ocr_reference_root).resolve()
    frame_root = Path(realvideo_frame_sample_root).resolve()
    registry_root = Path(realvideo_case_registry_root).resolve()
    proposal_root = Path(vision_roi_proposal_root).resolve()
    bridge_root = Path(vision_roi_to_ocr_bridge_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    if not _source_ok(sub_root, "realvideo_ocr_request_gated_submission_summary.json"):
        errs.append("gated_submission_not_ok")

    sub_summary = _read_json(sub_root / "realvideo_ocr_request_gated_submission_summary.json") or {}
    collection = _read_json(sub_root / "realvideo_ocr_request_submission_collection.json") or {}
    case_mapping_src = _read_json(sub_root / "realvideo_ocr_request_submission_case_mapping_report.json") or {}
    rejected_src = _read_json(sub_root / "realvideo_ocr_request_rejected_roi_guard_report.json") or {}
    ocr_ref_matrix = _read_json(ref_root / "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json") or {}

    ocr_results = [r for r in (collection.get("ocr_results") or []) if isinstance(r, dict)]
    success_results = [r for r in ocr_results if r.get("submission_status") == "success"]

    ref_by_cand = {
        str(r.get("ocr_request_candidate_id")): r
        for r in (ocr_ref_matrix.get("rows") or [])
        if isinstance(r, dict) and r.get("ocr_request_candidate_id")
    }

    candidate_entries: List[Dict[str, Any]] = []
    provider_counter: Counter[str] = Counter()
    empty_count = 0
    non_empty_count = 0
    evidence_traces: List[Dict[str, Any]] = []

    for res in success_results:
        cid = str(res.get("ocr_request_candidate_id") or "")
        ref = ref_by_cand.get(cid, {})
        ocr_ev = res.get("ocr_evidence") if isinstance(res.get("ocr_evidence"), dict) else {}
        eid = _evidence_id_for(cid, ocr_ev)
        tj = str(res.get("text_joined") or ocr_ev.get("text_joined") or "")
        items = ocr_ev.get("text_items") if isinstance(ocr_ev.get("text_items"), list) else []
        empty = res.get("empty_text")
        if empty is None:
            empty = not str(tj).strip() and not items
        empty = bool(empty)
        if empty:
            empty_count += 1
        else:
            non_empty_count += 1
        provider = str(ocr_ev.get("provider") or "rapidocr_candidate")
        provider_counter[provider] += 1

        source_chain = [
            "realvideo_frame_sample",
            "realvideo_roi_to_ocr_reference",
            "vision_roi_proposal",
            "vision_roi_to_ocr_bridge",
            "realvideo_ocr_request_gated_submission",
            "realvideo_ocr_evidence_readonly_consumer",
        ]

        entry = {
            "ocr_request_candidate_id": cid,
            "submission_id": str(res.get("submission_id") or f"sub_{cid}"),
            "ocr_evidence_id": eid,
            "source_frame_id": str(res.get("source_frame_id") or ""),
            "source_roi_id": str(res.get("source_roi_id") or ref.get("source_roi_id") or ""),
            "roi_type": str(ref.get("roi_type") or ELIGIBLE_ROI_TYPE),
            "provider": provider,
            "text_joined": tj,
            "text_items": items,
            "empty_text": empty,
            "bridge_pack_ref": res.get("bridge_pack_ref"),
            "fact_status": "not_fact",
            "write_allowed": False,
            "source_chain": source_chain,
        }
        candidate_entries.append(entry)
        evidence_traces.append(
            {
                "ocr_evidence_id": eid,
                "ocr_request_candidate_id": cid,
                "submission_id": entry["submission_id"],
                "source_frame_id": entry["source_frame_id"],
                "source_roi_id": entry["source_roi_id"],
                "frame_sample_ref": str(frame_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json"),
                "roi_reference_ref": str(ref.get("reference_id") or ""),
                "bridge_pack_ref": entry["bridge_pack_ref"],
            }
        )

    if len(candidate_entries) != 10:
        errs.append(f"candidate_index_count:{len(candidate_entries)}")

    by_candidate = {
        "schema_version": BY_CANDIDATE_SCHEMA,
        "index_count": len(candidate_entries),
        "entries": candidate_entries,
    }

    by_frame_map: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "evidence_refs": [],
            "roi_refs": [],
            "submission_refs": [],
            "empty_text_count": 0,
            "non_empty_text_count": 0,
        }
    )
    for ent in candidate_entries:
        fid = ent["source_frame_id"]
        by_frame_map[fid]["source_frame_id"] = fid
        by_frame_map[fid]["evidence_refs"].append(ent["ocr_evidence_id"])
        by_frame_map[fid]["roi_refs"].append(ent["source_roi_id"])
        by_frame_map[fid]["submission_refs"].append(ent["submission_id"])
        if ent["empty_text"]:
            by_frame_map[fid]["empty_text_count"] += 1
        else:
            by_frame_map[fid]["non_empty_text_count"] += 1

    frames = []
    for fid in sorted(by_frame_map.keys()):
        fm = by_frame_map[fid]
        frames.append(
            {
                "source_frame_id": fid,
                "evidence_refs": fm["evidence_refs"],
                "roi_refs": fm["roi_refs"],
                "submission_refs": fm["submission_refs"],
                "empty_text_count": fm["empty_text_count"],
                "non_empty_text_count": fm["non_empty_text_count"],
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    by_frame = {
        "schema_version": BY_FRAME_SCHEMA,
        "frame_count": len(frames),
        "frames": frames,
    }

    rois = []
    for ent in candidate_entries:
        rois.append(
            {
                "source_roi_id": ent["source_roi_id"],
                "source_frame_id": ent["source_frame_id"],
                "roi_type": ent["roi_type"],
                "ocr_evidence_ref": ent["ocr_evidence_id"],
                "submission_ref": ent["submission_id"],
                "text_joined": ent["text_joined"],
                "empty_text": ent["empty_text"],
                "provider": ent["provider"],
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    by_roi = {
        "schema_version": BY_ROI_SCHEMA,
        "roi_count": len(rois),
        "rois": rois,
    }

    sub_to_evidence = {ent["submission_id"]: ent["ocr_evidence_id"] for ent in candidate_entries}
    case_rows: List[Dict[str, Any]] = []
    for row in case_mapping_src.get("rows") or []:
        if not isinstance(row, dict):
            continue
        case_id = str(row.get("case_id") or "")
        sub_refs = row.get("submission_refs") if isinstance(row.get("submission_refs"), list) else []
        ev_refs = [sub_to_evidence[s] for s in sub_refs if s in sub_to_evidence]
        facility = row.get("requires_future_facility_specific_video") is True
        multi_later = row.get("requires_multi_frame_reference_later") is True
        notes = []
        if facility:
            notes.append("requires_future_facility_specific_video")
        if multi_later:
            notes.append("requires_multi_frame_reference_later")
        if not ev_refs and not facility and not multi_later:
            notes.append("no_submission_refs_in_this_phase")
        case_rows.append(
            {
                "case_id": case_id,
                "case_type": row.get("case_type"),
                "related_submission_refs": sub_refs,
                "related_evidence_refs": ev_refs,
                "evidence_available": len(ev_refs) > 0,
                "execution_status": row.get("execution_status"),
                "fact_status": "not_fact",
                "write_allowed": False,
                "requires_future_facility_specific_video": facility,
                "requires_multi_frame_reference_later": multi_later,
                "notes": "; ".join(notes) if notes else "readonly_index_only_not_fact_complete",
            }
        )

    by_case = {
        "schema_version": BY_CASE_SCHEMA,
        "case_count": len(case_rows),
        "cases": case_rows,
    }

    empty_guard = {
        "schema_version": EMPTY_GUARD_SCHEMA,
        "empty_text_count": empty_count,
        "empty_text_is_valid_ocr_result": True,
        "empty_text_is_not_failure": True,
        "empty_text_is_not_no_text_fact": True,
        "no_text_fact_written": False,
        "no_navigation_decision_from_empty_text": True,
        "requires_better_roi_or_text_bearing_video_for_non_empty_validation": non_empty_count == 0,
    }

    rejected_carryover = {
        "schema_version": REJECTED_CARRYOVER_SCHEMA,
        "total_roi_reference_count": rejected_src.get("total_roi_reference_count", 50),
        "selected_upper_sign_roi_count": rejected_src.get("selected_upper_sign_roi_count", 10),
        "rejected_roi_count": rejected_src.get("rejected_roi_count", 40),
        "ground_roi_submitted": rejected_src.get("ground_roi_submitted", False),
        "center_roi_submitted": rejected_src.get("center_roi_submitted", False),
        "left_roi_submitted": rejected_src.get("left_roi_submitted", False),
        "right_roi_submitted": rejected_src.get("right_roi_submitted", False),
        "non_text_roi_submission_count": sub_summary.get("non_text_roi_submission_count", 0),
        "full_frame_ocr_invoked": rejected_src.get("full_frame_ocr_invoked", False),
    }

    provider_summary = {
        "schema_version": PROVIDER_SUMMARY_SCHEMA,
        "provider_distribution": dict(provider_counter) if provider_counter else {"rapidocr_candidate": len(candidate_entries)},
        "real_ocr_invoked_upstream": sub_summary.get("real_ocr_invoked", False) is True,
        "rapidocr_invoked_upstream": sub_summary.get("rapidocr_invoked", False) is True,
        "rapidocr_reinvoked_in_this_phase": False,
        "paddleocr_invoked": False,
        "direct_provider_bypass": False,
        "mock_text_substitution": False,
        "provider_health_runtime_checked": False,
    }

    source_chain = {
        "schema_version": CHAIN_SCHEMA,
        "case_registry_ref": str(registry_root / "cross_modal_vision_ocr_realvideo_case_registry.json"),
        "frame_sample_ref": str(frame_root / "cross_modal_vision_ocr_realvideo_frame_sample_index.json"),
        "roi_to_ocr_reference_ref": str(ref_root / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_candidate.json"),
        "vision_roi_proposal_ref": str(proposal_root / "vision_roi_proposal_stub.json"),
        "vision_roi_to_ocr_bridge_ref": str(bridge_root / "vision_roi_to_ocr_request_candidates.json"),
        "gated_submission_ref": str(sub_root / "realvideo_ocr_request_submission_collection.json"),
        "readonly_consumer_build_step": PHASE_ID,
        "evidence_traces": evidence_traces,
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "realvideo_ocr_readonly_consumer_ready": len(candidate_entries) > 0 and not errs,
        "submission_count": collection.get("submission_count", len(ocr_results)),
        "success_count": collection.get("success_count", len(success_results)),
        "failed_count": collection.get("failed_count", 0),
        "evidence_count": len(candidate_entries),
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "rejected_roi_count": rejected_carryover["rejected_roi_count"],
        "frame_count": len(frames),
        "roi_count": len(rois),
        "provider_distribution": dict(provider_counter) if provider_counter else {"rapidocr_candidate": len(candidate_entries)},
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
            "RealVideo OCR reference update",
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
        "realvideo_ocr_evidence_readonly_consumer_executed": True,
        "readonly_consumer": True,
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

    provider_dist = dict(provider_counter) if provider_counter else {"rapidocr_candidate": len(candidate_entries)}
    phase_hint = "GO" if len(candidate_entries) == 10 and not errs else "CONDITIONAL_GO" if candidate_entries and not errs else "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "consumer_scope": "readonly_consumer",
        "based_on_gated_submission": sub_root.is_dir(),
        "based_on_roi_to_ocr_reference": ref_root.is_dir(),
        "based_on_frame_sample": frame_root.is_dir(),
        "based_on_case_registry": registry_root.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "submission_count_observed": len(ocr_results),
        "success_count_observed": len(success_results),
        "failed_count_observed": collection.get("failed_count", 0),
        "evidence_count_observed": len(candidate_entries),
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "provider_distribution": provider_dist,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
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
        by_candidate,
        by_frame,
        by_roi,
        by_case,
        empty_guard,
        rejected_carryover,
        provider_summary,
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
