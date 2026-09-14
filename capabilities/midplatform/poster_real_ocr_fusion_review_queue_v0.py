# -*- coding: utf-8 -*-
"""Poster Real OCR fusion review queue (pending only; no approval).

Phase-Poster-Real-OCR-Fusion-Review-Queue-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "Poster-Real-OCR-Fusion-Review-Queue-001"

SUMMARY_SCHEMA = "poster_real_ocr_fusion_review_queue_summary_v0"
QUEUE_CANDIDATE_SCHEMA = "poster_real_ocr_fusion_review_queue_candidate_v0"
QUEUE_MATRIX_SCHEMA = "poster_real_ocr_fusion_review_queue_matrix_v0"
RISK_SCHEMA = "poster_real_ocr_fusion_review_risk_inheritance_report_v0"
POLICY_SCHEMA = "poster_real_ocr_fusion_review_policy_report_v0"
DECISION_SCHEMA = "poster_real_ocr_fusion_review_decision_placeholder_report_v0"
CHAIN_SCHEMA = "poster_real_ocr_fusion_review_source_chain_report_v0"
METRICS_SCHEMA = "poster_real_ocr_fusion_review_metrics_candidate_report_v0"
BENCHMARK_SCHEMA = "poster_real_ocr_fusion_review_benchmark_link_report_v0"
HEALTH_SCHEMA = "poster_real_ocr_fusion_review_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_fusion_review_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_fusion_review_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_fusion_review_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "poster_real_ocr_fusion_review_open_followups_v0"
AUDIT_SCHEMA = "poster_real_ocr_fusion_review_audit_v0"

ALLOWED_NEXT_STEPS = (
    "ttl_gate_later",
    "policy_gate_later",
    "scene_delta_candidate_later",
)
FORBIDDEN_NEXT_STEPS = (
    "world_model_write",
    "scene_delta_write",
    "navigation_decision",
    "auto_approve",
)


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


def run_poster_real_ocr_fusion_review_queue_v0(
    *,
    poster_real_ocr_fusion_candidate_dryrun_root: str,
    poster_real_ocr_reference_closure_root: str,
    poster_real_ocr_reference_update_root: str,
    poster_real_ocr_readonly_consumer_root: str,
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
    dryrun = Path(poster_real_ocr_fusion_candidate_dryrun_root).resolve()
    closure = Path(poster_real_ocr_reference_closure_root).resolve()
    ref_upd = Path(poster_real_ocr_reference_update_root).resolve()
    consumer = Path(poster_real_ocr_readonly_consumer_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    if not _source_ok(dryrun, "poster_real_ocr_fusion_candidate_dryrun_summary.json"):
        errs.append("fusion_dryrun_not_ok")

    fusion_candidate = _read_json(dryrun / "poster_real_ocr_fusion_candidate.json") or {}
    dryrun_summary = _read_json(dryrun / "poster_real_ocr_fusion_candidate_dryrun_summary.json") or {}
    ttl_fusion = _read_json(dryrun / "poster_real_ocr_fusion_ttl_commercial_risk_report.json") or {}
    reading_fusion = _read_json(dryrun / "poster_real_ocr_fusion_reading_order_guard.json") or {}
    review_req = _read_json(dryrun / "poster_real_ocr_fusion_review_requirement_report.json") or {}
    visual_matrix = _read_json(dryrun / "poster_real_ocr_fusion_visual_context_matrix.json") or {}

    if not dryrun_summary.get("fusion_candidate_generated"):
        errs.append("fusion_candidate_not_generated")

    source_candidate_id = f"pfc_{fusion_candidate.get('candidate_type', 'poster')}_{uuid.uuid4().hex[:8]}"
    queue_item_id = f"queue_{source_candidate_id}"
    fusion_candidate_ref = str(dryrun / "poster_real_ocr_fusion_candidate.json")

    queue_candidate = {
        "schema_version": QUEUE_CANDIDATE_SCHEMA,
        "queue_scope": "review_queue_only",
        "queue_item_id": queue_item_id,
        "source_fusion_candidate_id": source_candidate_id,
        "source_fusion_candidate_ref": fusion_candidate_ref,
        "review_status": "pending_review",
        "approval_status": "not_approved",
        "auto_approve_allowed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "requires_human_or_policy_review": True,
        "requires_ttl_gate": bool(review_req.get("ttl_gate_required", True)),
        "requires_policy_gate": bool(review_req.get("policy_gate_required", True)),
        "allowed_next_steps": list(ALLOWED_NEXT_STEPS),
        "forbidden_next_steps": list(FORBIDDEN_NEXT_STEPS),
        "candidate_type": fusion_candidate.get("candidate_type"),
        "candidate_scope": fusion_candidate.get("candidate_scope"),
    }

    vis_rows = visual_matrix.get("rows") if isinstance(visual_matrix.get("rows"), list) else []
    visual_consumed = any(
        isinstance(v, dict) and v.get("consumed_as_text") is True for v in vis_rows
    )

    queue_matrix = {
        "schema_version": QUEUE_MATRIX_SCHEMA,
        "row_count": 1,
        "rows": [
            {
                "queue_item_id": queue_item_id,
                "source_candidate_id": source_candidate_id,
                "candidate_type": fusion_candidate.get("candidate_type"),
                "candidate_scope": fusion_candidate.get("candidate_scope"),
                "review_status": "pending_review",
                "approval_status": "not_approved",
                "auto_approve_allowed": False,
                "requires_review": True,
                "requires_ttl_gate": bool(review_req.get("ttl_gate_required", True)),
                "requires_policy_gate": bool(review_req.get("policy_gate_required", True)),
                "fact_status": "not_fact",
                "write_allowed": False,
                "scene_delta_candidate_allowed": False,
            }
        ],
    }

    risk_inheritance = {
        "schema_version": RISK_SCHEMA,
        "commercial_claim_status": str(ttl_fusion.get("commercial_claim_status") or "candidate_only"),
        "temporal_claim_status": str(ttl_fusion.get("temporal_claim_status") or "candidate_only"),
        "ttl_required_region_count": int(ttl_fusion.get("ttl_required_region_count") or 2),
        "reading_order_confidence": str(reading_fusion.get("reading_order_confidence") or "low"),
        "brand_identity_confirmed": False,
        "qr_decoded": False,
        "visual_context_consumed_as_text": bool(visual_consumed),
        "review_required_before_any_fact": True,
        "world_model_write_allowed": False,
        "inherited_from_fusion_dryrun": True,
        "source_ttl_report_ref": str(dryrun / "poster_real_ocr_fusion_ttl_commercial_risk_report.json"),
    }

    policy_report = {
        "schema_version": POLICY_SCHEMA,
        "all_candidates_pending_review": True,
        "approval_status_unchanged": True,
        "auto_approve_allowed": False,
        "auto_approve_invoked": False,
        "write_actions_forbidden": True,
        "scene_delta_candidate_forbidden_in_this_phase": True,
        "human_or_policy_gate_required": True,
        "ttl_gate_required": True,
        "policy_gate_required": True,
        "next_possible_phase": "Poster-Real-OCR-Fusion-TTL-Gate-DryRun-001",
        "alternate_next_possible_phase": "Poster-Real-OCR-Fusion-Policy-Gate-DryRun-001",
    }

    decision_placeholder = {
        "schema_version": DECISION_SCHEMA,
        "decision_status": "not_evaluated",
        "reviewer_type": None,
        "review_decision": None,
        "approval_granted": False,
        "rejection_granted": False,
        "hold_for_review": True,
        "decision_reason_codes": [],
        "decision_committed": False,
    }

    ref_upd_candidate = _read_json(ref_upd / "poster_real_ocr_updated_reference_candidate.json") or {}
    gated_root = Path(
        str(
            ref_upd_candidate.get("poster_real_ocr_gated_execution_root")
            or dryrun_summary.get("input_roots", {}).get("ocr_exec", "")
            if isinstance(dryrun_summary.get("input_roots"), dict)
            else ""
        )
        or str(Path(consumer).parent / "poster_real_ocr_gated_execution_smoke_v0")
    )

    source_chain = {
        "schema_version": CHAIN_SCHEMA,
        "fusion_candidate_dryrun_ref": fusion_candidate_ref,
        "reference_closure_ref": str(closure / "poster_real_ocr_reference_lineage_closure_report.json"),
        "reference_update_ref": str(ref_upd / "poster_real_ocr_updated_reference_candidate.json"),
        "readonly_consumer_ref": str(consumer / "poster_real_ocr_region_text_consumer_view.json"),
        "gated_execution_ref": str(gated_root / "poster_layout_text_evidence_candidate.json"),
        "review_queue_build_step": PHASE_ID,
        "queue_item_id": queue_item_id,
        "source_fusion_candidate_id": source_candidate_id,
        "real_ocr_text_evidence_refs": list(fusion_candidate.get("real_ocr_text_evidence_refs") or []),
        "traceability": "fusion_candidate → review_queue → (future ttl/policy gate)",
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "review_queue_ready": not bool(errs),
        "queue_item_count": 1,
        "pending_review_count": 1,
        "approval_granted_count": 0,
        "auto_approve_count": 0,
        "ttl_gate_required_count": 1,
        "policy_gate_required_count": 1,
        "scene_delta_candidate_generated": False,
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
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
        "fusion_committed": False,
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
        "not_approval": True,
        "not_review_decision": True,
        "not_fusion_fact": True,
        "no_scene_delta_candidate": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "no_qr_decode": True,
        "no_brand_recognition": True,
        "no_visual_symbol_registry": True,
        "no_scene_delta_world_model_write": True,
        "no_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": [
            "Poster fusion TTL gate dry-run",
            "Poster fusion policy gate dry-run",
            "Poster fusion review decision dry-run later",
            "Scene Delta candidate dry-run later",
            "WorldModel write readiness gate later",
            "Poster ground truth fixture later",
            "VisualSymbolRegistry integration later",
            "QR decode governance later",
            "Brand identity governance later",
            "Benchmark T2 collector later",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "poster_real_ocr_fusion_review_queue_executed": True,
        "review_queue_only": True,
        "queue_item_count": 1,
        "pending_review_count": 1,
        "approval_granted_count": 0,
        "auto_approve_invoked": False,
        "fusion_committed": False,
        "scene_delta_candidate_generated": False,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "benchmark_result_claimed": False,
        "provider_comparison_claimed": False,
        "model_selection_claimed": False,
        "production_readiness_claimed": False,
    }

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "queue_scope": "review_queue_only",
        "based_on_fusion_candidate_dryrun": dryrun.is_dir(),
        "based_on_reference_closure": closure.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "queue_item_count": 1,
        "pending_review_count": 1,
        "approval_granted_count": 0,
        "auto_approve_invoked": False,
        "fusion_committed": False,
        "scene_delta_candidate_generated": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": "GO" if not errs else "NO_GO",
        "output_root": str(out),
    }

    return (
        summary,
        queue_candidate,
        queue_matrix,
        risk_inheritance,
        policy_report,
        decision_placeholder,
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
