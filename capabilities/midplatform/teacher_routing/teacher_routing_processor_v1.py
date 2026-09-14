# -*- coding: utf-8 -*-
"""Teacher Routing Processor — deterministic teacher selection v1 (planning)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.teacher_routing.luna_teacher_routing_types_v1 import (
    POLICY_REF,
    REGISTRY_REF,
)

TEXT_GOALS = frozenset({"read_text", "identify_place", "find_direction"})
COMPLEX_GOALS = frozenset({"find_best_option", "complex_navigation", "navigate"})


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[3]


def _load_registry() -> Dict[str, Any]:
    path = _repo_root() / "capabilities/midplatform/teacher_routing/teacher_capability_registry_v1.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _load_policy() -> Dict[str, Any]:
    path = _repo_root() / "capabilities/midplatform/teacher_routing/teacher_routing_policy_v1.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _scene(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _plan_goal(plan: Dict[str, Any]) -> str:
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "unknown")


def _missing_types(situation: Dict[str, Any]) -> List[str]:
    return [m.get("info_type", "") for m in situation.get("missing_information_candidates", [])]


def _active_tools(plan: Dict[str, Any]) -> List[str]:
    return [t.get("capability_type", "") for t in plan.get("tool_plan_candidates", [])]


def _tool_available(capabilities: List[Dict[str, Any]], tool_id: str) -> bool:
    for c in capabilities:
        if c.get("capability_type") == tool_id:
            return c.get("availability", "available") != "unavailable"
    return False


def _uncertainty_high(situation: Dict[str, Any], validation: Optional[Dict[str, Any]] = None) -> bool:
    unc = situation.get("uncertainty") or {}
    scene_conf = float((situation.get("scene_profile_candidate") or {}).get("confidence") or 1.0)
    val_status = (validation or {}).get("validation_status_candidate", "")
    return bool(
        unc.get("needs_manual_review")
        or unc.get("needs_user_goal")
        or scene_conf < 0.5
        or _scene(situation) == "unknown_scene"
        or val_status in ("needs_review", "insufficient_information")
    )


def _teacher_entry(registry: Dict[str, Any], teacher_id: str) -> Optional[Dict[str, Any]]:
    for t in registry.get("teachers") or []:
        if t.get("teacher_id") == teacher_id:
            return t
    return None


def _base_route(routing_id: str) -> Dict[str, Any]:
    return {
        "routing_id": routing_id,
        "candidate_only": True,
        "not_fact": True,
        "routing_candidate": True,
        "does_not_override_l1_scene": True,
        "does_not_override_l2_plan": True,
        "no_teacher_execution": True,
        "no_tool_execution": True,
        "no_fact_write": True,
        "policy_refs": [POLICY_REF, REGISTRY_REF],
    }


def route_teacher_request(
    *,
    situation_understanding_candidate: Dict[str, Any],
    agent_plan_candidate: Dict[str, Any],
    decision_validation_candidate: Optional[Dict[str, Any]] = None,
    available_capabilities: Optional[List[Dict[str, Any]]] = None,
    user_goal_candidate: Optional[Dict[str, Any]] = None,
    need_capability: Optional[str] = None,
    complex_decision: bool = False,
) -> Dict[str, Any]:
    """
    Teacher Router — select Teacher or Tool based on Situation + Task + Missing Info.
    Does NOT execute Teacher or Tool; output is routing_candidate only.
    """
    routing_id = _uid("tr")
    registry = _load_registry()
    caps = available_capabilities or [
        {"capability_type": t, "availability": "available"}
        for t in ("ocr", "detection", "depth", "slam", "vlm")
    ]

    situation = situation_understanding_candidate
    plan = agent_plan_candidate
    validation = decision_validation_candidate or {}
    scene = _scene(situation)
    goal = _plan_goal(plan)
    if user_goal_candidate:
        goal = user_goal_candidate.get("goal_type", goal)
    missing = _missing_types(situation)
    tools = _active_tools(plan)
    val_status = validation.get("validation_status_candidate", "")

    # Case D / precise OCR — Qwen weakness
    if need_capability == "precise_ocr" or (
        "text_content" in missing and _tool_available(caps, "ocr") and need_capability != "scene_understanding"
    ):
        if _tool_available(caps, "ocr"):
            qwen = _teacher_entry(registry, "qwen_vl") or {}
            return {
                **_base_route(routing_id),
                "route_type": "tool_os",
                "teacher_request": False,
                "should_request_teacher": False,
                "selected_tool": "ocr",
                "selected_teacher": None,
                "exclude_teachers": ["qwen_vl"],
                "exclude_reason": (qwen.get("weaknesses") or ["precise_ocr"]),
                "routing_reason": "precise_ocr_route_to_tool_not_qwen",
                "rule_matched": "precise_ocr_not_qwen",
                "trace_refs": [{"stage": "teacher_router", "ref": routing_id, "rule": "precise_ocr_not_qwen"}],
            }

    # Case A — shopfront + text + OCR
    if (
        scene == "shopfront_sign"
        and ("text_content" in missing or goal in TEXT_GOALS)
        and _tool_available(caps, "ocr")
        and "ocr" in tools
        and val_status == "validated_candidate"
    ):
        return {
            **_base_route(routing_id),
            "route_type": "tool_os",
            "teacher_request": False,
            "should_request_teacher": False,
            "selected_tool": "ocr",
            "selected_teacher": None,
            "routing_reason": "OCR tool sufficient for shopfront text; Teacher not required",
            "rule_matched": "shopfront_text_use_ocr_not_teacher",
            "trace_refs": [{"stage": "teacher_router", "ref": routing_id, "rule": "shopfront_text_use_ocr_not_teacher"}],
        }

    # Case C — complex decision multi-teacher candidate
    if complex_decision or (
        goal in COMPLEX_GOALS
        and scene in ("indoor_mall", "complex_environment")
        and (user_goal_candidate or {}).get("interpreted_goal", "").find("吃饭") >= 0
    ):
        candidates = [
            {
                "teacher_id": "qwen_vl",
                "teacher_role": "perception_teacher",
                "priority": 1,
                "reason": "environment_perception",
                "status": "active",
                "candidate_only": True,
            },
            {
                "teacher_id": "gpt_vision",
                "teacher_role": "planning_teacher",
                "priority": 2,
                "reason": "complex_goal_planning",
                "status": "planned",
                "candidate_only": True,
            },
        ]
        return {
            **_base_route(routing_id),
            "route_type": "teacher_multi_candidate",
            "teacher_request": True,
            "should_request_teacher": True,
            "selected_teacher": "qwen_vl",
            "primary_teacher_role": "perception_teacher",
            "teacher_candidates": candidates,
            "routing_reason": "complex_decision_needs_perception_and_planning_teachers",
            "rule_matched": "complex_reasoning_multi_candidate",
            "no_multi_teacher_voting": True,
            "sequential_consultation_only": True,
            "trace_refs": [{"stage": "teacher_router", "ref": routing_id, "rule": "complex_reasoning_multi_candidate"}],
        }

    # Case B — unknown_scene + high uncertainty
    if scene == "unknown_scene" and _uncertainty_high(situation, validation):
        qwen = _teacher_entry(registry, "qwen_vl") or {}
        return {
            **_base_route(routing_id),
            "route_type": "teacher_single",
            "teacher_request": True,
            "should_request_teacher": True,
            "selected_teacher": "qwen_vl",
            "selected_teacher_role": "perception_teacher",
            "teacher_capabilities_matched": qwen.get("capabilities", []),
            "routing_reason": "unknown_scene_high_uncertainty",
            "rule_matched": "unknown_scene_high_uncertainty_qwen",
            "trace_refs": [{"stage": "teacher_router", "ref": routing_id, "rule": "unknown_scene_high_uncertainty_qwen"}],
        }

    # Routine noop
    if scene == "shopfront_sign" and "ocr" in tools and val_status == "validated_candidate":
        return {
            **_base_route(routing_id),
            "route_type": "noop",
            "teacher_request": False,
            "should_request_teacher": False,
            "selected_tool": "ocr",
            "routing_reason": "current plan sufficient",
            "rule_matched": "routine_case_noop",
            "trace_refs": [{"stage": "teacher_router", "ref": routing_id, "rule": "routine_case_noop"}],
        }

    return {
        **_base_route(routing_id),
        "route_type": "noop",
        "teacher_request": False,
        "should_request_teacher": False,
        "routing_reason": "no_routing_rule_matched_default_noop",
        "rule_matched": "default_noop",
        "trace_refs": [{"stage": "teacher_router", "ref": routing_id, "rule": "default_noop"}],
    }
