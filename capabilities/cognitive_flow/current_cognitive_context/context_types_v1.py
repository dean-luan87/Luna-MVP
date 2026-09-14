"""Stable types for Current Cognitive Context v1."""

from __future__ import annotations

from enum import Enum


CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1 = "luna.current_cognitive_context.v1"


class ContextLifecycleStatusV1(str, Enum):
    REQUESTED = "requested"
    BUILT = "built"
    VALIDATED = "validated"
    ACTIVE = "active"
    REFRESHED = "refreshed"
    SUPERSEDED = "superseded"
    ARCHIVED = "archived"


class ContextSufficiencyStatusV1(str, Enum):
    SUFFICIENT = "sufficient"
    CONDITIONALLY_SUFFICIENT = "conditionally_sufficient"
    INSUFFICIENT = "insufficient"
    UNKNOWN = "unknown"


class InformationGapTypeV1(str, Enum):
    MISSING_ENTITY = "missing_entity"
    MISSING_RELATION = "missing_relation"
    MISSING_STATE = "missing_state"
    MISSING_TIME = "missing_time"
    MISSING_LOCATION = "missing_location"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    STALE_INFORMATION = "stale_information"
    INSUFFICIENT_RESOLUTION = "insufficient_resolution"
    PERMISSION_RESTRICTED = "permission_restricted"


class ContextInvalidationReasonV1(str, Enum):
    SOURCE_SNAPSHOT_CHANGED = "source_snapshot_changed"
    FIELD_STATE_CHANGED = "field_state_changed"
    TASK_STAGE_CHANGED = "task_stage_changed"
    GOAL_CHANGED = "goal_changed"
    SUBJECT_CHANGED = "subject_changed"
    ATTENTION_SCOPE_CHANGED = "attention_scope_changed"
    TEMPORAL_SCOPE_EXPIRED = "temporal_scope_expired"
    CRITICAL_EVIDENCE_REVOKED = "critical_evidence_revoked"
    PERMISSION_SCOPE_CHANGED = "permission_scope_changed"


class ContextExclusionReasonV1(str, Enum):
    IRRELEVANT_TO_CURRENT_TASK = "irrelevant_to_current_task"
    OUTSIDE_ATTENTION_SCOPE = "outside_attention_scope"
    TEMPORALLY_STALE = "temporally_stale"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    DUPLICATE_REPRESENTATION = "duplicate_representation"
    OUTSIDE_SUBJECT_PERMISSION = "outside_subject_permission"
    OUTSIDE_SPATIAL_SCOPE = "outside_spatial_scope"
    DEFERRED_FOR_LATER_ANALYSIS = "deferred_for_later_analysis"
