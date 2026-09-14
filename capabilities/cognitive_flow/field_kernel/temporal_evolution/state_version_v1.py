"""Immutable Field State Version object for Temporal Evolution v1.

This module represents a State already produced by the Field State Reducer. It
does not create Field State, mutate Field State, or infer missing time.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1 = "luna.field_temporal_evolution.v1"


@dataclass(frozen=True)
class StateVersionV1:
    """One immutable, Reducer-originated version of a Field State.

    `previous_state_version_ref` creates an explicit version chain. A missing
    `valid_from` or `valid_until` is represented as such; callers may add the
    applicable unknown/estimated detail in `temporal_uncertainty`.
    """

    state_version_id: str
    field_ref: str
    field_state_ref: str
    previous_state_version_ref: str | None
    state_type: str
    state_value: Mapping[str, Any]
    valid_from: str | None
    valid_until: str | None
    transition_record_ref: str | None
    provenance: Mapping[str, Any]
    created_at: str
    trace_ref: str
    schema_version: str = TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1
    temporal_uncertainty: Mapping[str, Any] = field(default_factory=dict)
    produced_by: str = "field_state_reducer"
    immutable: bool = True
    state_mutation_executed: bool = False

    def __post_init__(self) -> None:
        if not self.state_version_id or not self.field_ref or not self.field_state_ref:
            raise ValueError("StateVersionV1 requires version, field, and Field State references")
        if self.produced_by != "field_state_reducer":
            raise ValueError("StateVersionV1 must originate from field_state_reducer")
        if not self.trace_ref:
            raise ValueError("StateVersionV1 requires trace_ref")

