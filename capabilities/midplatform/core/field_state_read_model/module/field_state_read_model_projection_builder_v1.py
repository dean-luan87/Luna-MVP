from __future__ import annotations

from typing import Any, Dict, Tuple

from .field_state_read_model_module_types_v1 import FieldStateReadProjectionCandidateV1


ALLOWED_TEMPORAL_STATUSES: Tuple[str, ...] = (
    "active",
    "stale",
    "expired",
    "revoked",
    "suspended",
    "superseded",
    "unknown",
)


def _sorted_projection(
    source_payload: Dict[str, Any], required_fields: Tuple[str, ...]
) -> Dict[str, Any]:
    projection: Dict[str, Any] = {}
    for field_name in sorted(required_fields):
        if field_name in source_payload:
            projection[field_name] = source_payload[field_name]
    return projection


def validate_state_candidate_v1(
    *,
    query: Dict[str, Any],
    state_candidate: Dict[str, Any] | None,
) -> Tuple[bool, Tuple[str, ...], Dict[str, Any] | None]:
    if state_candidate is None:
        return False, ("state_candidate_missing",), None

    reasons = []
    source_state_ref = state_candidate.get("source_state_ref")
    state_version = state_candidate.get("state_version")
    state_payload = state_candidate.get("state_payload")
    available_fields = state_candidate.get("available_fields")
    provenance_refs = state_candidate.get("provenance_refs")
    raw_temporal_status = state_candidate.get("temporal_status")
    temporal_status = "unknown" if raw_temporal_status is None else raw_temporal_status
    raw_trace_ref = state_candidate.get("trace_ref")
    trace_ref = "" if raw_trace_ref is None else raw_trace_ref
    raw_replay_key = state_candidate.get("replay_key")
    replay_key = "" if raw_replay_key is None else raw_replay_key

    if not isinstance(source_state_ref, str):
        reasons.append("invalid_source_state_ref_type")
    elif not source_state_ref.strip():
        reasons.append("missing_source_state_ref")
    if not isinstance(state_version, str):
        reasons.append("invalid_state_version_type")
    elif not state_version.strip():
        reasons.append("missing_state_version")
    if not isinstance(temporal_status, str):
        reasons.append("invalid_temporal_status_type")
    if not isinstance(trace_ref, str):
        reasons.append("invalid_trace_ref_type")
    if not isinstance(replay_key, str):
        reasons.append("invalid_replay_key_type")
    if not isinstance(state_payload, dict):
        reasons.append("invalid_state_payload_type")
    if available_fields is not None and not isinstance(available_fields, (list, tuple)):
        reasons.append("invalid_available_fields_type")
    if isinstance(available_fields, (list, tuple)) and any(
        not isinstance(item, str) or not item.strip() for item in available_fields
    ):
        reasons.append("invalid_available_fields_member_type")
    if provenance_refs is not None and not isinstance(provenance_refs, (list, tuple)):
        reasons.append("invalid_provenance_refs_type")
    if isinstance(provenance_refs, (list, tuple)) and any(
        not isinstance(item, str) or not item.strip() for item in provenance_refs
    ):
        reasons.append("invalid_provenance_refs_member_type")
    if temporal_status not in ALLOWED_TEMPORAL_STATUSES:
        reasons.append("unknown_temporal_status")

    query_field_state_ref = str(query.get("field_state_ref") or "")
    query_snapshot_ref = str(query.get("snapshot_ref") or "")
    if (
        query_field_state_ref
        and isinstance(source_state_ref, str)
        and query_field_state_ref != source_state_ref
    ):
        reasons.append("state_ref_mismatch")
    if (
        query_snapshot_ref
        and isinstance(source_state_ref, str)
        and query_snapshot_ref != source_state_ref
    ):
        reasons.append("state_ref_mismatch")
    if (
        trace_ref
        and str(query.get("trace_ref") or "")
        and trace_ref != query.get("trace_ref")
    ):
        reasons.append("trace_ref_mismatch")
    if (
        replay_key
        and str(query.get("replay_key") or "")
        and replay_key != query.get("replay_key")
    ):
        reasons.append("replay_key_mismatch")

    normalized = {
        "source_state_ref": source_state_ref if isinstance(source_state_ref, str) else "",
        "state_version": state_version if isinstance(state_version, str) else "",
        "state_payload": dict(state_payload) if isinstance(state_payload, dict) else {},
        "available_fields": tuple(available_fields)
        if isinstance(available_fields, (list, tuple))
        else tuple(),
        "provenance_refs": tuple(provenance_refs)
        if isinstance(provenance_refs, (list, tuple))
        else tuple(),
        "temporal_status": temporal_status,
        "trace_ref": trace_ref,
        "replay_key": replay_key,
    }
    return len(reasons) == 0, tuple(reasons), normalized


def build_projection_candidate_v1(
    *,
    query: Dict[str, Any],
    state_candidate: Dict[str, Any] | None,
) -> Tuple[
    FieldStateReadProjectionCandidateV1 | None, Tuple[str, ...], Dict[str, Any] | None
]:
    state_valid, state_reasons, normalized_state = validate_state_candidate_v1(
        query=query,
        state_candidate=state_candidate,
    )
    if not state_valid or normalized_state is None:
        return None, state_reasons, normalized_state

    source_state_ref = (
        normalized_state.get("source_state_ref")
        or query.get("field_state_ref")
        or query.get("snapshot_ref")
        or ""
    )
    state_version = normalized_state.get("state_version") or ""
    state_payload = dict(normalized_state.get("state_payload") or {})
    required_fields = tuple(query.get("required_fields") or ())
    available_fields = tuple(
        normalized_state.get("available_fields") or tuple(sorted(state_payload.keys()))
    )
    missing_fields = tuple(
        sorted(field for field in required_fields if field not in state_payload)
    )
    provenance_refs = tuple(normalized_state.get("provenance_refs") or ())
    temporal_status = normalized_state.get("temporal_status") or "unknown"
    trace_ref = normalized_state.get("trace_ref") or query.get("trace_ref") or ""
    replay_key = normalized_state.get("replay_key") or query.get("replay_key") or ""

    projection = _sorted_projection(state_payload, required_fields)

    return (
        FieldStateReadProjectionCandidateV1(
            source_state_ref=source_state_ref,
            state_version=state_version,
            projection=projection,
            available_fields=available_fields,
            missing_fields=missing_fields,
            provenance_refs=provenance_refs,
            temporal_status=temporal_status,
            trace_ref=trace_ref,
            replay_key=replay_key,
        ),
        tuple(),
        normalized_state,
    )
