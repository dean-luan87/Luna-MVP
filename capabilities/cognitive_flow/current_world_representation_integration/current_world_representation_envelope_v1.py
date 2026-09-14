"""Read-only reference envelope for the CWR integration DryRun v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from .integration_types_v1 import INTEGRATION_SCHEMA_VERSION_V1


_REPRESENTATION_STATUSES_V1 = {
    "complete",
    "incomplete",
    "stale",
    "unavailable",
    "permission_restricted",
    "unknown",
}


@dataclass(frozen=True)
class CurrentWorldRepresentationEnvelopeV1:
    """Immutable cross-module references; it owns neither State nor behavior."""

    schema_version: str
    representation_id: str
    field_ref: str
    field_identity_ref: str
    field_structure_refs: Tuple[str, ...]
    current_state_refs: Tuple[str, ...]
    state_version_refs: Tuple[str, ...]
    history_projection_ref: str | None
    snapshot_ref: str | None
    context_refs: Tuple[str, ...]
    active_context_ref: str | None
    source_event_refs: Tuple[str, ...]
    source_evidence_refs: Tuple[str, ...]
    temporal_scope: Mapping[str, Any]
    representation_status: str
    incomplete_reason_codes: Tuple[str, ...]
    provenance: Mapping[str, Any]
    trace: str
    read_only: bool = True
    state_mutation_executed: bool = False
    hypothesis_output_present: bool = False
    decision_output_present: bool = False

    def __post_init__(self) -> None:
        if self.schema_version != INTEGRATION_SCHEMA_VERSION_V1:
            raise ValueError("unsupported CWR Envelope schema_version")
        if self.representation_status not in _REPRESENTATION_STATUSES_V1:
            raise ValueError("unsupported CWR Envelope representation_status")
        if self.active_context_ref is not None and self.active_context_ref not in self.context_refs:
            raise ValueError("active_context_ref must be present in context_refs")
        if not self.representation_id or not self.field_ref or not self.field_identity_ref:
            raise ValueError("CWR Envelope requires stable representation and Field references")
        if not self.trace:
            raise ValueError("CWR Envelope requires trace")
