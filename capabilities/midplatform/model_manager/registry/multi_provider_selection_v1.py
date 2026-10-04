# -*- coding: utf-8 -*-
"""Multi-Provider Selection — capability-first competition v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    get_provider_relations,
    list_capability_providers,
)
from capabilities.midplatform.model_manager.engines.model_provider_routing_lifecycle_closure_v1 import (
    filter_model_provider_routing_lifecycle_eligible,
)

COST_TIER_SCORE = {"low": 1.0, "medium": 0.7, "high": 0.4}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _latency_score(latency_ms: float) -> float:
    if latency_ms <= 1000:
        return 1.0
    if latency_ms <= 2000:
        return 0.85
    if latency_ms <= 3000:
        return 0.7
    return 0.5


def _resource_score(
    *,
    model_id: str,
    execution_mode: str,
    runtime_availability: Dict[str, Any],
) -> float:
    if execution_mode == "local_runtime":
        internvl = runtime_availability.get("internvl2_5", {})
        if model_id.startswith("internvl") and not internvl.get("available", True):
            return 0.0
        return 1.0 if internvl.get("available", True) else 0.0
    if execution_mode == "external_api":
        api = runtime_availability.get("external_api", {})
        if model_id == "gemini_vision" and not api.get("gemini_available", True):
            return 0.0
        if model_id.startswith("qwen") and not api.get("qwen_available", True):
            return 0.0
        return 1.0 if api.get("network_available", True) else 0.0
    if execution_mode == "tool_os":
        return 1.0
    return 0.5


def compute_multi_provider_score(
    *,
    provider: Dict[str, Any],
    capability_id: str,
    runtime_availability: Optional[Dict[str, Any]] = None,
    historical_performance: Optional[Dict[str, float]] = None,
    scoring_mode: str = "balanced",
) -> Dict[str, Any]:
    """Multi-factor: capability + reliability + latency + cost + resource + historical."""
    runtime_availability = runtime_availability or {}
    cap_profile = (provider.get("routing_profile") or {}).get(capability_id) or {}
    if cap_profile.get("excluded"):
        return {
            "model_id": provider.get("model_id"),
            "routing_score": 0.0,
            "excluded": True,
            "exclusion_reason": f"weakness_for_{capability_id}",
            "resource_available": False,
            "candidate_only": True,
        }

    cap = cap_profile.get("capability_score", 0.3)
    rel = cap_profile.get("reliability", 0.5)
    lat = _latency_score(cap_profile.get("latency_ms", 3000))
    cost = COST_TIER_SCORE.get(cap_profile.get("cost_tier", "medium"), 0.7)
    model_id = provider.get("model_id", "")
    execution_mode = provider.get("execution_mode", "external_api")
    res = _resource_score(
        model_id=model_id,
        execution_mode=execution_mode,
        runtime_availability=runtime_availability,
    )
    hist = (historical_performance or {}).get(model_id, 0.5)

    if scoring_mode == "cost_priority":
        combined = round(cap * 0.20 + rel * 0.15 + lat * 0.10 + cost * 0.30 + res * 0.15 + hist * 0.10, 3)
    else:
        combined = round(cap * 0.30 + rel * 0.20 + lat * 0.15 + cost * 0.10 + res * 0.15 + hist * 0.10, 3)

    if res <= 0:
        combined = 0.0

    return {
        "model_id": model_id,
        "provider_type": provider.get("provider_type"),
        "execution_mode": execution_mode,
        "model_family": provider.get("model_family"),
        "capability_score": cap,
        "reliability": rel,
        "latency_score": lat,
        "cost_score": cost,
        "resource_score": res,
        "historical_performance": hist,
        "routing_score": combined,
        "resource_available": res > 0,
        "lifecycle_state": provider.get("lifecycle_state"),
        "relations": get_provider_relations(model_id),
        "candidate_only": True,
    }


def select_multi_provider_candidate(
    *,
    capability_id: str,
    runtime_availability: Optional[Dict[str, Any]] = None,
    historical_performance: Optional[Dict[str, float]] = None,
    scoring_mode: str = "balanced",
    execute: bool = False,
) -> Dict[str, Any]:
    """
    Capability-first routing → multi-factor competition → provider_selection_candidate.
    Does NOT execute model inference.
    """
    providers = list_capability_providers(capability_id)
    eligible_providers = filter_model_provider_routing_lifecycle_eligible(providers)

    scores: List[Dict[str, Any]] = []
    for prov in providers:
        if prov not in eligible_providers and prov.get("lifecycle_state") == "deprecated":
            continue
        score = compute_multi_provider_score(
            provider=prov,
            capability_id=capability_id,
            runtime_availability=runtime_availability,
            historical_performance=historical_performance,
            scoring_mode=scoring_mode,
        )
        if prov in eligible_providers:
            scores.append(score)
        elif score.get("excluded"):
            scores.append(score)

    scores.sort(key=lambda x: -x.get("routing_score", 0))
    resource_eligible = [s for s in scores if s.get("resource_available") and not s.get("excluded")]
    selected = resource_eligible[0] if resource_eligible else None

    return {
        "selection_id": _uid("mps"),
        "capability_id": capability_id,
        "capability_first": True,
        "provider_scores": scores,
        "eligible_providers": resource_eligible,
        "selected_provider": selected,
        "selected_model_id": (selected or {}).get("model_id"),
        "provider_selection_candidate": True,
        "produced_provider_candidate_not_decision": True,
        "execution_requested": execute,
        "execution_performed": False,
        "not_voting": True,
        "not_fusion": True,
        "scoring_mode": scoring_mode,
        "candidate_only": True,
        "not_fact": True,
    }


def build_provider_conflict_candidate(
    *,
    capability_id: str,
    provider_outputs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Case D: conflicting provider hypotheses — not auto-resolved."""
    conflicts = []
    for i, a in enumerate(provider_outputs):
        for b in provider_outputs[i + 1:]:
            if a.get("scene_hypothesis") != b.get("scene_hypothesis"):
                conflicts.append({
                    "provider_a": a.get("model_id"),
                    "hypothesis_a": a.get("scene_hypothesis"),
                    "provider_b": b.get("model_id"),
                    "hypothesis_b": b.get("scene_hypothesis"),
                })

    return {
        "conflict_id": _uid("pcc"),
        "capability_id": capability_id,
        "provider_outputs": provider_outputs,
        "conflicts": conflicts,
        "provider_conflict_candidate": True,
        "not_auto_resolved": True,
        "requires_validation": True,
        "validation_owner": "L2_5_Decision_Validation",
        "candidate_only": True,
        "not_fact": True,
    }
