# -*- coding: utf-8 -*-
"""Teacher Performance Processor — evaluate teacher value after validation v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.teacher_evaluation.luna_teacher_performance_types_v1 import (
    POLICY_REF,
    PROVIDER_ID,
    SCENE_USAGE_HINTS,
)
from capabilities.midplatform.teacher_evaluation.teacher_performance_metrics_v1 import (
    TeacherPerformanceMetrics,
    get_performance_metrics,
)

HIGH_VALUE_OUTCOMES = ("high_value_evidence", "accepted_evidence")
NEGATIVE_OUTCOMES = ("policy_rejection", "unsupported_claim", "scene_conflict")


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _scene(integration_result: Dict[str, Any]) -> str:
    sit = integration_result.get("situation_understanding_candidate") or {}
    return (sit.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _conflict_types(review: Dict[str, Any]) -> List[str]:
    return [c.get("conflict_type", "") for c in (review.get("conflict_candidates") or [])]


def classify_evaluation_outcome(
    *,
    scene: str,
    admission_status: str,
    validation_status: str,
    conflict_types: List[str],
    should_request: bool,
) -> str:
    if admission_status == "noop" and not should_request:
        return "noop_correct"
    if "unsupported_claim" in conflict_types:
        return "unsupported_claim"
    if "l1_scene_override_attempt" in conflict_types:
        return "scene_conflict"
    if validation_status == "rejected_by_policy":
        return "policy_rejection"
    if validation_status == "accepted_as_evidence":
        hint = SCENE_USAGE_HINTS.get(scene, {})
        if hint.get("recommended_usage") == "high":
            return "high_value_evidence"
        return "accepted_evidence"
    if validation_status == "accepted_as_alternative":
        return "accepted_alternative"
    return "insufficient_information"


def _compute_value_score(
    *,
    validation_status: str,
    evaluation_outcome: str,
    latency_ms: float,
    cost_estimate: float,
) -> float:
    base = 0.0
    if evaluation_outcome in HIGH_VALUE_OUTCOMES:
        base = 0.8
    elif evaluation_outcome == "noop_correct":
        base = 0.6
    elif evaluation_outcome == "accepted_alternative":
        base = 0.5
    elif evaluation_outcome in NEGATIVE_OUTCOMES:
        base = -0.5
    cost_penalty = min(cost_estimate * 10, 0.2)
    latency_penalty = min(latency_ms / 10000, 0.1)
    if validation_status == "rejected_by_policy":
        base = min(base, -0.3)
    return round(base - cost_penalty - latency_penalty, 4)


def _build_usage_profile_candidate(scene: str, *, provider_id: str = PROVIDER_ID) -> Dict[str, Any]:
    hint = SCENE_USAGE_HINTS.get(scene, {"recommended_usage": "medium", "reason": "default_uncertainty"})
    return {
        "profile_id": _uid("tup"),
        "scene_type": scene,
        "teacher_provider": provider_id,
        "recommended_usage": hint["recommended_usage"],
        "reason": hint["reason"],
        "candidate_only": True,
        "not_fact": True,
        "review_status": "pending_policy_review",
        "does_not_affect_current_decision": True,
    }


def build_usage_policy_update_candidate(
    profiles: List[Dict[str, Any]],
    reliability: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate policy improvement candidate — requires human/rule review before apply."""
    suggestions = []
    for p in profiles:
        if p.get("recommended_usage") == "low":
            suggestions.append({
                "scene_type": p["scene_type"],
                "suggestion": "strengthen_noop_for_routine_case",
                "teacher_provider": p.get("teacher_provider"),
            })
        elif p.get("recommended_usage") == "high":
            suggestions.append({
                "scene_type": p["scene_type"],
                "suggestion": "allow_admission_on_high_uncertainty",
                "teacher_provider": p.get("teacher_provider"),
            })
    return {
        "update_candidate_id": _uid("tpuc"),
        "source_type": "teacher_performance_evaluation",
        "suggested_policy_changes": suggestions,
        "reliability_summary_ref": reliability.get("metrics_id"),
        "review_status": "pending_policy_review",
        "no_auto_apply": True,
        "does_not_affect_current_decision": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, "teacher_usage_policy_v1"],
    }


def evaluate_teacher_performance(
    integration_result: Dict[str, Any],
    *,
    case_id: Optional[str] = None,
    metrics: Optional[TeacherPerformanceMetrics] = None,
    provider_id: str = PROVIDER_ID,
) -> Dict[str, Any]:
    """
    Evaluate teacher performance after validation.
    Does NOT affect current admission, plan, or scene decisions.
    """
    metrics = metrics or get_performance_metrics()
    evaluation_id = _uid("tpe")

    admission = integration_result.get("teacher_admission") or integration_result.get("teacher_request") or {}
    review = integration_result.get("teacher_validation_review") or {}
    raw = integration_result.get("raw_teacher_response") or {}

    scene = _scene(integration_result)
    admission_status = admission.get("admission_status", "unknown")
    validation_status = review.get("teacher_validation_status", "insufficient_information")
    should_request = admission.get("should_request_teacher", False)
    conflicts = _conflict_types(review)

    outcome = classify_evaluation_outcome(
        scene=scene,
        admission_status=admission_status,
        validation_status=validation_status,
        conflict_types=conflicts,
        should_request=should_request,
    )

    latency_ms = float(raw.get("latency_ms") or 0)
    cost_estimate = 0.0
    if raw.get("usage"):
        tokens = int((raw.get("usage") or {}).get("total_tokens") or 0)
        cost_estimate = round(tokens * 0.00001, 6)

    value_score = _compute_value_score(
        validation_status=validation_status,
        evaluation_outcome=outcome,
        latency_ms=latency_ms,
        cost_estimate=cost_estimate,
    )

    teacher_noop_correct = outcome == "noop_correct"

    record = {
        "record_id": _uid("tpr"),
        "evaluation_id": evaluation_id,
        "case_id": case_id or integration_result.get("case_id"),
        "job_id": integration_result.get("job_id"),
        "provider_id": provider_id,
        "scene_type": scene,
        "admission_status": admission_status,
        "validation_status": validation_status,
        "evaluation_outcome": outcome,
        "teacher_noop_correct": teacher_noop_correct,
        "value_score": value_score,
        "latency_ms": latency_ms,
        "cost_estimate": cost_estimate,
        "conflict_types": conflicts,
        "candidate_only": True,
        "not_fact": True,
        "does_not_affect_current_decision": True,
        "trace_refs": [
            {"stage": "teacher_performance_evaluation", "ref": evaluation_id},
            {"stage": "validation_status", "status": validation_status},
        ],
    }
    metrics.add_record(record)

    profile = _build_usage_profile_candidate(scene, provider_id=provider_id)
    reliability = metrics.to_reliability_metrics(provider_id=provider_id, metrics_id=_uid("trm"))
    policy_update = build_usage_policy_update_candidate([profile], reliability)

    return {
        "evaluation_id": evaluation_id,
        "teacher_performance_record": record,
        "teacher_usage_profile_candidate": profile,
        "teacher_reliability_metrics": reliability,
        "usage_policy_update_candidate": policy_update,
        "evaluation_outcome": outcome,
        "value_score": value_score,
        "teacher_noop_correct": teacher_noop_correct,
        "does_not_affect_current_decision": True,
        "no_auto_policy_update": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF],
    }
