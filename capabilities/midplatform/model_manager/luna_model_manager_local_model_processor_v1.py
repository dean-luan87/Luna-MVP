# -*- coding: utf-8 -*-
"""Luna Model Manager Local Model — planning processor v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.local_runtime.local_model_lifecycle_adapter_v1 import (
    LOCAL_MODEL_ID,
    run_local_model_admission_pipeline,
    run_local_version_upgrade,
)
from capabilities.midplatform.model_manager.luna_model_manager_local_model_types_v1 import (
    EXTERNAL_MODEL_ID,
    LOCAL_MODEL_ID as LOCAL_ID,
    POLICY_REF,
    RUNTIME_POLICY_REF,
)
from capabilities.midplatform.model_manager.runtime.runtime_resource_profile_v1 import (
    build_resource_profile,
    is_resource_available,
    resource_availability_score,
)

CAPABILITY_SCORES = {
    "unknown_scene_reasoning": {
        "qwen_vl": {"capability_score": 0.85, "execution_mode": "external_api"},
        "internvl2_5": {"capability_score": 0.82, "execution_mode": "local_runtime"},
        "gemini_vision": {"capability_score": 0.88, "execution_mode": "external_api"},
    },
}


def score_providers_with_resource(
    *,
    capability_id: str,
    resource_profiles: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Capability match + resource availability → unified routing scores."""
    base = CAPABILITY_SCORES.get(capability_id, {})
    scores: List[Dict[str, Any]] = []

    for model_id, meta in base.items():
        profile = resource_profiles.get(model_id) or {}
        cap_score = meta.get("capability_score", 0.3)
        res_score = resource_availability_score(profile) if profile else 1.0
        combined = round(cap_score * res_score, 2) if res_score > 0 else 0.0
        scores.append({
            "model_id": model_id,
            "execution_mode": meta.get("execution_mode", "external_api"),
            "capability_score": cap_score,
            "resource_score": res_score,
            "routing_score": combined,
            "resource_available": is_resource_available(profile) if profile else True,
            "candidate_only": True,
        })

    scores.sort(key=lambda x: -x["routing_score"])
    return scores


def build_provider_fallback_candidate(
    *,
    primary_model_id: str,
    fallback_model_id: str,
    reason: str,
    capability_id: str,
) -> Dict[str, Any]:
    """Explicit provider fallback — not silent model replacement."""
    return {
        "fallback_type": "provider_fallback_candidate",
        "primary_model_id": primary_model_id,
        "fallback_model_id": fallback_model_id,
        "fallback_reason": reason,
        "capability_id": capability_id,
        "not_silent_switch": True,
        "owned_by": "model_manager",
        "candidate_only": True,
        "not_fact": True,
    }


def run_local_model_integration_planning(
    *,
    scenario: str,
    gpu_memory_available_gb: float = 12,
    internvl_busy: bool = False,
) -> Dict[str, Any]:
    """Dispatch planning scenarios for smoke cases."""
    if scenario == "normal_admission":
        return run_local_model_admission_pipeline(gpu_memory_available_gb=gpu_memory_available_gb)
    if scenario == "gpu_insufficient":
        return run_local_model_admission_pipeline(gpu_memory_available_gb=2.0)
    if scenario == "local_vs_external":
        return _scenario_local_vs_external(internvl_busy=internvl_busy)
    if scenario == "version_upgrade":
        return run_local_version_upgrade(gpu_memory_available_gb=gpu_memory_available_gb)
    return {"success": False, "error": f"unknown_scenario:{scenario}"}


def _scenario_local_vs_external(*, internvl_busy: bool) -> Dict[str, Any]:
    """Case C: capability + resource aware provider selection."""
    internvl_status = "busy" if internvl_busy else "available"
    profiles = {
        "qwen_vl": build_resource_profile(
            model_id="qwen_vl",
            execution_mode="external_api",
            inference_time_ms_avg=3000,
            cost_tier="medium",
            api_quota_available=True,
        ),
        "internvl2_5": build_resource_profile(
            model_id="internvl2_5",
            execution_mode="local_runtime",
            gpu_memory_required_gb=8,
            gpu_memory_available_gb=12,
            inference_time_ms_avg=2000,
            runtime_status=internvl_status,
        ),
        "gemini_vision": build_resource_profile(
            model_id="gemini_vision",
            execution_mode="external_api",
            inference_time_ms_avg=500,
            cost_tier="high",
            api_quota_available=True,
        ),
    }

    scores = score_providers_with_resource(
        capability_id="unknown_scene_reasoning",
        resource_profiles=profiles,
    )
    selected = scores[0] if scores else None

    return {
        "capability_id": "unknown_scene_reasoning",
        "resource_profiles": profiles,
        "provider_scores": scores,
        "selected_provider": selected,
        "provider_selection_candidate": True,
        "routing_considers_resource": True,
        "model_manager_location_agnostic": True,
        "candidate_only": True,
        "not_fact": True,
        "policy_refs": [POLICY_REF, RUNTIME_POLICY_REF],
    }


def run_gpu_insufficient_with_fallback() -> Dict[str, Any]:
    """Case B: GPU insufficient → not_available → fallback to Qwen API."""
    admission = run_local_model_admission_pipeline(gpu_memory_available_gb=2.0)
    fallback = None
    if admission.get("blocked"):
        fallback = build_provider_fallback_candidate(
            primary_model_id=LOCAL_ID,
            fallback_model_id=EXTERNAL_MODEL_ID,
            reason="gpu_memory_insufficient",
            capability_id="unknown_scene_reasoning",
        )
    return {
        "admission_result": admission,
        "provider_fallback_candidate": fallback,
        "not_available": admission.get("blocked", False),
        "fallback_to_external_api": fallback is not None,
        "not_silent_switch": True,
        "candidate_only": True,
        "not_fact": True,
    }
