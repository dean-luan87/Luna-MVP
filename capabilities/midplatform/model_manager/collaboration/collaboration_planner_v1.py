# -*- coding: utf-8 -*-
"""Collaboration Planner — multi-capability orchestration v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

PIPELINE_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "identify_place": {
        "collaboration_mode": "pipeline",
        "capability_requirements": [
            "text_detection",
            "precise_ocr",
            "visual_context_reasoning",
        ],
        "provider_sequence": [
            {
                "step": 1,
                "capability_id": "object_detection",
                "provider_role": "text_detector",
                "model_id": "detection_v1",
                "execution_mode": "tool_os",
                "depends_on": [],
            },
            {
                "step": 2,
                "capability_id": "precise_ocr",
                "provider_role": "ocr_engine",
                "model_id": "ocr_v1",
                "execution_mode": "tool_os",
                "depends_on": [1],
            },
            {
                "step": 3,
                "capability_id": "unknown_scene_reasoning",
                "provider_role": "vlm_context_reasoner",
                "model_id": "qwen_vl",
                "execution_mode": "external_api",
                "depends_on": [2],
            },
        ],
    },
    "unknown_scene": {
        "collaboration_mode": "parallel_evidence",
        "capability_requirements": ["unknown_scene_reasoning", "spatial_structure"],
        "parallel_strategy": {
            "providers": [
                {"model_id": "qwen_vl", "provider_role": "scene_hypothesis", "execution_mode": "external_api"},
                {"model_id": "internvl2_5", "provider_role": "scene_hypothesis", "execution_mode": "local_runtime"},
                {"model_id": "detection_v1", "provider_role": "grounding_structure", "execution_mode": "tool_os"},
            ],
            "evidence_collection_plan": True,
            "not_voting": True,
        },
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def plan_pipeline_collaboration(
    *,
    goal_type: str,
    capability_requirements: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Case A: Pipeline — Text Detection + OCR + VLM Context."""
    template = PIPELINE_TEMPLATES.get(goal_type, PIPELINE_TEMPLATES["identify_place"])
    caps = capability_requirements or template["capability_requirements"]
    sequence = template["provider_sequence"]

    return {
        "plan_id": _uid("cp"),
        "goal_type": goal_type,
        "collaboration_mode": "pipeline",
        "capability_requirements": caps,
        "provider_sequence": sequence,
        "provider_count": len(sequence),
        "distinct_roles": len({s["provider_role"] for s in sequence}),
        "not_competition": True,
        "not_voting": True,
        "collaboration_plan_candidate": True,
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }


def plan_parallel_evidence_collaboration(
    *,
    goal_type: str = "unknown_scene",
    providers: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Case B: Parallel evidence collection — not answers, not voting."""
    template = PIPELINE_TEMPLATES.get(goal_type, PIPELINE_TEMPLATES["unknown_scene"])
    parallel = template.get("parallel_strategy", {})
    if providers:
        parallel = {**parallel, "providers": providers}

    return {
        "plan_id": _uid("pe"),
        "goal_type": goal_type,
        "collaboration_mode": "parallel_evidence",
        "capability_requirements": template.get("capability_requirements", []),
        "parallel_strategy": parallel,
        "evidence_collection_plan": True,
        "produces_answers": False,
        "not_voting": True,
        "not_competition": True,
        "collaboration_plan_candidate": True,
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }


def plan_challenge_collaboration(
    *,
    original_plan_capability: str,
    challenge_reason: str,
    challenger_model_id: str = "qwen_vl",
) -> Dict[str, Any]:
    """Challenge Mode — alternative explanation, does NOT override L2 plan."""
    return {
        "plan_id": _uid("ch"),
        "collaboration_mode": "challenge",
        "original_plan_capability": original_plan_capability,
        "challenge_reason": challenge_reason,
        "challenger": {
            "model_id": challenger_model_id,
            "provider_role": "teacher_challenger",
            "execution_mode": "external_api",
        },
        "override_plan": False,
        "challenge_does_not_override_plan": True,
        "collaboration_plan_candidate": True,
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }


def plan_collaboration_degradation(
    *,
    original_plan: Dict[str, Any],
    degraded_providers: List[Dict[str, Any]],
    reason: str,
    resource_constraint: str,
) -> Dict[str, Any]:
    """Case D: Resource limit — explicit degradation, not silent."""
    return {
        "degradation_id": _uid("cdg"),
        "original_plan_id": original_plan.get("plan_id"),
        "original_providers": original_plan.get("parallel_strategy", {}).get("providers")
            or original_plan.get("provider_sequence"),
        "degraded_providers": degraded_providers,
        "degradation_reason": reason,
        "resource_constraint": resource_constraint,
        "collaboration_degradation_candidate": True,
        "not_silent_degradation": True,
        "requires_validation_ack": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_collaboration_plan_for_goal(
    *,
    goal_type: str,
    scene_type: str = "unknown_scene",
    uncertainty_high: bool = False,
) -> Dict[str, Any]:
    """Dispatch collaboration plan by goal — planning only."""
    if goal_type in ("identify_place", "read_text") or scene_type == "shopfront_sign":
        plan = plan_pipeline_collaboration(goal_type="identify_place")
        return {"primary_plan": plan, "collaboration_mode": "pipeline"}
    if scene_type == "unknown_scene" or goal_type == "understand_environment":
        plan = plan_parallel_evidence_collaboration(goal_type="unknown_scene")
        result: Dict[str, Any] = {"primary_plan": plan, "collaboration_mode": "parallel_evidence"}
        if uncertainty_high:
            result["challenge_plan"] = plan_challenge_collaboration(
                original_plan_capability="precise_ocr",
                challenge_reason="uncertainty_high_after_validation",
            )
        return result
    return {"primary_plan": plan_pipeline_collaboration(goal_type=goal_type), "collaboration_mode": "pipeline"}
