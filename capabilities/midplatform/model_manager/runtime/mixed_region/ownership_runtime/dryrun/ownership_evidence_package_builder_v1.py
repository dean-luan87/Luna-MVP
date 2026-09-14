# -*- coding: utf-8 -*-
"""Ownership Evidence Package Builder — dryrun fixed output v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_ownership_evidence_package(
    *,
    source_region_id: str,
    attention_gate_status: str,
    entity_candidates: List[Dict[str, Any]],
    relation_candidates: List[Dict[str, Any]],
    text_owner_assignments: List[Dict[str, Any]],
    per_entity_channel_activation_candidates: List[Dict[str, Any]],
    missing_information_candidates: Optional[List[Dict[str, Any]]] = None,
    blocked_regions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    return {
        "ownership_evidence_package": {
            "package_id": _uid("oep"),
            "source_region_id": source_region_id,
            "attention_gate_status": attention_gate_status,
            "entity_candidates": entity_candidates,
            "relation_candidates": relation_candidates,
            "text_owner_assignments": text_owner_assignments,
            "per_entity_channel_activation_candidates": per_entity_channel_activation_candidates,
            "missing_information_candidates": missing_information_candidates or [],
            "attention_blocked_regions": blocked_regions or [],
            "candidate_only": True,
            "not_fact": True,
        },
        "no_global_ocr": True,
        "owner_required_for_text": all(
            t.get("owner_entity_id") for t in text_owner_assignments
        ) if text_owner_assignments else True,
        "candidate_only_not_fact": True,
    }
