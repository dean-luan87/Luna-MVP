from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


ERROR_CODES = (
    "INVALID_DEMAND",
    "INVALID_REQUEST",
    "INVALID_CAPABILITY_REQUIREMENT",
    "DUPLICATE_DEMAND",
    "DUPLICATE_REQUEST",
    "DUPLICATE_CAPABILITY_REQUIREMENT",
    "DUPLICATE_PROVIDER_SESSION",
    "DUPLICATE_EVIDENCE_FEEDBACK",
    "DUPLICATE_SUFFICIENCY_ADJUDICATION",
    "DUPLICATE_REDIRECT",
    "DUPLICATE_SWITCH",
    "REPEATED_PROVIDER_FAILURE_SIGNATURE",
    "RECONSIDERATION_DEPTH_EXCEEDED",
    "COMPLETED_OBSERVATION_IMMUTABLE",
    "PROVIDER_AUTONOMY_VIOLATION",
    "CONTRACT_MISMATCH",
    "VERSION_MISMATCH",
)


@dataclass(frozen=True)
class ActiveObservationControlErrorV1:
    code: str
    message: str
    source_refs: Tuple[str, ...]
    trace_ref: str
    terminal: bool = False


def make_error(
    code: str,
    message: str,
    source_refs: Tuple[str, ...],
    trace_ref: str,
    terminal: bool = False,
) -> ActiveObservationControlErrorV1:
    return ActiveObservationControlErrorV1(
        code=code,
        message=message,
        source_refs=source_refs,
        trace_ref=trace_ref,
        terminal=terminal,
    )
