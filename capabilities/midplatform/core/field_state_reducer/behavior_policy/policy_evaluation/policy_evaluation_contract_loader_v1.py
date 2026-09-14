from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


PLANNING_DIR = (
    Path(__file__).resolve().parents[6]
    / "docs/architecture/luna_field_state_reducer_behavior_policy_controlled_policy_evaluation_technical_planning_v1"
)


def _load_json(name: str) -> Dict[str, Any]:
    with open(PLANNING_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def load_policy_evaluation_contracts_v1() -> Dict[str, Dict[str, Any]]:
    return {
        "input_schema": _load_json(
            "field_state_reducer_policy_evaluation_input_schema_v1.json"
        ),
        "status_registry": _load_json(
            "field_state_reducer_policy_evaluation_status_registry_v1.json"
        ),
        "condition_registry": _load_json(
            "field_state_reducer_policy_evaluation_condition_type_registry_v1.json"
        ),
        "operator_registry": _load_json(
            "field_state_reducer_policy_evaluation_operator_registry_v1.json"
        ),
        "rule_schema": _load_json(
            "field_state_reducer_policy_evaluation_rule_schema_v1.json"
        ),
        "evaluation_matrix": _load_json(
            "field_state_reducer_policy_evaluation_matrix_v1.json"
        ),
        "evidence_contract": _load_json(
            "field_state_reducer_policy_evidence_sufficiency_contract_v1.json"
        ),
        "temporal_contract": _load_json(
            "field_state_reducer_policy_temporal_evaluation_contract_v1.json"
        ),
        "confidence_contract": _load_json(
            "field_state_reducer_policy_confidence_evaluation_contract_v1.json"
        ),
        "conflict_contract": _load_json(
            "field_state_reducer_policy_conflict_evaluation_contract_v1.json"
        ),
        "governance_contract": _load_json(
            "field_state_reducer_policy_governance_evaluation_contract_v1.json"
        ),
        "result_schema": _load_json(
            "field_state_reducer_policy_evaluation_result_schema_v1.json"
        ),
        "trace_schema": _load_json(
            "field_state_reducer_policy_evaluation_trace_schema_v1.json"
        ),
        "replay_contract": _load_json(
            "field_state_reducer_policy_evaluation_replay_contract_v1.json"
        ),
        "rejection_registry": _load_json(
            "field_state_reducer_policy_evaluation_rejection_reason_registry_v1.json"
        ),
        "minimum_cases": _load_json(
            "field_state_reducer_policy_evaluation_minimum_cases_v1.json"
        ),
        "negative_guards": _load_json(
            "field_state_reducer_policy_evaluation_negative_guards_v1.json"
        ),
        "summary": _load_json("field_state_reducer_policy_evaluation_summary_v1.json"),
    }
