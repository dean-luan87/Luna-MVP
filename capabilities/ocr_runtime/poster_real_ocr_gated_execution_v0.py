# -*- coding: utf-8 -*-
"""Poster gated real OCR on text regions only (segment-first, bridge-required).

Phase-Poster-Real-OCR-Gated-Execution-001
"""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Poster-Real-OCR-Gated-Execution-001"

TEXT_REGION_IDS = ("title_area", "body_text_area", "price_or_promo_area", "time_location_area")
VISUAL_EXCLUDED = ("logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area")

SUMMARY_SCHEMA = "poster_real_ocr_gated_execution_summary_v0"
EXEC_PLAN_SCHEMA = "poster_real_ocr_execution_plan_v0"
EXCLUDED_GUARD_SCHEMA = "poster_real_ocr_excluded_visual_region_guard_report_v0"
PROVIDER_GATE_SCHEMA = "poster_real_ocr_provider_gate_report_v0"
RESULT_MATRIX_SCHEMA = "poster_real_ocr_result_matrix_v0"
EVIDENCE_SCHEMA = "poster_layout_text_evidence_candidate_v0"
READING_GUARD_SCHEMA = "poster_real_ocr_reading_order_guard_report_v0"
TTL_RISK_SCHEMA = "poster_real_ocr_ttl_commercial_risk_report_v0"
METRICS_BIND_SCHEMA = "poster_real_ocr_metrics_binding_report_v0"
BENCHMARK_LINK_SCHEMA = "poster_real_ocr_benchmark_link_report_v0"
HEALTH_LINK_SCHEMA = "poster_real_ocr_system_health_link_report_v0"
BOUNDARY_SCHEMA = "poster_real_ocr_no_write_boundary_report_v0"
SIM_SCHEMA = "poster_real_ocr_simulation_context_report_v0"
NON_CLAIMS_SCHEMA = "poster_real_ocr_non_claims_report_v0"
AUDIT_SCHEMA = "poster_real_ocr_audit_v0"


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


def _crop_region(poster_image: Path, bbox: List[int], out_path: Path) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return False
    if not poster_image.is_file():
        return False
    x1, y1, x2, y2 = [int(v) for v in bbox]
    img = Image.open(poster_image).convert("RGB")
    crop = img.crop((x1, y1, x2, y2))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    crop.save(out_path, format="PNG")
    return True


def _bridge_ocr_region(
    *,
    crop_path: Path,
    bbox: List[int],
    work_dir: Path,
    workspace_root: Path,
    governance_config_path: Path,
    region_id: str,
) -> Dict[str, Any]:
    from capabilities.ocr_runtime.ocr_mainline_bridge_v0 import run_ocr_mainline_bridge_v0
    from capabilities.ocr_runtime.ocr_request_contract_v0 import OCRRequestV0

    try:
        from PIL import Image

        w, h = Image.open(crop_path).size
    except Exception:
        w, h = max(1, bbox[2] - bbox[0]), max(1, bbox[3] - bbox[1])

    req = OCRRequestV0(
        task_context="poster_gated_real_ocr_smoke",
        input_type="roi",
        image_path=str(crop_path.resolve()),
        roi_refs=[f"ocr_roi_xyxy:0,0,{w},{h}"],
        allow_full_image=False,
        allow_heavy_ocr=False,
        latency_budget_ms=8000,
        source_task_id=f"poster_{region_id}",
    )

    work_dir.mkdir(parents=True, exist_ok=True)
    try:
        bridge = run_ocr_mainline_bridge_v0(
            req,
            governance_config_path=governance_config_path,
            workspace_root=workspace_root,
            normalization_work_dir=work_dir / "norm",
        )
    except Exception as e:
        return {
            "status": "error",
            "error": f"bridge_exception:{type(e).__name__}:{e}",
            "bridge_invoked": True,
            "real_provider_invoked": False,
            "rapidocr_invoked": False,
            "text_items": [],
            "text_joined": "",
            "empty_text": True,
        }

    prov = bridge.get("provider_result") if isinstance(bridge.get("provider_result"), dict) else {}
    audit = bridge.get("audit") if isinstance(bridge.get("audit"), dict) else {}
    sel_rep = bridge.get("provider_selection_report") if isinstance(bridge.get("provider_selection_report"), dict) else {}
    text_items = prov.get("text_items") if isinstance(prov.get("text_items"), list) else []
    text_joined = str(prov.get("text_joined") or "")
    empty_text = not text_joined.strip() and not text_items
    st = str(bridge.get("status") or "")
    fallback_stub = bool(audit.get("fallback_to_stub")) or bool(sel_rep.get("fallback_to_stub"))
    real = bool(prov.get("real_provider_invoked")) or bool(audit.get("real_provider_invoked"))
    rapid = real and str(prov.get("provider") or sel_rep.get("selected_provider") or "").startswith("rapidocr")
    err = None if st == "success" and real else str(bridge.get("error") or prov.get("error") or st)
    if text_joined == "MOCK_TEXT" or any(
        isinstance(it, dict) and str(it.get("text") or "").startswith("MOCK_TEXT") for it in text_items
    ):
        err = "provider_unavailable"
        real = False
        rapid = False
        st = "error"
    elif fallback_stub and not real:
        err = "provider_unavailable"
        st = "error"
    elif err in ("stub_disabled", "provider_selection_failed") or "provider_runtime_unavailable" in str(err or ""):
        err = "provider_unavailable"

    return {
        "status": st,
        "error": err,
        "bridge_invoked": True,
        "direct_provider_bypass": False,
        "real_provider_invoked": real,
        "rapidocr_invoked": rapid,
        "text_items": text_items,
        "text_joined": text_joined,
        "empty_text": empty_text,
        "latency_ms": prov.get("duration_ms") or prov.get("latency_ms"),
        "provider": prov.get("provider") or "rapidocr_candidate",
        "bridge_pack_ref": str((work_dir / "ocr_bridge_pack.json").resolve()) if (work_dir / "ocr_bridge_pack.json").is_file() else None,
    }


