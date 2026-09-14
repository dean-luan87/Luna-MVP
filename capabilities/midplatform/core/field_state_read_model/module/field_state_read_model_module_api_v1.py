from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict

from .field_state_read_model_module_types_v1 import FieldStateReadResultV1
from .field_state_read_model_projection_builder_v1 import build_projection_candidate_v1
from .field_state_read_model_query_validator_v1 import validate_query_v1
from .field_state_read_model_result_builder_v1 import build_result_v1


def _to_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if is_dataclass(value):
        return asdict(value)
    raise TypeError("state_candidate_must_be_dict_or_dataclass")


def read_field_state(
    query: Any,
    state_candidate: Any,
) -> FieldStateReadResultV1:
    try:
        query_valid, rejection_reasons, normalized_query = validate_query_v1(query)
        normalized_state_candidate = (
            _to_dict(state_candidate) if state_candidate is not None else None
        )
        projection_candidate = None
        state_validation_reasons = tuple()
        if query_valid:
            (
                projection_candidate,
                state_validation_reasons,
                normalized_state_candidate,
            ) = build_projection_candidate_v1(
                query=normalized_query,
                state_candidate=normalized_state_candidate,
            )
        return build_result_v1(
            query=normalized_query,
            query_valid=query_valid,
            rejection_reasons=rejection_reasons,
            state_candidate=normalized_state_candidate,
            state_validation_reasons=state_validation_reasons,
            projection_candidate=projection_candidate,
        )
    except Exception as exc:
        fallback_query = {
            "query_id": "",
            "field_state_ref": "",
            "snapshot_ref": "",
            "trace_ref": "",
            "replay_key": "",
        }
        return build_result_v1(
            query=fallback_query,
            query_valid=False,
            rejection_reasons=(f"unhandled_exception:{type(exc).__name__}",),
            state_candidate=None,
            state_validation_reasons=tuple(),
            projection_candidate=None,
        )
