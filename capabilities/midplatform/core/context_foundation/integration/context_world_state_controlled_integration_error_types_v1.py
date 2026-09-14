"""Integration-level errors; downstream owner namespaces remain authoritative."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


ERROR_CODES = (
    "INVALID_OBSERVATION_HANDOFF",
    "MISSING_PROVENANCE",
    "MISSING_TEMPORAL_VALIDITY",
    "FIELD_EVENT_ADMISSION_REQUIRED",
    "DUPLICATE_OBSERVATION_HANDOFF",
    "DUPLICATE_FIELD_EVENT",
    "DUPLICATE_CONTEXT_UPDATE",
    "DUPLICATE_CURRENT_WORLD",
    "CONTEXT_FIELD_MUTATION_FORBIDDEN",
    "CURRENT_WORLD_FIELD_TRUTH_FORBIDDEN",
    "SECOND_FIELD_WRITER_FORBIDDEN",
    "SOURCE_REVOCATION",
    "TEMPORAL_INVALIDATION",
)


@dataclass(frozen=True)
class ContextWorldIntegrationErrorV1:
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
) -> ContextWorldIntegrationErrorV1:
    return ContextWorldIntegrationErrorV1(
        code=code,
        message=message,
        source_refs=source_refs,
        trace_ref=trace_ref,
        terminal=terminal,
    )
