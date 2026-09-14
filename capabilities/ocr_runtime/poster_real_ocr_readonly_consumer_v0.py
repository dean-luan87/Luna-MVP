# -*- coding: utf-8 -*-
"""Read-only consumer for Poster layout text evidence candidate.

Phase-Poster-Real-OCR-ReadOnly-Consumer-001
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Poster-Real-OCR-ReadOnly-Consumer-001"
REGION_ORDER = ("title_area", "body_text_area", "price_or_promo_area", "time_location_area")

SUMMARY_SCHEMA = "poster_real_ocr_readonly_consumer_summary_v0"
VIEW_SCHEMA = "poster_real_ocr_region_text_consumer_view_v0"
MATRIX_SCHEMA = "poster_real_ocr_region_text_matrix_v0"
INDEXES_SCHEMA = "poster_real_ocr_readonly_consumer_indexes_v0"
TTL_RISK_SCHEMA = "poster_real_ocr_readonly_ttl_risk_report_v0"
READING_GUARD_SCHEMA = "poster_real_ocr_readonly_reading_order_guard_v0"
VISUAL_SEP_SCHEMA = "poster_real_ocr_readonly_visual_track_separation_check_v0"
METRICS_SCHEMA = "poster_real_ocr_readonly_metrics_update_candidate_report_v0"
BENCHMARK_SCHEMA = "poster_real_ocr_readonly_benchmark_link_report_v0"
HEALTH_SCHEMA = "poster_real_ocr_readonly_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_readonly_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_readonly_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_readonly_non_claims_report_v0"
AUDIT_SCHEMA = "poster_real_ocr_readonly_audit_v0"
FOLLOWUPS_SCHEMA = "poster_real_ocr_readonly_open_followups_v0"


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


def _preview(text: str, max_len: int = 80) -> str:
    t = str(text or "")
    return t if len(t) <= max_len else t[: max_len - 3] + "..."


def _commercial_or_temporal_risk(region_id: str, risk_flags: List[str]) -> bool:
    if region_id in ("price_or_promo_area", "time_location_area"):
        return True
    return any(
        f in risk_flags
        for f in ("commercial_text_may_expire", "temporal_text_requires_ttl")
    )


def run_poster_real_ocr_readonly_consumer_v0(
    *,
    poster_real_ocr_gated_execution_root: str,
    poster_reference_only_root: str,
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
    ref_root = Path(poster_reference_only_root).resolve()
    track_b = Path(poster_track_b_closure_root).resolve()
    bench_root = Path(benchmark_real_values_smoke_root).resolve()
    health_root = Path(system_health_governance_root).resolve()
    sim_root = Path(simulation_lab_harness_root).resolve()

    if not _source_ok(ocr_root, "poster_real_ocr_gated_execution_summary.json"):
        errs.append("poster_real_ocr_gated_execution_not_ok")

    evidence_doc = _read_json(ocr_root / "poster_layout_text_evidence_candidate.json") or {}
    matrix_doc = _read_json(ocr_root / "poster_real_ocr_result_matrix.json") or {}
    ref_summary = _read_json(ref_root / "cross_modal_poster_ocr_reference_only_summary.json") or {}
    track_summary = _read_json(track_b / "poster_testboard_track_b_closure_summary.json") or {}

    region_evidence = [
        r for r in (evidence_doc.get("region_text_evidence") or []) if isinstance(r, dict)
    ]
    by_region: Dict[str, Dict[str, Any]] = {
        str(r.get("source_region_id")): r for r in region_evidence if r.get("source_region_id")
    }

    text_items_by_region: Dict[str, List[Any]] = {}
    for row in matrix_doc.get("rows") or []:
        if not isinstance(row, dict):
            continue
        rid = str(row.get("source_region_id") or "")
        if rid:
            text_items_by_region[rid] = list(row.get("text_items") or [])

    missing_regions = [rid for rid in REGION_ORDER if rid not in by_region]
    if missing_regions:
        errs.append(f"missing_regions:{','.join(missing_regions)}")

    non_empty = sum(1 for rid in REGION_ORDER if rid in by_region and not by_region[rid].get("empty_text"))
    empty_count = sum(1 for rid in REGION_ORDER if rid in by_region and by_region[rid].get("empty_text"))
    ttl_count = sum(1 for rid in REGION_ORDER if rid in by_region and by_region[rid].get("ttl_required"))

    consumer_items: List[Dict[str, Any]] = []
    matrix_rows: List[Dict[str, Any]] = []
    risk_by_region: Dict[str, List[str]] = {}

    for pos, rid in enumerate(REGION_ORDER):
        ev = by_region.get(rid, {})
        risk_flags = list(ev.get("risk_flags") or [])
        risk_by_region[rid] = risk_flags
        tj = str(ev.get("text_joined") or "")
        items = text_items_by_region.get(rid, [])
        consumer_items.append(
            {
                "consumer_item_id": f"pci_{rid}",
                "evidence_id": str(ev.get("evidence_id") or f"ev_{rid}_missing"),
                "source_region_id": rid,
                "region_type": rid,
                "text_joined": tj,
                "text_items": items,
                "empty_text": bool(ev.get("empty_text", not tj.strip())),
                "provider": str(ev.get("provider") or "unknown"),
                "ttl_required": bool(ev.get("ttl_required")),
                "risk_flags": risk_flags,
                "reading_order_position": pos,
                "fact_status": "not_fact",
                "write_allowed": False,
                "requires_review": True,
                "source_chain": list(ev.get("source_chain") or []),
            }
        )
        matrix_rows.append(
            {
                "region_id": rid,
                "region_type": rid,
                "has_text": not bool(ev.get("empty_text", not tj.strip())),
                "text_item_count": len(items),
                "text_joined_preview": _preview(tj),
                "provider": str(ev.get("provider") or "unknown"),
                "empty_text": bool(ev.get("empty_text", not tj.strip())),
                "ttl_required": bool(ev.get("ttl_required")),
                "commercial_or_temporal_risk": _commercial_or_temporal_risk(rid, risk_flags),
                "semantic_join_allowed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    # Indexes
    evidence_by_region_id: Dict[str, str] = {}
    evidence_by_provider: Dict[str, List[str]] = defaultdict(list)
    evidence_by_ttl_required: Dict[str, List[str]] = {"true": [], "false": []}
    evidence_by_empty_text: Dict[str, List[str]] = {"true": [], "false": []}
    evidence_by_risk_flag: Dict[str, List[str]] = defaultdict(list)
    evidence_by_fact_status: Dict[str, List[str]] = defaultdict(list)

    for item in consumer_items:
        eid = item["evidence_id"]
        rid = item["source_region_id"]
        evidence_by_region_id[rid] = eid
        evidence_by_provider[item["provider"]].append(eid)
        evidence_by_ttl_required["true" if item["ttl_required"] else "false"].append(eid)
        evidence_by_empty_text["true" if item["empty_text"] else "false"].append(eid)
        evidence_by_fact_status["not_fact"].append(eid)
        for rf in item.get("risk_flags") or []:
            evidence_by_risk_flag[str(rf)].append(eid)

    indexes = {
        "schema_version": INDEXES_SCHEMA,
        "evidence_by_region_id": evidence_by_region_id,
        "evidence_by_provider": dict(evidence_by_provider),
        "evidence_by_ttl_required": dict(evidence_by_ttl_required),
        "evidence_by_empty_text": dict(evidence_by_empty_text),
        "evidence_by_risk_flag": dict(evidence_by_risk_flag),
        "evidence_by_fact_status": dict(evidence_by_fact_status),
        "index_only": True,
        "evidence_mutated": False,
    }

    ttl_risk = {
        "schema_version": TTL_RISK_SCHEMA,
        "ttl_required_region_count": ttl_count,
        "commercial_text_may_expire_present": "commercial_text_may_expire"
        in (risk_by_region.get("price_or_promo_area") or []),
        "temporal_text_requires_ttl_present": "temporal_text_requires_ttl"
        in (risk_by_region.get("time_location_area") or []),
        "world_model_write_allowed": False,
        "fact_write_allowed": False,
        "requires_review_before_future_write": True,
        "risk_flags_by_region": risk_by_region,
    }

    reading_guard = {
        "schema_version": READING_GUARD_SCHEMA,
        "reading_order_confidence": str(evidence_doc.get("reading_order_confidence") or "low"),
        "semantic_join_allowed": False,
        "semantic_join_invoked": False,
        "cross_region_text_joined": False,
        "force_semantic_join_allowed": False,
        "region_order_preserved": list(REGION_ORDER),
        "interpretation_allowed": False,
        "reason_codes": [
            "complex_layout",
            "reading_order_uncertain",
            "real_ocr_candidate_not_fact",
        ],
    }

    vis_count = int(ref_summary.get("visual_symbol_reference_count") or 4)
    visual_sep = {
        "schema_version": VISUAL_SEP_SCHEMA,
        "poster_reference_only_root": str(ref_root),
        "poster_track_b_closure_root": str(track_b),
        "visual_symbol_track_exists": bool(ref_summary.get("based_on_visual_symbol_evidence")),
        "visual_symbol_region_count": vis_count,
        "visual_regions_consumed_by_this_phase": False,
        "logo_ocr_invoked": False,
        "qr_ocr_invoked": False,
        "product_ocr_invoked": False,
        "background_ocr_invoked": False,
        "qr_decoded": False,
        "brand_identity_confirmed": False,
        "visual_symbol_registry_invoked": False,
        "text_visual_overlap": False,
        "track_b_text_track_status": track_summary.get("text_track_status"),
        "track_b_visual_track_status": track_summary.get("visual_track_status"),
    }

    provider_dist = Counter(item["provider"] for item in consumer_items)
    metrics = {
        "schema_version": METRICS_SCHEMA,
        "poster_ocr_readonly_consumer_ready": True,
        "poster_ocr_region_count": len(REGION_ORDER),
        "poster_ocr_non_empty_region_count": non_empty,
        "poster_ocr_empty_region_count": empty_count,
        "poster_ocr_ttl_required_region_count": ttl_count,
        "poster_ocr_provider_distribution": dict(provider_dist),
        "poster_ocr_accuracy_computed": False,
        "ocr_accuracy_computed": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "future_collector_update_required": True,
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
        "no_scene_delta_world_model_write": True,
        "no_navigation": True,
        "not_production_ready": True,
    }

    followups = {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": ["Phase-Poster-Real-OCR-Reference-Update-001"],
        "item_count": 1,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "poster_real_ocr_readonly_consumer_executed": True,
        "readonly_consumer": True,
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

    phase_hint = "GO"
    if empty_count == len(REGION_ORDER) and not errs:
        phase_hint = "CONDITIONAL_GO"
    elif errs:
        phase_hint = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "consumer_scope": "readonly_consumer",
        "based_on_poster_real_ocr": True,
        "based_on_poster_reference_only": ref_root.is_dir(),
        "based_on_poster_track_b_closure": track_b.is_dir(),
        "based_on_benchmark_real_values_smoke": bench_root.is_dir(),
        "based_on_system_health_governance": health_root.is_dir(),
        "simulation_context_attached": sim_root.is_dir(),
        "evidence_count_observed": len(region_evidence),
        "region_count_observed": len([r for r in REGION_ORDER if r in by_region]),
        "non_empty_region_count": non_empty,
        "empty_region_count": empty_count,
        "ttl_required_region_count": ttl_count,
        "ocr_reinvoked": False,
        "rapidocr_reinvoked": False,
        "paddleocr_invoked": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
        "fact_status_summary": {"not_fact": len(consumer_items)},
        "write_allowed": False,
        "runtime_routing_changed": False,
        "poster_real_ocr_gated_execution_root": str(ocr_root),
        "phase_verdict_hint": phase_hint,
    }

    view = {
        "schema_version": VIEW_SCHEMA,
        "consumer_item_count": len(consumer_items),
        "items": consumer_items,
        "region_order": list(REGION_ORDER),
    }

    matrix_out = {
        "schema_version": MATRIX_SCHEMA,
        "row_count": len(matrix_rows),
        "rows": matrix_rows,
    }

    return (
        summary,
        view,
        matrix_out,
        indexes,
        ttl_risk,
        reading_guard,
        visual_sep,
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
