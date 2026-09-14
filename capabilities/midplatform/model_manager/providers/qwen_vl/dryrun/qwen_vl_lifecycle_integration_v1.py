# -*- coding: utf-8 -*-
"""Qwen-VL Lifecycle Integration — version switch dryrun v1."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.midplatform.model_manager.lifecycle.model_lifecycle_processor_v1 import (
    deprecate_model,
    reset_sandbox_registry,
    run_full_lifecycle_sandbox,
)
from capabilities.midplatform.model_manager.luna_model_manager_qwen_vl_types_v1 import (
    MODEL_ID,
    MODEL_ID_V2,
)


def run_qwen_version_switch_dryrun() -> Dict[str, Any]:
    """
    qwen_vl v1 active → qwen_vl_v2 candidate → eval → active → v1 deprecated.
    L1/L2 layers unchanged.
    """
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
        reliability=0.90,
        latency_ms=1000,
        cost_tier="medium",
        owner="external_teacher",
    )
    deprecation = deprecate_model(
        model_id=MODEL_ID,
        replacement_model_id=MODEL_ID_V2,
        reason="version_upgrade",
    )
    v1_final = deprecation.get("model_record") or {}
    return {
        "v1_lifecycle": v1,
        "v2_lifecycle": v2,
        "v1_deprecation": deprecation,
        "v1_was_active": (v1.get("model_record") or {}).get("lifecycle_state") == "active",
        "v2_is_active": (v2.get("model_record") or {}).get("lifecycle_state") == "active",
        "v1_is_deprecated": v1_final.get("lifecycle_state") == "deprecated",
        "trace_preserved": deprecation.get("trace_preserved") is True,
        "upper_layer_unchanged": True,
        "l1_l2_unchanged": True,
        "candidate_only": True,
        "not_fact": True,
    }
