#!/usr/bin/env python3
"""Static verifier for cognitive state formation architecture planning artifacts.

This script only validates file presence and schema-level planning constraints.
It does not execute runtime modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

BASE = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "cognitive_state_formation_architecture_plan_v1.md",
    "cognitive_state_formation_owner_boundary_v1.json",
    "cognitive_state_formation_concept_boundary_matrix_v1.json",
    "cognitive_state_formation_input_contract_v1.json",
    "cognitive_state_formation_output_contract_v1.json",
    "cognitive_state_formation_trace_provenance_contract_v1.json",
    "attention_candidate_schema_v1.json",
    "attention_selection_model_v1.json",
    "cognitive_hypothesis_schema_v1.json",
    "cognitive_hypothesis_state_model_v1.json",
    "cognitive_hypothesis_competition_model_v1.json",
    "current_world_candidate_schema_v1.json",
    "current_world_field_boundary_v1.json",
    "cognitive_state_formation_causal_handoff_v1.json",
    "cognitive_state_vector_candidate_contract_v1.json",
    "cognitive_state_formation_gap_registry_v1.json",
    "cognitive_state_formation_scenario_suite_v1.json",
    "cognitive_state_formation_negative_guards_v1.json",
    "phase_contract.json",
]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _expect(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def _contains_all(items: Iterable[str], required: Iterable[str]) -> bool:
    item_set = set(items)
    return all(r in item_set for r in required)


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        _expect((BASE / rel).exists(), f"missing file: {rel}", errors)

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return 1

    owner = _load_json(BASE / "cognitive_state_formation_owner_boundary_v1.json")
    _expect(
        owner.get("canonical_owner_candidate")
        == "Cognitive State Formation Governance",
        "canonical owner mismatch",
        errors,
    )

    output_contract = _load_json(
        BASE / "cognitive_state_formation_output_contract_v1.json"
    )
    forbidden_outputs = output_contract.get("forbidden_outputs", [])
    _expect(
        _contains_all(
            forbidden_outputs,
            [
                "field_truth_write",
                "causal_truth",
                "decision",
                "action",
                "task",
                "runtime_command",
            ],
        ),
        "forbidden outputs incomplete",
        errors,
    )

    boundary = _load_json(BASE / "current_world_field_boundary_v1.json")
    rules = boundary.get("rules", {})
    _expect(
        rules.get("current_world_not_equal_field_state") is True,
        "current_world_not_equal_field_state must be true",
        errors,
    )
    _expect(
        rules.get("current_world_cannot_modify_field_entities") is True,
        "current world must not modify field",
        errors,
    )

    handoff = _load_json(BASE / "cognitive_state_formation_causal_handoff_v1.json")
    _expect(
        handoff.get("handoff_type") == "CANDIDATE_REFERENCE_ONLY",
        "handoff type must be candidate reference only",
        errors,
    )

    scenarios = _load_json(BASE / "cognitive_state_formation_scenario_suite_v1.json")
    _expect(scenarios.get("scenario_count") == 20, "scenario_count must be 20", errors)
    _expect(
        len(scenarios.get("scenarios", [])) == 20,
        "scenario entries must be exactly 20",
        errors,
    )

    guards = _load_json(BASE / "cognitive_state_formation_negative_guards_v1.json")
    must_fail_if_present = guards.get("must_fail_if_present", [])
    _expect(
        _contains_all(
            must_fail_if_present,
            [
                "field_state_mutation",
                "causal_truth_label",
                "decision_output",
                "action_output",
                "trace_missing",
                "provenance_missing",
            ],
        ),
        "negative guards incomplete",
        errors,
    )

    phase = _load_json(BASE / "phase_contract.json")
    _expect(
        phase.get("agent_stop_state") == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "invalid agent stop state",
        errors,
    )

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return 1

    print(
        "[PASS] cognitive state formation architecture planning artifacts are structurally valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
