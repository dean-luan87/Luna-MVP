from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple


def _tuple_any(value: Any) -> Tuple[Any, ...]:
    if value is None:
        return tuple()
    if isinstance(value, (list, tuple)):
        return tuple(value)
    return (value,)


def build_field_perception_snapshot_v1(
    input_candidate: Mapping[str, Any],
) -> Dict[str, Any]:
    state = dict(input_candidate.get("current_field_state") or {})
    return {
        "schema_version": "field_perception_field_snapshot_adapter_v1",
        "field_snapshot_ref": str(
            state.get("field_snapshot_ref")
            or f"field_snapshot::{input_candidate.get('task_id')}"
        ),
        "known_entities": _tuple_any(state.get("known_entities")),
        "known_regions": _tuple_any(state.get("known_regions")),
        "temporary_overlays": _tuple_any(state.get("temporary_overlays")),
        "active_risks": _tuple_any(state.get("active_risks")),
        "navigation_relevance": dict(state.get("navigation_relevance") or {}),
        "uncertainties": _tuple_any(state.get("uncertainties")),
        "conflicts": _tuple_any(state.get("conflicts")),
        "stale_evidence": _tuple_any(state.get("stale_evidence")),
        "missing_information": _tuple_any(state.get("missing_information")),
    }
