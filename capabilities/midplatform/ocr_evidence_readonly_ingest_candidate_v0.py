# -*- coding: utf-8 -*-
"""MidPlatform OCR evidence read-only ingest candidate (Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001).

No fact writes, no Scene Delta, no WorldModel, no AI interpretation, no OCR provider calls.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

INGEST_CANDIDATE_SCHEMA = "midplatform_ocr_evidence_ingest_candidate_v0"
INGEST_AUDIT_SCHEMA = "midplatform_ocr_evidence_ingest_audit_v0"


def build_text_matrix_from_evidence_by_roi_v0(evidence_by_roi: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for roi_id, items in sorted(evidence_by_roi.items()):
        if not isinstance(items, list):
            continue
        for it in items:
            if not isinstance(it, dict):
                continue
            rows.append(
                {
                    "roi_id": it.get("roi_id") or roi_id,
                    "unit_id": it.get("unit_id"),
                    "line_order": it.get("line_order"),
                    "text": str(it.get("text") or ""),
                    "confidence": it.get("confidence"),
                    "source_unit_ref": it.get("source_unit_ref"),
                }
            )
    return rows


def build_midplatform_ocr_evidence_ingest_candidate_v0(
    *,
    consumer_view: Dict[str, Any],
    evidence_by_roi: Dict[str, Any],
    geometry_matrix: List[Any],
    source_chain_summary: Dict[str, Any],
    provider_summary: Dict[str, Any],
    source_consumer_view_ref: str,
) -> Tuple[Dict[str, Any], List[str]]:
    """Assemble ingest candidate JSON. Returns (candidate, validation_errors)."""
    errs: List[str] = []
    if not str(source_consumer_view_ref or "").strip():
        errs.append("missing_source_consumer_view_ref")

    ev_count = int(consumer_view.get("evidence_count") or 0)
    text_joined = str(consumer_view.get("text_joined") or "").strip()
    if ev_count < 1:
        errs.append("evidence_count_lt_1")
    if not text_joined:
        errs.append("text_joined_empty")

    if not isinstance(evidence_by_roi, dict) or not evidence_by_roi:
        errs.append("evidence_by_roi_empty")

    if not isinstance(geometry_matrix, list) or not geometry_matrix:
        errs.append("geometry_matrix_empty")

    if not isinstance(source_chain_summary, dict):
        errs.append("source_chain_summary_not_dict")
    elif "chain_item_count" not in source_chain_summary and "chain" not in source_chain_summary:
        errs.append("source_chain_summary_incomplete")

    if not isinstance(provider_summary, dict) or not provider_summary:
        errs.append("provider_summary_empty")

    candidate: Dict[str, Any] = {
        "schema_version": INGEST_CANDIDATE_SCHEMA,
        "candidate_id": f"mp_ocr_ingest_{uuid.uuid4().hex}",
        "source": "ocr_bridge_pack",
        "source_consumer_view_ref": str(source_consumer_view_ref),
        "evidence_count": ev_count,
        "text_joined": text_joined,
        "evidence_by_roi": evidence_by_roi,
        "geometry_matrix": geometry_matrix,
        "provider_summary": provider_summary,
        "source_chain_summary": source_chain_summary,
        "ingest_scope": "read_only_candidate",
        "allowed_next_actions": [
            "manual_review",
            "scene_delta_candidate_later",
            "ai_interpretation_later",
        ],
        "forbidden_actions": {
            "write_midplatform_fact": True,
            "write_scene_delta": True,
            "write_world_model": True,
            "invoke_ai_interpretation": True,
        },
    }
    return candidate, errs


def build_midplatform_ocr_evidence_ingest_audit_v0() -> Dict[str, Any]:
    return {
        "schema": INGEST_AUDIT_SCHEMA,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "ai_interpretation_invoked": False,
        "ocr_provider_invoked": False,
        "ocr_routing_changed": False,
    }


def build_ingest_summary_v0(
    *,
    input_consumer_root: str,
    candidate: Dict[str, Any],
    validation_errors: List[str],
    input_paths: Dict[str, str],
) -> Dict[str, Any]:
    return {
        "schema": "midplatform_ocr_evidence_ingest_candidate_summary_v0",
        "phase": "Phase-MidPlatform-OCR-Evidence-ReadOnly-Ingest-Candidate-001",
        "input_consumer_root": input_consumer_root,
        "input_paths": input_paths,
        "candidate_id": candidate.get("candidate_id"),
        "ingest_candidate_path": None,
        "validation_ok": len(validation_errors) == 0,
        "validation_errors": list(validation_errors),
        "evidence_count": candidate.get("evidence_count"),
        "ingest_scope": candidate.get("ingest_scope"),
    }
