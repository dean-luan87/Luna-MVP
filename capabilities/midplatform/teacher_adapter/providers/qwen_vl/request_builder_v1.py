# -*- coding: utf-8 -*-
"""Qwen-VL Teacher — request builder v1 (Luna evidence → Teacher input only)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.teacher_adapter.providers.qwen_vl.qwen_vl_teacher_types_v1 import (
    ALLOWED_INPUT_FIELDS,
    FORBIDDEN_INPUT_FIELDS,
    TEACHER_ROLE,
)

PERCEPTION_PROMPT_TEMPLATE = """You are a Perception Teacher for Luna vision system.
You provide evidence candidates only — never facts, plans, or tool execution commands.

Context:
- scene_candidate: {scene_candidate}
- plan_goal_candidate: {plan_goal}
- task: {task}
- missing_information: {missing_information}

Analyze the image and respond with JSON only:
{{
  "scene_hypothesis_candidates": [
    {{"scene_type": "...", "confidence_candidate": 0.0-1.0, "candidate_only": true}}
  ],
  "visual_attention_candidates": [],
  "task_clue_candidates": [],
  "tools_suggested": [],
  "named_entity_claims": [],
  "supporting_reason": "...",
  "uncertainty": 0.0-1.0,
  "candidate_only": true,
  "not_fact": true
}}

Rules:
- Output hypotheses, not confirmed facts.
- Do not override Luna scene or plan ownership.
- Do not command tool execution."""


def _scene(situation: Dict[str, Any]) -> str:
    return (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")


def _plan_goal(plan: Optional[Dict[str, Any]]) -> str:
    if not plan:
        return "understand_environment"
    return (plan.get("plan_goal_candidate") or {}).get("goal_type", "understand_environment")


def _missing_labels(situation: Dict[str, Any]) -> List[str]:
    return [m.get("info_type", "") for m in situation.get("missing_information_candidates", [])]


def validate_request_boundary(payload: Dict[str, Any]) -> Optional[str]:
    for key in payload:
        if key in FORBIDDEN_INPUT_FIELDS:
            return f"forbidden_field:{key}"
    for field in payload.get("forbidden_fields_present") or []:
        if field in FORBIDDEN_INPUT_FIELDS:
            return f"forbidden_field:{field}"
    return None


def build_teacher_request(
    *,
    situation_candidate: Dict[str, Any],
    plan_candidate: Optional[Dict[str, Any]] = None,
    image_ref: Optional[str] = None,
    image_path: Optional[str] = None,
    task: str = "understand_environment",
) -> Dict[str, Any]:
    """Convert Luna Evidence Layer fields into Qwen-VL Teacher request (no internal state)."""
    scene = _scene(situation_candidate)
    plan_goal = _plan_goal(plan_candidate)
    missing = _missing_labels(situation_candidate)

    prompt = PERCEPTION_PROMPT_TEMPLATE.format(
        scene_candidate=scene,
        plan_goal=plan_goal,
        task=task,
        missing_information=", ".join(missing) or "none",
    )

    payload = {
        "teacher_role": TEACHER_ROLE,
        "scene_candidate": scene,
        "plan_goal_candidate": plan_goal,
        "task": task,
        "image_ref": image_ref,
        "image_path": image_path,
        "missing_information": missing,
        "prompt_text": prompt,
        "allowed_input_fields": list(ALLOWED_INPUT_FIELDS),
        "candidate_only": True,
        "not_fact": True,
    }
    err = validate_request_boundary(payload)
    if err:
        payload["boundary_error"] = err
    return payload
