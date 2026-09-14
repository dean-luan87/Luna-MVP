# -*- coding: utf-8 -*-
"""Qwen-VL Provider — request builder v1 (Model Manager owned)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.luna_model_manager_qwen_vl_types_v1 import (
    FORBIDDEN_OUTPUT_TYPES,
    MODEL_ID,
)


def build_qwen_vl_provider_request(
    *,
    situation_understanding_candidate: Dict[str, Any],
    agent_plan_candidate: Dict[str, Any],
    decision_validation_candidate: Optional[Dict[str, Any]] = None,
    model_record: Optional[Dict[str, Any]] = None,
    image_reference: Optional[str] = None,
) -> Dict[str, Any]:
    """Build provider request from L1/L2/L2.5 + Model Manager routing context."""
    scene = (situation_understanding_candidate.get("scene_profile_candidate") or {}).get("scene_type", "")
    goal = (agent_plan_candidate.get("plan_goal_candidate") or {}).get("goal_type", "")
    missing = [
        m.get("info_type", "")
        for m in situation_understanding_candidate.get("missing_information_candidates", [])
    ]

    return {
        "request_type": "model_manager_provider_request",
        "model_id": (model_record or {}).get("model_id", MODEL_ID),
        "provider_type": "external_teacher",
        "image_reference": image_reference,
        "situation_candidate": situation_understanding_candidate,
        "plan_candidate": agent_plan_candidate,
        "validation_context": decision_validation_candidate,
        "scene_type": scene,
        "plan_goal": goal,
        "missing_information": missing,
        "forbidden_output_types": list(FORBIDDEN_OUTPUT_TYPES),
        "candidate_only": True,
        "not_fact": True,
        "managed_by": "model_manager",
    }
