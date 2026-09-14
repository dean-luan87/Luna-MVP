from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.core.field_state_read_model.module import read_field_state

from .field_state_read_model_controlled_source_adapter_v1 import (
    get_controlled_state_candidate,
)
from .field_state_read_model_runtime_envelope_builder_v1 import (
    build_runtime_envelope_v1,
)
from .field_state_read_model_runtime_types_v1 import RUNTIME_REQUEST_FIELDS_V1


def _to_mapping(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if is_dataclass(value):
        return asdict(value)
    raise TypeError("runtime_request_must_be_mapping_or_dataclass")


def validate_runtime_request_v1(
    runtime_request: Any,
) -> Tuple[bool, Tuple[str, ...], Dict[str, Any]]:
    candidate = _to_mapping(runtime_request)
    reasons = []
    unknown_fields = sorted(set(candidate.keys()) - set(RUNTIME_REQUEST_FIELDS_V1))
    if unknown_fields:
        reasons.append("unknown_runtime_field")

    if not str(candidate.get("runtime_request_id", "")):
        reasons.append("missing_runtime_request_id")
    if not isinstance(candidate.get("query"), dict):
        reasons.append("invalid_runtime_query_type")
    if not isinstance(candidate.get("source_request"), dict):
        reasons.append("invalid_runtime_source_request_type")
    if not str(candidate.get("trace_ref", "")):
        reasons.append("missing_runtime_trace_ref")
    if not str(candidate.get("replay_key", "")):
        reasons.append("missing_runtime_replay_key")
    if not isinstance(candidate.get("metadata", {}), dict):
        reasons.append("invalid_runtime_metadata_type")

    query = (
        dict(candidate.get("query") or {})
        if isinstance(candidate.get("query"), dict)
        else {}
    )
    source_request = (
        dict(candidate.get("source_request") or {})
        if isinstance(candidate.get("source_request"), dict)
        else {}
    )
    runtime_trace_ref = str(candidate.get("trace_ref", ""))
    runtime_replay_key = str(candidate.get("replay_key", ""))

    if (
        query
        and runtime_trace_ref
        and str(query.get("trace_ref") or "") != runtime_trace_ref
    ):
        reasons.append("trace_mismatch_runtime_query")
    if (
        query
        and runtime_replay_key
        and str(query.get("replay_key") or "") != runtime_replay_key
    ):
        reasons.append("replay_mismatch_runtime_query")
    if (
        source_request
        and runtime_trace_ref
        and str(source_request.get("trace_ref") or "") != runtime_trace_ref
    ):
        reasons.append("trace_mismatch_runtime_source")
    if (
        source_request
        and runtime_replay_key
        and str(source_request.get("replay_key") or "") != runtime_replay_key
    ):
        reasons.append("replay_mismatch_runtime_source")

    normalized = {
        "runtime_request_id": str(candidate.get("runtime_request_id", "")),
        "query": query,
        "source_request": source_request,
        "trace_ref": runtime_trace_ref,
        "replay_key": runtime_replay_key,
        "metadata": dict(candidate.get("metadata"))
        if isinstance(candidate.get("metadata"), dict)
        else {},
    }
    return len(reasons) == 0, tuple(reasons), normalized


def run_controlled_read_runtime(runtime_request: Any):
    try:
        request_valid, reasons, normalized = validate_runtime_request_v1(
            runtime_request
        )
        runtime_request_id = str(normalized.get("runtime_request_id") or "")
        trace_ref = str(normalized.get("trace_ref") or "")
        replay_key = str(normalized.get("replay_key") or "")

        if not request_valid:
            return build_runtime_envelope_v1(
                runtime_request_id=runtime_request_id,
                request_valid=False,
                source_status="source_rejected",
                source_reason=",".join(reasons),
                read_result=None,
                trace_ref=trace_ref,
                replay_key=replay_key,
                runtime_attempted=False,
                read_api_invoked=False,
                error_reason=",".join(reasons),
            )

        source_result = get_controlled_state_candidate(normalized["source_request"])
        source_status = source_result.source_status
        source_reason = source_result.source_reason

        if source_status == "source_rejected":
            return build_runtime_envelope_v1(
                runtime_request_id=runtime_request_id,
                request_valid=True,
                source_status=source_status,
                source_reason=source_reason,
                read_result=None,
                trace_ref=trace_ref,
                replay_key=replay_key,
                runtime_attempted=False,
                read_api_invoked=False,
                error_reason=source_reason,
            )

        read_result = read_field_state(
            normalized["query"], source_result.state_candidate
        )
        return build_runtime_envelope_v1(
            runtime_request_id=runtime_request_id,
            request_valid=True,
            source_status=source_status,
            source_reason=source_reason,
            read_result=read_result,
            trace_ref=trace_ref,
            replay_key=replay_key,
            runtime_attempted=True,
            read_api_invoked=True,
            error_reason="",
        )
    except Exception as exc:
        fallback = (
            _to_mapping(runtime_request) if isinstance(runtime_request, dict) else {}
        )
        return build_runtime_envelope_v1(
            runtime_request_id=str(fallback.get("runtime_request_id") or ""),
            request_valid=True,
            source_status="source_rejected",
            source_reason="",
            read_result=None,
            trace_ref=str(fallback.get("trace_ref") or ""),
            replay_key=str(fallback.get("replay_key") or ""),
            runtime_attempted=True,
            read_api_invoked=False,
            error_reason=f"runtime_contained:{type(exc).__name__}",
        )
