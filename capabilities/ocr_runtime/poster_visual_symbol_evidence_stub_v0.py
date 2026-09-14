# -*- coding: utf-8 -*-
"""Poster VisualSymbolEvidence stub (no OCR, no QR decode, no brand ID).

Phase-OCR-Poster-VisualSymbolEvidence-Stub-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "OCR-Poster-VisualSymbolEvidence-Stub-001"

SUMMARY_SCHEMA = "poster_visual_symbol_evidence_stub_summary_v0"
SCHEMA_STUB_SCHEMA = "poster_visual_symbol_evidence_schema_stub_v0"
ITEMS_SCHEMA = "poster_visual_symbol_evidence_items_v0"
MATRIX_SCHEMA = "poster_visual_symbol_evidence_matrix_v0"
EXCLUSION_LINK_SCHEMA = "poster_visual_symbol_ocr_exclusion_link_report_v0"
QR_LOGO_POLICY_SCHEMA = "poster_visual_symbol_qr_logo_policy_report_v0"
RISK_SCHEMA = "poster_visual_symbol_risk_report_v0"
METRICS_BINDING_SCHEMA = "poster_visual_symbol_metrics_binding_report_v0"
GATE_SCHEMA = "poster_visual_symbol_gate_policy_report_v0"
AUDIT_SCHEMA = "poster_visual_symbol_evidence_stub_audit_v0"

ITEM_SPECS: Tuple[Dict[str, Any], ...] = (
    {
        "source_region_id": "logo_area",
        "region_type": "logo_area",
        "symbol_candidate_type": "logo_candidate",
        "semantic_candidate": "unknown_brand_or_logo",
        "qr_decode_status": "not_applicable",
        "brand_identity_status": "not_confirmed",
        "risk_flags": ["visual_symbol_not_plain_text", "logo_not_brand_fact", "no_ordinary_ocr_chain"],
    },
    {
        "source_region_id": "qr_area",
        "region_type": "qr_area",
        "symbol_candidate_type": "qr_candidate",
        "semantic_candidate": "qr_or_barcode_candidate",
        "qr_decode_status": "not_decoded",
        "brand_identity_status": "not_applicable",
        "risk_flags": ["visual_symbol_not_plain_text", "qr_not_decoded", "no_ordinary_ocr_chain"],
    },
    {
        "source_region_id": "product_or_decoration_area",
        "region_type": "product_or_decoration_area",
        "symbol_candidate_type": "non_text_visual_candidate",
        "semantic_candidate": "product_or_decoration_candidate",
        "qr_decode_status": "not_applicable",
        "brand_identity_status": "not_applicable",
        "risk_flags": ["product_visual_not_text", "commercial_symbol_not_fact", "no_ordinary_ocr_chain"],
    },
    {
        "source_region_id": "background_or_decoration_area",
        "region_type": "background_or_decoration_area",
        "symbol_candidate_type": "background_or_decoration_candidate",
        "semantic_candidate": "non_text_background_candidate",
        "qr_decode_status": "not_applicable",
        "brand_identity_status": "not_applicable",
        "risk_flags": ["product_visual_not_text", "no_ordinary_ocr_chain"],
    },
)


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def build_schema_stub(*, source_image_ref: str) -> Dict[str, Any]:
    return {
        "schema_version": SCHEMA_STUB_SCHEMA,
        "field_definitions": {
            "evidence_id": {"type": "string", "required": True},
            "evidence_type": {"type": "string", "default": "VisualSymbolEvidence"},
            "source_image_ref": {"type": "string", "required": True},
            "source_region_id": {"type": "string", "required": True},
            "source_region_type": {"type": "string", "required": True},
            "bbox": {"type": "array", "items": "integer", "length": 4},
            "symbol_candidate_type": {"type": "string", "required": True},
            "semantic_candidate": {"type": "string", "required": True},
            "raw_visual_region_ref": {"type": "string", "required": True},
            "ocr_chain_allowed": {"type": "boolean", "default": False},
            "qr_decode_status": {"type": "string"},
            "brand_identity_status": {"type": "string"},
            "fact_status": {"type": "string", "default": "not_fact"},
            "confidence": {"type": "null", "default": None},
            "requires_review": {"type": "boolean", "default": True},
            "write_allowed": {"type": "boolean", "default": False},
            "source_chain": {"type": "object"},
            "risk_flags": {"type": "array", "items": "string"},
        },
        "source_image_ref": source_image_ref,
    }


def _build_item(
    spec: Dict[str, Any],
    *,
    bbox: List[int],
    source_image_ref: str,
    poster_gov_ref: str,
    ocr_plan_ref: str,
) -> Dict[str, Any]:
    rid = spec["source_region_id"]
    return {
        "evidence_id": f"vse_{rid}_v0",
        "evidence_type": "VisualSymbolEvidence",
        "source_image_ref": source_image_ref,
        "source_region_id": rid,
        "source_region_type": spec["region_type"],
        "bbox": bbox,
        "symbol_candidate_type": spec["symbol_candidate_type"],
        "semantic_candidate": spec["semantic_candidate"],
        "raw_visual_region_ref": f"{source_image_ref}#region={rid}",
        "ocr_chain_allowed": False,
        "qr_decode_status": spec["qr_decode_status"],
        "brand_identity_status": spec["brand_identity_status"],
        "fact_status": "not_fact",
        "confidence": None,
        "requires_review": True,
        "write_allowed": False,
        "source_chain": {
            "poster_layout_governance_ref": poster_gov_ref,
            "poster_region_ocr_plan_ref": ocr_plan_ref,
            "visual_symbol_evidence_stub_built": True,
        },
        "risk_flags": list(spec["risk_flags"]),
    }


def build_evidence_items(
    *,
    poster_root: Path,
    ocr_plan_root: Path,
    source_image_ref: str,
) -> Dict[str, Any]:
    excluded_doc = _read_json(ocr_plan_root / "poster_region_ocr_excluded_regions_report.json") or {}
    excluded = {r["region_id"]: r for r in (excluded_doc.get("excluded_regions") or []) if isinstance(r, dict)}
    poster_gov_ref = str(poster_root / "poster_layout_governance_summary.json")
    ocr_plan_ref = str(ocr_plan_root / "poster_region_ocr_plan_stub.json")

    items = []
    for spec in ITEM_SPECS:
        rid = spec["source_region_id"]
        ex = excluded.get(rid, {})
        items.append(
            _build_item(
                spec,
                bbox=list(ex.get("bbox") or []),
                source_image_ref=source_image_ref,
                poster_gov_ref=poster_gov_ref,
                ocr_plan_ref=ocr_plan_ref,
            )
        )
    return {"schema_version": ITEMS_SCHEMA, "item_count": len(items), "items": items}


def build_matrix(items_doc: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for it in items_doc.get("items") or []:
        if not isinstance(it, dict):
            continue
        rows.append(
            {
                "evidence_id": it.get("evidence_id"),
                "source_region_id": it.get("source_region_id"),
                "symbol_candidate_type": it.get("symbol_candidate_type"),
                "semantic_candidate": it.get("semantic_candidate"),
                "ocr_chain_allowed": it.get("ocr_chain_allowed"),
                "qr_decode_status": it.get("qr_decode_status"),
                "brand_identity_status": it.get("brand_identity_status"),
                "fact_status": it.get("fact_status"),
                "write_allowed": it.get("write_allowed"),
                "risk_flags": it.get("risk_flags"),
            }
        )
    return {"schema_version": MATRIX_SCHEMA, "row_count": len(rows), "rows": rows}


def build_ocr_exclusion_link(
    *,
    ocr_plan_root: Path,
    items_doc: Dict[str, Any],
    excluded_doc: Dict[str, Any],
) -> Dict[str, Any]:
    plan = _read_json(ocr_plan_root / "poster_region_ocr_plan_stub.json") or {}
    planned_ids = {
        pr.get("source_region_id")
        for pr in (plan.get("planned_regions") or [])
        if isinstance(pr, dict)
    }
    visual_ids = [it.get("source_region_id") for it in (items_doc.get("items") or []) if isinstance(it, dict)]
    excluded_ids = [r.get("region_id") for r in (excluded_doc.get("excluded_regions") or []) if isinstance(r, dict)]

    checks = []
    for rid in ("logo_area", "qr_area", "product_or_decoration_area", "background_or_decoration_area"):
        checks.append(
            {
                "region_id": rid,
                "in_ocr_planned_regions": rid in planned_ids,
                "in_visual_symbol_items": rid in visual_ids,
                "in_excluded_regions_report": rid in excluded_ids,
            }
        )

    return {
        "schema_version": EXCLUSION_LINK_SCHEMA,
        "ordinary_ocr_text_chain_excludes_logo_qr": True,
        "planned_region_ids": sorted(planned_ids),
        "visual_symbol_region_ids": visual_ids,
        "excluded_region_ids": excluded_ids,
        "per_region_checks": checks,
        "all_visual_regions_absent_from_ocr_plan": all(not c["in_ocr_planned_regions"] for c in checks),
    }


def build_qr_logo_policy() -> Dict[str, Any]:
    return {
        "schema_version": QR_LOGO_POLICY_SCHEMA,
        "qr_decoding_allowed_in_this_phase": False,
        "qr_decoded": False,
        "logo_brand_identification_allowed_in_this_phase": False,
        "brand_identity_confirmed": False,
        "commercial_fact_allowed": False,
        "external_brand_database_invoked": False,
        "cn_visual_symbol_registry_invoked": False,
        "future_visual_symbol_registry_required": True,
    }


def build_risk_report() -> Dict[str, Any]:
    risks = [
        ("visual_symbol_not_plain_text", "Logo/QR/icons are not plain OCR text"),
        ("logo_not_brand_fact", "Logo must not become brand fact"),
        ("qr_not_decoded", "QR content not decoded in stub phase"),
        ("product_visual_not_text", "Product/decoration is visual not text"),
        ("commercial_symbol_not_fact", "Commercial symbols are not durable facts"),
        ("no_ordinary_ocr_chain", "Visual symbols excluded from ordinary OCR chain"),
        ("no_world_model_write", "No WorldModel writes from visual symbols"),
        ("no_auto_approval", "No auto-approval from visual symbol stub"),
        ("requires_visual_symbol_registry_later", "Future CN/visual symbol registry may be required"),
    ]
    return {
        "schema_version": RISK_SCHEMA,
        "risks": [{"risk_id": rid, "description": desc} for rid, desc in risks],
    }


def build_metrics_binding() -> Dict[str, Any]:
    return {
        "schema_version": METRICS_BINDING_SCHEMA,
        "bound_metrics": [
            "visual_symbol_region_count",
            "visual_symbol_split_count",
            "full_image_ocr_forbidden_count",
            "non_text_region_count",
            "poster_image_count",
            "reference_candidate_count",
            "no_write_boundary_pass_rate",
            "future_visual_symbol_match_count",
            "future_qr_decode_count",
        ],
        "placeholder_metrics": [
            "reference_candidate_count",
            "future_visual_symbol_match_count",
            "future_qr_decode_count",
        ],
    }


def build_gate_policy() -> Dict[str, Any]:
    return {
        "schema_version": GATE_SCHEMA,
        "visual_symbol_evidence_not_fact": True,
        "ordinary_ocr_chain_allowed": False,
        "qr_decode_allowed": False,
        "brand_identity_confirm_allowed": False,
        "world_model_write_allowed": False,
        "scene_delta_write_allowed": False,
        "midplatform_fact_write_allowed": False,
        "auto_approval_allowed": False,
        "requires_midplatform_arbitration": True,
    }


def build_audit() -> Dict[str, Any]:
    return {
        "schema_version": AUDIT_SCHEMA,
        "poster_visual_symbol_evidence_stub_executed": True,
        "evidence_stub_only": True,
        "visual_symbol_evidence_generated": True,
        "ocr_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "qr_decoder_invoked": False,
        "brand_database_invoked": False,
        "visual_symbol_registry_invoked": False,
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
    ocr_plan_root: Path,
    metrics_collector_root: Path,
    realvideo_root: Path,
    item_count: int,
) -> Dict[str, Any]:
    return {
        "schema_version": SUMMARY_SCHEMA,
        "phase": PHASE_ID,
        "evidence_scope": "visual_symbol_stub_only",
        "based_on_poster_governance": poster_root.is_dir(),
        "based_on_region_ocr_plan": ocr_plan_root.is_dir(),
        "based_on_metrics_collector": metrics_collector_root.is_dir(),
        "based_on_realvideo_registry": realvideo_root.is_dir(),
        "poster_governance_root": str(poster_root),
        "poster_region_ocr_plan_root": str(ocr_plan_root),
        "visual_symbol_item_count": item_count,
        "ordinary_ocr_chain_excluded": True,
        "visual_symbol_evidence_generated": True,
        "qr_decoded": False,
        "brand_identity_confirmed": False,
        "ocr_invoked": False,
        "vision_provider_invoked": False,
        "fact_status": "not_fact",
        "write_allowed": False,
    }


def run_poster_visual_symbol_evidence_stub_v0(
    *,
    poster_governance_root: str,
    poster_region_ocr_plan_root: str,
    metrics_collector_root: str,
    realvideo_registry_root: str,
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
    List[str],
]:
    errs: List[str] = []
    poster = Path(poster_governance_root).resolve()
    plan = Path(poster_region_ocr_plan_root).resolve()
    mc = Path(metrics_collector_root).resolve()
    rv = Path(realvideo_registry_root).resolve()

    if not _read_json(poster / "poster_layout_governance_summary.json"):
        errs.append("missing_poster_governance")
    if not _read_json(plan / "poster_region_ocr_plan_stub.json"):
        errs.append("missing_ocr_plan")

    manifest = _read_json(poster / "poster_synthetic_fixture_manifest.json") or {}
    source_image_ref = str(manifest.get("source_image_ref") or "")

    schema_stub = build_schema_stub(source_image_ref=source_image_ref)
    items = build_evidence_items(
        poster_root=poster,
        ocr_plan_root=plan,
        source_image_ref=source_image_ref,
    )
    matrix = build_matrix(items)
    excluded_doc = _read_json(plan / "poster_region_ocr_excluded_regions_report.json") or {}
    exclusion = build_ocr_exclusion_link(ocr_plan_root=plan, items_doc=items, excluded_doc=excluded_doc)
    qr_logo = build_qr_logo_policy()
    risks = build_risk_report()
    metrics_binding = build_metrics_binding()
    gate = build_gate_policy()
    audit = build_audit()

    if int(items.get("item_count") or 0) < 4:
        errs.append("item_count_below_4")

    summary = build_summary(
        poster_root=poster,
        ocr_plan_root=plan,
        metrics_collector_root=mc,
        realvideo_root=rv,
        item_count=int(items.get("item_count") or 0),
    )
    phase_verdict = "GO" if not errs else "CONDITIONAL_GO"
    summary["phase_verdict_hint"] = phase_verdict
    summary["errors"] = list(errs)

    return summary, schema_stub, items, matrix, exclusion, qr_logo, risks, metrics_binding, gate, audit, errs
