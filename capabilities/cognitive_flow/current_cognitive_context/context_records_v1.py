"""Traceable inclusion and exclusion records for Current Cognitive Context v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from .context_types_v1 import (
    CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1,
    ContextExclusionReasonV1,
)


@dataclass(frozen=True)
class ContextInclusionRecordV1:
    record_id: str
    source_ref: str
    selected_object_ref: str
    inclusion_reason: str
    relevance_scope: str
    priority: str
    supporting_evidence_refs: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class ContextExclusionRecordV1:
    record_id: str
    source_ref: str
    excluded_object_ref: str
    exclusion_reason: str
    excluded_for_current_context_only: bool
    recoverable: bool
    source_snapshot_ref: str
    provenance: Mapping[str, Any]
    trace: str
    schema_version: str = CURRENT_COGNITIVE_CONTEXT_SCHEMA_VERSION_V1

    def __post_init__(self) -> None:
        allowed = {reason.value for reason in ContextExclusionReasonV1}
        if self.exclusion_reason not in allowed:
            raise ValueError("unsupported Context Exclusion Record reason")
        if not self.excluded_for_current_context_only:
            raise ValueError("Context exclusion must remain current-context-only")
        if not self.recoverable:
            raise ValueError("Context exclusion must preserve recoverable source access")
        if not self.source_ref or not self.source_snapshot_ref:
            raise ValueError("Context exclusion requires source references")
