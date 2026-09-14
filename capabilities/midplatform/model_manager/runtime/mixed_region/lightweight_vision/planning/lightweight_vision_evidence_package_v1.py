# -*- coding: utf-8 -*-
"""Lightweight Vision Evidence Package Builder v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_lightweight_vision_evidence_package(
    *,
    source_region_id: str,
    attention_gate_status: str,
    runtime_execution: Dict[str, Any],
    per_entity_channel_activation: Optional[List[Dict[str, Any]]] = None,
    validation_status_candidate: str = "pending_validation",
) -> Dict[str, Any]:
    return {
        "lightweight_vision_evidence_package": {
            "package_id": _uid("lvep"),
            "source_region_id": source_region_id,
            "attention_gate_status": attention_gate_status,
            "runtime_candidates": runtime_execution.get("runtime_candidates") or [],
            "entity_candidates": runtime_execution.get("entity_candidates") or [],
            "relation_candidates": runtime_execution.get("relation_candidates") or [],
            "layout_region_candidates": runtime_execution.get("layout_region_candidates") or [],
            "per_entity_channel_activation_candidates": per_entity_channel_activation or [],
            "validation_status_candidate": validation_status_candidate,
            "candidate_only": True,
            "not_fact": True,
        },
        "runtime_outputs_candidate_only": True,
        "runtime_does_not_assign_fact": True,
        "runtime_does_not_override_ownership_graph": True,
    }
