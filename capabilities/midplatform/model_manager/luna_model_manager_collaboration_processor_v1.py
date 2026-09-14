# -*- coding: utf-8 -*-
"""Luna Model Manager Collaboration — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.collaboration.collaboration_planner_v1 import (
    build_collaboration_plan_for_goal,
    plan_collaboration_degradation,
    plan_parallel_evidence_collaboration,
    plan_pipeline_collaboration,
)
from capabilities.midplatform.model_manager.collaboration.evidence_fusion_processor_v1 import (
    build_fusion_candidate,
)
from capabilities.midplatform.model_manager.collaboration.model_conflict_processor_v1 import (
    build_conflict_validation_review,
    build_model_conflict_candidate,
)
from capabilities.midplatform.model_manager.luna_model_manager_collaboration_types_v1 import (
    COLLABORATION_MODES,
    COLLABORATION_NOT,
    POLICY_REF,
)


def run_collaboration_planning(
    *,
    scenario: str = "shopfront_pipeline",
    goal_type: str = "identify_place",
    scene_type: str = "shopfront_sign",
) -> Dict[str, Any]:
    """Main collaboration planning orchestrator — planning only."""
    if scenario == "shopfront_pipeline":
        return run_shopfront_pipeline_planning(goal_type=goal_type)
    if scenario == "unknown_scene_parallel":
        return run_unknown_scene_parallel_planning()
    if scenario == "model_conflict":
        return run_model_conflict_planning()
    if scenario == "resource_degradation":
        return run_resource_degradation_planning()
    return run_shopfront_pipeline_planning(goal_type=goal_type, scene_type=scene_type)


def run_shopfront_pipeline_planning(
    *,
    goal_type: str = "identify_place",
    scene_type: str = "shopfront_sign",
) -> Dict[str, Any]:
    """Case A: identify_place → pipeline collaboration → fusion_candidate."""
    plan = plan_pipeline_collaboration(goal_type=goal_type)
    fusion = build_fusion_candidate(collaboration_plan=plan)
    roles = [s.get("provider_role") for s in plan.get("provider_sequence") or []]

    return {
        "scenario": "shopfront_pipeline",
        "goal_type": goal_type,
        "scene_type": scene_type,
        "collaboration_plan": plan,
        "fusion_candidate": fusion,
        "collaboration_mode": "pipeline",
        "has_three_distinct_roles": len(set(roles)) >= 3,
        "not_competition": plan.get("not_competition") is True,
        "not_voting": plan.get("not_voting") is True,
        "not_executed": plan.get("not_executed") is True,
        "collaboration_not_competition": True,
        "policy_ref": POLICY_REF,
        "candidate_only": True,
        "not_fact": True,
    }


def run_unknown_scene_parallel_planning() -> Dict[str, Any]:
    """Case B: unknown_scene → parallel evidence collection plan."""
    plan = plan_parallel_evidence_collaboration(goal_type="unknown_scene")
    fusion = build_fusion_candidate(collaboration_plan=plan)
    parallel = plan.get("parallel_strategy") or {}

    return {
        "scenario": "unknown_scene_parallel",
        "collaboration_plan": plan,
        "fusion_candidate": fusion,
        "collaboration_mode": "parallel_evidence",
        "evidence_collection_plan": parallel.get("evidence_collection_plan") is True,
        "produces_answers": plan.get("produces_answers") is False,
        "provider_count": len(parallel.get("providers") or []),
        "includes_qwen_and_internvl": {
            p.get("model_id") for p in parallel.get("providers") or []
        }.issuperset({"qwen_vl", "internvl2_5"}),
        "not_voting": True,
        "not_competition": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_model_conflict_planning() -> Dict[str, Any]:
    """Case C: Qwen airport vs InternVL mall → conflict → validation."""
    hypotheses = [
        {"model_id": "qwen_vl", "hypothesis_candidate": "airport_terminal", "evidence_type": "scene_hypothesis_candidate"},
        {"model_id": "internvl2_5", "hypothesis_candidate": "shopping_mall", "evidence_type": "scene_hypothesis_candidate"},
    ]
    conflict = build_model_conflict_candidate(provider_hypotheses=hypotheses)
    validation = build_conflict_validation_review(conflict)

    return {
        "scenario": "model_conflict",
        "model_conflict": conflict,
        "validation_review": validation,
        "conflict_detected": conflict.get("conflict_count", 0) > 0,
        "not_score_voting": conflict.get("not_score_voting") is True,
        "not_auto_resolved": conflict.get("not_auto_resolved") is True,
        "validation_requests_more_evidence": validation.get("validation_status") == "request_more_evidence",
        "no_fact_admission": conflict.get("no_fact_admission") is True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_resource_degradation_planning() -> Dict[str, Any]:
    """Case D: GPU insufficient → InternVL+Qwen plan degrades to Qwen only."""
    original = plan_parallel_evidence_collaboration(goal_type="unknown_scene")
    degraded = plan_collaboration_degradation(
        original_plan=original,
        degraded_providers=[{"model_id": "qwen_vl", "provider_role": "scene_hypothesis", "execution_mode": "external_api"}],
        reason="gpu_memory_insufficient",
        resource_constraint="internvl2_5_unavailable",
    )

    return {
        "scenario": "resource_degradation",
        "original_plan": original,
        "collaboration_degradation": degraded,
        "original_had_internvl": any(
            p.get("model_id") == "internvl2_5"
            for p in (original.get("parallel_strategy") or {}).get("providers") or []
        ),
        "degraded_to_qwen_only": len(degraded.get("degraded_providers") or []) == 1
            and (degraded.get("degraded_providers") or [{}])[0].get("model_id") == "qwen_vl",
        "not_silent_degradation": degraded.get("not_silent_degradation") is True,
        "collaboration_degradation_candidate": degraded.get("collaboration_degradation_candidate") is True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_multi_model_collaboration_planning_summary() -> Dict[str, Any]:
    """Full planning summary for review."""
    return {
        "phase_ref": "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001",
        "planning_only": True,
        "collaboration_modes": list(COLLABORATION_MODES),
        "collaboration_not": list(COLLABORATION_NOT),
        "collaboration_not_competition": True,
        "registry_distinct_from_collaboration": True,
        "module_refs": [
            "collaboration/collaboration_planner_v1.py",
            "collaboration/evidence_fusion_processor_v1.py",
            "collaboration/model_conflict_processor_v1.py",
        ],
        "candidate_only": True,
        "not_fact": True,
    }
