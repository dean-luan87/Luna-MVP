from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _base_query(
    case_id: str,
    required_fields: Tuple[str, ...] = ("status", "entities"),
) -> Dict[str, Any]:
    return {
        "query_id": f"query_{case_id}",
        "requester_ref": "contract_dryrun",
        "query_scope": "field_state",
        "field_state_ref": f"state_ref_{case_id}",
        "snapshot_ref": None,
        "task_ref": None,
        "scene_ref": None,
        "object_ref": None,
        "temporal_scope": None,
        "required_fields": list(required_fields),
        "trace_ref": f"trace_{case_id}",
        "replay_key": f"replay_{case_id}",
        "metadata": {"case_id": case_id},
    }


def _base_state(case_id: str) -> Dict[str, Any]:
    return {
        "source_state_ref": f"state_ref_{case_id}",
        "state_version": "v1",
        "state_payload": {
            "confidence": 0.92,
            "entities": ["pedestrian", "road"],
            "region": "front_corridor",
            "status": "active",
        },
        "available_fields": ["confidence", "entities", "region", "status"],
        "provenance_refs": [f"prov_{case_id}_1", f"prov_{case_id}_2"],
        "temporal_status": "active",
        "trace_ref": f"trace_{case_id}",
        "replay_key": f"replay_{case_id}",
    }


def _case(
    case_id: str,
    expected_status: str,
    *,
    query: Dict[str, Any],
    state_candidate: Dict[str, Any] | None,
    expected_rejection_contains: Tuple[str, ...] = tuple(),
    expected_projection_keys: Tuple[str, ...] = tuple(),
    expected_missing_fields: Tuple[str, ...] = tuple(),
    expected_provenance_refs: Tuple[str, ...] = tuple(),
) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "expected_status": expected_status,
        "query": query,
        "state_candidate": state_candidate,
        "expected_rejection_contains": list(expected_rejection_contains),
        "expected_projection_keys": list(expected_projection_keys),
        "expected_missing_fields": list(expected_missing_fields),
        "expected_provenance_refs": list(expected_provenance_refs),
    }


