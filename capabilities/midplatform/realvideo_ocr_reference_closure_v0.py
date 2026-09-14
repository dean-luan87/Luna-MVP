# -*- coding: utf-8 -*-
"""RealVideo OCR reference chain closure (aggregate only; no new capability).

Phase-RealVideo-OCR-Reference-Closure-001
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "RealVideo-OCR-Reference-Closure-001"
ELIGIBLE_ROI_TYPE = "upper_sign_roi"

SUMMARY_SCHEMA = "realvideo_ocr_reference_closure_summary_v0"
PHASE_MATRIX_SCHEMA = "realvideo_ocr_reference_closure_phase_matrix_v0"
LINEAGE_SCHEMA = "realvideo_ocr_reference_lineage_closure_report_v0"
ALIGNMENT_SCHEMA = "realvideo_ocr_reference_alignment_closure_report_v0"
REJECTED_SCHEMA = "realvideo_ocr_reference_rejected_roi_closure_report_v0"
EMPTY_SCHEMA = "realvideo_ocr_reference_empty_text_closure_report_v0"
CASE_SCHEMA = "realvideo_ocr_reference_case_mapping_closure_report_v0"
PROVIDER_SCHEMA = "realvideo_ocr_reference_provider_closure_report_v0"
METRICS_SCHEMA = "realvideo_ocr_reference_metrics_closure_candidate_report_v0"
BENCHMARK_SCHEMA = "realvideo_ocr_reference_closure_benchmark_link_report_v0"
HEALTH_SCHEMA = "realvideo_ocr_reference_closure_system_health_link_report_v0"
BOUNDARY_SCHEMA = "realvideo_ocr_reference_closure_no_write_boundary_report_v0"
SIM_SCHEMA = "realvideo_ocr_reference_closure_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "realvideo_ocr_reference_closure_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "realvideo_ocr_reference_closure_open_followups_v0"
AUDIT_SCHEMA = "realvideo_ocr_reference_closure_audit_v0"

CORE_PHASE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_key": "realvideo_case_registry",
        "phase_name": "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-CaseRegistry-001",
        "summary_file": "cross_modal_vision_ocr_realvideo_case_registry_summary.json",
        "verifier_file": None,
        "source_scope": "realvideo_case_registry",
        "contribution_to_closure": "case_registry_lineage",
        "core": True,
    },
    {
        "phase_key": "realvideo_frame_sample",
        "phase_name": "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-FrameSample-Smoke-001",
        "summary_file": "cross_modal_vision_ocr_realvideo_frame_sample_summary.json",
        "verifier_file": None,
        "source_scope": "realvideo_frame_sample",
        "contribution_to_closure": "frame_sample_lineage",
        "core": True,
    },
    {
        "phase_key": "realvideo_roi_to_ocr_reference",
        "phase_name": "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-ROI-to-OCR-Reference-001",
        "summary_file": "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_summary.json",
        "verifier_file": None,
        "source_scope": "roi_to_ocr_reference_only",
        "contribution_to_closure": "roi_and_ocr_request_reference",
        "core": True,
    },
    {
        "phase_key": "realvideo_ocr_request_gated_submission",
        "phase_name": "CrossModal-Vision-OCR-TestBoard-v1-RealVideo-OCRRequest-Gated-Submission-001",
        "summary_file": "realvideo_ocr_request_gated_submission_summary.json",
        "verifier_file": "realvideo_ocr_request_submission_verifier_report.json",
        "source_scope": "gated_ocr_request_submission",
        "contribution_to_closure": "ocr_submission_evidence_upstream",
        "core": True,
    },
    {
        "phase_key": "realvideo_ocr_evidence_readonly_consumer",
        "phase_name": "RealVideo-OCR-Evidence-ReadOnly-Consumer-001",
        "summary_file": "realvideo_ocr_evidence_readonly_consumer_summary.json",
        "verifier_file": "realvideo_ocr_readonly_verifier_report.json",
        "source_scope": "readonly_consumer",
        "contribution_to_closure": "readonly_consumer_index",
        "core": True,
    },
    {
        "phase_key": "realvideo_ocr_reference_update",
        "phase_name": "RealVideo-OCR-Reference-Update-001",
        "summary_file": "realvideo_ocr_reference_update_summary.json",
        "verifier_file": "realvideo_ocr_reference_update_verifier_report.json",
        "source_scope": "reference_only_update",
        "contribution_to_closure": "parallel_reference_update",
        "core": True,
    },
)

OPTIONAL_PHASE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_key": "vision_roi_proposal",
        "phase_name": "vision_roi_proposal_stub",
        "summary_file": "vision_roi_proposal_stub_summary.json",
        "verifier_file": None,
        "source_scope": "vision_roi_proposal_stub",
        "contribution_to_closure": "supporting_roi_proposal",
        "core": False,
    },
    {
        "phase_key": "vision_roi_to_ocr_bridge",
        "phase_name": "vision_roi_to_ocr_request_bridge",
        "summary_file": "vision_roi_to_ocr_request_bridge_summary.json",
        "verifier_file": None,
        "source_scope": "vision_roi_to_ocr_bridge",
        "contribution_to_closure": "supporting_ocr_request_bridge",
        "core": False,
    },
    {
        "phase_key": "benchmark_real_values_smoke",
        "phase_name": "CrossModal-Vision-OCR-TestBoard-Benchmark-Collector-Real-Values-Smoke-001",
        "summary_file": "cross_modal_vision_ocr_benchmark_real_values_smoke_summary.json",
        "verifier_file": None,
        "source_scope": "benchmark_real_values_smoke",
        "contribution_to_closure": "benchmark_link_context",
        "core": False,
    },
    {
        "phase_key": "system_health_governance",
        "phase_name": "SystemHealthCenter-Governance-001",
        "summary_file": "system_health_center_governance_summary.json",
        "verifier_file": None,
        "source_scope": "system_health_governance_contract",
        "contribution_to_closure": "health_link_context",
        "core": False,
    },
    {
        "phase_key": "simulation_lab_developer_full",
        "phase_name": "Luna-Simulation-Lab-Minimal-Harness-001",
        "summary_file": "simulation_summary.json",
        "verifier_file": None,
        "source_scope": "simulation_context",
        "contribution_to_closure": "simulation_context_attachment",
        "core": False,
    },
)


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _verdict_from_root(root: Path, spec: Dict[str, Any]) -> Tuple[str, List[str]]:
    blockers: List[str] = []
    sm = _read_json(root / str(spec["summary_file"]))
    if not isinstance(sm, dict):
        return "NO_GO", ["missing_summary"]
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    vf = spec.get("verifier_file")
    if vf:
        vr = _read_json(root / vf)
        if isinstance(vr, dict):
            v = str(vr.get("verdict") or "").upper()
            if v not in ("GO", "CONDITIONAL_GO"):
                blockers.extend(list(vr.get("blockers") or []))
                return v or "NO_GO", blockers
            return v, []
        if hint not in ("GO", "CONDITIONAL_GO"):
            blockers.append("missing_verifier_report")
    if hint in ("GO", "CONDITIONAL_GO"):
        return hint, blockers
    blockers.append(f"phase_hint:{hint}")
    return "NO_GO", blockers


def _build_phase_matrix(roots: Dict[str, Path]) -> Tuple[Dict[str, Any], List[str]]:
    rows: List[Dict[str, Any]] = []
    errs: List[str] = []
    for spec in (*CORE_PHASE_SPECS, *OPTIONAL_PHASE_SPECS):
        key = spec["phase_key"]
        root = roots[key]
        verdict, blockers = _verdict_from_root(root, spec)
        sm = _read_json(root / str(spec["summary_file"])) or {}
        ok = verdict in ("GO", "CONDITIONAL_GO") and not blockers
        if spec.get("core") and not ok:
            errs.append(f"phase_not_ok:{spec['phase_name']}")
        rows.append(
            {
                "phase_name": spec["phase_name"],
                "phase_key": key,
                "input_root": str(root),
                "source_status": "ok" if ok else "fail",
                "verifier_verdict": verdict,
                "blockers": blockers,
                "source_scope": spec["source_scope"],
                "fact_status": str(sm.get("fact_status") or "not_fact"),
                "write_status": "no_write",
                "routing_changed": False,
                "contribution_to_closure": spec["contribution_to_closure"],
                "core_phase": bool(spec.get("core")),
            }
        )
    return {"schema_version": PHASE_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}, errs


def run_realvideo_ocr_reference_closure_v0(
    *,
    realvideo_reference_update_root: str,
    realvideo_readonly_consumer_root: str,
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
    List[str],
]:
    errs: List[str] = []
    ref_upd = Path(realvideo_reference_update_root).resolve()
    consumer = Path(realvideo_readonly_consumer_root).resolve()
    gated = Path(realvideo_gated_submission_root).resolve()
    roi_ref = Path(realvideo_roi_to_ocr_reference_root).resolve()
    frame = Path(realvideo_frame_sample_root).resolve()
    registry = Path(realvideo_case_registry_root).resolve()
    proposal = Path(vision_roi_proposal_root).resolve()
    bridge = Path(vision_roi_to_ocr_bridge_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    roots = {
        "realvideo_case_registry": registry,
        "realvideo_frame_sample": frame,
        "realvideo_roi_to_ocr_reference": roi_ref,
        "realvideo_ocr_request_gated_submission": gated,
        "realvideo_ocr_evidence_readonly_consumer": consumer,
        "realvideo_ocr_reference_update": ref_upd,
        "vision_roi_proposal": proposal,
        "vision_roi_to_ocr_bridge": bridge,
        "benchmark_real_values_smoke": bench,
        "system_health_governance": health,
        "simulation_lab_developer_full": sim,
    }

    phase_matrix, phase_errs = _build_phase_matrix(roots)
    errs.extend(phase_errs)

    ref_summary = _read_json(ref_upd / "realvideo_ocr_reference_update_summary.json") or {}
    alignment_upd = _read_json(ref_upd / "realvideo_ocr_reference_update_alignment_matrix.json") or {}
    rejected_upd = _read_json(ref_upd / "realvideo_ocr_reference_update_rejected_roi_preservation_report.json") or {}
    empty_upd = _read_json(ref_upd / "realvideo_ocr_reference_update_empty_text_guard_report.json") or {}
    case_upd = _read_json(ref_upd / "realvideo_ocr_reference_update_case_mapping_report.json") or {}
    gated_summary = _read_json(gated / "realvideo_ocr_request_gated_submission_summary.json") or {}

    by_candidate = _read_json(consumer / "realvideo_ocr_evidence_by_candidate_index.json") or {}
    entries = [e for e in (by_candidate.get("entries") or []) if isinstance(e, dict)]
    ocr_req_matrix = _read_json(roi_ref / "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json") or {}
    roi_matrix = _read_json(roi_ref / "cross_modal_vision_ocr_realvideo_frame_to_roi_reference_matrix.json") or {}
    frame_index = _read_json(frame / "cross_modal_vision_ocr_realvideo_frame_sample_index.json") or {}

    ocr_req_rows = [r for r in (ocr_req_matrix.get("rows") or []) if isinstance(r, dict)]
    roi_rows = [r for r in (roi_matrix.get("rows") or []) if isinstance(r, dict)]

    ocr_ref_by_cand = {str(r.get("ocr_request_candidate_id")): r.get("reference_id") for r in ocr_req_rows}
    roi_ref_by_roi_id = {str(r.get("roi_id")): r.get("reference_id") for r in roi_rows}
    frame_ref_by_frame_id = {
        str(s.get("frame_id")): s.get("sample_id")
        for s in (frame_index.get("samples") or [])
        if isinstance(s, dict)
    }

    case_count = int(ref_summary.get("based_on_case_registry") and len(case_upd.get("rows") or []) or 0)
    case_count = len(case_upd.get("rows") or []) if case_upd else 16
    frame_sample_count = len(frame_index.get("samples") or [])
    roi_count = int(ref_summary.get("roi_reference_count") or len(roi_rows))
    ocr_req_count = int(ref_summary.get("ocr_request_reference_count") or len(ocr_req_rows))
    sub_count = int(ref_summary.get("ocr_submission_ref_count") or len(entries))
    ev_count = int(ref_summary.get("ocr_evidence_ref_count") or len(entries))
    aligned = int(ref_summary.get("aligned_ocr_evidence_count") or alignment_upd.get("row_count") or 0)
    empty_count = int(ref_summary.get("empty_text_count") or 0)
    non_empty_count = int(ref_summary.get("non_empty_text_count") or 0)
    rejected_count = int(ref_summary.get("rejected_roi_count") or rejected_upd.get("rejected_roi_count") or 0)

    if roi_count != 50 or ocr_req_count != 10 or ev_count != 10 or aligned != 10:
        errs.append("ref_counts_mismatch")

    lineage_path = out / "realvideo_ocr_reference_lineage_closure_report.json"
    closure_ref = str(lineage_path)

    registry_ref = str(registry / "cross_modal_vision_ocr_realvideo_case_registry.json")
    frame_index_ref = str(frame / "cross_modal_vision_ocr_realvideo_frame_sample_index.json")
    roi_candidate_ref = str(roi_ref / "cross_modal_vision_ocr_realvideo_roi_to_ocr_reference_candidate.json")
    ocr_req_matrix_ref = str(roi_ref / "cross_modal_vision_ocr_realvideo_ocr_request_reference_matrix.json")
    submission_coll_ref = str(gated / "realvideo_ocr_request_submission_collection.json")
    consumer_idx_ref = str(consumer / "realvideo_ocr_evidence_by_candidate_index.json")
    ref_upd_candidate_ref = str(ref_upd / "realvideo_ocr_updated_reference_candidate.json")

    evidence_lineage: List[Dict[str, Any]] = []
    for ent in entries:
        cid = str(ent.get("ocr_request_candidate_id") or "")
        fid = str(ent.get("source_frame_id") or "")
        rid = str(ent.get("source_roi_id") or "")
        steps = [
            "case_registry",
            "frame_sample",
            "roi_reference",
            "ocr_request_candidate",
            "gated_submission",
            "ocr_evidence",
            "readonly_consumer",
            "reference_update",
            "reference_closure",
        ]
        evidence_lineage.append(
            {
                "ocr_evidence_id": ent.get("ocr_evidence_id"),
                "ocr_request_candidate_id": cid,
                "case_registry_ref": registry_ref,
                "frame_sample_ref": frame_index_ref,
                "frame_sample_id": frame_ref_by_frame_id.get(fid),
                "roi_reference_ref": roi_candidate_ref,
                "roi_reference_id": roi_ref_by_roi_id.get(rid),
                "ocr_request_ref": ocr_req_matrix_ref,
                "ocr_request_reference_id": ocr_ref_by_cand.get(cid),
                "submission_ref": submission_coll_ref,
                "submission_id": ent.get("submission_id"),
                "ocr_evidence_ref": consumer_idx_ref,
                "readonly_consumer_ref": consumer_idx_ref,
                "reference_update_ref": ref_upd_candidate_ref,
                "final_closure_ref": closure_ref,
                "source_chain_steps": steps,
                "source_chain_step_count": len(steps),
            }
        )

    lineage = {
        "schema_version": LINEAGE_SCHEMA,
        "main_chain": [
            "case_registry",
            "frame_sample",
            "roi_reference",
            "ocr_request_candidate",
            "gated_submission",
            "ocr_evidence",
            "readonly_consumer",
            "reference_update",
            "reference_closure",
        ],
        "evidence_lineage_count": len(evidence_lineage),
        "evidence_lineage_rows": evidence_lineage,
    }

    align_rows = alignment_upd.get("rows") or []
    alignment_closure = {
        "schema_version": ALIGNMENT_SCHEMA,
        "aligned_ocr_evidence_count": aligned,
        "alignment_strategy": "aligned_by_ocr_request_candidate_id",
        "all_ocr_requests_aligned": aligned == 10 and all(
            r.get("alignment_status") == "aligned_by_ocr_request_candidate_id" for r in align_rows if isinstance(r, dict)
        ),
        "selected_roi_type": ELIGIBLE_ROI_TYPE,
        "accuracy_computed": False,
        "ground_truth_available": False,
        "empty_text_allowed": True,
        "empty_text_not_failure": True,
        "empty_text_not_no_text_fact": True,
        "non_empty_text_not_accuracy": True,
        "source_alignment_matrix_ref": str(ref_upd / "realvideo_ocr_reference_update_alignment_matrix.json"),
    }

    rejected_closure = {
        "schema_version": REJECTED_SCHEMA,
        "total_roi_reference_count": rejected_upd.get("total_roi_reference_count", roi_count),
        "selected_upper_sign_roi_count": rejected_upd.get("selected_upper_sign_roi_count", 10),
        "rejected_roi_count": rejected_count,
        "rejected_roi_refs_preserved": rejected_upd.get("rejected_roi_refs_preserved", True),
        "rejected_roi_evidence_generated": rejected_upd.get("rejected_roi_evidence_generated", False),
        "ground_roi_submitted": rejected_upd.get("ground_roi_submitted", False),
        "center_roi_submitted": rejected_upd.get("center_roi_submitted", False),
        "left_roi_submitted": rejected_upd.get("left_roi_submitted", False),
        "right_roi_submitted": rejected_upd.get("right_roi_submitted", False),
        "non_text_roi_submission_count": gated_summary.get("non_text_roi_submission_count", 0),
        "full_frame_ocr_invoked": rejected_upd.get("full_frame_ocr_invoked", False),
    }

    empty_closure = {
        "schema_version": EMPTY_SCHEMA,
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "empty_text_is_valid_ocr_result": empty_upd.get("empty_text_is_valid_ocr_result", True),
        "empty_text_is_not_failure": empty_upd.get("empty_text_is_not_failure", True),
        "empty_text_is_not_no_text_fact": empty_upd.get("empty_text_is_not_no_text_fact", True),
        "no_text_fact_written": empty_upd.get("no_text_fact_written", False),
        "no_scene_delta_from_empty_text": empty_upd.get("no_scene_delta_from_empty_text", True),
        "no_world_model_write_from_empty_text": True,
        "no_navigation_decision_from_empty_text": empty_upd.get("no_navigation_decision_from_empty_text", True),
        "future_text_bearing_video_required": empty_upd.get("future_text_bearing_video_required", non_empty_count == 0),
    }

    provider_counter = Counter(str(e.get("provider") or "rapidocr_candidate") for e in entries)
    provider_dist = dict(provider_counter) if provider_counter else {"rapidocr_candidate": len(entries)}

    case_closure_rows: List[Dict[str, Any]] = []
    for row in case_upd.get("rows") or []:
        if not isinstance(row, dict):
            continue
        facility = row.get("requires_future_facility_specific_video") is True
        multi_later = row.get("requires_multi_frame_reference_later") is True
        if facility:
            closure_status = "deferred_requires_future_facility_specific_video"
            notes = "facility case deferred; no fact or navigation"
        elif multi_later:
            closure_status = "deferred_requires_multi_frame_reference_later"
            notes = "duplicate/conflict deferred; multi-frame reference later"
        else:
            closure_status = "reference_closed_not_fact"
            notes = row.get("notes") or "reference chain closed; not fact_complete"
        case_closure_rows.append(
            {
                "case_id": row.get("case_id"),
                "case_type": row.get("case_type"),
                "related_roi_refs": row.get("related_roi_refs") or [],
                "related_ocr_request_refs": row.get("related_ocr_request_refs") or [],
                "related_submission_refs": row.get("related_submission_refs") or [],
                "related_evidence_refs": row.get("related_evidence_refs") or [],
                "closure_status": closure_status,
                "fact_status": "not_fact",
                "write_allowed": False,
                "fact_complete": False,
                "navigation_ready": False,
                "notes": notes,
            }
        )

    case_mapping_closure = {
        "schema_version": CASE_SCHEMA,
        "case_count": len(case_closure_rows),
        "rows": case_closure_rows,
    }

    provider_closure = {
        "schema_version": PROVIDER_SCHEMA,
        "provider_distribution": provider_dist,
        "real_ocr_invoked_upstream": gated_summary.get("real_ocr_invoked", True),
        "rapidocr_invoked_upstream": gated_summary.get("rapidocr_invoked", True),
        "rapidocr_reinvoked_in_this_phase": False,
        "paddleocr_invoked": False,
        "direct_provider_bypass": gated_summary.get("direct_provider_bypass", False),
        "mock_text_substitution": False,
        "provider_health_runtime_checked": False,
        "provider_comparison_claimed": False,
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "realvideo_ocr_reference_closure_ready": not bool(errs),
        "case_count": len(case_closure_rows),
        "frame_sample_count": frame_sample_count,
        "roi_reference_count": roi_count,
        "ocr_request_reference_count": ocr_req_count,
        "ocr_submission_ref_count": sub_count,
        "ocr_evidence_ref_count": ev_count,
        "aligned_ocr_evidence_count": aligned,
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "rejected_roi_count": rejected_count,
        "provider_distribution": provider_dist,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
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

    sim_sm = _read_json(sim / "simulation_summary.json") or {}
    sim_report = {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sim_sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sim_sm.get("simulation_output_root") or str(sim),
        "run_model": sim_sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }

    non_claims = {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_fusion": True,
        "not_realvideo_ocr_generalization_complete": True,
        "not_ocr_accuracy": True,
        "empty_text_not_means_no_text": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
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
            "RealVideo text-bearing frame sample later",
            "RealVideo multi-frame duplicate/conflict later",
            "facility-specific real video later",
            "real video quality metrics later",
            "OCR ground truth labeling later",
            "benchmark T2 collector later",
            "provider health runtime later",
            "SystemHealthCenter dry-run later",
            "Scene Delta candidate dry-run later",
            "RealVideo OCR fusion candidate dry-run later",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "realvideo_ocr_reference_closure_executed": True,
        "closure_only": True,
        "no_new_capability_added": True,
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

    phase_hint = "NO_GO" if errs else "GO"
    if not errs and empty_count == 10 and non_empty_count == 0:
        phase_hint = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "closure_scope": "reference_chain_closure_only",
        "realvideo_ocr_reference_status": "closed_for_reference_evaluation",
        "based_on_case_registry": registry.is_dir(),
        "based_on_frame_sample": frame.is_dir(),
        "based_on_roi_to_ocr_reference": roi_ref.is_dir(),
        "based_on_gated_submission": gated.is_dir(),
        "based_on_readonly_consumer": consumer.is_dir(),
        "based_on_reference_update": ref_upd.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim.is_dir(),
        "case_count": len(case_closure_rows),
        "frame_sample_count": frame_sample_count,
        "roi_reference_count": roi_count,
        "ocr_request_reference_count": ocr_req_count,
        "ocr_submission_ref_count": sub_count,
        "ocr_evidence_ref_count": ev_count,
        "aligned_ocr_evidence_count": aligned,
        "empty_text_count": empty_count,
        "non_empty_text_count": non_empty_count,
        "rejected_roi_count": rejected_count,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
        "scene_delta_candidate_generated": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": phase_hint,
        "output_root": str(out),
    }

    return (
        summary,
        phase_matrix,
        lineage,
        alignment_closure,
        rejected_closure,
        empty_closure,
        case_mapping_closure,
        provider_closure,
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
