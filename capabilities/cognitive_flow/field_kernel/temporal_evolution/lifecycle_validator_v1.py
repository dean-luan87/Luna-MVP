"""Pure lifecycle validation for Field Temporal Evolution v1."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .state_version_v1 import TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1
from .transition_record_v1 import TransitionRecordV1, TransitionTypeV1


class StateLifecycleStatusV1(str, Enum):
    CREATED = "created"
    ACTIVE = "active"
    UPDATED = "updated"
    UNCERTAIN = "uncertain"
    EXPIRED = "expired"
    ARCHIVED = "archived"


class LifecycleReasonCodeV1(str, Enum):
    VALID = "TEMPORAL_LIFECYCLE_VALID"
    SOURCE_REQUIRED = "TEMPORAL_LIFECYCLE_SOURCE_REQUIRED"
    EVENT_SOURCE_REQUIRED = "TEMPORAL_LIFECYCLE_EVENT_SOURCE_REQUIRED"
    CREATED_SOURCE_FORBIDDEN = "TEMPORAL_LIFECYCLE_CREATED_SOURCE_FORBIDDEN"
    ARCHIVED_TERMINAL = "TEMPORAL_LIFECYCLE_ARCHIVED_TERMINAL"
    EXPIRED_UPDATE_FORBIDDEN = "TEMPORAL_LIFECYCLE_EXPIRED_UPDATE_FORBIDDEN"
    TRANSITION_NOT_ALLOWED = "TEMPORAL_LIFECYCLE_TRANSITION_NOT_ALLOWED"
    TRANSITION_TYPE_MISMATCH = "TEMPORAL_LIFECYCLE_TRANSITION_TYPE_MISMATCH"


@dataclass(frozen=True)
class LifecycleValidationResultV1:
    """A deterministic validation outcome; it does not alter lifecycle state."""

    validation_result: bool
    reason_code: str
    source_lifecycle: str | None
    target_lifecycle: str
    transition_ref: str
    provenance: Mapping[str, Any]
    trace_ref: str
    schema_version: str = TEMPORAL_EVOLUTION_SCHEMA_VERSION_V1


_ALLOWED_TRANSITIONS_V1 = {
    (None, StateLifecycleStatusV1.CREATED.value),
    (StateLifecycleStatusV1.CREATED.value, StateLifecycleStatusV1.ACTIVE.value),
    (StateLifecycleStatusV1.CREATED.value, StateLifecycleStatusV1.UNCERTAIN.value),
    (StateLifecycleStatusV1.ACTIVE.value, StateLifecycleStatusV1.UPDATED.value),
    (StateLifecycleStatusV1.ACTIVE.value, StateLifecycleStatusV1.UNCERTAIN.value),
    (StateLifecycleStatusV1.ACTIVE.value, StateLifecycleStatusV1.EXPIRED.value),
    (StateLifecycleStatusV1.UNCERTAIN.value, StateLifecycleStatusV1.ACTIVE.value),
    (StateLifecycleStatusV1.UNCERTAIN.value, StateLifecycleStatusV1.EXPIRED.value),
    (StateLifecycleStatusV1.UPDATED.value, StateLifecycleStatusV1.ARCHIVED.value),
    (StateLifecycleStatusV1.EXPIRED.value, StateLifecycleStatusV1.ARCHIVED.value),
}


def validate_lifecycle_transition_v1(
    source_lifecycle: str | None,
    target_lifecycle: str,
    transition: TransitionRecordV1,
    provenance: Mapping[str, Any],
    trace_ref: str,
) -> LifecycleValidationResultV1:
    """Validate a planned State lifecycle transition without changing State.

    No system clock, Reducer, admission API, persistence, model, or external
    service is used. `created` is the sole transition with no source version.
    """

    result_provenance = dict(provenance)
    result_provenance.setdefault("transition_provenance", dict(transition.provenance))

    def result(valid: bool, code: LifecycleReasonCodeV1) -> LifecycleValidationResultV1:
        return LifecycleValidationResultV1(
            validation_result=valid,
            reason_code=code.value,
            source_lifecycle=source_lifecycle,
            target_lifecycle=target_lifecycle,
            transition_ref=transition.transition_id,
            provenance=result_provenance,
            trace_ref=trace_ref,
        )

    if not transition.event_ref:
        return result(False, LifecycleReasonCodeV1.EVENT_SOURCE_REQUIRED)
    if transition.transition_type == TransitionTypeV1.CREATED.value:
        if transition.source_state_version is not None or source_lifecycle is not None:
            return result(False, LifecycleReasonCodeV1.CREATED_SOURCE_FORBIDDEN)
    elif not transition.source_state_version:
        return result(False, LifecycleReasonCodeV1.SOURCE_REQUIRED)

    if source_lifecycle == StateLifecycleStatusV1.ARCHIVED.value:
        return result(False, LifecycleReasonCodeV1.ARCHIVED_TERMINAL)
    if (
        source_lifecycle == StateLifecycleStatusV1.EXPIRED.value
        and target_lifecycle == StateLifecycleStatusV1.UPDATED.value
    ):
        return result(False, LifecycleReasonCodeV1.EXPIRED_UPDATE_FORBIDDEN)
    if (source_lifecycle, target_lifecycle) not in _ALLOWED_TRANSITIONS_V1:
        return result(False, LifecycleReasonCodeV1.TRANSITION_NOT_ALLOWED)

    expected_type = {
        (None, StateLifecycleStatusV1.CREATED.value): TransitionTypeV1.CREATED.value,
        (StateLifecycleStatusV1.ACTIVE.value, StateLifecycleStatusV1.UPDATED.value): TransitionTypeV1.UPDATED.value,
        (StateLifecycleStatusV1.ACTIVE.value, StateLifecycleStatusV1.EXPIRED.value): TransitionTypeV1.EXPIRED.value,
        (StateLifecycleStatusV1.UNCERTAIN.value, StateLifecycleStatusV1.EXPIRED.value): TransitionTypeV1.EXPIRED.value,
        (StateLifecycleStatusV1.UPDATED.value, StateLifecycleStatusV1.ARCHIVED.value): TransitionTypeV1.ARCHIVED.value,
        (StateLifecycleStatusV1.EXPIRED.value, StateLifecycleStatusV1.ARCHIVED.value): TransitionTypeV1.ARCHIVED.value,
    }.get((source_lifecycle, target_lifecycle))
    if expected_type is not None and transition.transition_type != expected_type:
        return result(False, LifecycleReasonCodeV1.TRANSITION_TYPE_MISMATCH)
    return result(True, LifecycleReasonCodeV1.VALID)

