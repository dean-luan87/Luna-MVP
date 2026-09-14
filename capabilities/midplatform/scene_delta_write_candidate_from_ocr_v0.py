# -*- coding: utf-8 -*-
"""Scene Delta write candidate derived from OCR ingest / read-only event payload (stub).

Phase-MidPlatform-Scene-Delta-Write-Candidate-From-OCR-Ingest-Stub-001 — candidate JSON only;
no Scene Delta write, no fact layer, no WorldModel, no AI interpretation.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

WRITE_CANDIDATE_SCHEMA = "scene_delta_write_candidate_from_ocr_v0"
WRITE_CANDIDATE_AUDIT_SCHEMA = "scene_delta_write_candidate_from_ocr_audit_v0"

FORBIDDEN_TOPLEVEL_KEYS = frozenset(
    {
        "semantic_summary",
        "inferred_meaning",
        "object_meaning",
        "business_meaning",
        "environment_interpretation",
        "user_facing_explanation",
    }
)


def _provider_from_payload(provider_summary: Any) -> str:
    if not isinstance(provider_summary, dict):
        return "unknown_provider"
    pt = provider_summary.get("provider_trace")
    if isinstance(pt, dict) and pt.get("provider"):
        return str(pt.get("provider"))
    return "unknown_provider"


def _flatten_evidence_by_roi(evidence_by_roi: Any) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not isinstance(evidence_by_roi, dict):
        return rows
    for _roi_key, items in sorted(evidence_by_roi.items()):
        if not isinstance(items, list):
            continue
        for it in items:
            if isinstance(it, dict):
                rows.append(it)
    rows.sort(key=lambda r: (int(r.get("line_order") or 0), str(r.get("roi_id") or "")))
    return rows


def _has_original_geometry(it: Dict[str, Any]) -> bool:
    ob = it.get("original_bbox")
    if isinstance(ob, list) and len(ob) == 4:
        return True
    op = it.get("original_polygon")
    return isinstance(op, list) and len(op) > 0


def build_evidence_items_from_ocr_payload_v0(
    *,
    evidence_by_roi: Any,
    provider_name: str,
) -> Tuple[List[Dict[str, Any]], List[str]]:
    errs: List[str] = []
    items: List[Dict[str, Any]] = []
    for idx, row in enumerate(_flatten_evidence_by_roi(evidence_by_roi)):
        text = str(row.get("text") or "").strip()
        if not text:
            errs.append(f"evidence_missing_text_at_{idx}")
        roi_ok = bool(str(row.get("roi_id") or "").strip())
        unit_ok = bool(str(row.get("unit_id") or "").strip())
        if not roi_ok and not unit_ok:
            errs.append(f"evidence_missing_roi_or_unit_at_{idx}")
        if not _has_original_geometry(row):
            errs.append(f"evidence_missing_original_geometry_at_{idx}")
        conf = row.get("confidence")
        conf_out: Optional[float]
        if conf is None:
            conf_out = None
        else:
            try:
                conf_out = float(conf)
            except (TypeError, ValueError):
                conf_out = None
        items.append(
            {
                "text": str(row.get("text") or ""),
                "roi_id": row.get("roi_id"),
                "unit_id": row.get("unit_id"),
                "source_unit_ref": row.get("source_unit_ref"),
                "original_bbox": row.get("original_bbox"),
                "original_polygon": row.get("original_polygon"),
                "provider": provider_name,
                "confidence": conf_out,
                "evidence_role": "observed_text",
                "fact_status": "not_fact",
                "scene_delta_disposition": "scene_delta_candidate_later",
                "line_order": row.get("line_order"),
            }
        )
    return items, errs


def build_scene_delta_write_candidate_gate_stub_v0() -> Dict[str, Any]:
    return {
        "schema": "scene_delta_write_candidate_gate_stub_v0",
        "gate_required": True,
        "gate_status": "not_evaluated",
        "gate_reason_codes": [
            "ocr_evidence_requires_scene_delta_gate",
            "no_ai_interpretation",
            "no_world_fact_write",
        ],
    }


def build_scene_delta_write_candidate_audit_v0() -> Dict[str, Any]:
    return {
        "schema": WRITE_CANDIDATE_AUDIT_SCHEMA,
        "scene_delta_write_candidate_generated": True,
        "scene_delta_written": False,
        "midplatform_fact_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "database_write_invoked": False,
        "external_bus_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_routing_changed": False,
    }


def build_scene_delta_write_candidate_from_ocr_v0(
    *,
    event_payload: Dict[str, Any],
    geometry_matrix: Any,
) -> Tuple[Dict[str, Any], List[str]]:
    """
    Build write candidate from ``ocr_ingest_readonly_event_payload_v0``-shaped dict.

    ``geometry_matrix`` is the loaded JSON array from ``geometry_matrix_ref`` (for lineage / matrix export).
    """
    errs: List[str] = []

    ebr = event_payload.get("evidence_by_roi")
    provider = _provider_from_payload(event_payload.get("provider_summary"))
    evidence_items, e_errs = build_evidence_items_from_ocr_payload_v0(evidence_by_roi=ebr, provider_name=provider)
    errs.extend(e_errs)

    evc = len(evidence_items) if evidence_items else int(event_payload.get("evidence_count") or 0)
    tj = str(event_payload.get("text_joined") or "").strip()
    if evc < 1:
        errs.append("evidence_count_lt_1")
    if not tj:
        errs.append("text_joined_empty")
    if not evidence_items:
        errs.append("evidence_items_empty")

    scs = event_payload.get("source_chain_summary")
    if not isinstance(scs, dict):
        errs.append("source_chain_summary_missing")
        scs_out: Dict[str, Any] = {}
    else:
        scs_out = dict(scs)

    if not isinstance(geometry_matrix, list):
        errs.append("geometry_matrix_not_list")

    event_id = str(event_payload.get("event_id") or "").strip() or "unknown_event"
    ingest_cid = str(event_payload.get("candidate_id") or "").strip() or "unknown_ingest_candidate"

    candidate: Dict[str, Any] = {
        "schema_version": WRITE_CANDIDATE_SCHEMA,
        "candidate_id": f"sd_ocr_write_cand_{uuid.uuid4().hex}",
        "source_event_id": event_id,
        "source_ingest_candidate_id": ingest_cid,
        "source_type": "ocr_evidence",
        "candidate_scope": "write_candidate_only",
        "write_allowed": False,
        "requires_gate_approval": True,
        "evidence_count": evc,
        "text_joined": tj,
        "evidence_items": evidence_items,
        "spatial_reference": {
            "geometry_source": "ocr_original_geometry",
            "coordinate_space": "source_image",
        },
        "source_chain_summary": scs_out,
        "forbidden_actions": {
            "write_scene_delta": True,
            "write_midplatform_fact": True,
            "write_world_model": True,
            "invoke_ai_interpretation": True,
        },
    }
    return candidate, errs


def collect_forbidden_keys_in_object_v0(obj: Any, *, path: str = "$") -> List[str]:
    """Return paths where dict keys match forbidden AI / interpretation key names."""
    hits: List[str] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            if ks in FORBIDDEN_TOPLEVEL_KEYS:
                hits.append(f"{path}.{ks}")
            hits.extend(collect_forbidden_keys_in_object_v0(v, path=f"{path}.{ks}"))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits.extend(collect_forbidden_keys_in_object_v0(v, path=f"{path}[{i}]"))
    return hits

