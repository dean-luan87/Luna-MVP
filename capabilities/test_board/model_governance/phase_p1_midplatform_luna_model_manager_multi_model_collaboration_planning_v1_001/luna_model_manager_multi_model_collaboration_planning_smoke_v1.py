# -*- coding: utf-8 -*-
"""Luna Model Manager Multi-Model Collaboration — planning smoke fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.luna_model_manager_collaboration_processor_v1 import (
    run_collaboration_planning,
    run_model_conflict_planning,
    run_resource_degradation_planning,
    run_shopfront_pipeline_planning,
    run_unknown_scene_parallel_planning,
)
from capabilities.midplatform.model_manager.luna_model_manager_collaboration_types_v1 import (
    FINAL_BLOCKED,
    FINAL_GO,
    SMOKE_CASE_IDS,
)


def smoke_case_a_shopfront_pipeline() -> Dict[str, Any]:
    """Case A: identify_place → pipeline plan → fusion_candidate."""
    case_id = "case_a_shopfront_pipeline_collaboration"
    result = run_shopfront_pipeline_planning(goal_type="identify_place")
    plan = result.get("collaboration_plan") or {}
    fusion = result.get("fusion_candidate") or {}
    passed = (
        plan.get("collaboration_mode") == "pipeline"
        and plan.get("collaboration_plan_candidate") is True
        and result.get("has_three_distinct_roles") is True
        and fusion.get("fusion_candidate") is True
        and fusion.get("not_answer_fusion") is True
        and result.get("not_competition") is True
        and result.get("not_executed") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_b_unknown_scene_parallel() -> Dict[str, Any]:
    """Case B: unknown_scene → parallel evidence collection plan."""
    case_id = "case_b_unknown_scene_parallel_evidence"
    result = run_unknown_scene_parallel_planning()
    plan = result.get("collaboration_plan") or {}
    passed = (
        plan.get("collaboration_mode") == "parallel_evidence"
        and result.get("evidence_collection_plan") is True
        and plan.get("produces_answers") is False
        and result.get("includes_qwen_and_internvl") is True
        and result.get("not_voting") is True
        and plan.get("collaboration_plan_candidate") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_c_model_conflict() -> Dict[str, Any]:
    """Case C: model conflict → validation, not score voting."""
    case_id = "case_c_model_conflict_validation"
    result = run_model_conflict_planning()
    passed = (
        result.get("conflict_detected") is True
        and result.get("not_score_voting") is True
        and result.get("not_auto_resolved") is True
        and result.get("validation_requests_more_evidence") is True
        and result.get("no_fact_admission") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def smoke_case_d_resource_degradation() -> Dict[str, Any]:
    """Case D: GPU insufficient → explicit collaboration degradation."""
    case_id = "case_d_resource_collaboration_degradation"
    result = run_resource_degradation_planning()
    passed = (
        result.get("original_had_internvl") is True
        and result.get("degraded_to_qwen_only") is True
        and result.get("not_silent_degradation") is True
        and result.get("collaboration_degradation_candidate") is True
    )
    return {"case_id": case_id, "passed": passed, "result": result}


def run_smoke_cases() -> Dict[str, Any]:
    runners = [
        smoke_case_a_shopfront_pipeline,
        smoke_case_b_unknown_scene_parallel,
        smoke_case_c_model_conflict,
        smoke_case_d_resource_degradation,
    ]
    cases = [fn() for fn in runners]
    failed = [c["case_id"] for c in cases if not c.get("passed")]
    return {
        "phase_id": "Phase-P1-Midplatform-Luna-Model-Manager-Multi-Model-Collaboration-Planning-v1-001",
        "planning_only": True,
        "smoke_case_ids": list(SMOKE_CASE_IDS),
        "smoke_cases": cases,
        "smoke_passed": sum(1 for c in cases if c.get("passed")),
        "smoke_case_count": len(cases),
        "failed_checks": failed,
        "collaboration_not_competition": True,
        "final_decision": FINAL_GO if not failed else FINAL_BLOCKED,
    }
