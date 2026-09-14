from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


PLANNING_DIR = (
    Path(__file__).resolve().parents[6]
    / "docs/architecture/luna_field_state_reducer_behavior_policy_technical_planning_v1"
)


def _load_json(name: str) -> Dict[str, Any]:
    with open(PLANNING_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def load_policy_selection_contracts_v1() -> Dict[str, Dict[str, Any]]:
    return {
        "policy_registry": _load_json(
            "field_state_reducer_behavior_policy_registry_v1.json"
        ),
        "precedence_matrix": _load_json(
            "field_state_reducer_policy_precedence_matrix_v1.json"
        ),
        "composition_contract": _load_json(
            "field_state_reducer_policy_composition_contract_v1.json"
        ),
        "conflict_policy": _load_json(
            "field_state_reducer_conflict_policy_matrix_v1.json"
        ),
        "decision_schema": _load_json(
            "field_state_reducer_policy_decision_schema_v1.json"
        ),
        "replay_contract": _load_json(
            "field_state_reducer_policy_replay_contract_v1.json"
        ),
    }
