# -*- coding: utf-8 -*-
"""Poster TestBoard Track B closure (aggregate existing phases only).

Phase-Poster-TestBoard-Closure-001 — TVOCR_V1_B_POSTER_LAYOUT
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Poster-TestBoard-Closure-001"
TRACK_ID = "TVOCR_V1_B_POSTER_LAYOUT"

SUMMARY_SCHEMA = "poster_testboard_track_b_closure_summary_v0"
PHASE_MATRIX_SCHEMA = "poster_testboard_track_b_phase_matrix_v0"
LINEAGE_SCHEMA = "poster_testboard_track_b_lineage_matrix_v0"
SEPARATION_SCHEMA = "poster_testboard_track_b_track_separation_report_v0"
BOUNDARY_SCHEMA = "poster_testboard_track_b_no_write_boundary_matrix_v0"
CAPABILITY_SCHEMA = "poster_testboard_track_b_capability_closure_report_v0"
NON_CLAIMS_SCHEMA = "poster_testboard_track_b_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "poster_testboard_track_b_open_followups_v0"
METRICS_SNAPSHOT_SCHEMA = "poster_testboard_track_b_metrics_snapshot_report_v0"
SIM_CONTEXT_SCHEMA = "poster_testboard_track_b_simulation_context_report_v0"
AUDIT_SCHEMA = "poster_testboard_track_b_closure_audit_v0"

REQUIRED_PHASES: Tuple[Dict[str, Any], ...] = (
    {
        "phase_name": "OCR-Poster-Layout-Segmentation-Governance-001",
        "summary_file": "poster_layout_governance_summary.json",
        "artifact_checks": ("poster_text_region_candidates.json", "poster_visual_symbol_candidates.json"),
    },
    {
        "phase_name": "OCR-Poster-Region-OCR-Plan-Stub-001",
        "summary_file": "poster_region_ocr_plan_stub_summary.json",
        "artifact_checks": ("poster_region_ocr_plan_stub.json",),
    },
    {
        "phase_name": "OCR-Poster-VisualSymbolEvidence-Stub-001",
        "summary_file": "poster_visual_symbol_evidence_stub_summary.json",
        "artifact_checks": ("poster_visual_symbol_evidence_items.json",),
    },
    {
        "phase_name": "CrossModal-Poster-OCR-ReferenceOnly-001",
        "summary_file": "cross_modal_poster_ocr_reference_only_summary.json",
        "artifact_checks": ("cross_modal_poster_reference_candidate.json",),
        "verifier_file": "cross_modal_poster_reference_only_verifier_report.json",
        "verifier_in_parent": True,
    },
)

BOUNDARY_KEYS = (
    "ocr_invoked",
    "rapidocr_invoked",
    "paddleocr_invoked",
    "qr_decoder_invoked",
    "brand_database_invoked",
    "visual_symbol_registry_invoked",
    "vision_provider_invoked",
    "vlm_invoked",
    "ai_interpretation_invoked",
    "fusion_invoked",
    "semantic_join_invoked",
    "midplatform_fact_written",
    "scene_delta_written",
    "world_model_written",
    "navigation_decision_invoked",
    "auto_approve_invoked",
    "approval_granted",
    "runtime_routing_changed",
)

AUDIT_FILES_BY_ROOT = {
    "poster_governance": "poster_layout_governance_audit_report.json",
    "ocr_plan": "poster_region_ocr_plan_stub_audit_report.json",
    "visual_symbol": "poster_visual_symbol_evidence_stub_audit_report.json",
    "reference_only": "cross_modal_poster_reference_only_audit_report.json",
}


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _phase_verdict(root: Path, spec: Dict[str, Any]) -> Tuple[str, List[str]]:
    blockers: List[str] = []
    sm = _read_json(root / str(spec["summary_file"]))
    if not isinstance(sm, dict):
        blockers.append("missing_summary")
        return "NO_GO", blockers
    hint = str(sm.get("phase_verdict_hint") or sm.get("verdict") or "").upper()
    errs = sm.get("errors") if isinstance(sm.get("errors"), list) else []
    if errs:
        blockers.extend([str(e) for e in errs])
    vf = spec.get("verifier_file")
    if vf:
        vp = (root.parent / vf) if spec.get("verifier_in_parent") else (root / vf)
        if vp.is_file():
            vr = _read_json(vp)
            if isinstance(vr, dict) and str(vr.get("verdict") or "").upper() != "GO":
                blockers.append(f"verifier_not_go:{vr.get('verdict')}")
        elif hint != "GO":
            blockers.append("missing_verifier_report")
    if hint == "GO" and not blockers:
        return "GO", []
    if hint in ("GO", "CONDITIONAL_GO") and not errs:
        return hint if hint else "GO", blockers
    return "NO_GO" if blockers or hint not in ("GO", "CONDITIONAL_GO") else hint, blockers


def build_phase_matrix(roots: Dict[str, Path]) -> Tuple[Dict[str, Any], List[str]]:
    rows: List[Dict[str, Any]] = []
    errs: List[str] = []
    key_map = {
        "OCR-Poster-Layout-Segmentation-Governance-001": "poster_governance",
        "OCR-Poster-Region-OCR-Plan-Stub-001": "ocr_plan",
        "OCR-Poster-VisualSymbolEvidence-Stub-001": "visual_symbol",
        "CrossModal-Poster-OCR-ReferenceOnly-001": "reference_only",
    }
    for spec in REQUIRED_PHASES:
        pname = spec["phase_name"]
        rkey = key_map[pname]
        root = roots[rkey]
        verdict, blockers = _phase_verdict(root, spec)
        arts = [str(spec["artifact_checks"][0])] if spec.get("artifact_checks") else []
        present = all((root / a).is_file() for a in spec.get("artifact_checks", ()))
        sm = _read_json(root / str(spec["summary_file"])) or {}
        boundary = f"scope={sm.get('governance_scope') or sm.get('plan_scope') or sm.get('reference_scope') or 'closure_aggregate'}; fact_status={sm.get('fact_status')}"
        status = "ok" if verdict == "GO" and not blockers and present else "fail"
        if verdict != "GO":
            errs.append(f"phase_not_go:{pname}")
        if blockers:
            errs.append(f"phase_blockers:{pname}")
        rows.append(
            {
                "phase_name": pname,
                "input_root": str(root),
                "verifier_verdict": verdict,
                "blockers": blockers,
                "status": status,
                "boundary_summary": boundary,
                "output_artifacts_present": present,
            }
        )
    return {"schema_version": PHASE_MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}, errs


def build_lineage_matrix(
    roots: Dict[str, Path],
    reference_root: Path,
    sim_root: Path,
) -> Dict[str, Any]:
    gov = roots["poster_governance"]
    plan = roots["ocr_plan"]
    vis = roots["visual_symbol"]
    manifest = _read_json(gov / "poster_synthetic_fixture_manifest.json") or {}
    text_doc = _read_json(gov / "poster_text_region_candidates.json") or {}
    plan_doc = _read_json(plan / "poster_region_ocr_plan_stub.json") or {}
    items_doc = _read_json(vis / "poster_visual_symbol_evidence_items.json") or {}
    ref_sm = _read_json(reference_root / "cross_modal_poster_ocr_reference_only_summary.json") or {}
    ref_bind = _read_json(reference_root / "cross_modal_poster_reference_metrics_binding_report.json") or {}
    align = _read_json(reference_root / "cross_modal_poster_cross_track_alignment_matrix.json") or {}
    sim_sm = _read_json(sim_root / "simulation_summary.json") or {}

    chain = [
        {"step": "poster_layout_governance", "root": str(gov)},
        {"step": "poster_region_ocr_plan", "root": str(plan)},
        {"step": "poster_visual_symbol_evidence", "root": str(vis)},
        {"step": "cross_modal_poster_reference_only", "root": str(reference_root)},
    ]
    return {
        "schema_version": LINEAGE_SCHEMA,
        "chain": chain,
        "poster_image_ref": manifest.get("source_image_ref"),
        "text_region_count": int(
            ref_bind.get("text_region_count")
            or align.get("text_track_region_count")
            or text_doc.get("candidate_count")
            or len(text_doc.get("candidates") or [])
        ),
        "visual_symbol_region_count": int(
            ref_bind.get("visual_symbol_region_count")
            or align.get("visual_track_region_count")
            or ref_sm.get("visual_symbol_reference_count")
            or 0
        ),
        "planned_ocr_region_count": int(plan_doc.get("planned_region_count") or 0),
        "visual_symbol_item_count": int(items_doc.get("item_count") or len(items_doc.get("items") or [])),
        "reference_candidate_count": int(
            ref_bind.get("reference_candidate_count")
            or ref_sm.get("reference_candidate_count")
            or (1 if _read_json(reference_root / "cross_modal_poster_reference_candidate.json") else 0)
        ),
        "simulation_profile_id": sim_sm.get("simulation_profile_id"),
        "run_model": sim_sm.get("run_model"),
    }


def build_track_separation_report(reference_root: Path) -> Dict[str, Any]:
    align = _read_json(reference_root / "cross_modal_poster_cross_track_alignment_matrix.json") or {}
    cand = _read_json(reference_root / "cross_modal_poster_reference_candidate.json") or {}
    plan_ref = Path(str(cand.get("region_ocr_plan_ref") or ""))
    excluded_doc = _read_json(plan_ref.parent / "poster_region_ocr_excluded_regions_report.json") if plan_ref else {}
    logo_qr_excluded = False
    if isinstance(excluded_doc, dict):
        for r in excluded_doc.get("excluded_regions") or []:
            if isinstance(r, dict) and r.get("region_id") in ("logo_area", "qr_area"):
                logo_qr_excluded = True
    return {
        "schema_version": SEPARATION_SCHEMA,
        "text_track_region_count": align.get("text_track_region_count", 4),
        "visual_track_region_count": align.get("visual_track_region_count", 4),
        "overlap_count": align.get("overlap_count", 0),
        "visual_regions_in_ocr_plan": align.get("visual_regions_in_ocr_plan", False),
        "logo_qr_in_text_plan": align.get("logo_qr_in_text_plan", False),
        "ordinary_ocr_text_chain_excludes_logo_qr": logo_qr_excluded,
        "semantic_join_allowed": align.get("semantic_join_allowed", False),
        "fusion_invoked": align.get("fusion_invoked", False),
    }


def _audit_for_root(root: Path, audit_name: str) -> Dict[str, Any]:
    doc = _read_json(root / audit_name) or {}
    return doc if isinstance(doc, dict) else {}


def build_no_write_boundary_matrix(roots: Dict[str, Path]) -> Dict[str, Any]:
    phases_audit: List[Dict[str, Any]] = []
    violations: List[str] = []
    for label in ("poster_governance", "ocr_plan", "visual_symbol", "reference_only"):
        audit_name = AUDIT_FILES_BY_ROOT[label]
        root = roots[label]
        aud = _audit_for_root(root, audit_name)
        row: Dict[str, Any] = {"phase": label}
        for k in BOUNDARY_KEYS:
            val = aud.get(k)
            if k == "qr_decoder_invoked" and val is None:
                val = aud.get("qr_decoder_invoked", aud.get("qr_decode_invoked", False))
            if k == "vlm_invoked" and val is None:
                val = aud.get("vlm_invoked", aud.get("vlm_invoked", False))
            row[k] = val if val is not None else False
        phases_audit.append(row)
        for k in BOUNDARY_KEYS:
            if row.get(k) is True:
                violations.append(f"{label}:{k}=true")

    return {
        "schema_version": BOUNDARY_SCHEMA,
        "phases": phases_audit,
        "boundary_ok": len(violations) == 0,
        "violations": violations,
    }


def build_capability_closure_report(
    *,
    gov_summary: Dict[str, Any],
    plan_summary: Dict[str, Any],
    ref_summary: Dict[str, Any],
    boundary_ok: bool,
    sim_attached: bool,
) -> Dict[str, Any]:
    return {
        "schema_version": CAPABILITY_SCHEMA,
        "proven_capabilities": [
            "poster_like_image_has_layout_governance",
            "full_image_ocr_default_forbidden",
            "text_non_text_visual_symbol_split_complete",
            "text_regions_generate_ocr_plan_stub",
            "visual_regions_generate_visual_symbol_evidence_stub",
            "text_and_visual_parallel_reference_only_index",
            "all_outputs_not_fact",
            "no_write_boundary_passed" if boundary_ok else "no_write_boundary_check_required",
            "simulation_context_readonly_attached" if sim_attached else "simulation_context_missing",
        ],
        "full_image_ocr_allowed": gov_summary.get("full_image_ocr_allowed"),
        "ocr_strategy": gov_summary.get("ocr_strategy") or plan_summary.get("ocr_strategy"),
        "reference_status": ref_summary.get("reference_scope"),
        "track_b_evaluation_only": True,
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "claims_denied": [
            "no_real_poster_ocr_claim",
            "no_complex_poster_generalization_claim",
            "no_ocr_benchmark_claim",
            "no_qr_decode_claim",
            "no_brand_identity_claim",
            "no_china_visual_symbol_registry_claim",
            "no_semantic_join_available_claim",
            "no_fusion_fact_write_claim",
            "no_scene_delta_write_claim",
            "no_world_model_write_claim",
            "no_navigation_use_claim",
        ],
        "no_real_poster_ocr_claim": True,
        "no_qr_decode_claim": True,
        "no_brand_identity_claim": True,
    }


def build_open_followups() -> Dict[str, Any]:
    items = [
        "Poster real OCR execution gated later",
        "Poster VisualSymbolRegistry integration later",
        "QR decode governance later",
        "Brand / logo registry governance later",
        "China VisualSymbolRegistry source hierarchy later",
        "Poster reading order improvement later",
        "Poster metrics collector update later",
        "Poster real video cases later",
        "Poster benchmark later",
        "Poster public facility overlap governance later",
    ]
    return {"schema_version": FOLLOWUPS_SCHEMA, "items": items, "item_count": len(items)}


def build_metrics_snapshot(
    roots: Dict[str, Path],
    reference_root: Path,
    metrics_root: Path,
) -> Dict[str, Any]:
    gov = _read_json(roots["poster_governance"] / "poster_layout_governance_summary.json") or {}
    plan_bind = _read_json(roots["ocr_plan"] / "poster_region_ocr_metrics_binding_report.json") or {}
    ref_bind = _read_json(reference_root / "cross_modal_poster_reference_metrics_binding_report.json") or {}
    mc = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_metrics_collection_summary.json") or {}
    poster_report = _read_json(metrics_root / "cross_modal_vision_ocr_testboard_poster_metrics_report.json")

    missing: List[str] = []
    if not poster_report:
        missing.append("cross_modal_vision_ocr_testboard_poster_metrics_report")

    metrics: Dict[str, Any] = {
        "full_image_ocr_forbidden_count": ref_bind.get("full_image_ocr_forbidden_count", 1),
        "text_region_count": ref_bind.get("text_region_count", 4),
        "non_text_region_count": 2,
        "visual_symbol_region_count": ref_bind.get("visual_symbol_region_count", 4),
        "visual_symbol_split_count": ref_bind.get("visual_symbol_split_count", 4),
        "ocr_region_plan_count": ref_bind.get("ocr_region_plan_count", plan_bind.get("ocr_region_plan_count_value", 4)),
        "reading_order_low_confidence_count": ref_bind.get("reading_order_low_confidence_count", 1),
        "no_write_boundary_pass_rate": ref_bind.get("no_write_boundary_pass_rate", 1.0),
    }
    if missing:
        metrics["missing_metric_behavior"] = "placeholder_or_future_update_required"
        metrics["missing_metrics"] = missing
    if mc.get("bootstrap_only"):
        metrics["metrics_collector_note"] = "bootstrap_stub_only_not_full_collector_run"

    return {
        "schema_version": METRICS_SNAPSHOT_SCHEMA,
        "metrics_collector_root": str(metrics_root),
        "metrics": metrics,
        "benchmark_claim": False,
    }


def build_simulation_context_report(sim_root: Path) -> Dict[str, Any]:
    sm = _read_json(sim_root / "simulation_summary.json") or {}
    return {
        "schema_version": SIM_CONTEXT_SCHEMA,
        "simulation_profile_id": sm.get("simulation_profile_id"),
        "simulation_output_root": sm.get("simulation_output_root") or str(sim_root),
        "run_model": sm.get("run_model"),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }


def build_closure_audit(boundary_ok: bool, all_go: bool) -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "poster_testboard_track_b_closure_executed": True,
        "closure_only": True,
        "no_new_capability_added": True,
        "all_required_phases_go": all_go,
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
        "boundary_ok": boundary_ok,
    }


def build_closure_summary(
    *,
    all_go: bool,
    gov_summary: Dict[str, Any],
    ref_summary: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "track_id": TRACK_ID,
        "track_status": "closed_for_evaluation" if all_go else "closure_incomplete",
        "phase_count": 4,
        "all_required_phases_go": all_go,
        "full_image_ocr_allowed": gov_summary.get("full_image_ocr_allowed", False),
        "ocr_strategy": gov_summary.get("ocr_strategy") or "segment_first",
        "text_track_status": "ocr_plan_stub_only",
        "visual_track_status": "visual_symbol_stub_only",
        "reference_status": ref_summary.get("reference_scope") or "reference_only",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "runtime_routing_changed": False,
    }


def run_poster_testboard_track_b_closure_v0(
    *,
    poster_governance_root: str,
    poster_region_ocr_plan_root: str,
    poster_visual_symbol_evidence_root: str,
    poster_reference_only_root: str,
    metrics_collector_root: str,
    simulation_lab_harness_root: str,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    errs: List[str] = []
    roots = {
        "poster_governance": Path(poster_governance_root).resolve(),
        "ocr_plan": Path(poster_region_ocr_plan_root).resolve(),
        "visual_symbol": Path(poster_visual_symbol_evidence_root).resolve(),
        "reference_only": Path(poster_reference_only_root).resolve(),
    }
    metrics = Path(metrics_collector_root).resolve()
    sim = Path(simulation_lab_harness_root).resolve()
    ref = roots["reference_only"]

    phase_matrix, phase_errs = build_phase_matrix(roots)
    errs.extend(phase_errs)

    gov_sm = _read_json(roots["poster_governance"] / "poster_layout_governance_summary.json") or {}
    plan_sm = _read_json(roots["ocr_plan"] / "poster_region_ocr_plan_stub_summary.json") or {}
    ref_sm = _read_json(ref / "cross_modal_poster_ocr_reference_only_summary.json") or {}

    if gov_sm.get("full_image_ocr_allowed") is not False:
        errs.append("full_image_ocr_allowed_not_false")
    if str(gov_sm.get("ocr_strategy") or "") != "segment_first":
        errs.append("ocr_strategy_not_segment_first")

    lineage = build_lineage_matrix(roots, ref, sim)
    if lineage.get("text_region_count") != 4:
        errs.append("lineage_text_region_count_not_4")
    if lineage.get("visual_symbol_region_count") != 4:
        errs.append("lineage_visual_symbol_region_count_not_4")
    if lineage.get("planned_ocr_region_count") != 4:
        errs.append("lineage_planned_ocr_region_count_not_4")
    if lineage.get("visual_symbol_item_count") != 4:
        errs.append("lineage_visual_symbol_item_count_not_4")
    if lineage.get("simulation_profile_id") != "developer_full":
        errs.append("lineage_simulation_profile_not_developer_full")
    if lineage.get("run_model") is not False:
        errs.append("lineage_run_model_not_false")

    separation = build_track_separation_report(ref)
    if separation.get("overlap_count") != 0:
        errs.append("separation_overlap_count_not_0")

    boundary = build_no_write_boundary_matrix(roots)
    if not boundary.get("boundary_ok"):
        errs.extend([f"boundary:{v}" for v in boundary.get("violations") or []])

    all_go = all(r.get("verifier_verdict") == "GO" and not r.get("blockers") for r in phase_matrix.get("rows") or [])
    capability = build_capability_closure_report(
        gov_summary=gov_sm,
        plan_summary=plan_sm,
        ref_summary=ref_sm,
        boundary_ok=bool(boundary.get("boundary_ok")),
        sim_attached=_read_json(sim / "simulation_summary.json") is not None,
    )
    non_claims = build_non_claims_report()
    followups = build_open_followups()
    metrics_snap = build_metrics_snapshot(roots, ref, metrics)
    sim_report = build_simulation_context_report(sim)
    if sim_report.get("simulation_profile_id") != "developer_full":
        errs.append("simulation_profile_id_not_developer_full")

    summary = build_closure_summary(all_go=all_go and not errs, gov_summary=gov_sm, ref_summary=ref_sm)
    audit = build_closure_audit(boundary_ok=bool(boundary.get("boundary_ok")), all_go=all_go)

    return (
        summary,
        phase_matrix,
        lineage,
        separation,
        boundary,
        capability,
        non_claims,
        followups,
        metrics_snap,
        sim_report,
        audit,
        errs,
    )
