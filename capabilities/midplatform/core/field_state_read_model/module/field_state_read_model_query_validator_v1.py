from __future__ import annotations

from dataclasses import asdict, is_dataclass
from collections.abc import Mapping
from typing import Any, Dict, Tuple

from .field_state_read_model_module_types_v1 import (
    FieldStateReadQueryV1,
    QUERY_SCOPE_REGISTRY_V1,
)

_REQUIRED_TOP_LEVEL_FIELDS: Tuple[str, ...] = (
    "query_id",
    "requester_ref",
    "query_scope",
    "field_state_ref",
    "snapshot_ref",
    "task_ref",
    "scene_ref",
    "object_ref",
    "temporal_scope",
    "required_fields",
    "trace_ref",
    "replay_key",
    "metadata",
)


def _to_query_mapping(query: FieldStateReadQueryV1 | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(query, Mapping):
        return dict(query)
    if is_dataclass(query):
        return asdict(query)
    raise TypeError("query_must_be_mapping_or_dataclass")


def _normalize_required_fields(value: Any) -> Tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        return tuple()
    if any(not isinstance(item, str) or not item.strip() for item in value):
        return tuple()
    return tuple(value)


def _valid_optional_ref(value: Any) -> bool:
    return value is None or (isinstance(value, str) and bool(value.strip()))


def validate_query_v1(
    query: FieldStateReadQueryV1 | Dict[str, Any],
) -> Tuple[bool, Tuple[str, ...], Dict[str, Any]]:
    candidate = _to_query_mapping(query)
    unknown_fields = tuple(
        sorted(set(candidate.keys()) - set(_REQUIRED_TOP_LEVEL_FIELDS))
    )
    reasons = []

    for name in ("query_id", "requester_ref", "query_scope", "trace_ref", "replay_key"):
        if not isinstance(candidate.get(name), str) or not candidate.get(name, "").strip():
            reasons.append(f"missing_{name}")

    required_fields = _normalize_required_fields(candidate.get("required_fields"))
    if not isinstance(candidate.get("required_fields"), (list, tuple)):
        reasons.append("invalid_required_fields_type")
    if not required_fields:
        reasons.append("required_fields_empty")
    if any(not field_name for field_name in required_fields):
        reasons.append("required_fields_contains_empty")
    if isinstance(candidate.get("required_fields"), (list, tuple)) and any(
        not isinstance(item, str) for item in candidate["required_fields"]
    ):
        reasons.append("required_fields_member_type_invalid")
    if len(set(required_fields)) != len(required_fields):
        reasons.append("duplicate_required_fields")

    query_scope = candidate.get("query_scope", "") if isinstance(candidate.get("query_scope"), str) else ""
    if query_scope not in QUERY_SCOPE_REGISTRY_V1:
        reasons.append("unsupported_query_scope")

    field_state_ref = candidate.get("field_state_ref")
    snapshot_ref = candidate.get("snapshot_ref")
    if not _valid_optional_ref(field_state_ref) or not _valid_optional_ref(snapshot_ref):
        reasons.append("state_reference_type_invalid")
    if not (isinstance(field_state_ref, str) and field_state_ref.strip()) and not (isinstance(snapshot_ref, str) and snapshot_ref.strip()):
        reasons.append("missing_state_reference")
    for name in ("task_ref", "scene_ref", "object_ref"):
        if not _valid_optional_ref(candidate.get(name)):
            reasons.append(f"{name}_type_invalid")

    temporal_scope = candidate.get("temporal_scope")
    if temporal_scope is not None and not isinstance(temporal_scope, dict):
        reasons.append("invalid_temporal_scope_type")

    if not isinstance(candidate.get("metadata", {}), dict):
        reasons.append("metadata_must_be_dict")

    if unknown_fields:
        reasons.append("unknown_fields_not_allowed")

    if reasons:
        return False, tuple(dict.fromkeys(reasons)), {}

    normalized = {
        "query_id": str(candidate.get("query_id", "")),
        "requester_ref": str(candidate.get("requester_ref", "")),
        "query_scope": query_scope,
        "field_state_ref": str(field_state_ref)
        if field_state_ref is not None
        else None,
        "snapshot_ref": str(snapshot_ref) if snapshot_ref is not None else None,
        "task_ref": str(candidate.get("task_ref"))
        if candidate.get("task_ref") is not None
        else None,
        "scene_ref": str(candidate.get("scene_ref"))
        if candidate.get("scene_ref") is not None
        else None,
        "object_ref": str(candidate.get("object_ref"))
        if candidate.get("object_ref") is not None
        else None,
        "temporal_scope": dict(temporal_scope)
        if isinstance(temporal_scope, dict)
        else None,
        "required_fields": required_fields,
        "trace_ref": str(candidate.get("trace_ref", "")),
        "replay_key": str(candidate.get("replay_key", "")),
        "metadata": dict(candidate.get("metadata"))
        if isinstance(candidate.get("metadata"), dict)
        else {},
    }

    return len(reasons) == 0, tuple(reasons), normalized
