# -*- coding: utf-8 -*-
"""Field State Reducer controlled skeleton types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Tuple


class FieldStateStatusV1(str, Enum):
    CANDIDATE = "candidate"
    PROVISIONAL = "provisional"
    ACTIVE = "active"
    DEGRADED = "degraded"
    UNCERTAIN = "uncertain"
    CONFLICTED = "conflicted"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
    UNRESOLVED = "unresolved"


class FieldStateTypeV1(str, Enum):
    PRESENCE_STATE = "presence_state"
    ACCESSIBILITY_STATE = "accessibility_state"
    PATH_STATE = "path_state"
    OBSTRUCTION_STATE = "obstruction_state"
    FACILITY_STATE = "facility_state"
    SERVICE_STATE = "service_state"
    ENVIRONMENTAL_CONDITION_STATE = "environmental_condition_state"
    HUMAN_ACTIVITY_STATE = "human_activity_state"
    NAVIGATION_RELEVANCE_STATE = "navigation_relevance_state"
    TEMPORARY_OVERLAY_STATE = "temporary_overlay_state"
    UNCERTAINTY_STATE = "uncertainty_state"
    CONFLICT_STATE = "conflict_state"
    ENTITY_FIELD_OBSERVATION_RELATION_STATE = (
        "entity_field_observation_relation_state"
    )


class TemporalValidityStatusV1(str, Enum):
    NOT_YET_VALID = "not_yet_valid"
    ACTIVE = "active"
    EXPIRING = "expiring"
    EXPIRED = "expired"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
    UNKNOWN = "unknown"


class ReductionPolicyTypeV1(str, Enum):
    LATEST_VALID_EVENT = "latest_valid_event"
    HIGHEST_CONFIDENCE_VALID_EVENT = "highest_confidence_valid_event"
    MULTI_EVENT_CONSENSUS = "multi_event_consensus"
    NEGATIVE_EVENT_OVERRIDE = "negative_event_override"
    REVOCATION_OVERRIDE = "revocation_override"
    EXPIRATION_DEGRADE = "expiration_degrade"
    TEMPORARY_OVERLAY_SEPARATION = "temporary_overlay_separation"
    CONFLICT_PRESERVATION = "conflict_preservation"
    INSUFFICIENT_EVIDENCE_UNRESOLVED = "insufficient_evidence_unresolved"
    EXPLICIT_OWNER_OVERRIDE_CANDIDATE = "explicit_owner_override_candidate"
    NO_STATE_CHANGE = "no_state_change"


class ReductionDecisionTypeV1(str, Enum):
    SKELETON_NO_STATE_CHANGE = "skeleton_no_state_change"
    SKELETON_VALIDATION_BLOCKED = "skeleton_validation_blocked"


class StateChangeTypeV1(str, Enum):
    NO_STATE_CHANGE = "no_state_change"
    PLACEHOLDER_ONLY = "placeholder_only"


@dataclass(frozen=True)
class FieldStateReducerConfigSnapshotV1:
    reduction_policy_version: str
    event_type_registry_version: str
    conflict_resolution_matrix_version: str
    deterministic_evaluation_timestamp: str
    skeleton_only: bool = True
    not_runtime: bool = True
    not_production: bool = True


@dataclass(frozen=True)
class FieldStateReducerVersionSnapshotV1:
    reducer_version: str
    reduction_policy_version: str
    registry_version: str
    configuration_snapshot_ref: str


@dataclass(frozen=True)
class FieldStateReducerInputV1:
    admitted_field_events: Tuple[Dict[str, Any], ...]
    temporal_validity_snapshot: Dict[str, Any]
    reducer_config_snapshot: FieldStateReducerConfigSnapshotV1
    reducer_version_snapshot: FieldStateReducerVersionSnapshotV1
    direct_state_mutation_requested: bool = False
    skeleton_only: bool = True
    no_external_lookup: bool = True
    no_provider_recall: bool = True
    no_action_trigger: bool = True


@dataclass(frozen=True)
class FieldStateV1:
    state_id: str
    field_id: str
    state_type: str
    state_value: Optional[Dict[str, Any]]
    state_status: str
    confidence: float
    effective_from: Optional[str]
    effective_until: Optional[str]
    source_event_ids: Tuple[str, ...] = field(default_factory=tuple)
    supporting_event_ids: Tuple[str, ...] = field(default_factory=tuple)
    opposing_event_ids: Tuple[str, ...] = field(default_factory=tuple)
    ignored_event_ids: Tuple[str, ...] = field(default_factory=tuple)
    reducer_version: str = ""
    reduction_policy_version: str = ""
    temporal_snapshot_ref: str = ""
    conflict_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_chain: Tuple[str, ...] = field(default_factory=tuple)
    supersedes_state_id: Optional[str] = None
    derived_not_observed: bool = True
    created_at: str = ""
    updated_at: str = ""


@dataclass(frozen=True)
class FieldStateReducerOutputV1:
    resulting_state: Optional[FieldStateV1]
    reduction_decision: str
    applied_event_ids: Tuple[str, ...]
    rejected_event_ids: Tuple[str, ...]
    ignored_event_ids: Tuple[str, ...]
    conflict_ids: Tuple[str, ...]
    unresolved_conditions: Tuple[str, ...]
    reducer_trace: Dict[str, Any]
    deterministic_replay_key: str
    state_change_type: str
    mutation_allowed_only_by_reducer: bool = True
    skeleton_only: bool = True
    candidate_only: bool = True
    runtime_executed: bool = False
    state_mutation_executed: bool = False
