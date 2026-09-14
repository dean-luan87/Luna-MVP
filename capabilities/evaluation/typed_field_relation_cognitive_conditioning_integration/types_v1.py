"""Evaluation-only types for typed Field relation conditioning."""

from __future__ import annotations

from dataclasses import dataclass


SOURCE_MODE = "CONTROLLED_TYPED_FIELD_RELATION_COGNITIVE_CONDITIONING_TEST"
OBSERVED_IN_FIELD = "OBSERVED_IN_FIELD"
RELATION_KIND = "ENTITY_TO_FIELD_OBSERVATION_RELATION"


@dataclass(frozen=True)
class TypedRelationConditioningSpecV1:
    case_id: str
    context_ref: str
    role_ref: str
    task_ref: str
    goal_ref: str
    information_need_ref: str


__all__ = [
    "OBSERVED_IN_FIELD",
    "RELATION_KIND",
    "SOURCE_MODE",
    "TypedRelationConditioningSpecV1",
]
