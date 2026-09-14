# -*- coding: utf-8 -*-
"""Model Routing Engine — unified tool/model selection v1 (planning)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from capabilities.midplatform.model_manager.luna_model_manager_types_v1 import POLICY_REF

TEXT_GOALS = frozenset({"read_text", "identify_place", "find_direction"})
SCENE_SCORE_HINTS = {
    ("shopfront_sign", "text_recognition"): {"ocr_v1": 0.95, "qwen_vl": 0.4, "slam_v1": 0.0},
    ("unknown_scene", "unknown_scene_reasoning"): {"qwen_vl": 0.85, "ocr_v1": 0.1, "slam_v1": 0.2},
    ("indoor_mall", "complex_reasoning"): {"gpt_vision": 0.8, "qwen_vl": 0.65, "ocr_v1": 0.15},
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _repo_root() -> Path:
    for base in (Path.cwd(), Path(__file__).resolve().parents[3]):
        if (base / "capabilities/test_board/test_board_protocol_v1.py").is_file():
            return base
    return Path(__file__).resolve().parents[3]


def _load_json(rel: str) -> Dict[str, Any]:
    path = _repo_root() / rel
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


def _model_by_id(registry: Dict[str, Any], model_id: str) -> Optional[Dict[str, Any]]:
    for m in registry.get("models") or []:
        if m.get("model_id") == model_id:
            return m
    return None


def _routing_eligible(model: Dict[str, Any], lifecycle_policy: Dict[str, Any]) -> bool:
    state = model.get("lifecycle_state", "candidate")
    eligible = lifecycle_policy.get("routing_eligible_states") or ["admitted", "active"]
    admission = model.get("admission_status", "")
    return state in eligible and (admission == "admitted" or state == "active")


def resolve_capability_need(
    *,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    need_capability: Optional[str] = None,
) -> str:
    """Capability-first: determine what capability Luna needs."""
    scene = _scene(situation)
    goal = _plan_goal(plan)
    missing = _missing_types(situation)

    if need_capability:
        return need_capability
    if scene == "unknown_scene" or "scene_identity" in missing:
        return "unknown_scene_reasoning"
    if "text_content" in missing or goal in TEXT_GOALS or scene == "shopfront_sign":
        return "text_recognition"
    if goal in ("find_best_option", "complex_navigation"):
        return "complex_reasoning"
    if "navigation_map" in missing:
        return "spatial_mapping"
    return "object_detection"


def score_providers(
    *,
    capability_id: str,
    scene: str,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Score all providers for a capability need."""
    cap_registry = _load_json("capabilities/midplatform/model_manager/registries/capability_registry_v1.json")
    model_registry = _load_json("capabilities/midplatform/model_manager/registries/model_registry_v1.json")
    lifecycle = _load_json("capabilities/midplatform/model_manager/governance/model_lifecycle_policy_v1.json")

    cap_entry = next((c for c in cap_registry.get("capabilities") or [] if c.get("capability_id") == capability_id), None)
    if not cap_entry:
        return []

    hints = SCENE_SCORE_HINTS.get((scene, capability_id), {})
    goal = _plan_goal(plan)
    scores: List[Dict[str, Any]] = []

    for prov in cap_entry.get("providers") or []:
        model_id = prov.get("model_id", "")
        if model_id == "human_review":
            continue
        model = _model_by_id(model_registry, model_id)
        if not model or not _routing_eligible(model, lifecycle):
            if prov.get("status") != "active":
                continue
        base = hints.get(model_id, 0.3)
        if capability_id == "text_recognition" and model_id == "qwen_vl":
            base = 0.4
        if capability_id == "spatial_mapping" and goal in TEXT_GOALS and model_id == "slam_v1":
            base = 0.0
        if prov.get("status") == "candidate":
            base *= 0.5
        scores.append({
            "model_id": model_id,
            "provider_type": prov.get("provider_type", model.get("type") if model else "unknown"),
            "routing_score": round(base, 2),
            "priority": prov.get("priority", 99),
            "lifecycle_state": (model or {}).get("lifecycle_state", "candidate"),
            "candidate_only": True,
        })

    scores.sort(key=lambda x: (-x["routing_score"], x["priority"]))
    return scores


def route_model_request(
    *,
    situation_understanding_candidate: Dict[str, Any],
    agent_plan_candidate: Dict[str, Any],
    decision_validation_candidate: Optional[Dict[str, Any]] = None,
    need_capability: Optional[str] = None,
) -> Dict[str, Any]:
    """
  Unified Model Routing Engine.
  Capability-first → score providers → select best.
  Output routing_candidate only; does not execute.
    """
    routing_id = _uid("mr")
    situation = situation_understanding_candidate
    plan = agent_plan_candidate
    scene = _scene(situation)
    validation = decision_validation_candidate or {}
    val_status = validation.get("validation_status_candidate", "")

    capability_id = resolve_capability_need(
        situation=situation,
        plan=plan,
        need_capability=need_capability,
    )
    scores = score_providers(
        capability_id=capability_id,
        scene=scene,
        situation=situation,
        plan=plan,
    )

    selected = scores[0] if scores else None
    route_type = "noop"
    selected_model = None
    selected_tool = None
    should_invoke = False

    if selected and selected.get("routing_score", 0) >= 0.5:
        if selected.get("provider_type") == "tool":
            route_type = "tool"
            selected_tool = selected["model_id"]
            should_invoke = False
        else:
            route_type = "model"
            selected_model = selected["model_id"]
            should_invoke = True
    elif selected and selected.get("routing_score", 0) >= 0.3:
        route_type = "model" if selected.get("provider_type") == "teacher" else "tool"
        selected_model = selected["model_id"] if route_type == "model" else None
        selected_tool = selected["model_id"] if route_type == "tool" else None
        should_invoke = route_type == "model"

    if (
        scene == "shopfront_sign"
        and capability_id == "text_recognition"
        and val_status == "validated_candidate"
        and "ocr" in _active_tools(plan)
    ):
        ocr_score = next((s for s in scores if s["model_id"] == "ocr_v1"), None)
        if ocr_score:
            route_type = "tool"
            selected_tool = "ocr_v1"
            selected_model = None
            should_invoke = False
            selected = ocr_score

    return {
        "routing_id": routing_id,
        "capability_need": capability_id,
        "route_type": route_type,
        "selected_model_id": selected_model,
        "selected_tool_id": selected_tool,
        "selected_provider": selected,
        "provider_scores": scores,
        "should_invoke_model": should_invoke,
        "should_request_teacher": should_invoke and route_type == "model",
        "routing_reason": f"capability_first:{capability_id}",
        "capability_first": True,
        "candidate_only": True,
        "not_fact": True,
        "routing_candidate": True,
        "does_not_override_l1_scene": True,
        "does_not_override_l2_plan": True,
        "no_auto_execution": True,
        "policy_refs": [POLICY_REF, "model_lifecycle_policy_v1"],
        "trace_refs": [{"stage": "model_routing_engine", "ref": routing_id}],
    }
