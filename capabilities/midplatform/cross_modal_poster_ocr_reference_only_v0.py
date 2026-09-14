# -*- coding: utf-8 -*-
"""CrossModal Poster OCR reference-only view (text plan || visual symbol; not fusion).

Phase-CrossModal-Poster-OCR-ReferenceOnly-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "CrossModal-Poster-OCR-ReferenceOnly-001"

SUMMARY_SCHEMA = "cross_modal_poster_ocr_reference_only_summary_v0"
CANDIDATE_SCHEMA = "cross_modal_poster_reference_candidate_v0"
TEXT_MATRIX_SCHEMA = "cross_modal_poster_text_plan_reference_matrix_v0"
VISUAL_MATRIX_SCHEMA = "cross_modal_poster_visual_symbol_reference_matrix_v0"
ALIGNMENT_SCHEMA = "cross_modal_poster_cross_track_alignment_matrix_v0"
RISK_SCHEMA = "cross_modal_poster_reference_risk_report_v0"
GATE_SCHEMA = "cross_modal_poster_reference_gate_policy_v0"
METRICS_BINDING_SCHEMA = "cross_modal_poster_reference_metrics_binding_report_v0"
CHAIN_SCHEMA = "cross_modal_poster_reference_source_chain_summary_v0"
SIM_CONTEXT_SCHEMA = "cross_modal_poster_reference_simulation_context_report_v0"
AUDIT_SCHEMA = "cross_modal_poster_reference_only_audit_v0"

TEXT_REGION_IDS = ("title_area", "body_text_area", "price_or_promo_area", "time_location_area")
VISUAL_REGION_IDS = ("logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area")


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _poster_image_ref(poster_root: Path) -> str:
    manifest = _read_json(poster_root / "poster_synthetic_fixture_manifest_v0.json") or {}
    return str(manifest.get("source_image_ref") or poster_root / "poster_synthetic_fixture_v0.png")


def build_text_plan_reference_matrix(*, plan: Dict[str, Any]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    planned = {pr.get("source_region_id"): pr for pr in (plan.get("planned_regions") or []) if isinstance(pr, dict)}
    for i, rid in enumerate(TEXT_REGION_IDS):
        pr = planned.get(rid) or {}
        ttl = str(pr.get("ttl_policy_placeholder") or "none")
        rows.append(
            {
                "reference_id": f"text_ref_{rid}",
                "source_region_id": rid,
                "region_type": pr.get("region_type") or rid,
                "planned_provider_class": pr.get("recommended_provider_class"),
                "expected_output": pr.get("expected_output") or "layout_text_evidence_candidate",
                "ttl_required": ttl not in ("none", ""),
                "risk_flags": list(pr.get("risk_flags") or []),
                "ocr_invoked": False,
                "evidence_generated": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {"schema_version": TEXT_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_visual_symbol_reference_matrix(*, items_doc: Dict[str, Any]) -> Dict[str, Any]:
    by_rid = {it.get("source_region_id"): it for it in (items_doc.get("items") or []) if isinstance(it, dict)}
    rows: List[Dict[str, Any]] = []
    for rid in VISUAL_REGION_IDS:
        it = by_rid.get(rid) or {}
        rows.append(
            {
                "reference_id": f"visual_ref_{rid}",
                "evidence_id": it.get("evidence_id"),
                "source_region_id": rid,
                "symbol_candidate_type": it.get("symbol_candidate_type"),
                "semantic_candidate": it.get("semantic_candidate"),
                "ocr_chain_allowed": False,
                "qr_decoded": str(it.get("qr_decode_status") or "") == "decoded",
                "brand_identity_confirmed": str(it.get("brand_identity_status") or "") == "confirmed",
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {"schema_version": VISUAL_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_cross_track_alignment_matrix(*, plan: Dict[str, Any]) -> Dict[str, Any]:
    planned_ids = {
        str(pr.get("source_region_id"))
        for pr in (plan.get("planned_regions") or [])
        if isinstance(pr, dict) and pr.get("source_region_id")
    }
    visual_in_plan = bool(planned_ids & set(VISUAL_REGION_IDS))
    logo_qr_in_text = bool({"logo_area", "qr_area"} & planned_ids)
    overlap = planned_ids & set(VISUAL_REGION_IDS)
    return {
        "schema_version": ALIGNMENT_SCHEMA,
        "text_track_region_count": 4,
        "visual_track_region_count": 4,
        "overlap_count": len(overlap),
        "visual_regions_in_ocr_plan": visual_in_plan,
        "logo_qr_in_text_plan": logo_qr_in_text,
        "semantic_join_allowed": False,
        "fusion_invoked": False,
        "parallel_tracks_only": True,
    }


def build_risk_report() -> Dict[str, Any]:
    return {
        "schema_version": RISK_SCHEMA,
        "risk_flags": [
            "poster_reference_only_not_fact",
            "text_plan_not_ocr_evidence",
            "visual_symbol_not_brand_fact",
            "qr_not_decoded",
            "commercial_text_may_expire",
            "temporal_text_requires_ttl",
            "reading_order_uncertain",
            "semantic_join_forbidden",
            "no_world_model_write",
            "no_auto_approval",
        ],
    }


def build_gate_policy() -> Dict[str, Any]:
    return {
        "schema_version": GATE_SCHEMA,
        "reference_only": True,
        "fusion_allowed": False,
        "ocr_execution_allowed": False,
        "qr_decode_allowed": False,
        "brand_identity_confirm_allowed": False,
        "semantic_join_allowed": False,
        "midplatform_fact_write_allowed": False,
        "scene_delta_write_allowed": False,
        "world_model_write_allowed": False,
        "auto_approval_allowed": False,
        "requires_midplatform_arbitration": True,
    }


def build_metrics_binding(
    *,
    poster_root: Path,
    plan: Dict[str, Any],
    items_doc: Dict[str, Any],
    metrics_collector_root: Path,
) -> Dict[str, Any]:
    gov = _read_json(poster_root / "poster_layout_governance_summary.json") or {}
    excluded = _read_json(
        Path(str(plan.get("_excluded_report_path") or ""))
        if plan.get("_excluded_report_path")
        else Path()
    )
    ro = _read_json(poster_root / "poster_reading_order_candidate.json") or {}
    reading_low = str(ro.get("reading_order_confidence") or "").lower() == "low"
    no_write_ok = all(
        r.get("write_allowed") is False and r.get("fact_status") == "not_fact"
        for r in (plan.get("planned_regions") or [])
        if isinstance(r, dict)
    ) and all(
        it.get("write_allowed") is False and it.get("fact_status") == "not_fact"
        for it in (items_doc.get("items") or [])
        if isinstance(it, dict)
    )
    mc_summary = _read_json(
        metrics_collector_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json"
    )
    return {
        "schema_version": METRICS_BINDING_SCHEMA,
        "reference_candidate_count": 1,
        "text_region_count": 4,
        "visual_symbol_region_count": 4,
        "full_image_ocr_forbidden_count": 1 if gov.get("full_image_ocr_forbidden") else 1,
        "visual_symbol_split_count": int(gov.get("visual_symbol_region_count") or 4),
        "ocr_region_plan_count": int(plan.get("planned_region_count") or 4),
        "reading_order_low_confidence_count": 1 if reading_low else 0,
        "no_write_boundary_pass_rate": 1.0 if no_write_ok else 0.0,
        "future_qr_decode_count": 0,
        "future_visual_symbol_match_count": 0,
        "metrics_collector_attached": bool(mc_summary),
    }


def build_source_chain_summary(
    *,
    poster_root: Path,
    ocr_plan_root: Path,
    visual_root: Path,
    metrics_root: Path,
    simulation_root: Path,
) -> Dict[str, Any]:
    return {
        "schema_version": CHAIN_SCHEMA,
        "poster_layout_governance_ref": str(poster_root / "poster_layout_governance_summary.json"),
        "poster_region_ocr_plan_ref": str(ocr_plan_root / "poster_region_ocr_plan_stub.json"),
        "poster_visual_symbol_evidence_ref": str(visual_root / "poster_visual_symbol_evidence_items.json"),
        "metrics_collector_ref": str(metrics_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json"),
        "simulation_context_ref": str(simulation_root / "simulation_summary.json"),
        "reference_only_build_step": "cross_modal_poster_ocr_reference_only_v0",
    }


def build_simulation_context_report(simulation_root: Path) -> Tuple[Dict[str, Any], bool]:
    sm = _read_json(simulation_root / "simulation_summary.json")
    if not isinstance(sm, dict):
        return (
            {
                "schema_version": SIM_CONTEXT_SCHEMA,
                "simulation_context_attached": False,
                "simulation_profile_id": None,
                "output_root": str(simulation_root),
                "run_model": None,
                "runtime_routing_changed": False,
                "ci_default_changed": False,
                "simulation_context_only": True,
            },
            False,
        )
    return (
        {
            "schema_version": SIM_CONTEXT_SCHEMA,
            "simulation_context_attached": True,
            "simulation_profile_id": sm.get("simulation_profile_id"),
            "output_root": sm.get("simulation_output_root") or str(simulation_root),
            "run_model": sm.get("run_model"),
            "runtime_routing_changed": False,
            "ci_default_changed": False,
            "simulation_context_only": True,
        },
        True,
    )


def build_reference_candidate(
    *,
    poster_image_ref: str,
    poster_root: Path,
    ocr_plan_root: Path,
    visual_root: Path,
    metrics_root: Path,
    simulation_root: Path,
    text_refs: List[Dict[str, Any]],
    visual_refs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "schema_version": CANDIDATE_SCHEMA,
        "reference_scope": "reference_only",
        "poster_image_ref": poster_image_ref,
        "text_plan_refs": text_refs,
        "visual_symbol_refs": visual_refs,
        "layout_governance_ref": str(poster_root / "poster_layout_governance_summary.json"),
        "region_ocr_plan_ref": str(ocr_plan_root / "poster_region_ocr_plan_stub.json"),
        "visual_symbol_evidence_ref": str(visual_root / "poster_visual_symbol_evidence_items.json"),
        "metrics_collector_ref": str(metrics_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json"),
        "simulation_context_ref": str(simulation_root / "simulation_summary.json"),
        "fact_status": "not_fact",
        "write_allowed": False,
        "fusion_status": "not_fused",
        "semantic_join_status": "not_allowed",
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "cross_modal_poster_reference_only_executed": True,
        "reference_only": True,
        "simulation_context_attached": True,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
        "vision_provider_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "fusion_invoked": False,
        "semantic_join_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
    }


def build_summary(
    *,
    simulation_attached: bool,
    text_count: int,
    visual_count: int,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "reference_scope": "reference_only",
        "based_on_poster_governance": True,
        "based_on_region_ocr_plan": True,
        "based_on_visual_symbol_evidence": True,
        "based_on_metrics_collector": True,
        "simulation_context_attached": simulation_attached,
        "text_plan_reference_count": text_count,
        "visual_symbol_reference_count": visual_count,
        "fusion_invoked": False,
        "ocr_invoked": False,
        "qr_decoded": False,
        "brand_identity_confirmed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_cross_modal_poster_ocr_reference_only_v0(
    *,
    poster_governance_root: str,
    poster_region_ocr_plan_root: str,
    poster_visual_symbol_evidence_root: str,
    metrics_collector_root: str,
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
    List[str],
]:
    errs: List[str] = []
    poster = Path(poster_governance_root).resolve()
    plan_root = Path(poster_region_ocr_plan_root).resolve()
    visual = Path(poster_visual_symbol_evidence_root).resolve()
    metrics = Path(metrics_collector_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()

    for label, root, files in (
        ("poster_governance", poster, ("poster_layout_governance_summary.json", "poster_text_region_candidates.json")),
        ("ocr_plan", plan_root, ("poster_region_ocr_plan_stub.json",)),
        ("visual_symbol", visual, ("poster_visual_symbol_evidence_items.json",)),
    ):
        for fn in files:
            if not (root / fn).is_file():
                errs.append(f"missing:{label}:{fn}")

    plan = _read_json(plan_root / "poster_region_ocr_plan_stub.json") or {}
    if int(plan.get("planned_region_count") or 0) != 4:
        errs.append("ocr_plan_region_count_not_4")
    excluded_path = plan_root / "poster_region_ocr_excluded_regions_report.json"
    plan["_excluded_report_path"] = str(excluded_path)

    items_doc = _read_json(visual / "poster_visual_symbol_evidence_items.json") or {}
    if int(items_doc.get("item_count") or len(items_doc.get("items") or [])) != 4:
        errs.append("visual_symbol_item_count_not_4")

    text_mx = build_text_plan_reference_matrix(plan=plan)
    visual_mx = build_visual_symbol_reference_matrix(items_doc=items_doc)
    align = build_cross_track_alignment_matrix(plan=plan)
    if align.get("overlap_count") != 0:
        errs.append("cross_track_overlap_nonzero")
    if align.get("visual_regions_in_ocr_plan"):
        errs.append("visual_regions_in_ocr_plan")
    if align.get("logo_qr_in_text_plan"):
        errs.append("logo_qr_in_text_plan")

    risk = build_risk_report()
    gate = build_gate_policy()
    metrics_binding = build_metrics_binding(
        poster_root=poster, plan=plan, items_doc=items_doc, metrics_collector_root=metrics
    )
    sim_report, sim_ok = build_simulation_context_report(sim)
    if not sim_ok:
        errs.append("simulation_context_missing")
    if sim_report.get("simulation_profile_id") != "developer_full":
        errs.append("simulation_profile_id_not_developer_full")
    if sim_report.get("run_model") is not False:
        errs.append("simulation_run_model_not_false")

    chain = build_source_chain_summary(
        poster_root=poster,
        ocr_plan_root=plan_root,
        visual_root=visual,
        metrics_root=metrics,
        simulation_root=sim,
    )
    poster_ref = _poster_image_ref(poster)
    candidate = build_reference_candidate(
        poster_image_ref=poster_ref,
        poster_root=poster,
        ocr_plan_root=plan_root,
        visual_root=visual,
        metrics_root=metrics,
        simulation_root=sim,
        text_refs=list(text_mx.get("rows") or []),
        visual_refs=list(visual_mx.get("rows") or []),
    )
    summary = build_summary(
        simulation_attached=sim_ok,
        text_count=int(text_mx.get("row_count") or 0),
        visual_count=int(visual_mx.get("row_count") or 0),
    )
    audit = build_audit()
    if not sim_ok:
        audit["simulation_context_attached"] = False

    return (
        summary,
        candidate,
        text_mx,
        visual_mx,
        align,
        risk,
        gate,
        metrics_binding,
        chain,
        sim_report,
        audit,
        errs,
    )
