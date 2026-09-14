# -*- coding: utf-8 -*-
"""Capability Matching Processor — capability-first need resolution v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.engines.model_routing_engine_v1 import (
    resolve_capability_need,
)
from capabilities.midplatform.model_manager.luna_model_manager_processor_v1 import (
    lookup_capability_providers,
)


def match_capability_need(
    *,
    situation_understanding_candidate: Dict[str, Any],
    agent_plan_candidate: Dict[str, Any],
    decision_validation_candidate: Optional[Dict[str, Any]] = None,
    need_capability: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resolve required capability from L1/L2/L2.5 chain.
    Luna asks 'what capability do I need?' not 'which model?'.
    """
    capability_id = resolve_capability_need(
        situation=situation_understanding_candidate,
        plan=agent_plan_candidate,
        need_capability=need_capability,
    )
    lookup = lookup_capability_providers(capability_id)
    scene = (situation_understanding_candidate.get("scene_profile_candidate") or {}).get("scene_type", "")
    goal = (agent_plan_candidate.get("plan_goal_candidate") or {}).get("goal_type", "")

    return {
        "required_capability": capability_id,
        "capability_label": lookup.get("capability_label"),
        "capability_lookup": lookup,
        "scene_type": scene,
        "plan_goal": goal,
        "validation_status": (decision_validation_candidate or {}).get("validation_status_candidate"),
        "capability_first": True,
        "candidate_only": True,
        "not_fact": True,
    }
