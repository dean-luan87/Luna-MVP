# -*- coding: utf-8 -*-
"""Ownership Evidence Builder — Layer: who owns this information v1."""

from __future__ import annotations

from typing import Any, Dict
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_ownership_evidence(
    *,
    owner_analysis: Dict[str, Any],
    occlusion_graph: Dict[str, Any],
    text_assignment: Dict[str, Any],
) -> Dict[str, Any]:
    """Build Ownership Channel evidence — spatial ownership, not OCR."""
    return {
        "evidence_id": _uid("oev"),
        "type": "ownership_candidate",
        "object_candidates": owner_analysis.get("object_candidates") or [],
        "object_count": owner_analysis.get("object_count", 0),
        "occlusion_relation": occlusion_graph.get("occlusion_relation") or [],
        "per_owner_text_count": text_assignment.get("owner_count", 0),
        "text_with_owners": text_assignment.get("text_with_owners") or [],
        "per_owner_documents": text_assignment.get("per_owner_documents") or [],
        "region_discovery_before_ocr": True,
        "not_full_image_text_merge": True,
        "candidate_only": True,
        "not_fact": True,
    }
