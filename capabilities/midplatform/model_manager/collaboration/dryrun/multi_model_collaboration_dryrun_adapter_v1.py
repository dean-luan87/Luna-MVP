# -*- coding: utf-8 -*-
"""Multi-Model Collaboration DryRun Adapter — full Model OS loop v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.collaboration.dryrun.collaboration_conflict_dryrun_processor_v1 import (
    build_challenge_dryrun,
    build_semantic_conflict_dryrun,
)
from capabilities.midplatform.model_manager.collaboration.dryrun.collaboration_degradation_processor_v1 import (
    run_resource_degradation_dryrun,
)
from capabilities.midplatform.model_manager.collaboration.dryrun.collaboration_execution_planner_v1 import (
    build_tool_os_handoff_candidate,
    plan_parallel_execution,
    plan_pipeline_execution,
)
from capabilities.midplatform.model_manager.collaboration.dryrun.evidence_fusion_dryrun_processor_v1 import (
    build_parallel_fusion_dryrun,
    build_pipeline_fusion_dryrun,
    build_validation_review_for_fusion,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_MULTI_MODEL_COLLABORATION_DRYRUN_BLOCKED"
DRYRUN_POLICY_REF = "collaboration/dryrun/multi_model_collaboration_dryrun_policy_v1.json"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _l1_situation_shopfront() -> Dict[str, Any]:
    return {
        "situation_id": _uid("sit"),
        "scene_profile_candidate": {"scene_type": "shopfront_sign", "confidence": 0.7},
        "missing_information_candidates": [{"info_type": "place_identity"}],
        "candidate_only": True,
        "not_fact": True,
    }


def _l1_situation_unknown() -> Dict[str, Any]:
    return {
        "situation_id": _uid("sit"),
        "scene_profile_candidate": {"scene_type": "unknown_environment", "confidence": 0.4},
        "missing_information_candidates": [{"info_type": "scene_identity"}],
        "candidate_only": True,
        "not_fact": True,
    }


def _l2_plan_identify_place() -> Dict[str, Any]:
    return {
        "plan_id": _uid("plan"),
        "plan_goal_candidate": {"goal_type": "identify_place", "description": "需要确认店名"},
        "tool_plan_candidates": [{"capability_type": "precise_ocr", "priority": 1}],
        "candidate_only": True,
        "not_fact": True,
    }


def _l2_plan_understand_scene() -> Dict[str, Any]:
    return {
        "plan_id": _uid("plan"),
        "plan_goal_candidate": {"goal_type": "understand_scene", "description": "理解未知环境"},
        "candidate_only": True,
        "not_fact": True,
    }


def run_pipeline_collaboration_dryrun() -> Dict[str, Any]:
    """Case A: shopfront_sign → pipeline slots → fusion → validation → handoff."""
    situation = _l1_situation_shopfront()
    plan = _l2_plan_identify_place()
    execution_plan = plan_pipeline_execution(goal_type="identify_place", scene_type="shopfront_sign")
    fusion = build_pipeline_fusion_dryrun(execution_plan=execution_plan)
    validation = build_validation_review_for_fusion(fusion)
    handoff = build_tool_os_handoff_candidate(
        filled_slots=execution_plan.get("filled_slots") or [],
        collaboration_type="pipeline",
    )

    return {
        "case": "case_a_pipeline_collaboration_shopfront",
        "l1_situation": situation,
        "l2_plan": plan,
        "collaboration_plan": execution_plan,
        "evidence_fusion": fusion,
        "validation_review": validation,
        "tool_os_handoff": handoff,
        "collaboration_type": "pipeline",
        "sequence": execution_plan.get("sequence"),
        "uses_collaboration_slots": len(execution_plan.get("collaboration_slots") or []) >= 3,
        "direct_vlm_skipped": execution_plan.get("direct_vlm_skipped") is True,
        "ocr_is_primary": execution_plan.get("ocr_is_primary") is True,
        "vlm_context_only": execution_plan.get("vlm_is_context_only") is True,
        "fusion_candidate": fusion.get("fusion_candidate") is True,
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_parallel_evidence_dryrun() -> Dict[str, Any]:
    """Case B: unknown_environment → parallel evidence set."""
    situation = _l1_situation_unknown()
    plan = _l2_plan_understand_scene()
    execution_plan = plan_parallel_execution()
    fusion = build_parallel_fusion_dryrun(execution_plan=execution_plan)
    validation = build_validation_review_for_fusion(fusion)

    return {
        "case": "case_b_parallel_evidence_unknown_scene",
        "l1_situation": situation,
        "l2_plan": plan,
        "collaboration_plan": execution_plan,
        "evidence_fusion": fusion,
        "validation_review": validation,
        "evidence_set": fusion.get("evidence_set"),
        "produces_single_answer": fusion.get("produces_single_answer") is False,
        "not_merged_hypothesis": fusion.get("not_merged_hypothesis") is True,
        "evidence_set_count": fusion.get("evidence_set_count", 0) >= 3,
        "not_voting": fusion.get("not_voting") is True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_challenge_mode_dryrun() -> Dict[str, Any]:
    """Case C: OCR plan + low confidence → challenge, plan unchanged."""
    plan = _l2_plan_identify_place()
    result = build_challenge_dryrun(selected_plan_capability="precise_ocr", validation_confidence=0.35)
    return {
        "case": "case_c_challenge_mode_teacher",
        "l2_plan": plan,
        **result,
        "selected_plan_still_ocr": (result.get("validation_review") or {}).get("selected_plan") == "precise_ocr",
        "candidate_only": True,
        "not_fact": True,
    }


def run_evidence_conflict_dryrun() -> Dict[str, Any]:
    """Case D: semantic conflict → validation, no confidence voting."""
    result = build_semantic_conflict_dryrun()
    return {
        "case": "case_d_evidence_conflict_semantic",
        **result,
        "conflict_type_semantic": (result.get("model_conflict_candidate") or {}).get("conflict_type") == "semantic_conflict",
        "resolution_request_more_evidence": (result.get("model_conflict_candidate") or {}).get("resolution") == "request_more_evidence",
        "candidate_only": True,
        "not_fact": True,
    }


def run_collaboration_degradation_dryrun() -> Dict[str, Any]:
    """Case E: GPU unavailable → explicit degradation."""
    result = run_resource_degradation_dryrun()
    return {
        "case": "case_e_resource_collaboration_degradation",
        **result,
        "collaboration_degradation_candidate": (result.get("collaboration_degradation") or {}).get("collaboration_degradation_candidate") is True,
        "candidate_only": True,
        "not_fact": True,
    }


def run_multi_model_collaboration_dryrun(
    *,
    case_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Full collaboration dryrun orchestrator."""
    dispatch = {
        "case_a_pipeline_collaboration_shopfront": run_pipeline_collaboration_dryrun,
        "case_b_parallel_evidence_unknown_scene": run_parallel_evidence_dryrun,
        "case_c_challenge_mode_teacher": run_challenge_mode_dryrun,
        "case_d_evidence_conflict_semantic": run_evidence_conflict_dryrun,
        "case_e_resource_collaboration_degradation": run_collaboration_degradation_dryrun,
    }
    if case_id and case_id in dispatch:
        return dispatch[case_id]()

    return {
        "phase": "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-DryRun-v1-001",
        "model_os_collaboration_loop": True,
        "dryrun_only": True,
        "candidate_only": True,
        "not_fact": True,
    }
