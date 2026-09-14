from __future__ import annotations

from typing import Any, Dict, Mapping


def build_field_perception_stop_condition_v1(
    information_gap: Mapping[str, Any],
    observation_goal: Mapping[str, Any],
) -> Dict[str, Any]:
    gap = tuple(information_gap.get("information_gap") or ())
    goal = str(observation_goal.get("observation_goal") or "")
    return {
        "schema_version": "field_perception_stop_condition_v1",
        "stop_condition": {
            "condition_id": f"stop::{goal or 'none'}",
            "rule": "stop_when_minimum_sufficient_evidence_collected",
            "required_evidence_count": 0 if not gap else 1,
            "confidence_requirement": 0.85 if gap else 0.6,
        },
    }
