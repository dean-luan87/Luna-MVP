# -*- coding: utf-8 -*-
"""Poster region OCR plan stub (plan only, no OCR execution).

Phase-OCR-Poster-Region-OCR-Plan-Stub-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Poster-Region-OCR-Plan-Stub-001"

SUMMARY_SCHEMA = "poster_region_ocr_plan_stub_summary_v0"
PLAN_SCHEMA = "poster_region_ocr_plan_stub_v0"
EXCLUDED_SCHEMA = "poster_region_ocr_excluded_regions_report_v0"
RISK_SCHEMA = "poster_region_ocr_risk_matrix_v0"
PROVIDER_SCHEMA = "poster_region_ocr_provider_plan_matrix_v0"
READING_GUARD_SCHEMA = "poster_region_ocr_reading_order_guard_v0"
METRICS_BINDING_SCHEMA = "poster_region_ocr_metrics_binding_report_v0"
GATE_SCHEMA = "poster_region_ocr_gate_policy_report_v0"
AUDIT_SCHEMA = "poster_region_ocr_plan_stub_audit_v0"

PROVIDER_MAP = {
    "title_area": (
        "rapidocr_or_paddleocr_lightweight",
        "title_text_lightweight_ocr_planned",
    ),
    "body_text_area": (
        "rapidocr_or_paddleocr_lightweight",
        "body_text_lightweight_ocr_planned",
    ),
    "price_or_promo_area": (
        "numeric_text_or_promo_text_ocr_candidate",
        "promo_numeric_text_planned",
    ),
    "time_location_area": (
        "temporal_text_ocr_candidate",
        "date_time_text_planned",
    ),
}

PRIORITY = {
    "title_area": 1,
    "body_text_area": 2,
    "price_or_promo_area": 3,
    "time_location_area": 4,
}

TTL_POLICY = {
    "title_area": "none",
    "body_text_area": "none",
    "price_or_promo_area": "commercial_text_ttl_required",
    "time_location_area": "temporal_text_ttl_required",
}


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _planned_region(text_cand: Dict[str, Any]) -> Dict[str, Any]:
    rid = str(text_cand["region_id"])
    pclass, reason = PROVIDER_MAP[rid]
    risks = list(text_cand.get("risk_flags") or [])
    if "layout_text_not_fact" not in risks:
        risks.append("layout_text_not_fact")
    if rid != "title_area" and "reading_order_uncertain" not in risks:
        risks.append("reading_order_uncertain")
    return {
        "plan_region_id": f"plan_{rid}",
        "source_region_id": rid,
        "region_type": text_cand.get("region_type"),
        "bbox": list(text_cand.get("bbox") or []),
        "ocr_allowed": True,
        "recommended_provider_class": pclass,
        "provider_selection_reason": reason,
        "priority": PRIORITY[rid],
        "latency_budget_ms_placeholder": 800,
        "timeout_policy_placeholder": "poster_region_ocr_timeout_stub_v0",
        "expected_output": "layout_text_evidence_candidate",
        "fact_status": "not_fact",
        "write_allowed": False,
        "risk_flags": risks,
        "ttl_policy_placeholder": TTL_POLICY[rid],
    }


def build_plan_stub(*, poster_root: Path) -> Dict[str, Any]:
    text_doc = _read_json(poster_root / "poster_text_region_candidates.json") or {}
    cands = [c for c in (text_doc.get("candidates") or []) if isinstance(c, dict)]
    planned = [_planned_region(c) for c in cands]
    return {
        "schema_version": PLAN_SCHEMA,
        "phase": PHASE_ID,
        "full_image_ocr_allowed": False,
        "ocr_strategy": "segment_first",
        "planned_region_count": len(planned),
        "planned_regions": planned,
        "plan_candidate_only": True,
    }


def build_excluded_report(*, poster_root: Path) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    vis = _read_json(poster_root / "poster_visual_symbol_candidates.json") or {}
    for c in vis.get("candidates") or []:
        if not isinstance(c, dict):
            continue
        rid = c.get("region_id")
        routed = "visual_symbol_candidate" if rid == "logo_area" else "qr_candidate"
        rows.append(
            {
                "region_id": rid,
                "region_type": c.get("region_type"),
                "bbox": c.get("bbox"),
                "exclusion_reason": "visual_symbol_not_ordinary_ocr_text",
                "ocr_allowed": False,
                "routed_to": routed,
            }
        )
    non = _read_json(poster_root / "poster_non_text_region_candidates.json") or {}
    for c in non.get("candidates") or []:
        if not isinstance(c, dict):
            continue
        rows.append(
            {
                "region_id": c.get("region_id"),
                "region_type": c.get("region_type"),
                "bbox": c.get("bbox"),
                "exclusion_reason": "non_text_region_filtered",
                "ocr_allowed": False,
                "routed_to": "non_text_region_candidate",
            }
        )
    return {"schema_version": EXCLUDED_SCHEMA, "excluded_region_count": len(rows), "excluded_regions": rows}


def build_risk_matrix(plan: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for pr in plan.get("planned_regions") or []:
        if not isinstance(pr, dict):
            continue
        rid = pr.get("source_region_id")
        flags = list(pr.get("risk_flags") or [])
        rows.append(
            {
                "region_id": rid,
                "region_type": pr.get("region_type"),
                "risk_flags": flags,
                "ttl_required": pr.get("ttl_policy_placeholder") not in (None, "none"),
                "reading_order_sensitive": True,
                "semantic_join_allowed": False,
            }
        )
    return {
        "schema_version": RISK_SCHEMA,
        "summary_level_risk_flags": ["reading_order_uncertain", "layout_text_not_fact"],
        "row_count": len(rows),
        "rows": rows,
    }


def build_provider_plan_matrix(plan: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for pr in plan.get("planned_regions") or []:
        if not isinstance(pr, dict):
            continue
        pclass = pr.get("recommended_provider_class")
        fallback = "future_heavy_provider_candidate" if "lightweight" in str(pclass) else "rapidocr_or_paddleocr_lightweight"
        rows.append(
            {
                "region_id": pr.get("source_region_id"),
                "recommended_provider_class": pclass,
                "provider_priority": pr.get("priority"),
                "fallback_provider_class": fallback,
                "direct_model_invocation_allowed": False,
                "provider_invoked": False,
                "provider_selection_status": "planned_only",
                "rapidocr_enabled": False,
                "paddleocr_enabled": False,
            }
        )
    return {"schema_version": PROVIDER_SCHEMA, "row_count": len(rows), "rows": rows}


def build_reading_order_guard(*, poster_root: Path) -> Dict[str, Any]:
    ro = _read_json(poster_root / "poster_reading_order_candidate.json") or {}
    return {
        "schema_version": READING_GUARD_SCHEMA,
        "reading_order_confidence": ro.get("reading_order_confidence", "low"),
        "force_semantic_join_allowed": False,
        "semantic_join_status": "forbidden_in_this_phase",
        "ordered_region_ids": list(ro.get("ordered_region_ids") or []),
        "reason_codes": list(ro.get("reason_codes") or [])
        + ["region_plan_stub_only"],
    }


def build_metrics_binding_report() -> Dict[str, Any]:
    return {
        "schema_version": METRICS_BINDING_SCHEMA,
        "bound_metrics": [
            "ocr_region_plan_count",
            "text_region_count",
            "non_text_region_count",
            "visual_symbol_region_count",
            "full_image_ocr_forbidden_count",
            "reading_order_low_confidence_count",
            "visual_symbol_split_count",
            "performance_metrics_available",
            "per_case_latency_ms",
            "total_pipeline_latency_ms",
        ],
        "ocr_region_plan_count_value": 4,
        "performance_metrics_are_placeholders": True,
    }


def build_gate_policy() -> Dict[str, Any]:
    return {
        "schema_version": GATE_SCHEMA,
        "full_image_ocr_allowed": False,
        "only_text_regions_planned": True,
        "logo_qr_excluded_from_ordinary_ocr": True,
        "layout_text_evidence_not_fact": True,
        "commercial_text_requires_ttl": True,
        "reading_order_low_confidence_blocks_semantic_join": True,
        "world_model_write_allowed": False,
        "scene_delta_write_allowed": False,
        "auto_approval_allowed": False,
        "midplatform_fact_write_allowed": False,
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "poster_region_ocr_plan_stub_executed": True,
        "plan_only": True,
        "full_image_ocr_allowed": False,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "vision_provider_invoked": False,
        "vlm_invoked": False,
        "ai_interpretation_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
    }


def build_summary(
    *,
    poster_root: Path,
    realvideo_root: Path,
    metrics_collector_root: Path,
    plan_count: int,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "plan_scope": "ocr_plan_stub_only",
        "based_on_poster_governance": poster_root.is_dir(),
        "based_on_realvideo_registry": realvideo_root.is_dir(),
        "based_on_metrics_collector": metrics_collector_root.is_dir(),
        "poster_governance_root": str(poster_root),
        "realvideo_registry_root": str(realvideo_root),
        "metrics_collector_root": str(metrics_collector_root),
        "planned_region_count": plan_count,
        "full_image_ocr_allowed": False,
        "ocr_strategy": "segment_first",
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_poster_region_ocr_plan_stub_v0(
    *,
    poster_governance_root: str,
    realvideo_registry_root: str,
    metrics_collector_root: str,
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
    List[str],
]:
    errs: List[str] = []
    poster = Path(poster_governance_root).resolve()
    rv = Path(realvideo_registry_root).resolve()
    mc = Path(metrics_collector_root).resolve()

    if not _read_json(poster / "poster_layout_governance_summary.json"):
        errs.append("missing_poster_governance_summary")
    if not _read_json(poster / "poster_text_region_candidates.json"):
        errs.append("missing_text_region_candidates")

    plan = build_plan_stub(poster_root=poster)
    if plan.get("planned_region_count") != 4:
        errs.append("planned_region_count_not_4")

    excluded = build_excluded_report(poster_root=poster)
    risk = build_risk_matrix(plan)
    provider = build_provider_plan_matrix(plan)
    reading = build_reading_order_guard(poster_root=poster)
    metrics_binding = build_metrics_binding_report()
    gate = build_gate_policy()
    audit = build_audit()

    summary = build_summary(
        poster_root=poster,
        realvideo_root=rv,
        metrics_collector_root=mc,
        plan_count=int(plan.get("planned_region_count") or 0),
    )
    phase_verdict = "GO" if not errs else "NO_GO"
    summary["phase_verdict_hint"] = phase_verdict
    summary["errors"] = list(errs)

    return summary, plan, excluded, risk, provider, reading, metrics_binding, gate, audit, errs
