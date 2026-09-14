# -*- coding: utf-8 -*-
"""Field State Reducer controlled skeleton trace types v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class FieldStateReducerDecisionStepV1:
    step_id: str
    step_name: str
    step_result: str
    notes: str = ""


@dataclass(frozen=True)
class FieldStateReducerConflictRefV1:
    conflict_id: str
    conflict_type: str
    preserved: bool = True


@dataclass(frozen=True)
class FieldStateReducerReplayKeyV1:
    reducer_version: str
    reduction_policy_version: str
    deterministic_evaluation_timestamp: str
    stable_event_id_fingerprint: str


@dataclass(frozen=True)
class FieldStateReducerProvenanceRefV1:
    provenance_id: str
    source_event_ids: Tuple[str, ...]
    accepted_event_ids: Tuple[str, ...]
    rejected_event_ids: Tuple[str, ...]
    ignored_event_ids: Tuple[str, ...]


@dataclass(frozen=True)
class FieldStateReducerTraceV1:
    trace_id: str
    state_id: str
    reducer_run_id: str
    reducer_version: str
    policy_version: str
    input_event_ids: Tuple[str, ...]
    ordered_event_ids: Tuple[str, ...]
    accepted_event_ids: Tuple[str, ...]
    rejected_event_ids: Tuple[str, ...]
    ignored_event_ids: Tuple[str, ...]
    conflict_ids: Tuple[str, ...]
    temporal_snapshot: Dict[str, Any]
    decision_steps: Tuple[FieldStateReducerDecisionStepV1, ...] = field(
        default_factory=tuple
    )
    resulting_state_hash: str = ""
    replay_key: str = ""
    created_at: str = ""
