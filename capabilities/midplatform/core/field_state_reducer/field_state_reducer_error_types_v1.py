# -*- coding: utf-8 -*-
"""Field State Reducer controlled skeleton error namespace v1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


ERROR_NAMESPACE_V1 = "LUNA-PROTO-L2-FIELD-STATE-REDUCER-SKELETON-V1::*"


class FieldStateReducerErrorCodeV1(str, Enum):
    INVALID_REDUCER_INPUT = "invalid_reducer_input"
    RAW_OBSERVATION_NOT_ALLOWED = "raw_observation_not_allowed"
    NON_ADMITTED_EVENT_NOT_ALLOWED = "non_admitted_event_not_allowed"
    MISSING_TEMPORAL_SNAPSHOT = "missing_temporal_snapshot"
    MISSING_VERSION_SNAPSHOT = "missing_version_snapshot"
    UNSTABLE_EVENT_ORDER = "unstable_event_order"
    DIRECT_STATE_MUTATION_FORBIDDEN = "direct_state_mutation_forbidden"
    PROVIDER_RECALL_FORBIDDEN = "provider_recall_forbidden"
    EXTERNAL_LOOKUP_FORBIDDEN = "external_lookup_forbidden"
    ACTION_TRIGGER_FORBIDDEN = "action_trigger_forbidden"
    EVENT_MUTATION_FORBIDDEN = "event_mutation_forbidden"
    RUNTIME_EXECUTION_FORBIDDEN = "runtime_execution_forbidden"
    DATABASE_ACCESS_FORBIDDEN = "database_access_forbidden"
    SCHEDULER_ACCESS_FORBIDDEN = "scheduler_access_forbidden"
    UNSUPPORTED_REDUCTION_POLICY = "unsupported_reduction_policy"
    UNRESOLVED_CONFLICT_PRESERVED = "unresolved_conflict_preserved"


@dataclass(frozen=True)
class FieldStateReducerErrorV1:
    code: FieldStateReducerErrorCodeV1
    message: str
    namespace: str = ERROR_NAMESPACE_V1
    detail: Optional[str] = None
    blocker: bool = True
