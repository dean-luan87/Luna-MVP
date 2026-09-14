# -*- coding: utf-8 -*-
"""Read-only consumer for OCR bridge_pack (Phase-OCR-Evidence-Consumer-ReadOnly-Smoke-001).

Does not write MidPlatform, Scene Delta, or WorldModel; does not invoke AI interpretation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

BRIDGE_PACK_SCHEMA = "ocr_evidence_pack_candidate_v0"
CONSUMER_VIEW_SCHEMA = "ocr_evidence_readonly_consumer_view_v0"
CONSUMER_AUDIT_SCHEMA = "ocr_evidence_readonly_consumer_audit_v0"


def validate_bridge_pack_schema_v0(bridge_pack: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs: List[str] = []
    if not isinstance(bridge_pack, dict):
        return False, ["bridge_pack_not_dict"]
    if str(bridge_pack.get("schema_version") or "") != BRIDGE_PACK_SCHEMA:
        errs.append(f"bridge_pack_schema_version_expected_{BRIDGE_PACK_SCHEMA}")
    return (len(errs) == 0, errs)


def _canonical_evidence_row_v0(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "line_order": row.get("line_order"),
        "text": str(row.get("text") or ""),
        "confidence": float(row.get("confidence") or row.get("score") or 0.0),
        "roi_id": row.get("roi_id"),
        "unit_id": row.get("unit_id"),
        "source_unit_ref": row.get("source_unit_ref"),
        "coordinate_lift_applied": row.get("coordinate_lift_applied"),
        "local_bbox": row.get("local_bbox"),
        "local_polygon": row.get("local_polygon"),
        "original_bbox": row.get("original_bbox"),
        "original_polygon": row.get("original_polygon"),
        "roi_bbox_in_original": row.get("roi_bbox_in_original"),
        "evidence_scope": row.get("evidence_scope"),
    }


def build_readonly_consumer_view_v0(
    bridge_pack: Dict[str, Any],
    *,
    source_reference_chain: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build ``read_only_consumer_view`` from ``bridge_pack`` only (no side effects)."""
    elig = bridge_pack.get("eligible_text_evidence") if isinstance(bridge_pack.get("eligible_text_evidence"), list) else []
    texts: List[str] = []
    by_roi: Dict[str, List[Dict[str, Any]]] = {}
    geom_matrix: List[Dict[str, Any]] = []

    for row in elig:
        if not isinstance(row, dict):
            continue
        t = str(row.get("text") or "").strip()
        if t:
            texts.append(t)
        rid = str(row.get("roi_id") or "") or "_no_roi_id"
        by_roi.setdefault(rid, []).append(_canonical_evidence_row_v0(row))
        geom_matrix.append(
            {
                "line_order": row.get("line_order"),
                "roi_id": row.get("roi_id"),
                "unit_id": row.get("unit_id"),
                "source_unit_ref": row.get("source_unit_ref"),
                "local_bbox": row.get("local_bbox"),
                "local_polygon": row.get("local_polygon"),
                "original_bbox": row.get("original_bbox"),
                "original_polygon": row.get("original_polygon"),
            }
        )

    joined = str(bridge_pack.get("raw_text_joined") or "").strip()
    if not joined and texts:
        joined = " | ".join(texts)

    chain = list(source_reference_chain or [])
    chain_summary = {
        "chain_item_count": len(chain),
        "chain_head": chain[0] if chain else None,
        "chain_tail": chain[-1] if chain else None,
        "chain": chain,
    }

    return {
        "schema_version": CONSUMER_VIEW_SCHEMA,
        "evidence_count": len(elig),
        "text_joined": joined,
        "evidence_by_roi": by_roi,
        "evidence_geometry_matrix": geom_matrix,
        "provider_summary": {
            "provider_trace": bridge_pack.get("provider_trace"),
            "evidence_scope": bridge_pack.get("evidence_scope"),
            "full_image_claim_allowed": bridge_pack.get("full_image_claim_allowed"),
            "reading_order_confidence": bridge_pack.get("reading_order_confidence"),
        },
        "source_reference_chain_summary": chain_summary,
    }


def build_readonly_consumer_audit_v0() -> Dict[str, Any]:
    """Explicit read-only audit flags (consumer does not write external systems)."""
    return {
        "schema": CONSUMER_AUDIT_SCHEMA,
        "midplatform_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "paddleocr_invoked": False,
        "ocr_routing_changed": False,
    }


def run_ocr_evidence_readonly_consume_v0(
    bridge_pack: Dict[str, Any],
    *,
    source_reference_chain: Optional[List[str]] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], List[str]]:
    """
    Returns (summary, consumer_view, audit, validation_errors).

    ``validation_errors`` non-empty means bridge_pack schema failed; caller may still emit audit with NO_GO.
    """
    ok, errs = validate_bridge_pack_schema_v0(bridge_pack)
    view = build_readonly_consumer_view_v0(bridge_pack, source_reference_chain=source_reference_chain)
    audit = build_readonly_consumer_audit_v0()
    summary: Dict[str, Any] = {
        "schema": "ocr_evidence_readonly_consumer_summary_v0",
        "bridge_pack_schema_version": bridge_pack.get("schema_version"),
        "validation_ok": ok,
        "validation_errors": list(errs),
        "evidence_count": view.get("evidence_count"),
        "text_joined_preview": (str(view.get("text_joined") or ""))[:400],
        "roi_keys_in_evidence_by_roi": sorted((view.get("evidence_by_roi") or {}).keys()) if isinstance(view.get("evidence_by_roi"), dict) else [],
    }
    return summary, view, audit, errs
