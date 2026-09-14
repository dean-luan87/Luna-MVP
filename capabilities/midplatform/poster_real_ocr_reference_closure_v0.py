# -*- coding: utf-8 -*-
"""Poster Real OCR reference chain closure (aggregate only; no new capability).

Phase-Poster-Real-OCR-Reference-Closure-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Poster-Real-OCR-Reference-Closure-001"
TEXT_REGION_IDS = ("title_area", "body_text_area", "price_or_promo_area", "time_location_area")
VISUAL_REGION_IDS = ("logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area")

SUMMARY_SCHEMA = "poster_real_ocr_reference_closure_summary_v0"
PHASE_MATRIX_SCHEMA = "poster_real_ocr_reference_closure_phase_matrix_v0"
LINEAGE_SCHEMA = "poster_real_ocr_reference_lineage_closure_report_v0"
TRACK_SCHEMA = "poster_real_ocr_reference_track_closure_matrix_v0"
ALIGNMENT_SCHEMA = "poster_real_ocr_reference_alignment_closure_report_v0"
VISUAL_CLOSURE_SCHEMA = "poster_real_ocr_reference_visual_symbol_closure_report_v0"
READING_SCHEMA = "poster_real_ocr_reference_reading_order_closure_report_v0"
TTL_SCHEMA = "poster_real_ocr_reference_ttl_risk_closure_report_v0"
METRICS_SCHEMA = "poster_real_ocr_reference_metrics_closure_candidate_report_v0"
BENCHMARK_SCHEMA = "poster_real_ocr_reference_closure_benchmark_link_report_v0"
HEALTH_SCHEMA = "poster_real_ocr_reference_closure_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_reference_closure_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_reference_closure_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_reference_closure_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "poster_real_ocr_reference_closure_open_followups_v0"
AUDIT_SCHEMA = "poster_real_ocr_reference_closure_audit_v0"

PHASE_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "phase_key": "poster_layout_governance",
        "phase_name": "OCR-Poster-Layout-Segmentation-Governance-001",
        "summary_file": "poster_layout_governance_summary.json",
        "verifier_file": None,
        "source_scope": "layout_segmentation_governance",
        "contribution_to_closure": "layout_regions_and_gate_policy",
    },
    {
        "phase_key": "poster_region_ocr_plan",
        "phase_name": "OCR-Poster-Region-OCR-Plan-Stub-001",
        "summary_file": "poster_region_ocr_plan_stub_summary.json",
        "verifier_file": None,
        "source_scope": "region_ocr_plan_stub",
        "contribution_to_closure": "text_region_ocr_plan_lineage",
    },
    {
        "phase_key": "poster_visual_symbol_evidence",
        "phase_name": "OCR-Poster-VisualSymbolEvidence-Stub-001",
        "summary_file": "poster_visual_symbol_evidence_stub_summary.json",
        "verifier_file": None,
        "source_scope": "visual_symbol_evidence_stub",
        "contribution_to_closure": "visual_symbol_track_lineage",
    },
    {
        "phase_key": "original_poster_reference_only",
        "phase_name": "CrossModal-Poster-OCR-ReferenceOnly-001",
        "summary_file": "cross_modal_poster_ocr_reference_only_summary.json",
        "verifier_file": "cross_modal_poster_reference_only_verifier_report.json",
        "source_scope": "reference_only_parallel_index",
        "contribution_to_closure": "original_text_and_visual_reference",
    },
    {
        "phase_key": "poster_real_ocr_gated_execution",
        "phase_name": "Poster-Real-OCR-Gated-Execution-001",
        "summary_file": "poster_real_ocr_gated_execution_summary.json",
        "verifier_file": "poster_real_ocr_verifier_report.json",
        "source_scope": "gated_real_ocr_smoke",
        "contribution_to_closure": "real_ocr_text_evidence_generation",
    },
    {
        "phase_key": "poster_real_ocr_readonly_consumer",
        "phase_name": "Poster-Real-OCR-ReadOnly-Consumer-001",
        "summary_file": "poster_real_ocr_readonly_consumer_summary.json",
        "verifier_file": "poster_real_ocr_readonly_verifier_report.json",
        "source_scope": "readonly_consumer",
        "contribution_to_closure": "readonly_consumer_index",
    },
    {
        "phase_key": "poster_real_ocr_reference_update",
        "phase_name": "Poster-Real-OCR-Reference-Update-001",
        "summary_file": "poster_real_ocr_reference_update_summary.json",
        "verifier_file": "poster_real_ocr_reference_update_verifier_report.json",
        "source_scope": "reference_only_update",
        "contribution_to_closure": "parallel_reference_update",
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
    for spec in PHASE_SPECS:
        key = spec["phase_key"]
        root = roots[key]
        verdict, blockers = _verdict_from_root(root, spec)
        sm = _read_json(root / str(spec["summary_file"])) or {}
        ok = verdict in ("GO", "CONDITIONAL_GO") and not blockers
        if not ok:
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
            }
        )
    return {"schema_version": PHASE_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}, errs


def run_poster_real_ocr_reference_closure_v0(
    *,
    poster_layout_governance_root: str,
    poster_region_ocr_plan_root: str,
    poster_visual_symbol_evidence_root: str,
    poster_original_reference_only_root: str,
    poster_track_b_closure_root: str,
    poster_real_ocr_gated_execution_root: str,
    poster_real_ocr_readonly_consumer_root: str,
    poster_real_ocr_reference_update_root: str,
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
    out = Path(output_root).resolve()
    layout = Path(poster_layout_governance_root).resolve()
    plan = Path(poster_region_ocr_plan_root).resolve()
    visual = Path(poster_visual_symbol_evidence_root).resolve()
    orig_ref = Path(poster_original_reference_only_root).resolve()
    track_b = Path(poster_track_b_closure_root).resolve()
    ocr_exec = Path(poster_real_ocr_gated_execution_root).resolve()
    consumer = Path(poster_real_ocr_readonly_consumer_root).resolve()
    ref_upd = Path(poster_real_ocr_reference_update_root).resolve()
    bench = Path(benchmark_real_values_smoke_root).resolve()
    health = Path(system_health_governance_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()

    roots = {
        "poster_layout_governance": layout,
        "poster_region_ocr_plan": plan,
        "poster_visual_symbol_evidence": visual,
        "original_poster_reference_only": orig_ref,
        "poster_real_ocr_gated_execution": ocr_exec,
        "poster_real_ocr_readonly_consumer": consumer,
        "poster_real_ocr_reference_update": ref_upd,
    }

    phase_matrix, phase_errs = _build_phase_matrix(roots)
    errs.extend(phase_errs)

    ref_upd_summary = _read_json(ref_upd / "poster_real_ocr_reference_update_summary.json") or {}
    ref_candidate = _read_json(ref_upd / "poster_real_ocr_updated_reference_candidate.json") or {}
    alignment = _read_json(ref_upd / "poster_real_ocr_text_plan_alignment_matrix.json") or {}
    reading_upd = _read_json(ref_upd / "poster_real_ocr_reference_update_reading_order_guard.json") or {}
    ttl_upd = _read_json(ref_upd / "poster_real_ocr_reference_update_ttl_risk_report.json") or {}
    visual_preserve = _read_json(
        ref_upd / "poster_real_ocr_visual_symbol_reference_preservation_report.json"
    ) or {}

    plan_count = int(ref_upd_summary.get("original_text_plan_ref_count") or 0)
    real_count = int(ref_upd_summary.get("real_ocr_text_evidence_ref_count") or 0)
    vis_count = int(ref_upd_summary.get("visual_symbol_ref_count") or 0)
    aligned = int(alignment.get("aligned_region_count") or 0)
    ttl_count = int(ttl_upd.get("ttl_required_region_count") or 2)

    if plan_count != 4 or real_count != 4 or vis_count != 4 or aligned != 4:
        errs.append("ref_counts_mismatch")

    lineage_path = out / "poster_real_ocr_reference_lineage_closure_report.json"
    closure_ref = str(lineage_path)

    text_lineage: List[Dict[str, Any]] = []
    real_by_region = {
        str(r.get("source_region_id")): r
        for r in (ref_candidate.get("real_ocr_text_evidence_refs") or [])
        if isinstance(r, dict)
    }
    for rid in TEXT_REGION_IDS:
        text_lineage.append(
            {
                "source_region_id": rid,
                "layout_region_ref": str(layout / "poster_text_region_candidates.json"),
                "ocr_plan_ref": str(plan / "poster_region_ocr_plan_stub.json"),
                "real_ocr_execution_ref": str(ocr_exec / "poster_layout_text_evidence_candidate.json"),
                "readonly_consumer_ref": str(consumer / "poster_real_ocr_region_text_consumer_view.json"),
                "reference_update_ref": str(ref_upd / "poster_real_ocr_updated_reference_candidate.json"),
                "final_closure_ref": closure_ref,
                "real_ocr_evidence_id": (real_by_region.get(rid) or {}).get("evidence_id"),
            }
        )

    vis_by_region = {
        str(r.get("source_region_id")): r
        for r in (ref_candidate.get("visual_symbol_refs") or [])
        if isinstance(r, dict)
    }
    visual_lineage: List[Dict[str, Any]] = []
    for rid in VISUAL_REGION_IDS:
        visual_lineage.append(
            {
                "source_region_id": rid,
                "visual_symbol_evidence_ref": str(visual / "poster_visual_symbol_evidence_items.json"),
                "original_reference_ref": str(orig_ref / "cross_modal_poster_reference_candidate.json"),
                "reference_update_ref": str(ref_upd / "poster_real_ocr_updated_reference_candidate.json"),
                "final_closure_ref": closure_ref,
                "evidence_id": (vis_by_region.get(rid) or {}).get("evidence_id"),
            }
        )

    lineage = {
        "schema_version": LINEAGE_SCHEMA,
        "text_main_chain": [
            "layout_governance",
            "region_ocr_plan",
            "real_ocr_gated_execution",
            "readonly_consumer",
            "reference_update",
            "reference_closure",
        ],
        "visual_side_chain": [
            "layout_governance",
            "visual_symbol_evidence",
            "original_reference_only",
            "reference_update",
            "reference_closure",
        ],
        "text_region_lineage": text_lineage,
        "visual_region_lineage": visual_lineage,
        "poster_track_b_closure_ref": str(track_b / "poster_testboard_track_b_closure_summary.json"),
    }

    track_matrix = {
        "schema_version": TRACK_SCHEMA,
        "tracks": [
            {
                "track_name": "text_plan_track",
                "ref_count": plan_count,
                "status": "preserved",
                "semantic_join_allowed": False,
                "fusion_allowed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "track_name": "real_ocr_text_track",
                "ref_count": real_count,
                "status": "reference_ready",
                "semantic_join_allowed": False,
                "fusion_allowed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
            {
                "track_name": "visual_symbol_track",
                "ref_count": vis_count,
                "status": "preserved_not_text",
                "semantic_join_allowed": False,
                "fusion_allowed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            },
        ],
    }

    alignment_closure = {
        "schema_version": ALIGNMENT_SCHEMA,
        "aligned_region_count": aligned,
        "alignment_strategy": "aligned_by_region_id",
        "all_text_regions_aligned": aligned == 4,
        "accuracy_computed": False,
        "ground_truth_available": False,
        "empty_text_allowed": True,
        "non_empty_text_not_accuracy": True,
        "source_alignment_matrix_ref": str(ref_upd / "poster_real_ocr_text_plan_alignment_matrix.json"),
    }

    visual_closure = {
        "schema_version": VISUAL_CLOSURE_SCHEMA,
        "visual_symbol_ref_count": vis_count,
        "visual_symbol_track_preserved": bool(visual_preserve.get("visual_symbol_refs_preserved")),
        "visual_symbols_consumed_as_text": False,
        "logo_area_ocr_invoked": False,
        "qr_area_ocr_invoked": False,
        "product_area_ocr_invoked": False,
        "background_area_ocr_invoked": False,
        "qr_decoded": False,
        "brand_identity_confirmed": False,
        "visual_symbol_registry_invoked": False,
        "commercial_symbol_not_fact": True,
    }

    reading_closure = {
        "schema_version": READING_SCHEMA,
        "reading_order_confidence": str(reading_upd.get("reading_order_confidence") or "low"),
        "force_semantic_join_allowed": False,
        "semantic_join_invoked": False,
        "cross_region_text_joined": False,
        "interpretation_allowed": False,
        "reason_codes": [
            "complex_layout",
            "reading_order_uncertain",
            "real_ocr_candidate_not_fact",
            "closure_only",
        ],
    }

    ttl_closure = {
        "schema_version": TTL_SCHEMA,
        "ttl_required_region_count": ttl_count,
        "price_or_promo_area_ttl_required": True,
        "time_location_area_ttl_required": True,
        "commercial_text_may_expire_present": bool(ttl_upd.get("commercial_text_may_expire_present")),
        "temporal_text_requires_ttl_present": bool(ttl_upd.get("temporal_text_requires_ttl_present")),
        "world_model_write_allowed": False,
        "fact_write_allowed": False,
        "requires_review_before_future_write": True,
    }

    metrics = {
        "schema_version": METRICS_SCHEMA,
        "poster_real_ocr_reference_closure_ready": not bool(errs),
        "original_text_plan_ref_count": plan_count,
        "real_ocr_text_evidence_ref_count": real_count,
        "visual_symbol_ref_count": vis_count,
        "aligned_region_count": aligned,
        "ttl_required_region_count": ttl_count,
        "semantic_join_blocked": True,
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
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "no_semantic_join": True,
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
            "Poster real OCR fusion candidate dry-run later",
            "Poster TTL policy gate later",
            "Poster reading order governance v1 later",
            "Poster ground truth fixture later",
            "Poster OCR accuracy metric later",
            "VisualSymbolRegistry integration later",
            "QR decode governance later",
            "Brand identity governance later",
            "Scene Delta candidate dry-run later",
            "WorldModel write readiness gate later",
        ],
        "item_count": 10,
    }

    audit = {
        "schema_version": AUDIT_SCHEMA,
        "poster_real_ocr_reference_closure_executed": True,
        "closure_only": True,
        "no_new_capability_added": True,
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

    empty_real = sum(1 for r in real_by_region.values() if r.get("empty_text"))
    phase_hint = "GO" if not errs else "NO_GO"
    if not errs and empty_real == 4:
        phase_hint = "CONDITIONAL_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "closure_scope": "reference_chain_closure_only",
        "poster_real_ocr_reference_status": "closed_for_reference_evaluation",
        "based_on_layout_governance": layout.is_dir(),
        "based_on_region_ocr_plan": plan.is_dir(),
        "based_on_visual_symbol_evidence": visual.is_dir(),
        "based_on_original_reference_only": orig_ref.is_dir(),
        "based_on_real_ocr_execution": ocr_exec.is_dir(),
        "based_on_readonly_consumer": consumer.is_dir(),
        "based_on_reference_update": ref_upd.is_dir(),
        "simulation_context_attached": sim.is_dir(),
        "original_text_plan_ref_count": plan_count,
        "real_ocr_text_evidence_ref_count": real_count,
        "visual_symbol_ref_count": vis_count,
        "aligned_region_count": aligned,
        "ttl_required_region_count": ttl_count,
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
        track_matrix,
        alignment_closure,
        visual_closure,
        reading_closure,
        ttl_closure,
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
