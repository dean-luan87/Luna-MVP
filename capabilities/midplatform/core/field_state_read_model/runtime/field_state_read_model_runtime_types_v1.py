from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Tuple


SOURCE_MODE_REGISTRY_V1: Tuple[str, ...] = (
    "candidate_available",
    "candidate_unavailable",
    "candidate_malformed",
    "source_rejected",
)

RUNTIME_STATUS_REGISTRY_V1: Tuple[str, ...] = (
    "runtime_completed",
    "runtime_partial",
    "runtime_unavailable",
    "runtime_rejected",
    "runtime_error_contained",
)

RUNTIME_REQUEST_FIELDS_V1: Tuple[str, ...] = (
    "runtime_request_id",
    "query",
    "source_request",
    "trace_ref",
    "replay_key",
    "metadata",
)

SOURCE_REQUEST_FIELDS_V1: Tuple[str, ...] = (
    "source_request_id",
    "requested_state_ref",
    "requested_snapshot_ref",
    "trace_ref",
    "replay_key",
    "source_mode",
    "controlled_payload",
)

RUNTIME_ENVELOPE_FIELDS_V1: Tuple[str, ...] = (
    "runtime_request_id",
    "runtime_status",
    "source_status",
    "read_status",
    "read_result",
    "source_reason",
    "trace_ref",
    "replay_key",
    "runtime_attempted",
    "read_api_invoked",
    "external_io_executed",
    "state_mutation_executed",
    "runtime_loop_executed",
    "candidate_only",
    "boundary_flags",
    "error_reason",
)


@dataclass(frozen=True)
class ControlledStateSourceRequestV1:
    source_request_id: str
    requested_state_ref: str | None
    requested_snapshot_ref: str | None
    trace_ref: str
    replay_key: str
    source_mode: str
    controlled_payload: Dict[str, Any]


@dataclass(frozen=True)
class ControlledStateSourceResultV1:
    source_request_id: str
    source_status: str
    state_candidate: Dict[str, Any] | None
    source_reason: str
    trace_ref: str
    replay_key: str
    runtime_source_connected: bool = False
    external_io_executed: bool = False
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldStateReadRuntimeRequestV1:
    runtime_request_id: str
    query: Dict[str, Any]
    source_request: Dict[str, Any]
    trace_ref: str
    replay_key: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class FieldStateReadRuntimeEnvelopeV1:
    runtime_request_id: str
    runtime_status: str
    source_status: str
    read_status: str
    read_result: Dict[str, Any]
    source_reason: str
    trace_ref: str
    replay_key: str
    runtime_attempted: bool
    read_api_invoked: bool
    external_io_executed: bool
    state_mutation_executed: bool
    runtime_loop_executed: bool
    candidate_only: bool
    boundary_flags: Dict[str, bool]
    error_reason: str = ""
