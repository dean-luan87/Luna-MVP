# -*- coding: utf-8 -*-
"""Luna Model Manager Qwen-VL — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict, Optional

from capabilities.midplatform.model_manager.lifecycle.model_lifecycle_processor_v1 import (
    deprecate_model,
    reset_sandbox_registry,
    run_full_lifecycle_sandbox,
)
from capabilities.midplatform.model_manager.model_manager_dryrun.luna_model_manager_dryrun_adapter_v1 import (
    run_model_manager_dryrun,
)
from capabilities.midplatform.model_manager.model_manager_dryrun.model_selection_processor_v1 import (
    build_fallback_plan_candidate,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.qwen_vl_request_builder_v1 import (
    build_qwen_vl_provider_request,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.qwen_vl_provider_adapter_v1 import (
    invoke_qwen_vl_provider,
    load_qwen_model_from_registry,
    review_qwen_provider_evidence,
)
from capabilities.midplatform.model_manager.luna_model_manager_qwen_vl_types_v1 import (
    MODEL_ID,
    MODEL_ID_V2,
    POLICY_REF,
)

FROZEN_MODULES = (
    "teacher_adapter_qwen_vl",
    "model_manager_foundation",
    "model_manager_lifecycle",
)


def run_model_manager_qwen_vl_planning(
    job_envelope: Dict[str, Any],
    *,
    mock_scenario: Optional[str] = None,
    simulate_timeout: bool = False,
    model_id: str = MODEL_ID,
    score_profile: Optional[str] = None,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    plan_override: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Full planning chain:
    L1→L2→L2.5→Model Manager→Registry Gate→Qwen Provider→Evidence→Validation.
    """
    mm_result = run_model_manager_dryrun(
        job_envelope,
        user_goal_candidate=user_goal_candidate,
        plan_override=plan_override,
        score_profile=score_profile,
    )

    situation = mm_result.get("situation_understanding_candidate") or {}
    plan = mm_result.get("agent_plan_candidate") or {}
    validation = mm_result.get("decision_validation_candidate") or {}
    routing = mm_result.get("provider_selection_candidate") or {}
    selection = routing

    model_record = load_qwen_model_from_registry(model_id)
    selected_id = selection.get("selected_model_id") or selection.get("selected_tool_id")
    qwen_selected = selected_id == model_id or selection.get("should_request_teacher") is True

    provider_result = None
    provider_review = None
    fallback_plan = None

    if qwen_selected and selected_id == model_id:
        provider_request = build_qwen_vl_provider_request(
            situation_understanding_candidate=situation,
            agent_plan_candidate=plan,
            decision_validation_candidate=validation,
            model_record=model_record,
        )
        provider_result = invoke_qwen_vl_provider(
            provider_request=provider_request,
            model_record=model_record,
            mock_scenario=mock_scenario,
            simulate_timeout=simulate_timeout,
        )
        provider_review = review_qwen_provider_evidence(
            provider_result=provider_result,
            routing_result=selection,
            plan=plan,
            situation=situation,
        )
        if provider_review.get("fallback_required"):
            fallback_plan = build_fallback_plan_candidate(
                capability_id=(mm_result.get("capability_match_candidate") or {}).get("required_capability", ""),
                original_plan=plan,
                missing={
                    "missing_id": "provider_error",
                    "capability_missing_candidate": False,
                    "provider_error_candidate": True,
                },
            )
    elif not qwen_selected:
        provider_review = {
            "validation_status": "noop",
            "not_selected_reason": selection.get("routing_reason", "specialized_tool_preferred"),
            "qwen_noop": True,
            "selected_plan_unchanged": True,
            "candidate_only": True,
            "not_fact": True,
        }

    return {
        "planning_id": f"mmqvp_{model_id}",
        "frozen_prerequisites": list(FROZEN_MODULES),
        "model_manager_result": mm_result,
        "model_record": model_record,
        "registry_owned": True,
        "no_hardcoded_provider_call": True,
        "capability_match": mm_result.get("capability_match_candidate"),
        "routing_selection": selection,
        "qwen_selected": qwen_selected and selected_id == model_id,
        "provider_result": provider_result,
        "provider_validation_review": provider_review,
        "fallback_plan_candidate": fallback_plan,
        "does_not_affect_current_decision": True,
        "no_auto_execution": True,
        "no_fact_write": True,
        "planning_only": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF],
    }


def run_qwen_lifecycle_version_switch_planning() -> Dict[str, Any]:
    """Case E: qwen_vl v1 active → v2 candidate → eval → active → v1 deprecated."""
    reset_sandbox_registry()
    v1 = run_full_lifecycle_sandbox(
        model_id=MODEL_ID,
        model_label="Qwen-VL v1",
        model_type="vision_language_model",
        capabilities=["scene_understanding", "visual_reasoning", "unknown_scene_reasoning"],
        capability_id="unknown_scene_reasoning",
        reliability=0.85,
        latency_ms=1200,
        cost_tier="medium",
        owner="external_teacher",
    )
    v2 = run_full_lifecycle_sandbox(
        model_id=MODEL_ID_V2,
        model_label="Qwen-VL v2",
        model_type="vision_language_model",
        capabilities=["scene_understanding", "visual_reasoning", "unknown_scene_reasoning"],
        capability_id="unknown_scene_reasoning",
        reliability=0.88,
        latency_ms=1100,
        cost_tier="medium",
        owner="external_teacher",
    )
    deprecation = deprecate_model(
        model_id=MODEL_ID,
        replacement_model_id=MODEL_ID_V2,
        reason="version_upgrade",
    )
    return {
        "v1_lifecycle": v1,
        "v2_lifecycle": v2,
        "v1_deprecation": deprecation,
        "v2_active": (v2.get("model_record") or {}).get("lifecycle_state") == "active",
        "v1_deprecated": (deprecation.get("model_record") or {}).get("lifecycle_state") == "deprecated",
        "upper_layer_unchanged": True,
        "candidate_only": True,
        "not_fact": True,
    }
