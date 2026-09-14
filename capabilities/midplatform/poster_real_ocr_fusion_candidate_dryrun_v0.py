# -*- coding: utf-8 -*-
"""Poster Real OCR fusion candidate dry-run (candidate only; not committed fusion).

Phase-Poster-Real-OCR-Fusion-Candidate-DryRun-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

PHASE_ID = "Poster-Real-OCR-Fusion-Candidate-DryRun-001"
TEXT_REGION_IDS = ("title_area", "body_text_area", "price_or_promo_area", "time_location_area")
VISUAL_REGION_IDS = ("logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area")

ROLE_IN_CANDIDATE = {
    "title_area": "poster_title_candidate",
    "body_text_area": "poster_body_text_candidate",
    "price_or_promo_area": "promo_or_price_candidate",
    "time_location_area": "temporal_or_location_candidate",
}

SUMMARY_SCHEMA = "poster_real_ocr_fusion_candidate_dryrun_summary_v0"
FUSION_CANDIDATE_SCHEMA = "poster_real_ocr_fusion_candidate_v0"
INPUT_MATRIX_SCHEMA = "poster_real_ocr_fusion_input_matrix_v0"
VISUAL_CTX_SCHEMA = "poster_real_ocr_fusion_visual_context_matrix_v0"
HYPOTHESIS_SCHEMA = "poster_real_ocr_fusion_hypothesis_matrix_v0"
READING_SCHEMA = "poster_real_ocr_fusion_reading_order_guard_v0"
TTL_SCHEMA = "poster_real_ocr_fusion_ttl_commercial_risk_report_v0"
REVIEW_SCHEMA = "poster_real_ocr_fusion_review_requirement_report_v0"
CHAIN_SCHEMA = "poster_real_ocr_fusion_source_chain_report_v0"
METRICS_SCHEMA = "poster_real_ocr_fusion_metrics_candidate_report_v0"
BENCHMARK_SCHEMA = "poster_real_ocr_fusion_benchmark_link_report_v0"
HEALTH_SCHEMA = "poster_real_ocr_fusion_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_fusion_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_fusion_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_fusion_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "poster_real_ocr_fusion_open_followups_v0"
AUDIT_SCHEMA = "poster_real_ocr_fusion_audit_v0"


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


def run_poster_real_ocr_fusion_candidate_dryrun_v0(
    *,
    poster_real_ocr_reference_update_root: str,
    poster_real_ocr_reference_closure_root: str,
    poster_real_ocr_readonly_consumer_root: str,
    poster_real_ocr_gated_execution_root: str,
    poster_visual_symbol_evidence_root: str,
    poster_track_b_closure_root: str,
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
    ref_upd = Path(poster_real_ocr_reference_update_root).resolve()
    closure = Path(poster_real_ocr_reference_closure_root).resolve()
    consumer = Path(poster_real_ocr_readonly_consumer_root).resolve()
    ocr_exec = Path(poster_real_ocr_gated_execution_root).resolve()
    visual = Path(poster_visual_symbol_evidence_root).resolve()
    track_b = Path(poster_track_b_closure_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()
    out = Path(output_root).resolve()

    if not _source_ok(ref_upd, "poster_real_ocr_reference_update_summary.json"):
        errs.append("reference_update_not_ok")
    if not _source_ok(closure, "poster_real_ocr_reference_closure_summary.json"):
        errs.append("reference_closure_not_ok")

    ref_candidate = _read_json(ref_upd / "poster_real_ocr_updated_reference_candidate.json") or {}
    lineage = _read_json(closure / "poster_real_ocr_reference_lineage_closure_report.json") or {}
    consumer_view = _read_json(consumer / "poster_real_ocr_region_text_consumer_view.json") or {}
    vis_items_doc = _read_json(visual / "poster_visual_symbol_evidence_items.json") or {}
    ttl_upd = _read_json(ref_upd / "poster_real_ocr_reference_update_ttl_risk_report.json") or {}

    real_by_region = {
        str(r.get("source_region_id")): r
        for r in (ref_candidate.get("real_ocr_text_evidence_refs") or [])
        if isinstance(r, dict)
    }
    vis_by_region = {
        str(it.get("source_region_id")): it
        for it in (vis_items_doc.get("items") or [])
        if isinstance(it, dict)
    }
    vis_refs_from_candidate = {
        str(r.get("source_region_id")): r
        for r in (ref_candidate.get("visual_symbol_refs") or [])
        if isinstance(r, dict)
    }

    lineage_by_text = {
        str(t.get("source_region_id")): t
        for t in (lineage.get("text_region_lineage") or [])
        if isinstance(t, dict)
    }

    ref_candidate_path = str(ref_upd / "poster_real_ocr_updated_reference_candidate.json")
    closure_path = str(closure / "poster_real_ocr_reference_lineage_closure_report.json")

    layout_region_refs = [
        str(lineage_by_text.get(rid, {}).get("layout_region_ref") or "")
        for rid in TEXT_REGION_IDS
    ]

    fusion_input_rows: List[Dict[str, Any]] = []
    for rid in TEXT_REGION_IDS:
        cons_item = next(
            (it for it in (consumer_view.get("items") or []) if isinstance(it, dict) and it.get("source_region_id") == rid),
            {},
        )
        real_ref = real_by_region.get(rid, {})
        lin = lineage_by_text.get(rid, {})
        fusion_input_rows.append(
            {
                "input_id": f"fusion_in_{rid}",
                "source_region_id": rid,
                "region_type": rid,
                "visual_region_ref": None,
                "real_ocr_evidence_ref": str(real_ref.get("reference_id") or f"real_ocr_ref_{rid}"),
                "text_joined": str(cons_item.get("text_joined") or real_ref.get("text_joined") or ""),
                "empty_text": bool(cons_item.get("empty_text", real_ref.get("empty_text"))),
                "ttl_required": bool(cons_item.get("ttl_required", real_ref.get("ttl_required"))),
                "risk_flags": list(cons_item.get("risk_flags") or real_ref.get("risk_flags") or []),
                "role_in_candidate": ROLE_IN_CANDIDATE[rid],
                "fact_status": "not_fact",
                "write_allowed": False,
                "lineage": {
                    "layout_region_ref": lin.get("layout_region_ref"),
                    "ocr_plan_ref": lin.get("ocr_plan_ref"),
                    "real_ocr_execution_ref": lin.get("real_ocr_execution_ref"),
                    "readonly_consumer_ref": lin.get("readonly_consumer_ref"),
                    "reference_update_ref": lin.get("reference_update_ref"),
                    "reference_closure_ref": lin.get("final_closure_ref"),
                    "fusion_dryrun_ref": str(out / "poster_real_ocr_fusion_candidate.json"),
                },
            }
        )

    visual_ctx_rows: List[Dict[str, Any]] = []
    for rid in VISUAL_REGION_IDS:
        it = vis_by_region.get(rid, {})
        cref = vis_refs_from_candidate.get(rid, {})
        visual_ctx_rows.append(
            {
                "visual_context_id": f"vis_ctx_{rid}",
                "source_region_id": rid,
                "symbol_candidate_type": it.get("symbol_candidate_type") or cref.get("symbol_candidate_type"),
                "semantic_candidate": str(it.get("semantic_candidate") or cref.get("semantic_candidate") or ""),
                "used_as_context": True,
                "consumed_as_text": False,
                "ocr_chain_allowed": False,
                "qr_decoded": False,
                "brand_identity_confirmed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
                "evidence_id": it.get("evidence_id") or cref.get("evidence_id"),
            }
        )

    supporting_all = [r["input_id"] for r in fusion_input_rows] + [r["visual_context_id"] for r in visual_ctx_rows]
    hypothesis_rows = [
        {
            "hypothesis_id": "hyp_poster_like",
            "hypothesis_type": "poster_like_content_candidate",
            "supporting_refs": supporting_all,
            "confidence_placeholder": None,
            "fact_status": "not_fact",
            "requires_review": True,
            "allowed_next_step": "review_queue_later",
        },
        {
            "hypothesis_id": "hyp_commercial",
            "hypothesis_type": "commercial_or_promo_candidate",
            "supporting_refs": ["fusion_in_price_or_promo_area", "fusion_in_body_text_area"],
            "confidence_placeholder": None,
            "fact_status": "not_fact",
            "requires_review": True,
            "allowed_next_step": "ttl_gate_later",
        },
        {
            "hypothesis_id": "hyp_price",
            "hypothesis_type": "price_or_discount_text_candidate",
            "supporting_refs": ["fusion_in_price_or_promo_area"],
            "confidence_placeholder": None,
            "fact_status": "not_fact",
            "requires_review": True,
            "allowed_next_step": "policy_gate_later",
        },
        {
            "hypothesis_id": "hyp_temporal",
            "hypothesis_type": "temporal_validity_text_candidate",
            "supporting_refs": ["fusion_in_time_location_area"],
            "confidence_placeholder": None,
            "fact_status": "not_fact",
            "requires_review": True,
            "allowed_next_step": "ttl_gate_later",
        },
        {
            "hypothesis_id": "hyp_visual_ctx",
            "hypothesis_type": "visual_symbol_context_present",
            "supporting_refs": [r["visual_context_id"] for r in visual_ctx_rows],
            "confidence_placeholder": None,
            "fact_status": "not_fact",
            "requires_review": True,
            "allowed_next_step": "review_queue_later",
        },
        {
            "hypothesis_id": "hyp_brand_unconfirmed",
            "hypothesis_type": "brand_identity_unconfirmed",
            "supporting_refs": ["vis_ctx_logo_area"],
            "confidence_placeholder": None,
            "fact_status": "not_fact",
            "requires_review": True,
            "allowed_next_step": "policy_gate_later",
        },
        {
            "hypothesis_id": "hyp_qr_undecoded",
            "hypothesis_type": "qr_undecoded",
            "supporting_refs": ["vis_ctx_qr_area"],
            "confidence_placeholder": None,
            "fact_status": "not_fact",
            "requires_review": True,
            "allowed_next_step": "policy_gate_later",
        },
        {
            "hypothesis_id": "hyp_review_required",
            "hypothesis_type": "review_required_before_any_fact",
            "supporting_refs": supporting_all,
            "confidence_placeholder": None,
            "fact_status": "not_fact",
            "requires_review": True,
            "allowed_next_step": "review_queue_later",
        },
    ]

    fusion_candidate = {
        "schema_version": FUSION_CANDIDATE_SCHEMA,
        "candidate_scope": "dryrun_only",
        "candidate_type": "poster_commercial_text_candidate",
        "source_reference_candidate_ref": ref_candidate_path,
        "source_lineage_closure_ref": closure_path,
        "layout_region_refs": layout_region_refs,
        "real_ocr_text_evidence_refs": list(ref_candidate.get("real_ocr_text_evidence_refs") or []),
        "visual_symbol_context_refs": list(ref_candidate.get("visual_symbol_refs") or []),
        "candidate_hypothesis": {
            "poster_like_content_candidate": True,
            "commercial_or_promo_candidate": True,
            "temporal_or_validity_text_candidate": True,
            "price_or_discount_text_candidate": True,
            "brand_identity_confirmed": False,
            "qr_decoded": False,
        },
        "confidence": None,
        "requires_review": True,
        "fact_status": "not_fact",
        "write_allowed": False,
        "fusion_committed": False,
    }

    input_matrix = {
        "schema_version": INPUT_MATRIX_SCHEMA,
        "text_input_region_count": len(fusion_input_rows),
        "rows": fusion_input_rows,
    }

    visual_matrix = {
        "schema_version": VISUAL_CTX_SCHEMA,
        "visual_context_count": len(visual_ctx_rows),
        "rows": visual_ctx_rows,
    }

    hypothesis_matrix = {
        "schema_version": HYPOTHESIS_SCHEMA,
        "hypothesis_count": len(hypothesis_rows),
        "rows": hypothesis_rows,
    }

    reading_guard = {
        "schema_version": READING_SCHEMA,
        "reading_order_confidence": "low",
        "cross_region_text_joined": False,
        "semantic_join_committed": False,
        "force_semantic_join_allowed": False,
        "interpretation_allowed": False,
        "fusion_candidate_allowed": True,
        "fusion_fact_allowed": False,
        "reason_codes": [
            "complex_layout",
            "reading_order_uncertain",
            "fusion_dryrun_only",
            "real_ocr_candidate_not_fact",
        ],
    }

    ttl_risk = {
        "schema_version": TTL_SCHEMA,
        "ttl_required_region_count": int(ttl_upd.get("ttl_required_region_count") or 2),
        "price_or_promo_area_ttl_required": True,
        "time_location_area_ttl_required": True,
        "commercial_text_may_expire_present": bool(ttl_upd.get("commercial_text_may_expire_present")),
        "temporal_text_requires_ttl_present": bool(ttl_upd.get("temporal_text_requires_ttl_present")),
        "commercial_claim_status": "candidate_only",
        "temporal_claim_status": "candidate_only",
        "world_model_write_allowed": False,
        "scene_delta_write_allowed": False,
        "requires_ttl_gate_before_future_write": True,
    }

    review_req = {
        "schema_version": REVIEW_SCHEMA,
        "review_required": True,
        "auto_approve_allowed": False,
        "policy_gate_required": True,
        "ttl_gate_required": True,
        "human_or_policy_review_required": True,
        "fact_write_allowed": False,
        "scene_delta_candidate_allowed_in_this_phase": False,
        "next_possible_phase": "Poster-Real-OCR-Fusion-Review-Queue-001",
    }

    source_chain = {
        "schema_version": CHAIN_SCHEMA,
        "reference_update_ref": ref_candidate_path,
        "reference_closure_ref": closure_path,
        "readonly_consumer_ref": str(consumer / "poster_real_ocr_region_text_consumer_view.json"),
        "gated_execution_ref": str(ocr_exec / "poster_layout_text_evidence_candidate.json"),
        "visual_symbol_evidence_ref": str(visual / "poster_visual_symbol_evidence_items.json"),
        "fusion_candidate_build_step": PHASE_ID,
        "fusion_input_lineage_rows": [r.get("lineage") for r in fusion_input_rows],
        "poster_track_b_closure_ref": str(track_b / "poster_testboard_track_b_closure_summary.json"),
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "poster_fusion_candidate_dryrun_ready": not bool(errs),
        "fusion_candidate_count": 1,
        "fusion_committed": False,
        "semantic_join_committed": False,
        "visual_context_count": len(visual_ctx_rows),
        "text_input_region_count": len(fusion_input_rows),
        "ttl_required_region_count": int(ttl_risk.get("ttl_required_region_count") or 2),
        "review_required": True,
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
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
        "semantic_join_committed": False,
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
        "not_fusion_fact": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "no_semantic_join_committed": True,
        "no_scene_delta_candidate": True,
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
            "Poster fusion review queue later",
            "Poster TTL gate later",
            "Poster policy gate later",
            "Scene Delta candidate dry-run later",
            "Poster ground truth fixture later",
            "VisualSymbolRegistry integration later",
            "QR decode governance later",
            "Brand identity governance later",
            "WorldModel write readiness gate later",
            "Benchmark T2 collector later",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "poster_real_ocr_fusion_candidate_dryrun_executed": True,
        "dryrun_only": True,
        "fusion_candidate_generated": True,
        "fusion_committed": False,
        "semantic_join_committed": False,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "full_image_ocr_invoked": False,
        "visual_region_ocr_invoked": False,
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
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

    empty_count = sum(1 for r in fusion_input_rows if r.get("empty_text"))
    phase_hint = "GO" if not errs else "NO_GO"
    if not errs and empty_count == 4:
        phase_hint = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "dryrun_scope": "fusion_candidate_dryrun_only",
        "based_on_reference_update": ref_upd.is_dir(),
        "based_on_reference_closure": closure.is_dir(),
        "based_on_readonly_consumer": consumer.is_dir(),
        "based_on_visual_symbol_evidence": visual.is_dir(),
        "based_on_benchmark_real_values_smoke": bench.is_dir(),
        "based_on_system_health_governance": health.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "fusion_candidate_generated": True,
        "fusion_candidate_count": 1,
        "fusion_committed": False,
        "semantic_join_committed": False,
        "scene_delta_candidate_generated": False,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "phase_verdict_hint": phase_hint,
        "output_root": str(out),
    }

    return (
        summary,
        fusion_candidate,
        input_matrix,
        visual_matrix,
        hypothesis_matrix,
        reading_guard,
        ttl_risk,
        review_req,
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
