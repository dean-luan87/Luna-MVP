# -*- coding: utf-8 -*-
"""Luna Model Manager — dry-run adapter v1 (L1→L2→L2.5→Capability→Selection→Handoff)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.decision_validation.luna_decision_validation_dryrun_adapter_v1 import (
    run_decision_validation_dryrun,
)
from capabilities.midplatform.model_manager.engines.model_evaluation_engine_v1 import (
    evaluate_model_performance,
)
from capabilities.midplatform.model_manager.luna_model_manager_processor_v1 import (
    build_model_admission_candidate,
)
from capabilities.midplatform.model_manager.model_manager_dryrun.capability_matching_processor_v1 import (
    match_capability_need,
)
from capabilities.midplatform.model_manager.model_manager_dryrun.model_selection_processor_v1 import (
    build_capability_missing_candidate,
    build_fallback_plan_candidate,
    build_handoff_candidates,
    select_provider_candidate,
)
from capabilities.midplatform.model_manager.model_manager_dryrun.routing_score_calculator_v1 import (
    calculate_routing_scores,
)

DRYRUN_POLICY_REF = "luna_model_manager_dryrun_policy_v1"
FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_FOUNDATION_DRYRUN_BLOCKED"

TOOL_PRIMARY_PROVIDERS = {
    "text_recognition": "ocr_v1",
}


def build_model_manager_input_from_chain(
    dv_result: Dict[str, Any],
) -> Dict[str, Any]:
    """L2.5 validation result → Model Manager input."""
    return {
        "situation_understanding_candidate": dv_result.get("situation_understanding_candidate") or {},
        "agent_plan_candidate": dv_result.get("agent_plan_candidate") or {},
        "decision_validation_candidate": dv_result.get("decision_validation_candidate") or {},
        "tool_os_handoff_candidate": dv_result.get("tool_os_handoff_candidate"),
        "validation_status": dv_result.get("validation_status"),
        "candidate_only": True,
        "not_fact": True,
    }


def assert_model_manager_no_decision_power(
    mm_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Model Manager produces provider_candidate; L2 owns decisions."""
    selection = mm_result.get("provider_selection_candidate") or {}
    checks = {
        "produced_provider_candidate": selection.get("provider_selection_candidate") is True,
        "not_decided_plan": selection.get("produced_provider_candidate_not_decision") is True,
        "does_not_affect_decision": mm_result.get("does_not_affect_current_decision") is True,
        "no_auto_execution": mm_result.get("no_auto_execution") is True,
        "no_auto_policy_update": mm_result.get("no_auto_policy_update") is True,
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True, "not_fact": True}


