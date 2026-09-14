# -*- coding: utf-8 -*-
"""Poster Real OCR fusion TTL gate dry-run (evaluation only; no approval).

Phase-Poster-Real-OCR-Fusion-TTL-Gate-DryRun-001
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "Poster-Real-OCR-Fusion-TTL-Gate-DryRun-001"
TTL_REGION_IDS = ("price_or_promo_area", "time_location_area")

SUMMARY_SCHEMA = "poster_real_ocr_fusion_ttl_gate_dryrun_summary_v0"
GATE_CANDIDATE_SCHEMA = "poster_real_ocr_fusion_ttl_gate_candidate_v0"
REGION_MATRIX_SCHEMA = "poster_real_ocr_fusion_ttl_region_evaluation_matrix_v0"
RISK_CLASS_SCHEMA = "poster_real_ocr_fusion_ttl_risk_classification_report_v0"
POLICY_REQ_SCHEMA = "poster_real_ocr_fusion_ttl_policy_requirement_report_v0"
CARRYOVER_SCHEMA = "poster_real_ocr_fusion_ttl_review_queue_carryover_report_v0"
DECISION_MATRIX_SCHEMA = "poster_real_ocr_fusion_ttl_gate_decision_matrix_v0"
CHAIN_SCHEMA = "poster_real_ocr_fusion_ttl_source_chain_report_v0"
METRICS_SCHEMA = "poster_real_ocr_fusion_ttl_metrics_candidate_report_v0"
BENCHMARK_SCHEMA = "poster_real_ocr_fusion_ttl_benchmark_link_report_v0"
HEALTH_SCHEMA = "poster_real_ocr_fusion_ttl_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_fusion_ttl_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_fusion_ttl_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_fusion_ttl_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "poster_real_ocr_fusion_ttl_open_followups_v0"
AUDIT_SCHEMA = "poster_real_ocr_fusion_ttl_audit_v0"

ALLOWED_NEXT_STEPS = ("policy_gate_later", "review_decision_later", "scene_delta_candidate_later")
FORBIDDEN_NEXT_STEPS = ("world_model_write", "scene_delta_write", "navigation_decision", "auto_approve")

BLOCKING_REASONS = (
    "commercial_text_requires_ttl",
    "temporal_text_requires_ttl",
    "review_required_before_fact",
    "source_validation_missing",
    "expiry_strategy_missing",
)

POLICY_REQUIREMENTS = (
    ("explicit_validity_period_required", "no_explicit_ttl_policy_in_phase"),
    ("source_validation_required", "ocr_evidence_source_not_validated_for_write"),
    ("review_approval_required", "approval_status_not_approved"),
    ("expiry_strategy_required", "expiry_strategy_not_defined"),
    ("rollback_strategy_required", "rollback_strategy_not_defined"),
    ("stale_detection_required", "stale_detection_not_implemented"),
    ("conflict_detection_required", "conflict_detection_not_implemented"),
    ("user_visible_uncertainty_required", "user_visible_uncertainty_policy_missing"),
)

_DATE_PATTERN = re.compile(r"\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}")


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


def _detect_validity_period(text: str) -> bool:
    return bool(_DATE_PATTERN.search(str(text or "")))


def run_poster_real_ocr_fusion_ttl_gate_dryrun_v0(
    *,
    poster_fusion_review_queue_root: str,
    poster_fusion_candidate_dryrun_root: str,
    poster_reference_closure_root: str,
    poster_readonly_consumer_root: str,
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
    queue_root = Path(poster_fusion_review_queue_root).resolve()
    dryrun = Path(poster_fusion_candidate_dryrun_root).resolve()
    closure = Path(poster_reference_closure_root).resolve()
    consumer = Path(poster_readonly_consumer_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    if not _source_ok(queue_root, "poster_real_ocr_fusion_review_queue_summary.json"):
        errs.append("review_queue_not_ok")

    queue_candidate = _read_json(queue_root / "poster_real_ocr_fusion_review_queue_candidate.json") or {}
    fusion_input = _read_json(dryrun / "poster_real_ocr_fusion_input_matrix.json") or {}
    risk_inherit = _read_json(queue_root / "poster_real_ocr_fusion_review_risk_inheritance_report.json") or {}

    queue_item_id = str(queue_candidate.get("queue_item_id") or "")
    fusion_candidate_id = str(queue_candidate.get("source_fusion_candidate_id") or "")

    input_by_region: Dict[str, Dict[str, Any]] = {}
    for row in fusion_input.get("rows") or []:
        if isinstance(row, dict) and row.get("source_region_id"):
            input_by_region[str(row["source_region_id"])] = row

    ttl_region_rows: List[Dict[str, Any]] = []
    for rid in TTL_REGION_IDS:
        inp = input_by_region.get(rid, {})
        tj = str(inp.get("text_joined") or "")
        ttl_reason = (
            "commercial_text_may_expire"
            if rid == "price_or_promo_area"
            else "temporal_text_requires_ttl"
        )
        expiry_detected = _detect_validity_period(tj) if rid == "time_location_area" else False
        ttl_region_rows.append(
            {
                "ttl_eval_id": f"ttl_eval_{rid}",
                "source_region_id": rid,
                "region_type": rid,
                "text_joined": tj,
                "ttl_required": True,
                "ttl_reason": ttl_reason,
                "commercial_or_temporal_risk": True,
                "expiry_detected": expiry_detected or rid == "price_or_promo_area",
                "explicit_validity_period_detected": expiry_detected,
                "source_validation_available": False,
                "ttl_gate_decision": "hold_for_review",
                "fact_status": "not_fact",
                "write_allowed": False,
                "real_ocr_evidence_ref": inp.get("real_ocr_evidence_ref"),
                "lineage": inp.get("lineage"),
            }
        )

    gate_candidate = {
        "schema_version": GATE_CANDIDATE_SCHEMA,
        "gate_scope": "ttl_gate_dryrun_only",
        "source_queue_item_id": queue_item_id,
        "source_fusion_candidate_id": fusion_candidate_id,
        "ttl_gate_status": "evaluated_dryrun",
        "ttl_gate_decision": "hold_for_review",
        "ttl_gate_passed": False,
        "approval_status": "not_approved",
        "review_status": "pending_review",
        "fact_status": "not_fact",
        "write_allowed": False,
        "requires_ttl_policy": True,
        "requires_expiry_strategy": True,
        "requires_source_validation": True,
        "requires_human_or_policy_review": True,
        "allowed_next_steps": list(ALLOWED_NEXT_STEPS),
        "forbidden_next_steps": list(FORBIDDEN_NEXT_STEPS),
    }

    region_matrix = {
        "schema_version": REGION_MATRIX_SCHEMA,
        "ttl_required_region_count": len(ttl_region_rows),
        "rows": ttl_region_rows,
    }

    risk_classification = {
        "schema_version": RISK_CLASS_SCHEMA,
        "commercial_text_may_expire": True,
        "temporal_text_requires_ttl": True,
        "price_or_discount_claim_candidate_only": True,
        "temporal_validity_claim_candidate_only": True,
        "expiry_strategy_required": True,
        "source_validation_required": True,
        "no_world_model_write_without_ttl_policy": True,
        "no_scene_delta_write_without_ttl_policy": True,
    }

    policy_requirements = {
        "schema_version": POLICY_REQ_SCHEMA,
        "requirements": [
            {
                "requirement_id": req_id,
                "required_before_write": True,
                "satisfied_in_this_phase": False,
                "missing_reason": missing,
            }
            for req_id, missing in POLICY_REQUIREMENTS
        ],
    }

    carryover = {
        "schema_version": CARRYOVER_SCHEMA,
        "source_review_status": str(queue_candidate.get("review_status") or "pending_review"),
        "source_approval_status": str(queue_candidate.get("approval_status") or "not_approved"),
        "target_review_status": "pending_review",
        "target_approval_status": "not_approved",
        "approval_status_unchanged": True,
        "review_status_unchanged": True,
        "auto_approve_allowed": False,
        "approval_granted": False,
    }

    decision_matrix = {
        "schema_version": DECISION_MATRIX_SCHEMA,
        "row_count": 1,
        "rows": [
            {
                "queue_item_id": queue_item_id,
                "fusion_candidate_id": fusion_candidate_id,
                "ttl_gate_status": "evaluated_dryrun",
                "ttl_gate_decision": "hold_for_review",
                "ttl_gate_passed": False,
                "ttl_gate_blocking_reasons": list(BLOCKING_REASONS),
                "allowed_next_steps": list(ALLOWED_NEXT_STEPS),
                "forbidden_next_steps": list(FORBIDDEN_NEXT_STEPS),
                "fact_write_allowed": False,
                "scene_delta_candidate_allowed": False,
                "world_model_write_allowed": False,
            }
        ],
    }

    gated_root = Path(str(consumer).replace("readonly_consumer", "gated_execution"))
    if not gated_root.is_dir():
        gated_root = consumer.parent / "poster_real_ocr_gated_execution_smoke_v0"

    source_chain = {
        "schema_version": CHAIN_SCHEMA,
        "review_queue_ref": str(queue_root / "poster_real_ocr_fusion_review_queue_candidate.json"),
        "fusion_candidate_dryrun_ref": str(dryrun / "poster_real_ocr_fusion_candidate.json"),
        "reference_closure_ref": str(closure / "poster_real_ocr_reference_lineage_closure_report.json"),
        "readonly_consumer_ref": str(consumer / "poster_real_ocr_region_text_consumer_view.json"),
        "gated_execution_ref": str(gated_root / "poster_layout_text_evidence_candidate.json"),
        "ttl_gate_build_step": PHASE_ID,
        "ttl_region_evidence_trace": [
            {
                "source_region_id": r["source_region_id"],
                "real_ocr_evidence_ref": r.get("real_ocr_evidence_ref"),
                "text_joined": r.get("text_joined"),
            }
            for r in ttl_region_rows
        ],
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "ttl_gate_dryrun_ready": not bool(errs),
        "ttl_candidate_count": 1,
        "ttl_required_region_count": len(ttl_region_rows),
        "ttl_gate_passed_count": 0,
        "ttl_gate_hold_count": 1,
        "approval_granted_count": 0,
        "scene_delta_candidate_generated": False,
        "world_model_write_allowed": False,
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
        "not_ttl_approval": True,
        "not_commercial_temporal_fact_write": True,
        "not_fusion_fact": True,
        "no_scene_delta_candidate": True,
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
            "Poster fusion policy gate dry-run",
            "Poster fusion review decision dry-run",
            "Poster TTL policy implementation later",
            "Poster expiry strategy later",
            "stale detection for commercial text later",
            "Scene Delta candidate dry-run later",
            "WorldModel write readiness gate later",
            "Poster ground truth fixture later",
            "Benchmark T2 collector later",
            "user-visible uncertainty policy later",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "poster_real_ocr_fusion_ttl_gate_dryrun_executed": True,
        "ttl_gate_dryrun_only": True,
        "ttl_gate_evaluated": True,
        "ttl_gate_passed_count": 0,
        "ttl_gate_hold_count": 1,
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
    if not errs and all(not str(input_by_region.get(rid, {}).get("text_joined") or "").strip() for rid in TTL_REGION_IDS):
        phase_hint = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "gate_scope": "ttl_gate_dryrun_only",
        "based_on_review_queue": queue_root.is_dir(),
        "based_on_fusion_candidate_dryrun": dryrun.is_dir(),
        "based_on_reference_closure": closure.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "ttl_gate_evaluated": True,
        "ttl_candidate_count": 1,
        "ttl_required_region_count": len(ttl_region_rows),
        "ttl_gate_passed_count": 0,
        "ttl_gate_hold_count": 1,
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
        gate_candidate,
        region_matrix,
        risk_classification,
        policy_requirements,
        carryover,
        decision_matrix,
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
