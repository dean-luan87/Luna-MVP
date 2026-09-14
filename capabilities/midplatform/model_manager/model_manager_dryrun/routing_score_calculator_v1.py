# -*- coding: utf-8 -*-
"""Routing Score Calculator — unified provider scoring v1 (dryrun)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.engines.model_routing_engine_v1 import (
    score_providers,
)

DRYRUN_SCORE_PROFILES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "shopfront_ocr": {
        "text_recognition": {
            "ocr_v1": {"routing_score": 0.95, "provider_type": "tool"},
            "qwen_vl": {"routing_score": 0.4, "provider_type": "teacher"},
            "slam_v1": {"routing_score": 0.0, "provider_type": "tool", "noop_reason": "not_for_text"},
            "depth_v1": {"routing_score": 0.0, "provider_type": "tool", "noop_reason": "not_for_text"},
            "detection_v1": {"routing_score": 0.0, "provider_type": "tool", "noop_reason": "tracking_not_needed"},
        },
    },
    "unknown_scene_multi": {
        "unknown_scene_reasoning": {
            "qwen_vl": {"routing_score": 0.85, "provider_type": "teacher", "lifecycle_state": "active", "admission_status": "admitted"},
            "gemini_vision": {"routing_score": 0.82, "provider_type": "teacher", "lifecycle_state": "candidate", "admission_status": "pending_review"},
            "human_review": {"routing_score": 0.75, "provider_type": "fallback", "lifecycle_state": "active", "admission_status": "admitted"},
        },
    },
    "reliability_priority": {
        "unknown_scene_reasoning": {
            "qwen_vl": {
                "routing_score": 0.85,
                "provider_type": "teacher",
                "latency_ms": 3000,
                "reliability": 0.9,
            },
            "gemini_vision": {
                "routing_score": 0.82,
                "provider_type": "teacher",
                "latency_ms": 500,
                "reliability": 0.7,
            },
        },
    },
}


def _apply_profile(
    profile_name: str,
    capability_id: str,
    *,
    unavailable_providers: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    profile = DRYRUN_SCORE_PROFILES.get(profile_name, {}).get(capability_id, {})
    unavailable = set(unavailable_providers or [])
    scores: List[Dict[str, Any]] = []
    for model_id, meta in profile.items():
        if model_id in unavailable:
            continue
        scores.append({
            "model_id": model_id,
            "provider_type": meta.get("provider_type", "unknown"),
            "routing_score": meta.get("routing_score", 0),
            "latency_ms": meta.get("latency_ms"),
            "reliability": meta.get("reliability"),
            "noop_reason": meta.get("noop_reason"),
            "priority": meta.get("priority", 99),
            "lifecycle_state": meta.get("lifecycle_state", "active"),
            "admission_status": meta.get("admission_status", "admitted"),
            "candidate_only": True,
        })
    scores.sort(key=lambda x: (-x["routing_score"], x.get("priority", 99)))
    return scores


def calculate_routing_scores(
    *,
    capability_id: str,
    scene: str,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    score_profile: Optional[str] = None,
    scoring_mode: str = "default",
    unavailable_providers: Optional[List[str]] = None,
    admitted_only: bool = False,
) -> Dict[str, Any]:
    """
    Score all providers for a capability need.
    scoring_mode=reliability_priority → prefer reliability over latency.
    """
    if score_profile:
        scores = _apply_profile(score_profile, capability_id, unavailable_providers=unavailable_providers)
    else:
        scores = score_providers(
            capability_id=capability_id,
            scene=scene,
            situation=situation,
            plan=plan,
        )
        if unavailable_providers:
            scores = [s for s in scores if s.get("model_id") not in unavailable_providers]

    if admitted_only:
        scores = [
            s for s in scores
            if s.get("admission_status") == "admitted"
            and s.get("lifecycle_state") in ("admitted", "active")
        ]

    routing_reason = "capability_first"
    if scoring_mode == "reliability_priority":
        scored = [s for s in scores if s.get("reliability") is not None]
        if scored:
            scored.sort(key=lambda x: (-x.get("reliability", 0), -x.get("routing_score", 0)))
            scores = scored
            routing_reason = "reliability_priority"

    noop_providers = [s for s in scores if s.get("routing_score", 0) <= 0]
    eligible = [s for s in scores if s.get("routing_score", 0) > 0]

    return {
        "capability_id": capability_id,
        "provider_scores": scores,
        "eligible_providers": eligible,
        "noop_providers": noop_providers,
        "routing_reason": routing_reason,
        "scoring_mode": scoring_mode,
        "candidate_only": True,
        "not_fact": True,
    }
