# -*- coding: utf-8 -*-
"""Document Surface — candidate normalizer v1."""

from __future__ import annotations

from typing import Any, Dict, List

FORBIDDEN_OUTPUT_KEYS = (
    "ocr_text", "text_content", "document_type", "invoice_fact", "contract_fact",
    "receipt_fact", "layout_block", "owner_fact", "merged_document_content",
)


def normalize_document_surface_candidates(
    execution_result: Dict[str, Any],
    *,
    category: str,
) -> Dict[str, Any]:
    surfaces = execution_result.get("document_surface_candidates") or []
    normalized: List[Dict[str, Any]] = []
    for s in surfaces:
        item = {k: v for k, v in s.items() if k not in FORBIDDEN_OUTPUT_KEYS}
        item.setdefault("candidate_only", True)
        item.setdefault("not_fact", True)
        item.setdefault("output_type", "document_surface_candidate")
        normalized.append(item)

    return {
        "document_surface_candidates": normalized,
        "polygon_candidates": execution_result.get("polygon_candidates") or [],
        "quadrilateral_candidates": execution_result.get("quadrilateral_candidates") or [],
        "boundary_quality_candidate": execution_result.get("boundary_quality_candidate"),
        "runtime_status_candidate": execution_result.get("runtime_status_candidate"),
        "category": category,
        "candidate_only": True,
        "not_fact": True,
        "no_ocr_text": True,
        "no_fact_fields": not any(k in execution_result for k in FORBIDDEN_OUTPUT_KEYS),
    }
