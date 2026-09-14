# -*- coding: utf-8 -*-
"""Qwen-VL Provider DryRun Adapter — full Model Manager closed loop v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.engines.model_evaluation_engine_v1 import (
    evaluate_model_performance,
)
from capabilities.midplatform.model_manager.model_manager_dryrun.luna_model_manager_dryrun_adapter_v1 import (
    run_model_manager_dryrun,
)
from capabilities.midplatform.model_manager.model_manager_dryrun.model_selection_processor_v1 import (
    build_fallback_plan_candidate,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.dryrun.qwen_vl_evidence_normalizer_v1 import (
    detect_unsupported_claim,
    normalize_qwen_evidence_candidate,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.dryrun.qwen_vl_model_usage_metrics_v1 import (
    get_qwen_model_usage_metrics,
)
from capabilities.midplatform.model_manager.providers.qwen_vl.dryrun.qwen_vl_routing_validation_v1 import (
    validate_model_manager_no_goal_ownership,
    validate_no_silent_model_switch,
    validate_provider_request_boundary,
    validate_routing_candidate,
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
    POLICY_REF,
)

DRYRUN_POLICY_REF = "qwen_vl_provider_dryrun_policy_v1"
FINAL_GO = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_MODEL_MANAGER_QWENVL_REAL_PROVIDER_INTEGRATION_DRYRUN_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_qwen_vl_provider_dryrun(
    job_envelope: Dict[str, Any],
    *,
    case_id: str = "dryrun",
    mock_scenario: Optional[str] = None,
    simulate_timeout: bool = False,
    model_id: str = MODEL_ID,
    score_profile: Optional[str] = None,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    plan_override: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Full closed loop:
    Registry → Lifecycle → Capability → Routing → Provider → Evidence → Validation → Evaluation.
    """
    dryrun_id = _uid("qvd")
    metrics = get_qwen_model_usage_metrics()

    mm_result = run_model_manager_dryrun(
        job_envelope,
        user_goal_candidate=user_goal_candidate,
        plan_override=plan_override,
        score_profile=score_profile,
    )

    situation = mm_result.get("situation_understanding_candidate") or {}
    plan = mm_result.get("agent_plan_candidate") or {}
    validation = mm_result.get("decision_validation_candidate") or {}
    capability_match = mm_result.get("capability_match_candidate") or {}
    routing = mm_result.get("provider_selection_candidate") or {}

    model_record = load_qwen_model_from_registry(model_id)
    selected_id = routing.get("selected_model_id") or routing.get("selected_tool_id")
    qwen_selected = selected_id == model_id

    routing_validation = validate_routing_candidate(
        capability_match=capability_match,
        routing_selection=routing,
        model_record=model_record,
    )
    goal_ownership = validate_model_manager_no_goal_ownership(plan=plan, routing_selection=routing)

    provider_result = None
    provider_review = None
    normalized_evidence = None
    fallback_plan = None
    silent_switch_check = None
    request_boundary = None

    if qwen_selected:
        metrics.record_selected(case_id=case_id, latency_ms=50.0)
        provider_request = build_qwen_vl_provider_request(
            situation_understanding_candidate=situation,
            agent_plan_candidate=plan,
            decision_validation_candidate=validation,
            model_record=model_record,
        )
        request_boundary = validate_provider_request_boundary(provider_request)

        provider_result = invoke_qwen_vl_provider(
            provider_request=provider_request,
            model_record=model_record,
            mock_scenario=mock_scenario,
            simulate_timeout=simulate_timeout,
        )

        parsed = (provider_result or {}).get("parsed_response") or {}
        if parsed.get("parse_status") == "ok":
            normalized_evidence = normalize_qwen_evidence_candidate(
                parsed_response=parsed,
                situation_candidate=situation,
                plan_candidate=plan,
                raw_envelope={"raw_response_ref": provider_result.get("raw_response_ref")},
            )
            if detect_unsupported_claim(normalized_evidence):
                provider_result["has_unsupported_claim"] = True
                provider_result["evidence_candidate"] = None
            elif normalized_evidence:
                provider_result["evidence_candidate"] = normalized_evidence

        provider_review = review_qwen_provider_evidence(
            provider_result=provider_result or {},
            routing_result=routing,
            plan=plan,
            situation=situation,
        )
        metrics.record_validation(case_id=case_id, status=provider_review.get("validation_status", "noop"))

        if provider_review.get("fallback_required"):
            fallback_plan = build_fallback_plan_candidate(
                capability_id=capability_match.get("required_capability", ""),
                original_plan=plan,
                missing={
                    "missing_id": "provider_error",
                    "provider_error_candidate": True,
                },
            )
            silent_switch_check = validate_no_silent_model_switch(
                provider_result=provider_result or {},
                fallback_plan=fallback_plan,
            )
    else:
        metrics.record_noop(case_id=case_id, reason=routing.get("routing_reason", "not_selected"))
        provider_review = {
            "validation_status": "noop",
            "qwen_noop": True,
            "not_selected_reason": routing.get("routing_reason", "capability_mismatch"),
            "selected_plan_unchanged": True,
            "candidate_only": True,
            "not_fact": True,
        }

    evaluation_record = None
    if qwen_selected or metrics.noop_count > 0:
        evaluation_record = evaluate_model_performance(
            model_id=model_id,
            scene_type=(situation.get("scene_profile_candidate") or {}).get("scene_type", ""),
            performance_metrics=metrics.to_evaluation_metrics(),
            routing_result=routing,
        )

    return {
        "dryrun_id": dryrun_id,
        "case_id": case_id,
        "chain": [
            "model_registry",
            "lifecycle_state",
            "capability_match",
            "routing_candidate",
            "qwen_vl_provider",
            "evidence_candidate",
            "validation",
            "evaluation_record",
        ],
        "model_record": model_record,
        "model_manager_result": mm_result,
        "capability_match": capability_match,
        "routing_selection": routing,
        "provider_selected": qwen_selected,
        "provider_selected_id": selected_id if qwen_selected else None,
        "provider_result": provider_result,
        "normalized_evidence": normalized_evidence,
        "provider_validation_review": provider_review,
        "fallback_plan_candidate": fallback_plan,
        "model_usage_metrics": metrics.to_evaluation_metrics(),
        "model_evaluation_record": evaluation_record,
        "routing_validation": routing_validation,
        "request_boundary_validation": request_boundary,
        "goal_ownership_validation": goal_ownership,
        "silent_switch_validation": silent_switch_check,
        "registry_owned": True,
        "no_silent_model_switch": (silent_switch_check or {}).get("passed", True),
        "does_not_affect_current_decision": True,
        "no_auto_execution": True,
        "no_fact_write": True,
        "dryrun_only": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, DRYRUN_POLICY_REF],
    }
