"""Governed State Version transition record for Temporal Evolution v1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .state_version_v1 import TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1


class TransitionTypeV1(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    EXPIRED = "expired"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class TransitionRecordV1:
    """A descriptive record of an already governed State-version transition.

    `event_ref` is the admitted-event or governed expiry/archival event source
    reference. It records a source boundary only; it must not be interpreted as
    an explanation of why the transition happened.
    """

    transition_id: str
    source_state_version: str | None
    target_state_version: str
    event_ref: str
    transition_type: str
    transition_time: str | None
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1
    transition_time_status: str = "known"
    causes_asserted: bool = False
    state_mutation_executed: bool = False

    def __post_init__(self) -> None:
        allowed = {item.value for item in TransitionTypeV1}
        if self.transition_type not in allowed:
            raise ValueError("unsupported State Version transition_type")
        if not self.transition_id or not self.target_state_version or not self.event_ref:
            raise ValueError("TransitionRecordV1 requires transition, target, and event references")
        if not self.trace_ref:
            raise ValueError("TransitionRecordV1 requires trace_ref")
        if self.transition_type == TransitionTypeV1.CREATED.value:
            if self.source_state_version is not None:
                raise ValueError("created transition must not have a source State Version")
        elif not self.source_state_version:
            raise ValueError("non-created transition requires source State Version")

