# -*- coding: utf-8 -*-
"""Local Model Runtime Selection — capability + runtime multi-factor v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.runtime.runtime_resource_profile_v1 import (
    is_resource_available,
    resource_availability_score,
)

COST_TIER_SCORE = {"low": 1.0, "medium": 0.7, "high": 0.4}

PROVIDER_META: Dict[str, Dict[str, Any]] = {
    "qwen_vl": {
        "capability_score": 0.85,
        "reliability": 0.90,
        "latency_ms": 3000,
        "cost_tier": "medium",
        "execution_mode": "external_api",
    },
    "internvl2_5": {
        "capability_score": 0.82,
        "reliability": 0.85,
        "latency_ms": 2000,
        "cost_tier": "low",
        "execution_mode": "local_runtime",
    },
    "gemini_vision": {
        "capability_score": 0.88,
        "reliability": 0.70,
        "latency_ms": 500,
        "cost_tier": "high",
        "execution_mode": "external_api",
    },
}


def _latency_score(latency_ms: float) -> float:
    if latency_ms <= 1000:
        return 1.0
    if latency_ms <= 2000:
        return 0.85
    if latency_ms <= 3000:
        return 0.7
    return 0.5


def compute_provider_score(
    *,
    model_id: str,
    meta: Dict[str, Any],
    resource_profile: Dict[str, Any],
    scoring_mode: str = "balanced",
) -> Dict[str, Any]:
    """Multi-factor: capability + reliability + latency + cost + resource."""
    cap = meta.get("capability_score", 0.3)
    rel = meta.get("reliability", 0.5)
    lat = _latency_score(meta.get("latency_ms", 3000))
    cost = COST_TIER_SCORE.get(meta.get("cost_tier", "medium"), 0.7)
    res = resource_availability_score(resource_profile) if resource_profile else 0.0

    if not is_resource_available(resource_profile):
        res = 0.0

    if scoring_mode == "cost_priority":
        combined = round((cap * 0.25 + rel * 0.15 + lat * 0.1 + cost * 0.35 + res * 0.15), 3)
        selection_reason = "local_runtime_available_cost_priority" if model_id == "internvl2_5" and res > 0 else "balanced"
    else:
        combined = round((cap * 0.35 + rel * 0.25 + lat * 0.15 + cost * 0.1 + res * 0.15), 3)
        selection_reason = "multi_factor_balanced"

    return {
        "model_id": model_id,
        "execution_mode": meta.get("execution_mode", "external_api"),
        "capability_score": cap,
        "reliability": rel,
        "latency_score": lat,
        "cost_score": cost,
        "resource_score": res,
        "routing_score": combined if res > 0 else 0.0,
        "resource_available": res > 0,
        "selection_reason": selection_reason,
        "candidate_only": True,
    }


def select_runtime_provider(
    *,
    capability_id: str,
    resource_profiles: Dict[str, Dict[str, Any]],
    scoring_mode: str = "balanced",
    provider_filter: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Capability Match + Runtime Availability → Provider Candidate.
    Runtime Capability: ability belongs to model, resource belongs to runtime.
    """
    scores: List[Dict[str, Any]] = []
    for model_id, meta in PROVIDER_META.items():
        if provider_filter and model_id not in provider_filter:
            continue
        profile = resource_profiles.get(model_id, {})
        scores.append(compute_provider_score(
            model_id=model_id,
            meta=meta,
            resource_profile=profile,
            scoring_mode=scoring_mode,
        ))

    scores.sort(key=lambda x: -x["routing_score"])
    eligible = [s for s in scores if s.get("resource_available")]
    selected = eligible[0] if eligible else None

    return {
        "capability_id": capability_id,
        "provider_scores": scores,
        "eligible_providers": eligible,
        "selected_provider": selected,
        "provider_selection_candidate": True,
        "produced_provider_candidate_not_decision": True,
        "runtime_capability_match": True,
        "scoring_mode": scoring_mode,
        "candidate_only": True,
        "not_fact": True,
    }
