"""Fail-closed classification for runtime side-effect evidence."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


DECLARED_NOT_EXECUTED = "DECLARED_NOT_EXECUTED"
REQUEST_NOT_ISSUED = "REQUEST_NOT_ISSUED"
CONTROLLED_PATH_NOT_EXECUTED = "CONTROLLED_PATH_NOT_EXECUTED"
OBSERVED_NOT_EXECUTED = "OBSERVED_NOT_EXECUTED"
CONTROLLED_WITHHOLD = "CONTROLLED_WITHHOLD"
UNKNOWN = "UNKNOWN"


_INDEPENDENT_OBSERVATION_AUTHORITY = object()


@dataclass(frozen=True)
class IndependentSideEffectObservation:
    """Typed boundary for a genuinely separate observation authority.

    The private marker is intentionally unavailable to producer mappings. No
    current Luna producer can construct this authority, so producer artifacts
    cannot manufacture OBSERVED_NOT_EXECUTED by setting fields.
    """

    status: str
    authority_ref: str
    evidence_refs: tuple[str, ...]
    _authority: object = field(default=None, repr=False, compare=False)


def classify_side_effect_map(value: Any) -> str:
    """Classify producer-side flags without upgrading them to observation."""
    if not isinstance(value, Mapping) or not value:
        return UNKNOWN
    statuses = tuple(value.values())
    if any(not isinstance(status, str) for status in statuses):
        return UNKNOWN
    if all(status == OBSERVED_NOT_EXECUTED for status in statuses):
        return CONTROLLED_WITHHOLD
    if all(status == DECLARED_NOT_EXECUTED for status in statuses):
        return DECLARED_NOT_EXECUTED
    if all(status == REQUEST_NOT_ISSUED for status in statuses):
        return REQUEST_NOT_ISSUED
    if all(status == CONTROLLED_PATH_NOT_EXECUTED for status in statuses):
        return CONTROLLED_PATH_NOT_EXECUTED
    return UNKNOWN


def classify_producer_record(value: Any) -> str:
    """Classify producer declarations without upgrading them to observation."""
    if not isinstance(value, Mapping):
        return UNKNOWN
    status = value.get("status")
    if status == OBSERVED_NOT_EXECUTED:
        return CONTROLLED_WITHHOLD
    if status in {
        DECLARED_NOT_EXECUTED,
        REQUEST_NOT_ISSUED,
        CONTROLLED_PATH_NOT_EXECUTED,
        CONTROLLED_WITHHOLD,
    }:
        return status
    return UNKNOWN


def classify_independent_observation(value: Any) -> str:
    """Classify only a separately typed observation authority.

    This API is deliberately unusable by ordinary artifact mappings. It is
    retained for a future externally supplied observer and has no current
    producer caller.
    """
    if not isinstance(value, IndependentSideEffectObservation):
        return UNKNOWN
    if value._authority is not _INDEPENDENT_OBSERVATION_AUTHORITY:
        return CONTROLLED_WITHHOLD
    if value.status != OBSERVED_NOT_EXECUTED or not value.authority_ref or not value.evidence_refs:
        return CONTROLLED_WITHHOLD
    return OBSERVED_NOT_EXECUTED


def classify_observer_record(value: Any) -> str:
    """Backward-compatible name for producer-side classification."""
    return classify_producer_record(value)


__all__ = [
    "CONTROLLED_PATH_NOT_EXECUTED",
    "CONTROLLED_WITHHOLD",
    "DECLARED_NOT_EXECUTED",
    "OBSERVED_NOT_EXECUTED",
    "REQUEST_NOT_ISSUED",
    "UNKNOWN",
    "IndependentSideEffectObservation",
    "classify_independent_observation",
    "classify_observer_record",
    "classify_producer_record",
    "classify_side_effect_map",
]
