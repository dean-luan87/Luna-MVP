# -*- coding: utf-8 -*-
"""Collaboration Execution Planner — slot-based orchestration v1 (dryrun)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    get_provider_by_id,
    list_capability_providers,
)

SLOT_TEMPLATES: Dict[str, List[Dict[str, Any]]] = {
    "identify_place": [
        {"slot_id": "slot_1", "capability": "text_detection", "role": "text_detector", "step": 1, "depends_on": []},
        {"slot_id": "slot_2", "capability": "text_recognition", "role": "ocr", "step": 2, "depends_on": ["slot_1"]},
        {"slot_id": "slot_3", "capability": "context_reasoning", "role": "vlm_context", "step": 3, "depends_on": ["slot_2"]},
    ],
    "understand_scene": [
        {"slot_id": "slot_a", "capability": "unknown_scene_reasoning", "role": "scene_hypothesis", "parallel": True},
        {"slot_id": "slot_b", "capability": "visual_reasoning", "role": "visual_reasoning", "parallel": True},
        {"slot_id": "slot_c", "capability": "object_detection", "role": "grounding", "parallel": True},
    ],
}

SLOT_PROVIDER_FILL: Dict[str, str] = {
    "text_detection": "detection_v1",
    "text_recognition": "ocr_v1",
    "precise_ocr": "ocr_v1",
    "context_reasoning": "qwen_vl",
    "unknown_scene_reasoning_qwen": "qwen_vl",
    "visual_reasoning_local": "internvl2_5",
    "object_detection": "detection_v1",
}

PIPELINE_SEQUENCE_ROLES = ("text_detector", "ocr", "vlm_context")


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_collaboration_slots(
    *,
    goal_type: str,
    collaboration_type: str = "pipeline",
) -> List[Dict[str, Any]]:
    """Build capability slots — not bound to models."""
    key = "identify_place" if collaboration_type == "pipeline" else "understand_scene"
    return [dict(s) for s in SLOT_TEMPLATES.get(key, [])]


def fill_collaboration_slots(
    slots: List[Dict[str, Any]],
    *,
    overrides: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """Model Manager fills slots with providers from registry."""
    overrides = overrides or {}
    filled: List[Dict[str, Any]] = []
    for slot in slots:
        cap = slot.get("capability", "")
        role = slot.get("role", "")
        model_id = overrides.get(slot.get("slot_id", ""))
        if not model_id:
            if role == "scene_hypothesis":
                model_id = "qwen_vl"
            elif role == "visual_reasoning":
                model_id = "internvl2_5"
            elif role == "grounding":
                model_id = "detection_v1"
            else:
                model_id = SLOT_PROVIDER_FILL.get(cap, "")
        provider = get_provider_by_id(model_id) or {}
        filled.append({
            **slot,
            "filled_model_id": model_id,
            "execution_mode": provider.get("execution_mode", "tool_os"),
            "provider_type": provider.get("provider_type", "tool"),
            "slot_filled": bool(model_id),
            "candidate_only": True,
        })
    return filled


def plan_pipeline_execution(
    *,
    goal_type: str = "identify_place",
    scene_type: str = "shopfront_sign",
) -> Dict[str, Any]:
    """Case A: Pipeline — slots first, then provider fill."""
    slots = build_collaboration_slots(goal_type=goal_type, collaboration_type="pipeline")
    filled = fill_collaboration_slots(slots)
    sequence_roles = [s.get("role") for s in filled]

    return {
        "plan_id": _uid("cex"),
        "collaboration_type": "pipeline",
        "goal_type": goal_type,
        "scene_type": scene_type,
        "collaboration_slots": slots,
        "filled_slots": filled,
        "sequence": list(PIPELINE_SEQUENCE_ROLES),
        "reason": "text evidence required before semantic interpretation",
        "ocr_is_primary": filled[1].get("role") == "ocr" if len(filled) > 1 else False,
        "vlm_is_context_only": filled[-1].get("role") == "vlm_context" if filled else False,
        "vlm_not_first": sequence_roles[0] != "vlm_context" if sequence_roles else True,
        "direct_vlm_skipped": sequence_roles[0] != "vlm_context",
        "collaboration_plan_candidate": True,
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }


def plan_parallel_execution(
    *,
    goal_type: str = "understand_scene",
    scene_type: str = "unknown_environment",
) -> Dict[str, Any]:
    """Case B: Parallel evidence plan from slots."""
    slots = build_collaboration_slots(goal_type=goal_type, collaboration_type="parallel")
    filled = fill_collaboration_slots(slots)

    return {
        "plan_id": _uid("pex"),
        "collaboration_type": "parallel_evidence",
        "goal_type": goal_type,
        "scene_type": scene_type,
        "collaboration_slots": slots,
        "filled_slots": filled,
        "evidence_collection_plan": True,
        "not_voting": True,
        "produces_single_answer": False,
        "collaboration_plan_candidate": True,
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_tool_os_handoff_candidate(
    *,
    filled_slots: List[Dict[str, Any]],
    collaboration_type: str,
) -> Dict[str, Any]:
    """Tool OS handoff — selection only, no execution."""
    tool_slots = [s for s in filled_slots if s.get("execution_mode") == "tool_os"]
    model_slots = [s for s in filled_slots if s.get("execution_mode") != "tool_os"]

    return {
        "handoff_id": _uid("toh"),
        "target": "tool_os",
        "collaboration_type": collaboration_type,
        "tool_slot_handoffs": [
            {
                "slot_id": s.get("slot_id"),
                "tool_id": s.get("filled_model_id"),
                "capability": s.get("capability"),
                "handoff_type": "tool_execution_request_candidate",
                "not_executed": True,
            }
            for s in tool_slots
        ],
        "model_slot_handoffs": [
            {
                "slot_id": s.get("slot_id"),
                "model_id": s.get("filled_model_id"),
                "handoff_type": "teacher_evidence_request_candidate",
                "not_executed": True,
            }
            for s in model_slots
        ],
        "tool_os_handoff_candidate": True,
        "candidate_only": True,
        "not_fact": True,
    }
