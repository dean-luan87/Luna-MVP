"""Read-only Field History Projection assembly for Temporal Evolution v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Tuple

from .state_version_v1 import StateVersionV1, TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1
from .transition_record_v1 import TransitionRecordV1


@dataclass(frozen=True)
class TimelineEntryV1:
    sequence: int
    entry_type: str
    entry_ref: str
    recorded_time: str | None
    time_status: str
    provenance: Mapping[str, Any]
    schema_version: str = TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class FieldHistoryProjectionV1:
    """A descriptive, immutable history view for one Field.

    Input order is preserved deliberately: unknown or estimated time must not
    be silently sorted into a fabricated chronology.
    """

    field_ref: str
    state_versions: Tuple[StateVersionV1, ...]
    transitions: Tuple[TransitionRecordV1, ...]
    timeline: Tuple[TimelineEntryV1, ...]
    provenance: Mapping[str, Any]
    snapshot_time: str
    trace_ref: str
    schema_version: str = TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1
    read_only: bool = True
    state_mutation_executed: bool = False


def build_field_history_projection_v1(
    field_ref: str,
    state_versions: Iterable[StateVersionV1],
    transitions: Iterable[TransitionRecordV1],
    snapshot_time: str,
    provenance: Mapping[str, Any],
    trace_ref: str,
) -> FieldHistoryProjectionV1:
    """Build a read-only projection without sorting, mutation, or I/O."""

    versions = tuple(version for version in state_versions if version.field_ref == field_ref)
    records = tuple(transitions)
    version_refs = {version.state_version_id for version in versions}
    records = tuple(
        record
        for record in records
        if record.target_state_version in version_refs
        or record.source_state_version in version_refs
    )

    timeline = []
    for version in versions:
        timeline.append(
            TimelineEntryV1(
                sequence=len(timeline),
                entry_type="state_version",
                entry_ref=version.state_version_id,
                recorded_time=version.valid_from,
                time_status=str(version.temporal_uncertainty.get("valid_from_status", "known")),
                provenance={"state_version_provenance": dict(version.provenance)},
            )
        )
    for record in records:
        timeline.append(
            TimelineEntryV1(
                sequence=len(timeline),
                entry_type="transition_record",
                entry_ref=record.transition_id,
                recorded_time=record.transition_time,
                time_status=record.transition_time_status,
                provenance={"transition_provenance": dict(record.provenance)},
            )
        )

    projection_provenance = dict(provenance)
    projection_provenance.setdefault("input_order_preserved", True)
    projection_provenance.setdefault("history_is_not_experience", True)
    return FieldHistoryProjectionV1(
        field_ref=field_ref,
        state_versions=versions,
        transitions=records,
        timeline=tuple(timeline),
        provenance=projection_provenance,
        snapshot_time=snapshot_time,
        trace_ref=trace_ref,
    )

