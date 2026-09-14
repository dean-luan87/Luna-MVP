# -*- coding: utf-8 -*-
"""Field State Reducer protocol v1 (controlled skeleton only)."""

from __future__ import annotations

from typing import Any, Dict, Protocol, Tuple

from capabilities.midplatform.core.field_state_reducer.field_state_reducer_trace_types_v1 import (
    FieldStateReducerTraceV1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_types_v1 import (
    FieldStateReducerInputV1,
    FieldStateReducerOutputV1,
)


class FieldStateReducerProtocolV1(Protocol):
    """Protocol only. No real reduction logic is allowed at this stage."""

    def validate_input(
        self, reducer_input: FieldStateReducerInputV1
    ) -> Tuple[bool, Tuple[str, ...]]:
        """Validate controlled skeleton input contract without runtime side effects."""

    def order_events(
        self, reducer_input: FieldStateReducerInputV1
    ) -> Tuple[Dict[str, Any], ...]:
        """Build deterministic placeholder ordering only; no semantic winner selection."""

    def reduce(
        self, reducer_input: FieldStateReducerInputV1
    ) -> FieldStateReducerOutputV1:
        """Return controlled placeholder output only. No real state mutation, no active state creation."""

    def build_trace(
        self,
        reducer_input: FieldStateReducerInputV1,
        ordered_events: Tuple[Dict[str, Any], ...],
        issues: Tuple[str, ...],
    ) -> FieldStateReducerTraceV1:
        """Build non-runtime provenance trace for static review."""

    def build_replay_key(
        self,
        reducer_input: FieldStateReducerInputV1,
        ordered_events: Tuple[Dict[str, Any], ...],
    ) -> str:
        """Build deterministic placeholder replay key with version snapshots."""
