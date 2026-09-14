# -*- coding: utf-8 -*-
"""Local Model Lifecycle Adapter — extended admission pipeline v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.lifecycle.model_admission_processor_v1 import (
    complete_admission,
    start_admission_pipeline,
)
from capabilities.midplatform.model_manager.lifecycle.model_lifecycle_processor_v1 import (
    activate_model,
    deprecate_model,
    discover_model,
    reset_sandbox_registry,
    run_sandbox_evaluation,
    _persist,
)
from capabilities.midplatform.model_manager.lifecycle.model_registry_state_machine_v1 import (
    is_routing_eligible,
    transition_model_state,
)
from capabilities.midplatform.model_manager.runtime.local_model_runtime_adapter_v1 import (
    build_local_model_record,
    run_environment_check,
)
from capabilities.midplatform.model_manager.runtime.runtime_resource_profile_v1 import (
    build_resource_profile,
)

LOCAL_MODEL_ID = "internvl2_5"
LOCAL_MODEL_ID_V2 = "internvl2_5_v2"


def run_local_model_admission_pipeline(
    *,
    model_id: str = LOCAL_MODEL_ID,
    model_label: str = "InternVL 2.5",
    capabilities: Optional[List[str]] = None,
    capability_id: str = "unknown_scene_reasoning",
    gpu_memory_available_gb: float = 12,
    cuda_available: bool = True,
    reliability: float = 0.82,
    latency_ms: float = 2000,
) -> Dict[str, Any]:
    """
    Local model lifecycle:
    discovery → candidate → environment_check → runtime_compat → benchmark → admitted → active
    """
    caps = capabilities or ["scene_understanding", "visual_reasoning", "unknown_scene_reasoning"]
    record = build_local_model_record(
        model_id=model_id,
        model_label=model_label,
        capabilities=caps,
    )
    discovery = discover_model(
        model_id=model_id,
        model_label=model_label,
        model_type="vision_language_model",
        capabilities=caps,
        owner="local_runtime",
    )
    record = discovery["model_record"]
    record["execution_mode"] = "local_runtime"
    record["provider_adapter"] = "local_vlm_adapter"

    env_check = run_environment_check(
        record,
        gpu_memory_available_gb=gpu_memory_available_gb,
        cuda_available=cuda_available,
    )
    record["environment_check"] = env_check

    if not env_check.get("all_passed"):
        blocked = transition_model_state(
            model_record=record,
            to_state="blocked",
            reason=env_check.get("failure_reason", "environment_check_failed"),
        )
        if blocked.get("success"):
            _persist(model_id, blocked["model_record"])
        return {
            "success": False,
            "admitted": False,
            "blocked": True,
            "environment_check": env_check,
            "model_record": blocked.get("model_record", record),
            "routing_eligible": False,
            "candidate_only": True,
        }

    admission_start = start_admission_pipeline(model_record=record)
    record = admission_start["model_record"]
    _persist(model_id, record)

    evaluation = run_sandbox_evaluation(
        model_id=model_id,
        capability_id=capability_id,
        reliability=reliability,
        latency_ms=latency_ms,
        cost_tier="low",
    )
    admission = complete_admission(
        model_record=record,
        benchmark_record=evaluation["benchmark_record"],
    )
    record = admission["model_record"]
    _persist(model_id, record)

    activation = activate_model(model_id=model_id)
    record = activation.get("model_record", record)

    resource_profile = build_resource_profile(
        model_id=model_id,
        execution_mode="local_runtime",
        gpu_memory_required_gb=(record.get("resource_profile") or {}).get("gpu_memory_required_gb", 8),
        gpu_memory_available_gb=gpu_memory_available_gb,
        inference_time_ms_avg=latency_ms,
        runtime_status="available",
    )

    return {
        "success": admission.get("admitted", False),
        "admitted": admission.get("admitted", False),
        "environment_check": env_check,
        "evaluation": evaluation,
        "admission": admission,
        "activation": activation,
        "model_record": record,
        "resource_profile": resource_profile,
        "routing_eligible": is_routing_eligible(
            record.get("lifecycle_state", ""),
            admission_status=record.get("admission_status", ""),
        ),
        "candidate_only": True,
        "not_fact": True,
    }


def run_local_version_upgrade(
    *,
    gpu_memory_available_gb: float = 12,
) -> Dict[str, Any]:
    """InternVL v1 active → v2 candidate → benchmark → v2 active → v1 deprecated."""
    reset_sandbox_registry()
    v1 = run_local_model_admission_pipeline(
        model_id=LOCAL_MODEL_ID,
        model_label="InternVL 2.5 v1",
        gpu_memory_available_gb=gpu_memory_available_gb,
        reliability=0.80,
    )
    v2 = run_local_model_admission_pipeline(
        model_id=LOCAL_MODEL_ID_V2,
        model_label="InternVL 2.5 v2",
        gpu_memory_available_gb=gpu_memory_available_gb,
        reliability=0.86,
        latency_ms=1800,
    )
    deprecation = deprecate_model(
        model_id=LOCAL_MODEL_ID,
        replacement_model_id=LOCAL_MODEL_ID_V2,
        reason="version_upgrade",
    )
    return {
        "v1_lifecycle": v1,
        "v2_lifecycle": v2,
        "v1_deprecation": deprecation,
        "v1_deprecated": (deprecation.get("model_record") or {}).get("lifecycle_state") == "deprecated",
        "v2_active": (v2.get("model_record") or {}).get("lifecycle_state") == "active",
        "trace_preserved": deprecation.get("trace_preserved") is True,
        "upper_layer_unchanged": True,
        "l1_l2_unchanged": True,
        "candidate_only": True,
        "not_fact": True,
    }