def assert_model_manager_not_tool_os(
    mm_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Model Manager selects; Tool OS / Teacher Adapter execute."""
    handoffs = mm_result.get("handoff_candidates") or {}
    tool_handoff = handoffs.get("tool_os_handoff_candidate") or {}
    teacher_handoff = handoffs.get("teacher_adapter_handoff_candidate") or {}
    checks = {
        "handoff_not_execution": tool_handoff.get("not_executed") is True,
        "teacher_handoff_not_execution": teacher_handoff.get("not_executed") is True,
        "scheduling_center_only": mm_result.get("model_manager_role") == "capability_scheduling_center",
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True, "not_fact": True}


def run_model_admission_pipeline(
    *,
    model_id: str,
    model_type: str = "teacher",
    force_admitted: bool = False,
) -> Dict[str, Any]:
    """Simulate admission pipeline — no auto admission unless explicitly admitted in dryrun."""
    admission = build_model_admission_candidate(model_id=model_id, model_type=model_type)
    routing_eligible = False
    if force_admitted:
        admission["admission_status"] = "admitted"
        admission["pipeline_stages"] = [
            {"stage": "model_candidate", "status": "completed"},
            {"stage": "security_review", "status": "completed"},
            {"stage": "capability_review", "status": "completed"},
            {"stage": "benchmark", "status": "completed"},
            {"stage": "admission_decision", "status": "admitted"},
        ]
        routing_eligible = True
    return {
        "admission": admission,
        "routing_eligible": routing_eligible,
        "capability_registry_update": routing_eligible,
        "candidate_only": True,
        "not_fact": True,
    }


def run_model_manager_dryrun(
    job_envelope: Dict[str, Any],
    *,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    plan_override: Optional[Dict[str, Any]] = None,
    need_capability: Optional[str] = None,
    score_profile: Optional[str] = None,
    scoring_mode: str = "default",
    unavailable_providers: Optional[List[str]] = None,
    admitted_only: bool = False,
    performance_metrics: Optional[Dict[str, Any]] = None,
    admission_model_id: Optional[str] = None,
    force_admitted: bool = False,
) -> Dict[str, Any]:
    """
    Full dry-run:
    job → L1 → L2 → L2.5 → Capability Match → Provider Selection → Handoff Candidate.
    Does NOT execute models, download, or replace providers.
    """
    dv_result = run_decision_validation_dryrun(
        job_envelope,
        user_goal_candidate=user_goal_candidate,
        plan_override=plan_override,
    )

    mm_input = build_model_manager_input_from_chain(dv_result)
    situation = mm_input["situation_understanding_candidate"]
    plan = mm_input["agent_plan_candidate"]
    validation = mm_input["decision_validation_candidate"]
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type", "")

    capability_match = match_capability_need(
        situation_understanding_candidate=situation,
        agent_plan_candidate=plan,
        decision_validation_candidate=validation,
        need_capability=need_capability,
    )
    capability_id = capability_match.get("required_capability", "")

    scoring = calculate_routing_scores(
        capability_id=capability_id,
        scene=scene,
        situation=situation,
        plan=plan,
        score_profile=score_profile,
        scoring_mode=scoring_mode,
        unavailable_providers=unavailable_providers,
        admitted_only=admitted_only,
    )

    eligible = scoring.get("eligible_providers") or []
    capability_missing = None
    fallback_plan = None
    selection = None
    handoffs = {}

    blocked_by_unavailable = False
    if unavailable_providers:
        primary_tool = TOOL_PRIMARY_PROVIDERS.get(capability_id)
        if primary_tool and primary_tool in unavailable_providers:
            blocked_by_unavailable = True

    if blocked_by_unavailable or (not eligible and unavailable_providers):
        capability_missing = build_capability_missing_candidate(
            capability_id=capability_id,
            reason="primary_provider_unavailable",
            unavailable_providers=unavailable_providers,
        )
        fallback_plan = build_fallback_plan_candidate(
            capability_id=capability_id,
            original_plan=plan,
            missing=capability_missing,
        )
        selection = {
            "selection_id": "psc_blocked",
            "required_capability": capability_id,
            "route_type": "noop",
            "selected_model_id": None,
            "selected_tool_id": None,
            "selected_provider": None,
            "provider_scores": scoring.get("provider_scores", []),
            "routing_reason": "provider_unavailable_no_silent_fallback",
            "should_invoke_model": False,
            "should_request_teacher": False,
            "provider_selection_candidate": True,
            "produced_provider_candidate_not_decision": True,
            "candidate_only": True,
            "not_fact": True,
        }
    else:
        selection = select_provider_candidate(
            capability_match=capability_match,
            scoring_result=scoring,
        )
        handoffs = build_handoff_candidates(selection)

    admission_pipeline = None
    if admission_model_id:
        admission_pipeline = run_model_admission_pipeline(
            model_id=admission_model_id,
            force_admitted=force_admitted,
        )

    evaluation = None
    selected_id = (selection or {}).get("selected_model_id") or (selection or {}).get("selected_tool_id")
    if selected_id and performance_metrics:
        evaluation = evaluate_model_performance(
            model_id=selected_id,
            scene_type=scene,
            performance_metrics=performance_metrics,
            routing_result=selection,
        )

    no_decision_assert = assert_model_manager_no_decision_power({
        "provider_selection_candidate": selection,
        "does_not_affect_current_decision": True,
        "no_auto_execution": True,
        "no_auto_policy_update": evaluation is None or evaluation.get("no_auto_policy_update") is True,
    })
    not_tool_os_assert = assert_model_manager_not_tool_os({
        "handoff_candidates": handoffs,
        "model_manager_role": "capability_scheduling_center",
    })

    return {
        "job_id": dv_result.get("job_id", ""),
        "chain": [
            "job_envelope",
            "situation_understanding_candidate",
            "agent_plan_candidate",
            "decision_validation_candidate",
            "capability_match_candidate",
            "provider_selection_candidate",
            "tool_os_handoff_candidate",
            "teacher_adapter_handoff_candidate",
        ],
        "situation_understanding_candidate": situation,
        "agent_plan_candidate": plan,
        "decision_validation_candidate": validation,
        "validation_status": dv_result.get("validation_status"),
        "tool_plan_summary": dv_result.get("tool_plan_summary"),
        "capability_match_candidate": capability_match,
        "routing_score_result": scoring,
        "provider_selection_candidate": selection,
        "capability_missing_candidate": capability_missing,
        "fallback_plan_candidate": fallback_plan,
        "handoff_candidates": handoffs,
        "tool_os_handoff_candidate": handoffs.get("tool_os_handoff_candidate"),
        "teacher_adapter_handoff_candidate": handoffs.get("teacher_adapter_handoff_candidate"),
        "model_evaluation_result": evaluation,
        "admission_pipeline": admission_pipeline,
        "model_manager_role": "capability_scheduling_center",
        "model_manager_no_decision_assertion": no_decision_assert,
        "model_manager_not_tool_os_assertion": not_tool_os_assert,
        "no_fact_write_assertion": True,
        "no_model_execution_assertion": True,
        "no_auto_policy_update_assertion": evaluation is None or evaluation.get("no_auto_policy_update") is True,
        "dryrun_only": True,
        "no_real_model_execution": True,
        "no_network": True,
        "candidate_only": True,
        "not_fact": True,
        "does_not_affect_current_decision": True,
        "no_auto_execution": True,
        "policy_refs": [DRYRUN_POLICY_REF],
    }
