from __future__ import annotations

import copy
from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Tuple

from .field_state_read_model_runtime_types_v1 import (
    ControlledStateSourceResultV1,
    SOURCE_MODE_REGISTRY_V1,
    SOURCE_REQUEST_FIELDS_V1,
)


def _to_mapping(source_request: Any) -> Dict[str, Any]:
    if isinstance(source_request, dict):
        return dict(source_request)
    if is_dataclass(source_request):
        return asdict(source_request)
    raise TypeError("source_request_must_be_mapping_or_dataclass")


def validate_source_request_v1(
    source_request: Any,
) -> Tuple[bool, Tuple[str, ...], Dict[str, Any]]:
    candidate = _to_mapping(source_request)
    reasons = []
    unknown_fields = sorted(set(candidate.keys()) - set(SOURCE_REQUEST_FIELDS_V1))
    if unknown_fields:
        reasons.append("unknown_source_request_field")

    for field_name in ("source_request_id", "trace_ref", "replay_key", "source_mode"):
        if not str(candidate.get(field_name, "")):
            reasons.append(f"missing_{field_name}")

    source_mode = str(candidate.get("source_mode", ""))
    if source_mode not in SOURCE_MODE_REGISTRY_V1:
        reasons.append("invalid_source_mode")

    controlled_payload = candidate.get("controlled_payload")
    if not isinstance(controlled_payload, dict):
        reasons.append("invalid_controlled_payload_type")

    normalized = {
        "source_request_id": str(candidate.get("source_request_id", "")),
        "requested_state_ref": str(candidate.get("requested_state_ref"))
        if candidate.get("requested_state_ref") is not None
        else None,
        "requested_snapshot_ref": str(candidate.get("requested_snapshot_ref"))
        if candidate.get("requested_snapshot_ref") is not None
        else None,
        "trace_ref": str(candidate.get("trace_ref", "")),
        "replay_key": str(candidate.get("replay_key", "")),
        "source_mode": source_mode,
        "controlled_payload": copy.deepcopy(controlled_payload)
        if isinstance(controlled_payload, dict)
        else {},
    }
    return len(reasons) == 0, tuple(reasons), normalized


def get_controlled_state_candidate(
    source_request: Any,
) -> ControlledStateSourceResultV1:
    valid, reasons, normalized = validate_source_request_v1(source_request)
    if not valid:
        return ControlledStateSourceResultV1(
            source_request_id=str(normalized.get("source_request_id") or ""),
            source_status="source_rejected",
            state_candidate=None,
            source_reason=",".join(reasons),
            trace_ref=str(normalized.get("trace_ref") or ""),
            replay_key=str(normalized.get("replay_key") or ""),
            runtime_source_connected=False,
            external_io_executed=False,
            candidate_only=True,
        )

    payload = copy.deepcopy(normalized.get("controlled_payload") or {})
    if payload.get("force_adapter_exception") is True:
        raise ValueError("controlled_source_adapter_exception")

    source_mode = str(normalized.get("source_mode") or "")
    state_candidate = copy.deepcopy(payload.get("state_candidate"))
    source_reason = ""

    if source_mode == "candidate_available":
        source_status = "candidate_available"
    elif source_mode == "candidate_unavailable":
        source_status = "candidate_unavailable"
        state_candidate = None
        source_reason = "candidate_not_available"
    elif source_mode == "candidate_malformed":
        source_status = "candidate_malformed"
        source_reason = "candidate_payload_malformed"
    else:
        source_status = "source_rejected"
        state_candidate = None
        source_reason = str(payload.get("source_reason") or "source_request_rejected")

    return ControlledStateSourceResultV1(
        source_request_id=str(normalized.get("source_request_id") or ""),
        source_status=source_status,
        state_candidate=state_candidate,
        source_reason=source_reason,
        trace_ref=str(normalized.get("trace_ref") or ""),
        replay_key=str(normalized.get("replay_key") or ""),
        runtime_source_connected=False,
        external_io_executed=False,
        candidate_only=True,
    )
