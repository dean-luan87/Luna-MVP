"""Fixed-fixture Temporal Evolution examples v1.

This module is not a runner. The scenarios construct immutable records only;
they never call a Reducer, database, network, model, or system clock.
"""

from __future__ import annotations

from typing import Dict, Tuple

from capabilities.cognitive_flow.field_kernel.temporal_evolution.history_projection_v1 import (
    FieldHistoryProjectionV1,
    build_field_history_projection_v1,
)
from capabilities.cognitive_flow.field_kernel.temporal_evolution.state_version_v1 import StateVersionV1
from capabilities.cognitive_flow.field_kernel.temporal_evolution.transition_record_v1 import TransitionRecordV1


def _version(
    field_ref: str,
    version_id: str,
    state_ref: str,
    previous: str | None,
    value: str,
    valid_from: str | None,
    trace_ref: str,
    uncertainty: Dict[str, object] | None = None,
) -> StateVersionV1:
    return StateVersionV1(
        state_version_id=version_id,
        field_ref=field_ref,
        field_state_ref=state_ref,
        previous_state_version_ref=previous,
        state_type="accessibility_state",
        state_value={"value": value},
        valid_from=valid_from,
        valid_until=None,
        transition_record_ref=None,
        provenance={"fixture": "temporal_evolution_v1"},
        created_at="2026-01-01T00:00:00Z",
        trace_ref=trace_ref,
        temporal_uncertainty=uncertainty or {},
    )


def shopping_mall_shop_status_history_v1() -> FieldHistoryProjectionV1:
    """Fixed chain: operating -> renovating -> closed."""

    field_ref = "field:shopping_mall:v1"
    trace_ref = "trace:temporal:shopping_mall:v1"
    versions = (
        _version(field_ref, "version:mall:1", "state:mall:1", None, "operating", "2026-01-01T00:00:00Z", trace_ref),
        _version(field_ref, "version:mall:2", "state:mall:2", "version:mall:1", "renovating", "2026-03-01T00:00:00Z", trace_ref),
        _version(field_ref, "version:mall:3", "state:mall:3", "version:mall:2", "closed", "2026-06-01T00:00:00Z", trace_ref),
    )
    transitions = (
        TransitionRecordV1("transition:mall:1", None, "version:mall:1", "event:mall:1", "created", "2026-01-01T00:00:00Z", {"fixture": True}, trace_ref),
        TransitionRecordV1("transition:mall:2", "version:mall:1", "version:mall:2", "event:mall:2", "updated", "2026-03-01T00:00:00Z", {"fixture": True}, trace_ref),
        TransitionRecordV1("transition:mall:3", "version:mall:2", "version:mall:3", "event:mall:3", "updated", "2026-06-01T00:00:00Z", {"fixture": True}, trace_ref),
    )
    return build_field_history_projection_v1(field_ref, versions, transitions, "2026-06-01T00:00:00Z", {"fixture": "shopping_mall"}, trace_ref)


def airport_entrance_status_history_v1() -> FieldHistoryProjectionV1:
    """Fixed chain: open -> restricted -> open."""

    field_ref = "field:airport:v1"
    trace_ref = "trace:temporal:airport:v1"
    versions = (
        _version(field_ref, "version:airport:1", "state:airport:1", None, "open", "2026-01-01T00:00:00Z", trace_ref),
        _version(field_ref, "version:airport:2", "state:airport:2", "version:airport:1", "restricted", "2026-01-01T01:00:00Z", trace_ref),
        _version(field_ref, "version:airport:3", "state:airport:3", "version:airport:2", "open", "2026-01-01T03:00:00Z", trace_ref),
    )
    transitions = (
        TransitionRecordV1("transition:airport:1", None, "version:airport:1", "event:airport:1", "created", "2026-01-01T00:00:00Z", {"fixture": True}, trace_ref),
        TransitionRecordV1("transition:airport:2", "version:airport:1", "version:airport:2", "event:airport:2", "updated", "2026-01-01T01:00:00Z", {"fixture": True}, trace_ref),
        TransitionRecordV1("transition:airport:3", "version:airport:2", "version:airport:3", "event:airport:3", "updated", "2026-01-01T03:00:00Z", {"fixture": True}, trace_ref),
    )
    return build_field_history_projection_v1(field_ref, versions, transitions, "2026-01-01T03:00:00Z", {"fixture": "airport"}, trace_ref)


def incomplete_time_history_v1() -> FieldHistoryProjectionV1:
    """Fixed Unknown / Estimated / Uncertain temporal representation fixture."""

    field_ref = "field:street:v1"
    trace_ref = "trace:temporal:incomplete:v1"
    version = _version(
        field_ref,
        "version:street:1",
        "state:street:1",
        None,
        "closed_candidate",
        None,
        trace_ref,
        {"valid_from_status": "unknown", "valid_until_status": "estimated", "lifecycle": "uncertain"},
    )
    transition = TransitionRecordV1(
        "transition:street:1", None, "version:street:1", "event:street:1", "created", None,
        {"fixture": True, "time_information": "incomplete"}, trace_ref,
        transition_time_status="unknown",
    )
    return build_field_history_projection_v1(field_ref, (version,), (transition,), "2026-01-01T00:00:00Z", {"fixture": "incomplete_time"}, trace_ref)

