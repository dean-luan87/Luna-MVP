"""Immutable caller-provided input contexts for Current Cognitive Context v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from .context_types_v1 import CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class SubjectContextV1:
    subject_ref: str
    subject_role: str
    subject_location_ref: str | None
    subject_capability_constraints: Tuple[str, ...]
    subject_permission_scope: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class TaskContextV1:
    task_ref: str
    task_type: str
    task_stage: str
    task_priority: str
    task_constraints: Tuple[str, ...]
    task_status: str
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class GoalContextV1:
    goal_ref: str
    primary_goal: str
    secondary_goal_refs: Tuple[str, ...]
    success_condition_refs: Tuple[str, ...]
    stop_condition_refs: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class AttentionContextV1:
    attention_scope: str
    attention_targets: Tuple[str, ...]
    attention_priority: str
    excluded_targets: Tuple[str, ...]
    attention_reason_refs: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class TemporalContextV1:
    current_time_reference: str | None
    valid_time_scope: Mapping[str, Any]
    history_window_reference: str | None
    temporal_uncertainty: Mapping[str, Any]
    stale_state_references: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1
