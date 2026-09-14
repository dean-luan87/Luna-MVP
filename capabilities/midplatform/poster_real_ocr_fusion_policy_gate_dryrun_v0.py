# -*- coding: utf-8 -*-
"""Poster Real OCR fusion policy gate dry-run (evaluation only; no approval).

Phase-Poster-Real-OCR-Fusion-Policy-Gate-DryRun-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "Poster-Real-OCR-Fusion-Policy-Gate-DryRun-001"
TTL_REGION_IDS = ("price_or_promo_area", "time_location_area")

SUMMARY_SCHEMA = "poster_real_ocr_fusion_policy_gate_dryrun_summary_v0"
GATE_CANDIDATE_SCHEMA = "poster_real_ocr_fusion_policy_gate_candidate_v0"
REQ_MATRIX_SCHEMA = "poster_real_ocr_fusion_policy_requirement_matrix_v0"
DECISION_MATRIX_SCHEMA = "poster_real_ocr_fusion_policy_gate_decision_matrix_v0"
TTL_CARRYOVER_SCHEMA = "poster_real_ocr_fusion_policy_ttl_carryover_report_v0"
REVIEW_CARRYOVER_SCHEMA = "poster_real_ocr_fusion_policy_review_queue_carryover_report_v0"
COMM_TEMP_SCHEMA = "poster_real_ocr_fusion_policy_commercial_temporal_report_v0"
VISUAL_SCHEMA = "poster_real_ocr_fusion_policy_visual_symbol_report_v0"
SCENE_DELTA_SCHEMA = "poster_real_ocr_fusion_policy_scene_delta_eligibility_report_v0"
CHAIN_SCHEMA = "poster_real_ocr_fusion_policy_source_chain_report_v0"
METRICS_SCHEMA = "poster_real_ocr_fusion_policy_metrics_candidate_report_v0"
BENCHMARK_SCHEMA = "poster_real_ocr_fusion_policy_benchmark_link_report_v0"
HEALTH_SCHEMA = "poster_real_ocr_fusion_policy_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_fusion_policy_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_fusion_policy_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_fusion_policy_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "poster_real_ocr_fusion_policy_open_followups_v0"
AUDIT_SCHEMA = "poster_real_ocr_fusion_policy_audit_v0"

ALLOWED_NEXT_STEPS = ("review_decision_later", "ttl_policy_later", "scene_delta_candidate_later")
FORBIDDEN_NEXT_STEPS = ("world_model_write", "scene_delta_write", "navigation_decision", "auto_approve")

POLICY_BLOCKING_REASONS = (
    "ttl_gate_hold_for_review",
    "review_decision_missing",
    "source_validation_missing",
    "user_visible_uncertainty_policy_missing",
    "scene_delta_policy_not_satisfied",
    "world_model_write_forbidden",
)

POLICY_REQUIREMENTS = (
    {
        "requirement_id": "review_decision_required",
        "requirement_name": "Review decision required before Scene Delta candidate",
        "blocking": True,
        "satisfied": False,
        "missing_reason": "review_status_pending_no_decision",
        "source_evidence": "review_queue_candidate",
    },
    {
        "requirement_id": "ttl_policy_required",
        "requirement_name": "TTL policy required while TTL gate holds",
        "blocking": True,
        "satisfied": False,
        "missing_reason": "ttl_gate_hold_for_review",
        "source_evidence": "ttl_gate_candidate",
    },
    {
        "requirement_id": "source_validation_required",
        "requirement_name": "OCR source validation required before fact write",
        "blocking": True,
        "satisfied": False,
        "missing_reason": "source_validation_not_performed",
        "source_evidence": "fusion_input_matrix",
    },
    {
        "requirement_id": "user_visible_uncertainty_required",
        "requirement_name": "User-visible uncertainty policy required",
        "blocking": True,
        "satisfied": False,
        "missing_reason": "user_visible_uncertainty_policy_missing",
        "source_evidence": "policy_gate_dryrun",
    },
    {
        "requirement_id": "conflict_detection_required",
        "requirement_name": "Conflict detection required",
        "blocking": False,
        "satisfied": False,
        "missing_reason": "conflict_detection_not_implemented",
        "source_evidence": "policy_gate_dryrun",
    },
    {
        "requirement_id": "stale_detection_required",
        "requirement_name": "Stale detection for commercial text required",
        "blocking": False,
        "satisfied": False,
        "missing_reason": "stale_detection_not_implemented",
        "source_evidence": "policy_gate_dryrun",
    },
    {
        "requirement_id": "visual_symbol_not_fact_required",
        "requirement_name": "Visual symbol must not be consumed as text fact",
        "blocking": False,
        "satisfied": True,
        "missing_reason": None,
        "source_evidence": "visual_context_matrix",
    },
    {
        "requirement_id": "brand_identity_unconfirmed_required",
        "requirement_name": "Brand identity must remain unconfirmed in this phase",
        "blocking": False,
        "satisfied": True,
        "missing_reason": None,
        "source_evidence": "visual_context_matrix",
    },
    {
        "requirement_id": "qr_undecoded_required",
        "requirement_name": "QR must not be decoded in this phase",
        "blocking": False,
        "satisfied": True,
        "missing_reason": None,
        "source_evidence": "visual_context_matrix",
    },
    {
        "requirement_id": "benchmark_non_claim_required",
        "requirement_name": "No benchmark score claim in this phase",
        "blocking": False,
        "satisfied": True,
        "missing_reason": None,
        "source_evidence": "benchmark_link_report",
    },
    {
        "requirement_id": "no_write_boundary_required",
        "requirement_name": "No-write boundary must hold",
        "blocking": False,
        "satisfied": True,
        "missing_reason": None,
        "source_evidence": "policy_gate_dryrun",
    },
    {
        "requirement_id": "human_or_policy_review_required",
        "requirement_name": "Human or policy review required",
        "blocking": False,
        "satisfied": False,
        "missing_reason": "approval_status_not_approved",
        "source_evidence": "review_queue_candidate",
    },
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


def run_poster_real_ocr_fusion_policy_gate_dryrun_v0(
    *,
    poster_fusion_ttl_gate_root: str,
    poster_fusion_review_queue_root: str,
    poster_fusion_candidate_dryrun_root: str,
    poster_reference_closure_root: str,
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
    ttl_root = Path(poster_fusion_ttl_gate_root).resolve()
    queue_root = Path(poster_fusion_review_queue_root).resolve()
    dryrun = Path(poster_fusion_candidate_dryrun_root).resolve()
    closure = Path(poster_reference_closure_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    if not _source_ok(ttl_root, "poster_real_ocr_fusion_ttl_gate_dryrun_summary.json"):
        errs.append("ttl_gate_not_ok")
    if not _source_ok(queue_root, "poster_real_ocr_fusion_review_queue_summary.json"):
        errs.append("review_queue_not_ok")

    ttl_candidate = _read_json(ttl_root / "poster_real_ocr_fusion_ttl_gate_candidate.json") or {}
    ttl_region_matrix = _read_json(ttl_root / "poster_real_ocr_fusion_ttl_region_evaluation_matrix.json") or {}
    ttl_risk = _read_json(ttl_root / "poster_real_ocr_fusion_ttl_risk_classification_report.json") or {}
    queue_candidate = _read_json(queue_root / "poster_real_ocr_fusion_review_queue_candidate.json") or {}
    risk_inherit = _read_json(queue_root / "poster_real_ocr_fusion_review_risk_inheritance_report.json") or {}
    fusion_candidate = _read_json(dryrun / "poster_real_ocr_fusion_candidate.json") or {}
    fusion_input = _read_json(dryrun / "poster_real_ocr_fusion_input_matrix.json") or {}
    visual_matrix = _read_json(dryrun / "poster_real_ocr_fusion_visual_context_matrix.json") or {}
    reading_order = _read_json(dryrun / "poster_real_ocr_fusion_reading_order_guard.json") or {}

    queue_item_id = str(queue_candidate.get("queue_item_id") or ttl_candidate.get("source_queue_item_id") or "")
    fusion_candidate_id = str(
        queue_candidate.get("source_fusion_candidate_id") or ttl_candidate.get("source_fusion_candidate_id") or ""
    )
    ttl_gate_candidate_id = f"ttl_gate_{fusion_candidate_id}" if fusion_candidate_id else "ttl_gate_unknown"

    ttl_gate_decision = str(ttl_candidate.get("ttl_gate_decision") or "hold_for_review")
    ttl_gate_passed = ttl_candidate.get("ttl_gate_passed", False) is True
    ttl_gate_status = str(ttl_candidate.get("ttl_gate_status") or "evaluated_dryrun")

    explicit_validity = any(
        isinstance(r, dict) and r.get("explicit_validity_period_detected") is True
        for r in (ttl_region_matrix.get("rows") or [])
    )

    input_by_region: Dict[str, Dict[str, Any]] = {}
    for row in fusion_input.get("rows") or []:
        if isinstance(row, dict) and row.get("source_region_id"):
            input_by_region[str(row["source_region_id"])] = row

    ttl_region_trace = []
    for rid in TTL_REGION_IDS:
        inp = input_by_region.get(rid, {})
        ttl_row = next(
            (r for r in (ttl_region_matrix.get("rows") or []) if isinstance(r, dict) and r.get("source_region_id") == rid),
            {},
        )
        ttl_region_trace.append(
            {
                "source_region_id": rid,
                "text_joined": inp.get("text_joined") or ttl_row.get("text_joined"),
                "real_ocr_evidence_ref": inp.get("real_ocr_evidence_ref") or ttl_row.get("real_ocr_evidence_ref"),
                "ttl_gate_decision": ttl_row.get("ttl_gate_decision") or "hold_for_review",
            }
        )

    policy_gate_candidate = {
        "schema_version": GATE_CANDIDATE_SCHEMA,
        "gate_scope": "policy_gate_dryrun_only",
        "source_ttl_gate_candidate_id": ttl_gate_candidate_id,
        "source_queue_item_id": queue_item_id,
        "source_fusion_candidate_id": fusion_candidate_id,
        "policy_gate_status": "evaluated_dryrun",
        "policy_gate_decision": "hold_for_review",
        "policy_gate_passed": False,
        "approval_status": "not_approved",
        "review_status": "pending_review",
        "fact_status": "not_fact",
        "write_allowed": False,
        "scene_delta_candidate_allowed": False,
        "requires_review_decision": True,
        "requires_ttl_policy": True,
        "requires_source_validation": True,
        "requires_user_visible_uncertainty_policy": True,
        "requires_conflict_check": True,
        "requires_stale_detection": True,
        "allowed_next_steps": list(ALLOWED_NEXT_STEPS),
        "forbidden_next_steps": list(FORBIDDEN_NEXT_STEPS),
    }

    req_rows = []
    for req in POLICY_REQUIREMENTS:
        req_rows.append(
            {
                "requirement_id": req["requirement_id"],
                "requirement_name": req["requirement_name"],
                "required_before_scene_delta_candidate": True,
                "required_before_fact_write": True,
                "satisfied_in_this_phase": req["satisfied"],
                "source_evidence": req["source_evidence"],
                "missing_reason": req["missing_reason"],
                "blocking": req["blocking"],
            }
        )

    requirement_matrix = {
        "schema_version": REQ_MATRIX_SCHEMA,
        "requirement_count": len(req_rows),
        "rows": req_rows,
    }

    decision_matrix = {
        "schema_version": DECISION_MATRIX_SCHEMA,
        "row_count": 1,
        "rows": [
            {
                "queue_item_id": queue_item_id,
                "fusion_candidate_id": fusion_candidate_id,
                "ttl_gate_decision": ttl_gate_decision,
                "policy_gate_status": "evaluated_dryrun",
                "policy_gate_decision": "hold_for_review",
                "policy_gate_passed": False,
                "policy_blocking_reasons": list(POLICY_BLOCKING_REASONS),
                "scene_delta_candidate_allowed": False,
                "fact_write_allowed": False,
                "world_model_write_allowed": False,
                "navigation_decision_allowed": False,
            }
        ],
    }

    ttl_carryover = {
        "schema_version": TTL_CARRYOVER_SCHEMA,
        "ttl_gate_status": ttl_gate_status,
        "ttl_gate_decision": ttl_gate_decision,
        "ttl_gate_passed": ttl_gate_passed,
        "ttl_required_region_count": ttl_region_matrix.get("ttl_required_region_count", 2),
        "commercial_text_may_expire": ttl_risk.get("commercial_text_may_expire", True),
        "temporal_text_requires_ttl": ttl_risk.get("temporal_text_requires_ttl", True),
        "explicit_validity_period_detected": explicit_validity,
        "policy_gate_must_respect_ttl_hold": ttl_gate_decision == "hold_for_review" and not ttl_gate_passed,
    }

    review_carryover = {
        "schema_version": REVIEW_CARRYOVER_SCHEMA,
        "source_review_status": str(queue_candidate.get("review_status") or "pending_review"),
        "source_approval_status": str(queue_candidate.get("approval_status") or "not_approved"),
        "target_review_status": "pending_review",
        "target_approval_status": "not_approved",
        "approval_status_unchanged": True,
        "review_status_unchanged": True,
        "auto_approve_allowed": False,
        "approval_granted": False,
    }

    commercial_temporal = {
        "schema_version": COMM_TEMP_SCHEMA,
        "commercial_claim_status": risk_inherit.get("commercial_claim_status", "candidate_only"),
        "temporal_claim_status": risk_inherit.get("temporal_claim_status", "candidate_only"),
        "commercial_text_requires_ttl": True,
        "temporal_text_requires_ttl": True,
        "commercial_text_requires_source_validation": True,
        "temporal_text_requires_source_validation": True,
        "commercial_text_world_model_write_allowed": False,
        "temporal_text_world_model_write_allowed": False,
        "commercial_text_scene_delta_allowed": False,
        "temporal_text_scene_delta_allowed": False,
        "reading_order_confidence": risk_inherit.get("reading_order_confidence") or reading_order.get("confidence"),
        "reading_order_blocks_fact_fusion": (
            str(risk_inherit.get("reading_order_confidence") or reading_order.get("confidence") or "").lower() == "low"
        ),
    }

    visual_rows = visual_matrix.get("rows") if isinstance(visual_matrix.get("rows"), list) else []
    visual_count = visual_matrix.get("visual_context_count", len(visual_rows))
    visual_consumed_as_text = any(
        isinstance(r, dict) and r.get("consumed_as_text") is True for r in visual_rows
    )

    visual_symbol = {
        "schema_version": VISUAL_SCHEMA,
        "visual_context_present": bool(visual_rows),
        "visual_symbol_context_count": visual_count,
        "visual_context_consumed_as_text": visual_consumed_as_text,
        "logo_not_brand_fact": True,
        "brand_identity_confirmed": fusion_candidate.get("candidate_hypothesis", {}).get(
            "brand_identity_confirmed", False
        )
        if isinstance(fusion_candidate.get("candidate_hypothesis"), dict)
        else False,
        "qr_decoded": fusion_candidate.get("candidate_hypothesis", {}).get("qr_decoded", False)
        if isinstance(fusion_candidate.get("candidate_hypothesis"), dict)
        else False,
        "visual_symbol_registry_invoked": False,
        "visual_symbol_policy_not_satisfied": True,
    }

    scene_delta_blocking = list(POLICY_BLOCKING_REASONS) + ["reading_order_confidence_low"]
    scene_delta_eligibility = {
        "schema_version": SCENE_DELTA_SCHEMA,
        "scene_delta_candidate_allowed": False,
        "scene_delta_candidate_generated": False,
        "eligibility_status": "not_eligible_in_this_phase",
        "blocking_reasons": scene_delta_blocking,
        "required_future_gates": [
            "review_decision_gate",
            "ttl_policy_gate",
            "source_validation_gate",
            "user_visible_uncertainty_gate",
            "conflict_detection_gate",
        ],
    }

    consumer_ref = ""
    gated_ref = ""
    for row in fusion_input.get("rows") or []:
        if isinstance(row, dict) and row.get("lineage"):
            lineage = row["lineage"]
            consumer_ref = consumer_ref or str(lineage.get("readonly_consumer_ref") or "")
            gated_ref = gated_ref or str(lineage.get("real_ocr_execution_ref") or "")
            break

    source_chain = {
        "schema_version": CHAIN_SCHEMA,
        "ttl_gate_ref": str(ttl_root / "poster_real_ocr_fusion_ttl_gate_candidate.json"),
        "review_queue_ref": str(queue_root / "poster_real_ocr_fusion_review_queue_candidate.json"),
        "fusion_candidate_dryrun_ref": str(dryrun / "poster_real_ocr_fusion_candidate.json"),
        "reference_closure_ref": str(closure / "poster_real_ocr_reference_lineage_closure_report.json"),
        "readonly_consumer_ref": consumer_ref,
        "gated_execution_ref": gated_ref,
        "policy_gate_build_step": PHASE_ID,
        "policy_candidate_ttl_region_trace": ttl_region_trace,
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "policy_gate_dryrun_ready": not bool(errs),
        "policy_candidate_count": 1,
        "policy_gate_passed_count": 0,
        "policy_gate_hold_count": 1,
        "policy_gate_reject_count": 0,
        "scene_delta_candidate_allowed_count": 0,
        "scene_delta_candidate_generated": False,
        "approval_granted_count": 0,
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
        "not_policy_approval": True,
        "not_scene_delta_candidate_ready": True,
        "not_commercial_temporal_fact_write": True,
        "not_fusion_fact": True,
        "not_world_model_write_readiness": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "no_qr_decode": True,
        "no_brand_recognition": True,
        "no_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": [
            "Poster fusion review decision dry-run",
            "Poster TTL policy implementation later",
            "source validation gate later",
            "user-visible uncertainty policy later",
            "conflict detection gate later",
            "stale detection gate later",
            "Scene Delta candidate dry-run later",
            "WorldModel write readiness gate later",
            "Poster ground truth fixture later",
            "Benchmark T2 collector later",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "poster_real_ocr_fusion_policy_gate_dryrun_executed": True,
        "policy_gate_dryrun_only": True,
        "policy_gate_evaluated": True,
        "policy_gate_passed_count": 0,
        "policy_gate_hold_count": 1,
        "policy_gate_reject_count": 0,
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

    phase_hint = "GO" if not errs else "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "gate_scope": "policy_gate_dryrun_only",
        "based_on_ttl_gate": ttl_root.is_dir(),
        "based_on_review_queue": queue_root.is_dir(),
        "based_on_fusion_candidate_dryrun": dryrun.is_dir(),
        "based_on_reference_closure": closure.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "policy_gate_evaluated": True,
        "policy_candidate_count": 1,
        "policy_gate_passed_count": 0,
        "policy_gate_hold_count": 1,
        "policy_gate_reject_count": 0,
        "approval_granted_count": 0,
        "auto_approve_invoked": False,
        "fusion_committed": False,
        "scene_delta_candidate_generated": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": phase_hint,
        "output_root": str(out),
    }

    return (
        summary,
        policy_gate_candidate,
        requirement_matrix,
        decision_matrix,
        ttl_carryover,
        review_carryover,
        commercial_temporal,
        visual_symbol,
        scene_delta_eligibility,
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
