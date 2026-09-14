# -*- coding: utf-8 -*-
"""Ownership Real Runtime Evidence Package Builder v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_ownership_evidence_package(
    *,
    entity_candidates: List[Dict[str, Any]],
    relation_candidates: List[Dict[str, Any]],
    text_owner_assignments: List[Dict[str, Any]],
    channel_activation: Dict[str, Any],
    missing_information: Optional[List[Dict[str, Any]]] = None,
    blocked_regions: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    return {
        "package_id": _uid("oep"),
        "entity_candidates": entity_candidates,
        "relation_candidates": relation_candidates,
        "text_owner_assignments": text_owner_assignments,
        "per_entity_channel_activation": channel_activation.get("per_entity_activation") or [],
        "missing_information_candidates": missing_information or [],
        "attention_blocked_regions": blocked_regions or [],
        "candidate_only": True,
        "not_fact": True,
    }
