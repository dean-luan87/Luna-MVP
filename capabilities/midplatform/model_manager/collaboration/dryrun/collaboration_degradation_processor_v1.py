# -*- coding: utf-8 -*-
"""Collaboration Degradation Processor — explicit resource downgrade v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.collaboration.dryrun.collaboration_execution_planner_v1 import (
    fill_collaboration_slots,
    plan_parallel_execution,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_collaboration_degradation(
    *,
    original_plan: Dict[str, Any],
    resource_constraint: str = "gpu_unavailable",
    degraded_model_ids: Optional[List[str]] = None,
    lost_capabilities: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Case E: explicit degradation with lost_capability — not silent."""
    original_filled = original_plan.get("filled_slots") or []
    degraded_model_ids = degraded_model_ids or ["qwen_vl"]
    lost_capabilities = lost_capabilities or ["local_visual_reasoning"]

    degraded_slots = [
        {
            "slot_id": "slot_degraded",
            "capability": "unknown_scene_reasoning",
            "role": "scene_hypothesis",
            "filled_model_id": degraded_model_ids[0],
            "execution_mode": "external_api",
            "degraded_from": [s.get("filled_model_id") for s in original_filled],
        }
    ]

    return {
        "degradation_id": _uid("cdg"),
        "original_plan_id": original_plan.get("plan_id"),
        "original_collaboration_type": original_plan.get("collaboration_type"),
        "original_filled_slots": original_filled,
        "degraded_slots": degraded_slots,
        "degraded_model_ids": degraded_model_ids,
        "resource_constraint": resource_constraint,
        "lost_capability": lost_capabilities,
        "lost_capabilities": lost_capabilities,
        "collaboration_degradation_candidate": True,
        "not_silent_degradation": True,
        "requires_validation_ack": True,
        "example_original": "Parallel: InternVL + Grounding",
        "example_degraded": "Qwen only",
        "candidate_only": True,
        "not_fact": True,
    }


def run_resource_degradation_dryrun() -> Dict[str, Any]:
    """Full Case E dryrun."""
    original = plan_parallel_execution()
    degradation = build_collaboration_degradation(
        original_plan=original,
        resource_constraint="internvl2_5_gpu_unavailable",
        degraded_model_ids=["qwen_vl"],
        lost_capabilities=["local_visual_reasoning"],
    )
    validation = {
        "review_id": _uid("dvr"),
        "validation_status": "degradation_acknowledged",
        "not_silent": True,
        "lost_capability_recorded": True,
        "candidate_only": True,
        "not_fact": True,
    }
    return {
        "original_plan": original,
        "collaboration_degradation": degradation,
        "validation_review": validation,
        "had_internvl_in_original": any(
            s.get("filled_model_id") == "internvl2_5" for s in original.get("filled_slots") or []
        ),
        "degraded_to_qwen_only": degradation.get("degraded_model_ids") == ["qwen_vl"],
        "lost_capability_recorded": "local_visual_reasoning" in (degradation.get("lost_capabilities") or []),
        "not_silent_degradation": degradation.get("not_silent_degradation") is True,
        "candidate_only": True,
        "not_fact": True,
    }