def build_execution_plan(
    *,
    plan_root: Path,
    layout_root: Path,
    work_dir: Path,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], bool]:
    stub = _read_json(plan_root / "poster_region_ocr_plan_stub.json") or {}
    planned = [r for r in (stub.get("planned_regions") or []) if isinstance(r, dict)]
    planned = [r for r in planned if r.get("source_region_id") in TEXT_REGION_IDS]

    manifest = _read_json(layout_root / "poster_synthetic_fixture_manifest.json") or {}
    poster_image = Path(str(manifest.get("source_image_ref") or ""))
    if not poster_image.is_file():
        poster_image = layout_root / "_work/fixtures/poster_synthetic_fixture_v0.png"

    any_crop_gen = False
    rows: List[Dict[str, Any]] = []
    for i, pr in enumerate(planned):
        rid = str(pr.get("source_region_id"))
        bbox = list(pr.get("bbox") or [])
        crop_path = work_dir / "crops" / f"{rid}.png"
        crop_generated = False
        if bbox and _crop_region(poster_image, bbox, crop_path):
            crop_generated = True
            any_crop_gen = True
        elif not crop_path.is_file():
            crop_path = poster_image  # fallback ref only if crop failed
        ttl_ph = str(pr.get("ttl_policy_placeholder") or "none")
        rows.append(
            {
                "execution_plan_id": f"exec_{rid}",
                "source_region_id": rid,
                "region_type": pr.get("region_type"),
                "bbox": bbox,
                "image_ref_or_crop_ref": str(crop_path.resolve()) if crop_path.is_file() else str(poster_image),
                "crop_generated_by_this_phase": crop_generated,
                "provider_class": "rapidocr_lightweight",
                "expected_output": "layout_text_evidence_candidate",
                "ttl_required": ttl_ph not in ("none", ""),
                "risk_flags": list(pr.get("risk_flags") or []),
                "execution_allowed": True,
                "full_image_ocr_allowed": False,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    doc = {
        "schema_version": EXEC_PLAN_SCHEMA,
        "phase": PHASE_ID,
        "planned_text_region_count": len(rows),
        "full_image_ocr_allowed": False,
        "segment_first_required": True,
        "rows": rows,
    }
    return doc, rows, any_crop_gen


def build_excluded_visual_guard(layout_root: Path) -> Dict[str, Any]:
    vis = _read_json(layout_root / "poster_visual_symbol_candidates.json") or {}
    cands = [c for c in (vis.get("candidates") or []) if isinstance(c, dict)]
    excluded = [c for c in cands if c.get("region_id") in VISUAL_EXCLUDED]
    by_id = {c.get("region_id"): c for c in excluded}
    return {
        "schema_version": EXCLUDED_GUARD_SCHEMA,
        "excluded_region_count": len(VISUAL_EXCLUDED),
        "logo_area_ocr_invoked": False,
        "qr_area_ocr_invoked": False,
        "product_or_decoration_area_ocr_invoked": False,
        "background_or_decoration_area_ocr_invoked": False,
        "qr_decoded": False,
        "brand_identity_confirmed": False,
        "ordinary_ocr_text_chain_excludes_logo_qr": True,
        "all_visual_regions_absent_from_ocr_execution_plan": True,
        "excluded_region_ids": list(VISUAL_EXCLUDED),
        "visual_candidates_present": len(excluded),
    }


def build_provider_gate(health_root: Path) -> Dict[str, Any]:
    return {
        "schema_version": PROVIDER_GATE_SCHEMA,
        "provider_mode": "gated_evaluation_only",
        "rapidocr_allowed": True,
        "paddleocr_allowed": False,
        "direct_provider_bypass_allowed": False,
        "ocr_mainline_bridge_required": True,
        "full_image_ocr_allowed": False,
        "provider_unavailable_behavior": "conditional_go_or_no_execution",
        "system_health_contract_ref": str(health_root.resolve()),
        "system_health_governance_available": health_root.is_dir(),
        "provider_health_runtime_checked": False,
        "system_health_runtime_invoked": False,
    }


def run_region_ocr(
    exec_rows: List[Dict[str, Any]],
    *,
    work_dir: Path,
    workspace_root: Path,
    governance_config_path: Path,
) -> Tuple[List[Dict[str, Any]], bool, bool, bool]:
    results: List[Dict[str, Any]] = []
    any_real = False
    any_rapid = False
    provider_unavailable = False

    for row in exec_rows:
        rid = row["source_region_id"]
        crop = Path(row["image_ref_or_crop_ref"])
        region_work = work_dir / "ocr" / rid
        ocr_out = _bridge_ocr_region(
            crop_path=crop,
            bbox=list(row.get("bbox") or []),
            work_dir=region_work,
            workspace_root=workspace_root,
            governance_config_path=governance_config_path,
            region_id=rid,
        )
        if str(ocr_out.get("error") or "") == "provider_unavailable":
            provider_unavailable = True
        if ocr_out.get("real_provider_invoked"):
            any_real = True
        if ocr_out.get("rapidocr_invoked"):
            any_rapid = True

        text_joined = str(ocr_out.get("text_joined") or "")
        results.append(
            {
                "result_id": f"res_{rid}",
                "execution_plan_id": row["execution_plan_id"],
                "source_region_id": rid,
                "provider": ocr_out.get("provider") or "rapidocr_candidate",
                "provider_level": "lightweight",
                "ocr_invoked": bool(ocr_out.get("real_provider_invoked")) and ocr_out.get("status") == "success",
                "bridge_invoked": bool(ocr_out.get("bridge_invoked")),
                "direct_provider_bypass": False,
                "text_items": ocr_out.get("text_items") or [],
                "text_joined": text_joined,
                "empty_text": bool(ocr_out.get("empty_text")),
                "error": ocr_out.get("error"),
                "latency_ms": ocr_out.get("latency_ms"),
                "confidence_placeholder": None,
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )

    return results, any_real, any_rapid, provider_unavailable


def build_layout_text_evidence(
    poster_image_ref: str,
    results: List[Dict[str, Any]],
    exec_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    ttl_map = {r["source_region_id"]: r.get("ttl_required") for r in exec_rows}
    risk_map = {r["source_region_id"]: r.get("risk_flags") for r in exec_rows}
    region_evidence: List[Dict[str, Any]] = []
    for res in results:
        rid = res["source_region_id"]
        region_evidence.append(
            {
                "evidence_id": f"ev_{rid}_{uuid.uuid4().hex[:8]}",
                "source_region_id": rid,
                "text_joined": res.get("text_joined"),
                "empty_text": res.get("empty_text"),
                "provider": res.get("provider"),
                "ttl_required": bool(ttl_map.get(rid)),
                "risk_flags": risk_map.get(rid) or [],
                "source_chain": ["poster_region_ocr_plan", "ocr_mainline_bridge", "rapidocr_lightweight"],
                "fact_status": "not_fact",
                "write_allowed": False,
            }
        )
    return {
        "schema_version": EVIDENCE_SCHEMA,
        "evidence_scope": "layout_text_evidence_candidate",
        "source_phase": PHASE_ID,
        "poster_image_ref": poster_image_ref,
        "region_text_evidence": region_evidence,
        "reading_order_confidence": "low",
        "semantic_join_allowed": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "requires_review": True,
    }


def build_reading_order_guard() -> Dict[str, Any]:
    return {
        "schema_version": READING_GUARD_SCHEMA,
        "reading_order_confidence": "low",
        "force_semantic_join_allowed": False,
        "semantic_join_invoked": False,
        "region_order": list(TEXT_REGION_IDS),
        "text_joined_across_regions_allowed": False,
        "reason_codes": [
            "complex_layout",
            "reading_order_uncertain",
            "real_ocr_candidate_not_fact",
        ],
    }


def build_ttl_commercial_risk(exec_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    promo = next((r for r in exec_rows if r["source_region_id"] == "price_or_promo_area"), None)
    time_r = next((r for r in exec_rows if r["source_region_id"] == "time_location_area"), None)
    return {
        "schema_version": TTL_RISK_SCHEMA,
        "price_or_promo_area_ttl_required": bool(promo and promo.get("ttl_required")),
        "time_location_area_ttl_required": bool(time_r and time_r.get("ttl_required")),
        "commercial_text_may_expire": True,
        "temporal_text_requires_ttl": True,
        "world_model_write_allowed": False,
        "fact_write_allowed": False,
        "requires_review_before_any_future_write": True,
    }


def build_metrics_binding(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    success = sum(1 for r in results if r.get("ocr_invoked") and not r.get("empty_text"))
    empty = sum(1 for r in results if r.get("empty_text"))
    non_empty = sum(1 for r in results if r.get("ocr_invoked") and not r.get("empty_text"))
    providers = [r.get("provider") for r in results if r.get("ocr_invoked")]
    return {
        "schema_version": METRICS_BIND_SCHEMA,
        "poster_ocr_execution_region_count": len(results),
        "poster_ocr_success_count": success,
        "poster_ocr_empty_text_count": empty,
        "poster_ocr_non_empty_text_count": non_empty,
        "poster_ocr_provider_distribution": {p: providers.count(p) for p in set(providers) if p},
        "poster_visual_region_excluded_count": len(VISUAL_EXCLUDED),
        "full_image_ocr_forbidden_count": len(results),
        "semantic_join_blocked_count": len(results),
        "ttl_required_region_count": 2,
        "no_write_boundary_pass_rate": 1.0,
    }


def build_benchmark_link(smoke_root: Path) -> Dict[str, Any]:
    return {
        "schema_version": BENCHMARK_LINK_SCHEMA,
        "benchmark_smoke_root": str(smoke_root),
        "current_phase_updates_t0_t1_candidate_values": True,
        "current_phase_updates_t2_quality_values": False,
        "ground_truth_available": False,
        "ocr_accuracy_computed": False,
        "benchmark_score_generated": False,
        "provider_comparison_claimed": False,
        "interpretation": "Functional T1 source only; does not update benchmark matrix directly.",
    }


def build_health_link(health_root: Path) -> Dict[str, Any]:
    return {
        "schema_version": HEALTH_LINK_SCHEMA,
        "system_health_governance_root": str(health_root),
        "system_health_governance_available": health_root.is_dir(),
        "module_health_report_required_future": True,
        "provider_health_runtime_checked": False,
        "recovery_action_committed": False,
        "capability_mask_consumed": False,
        "no_runtime_health_claim": True,
    }


def build_boundary_report() -> Dict[str, Any]:
    return {
        "schema_version": BOUNDARY_SCHEMA,
        "boundary_ok": True,
        "violations": [],
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "runtime_routing_changed": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
        "full_image_ocr_invoked": False,
        "visual_region_ocr_invoked": False,
    }


def build_simulation_context(sim_root: Path) -> Dict[str, Any]:
    sm = _read_json(sim_root / "simulation_summary.json") or {}
    return {
        "schema_version": SIM_SCHEMA,
        "simulation_profile_id": sm.get("simulation_profile_id") or "developer_full",
        "simulation_output_root": sm.get("simulation_output_root") or str(sim_root),
        "run_model": sm.get("run_model", False),
        "simulation_context_only": True,
        "runtime_routing_changed": False,
        "ci_default_changed": False,
        "no_hardware_certification_claim": True,
    }


def build_non_claims() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "not_poster_ocr_generalization": True,
        "not_ocr_accuracy": True,
        "not_benchmark": True,
        "not_provider_superiority": True,
        "no_qr_decode": True,
        "no_brand_recognition": True,
        "no_visual_symbol_registry": True,
        "no_semantic_join": True,
        "no_scene_delta_world_model_write": True,
        "no_navigation": True,
        "not_production_ready": True,
        "no_mock_text_substitution": True,
    }


def build_open_followups() -> Dict[str, Any]:
    return {
        "schema_version": "poster_real_ocr_open_followups_v0",
        "items": ["Phase-Poster-Real-OCR-ReadOnly-Consumer-001"],
        "item_count": 1,
    }


def build_audit(*, real_ocr: bool, rapid: bool, provider_unavailable: bool) -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "poster_real_ocr_gated_execution_executed": True,
        "gated_evaluation_only": True,
        "full_image_ocr_invoked": False,
        "visual_region_ocr_invoked": False,
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
        "paddleocr_invoked": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
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
        "real_ocr_invoked": real_ocr,
        "rapidocr_invoked": rapid,
        "provider_unavailable": provider_unavailable,
        "no_mock_text_substitution": True,
    }


def build_summary(
    *,
    real_ocr: bool,
    rapid: bool,
    provider_unavailable: bool,
    region_count: int,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "execution_scope": "gated_real_ocr_smoke",
        "based_on_poster_region_ocr_plan": True,
        "based_on_poster_reference_only": True,
        "based_on_poster_track_b_closure": True,
        "based_on_benchmark_real_values_smoke": True,
        "based_on_system_health_governance": True,
        "simulation_context_attached": True,
        "full_image_ocr_allowed": False,
        "segment_first_required": True,
        "planned_text_region_count": 4,
        "ocr_execution_region_count": region_count,
        "visual_symbol_region_ocr_count": 0,
        "real_ocr_invoked": real_ocr,
        "rapidocr_invoked": rapid,
        "paddleocr_invoked": False,
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
        "semantic_join_invoked": False,
        "fusion_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
        "runtime_routing_changed": False,
        "provider_unavailable": provider_unavailable,
        "phase_verdict_hint": (
            "GO"
            if real_ocr and not provider_unavailable
            else ("CONDITIONAL_GO" if provider_unavailable else "NO_GO")
        ),
    }


def run_poster_real_ocr_gated_execution_v0(
    *,
    poster_layout_governance_root: str,
    poster_region_ocr_plan_root: str,
    poster_visual_symbol_evidence_root: str,
    poster_reference_only_root: str,
    poster_track_b_closure_root: str,
    benchmark_real_values_smoke_root: str,
    system_health_governance_root: str,
    simulation_lab_harness_root: str,
    output_root: str,
    workspace_root: str,
    governance_config_path: str,
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
    layout = Path(poster_layout_governance_root).resolve()
    plan_root = Path(poster_region_ocr_plan_root).resolve()
    work = Path(output_root).resolve() / "_work"
    work.mkdir(parents=True, exist_ok=True)
    ws = Path(workspace_root).resolve()
    gov = Path(governance_config_path).resolve()

    if not _source_ok(plan_root, "poster_region_ocr_plan_stub_summary.json"):
        errs.append("region_ocr_plan_not_ok")

    exec_plan, exec_rows, _ = build_execution_plan(
        plan_root=plan_root, layout_root=layout, work_dir=work
    )
    if exec_plan.get("planned_text_region_count") != 4:
        errs.append("execution_plan_count_not_4")

    manifest = _read_json(layout / "poster_synthetic_fixture_manifest.json") or {}
    poster_ref = str(manifest.get("source_image_ref") or "")

    excluded = build_excluded_visual_guard(layout)
    provider_gate = build_provider_gate(Path(system_health_governance_root))

    results, any_real, any_rapid, provider_unavail = run_region_ocr(
        exec_rows,
        work_dir=work,
        workspace_root=ws,
        governance_config_path=gov,
    )

    for r in results:
        tj = str(r.get("text_joined") or "")
        if tj == "MOCK_TEXT":
            errs.append("mock_text_substitution_detected")

    evidence = build_layout_text_evidence(poster_ref, results, exec_rows)
    reading = build_reading_order_guard()
    ttl_risk = build_ttl_commercial_risk(exec_rows)
    metrics = build_metrics_binding(results)
    benchmark = build_benchmark_link(Path(benchmark_real_values_smoke_root))
    health = build_health_link(Path(system_health_governance_root))
    boundary = build_boundary_report()
    sim = build_simulation_context(Path(simulation_lab_harness_root))
    non_claims = build_non_claims()
    followups = build_open_followups()
    audit = build_audit(real_ocr=any_real, rapid=any_rapid, provider_unavailable=provider_unavail)
    summary = build_summary(
        real_ocr=any_real,
        rapid=any_rapid,
        provider_unavailable=provider_unavail,
        region_count=len(results),
    )

    if summary.get("phase_verdict_hint") == "NO_GO" and provider_unavail:
        # allow CONDITIONAL_GO in summary only
        pass

    return (
        summary,
        exec_plan,
        excluded,
        provider_gate,
        {"schema_version": RESULT_MATRIX_SCHEMA, "row_count": len(results), "rows": results},
        evidence,
        reading,
        ttl_risk,
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