def build_contract_fixtures_v1() -> List[Dict[str, Any]]:
    cases: List[Dict[str, Any]] = []

    q = _base_query("field_state_ref_only")
    cases.append(
        _case(
            "field_state_ref_only_read_ready",
            "read_ready",
            query=q,
            state_candidate=_base_state("field_state_ref_only"),
            expected_projection_keys=("entities", "status"),
        )
    )

    q = _base_query("snapshot_ref_only")
    q["field_state_ref"] = None
    q["snapshot_ref"] = "state_ref_snapshot_ref_only"
    s = _base_state("snapshot_ref_only")
    s["source_state_ref"] = "state_ref_snapshot_ref_only"
    cases.append(
        _case(
            "snapshot_ref_only_read_ready",
            "read_ready",
            query=q,
            state_candidate=s,
            expected_projection_keys=("entities", "status"),
        )
    )

    q = _base_query("both_refs")
    q["snapshot_ref"] = "state_ref_both_refs"
    s = _base_state("both_refs")
    s["source_state_ref"] = "state_ref_both_refs"
    cases.append(
        _case(
            "both_refs_read_ready",
            "read_ready",
            query=q,
            state_candidate=s,
            expected_projection_keys=("entities", "status"),
        )
    )

    q = _base_query("full_projection", ("confidence", "entities", "region", "status"))
    cases.append(
        _case(
            "full_projection",
            "read_ready",
            query=q,
            state_candidate=_base_state("full_projection"),
            expected_projection_keys=("confidence", "entities", "region", "status"),
        )
    )

    q = _base_query("partial_projection")
    s = _base_state("partial_projection")
    s["state_payload"].pop("entities")
    s["available_fields"] = ["confidence", "region", "status"]
    cases.append(
        _case(
            "partial_projection",
            "partial_projection",
            query=q,
            state_candidate=s,
            expected_projection_keys=("status",),
            expected_missing_fields=("entities",),
        )
    )

    q = _base_query("insufficient_projection")
    s = _base_state("insufficient_projection")
    s["state_payload"] = {"region": "front_corridor"}
    s["available_fields"] = ["region"]
    cases.append(
        _case(
            "insufficient_projection",
            "insufficient_state",
            query=q,
            state_candidate=s,
            expected_projection_keys=tuple(),
            expected_missing_fields=("entities", "status"),
        )
    )

    q = _base_query("stale_full_payload")
    s = _base_state("stale_full_payload")
    s["temporal_status"] = "stale"
    cases.append(
        _case(
            "stale_with_full_payload",
            "stale_state",
            query=q,
            state_candidate=s,
            expected_projection_keys=("entities", "status"),
        )
    )

    cases.append(
        _case(
            "unavailable_without_candidate",
            "state_unavailable",
            query=_base_query("unavailable_without_candidate"),
            state_candidate=None,
        )
    )

    q = _base_query("invalid_overrides_unavailable")
    q["query_id"] = ""
    cases.append(
        _case(
            "invalid_query_overrides_unavailable",
            "query_rejected",
            query=q,
            state_candidate=None,
            expected_rejection_contains=("missing_query_id",),
        )
    )

    q = _base_query("unavailable_overrides_stale")
    s = _base_state("unavailable_overrides_stale")
    s["source_state_ref"] = ""
    s["temporal_status"] = "stale"
    cases.append(
        _case(
            "unavailable_overrides_stale",
            "state_unavailable",
            query=q,
            state_candidate=s,
            expected_rejection_contains=("missing_source_state_ref",),
        )
    )

    q = _base_query("stale_overrides_insufficient")
    s = _base_state("stale_overrides_insufficient")
    s["temporal_status"] = "stale"
    s["state_payload"] = {"region": "front_corridor"}
    s["available_fields"] = ["region"]
    cases.append(
        _case(
            "stale_overrides_insufficient",
            "stale_state",
            query=q,
            state_candidate=s,
            expected_missing_fields=("entities", "status"),
        )
    )

    q = _base_query("insufficient_overrides_partial")
    s = _base_state("insufficient_overrides_partial")
    s["state_payload"] = {"region": "front_corridor"}
    s["available_fields"] = ["region"]
    cases.append(
        _case(
            "insufficient_overrides_partial",
            "insufficient_state",
            query=q,
            state_candidate=s,
            expected_missing_fields=("entities", "status"),
        )
    )

    q = _base_query("partial_overrides_ready", ("entities", "missing_field", "status"))
    s = _base_state("partial_overrides_ready")
    cases.append(
        _case(
            "partial_overrides_ready",
            "partial_projection",
            query=q,
            state_candidate=s,
            expected_projection_keys=("entities", "status"),
            expected_missing_fields=("missing_field",),
        )
    )

    invalid_query_cases = [
        ("missing_query_id", {"query_id": ""}, ("missing_query_id",)),
        ("missing_requester_ref", {"requester_ref": ""}, ("missing_requester_ref",)),
        (
            "missing_query_scope",
            {"query_scope": ""},
            ("missing_query_scope", "unsupported_query_scope"),
        ),
        ("missing_trace_ref", {"trace_ref": ""}, ("missing_trace_ref",)),
        ("missing_replay_key", {"replay_key": ""}, ("missing_replay_key",)),
        ("empty_required_fields", {"required_fields": []}, ("required_fields_empty",)),
        (
            "missing_both_state_refs",
            {"field_state_ref": None, "snapshot_ref": None},
            ("missing_state_reference",),
        ),
        (
            "invalid_query_scope",
            {"query_scope": "bad_scope"},
            ("unsupported_query_scope",),
        ),
        (
            "unknown_query_field",
            {"unknown_field": "forbidden"},
            ("unknown_fields_not_allowed",),
        ),
        (
            "invalid_required_fields_type",
            {"required_fields": "status"},
            ("invalid_required_fields_type", "required_fields_empty"),
        ),
        (
            "duplicate_required_fields",
            {"required_fields": ["status", "status"]},
            ("duplicate_required_fields",),
        ),
        (
            "invalid_temporal_scope_type",
            {"temporal_scope": "bad"},
            ("invalid_temporal_scope_type",),
        ),
        ("invalid_metadata_type", {"metadata": "bad"}, ("metadata_must_be_dict",)),
    ]
    for case_id, overrides, expected_reasons in invalid_query_cases:
        query = _base_query(case_id)
        query.update(overrides)
        state = _base_state(case_id)
        cases.append(
            _case(
                case_id,
                "query_rejected",
                query=query,
                state_candidate=state,
                expected_rejection_contains=expected_reasons,
            )
        )

    invalid_state_cases = [
        (
            "invalid_state_payload_type",
            {"state_payload": "bad"},
            ("invalid_state_payload_type",),
        ),
        (
            "invalid_available_fields_type",
            {"available_fields": "bad"},
            ("invalid_available_fields_type",),
        ),
        (
            "missing_source_state_ref",
            {"source_state_ref": ""},
            ("missing_source_state_ref",),
        ),
        ("missing_state_version", {"state_version": ""}, ("missing_state_version",)),
        (
            "invalid_provenance_refs_type",
            {"provenance_refs": "bad"},
            ("invalid_provenance_refs_type",),
        ),
        (
            "unknown_temporal_status",
            {"temporal_status": "future_magic"},
            ("unknown_temporal_status",),
        ),
        (
            "state_ref_mismatch",
            {"source_state_ref": "other_ref"},
            ("state_ref_mismatch",),
        ),
        (
            "replay_key_mismatch",
            {"replay_key": "other_replay"},
            ("replay_key_mismatch",),
        ),
        ("trace_ref_mismatch", {"trace_ref": "other_trace"}, ("trace_ref_mismatch",)),
    ]
    for case_id, overrides, expected_reasons in invalid_state_cases:
        query = _base_query(case_id)
        state = _base_state(case_id)
        state.update(overrides)
        cases.append(
            _case(
                case_id,
                "state_unavailable",
                query=query,
                state_candidate=state,
                expected_rejection_contains=expected_reasons,
            )
        )

    q = _base_query("stable_required_field_order", ("status", "confidence", "entities"))
    cases.append(
        _case(
            "stable_required_field_order",
            "read_ready",
            query=q,
            state_candidate=_base_state("stable_required_field_order"),
            expected_projection_keys=("confidence", "entities", "status"),
        )
    )

    q = _base_query("stable_missing_field_order", ("zeta", "alpha", "status"))
    s = _base_state("stable_missing_field_order")
    cases.append(
        _case(
            "stable_missing_field_order",
            "partial_projection",
            query=q,
            state_candidate=s,
            expected_projection_keys=("status",),
            expected_missing_fields=("alpha", "zeta"),
        )
    )

    q = _base_query("stable_provenance_order", ("status",))
    s = _base_state("stable_provenance_order")
    s["provenance_refs"] = ["prov_b", "prov_a", "prov_c"]
    cases.append(
        _case(
            "stable_provenance_order",
            "read_ready",
            query=q,
            state_candidate=s,
            expected_projection_keys=("status",),
            expected_provenance_refs=("prov_b", "prov_a", "prov_c"),
        )
    )

    q = _base_query("stable_json_serialization", ("entities", "status"))
    cases.append(
        _case(
            "stable_json_serialization",
            "read_ready",
            query=q,
            state_candidate=_base_state("stable_json_serialization"),
            expected_projection_keys=("entities", "status"),
        )
    )

    q = _base_query("deterministic_replay", ("region", "status"))
    cases.append(
        _case(
            "deterministic_replay",
            "read_ready",
            query=q,
            state_candidate=_base_state("deterministic_replay"),
            expected_projection_keys=("region", "status"),
        )
    )

    q = _base_query("query_input_immutability", ("region", "status"))
    cases.append(
        _case(
            "query_input_immutability",
            "read_ready",
            query=q,
            state_candidate=_base_state("query_input_immutability"),
            expected_projection_keys=("region", "status"),
        )
    )

    q = _base_query("state_candidate_immutability", ("region", "status"))
    cases.append(
        _case(
            "state_candidate_immutability",
            "read_ready",
            query=q,
            state_candidate=_base_state("state_candidate_immutability"),
            expected_projection_keys=("region", "status"),
        )
    )

    q = _base_query("boundary_flags_constant", ("status",))
    cases.append(
        _case(
            "boundary_flags_constant",
            "read_ready",
            query=q,
            state_candidate=_base_state("boundary_flags_constant"),
            expected_projection_keys=("status",),
        )
    )

    q = _base_query("runtime_executed_false", ("status",))
    cases.append(
        _case(
            "runtime_executed_false",
            "read_ready",
            query=q,
            state_candidate=_base_state("runtime_executed_false"),
            expected_projection_keys=("status",),
        )
    )

    q = _base_query("candidate_only_true", ("status",))
    cases.append(
        _case(
            "candidate_only_true",
            "read_ready",
            query=q,
            state_candidate=_base_state("candidate_only_true"),
            expected_projection_keys=("status",),
        )
    )

    return cases
