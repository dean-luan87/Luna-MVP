# -*- coding: utf-8 -*-
"""Text Owner Assignment Simulator — slot_text_owner_assignment dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_real_runtime.planning.slot_text_owner_assignment_v1 import (
    run_slot_text_owner_assignment,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def simulate_text_owner_assignment(
    *,
    fixture: Dict[str, Any],
    discovery: Dict[str, Any],
    occlusion: Dict[str, Any],
) -> Dict[str, Any]:
    """slot_text_owner_assignment — every text region MUST bind owner_entity_id."""
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

    result = run_slot_text_owner_assignment(
        discovery=owner_discovery,
        occlusion=occlusion,
        profile_key=fixture.get("profile_key", "stacked_documents"),
        entity_id_map=fixture.get("entity_id_map") or {},
        blocked_entity_ids=_blocked_ids(fixture),
    )

    assignments: List[Dict[str, Any]] = []
    for t in result.get("text_owner_assignments") or []:
        assignments.append({
            "text_region_id": t.get("text_region_id"),
            "owner_entity_id": t.get("owner_entity_id"),
            "text_candidate": t.get("text_candidate"),
            "assignment_confidence": t.get("assignment_confidence", 0.0),
            "assignment_status": "assigned_candidate",
            "reflection_artifact": t.get("reflection_artifact", False),
            "partially_occluded": t.get("partially_occluded", False),
            "candidate_only": True,
            "not_fact": True,
        })

    return {
        "slot_id": "slot_text_owner_assignment",
        "slot_status": "completed",
        "assignment_id": _uid("toas"),
        "text_owner_assignments": assignments,
        "owner_required_for_text": all(a.get("owner_entity_id") for a in assignments),
        "no_flat_merge": result.get("not_flat_merge") is True,
        "no_global_ocr": True,
        "candidate_only": True,
    }
