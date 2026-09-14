# -*- coding: utf-8
"""Qwen-VL Teacher provider stub v1 — no real API."""

from __future__ import annotations

from typing import Any, Dict, List

PROVIDER_ID = "qwen_vl"
PROVIDER_LABEL = "Qwen-VL (stub)"


def invoke_qwen_vl_teacher_stub(
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
        "perception_output": {
            "scene_hypothesis_candidates": [
                {"scene_type": "unknown_scene", "confidence": 0.4, "candidate_only": True, "not_fact": True},
            ],
            "visual_evidence_candidates": [],
            "uncertainty": 0.4,
            "candidate_only": True,
            "not_fact": True,
        },
        "confidence": 0.4,
        "stub_only": True,
        "no_network": True,
    }
