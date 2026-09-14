# -*- coding: utf-8 -*-
"""Model Evaluation Engine — unified provider evaluation v1 (planning)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

POLICY_REF = "model_admission_policy_v1"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_model_evaluation_profile(
    *,
    model_id: str,
    scene_type: str,
    metrics: Dict[str, Any],
) -> Dict[str, Any]:
    """Build unified evaluation profile for any provider (tool or teacher)."""
    return {
        "profile_id": _uid("mep"),
        "model_id": model_id,
        "scene_type": scene_type,
        "accuracy_candidate": metrics.get("useful_evidence_rate", metrics.get("evidence_accept_rate", 0)),
        "latency_ms_avg": metrics.get("latency_ms_avg", 0),
        "cost_estimate": metrics.get("cost_estimate_total", 0),
        "scene_fit_score": metrics.get("teacher_value_score", metrics.get("teacher_value_score_avg", 0)),
        "error_types": _error_types_from_metrics(metrics),
        "user_feedback_value": metrics.get("accepted_evidence_count", 0),
        "routing_profile_candidate": {
            "recommended_usage": _recommended_usage(scene_type, model_id),
            "reason": f"evaluation_aggregate_for_{scene_type}",
        },
        "candidate_only": True,
        "not_fact": True,
        "does_not_affect_current_decision": True,
        "review_status": "pending_policy_review",
    }


def _error_types_from_metrics(metrics: Dict[str, Any]) -> List[str]:
    errors = []
    if metrics.get("unsupported_claim_rate", 0) > 0:
        errors.append("unsupported_claim")
    if metrics.get("scene_conflict_rate", 0) > 0:
        errors.append("scene_conflict")
    if metrics.get("policy_violation_rate", 0) > 0:
        errors.append("policy_violation")
    if metrics.get("rejection_rate", 0) > 0.5:
        errors.append("high_rejection")
    return errors


def _recommended_usage(scene: str, model_id: str) -> str:
    if scene == "unknown_scene" and model_id == "qwen_vl":
        return "high"
    if scene == "shopfront_sign" and model_id == "ocr_v1":
        return "high"
    if scene == "shopfront_sign" and model_id == "qwen_vl":
        return "low"
    return "medium"


def evaluate_model_performance(
    *,
    model_id: str,
    scene_type: str,
    performance_metrics: Dict[str, Any],
    routing_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Unified Model Evaluation Engine output.
    Subsumes Teacher Performance Evaluation; does not auto-update routing.
    """
    evaluation_id = _uid("mev")
    profile = build_model_evaluation_profile(
        model_id=model_id,
        scene_type=scene_type,
        metrics=performance_metrics,
    )
    return {
        "evaluation_id": evaluation_id,
        "model_id": model_id,
        "evaluation_engine": "model_evaluation_engine_v1",
        "model_evaluation_profile": profile,
        "routing_profile_candidate": profile.get("routing_profile_candidate"),
        "reliability_summary": {
            "evidence_accept_rate": performance_metrics.get("evidence_accept_rate", 0),
            "rejection_rate": performance_metrics.get("rejection_rate", 0),
            "hallucination_rate": performance_metrics.get("hallucination_rate", 0),
            "useful_evidence_rate": performance_metrics.get("useful_evidence_rate", 0),
        },
        "routing_result_ref": (routing_result or {}).get("routing_id"),
        "does_not_affect_current_decision": True,
        "no_auto_policy_update": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF],
    }
