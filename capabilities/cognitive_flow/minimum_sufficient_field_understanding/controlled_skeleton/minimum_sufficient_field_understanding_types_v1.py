"""Immutable candidate-only types for Minimum Sufficient Field Understanding v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Tuple


MINIMUM_SUFFICIENT_FIELD_UNDERSTANDING_SCHEMA_VERSION_V1 = (
    "luna.minimum_sufficient_field_understanding.controlled_skeleton.v1"
)

_IDENTITY_STATUSES_V1 = frozenset(("known", "partially_known", "unknown"))


@dataclass(frozen=True)
class BehaviorBoundaryCandidateV1:
    """Current behavior constraints, never an action or permission grant."""

    allowed_behavior_candidate: Tuple[str, ...]
    forbidden_behavior_candidate: Tuple[str, ...]
    risk_boundary: Mapping[str, object]
    exploration_boundary: Mapping[str, object]


@dataclass(frozen=True)
class MinimumSufficientFieldUnderstandingCandidateV1:
    """Minimum behavior-constraint understanding for an incompletely known Field."""

    field_reference: str
    identity_status: str
    constraint_reference: str
    behavior_boundary: BehaviorBoundaryCandidateV1
    information_gap: Tuple[str, ...]
    uncertainty: Mapping[str, object]
    temporal_scope: Mapping[str, object]
    spatial_scope: Mapping[str, object]
    task_reference: str
    provenance: Mapping[str, object]
    trace_ref: str
    candidate_status: str
    candidate_only: bool = True
    not_fact: bool = True
    not_state: bool = True
    not_decision: bool = True
    not_action: bool = True
    schema_version: str = MINIMUM_SUFFICIENT_FIELD_UNDERSTANDING_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class MinimumSufficientFieldUnderstandingSkeletonFlagsV1:
    """Explicitly records the non-executing skeleton boundary."""

    runtime_executed: bool = False
    inference_executed: bool = False
    model_invoked: bool = False
    provider_invoked: bool = False
    external_call: bool = False
    action_created: bool = False
    decision_created: bool = False
    field_kernel_integrated: bool = False
    reducer_integrated: bool = False
    state_mutation: bool = False
    memory_updated: bool = False
    learning_integrated: bool = False
    hive_integrated: bool = False


def is_identity_status_v1(value: str) -> bool:
    """Return whether a declared identity status belongs to the frozen v1 set."""

    return value in _IDENTITY_STATUSES_V1
