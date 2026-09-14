# -*- coding: utf-8
"""GPT Vision Teacher provider stub v1 — no real API."""

from __future__ import annotations

from typing import Any, Dict, List

PROVIDER_ID = "gpt_vision"
PROVIDER_LABEL = "GPT Vision (stub)"


def invoke_gpt_vision_teacher_stub(
    *,
    teacher_role: str,
    task_type: str,
    input_evidence: List[Dict[str, Any]],
    situation: Dict[str, Any],
    agent_plan: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    return {
        "provider_id": PROVIDER_ID,
        "provider_label": PROVIDER_LABEL,
        "teacher_role": teacher_role,
        "task_type": task_type,
        "planning_output": {
            "alternative_plan_candidate": {
                "plan_goal_type": "navigate",
                "strategy_type": "navigation_support",
                "suggested_steps_summary": "confirm entrance then read sign",
                "does_not_override_selected_plan": True,
                "candidate_only": True,
                "not_fact": True,
            },
            "candidate_only": True,
            "not_fact": True,
        },
        "confidence": 0.55,
        "stub_only": True,
        "no_network": True,
    }
