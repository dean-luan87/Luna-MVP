from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from capabilities.midplatform.core.field_state_read_model.module import (
    get_default_boundary_flags_v1,
)

from .field_state_read_model_runtime_types_v1 import (
    FieldStateReadRuntimeEnvelopeV1,
    RUNTIME_STATUS_REGISTRY_V1,
)


def classify_runtime_status_v1(
    *,
    request_valid: bool,
    source_status: str,
    read_status: str,
    error_reason: str,
) -> str:
    if error_reason.startswith("runtime_contained:"):
        return "runtime_error_contained"
    if not request_valid:
        return "runtime_rejected"
    if source_status == "source_rejected":
        return "runtime_rejected"
    if source_status in {"candidate_unavailable", "candidate_malformed"}:
        return "runtime_unavailable"
    if read_status == "query_rejected":
        return "runtime_rejected"
    if read_status == "state_unavailable":
        return "runtime_unavailable"
    if read_status in {"partial_projection", "insufficient_state", "stale_state"}:
        return "runtime_partial"
    return "runtime_completed"


def build_runtime_envelope_v1(
    *,
    runtime_request_id: str,
    request_valid: bool,
    source_status: str,
    source_reason: str,
    read_result: Any,
    trace_ref: str,
    replay_key: str,
    runtime_attempted: bool,
    read_api_invoked: bool,
    error_reason: str,
) -> FieldStateReadRuntimeEnvelopeV1:
    read_result_dict = asdict(read_result) if read_result is not None else {}
    read_status = str(read_result_dict.get("read_status") or "")
    boundary_flags = dict(
        read_result_dict.get("boundary_flags") or get_default_boundary_flags_v1()
    )
    runtime_status = classify_runtime_status_v1(
        request_valid=request_valid,
        source_status=source_status,
        read_status=read_status,
        error_reason=error_reason,
    )
    if runtime_status not in RUNTIME_STATUS_REGISTRY_V1:
        runtime_status = "runtime_error_contained"

    return FieldStateReadRuntimeEnvelopeV1(
        runtime_request_id=runtime_request_id,
        runtime_status=runtime_status,
        source_status=source_status,
        read_status=read_status,
        read_result=read_result_dict,
        source_reason=source_reason,
        trace_ref=trace_ref,
        replay_key=replay_key,
        runtime_attempted=runtime_attempted,
        read_api_invoked=read_api_invoked,
        external_io_executed=False,
        state_mutation_executed=False,
        runtime_loop_executed=False,
        candidate_only=True,
        boundary_flags=boundary_flags,
        error_reason=error_reason,
    )
