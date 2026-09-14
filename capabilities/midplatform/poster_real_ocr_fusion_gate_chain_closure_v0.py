# -*- coding: utf-8 -*-
"""Poster Real OCR fusion gate chain closure (aggregate only; no new capability).

Phase-Poster-Real-OCR-Fusion-Gate-Chain-Closure-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "Poster-Real-OCR-Fusion-Gate-Chain-Closure-001"
TTL_REGION_IDS = ("price_or_promo_area", "time_location_area")

SUMMARY_SCHEMA = "poster_real_ocr_fusion_gate_chain_closure_summary_v0"
PHASE_MATRIX_SCHEMA = "poster_real_ocr_fusion_gate_chain_phase_matrix_v0"
LINEAGE_SCHEMA = "poster_real_ocr_fusion_gate_chain_lineage_report_v0"
DECISION_SCHEMA = "poster_real_ocr_fusion_gate_chain_decision_matrix_v0"
BLOCKING_SCHEMA = "poster_real_ocr_fusion_gate_chain_blocking_reasons_rollup_v0"
REVIEW_APPROVAL_SCHEMA = "poster_real_ocr_fusion_gate_chain_review_approval_closure_report_v0"
TTL_CLOSURE_SCHEMA = "poster_real_ocr_fusion_gate_chain_ttl_closure_report_v0"
POLICY_CLOSURE_SCHEMA = "poster_real_ocr_fusion_gate_chain_policy_closure_report_v0"
COMM_TEMP_SCHEMA = "poster_real_ocr_fusion_gate_chain_commercial_temporal_closure_report_v0"
VISUAL_SCHEMA = "poster_real_ocr_fusion_gate_chain_visual_symbol_boundary_report_v0"
SCENE_DELTA_SCHEMA = "poster_real_ocr_fusion_gate_chain_scene_delta_non_eligibility_report_v0"
METRICS_SCHEMA = "poster_real_ocr_fusion_gate_chain_metrics_closure_candidate_report_v0"
BENCHMARK_SCHEMA = "poster_real_ocr_fusion_gate_chain_benchmark_link_report_v0"
HEALTH_SCHEMA = "poster_real_ocr_fusion_gate_chain_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_fusion_gate_chain_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_fusion_gate_chain_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_fusion_gate_chain_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "poster_real_ocr_fusion_gate_chain_open_followups_v0"
AUDIT_SCHEMA = "poster_real_ocr_fusion_gate_chain_audit_v0"

CORE_PHASE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_key": "fusion_candidate_dryrun",
        "phase_name": "Poster-Real-OCR-Fusion-Candidate-DryRun-001",
        "summary_file": "poster_real_ocr_fusion_candidate_dryrun_summary.json",
        "verifier_file": "poster_real_ocr_fusion_verifier_report.json",
        "phase_role": "fusion_candidate_generation",
        "contribution_to_gate_chain": "fusion_candidate_dryrun",
    },
    {
        "phase_key": "fusion_review_queue",
        "phase_name": "Poster-Real-OCR-Fusion-Review-Queue-001",
        "summary_file": "poster_real_ocr_fusion_review_queue_summary.json",
        "verifier_file": "poster_real_ocr_fusion_review_verifier_report.json",
        "phase_role": "review_queue_enqueue",
        "contribution_to_gate_chain": "fusion_review_queue",
    },
    {
        "phase_key": "fusion_ttl_gate_dryrun",
        "phase_name": "Poster-Real-OCR-Fusion-TTL-Gate-DryRun-001",
        "summary_file": "poster_real_ocr_fusion_ttl_gate_dryrun_summary.json",
        "verifier_file": "poster_real_ocr_fusion_ttl_verifier_report.json",
        "phase_role": "ttl_gate_evaluation",
        "contribution_to_gate_chain": "fusion_ttl_gate_dryrun",
    },
    {
        "phase_key": "fusion_policy_gate_dryrun",
        "phase_name": "Poster-Real-OCR-Fusion-Policy-Gate-DryRun-001",
        "summary_file": "poster_real_ocr_fusion_policy_gate_dryrun_summary.json",
        "verifier_file": "poster_real_ocr_fusion_policy_verifier_report.json",
        "phase_role": "policy_gate_evaluation",
        "contribution_to_gate_chain": "fusion_policy_gate_dryrun",
    },
)

SUPPORT_PHASE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_key": "reference_closure",
        "phase_name": "Poster-Real-OCR-Reference-Closure-001",
        "summary_file": "poster_real_ocr_reference_closure_summary.json",
        "verifier_file": "poster_real_ocr_reference_closure_verifier_report.json",
        "phase_role": "reference_lineage_support",
        "contribution_to_gate_chain": "reference_closure",
    },
    {
        "phase_key": "readonly_consumer",
        "phase_name": "Poster-Real-OCR-ReadOnly-Consumer-001",
        "summary_file": "poster_real_ocr_readonly_consumer_summary.json",
        "verifier_file": "poster_real_ocr_readonly_verifier_report.json",
        "phase_role": "readonly_consumer_support",
        "contribution_to_gate_chain": "readonly_consumer",
    },
    {
        "phase_key": "gated_execution",
        "phase_name": "Poster-Real-OCR-Gated-Execution-001",
        "summary_file": "poster_real_ocr_gated_execution_summary.json",
        "verifier_file": "poster_real_ocr_verifier_report.json",
        "phase_role": "gated_real_ocr_support",
        "contribution_to_gate_chain": "gated_execution",
    },
)

BLOCKING_ROLLUP_SPECS: Tuple[Dict[str, str], ...] = (
    ("review_decision_missing", "fusion_review_queue"),
    ("ttl_policy_required", "fusion_ttl_gate_dryrun"),
    ("source_validation_required", "fusion_policy_gate_dryrun"),
    ("user_visible_uncertainty_required", "fusion_policy_gate_dryrun"),
    ("conflict_detection_required", "fusion_policy_gate_dryrun"),
    ("stale_detection_required", "fusion_policy_gate_dryrun"),
    ("scene_delta_policy_not_satisfied", "fusion_policy_gate_dryrun"),
    ("world_model_write_forbidden", "fusion_policy_gate_dryrun"),
    ("commercial_text_requires_ttl", "fusion_ttl_gate_dryrun"),
    ("temporal_text_requires_ttl", "fusion_ttl_gate_dryrun"),
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
    if hint in ("GO", "CONDITIONAL_GO"):
        return hint, blockers
    blockers.append(f"phase_hint:{hint}")
    return "NO_GO", blockers


def _build_phase_rows(roots: Dict[str, Path], specs: Tuple[Dict[str, Any], ...]) -> Tuple[List[Dict[str, Any]], List[str]]:
    rows: List[Dict[str, Any]] = []
    errs: List[str] = []
    for spec in specs:
        key = spec["phase_key"]
        root = roots[key]
        verdict, blockers = _verdict_from_root(root, spec)
        sm = _read_json(root / str(spec["summary_file"])) or {}
        ok = verdict in ("GO", "CONDITIONAL_GO") and not blockers
        if key in {s["phase_key"] for s in CORE_PHASE_SPECS} and not ok:
            errs.append(f"core_phase_not_ok:{spec['phase_name']}")
        rows.append(
            {
                "phase_name": spec["phase_name"],
                "phase_key": key,
                "input_root": str(root),
                "source_status": "ok" if ok else "fail",
                "verifier_verdict": verdict,
                "blockers": blockers,
                "phase_role": spec["phase_role"],
                "output_status": "available" if ok else "incomplete",
                "write_status": "no_write",
                "routing_changed": False,
                "contribution_to_gate_chain": spec["contribution_to_gate_chain"],
            }
        )
    return rows, errs


def run_poster_real_ocr_fusion_gate_chain_closure_v0(
    *,
    poster_fusion_candidate_dryrun_root: str,
    poster_fusion_review_queue_root: str,
    poster_fusion_ttl_gate_root: str,
    poster_fusion_policy_gate_root: str,
    poster_reference_closure_root: str,
    poster_readonly_consumer_root: str,
    poster_gated_execution_root: str,
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
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    dryrun = Path(poster_fusion_candidate_dryrun_root).resolve()
    queue_root = Path(poster_fusion_review_queue_root).resolve()
    ttl_root = Path(poster_fusion_ttl_gate_root).resolve()
    policy_root = Path(poster_fusion_policy_gate_root).resolve()
    closure = Path(poster_reference_closure_root).resolve()
    consumer = Path(poster_readonly_consumer_root).resolve()
    gated = Path(poster_gated_execution_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    roots: Dict[str, Path] = {
        "fusion_candidate_dryrun": dryrun,
        "fusion_review_queue": queue_root,
        "fusion_ttl_gate_dryrun": ttl_root,
        "fusion_policy_gate_dryrun": policy_root,
        "reference_closure": closure,
        "readonly_consumer": consumer,
        "gated_execution": gated,
    }

    core_rows, core_errs = _build_phase_rows(roots, CORE_PHASE_SPECS)
    support_rows, _ = _build_phase_rows(roots, SUPPORT_PHASE_SPECS)
    errs.extend(core_errs)

    fusion_candidate = _read_json(dryrun / "poster_real_ocr_fusion_candidate.json") or {}
    queue_candidate = _read_json(queue_root / "poster_real_ocr_fusion_review_queue_candidate.json") or {}
    ttl_candidate = _read_json(ttl_root / "poster_real_ocr_fusion_ttl_gate_candidate.json") or {}
    policy_candidate = _read_json(policy_root / "poster_real_ocr_fusion_policy_gate_candidate.json") or {}
    ttl_region_matrix = _read_json(ttl_root / "poster_real_ocr_fusion_ttl_region_evaluation_matrix.json") or {}
    fusion_input = _read_json(dryrun / "poster_real_ocr_fusion_input_matrix.json") or {}
    visual_matrix = _read_json(dryrun / "poster_real_ocr_fusion_visual_context_matrix.json") or {}
    risk_inherit = _read_json(queue_root / "poster_real_ocr_fusion_review_risk_inheritance_report.json") or {}
    policy_req = _read_json(policy_root / "poster_real_ocr_fusion_policy_requirement_matrix.json") or {}
    policy_ttl_carry = _read_json(policy_root / "poster_real_ocr_fusion_policy_ttl_carryover_report.json") or {}

    fusion_candidate_id = str(
        queue_candidate.get("source_fusion_candidate_id")
        or ttl_candidate.get("source_fusion_candidate_id")
        or fusion_candidate.get("candidate_id")
        or ""
    )
    queue_item_id = str(queue_candidate.get("queue_item_id") or ttl_candidate.get("source_queue_item_id") or "")
    ttl_gate_candidate_id = str(policy_candidate.get("source_ttl_gate_candidate_id") or f"ttl_gate_{fusion_candidate_id}")
    policy_gate_candidate_id = f"policy_gate_{fusion_candidate_id}" if fusion_candidate_id else "policy_gate_unknown"

    ocr_refs: List[str] = []
    ttl_region_refs: List[Dict[str, Any]] = []
    ref_update_ref = ""
    for row in fusion_input.get("rows") or []:
        if not isinstance(row, dict):
            continue
        rid = str(row.get("source_region_id") or "")
        ref = row.get("real_ocr_evidence_ref")
        if ref:
            ocr_refs.append(str(ref))
        if rid in TTL_REGION_IDS:
            ttl_region_refs.append(
                {
                    "source_region_id": rid,
                    "real_ocr_evidence_ref": ref,
                    "text_joined": row.get("text_joined"),
                }
            )
        lineage = row.get("lineage") if isinstance(row.get("lineage"), dict) else {}
        if lineage.get("reference_update_ref") and not ref_update_ref:
            ref_update_ref = str(lineage["reference_update_ref"])

    phase_matrix = {
        "schema_version": PHASE_MATRIX_SCHEMA,
        "core_gate_phase_count": len(core_rows),
        "support_phase_count": len(support_rows),
        "rows": core_rows + support_rows,
    }

    lineage_report = {
        "schema_version": LINEAGE_SCHEMA,
        "chain_steps": [
            {"step": "gated_execution", "ref": str(gated / "poster_layout_text_evidence_candidate.json")},
            {"step": "readonly_consumer", "ref": str(consumer / "poster_real_ocr_region_text_consumer_view.json")},
            {"step": "reference_update", "ref": ref_update_ref or None},
            {"step": "reference_closure", "ref": str(closure / "poster_real_ocr_reference_lineage_closure_report.json")},
            {"step": "fusion_candidate_dryrun", "ref": str(dryrun / "poster_real_ocr_fusion_candidate.json")},
            {"step": "review_queue", "ref": str(queue_root / "poster_real_ocr_fusion_review_queue_candidate.json")},
            {"step": "ttl_gate_dryrun", "ref": str(ttl_root / "poster_real_ocr_fusion_ttl_gate_candidate.json")},
            {"step": "policy_gate_dryrun", "ref": str(policy_root / "poster_real_ocr_fusion_policy_gate_candidate.json")},
            {"step": "gate_chain_closure", "ref": str(out / "poster_real_ocr_fusion_gate_chain_closure_summary.json")},
        ],
        "gate_item_trace": {
            "fusion_candidate_id": fusion_candidate_id,
            "queue_item_id": queue_item_id,
            "ttl_gate_candidate_id": ttl_gate_candidate_id,
            "policy_gate_candidate_id": policy_gate_candidate_id,
            "real_ocr_evidence_refs": sorted(set(ocr_refs)),
            "ttl_region_refs": ttl_region_refs,
        },
    }

    final_blocking = [
        "review_decision_missing",
        "ttl_policy_required",
        "source_validation_required",
        "user_visible_uncertainty_required",
        "conflict_detection_required",
        "stale_detection_required",
        "scene_delta_policy_not_satisfied",
        "world_model_write_forbidden",
        "commercial_text_requires_ttl",
        "temporal_text_requires_ttl",
        "reading_order_confidence_low",
    ]

    decision_matrix = {
        "schema_version": DECISION_SCHEMA,
        "row_count": 1,
        "rows": [
            {
                "fusion_candidate_id": fusion_candidate_id,
                "queue_item_id": queue_item_id,
                "review_status": str(queue_candidate.get("review_status") or "pending_review"),
                "approval_status": str(queue_candidate.get("approval_status") or "not_approved"),
                "ttl_gate_status": str(ttl_candidate.get("ttl_gate_status") or "evaluated_dryrun"),
                "ttl_gate_decision": str(ttl_candidate.get("ttl_gate_decision") or "hold_for_review"),
                "ttl_gate_passed": ttl_candidate.get("ttl_gate_passed", False) is True,
                "policy_gate_status": str(policy_candidate.get("policy_gate_status") or "evaluated_dryrun"),
                "policy_gate_decision": str(policy_candidate.get("policy_gate_decision") or "hold_for_review"),
                "policy_gate_passed": policy_candidate.get("policy_gate_passed", False) is True,
                "final_gate_chain_decision": "hold_for_review",
                "final_blocking_reasons": final_blocking,
                "scene_delta_candidate_allowed": False,
                "world_model_write_allowed": False,
                "fact_write_allowed": False,
            }
        ],
    }

    blocking_rows = []
    for reason_code, source_gate in BLOCKING_ROLLUP_SPECS:
        blocking_rows.append(
            {
                "reason_code": reason_code,
                "source_gate": source_gate,
                "blocking": True,
                "required_future_resolution": f"resolve_{reason_code}",
                "current_status": "unresolved",
            }
        )
    blocking_rollup = {
        "schema_version": BLOCKING_SCHEMA,
        "reason_count": len(blocking_rows),
        "rows": blocking_rows,
    }

    review_approval = {
        "schema_version": REVIEW_APPROVAL_SCHEMA,
        "review_status": "pending_review",
        "approval_status": "not_approved",
        "approval_granted": False,
        "auto_approve_invoked": False,
        "decision_committed": False,
        "review_decision_available": False,
        "review_decision_required": True,
        "manual_or_policy_review_required": True,
    }

    explicit_validity = policy_ttl_carry.get("explicit_validity_period_detected")
    if explicit_validity is None:
        explicit_validity = any(
            isinstance(r, dict) and r.get("explicit_validity_period_detected") is True
            for r in (ttl_region_matrix.get("rows") or [])
        )

    ttl_closure = {
        "schema_version": TTL_CLOSURE_SCHEMA,
        "ttl_gate_evaluated": True,
        "ttl_gate_status": str(ttl_candidate.get("ttl_gate_status") or "evaluated_dryrun"),
        "ttl_gate_decision": str(ttl_candidate.get("ttl_gate_decision") or "hold_for_review"),
        "ttl_gate_passed": False,
        "ttl_required_region_count": ttl_region_matrix.get("ttl_required_region_count", 2),
        "commercial_text_may_expire": True,
        "temporal_text_requires_ttl": True,
        "explicit_validity_period_detected": bool(explicit_validity),
        "ttl_policy_satisfied": False,
        "expiry_strategy_satisfied": False,
        "source_validation_satisfied": False,
    }

    blocking_req_count = sum(
        1
        for r in (policy_req.get("rows") or [])
        if isinstance(r, dict) and r.get("blocking") is True
    )

    policy_closure = {
        "schema_version": POLICY_CLOSURE_SCHEMA,
        "policy_gate_evaluated": True,
        "policy_gate_status": str(policy_candidate.get("policy_gate_status") or "evaluated_dryrun"),
        "policy_gate_decision": str(policy_candidate.get("policy_gate_decision") or "hold_for_review"),
        "policy_gate_passed": False,
        "blocking_requirement_count": blocking_req_count,
        "scene_delta_candidate_allowed": False,
        "scene_delta_candidate_generated": False,
        "world_model_write_allowed": False,
        "navigation_decision_allowed": False,
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
    }

    visual_rows = visual_matrix.get("rows") if isinstance(visual_matrix.get("rows"), list) else []
    visual_boundary = {
        "schema_version": VISUAL_SCHEMA,
        "visual_context_present": bool(visual_rows),
        "visual_symbol_context_count": visual_matrix.get("visual_context_count", len(visual_rows)),
        "visual_context_consumed_as_text": risk_inherit.get("visual_context_consumed_as_text", False) is True,
        "logo_not_brand_fact": True,
        "brand_identity_confirmed": risk_inherit.get("brand_identity_confirmed", False) is True,
        "qr_decoded": risk_inherit.get("qr_decoded", False) is True,
        "visual_symbol_registry_invoked": False,
        "visual_symbol_policy_not_satisfied": True,
    }

    scene_delta_non_eligibility = {
        "schema_version": SCENE_DELTA_SCHEMA,
        "scene_delta_candidate_allowed": False,
        "scene_delta_candidate_generated": False,
        "eligibility_status": "not_eligible_after_gate_chain",
        "blocking_reasons": final_blocking,
        "required_future_gates": [
            "review_decision_gate",
            "ttl_policy_gate",
            "source_validation_gate",
            "user_visible_uncertainty_gate",
            "conflict_detection_gate",
            "stale_detection_gate",
        ],
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "fusion_gate_chain_closure_ready": not bool(errs),
        "fusion_candidate_count": 1,
        "queue_item_count": 1,
        "ttl_gate_evaluated_count": 1,
        "policy_gate_evaluated_count": 1,
        "final_hold_for_review_count": 1,
        "approval_granted_count": 0,
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
        "not_review_approval": True,
        "not_ttl_approval": True,
        "not_policy_approval": True,
        "not_scene_delta_candidate_ready": True,
        "not_fusion_fact": True,
        "not_commercial_temporal_fact_write": True,
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
        "poster_real_ocr_fusion_gate_chain_closure_executed": True,
        "closure_only": True,
        "no_new_capability_added": True,
        "gate_chain_status": "closed_for_gate_chain_evaluation",
        "final_gate_chain_decision": "hold_for_review",
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
        "closure_scope": "fusion_gate_chain_closure_only",
        "gate_chain_status": "closed_for_gate_chain_evaluation",
        "based_on_fusion_candidate_dryrun": dryrun.is_dir(),
        "based_on_review_queue": queue_root.is_dir(),
        "based_on_ttl_gate": ttl_root.is_dir(),
        "based_on_policy_gate": policy_root.is_dir(),
        "based_on_reference_closure": closure.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "fusion_candidate_count": 1,
        "queue_item_count": 1,
        "ttl_gate_evaluated_count": 1,
        "policy_gate_evaluated_count": 1,
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
        phase_matrix,
        lineage_report,
        decision_matrix,
        blocking_rollup,
        review_approval,
        ttl_closure,
        policy_closure,
        commercial_temporal,
        visual_boundary,
        scene_delta_non_eligibility,
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
