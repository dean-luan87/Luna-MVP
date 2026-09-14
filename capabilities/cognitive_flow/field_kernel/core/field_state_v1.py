"""Reducer-produced Field State representation object v1.

Field Kernel exposes this immutable view but never creates it from raw input or
changes it. The Field State Reducer remains its sole mutation authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Tuple

from .field_identity_v1 import FIELD_KERNEL_SCHEMA_VERSION_V1


@dataclass(frozen=True)
class FieldStateV1:
    """One current, time-bounded Reducer-produced state description."""

    state_id: str
    target_ref: str
    state_type: str
    value: Mapping[str, Any]
    valid_time: Mapping[str, Any]
    evidence_refs: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    trace_ref: str
    provenance: Mapping[str, Any]
    schema_version: str = FIELD_KERNEL_SCHEMA_VERSION_V1
    produced_by: str = "field_state_reducer"
    candidate_only: bool = True
    state_mutation_executed: bool = False


def field_state_from_reducer_output_v1(
    reducer_state: Mapping[str, Any],
) -> FieldStateV1:
    """Build a read representation from a Reducer-produced state mapping.

    This is projection-only conversion. It rejects a mapping that does not
    explicitly identify the Field State Reducer as its producer; it performs no
    reduction or state mutation.
    """

    source = dict(reducer_state)
    if source.get("produced_by") != "field_state_reducer":
        raise ValueError("FieldStateV1 must originate from field_state_reducer")

    provenance = dict(source.get("provenance") or {})
    provenance.setdefault("reducer_output_ref", source.get("reducer_output_ref", ""))
    value = source.get("value", source.get("state_value"))
    if not isinstance(value, Mapping):
        raise ValueError("reducer-produced state value must be a mapping")
    valid_time = source.get("valid_time")
    if not isinstance(valid_time, Mapping):
        valid_time = {
            "effective_from": source.get("effective_from"),
            "effective_until": source.get("effective_until"),
        }

    target_ref = source.get("target_ref", source.get("field_id"))
    if not isinstance(target_ref, str) or not target_ref:
        raise ValueError("reducer-produced state requires target_ref or field_id")
    trace_ref = source.get("trace_ref", "")
    if not isinstance(trace_ref, str) or not trace_ref:
        raise ValueError("reducer-produced state requires trace_ref")

    return FieldStateV1(
        state_id=str(source.get("state_id") or ""),
        target_ref=target_ref,
        state_type=str(source.get("state_type") or ""),
        value=dict(value),
        valid_time=dict(valid_time),
        evidence_refs=tuple(source.get("evidence_refs") or ()),
        source_chain=tuple(source.get("source_chain") or ()),
        trace_ref=trace_ref,
        provenance=provenance,
        schema_version=str(source.get("schema_version") or FIELD_KERNEL_SCHEMA_VERSION_V1),
        candidate_only=bool(source.get("candidate_only", True)),
    )
