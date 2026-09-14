# -*- coding: utf-8 -*-
"""Poster Real OCR reference-only update (parallel refs; no fusion).

Phase-Poster-Real-OCR-Reference-Update-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Poster-Real-OCR-Reference-Update-001"
TEXT_REGION_IDS = ("title_area", "body_text_area", "price_or_promo_area", "time_location_area")
VISUAL_REGION_IDS = ("logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area")

SUMMARY_SCHEMA = "poster_real_ocr_reference_update_summary_v0"
CANDIDATE_SCHEMA = "poster_real_ocr_updated_reference_candidate_v0"
ALIGNMENT_SCHEMA = "poster_real_ocr_text_plan_alignment_matrix_v0"
VISUAL_PRESERVE_SCHEMA = "poster_real_ocr_visual_symbol_reference_preservation_report_v0"
TRACK_SEP_SCHEMA = "poster_real_ocr_reference_update_track_separation_report_v0"
READING_SCHEMA = "poster_real_ocr_reference_update_reading_order_guard_v0"
TTL_SCHEMA = "poster_real_ocr_reference_update_ttl_risk_report_v0"
CHAIN_SCHEMA = "poster_real_ocr_reference_update_source_chain_report_v0"
METRICS_SCHEMA = "poster_real_ocr_reference_update_metrics_candidate_report_v0"
BENCHMARK_SCHEMA = "poster_real_ocr_reference_update_benchmark_link_report_v0"
HEALTH_SCHEMA = "poster_real_ocr_reference_update_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_reference_update_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_reference_update_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_reference_update_non_claims_report_v0"
AUDIT_SCHEMA = "poster_real_ocr_reference_update_audit_v0"
FOLLOWUPS_SCHEMA = "poster_real_ocr_reference_update_open_followups_v0"


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _source_ok(root: Path, summary_name: str) -> bool:
    sm = _read_json(root / summary_name) or {}
    if not sm:
        return False
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    return hint in ("GO", "CONDITIONAL_GO") or sm.get("track_status") == "closed_for_evaluation"


def _plan_ref_id(region_id: str) -> str:
    return f"text_ref_{region_id}"


def _real_ocr_ref_id(region_id: str) -> str:
    return f"real_ocr_ref_{region_id}"


def run_poster_real_ocr_reference_update_v0(
    *,
    poster_real_ocr_gated_execution_root: str,
    poster_real_ocr_readonly_consumer_root: str,
    poster_original_reference_only_root: str,
    poster_visual_symbol_evidence_root: str,
    poster_track_b_closure_root: str,
    benchmark_real_values_smoke_root: str,
    system_health_governance_root: str,
    simulation_lab_harness_root: str,
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
    ocr_root = Path(poster_real_ocr_gated_execution_root).resolve()
    consumer_root = Path(poster_real_ocr_readonly_consumer_root).resolve()
    orig_ref_root = Path(poster_original_reference_only_root).resolve()
    visual_root = Path(poster_visual_symbol_evidence_root).resolve()
    track_b = Path(poster_track_b_closure_root).resolve()
    bench_root = Path(benchmark_real_values_smoke_root).resolve()
    health_root = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()

    if not _source_ok(ocr_root, "poster_real_ocr_gated_execution_summary.json"):
        errs.append("gated_execution_not_ok")
    if not _source_ok(consumer_root, "poster_real_ocr_readonly_consumer_summary.json"):
        errs.append("readonly_consumer_not_ok")
    if not _source_ok(orig_ref_root, "cross_modal_poster_ocr_reference_only_summary.json"):
        errs.append("original_reference_not_ok")

    orig_candidate = _read_json(orig_ref_root / "cross_modal_poster_reference_candidate.json") or {}
    consumer_view = _read_json(consumer_root / "poster_real_ocr_region_text_consumer_view.json") or {}
    evidence_doc = _read_json(ocr_root / "poster_layout_text_evidence_candidate.json") or {}
    reading_consumer = _read_json(consumer_root / "poster_real_ocr_readonly_reading_order_guard.json") or {}
    ttl_consumer = _read_json(consumer_root / "poster_real_ocr_readonly_ttl_risk_report.json") or {}

    plan_root = Path(str(orig_candidate.get("region_ocr_plan_ref") or "")).parent
    plan_doc = _read_json(plan_root / "poster_region_ocr_plan_stub.json") if plan_root.is_dir() else {}
    planned_by_id = {
        str(pr.get("source_region_id")): pr
        for pr in (plan_doc.get("planned_regions") or [])
        if isinstance(pr, dict)
    }

    original_plan_refs = list(orig_candidate.get("text_plan_refs") or [])
    if len(original_plan_refs) != 4:
        text_matrix = _read_json(orig_ref_root / "cross_modal_poster_text_plan_reference_matrix.json") or {}
        original_plan_refs = list(text_matrix.get("rows") or [])
    visual_symbol_refs = list(orig_candidate.get("visual_symbol_refs") or [])

    consumer_by_region: Dict[str, Dict[str, Any]] = {}
    for item in consumer_view.get("items") or []:
        if isinstance(item, dict) and item.get("source_region_id"):
            consumer_by_region[str(item["source_region_id"])] = item

    poster_image_ref = str(
        orig_candidate.get("poster_image_ref")
        or evidence_doc.get("poster_image_ref")
        or ""
    )

    real_ocr_refs: List[Dict[str, Any]] = []
    alignment_rows: List[Dict[str, Any]] = []
    chain_evidence_rows: List[Dict[str, Any]] = []

    for rid in TEXT_REGION_IDS:
        cons = consumer_by_region.get(rid, {})
        plan = planned_by_id.get(rid, {})
        plan_ref = next(
            (r for r in original_plan_refs if isinstance(r, dict) and r.get("source_region_id") == rid),
            {},
        )
        eid = str(cons.get("evidence_id") or f"ev_{rid}_missing")
        real_ref = {
            "reference_id": _real_ocr_ref_id(rid),
            "evidence_id": eid,
            "source_region_id": rid,
            "region_type": rid,
            "provider": str(cons.get("provider") or "unknown"),
            "text_joined": str(cons.get("text_joined") or ""),
            "empty_text": bool(cons.get("empty_text")),
            "ttl_required": bool(cons.get("ttl_required")),
            "risk_flags": list(cons.get("risk_flags") or []),
            "source_chain": list(cons.get("source_chain") or [])
            + ["poster_real_ocr_reference_update"],
            "consumer_item_id": cons.get("consumer_item_id"),
            "gated_execution_ref": str(ocr_root / "poster_layout_text_evidence_candidate.json"),
            "readonly_consumer_ref": str(consumer_root / "poster_real_ocr_region_text_consumer_view.json"),
            "fact_status": "not_fact",
            "write_allowed": False,
        }
        real_ocr_refs.append(real_ref)

        alignment_rows.append(
            {
                "source_region_id": rid,
                "region_type": rid,
                "original_plan_ref_id": str(plan_ref.get("reference_id") or _plan_ref_id(rid)),
                "real_ocr_evidence_id": eid,
                "planned_provider_class": plan_ref.get("planned_provider_class")
                or plan.get("recommended_provider_class"),
                "actual_provider": str(cons.get("provider") or "unknown"),
                "text_joined": str(cons.get("text_joined") or ""),
                "empty_text": bool(cons.get("empty_text")),
                "ttl_required": bool(cons.get("ttl_required")),
                "risk_flags": list(cons.get("risk_flags") or plan_ref.get("risk_flags") or []),
                "alignment_status": "aligned_by_region_id",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

        chain_evidence_rows.append(
            {
                "source_region_id": rid,
                "chain": [
                    str(plan_root / "poster_region_ocr_plan_stub.json"),
                    str(ocr_root / "poster_real_ocr_execution_plan.json"),
                    str(ocr_root / "poster_layout_text_evidence_candidate.json"),
                    str(consumer_root / "poster_real_ocr_region_text_consumer_view.json"),
                    "poster_real_ocr_reference_update",
                ],
                "evidence_id": eid,
            }
        )

    if len(original_plan_refs) != 4:
        errs.append("original_plan_ref_count_not_4")
    if len(real_ocr_refs) != 4:
        errs.append("real_ocr_ref_count_not_4")
    if len(visual_symbol_refs) != 4:
        errs.append("visual_symbol_ref_count_not_4")

    updated_candidate = {
        "schema_version": CANDIDATE_SCHEMA,
        "reference_scope": "reference_only",
        "poster_image_ref": poster_image_ref,
        "original_text_plan_refs": original_plan_refs,
        "real_ocr_text_evidence_refs": real_ocr_refs,
        "visual_symbol_refs": visual_symbol_refs,
        "track_separation": {
            "text_plan_track": "plan_only",
            "real_ocr_text_track": "layout_text_evidence_candidate",
            "visual_symbol_track": "visual_symbol_evidence_candidate",
            "semantic_join_allowed": False,
            "fusion_status": "not_fused",
        },
        "fact_status": "not_fact",
        "write_allowed": False,
        "requires_review": True,
        "original_reference_only_root": str(orig_ref_root),
        "poster_real_ocr_gated_execution_root": str(ocr_root),
        "poster_real_ocr_readonly_consumer_root": str(consumer_root),
    }

    alignment_matrix = {
        "schema_version": ALIGNMENT_SCHEMA,
        "aligned_region_count": len(alignment_rows),
        "rows": alignment_rows,
    }

    visual_preserve = {
        "schema_version": VISUAL_PRESERVE_SCHEMA,
        "visual_symbol_ref_count": len(visual_symbol_refs),
        "visual_symbol_refs_preserved": len(visual_symbol_refs) == 4,
        "visual_symbols_consumed_as_text": False,
        "logo_area_ocr_invoked": False,
        "qr_area_ocr_invoked": False,
        "product_area_ocr_invoked": False,
        "background_area_ocr_invoked": False,
        "qr_decoded": False,
        "brand_identity_confirmed": False,
        "visual_symbol_registry_invoked": False,
        "visual_symbol_evidence_root": str(visual_root),
    }

    track_sep = {
        "schema_version": TRACK_SEP_SCHEMA,
        "text_plan_track_exists": len(original_plan_refs) == 4,
        "real_ocr_text_track_exists": len(real_ocr_refs) == 4,
        "visual_symbol_track_exists": len(visual_symbol_refs) == 4,
        "text_visual_overlap": False,
        "visual_regions_in_real_ocr_text_track": False,
        "logo_qr_in_text_track": False,
        "semantic_join_allowed": False,
        "fusion_invoked": False,
        "reference_only": True,
        "track_b_closure_root": str(track_b),
    }

    reading_guard = {
        "schema_version": READING_SCHEMA,
        "reading_order_confidence": str(
            reading_consumer.get("reading_order_confidence")
            or evidence_doc.get("reading_order_confidence")
            or "low"
        ),
        "semantic_join_allowed": False,
        "semantic_join_invoked": False,
        "cross_region_text_joined": False,
        "force_semantic_join_allowed": False,
        "interpretation_allowed": False,
        "region_order_preserved": list(TEXT_REGION_IDS),
        "inherited_from_readonly_consumer": True,
    }

    ttl_risk = {
        "schema_version": TTL_SCHEMA,
        "ttl_required_region_count": int(ttl_consumer.get("ttl_required_region_count") or 2),
        "price_or_promo_area_ttl_required": True,
        "time_location_area_ttl_required": True,
        "commercial_text_may_expire_present": bool(
            ttl_consumer.get("commercial_text_may_expire_present")
        ),
        "temporal_text_requires_ttl_present": bool(
            ttl_consumer.get("temporal_text_requires_ttl_present")
        ),
        "world_model_write_allowed": False,
        "fact_write_allowed": False,
        "requires_review_before_future_write": True,
        "risk_flags_by_region": ttl_consumer.get("risk_flags_by_region") or {},
    }

    layout_gov = Path(str(orig_candidate.get("layout_governance_ref") or "")).parent
    source_chain = {
        "schema_version": CHAIN_SCHEMA,
        "poster_layout_governance_ref": str(
            layout_gov / "poster_layout_governance_summary.json"
            if layout_gov.is_dir()
            else orig_candidate.get("layout_governance_ref")
        ),
        "poster_region_ocr_plan_ref": str(plan_root / "poster_region_ocr_plan_stub.json"),
        "poster_visual_symbol_evidence_ref": str(
            visual_root / "poster_visual_symbol_evidence_items.json"
        ),
        "original_poster_reference_only_ref": str(
            orig_ref_root / "cross_modal_poster_reference_candidate.json"
        ),
        "poster_real_ocr_gated_execution_ref": str(
            ocr_root / "poster_layout_text_evidence_candidate.json"
        ),
        "poster_real_ocr_readonly_consumer_ref": str(
            consumer_root / "poster_real_ocr_region_text_consumer_view.json"
        ),
        "reference_update_build_step": PHASE_ID,
        "real_ocr_evidence_chain_rows": chain_evidence_rows,
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "poster_real_ocr_reference_update_ready": True,
        "original_text_plan_ref_count": len(original_plan_refs),
        "real_ocr_text_evidence_ref_count": len(real_ocr_refs),
        "visual_symbol_ref_count": len(visual_symbol_refs),
        "aligned_region_count": len(alignment_rows),
        "ttl_required_region_count": int(ttl_risk.get("ttl_required_region_count") or 2),
        "semantic_join_blocked": True,
        "fusion_invoked": False,
        "ocr_accuracy_computed": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "can_feed_future_t1_collector": True,
    }

    benchmark = {
        "schema_version": BENCHMARK_SCHEMA,
        "benchmark_smoke_root": str(bench_root),
        "benchmark_real_values_smoke_available": bench_root.is_dir(),
        "current_phase_updates_benchmark_values": False,
        "can_feed_future_t1_collector": True,
        "t2_quality_values_collected": False,
        "ground_truth_available": False,
        "ocr_accuracy_computed": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
    }

    health = {
        "schema_version": HEALTH_SCHEMA,
        "system_health_governance_root": str(health_root),
        "system_health_governance_available": health_root.is_dir(),
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
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
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
        "full_image_ocr_invoked": False,
        "visual_region_ocr_invoked": False,
    }

    sim_sm = _read_json(sim_root / "simulation_summary.json") or {}
    sim = {
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
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "no_semantic_join": True,
        "no_fusion": True,
        "no_qr_decode": True,
        "no_brand_recognition": True,
        "no_visual_symbol_registry": True,
        "no_scene_delta_candidate": True,
        "no_scene_delta_world_model_write": True,
        "no_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": ["Phase-Poster-Real-OCR-Reference-Closure-001"],
        "item_count": 1,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "poster_real_ocr_reference_update_executed": True,
        "reference_only_update": True,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "full_image_ocr_invoked": False,
        "visual_region_ocr_invoked": False,
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
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

    empty_real = sum(1 for r in real_ocr_refs if r.get("empty_text"))
    phase_hint = "GO"
    if empty_real == 4 and not errs:
        phase_hint = "CONDITIONAL_GO"
    elif errs:
        phase_hint = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "reference_scope": "reference_only_update",
        "based_on_original_poster_reference": True,
        "based_on_real_ocr_readonly_consumer": True,
        "based_on_visual_symbol_evidence": visual_root.is_dir(),
        "based_on_poster_track_b_closure": track_b.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "original_text_plan_ref_count": len(original_plan_refs),
        "real_ocr_text_evidence_ref_count": len(real_ocr_refs),
        "visual_symbol_ref_count": len(visual_symbol_refs),
        "reference_candidate_count": 1,
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
    }

    return (
        summary,
        updated_candidate,
        alignment_matrix,
        visual_preserve,
        track_sep,
        reading_guard,
        ttl_risk,
        source_chain,
        metrics,
        benchmark,
        health,
        boundary,
        sim,
        non_claims,
        followups,
        audit,
        errs,
    )
