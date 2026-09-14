from __future__ import annotations

from typing import Any, Dict, Tuple

from .field_state_read_model_module_types_v1 import (
    FieldStateReadProjectionCandidateV1,
    FieldStateReadResultV1,
    READ_STATUS_REGISTRY_V1,
    get_default_boundary_flags_v1,
)


def classify_read_status_v1(
    *,
    query_valid: bool,
    state_candidate: Dict[str, Any] | None,
    state_validation_reasons: Tuple[str, ...],
    projection_candidate: FieldStateReadProjectionCandidateV1 | None,
) -> Tuple[str, str, str, str]:
    if not query_valid:
        return "query_rejected", "", "", "invalid_query"

    if state_candidate is None or state_validation_reasons:
        return "state_unavailable", "", "", ""

    temporal_status = str(
        (projection_candidate.temporal_status if projection_candidate else "unknown")
        or "unknown"
    )
    if temporal_status in {"stale", "expired", "revoked", "suspended", "superseded"}:
        return "stale_state", temporal_status, "", ""

    if projection_candidate is None:
        return "state_unavailable", "", "", ""

    available_count = len(projection_candidate.projection)
    required_count = len(tuple(projection_candidate.projection.keys())) + len(
        projection_candidate.missing_fields
    )

    if available_count == 0:
        return "insufficient_state", "", "required_fields_unavailable", ""

    if len(projection_candidate.missing_fields) > 0:
        return "partial_projection", "", "", ""

    if required_count >= 0:
        return "read_ready", "", "", ""

    return "state_unavailable", "", "", ""


def build_result_v1(
    *,
    query: Dict[str, Any],
    query_valid: bool,
    rejection_reasons: Tuple[str, ...],
    state_candidate: Dict[str, Any] | None,
    state_validation_reasons: Tuple[str, ...],
    projection_candidate: FieldStateReadProjectionCandidateV1 | None,
) -> FieldStateReadResultV1:
    read_status, stale_reason, insufficiency_reason, default_rejection_reason = (
        classify_read_status_v1(
            query_valid=query_valid,
            state_candidate=state_candidate,
            state_validation_reasons=state_validation_reasons,
            projection_candidate=projection_candidate,
        )
    )

    if read_status not in READ_STATUS_REGISTRY_V1:
        read_status = "query_rejected"

    boundary_flags = get_default_boundary_flags_v1()
    rejection_reason = default_rejection_reason
    if rejection_reasons:
        rejection_reason = ",".join(rejection_reasons)
    elif state_validation_reasons:
        rejection_reason = ",".join(state_validation_reasons)

    if projection_candidate is None:
        projection: Dict[str, Any] = {}
        source_state_ref = str(
            query.get("field_state_ref") or query.get("snapshot_ref") or ""
        )
        state_version = ""
        provenance_refs: Tuple[str, ...] = tuple()
        trace_ref = str(query.get("trace_ref") or "")
        replay_key = str(query.get("replay_key") or "")
    else:
        projection = dict(projection_candidate.projection)
        projection["missing_fields"] = list(projection_candidate.missing_fields)
        source_state_ref = projection_candidate.source_state_ref
        state_version = projection_candidate.state_version
        provenance_refs = projection_candidate.provenance_refs
        trace_ref = projection_candidate.trace_ref
        replay_key = projection_candidate.replay_key

    module_status = "completed_candidate"
    if read_status == "query_rejected":
        module_status = "rejected_input"
    elif read_status == "state_unavailable":
        module_status = "unavailable_candidate"
    elif read_status == "stale_state":
        module_status = "stale_candidate"
    elif read_status == "insufficient_state":
        module_status = "insufficient_candidate"
    elif read_status == "partial_projection":
        module_status = "partial_candidate"

    return FieldStateReadResultV1(
        query_id=str(query.get("query_id") or ""),
        read_status=read_status,
        projection=projection,
        state_version=state_version,
        source_state_ref=source_state_ref,
        provenance_refs=provenance_refs,
        trace_ref=trace_ref,
        replay_key=replay_key,
        stale_reason=stale_reason,
        insufficiency_reason=insufficiency_reason,
        rejection_reason=rejection_reason,
        boundary_flags=boundary_flags,
        module_status=module_status,
        runtime_executed=False,
    )
