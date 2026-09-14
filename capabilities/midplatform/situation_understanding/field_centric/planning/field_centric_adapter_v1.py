# -*- coding: utf-8 -*-
"""Field-Centric Object Role Planning Adapter v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.situation_understanding.field_centric.planning.attention_from_field_v1 import (
    allocate_attention_from_field,
)
from capabilities.midplatform.situation_understanding.field_centric.planning.field_understanding_v1 import (
    understand_field,
)
from capabilities.midplatform.situation_understanding.field_centric.planning.interaction_graph_v1 import (
    build_interaction_graph,
)
from capabilities.midplatform.situation_understanding.field_centric.planning.object_role_inference_v1 import (
    infer_object_roles,
)
from capabilities.midplatform.situation_understanding.field_centric.planning.unresolved_object_memory_v1 import (
    record_unresolved_objects,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_FIELD_CENTRIC_OBJECT_ROLE_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_FIELD_CENTRIC_OBJECT_ROLE_PLANNING_BLOCKED"

PLANNING_FIXTURES: Dict[str, Dict[str, Any]] = {
    "metal_rack_furniture": {
        "field_key": "home_furniture_store",
        "object_ids": ["metal_rack"],
        "interaction_fixture_key": "metal_rack_furniture",
        "goal_type": "understand_environment",
    },
    "metal_rack_construction": {
        "field_key": "construction_site",
        "object_ids": ["metal_rack"],
        "interaction_fixture_key": "metal_rack_construction",
        "goal_type": "assess_safety",
    },
    "person_machine_greenery": {
        "field_key": "greenery_maintenance_zone",
        "object_ids": ["person_with_machine", "scissor_machine"],
        "interaction_fixture_key": "person_machine_greenery",
        "goal_type": "understand_environment",
    },
    "person_machine_mall": {
        "field_key": "shopping_mall_public_area",
        "object_ids": ["person_with_machine"],
        "interaction_fixture_key": "person_machine_mall",
        "goal_type": "assess_safety",
    },
    "unknown_sculpture_interaction": {
        "field_key": "shopping_mall_public_area",
        "object_ids": ["unknown_sculpture"],
        "interaction_fixture_key": "unknown_sculpture_touch",
        "goal_type": "understand_environment",
    },
    "unknown_no_interaction": {
        "field_key": "shopping_mall_public_area",
        "object_ids": ["unknown_object"],
        "interaction_fixture_key": "unknown_object_no_interaction",
        "goal_type": "understand_environment",
        "external_query_attempted": True,
        "goal_relevant": False,
    },
    "attention_subway_exit": {
        "field_key": "subway_platform",
        "object_ids": ["glowing_screen"],
        "interaction_fixture_key": "",
        "goal_type": "find_exit",
    },
    "attention_mall_exit": {
        "field_key": "shopping_mall_public_area",
        "object_ids": [],
        "interaction_fixture_key": "",
        "goal_type": "find_exit",
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_field_centric_object_role_planning(
    *,
    fixture_key: str = "metal_rack_furniture",
    situation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Field-Centric pipeline:
    Field → Profile → Interaction → Role → Unresolved Memory → Attention
    """
    fixture = PLANNING_FIXTURES.get(fixture_key, PLANNING_FIXTURES["metal_rack_furniture"])
    field_key = fixture.get("field_key", "shopping_mall_public_area")
    object_ids: List[str] = fixture.get("object_ids") or []
    interaction_key = fixture.get("interaction_fixture_key", "")

    field = understand_field(field_key=field_key)
    interaction = build_interaction_graph(fixture_key=interaction_key) if interaction_key else {"has_interaction": False, "interaction_edges": []}
    roles = infer_object_roles(
        field_key=field_key,
        object_ids=object_ids,
        interaction_graph=interaction,
        interaction_fixture_key=interaction_key,
    )
    unresolved = record_unresolved_objects(
        object_ids=object_ids,
        role_candidates=roles.get("object_role_candidates") or [],
        field_understanding=field,
        has_interaction=interaction.get("has_interaction", False),
        goal_relevant=fixture.get("goal_relevant", False),
        external_query_attempted=fixture.get("external_query_attempted", False),
    )
    attention = allocate_attention_from_field(
        field_understanding=field,
        goal_type=fixture.get("goal_type", "understand_environment"),
        field_key=field_key,
    )

    return {
        "planning_only": True,
        "fixture_key": fixture_key,
        "situation": situation or {},
        "field_understanding": field,
        "interaction_graph": interaction,
        "object_role_inference": roles,
        "unresolved_object_memory": unresolved,
        "attention_from_field": attention,
        "field_centric": True,
        "field_before_object_role": True,
        "not_object_first_recognition": True,
        "governance_loop_complete": True,
        "candidate_only": True,
        "not_fact": True,
    }
