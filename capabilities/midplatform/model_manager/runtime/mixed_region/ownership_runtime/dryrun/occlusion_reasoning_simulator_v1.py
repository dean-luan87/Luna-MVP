# -*- coding: utf-8 -*-
"""Occlusion Reasoning Simulator — slot_occlusion_reasoning dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.slot_occlusion_reasoning_v1 import (
    run_slot_occlusion_reasoning,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def simulate_occlusion_reasoning(
    *,
    fixture: Dict[str, Any],
    discovery: Dict[str, Any],
) -> Dict[str, Any]:
    """slot_occlusion_reasoning — occlusion / attachment / reflection relations."""
    from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_runtime.dryrun.ownership_discovery_simulator_v1 import (
        _blocked_ids,
    )

    owner_discovery = {
        "entity_candidates": [
            {
                "entity_id": e.get("entity_id"),
                "entity_type_candidate": (e.get("entity_type_candidate") or "").replace("_surface", ""),
                "ownership_candidate": e.get("ownership_candidate"),
            }
            for e in discovery.get("entity_candidates") or []
        ],
    }

    result = run_slot_occlusion_reasoning(
        discovery=owner_discovery,
        profile_key=fixture.get("profile_key", "stacked_documents"),
        entity_id_map=fixture.get("entity_id_map") or {},
        blocked_entity_ids=_blocked_ids(fixture),
    )

    relations: List[Dict[str, Any]] = []
    for r in result.get("relation_candidates") or []:
        relations.append({
            "relation_id": r.get("relation_id", _uid("rel")),
            "entity_a": r.get("entity_a"),
            "entity_b": r.get("entity_b"),
            "relation_type": r.get("relation_type"),
            "candidate_only": True,
            "not_fact": True,
        })

    return {
        "slot_id": "slot_occlusion_reasoning",
        "slot_status": "completed",
        "reasoning_id": _uid("ors"),
        "relation_candidates": relations,
        "occlusion_not_absence": result.get("not_assume_missing_absent") is True,
        "candidate_only": True,
    }
