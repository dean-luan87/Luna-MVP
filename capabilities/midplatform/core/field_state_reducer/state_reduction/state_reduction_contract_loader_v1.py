from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


REDUCER_PLANNING_DIR = (
    Path(__file__).resolve().parents[5]
    / "docs/architecture/luna_field_state_reducer_technical_planning_v1"
)
TEMPORAL_PLANNING_DIR = (
    Path(__file__).resolve().parents[5]
    / "docs/architecture/luna_field_event_temporal_validity_protocol_planning_v1"
)


def _load_json(base: Path, name: str) -> Dict[str, Any]:
    with open(base / name, "r", encoding="utf-8") as f:
        return json.load(f)


def load_state_reduction_contracts_v1() -> Dict[str, Dict[str, Any]]:
    return {
        "input_contract": _load_json(
            REDUCER_PLANNING_DIR, "field_state_reducer_input_contract_v1.json"
        ),
        "output_contract": _load_json(
            REDUCER_PLANNING_DIR, "field_state_reducer_output_contract_v1.json"
        ),
        "status_transition_matrix": _load_json(
            REDUCER_PLANNING_DIR, "field_state_status_transition_matrix_v1.json"
        ),
        "status_registry": _load_json(
            REDUCER_PLANNING_DIR, "field_state_status_registry_v1.json"
        ),
        "reduction_policy_registry": _load_json(
            REDUCER_PLANNING_DIR, "field_state_reduction_policy_registry_v1.json"
        ),
        "conflict_resolution_matrix": _load_json(
            REDUCER_PLANNING_DIR, "field_state_conflict_resolution_matrix_v1.json"
        ),
        "temporal_reduction_contract": _load_json(
            REDUCER_PLANNING_DIR, "field_state_temporal_reduction_contract_v1.json"
        ),
        "replay_contract": _load_json(
            REDUCER_PLANNING_DIR, "field_state_replay_contract_v1.json"
        ),
        "provenance_trace_schema": _load_json(
            REDUCER_PLANNING_DIR, "field_state_provenance_trace_schema_v1.json"
        ),
        "negative_guards": _load_json(
            REDUCER_PLANNING_DIR, "field_state_reducer_negative_guards_v1.json"
        ),
        "temporal_validity_schema": _load_json(
            TEMPORAL_PLANNING_DIR, "temporal_validity_schema_v1.json"
        ),
        "temporal_status_transition_matrix": _load_json(
            TEMPORAL_PLANNING_DIR, "temporal_status_transition_matrix_v1.json"
        ),
        "temporary_overlay_protocol": _load_json(
            TEMPORAL_PLANNING_DIR, "temporary_overlay_protocol_v1.json"
        ),
        "event_temporal_negative_guards": _load_json(
            TEMPORAL_PLANNING_DIR,
            "field_event_temporal_validity_protocol_negative_guards_v1.json",
        ),
    }
