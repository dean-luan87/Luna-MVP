# -*- coding: utf-8
"""Gemini Teacher provider stub v1 — no real API."""

from __future__ import annotations

from typing import Any, Dict, List

PROVIDER_ID = "gemini"
PROVIDER_LABEL = "Gemini Vision (stub)"


def invoke_gemini_teacher_stub(
    *,
    teacher_role: str,
    task_type: str,
    input_evidence: List[Dict[str, Any]],
    situation: Dict[str, Any],
    agent_plan: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type", "unknown_scene")
    if teacher_role == "perception_teacher":
        return {
            "provider_id": PROVIDER_ID,
            "provider_label": PROVIDER_LABEL,
            "teacher_role": teacher_role,
            "task_type": task_type,
            "perception_output": {
                "scene_hypothesis_candidates": [
                    {"scene_type": "shopfront_sign", "confidence": 0.42, "candidate_only": True, "not_fact": True},
                    {"scene_type": "subway_platform", "confidence": 0.35, "candidate_only": True, "not_fact": True},
                ],
                "visual_evidence_candidates": [],
                "uncertainty": 0.35,
                "wording": "evidence supports scene hypothesis candidates",
                "candidate_only": True,
                "not_fact": True,
            },
            "confidence": 0.42 if scene == "unknown_scene" else 0.55,
            "stub_only": True,
            "no_network": True,
        }
    if teacher_role == "planning_teacher":
        return {
            "provider_id": PROVIDER_ID,
            "provider_label": PROVIDER_LABEL,
            "teacher_role": teacher_role,
            "task_type": task_type,
            "planning_output": {
                "alternative_plan_candidate": {
                    "plan_goal_type": "navigate",
                    "strategy_type": "navigation_support",
                    "suggested_steps_summary": "建议先确认入口位置，再读取招牌",
                    "tools_suggested": ["detection", "depth"],
                    "does_not_override_selected_plan": True,
                    "candidate_only": True,
                    "not_fact": True,
                },
                "candidate_only": True,
                "not_fact": True,
            },
            "confidence": 0.58,
            "stub_only": True,
            "no_network": True,
        }
    return {
        "provider_id": PROVIDER_ID,
        "provider_label": PROVIDER_LABEL,
        "teacher_role": teacher_role,
        "task_type": task_type,
        "learning_output": {
            "learning_summary": "teacher case candidate from gemini stub",
            "review_status": "pending_policy_review",
            "candidate_only": True,
            "not_fact": True,
        },
        "confidence": 0.5,
        "stub_only": True,
        "no_network": True,
    }
