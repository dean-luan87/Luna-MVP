# -*- coding: utf-8
"""InternVL Teacher provider stub v1 — no real API."""

from __future__ import annotations

from typing import Any, Dict, List

PROVIDER_ID = "internvl"
PROVIDER_LABEL = "InternVL (stub)"


def invoke_internvl_teacher_stub(
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
        "learning_output": {
            "learning_summary": "internvl teacher learning candidate stub",
            "review_status": "pending_policy_review",
            "candidate_only": True,
            "not_fact": True,
        },
        "confidence": 0.48,
        "stub_only": True,
        "no_network": True,
    }
