# -*- coding: utf-8 -*-
"""Ownership Discovery Simulator — slot_ownership_discovery dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.slot_ownership_discovery_v1 import (
    run_slot_ownership_discovery,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def simulate_ownership_discovery(
    *,
    fixture: Dict[str, Any],
    slot_binding: Dict[str, Any],
) -> Dict[str, Any]:
    """slot_ownership_discovery — entity / surface discovery in gated region only."""
    if slot_binding.get("binding_status") != "bound":
        return {
            "slot_id": "slot_ownership_discovery",
            "slot_status": "skipped_gate_blocked",
            "entity_candidates": [],
            "candidate_only": True,
        }

    gate = fixture.get("attention_gate") or {}
    result = run_slot_ownership_discovery(
        profile_key=fixture.get("profile_key", "stacked_documents"),
        attention_gate=gate,
        entity_id_map=fixture.get("entity_id_map") or {},
        blocked_entity_ids=_blocked_ids(fixture),
        upstream_region_id=slot_binding.get("source_region_id", "region_001"),
    )

    entities: List[Dict[str, Any]] = []
    for e in result.get("entity_candidates") or []:
        entities.append({
            "entity_id": e.get("entity_id"),
            "entity_type_candidate": f"{e.get('entity_type_candidate', 'unknown')}_surface",
            "attention_gate": e.get("attention_gate", "allowed"),
            "ownership_candidate": e.get("ownership_candidate"),
            "candidate_only": True,
            "not_fact": True,
        })

    return {
        "slot_id": "slot_ownership_discovery",
        "slot_status": "completed",
        "discovery_id": _uid("ods"),
        "entity_candidates": entities,
        "entity_count": len(entities),
        "carrier_before_ocr": result.get("carrier_before_ocr") is True,
        "not_global_ocr": True,
        "candidate_only": True,
    }


def _blocked_ids(fixture: Dict[str, Any]) -> List[str]:
    from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.dryrun_fixtures_v1 import (
        blocked_entity_ids,
    )
    return blocked_entity_ids(fixture)
