# -*- coding: utf-8 -*-
"""Document Surface Evidence Package Builder — dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_document_surface_evidence_package(
    *,
    source_region_id: str,
    attention_gate_status: str,
    document_surface_candidates: List[Dict[str, Any]],
    relation_hint_candidates: List[Dict[str, Any]],
    entity_candidates: List[Dict[str, Any]],
    text_owner_assignment_candidates: List[Dict[str, Any]],
    validation_status_candidate: str = "pending_validation",
    next_slot_candidate: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "package_id": _uid("dsep"),
        "source_region_id": source_region_id,
        "attention_gate_status": attention_gate_status,
        "document_surface_candidates": document_surface_candidates,
        "relation_hint_candidates": relation_hint_candidates,
        "entity_candidates": entity_candidates,
        "text_owner_assignment_candidates": text_owner_assignment_candidates,
        "next_slot_candidate": next_slot_candidate,
        "validation_status_candidate": validation_status_candidate,
        "surface_candidate_before_text_owner": True,
        "no_ocr_text_output": True,
        "no_merge_overlapped_documents": len(document_surface_candidates) >= 1,
        "candidate_only": True,
        "not_fact": True,
    }
