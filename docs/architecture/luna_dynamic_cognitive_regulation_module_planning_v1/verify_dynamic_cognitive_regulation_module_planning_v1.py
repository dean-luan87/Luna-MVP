#!/usr/bin/env python3
"""Static verifier for dynamic cognitive regulation module planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

BASE = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "dynamic_cognitive_regulation_architecture_plan_v1.md",
    "dynamic_cognitive_regulation_owner_boundary_v1.json",
    "dynamic_cognitive_regulation_concept_boundary_matrix_v1.json",
    "cognitive_state_vector_input_contract_v1.json",
    "dynamic_regulation_candidate_schema_v1.json",
    "dynamic_regulation_function_contract_v1.json",
    "cognitive_parameter_classification_v1.json",
    "cognitive_parameter_bounds_contract_v1.json",
    "cognitive_parameter_genome_candidate_schema_v1.json",
    "self_regulation_state_model_v1.json",
    "attention_influence_boundary_v1.json",
    "intent_influence_boundary_v1.json",
    "hypothesis_influence_boundary_v1.json",
    "emotion_influence_boundary_v1.json",
    "resource_influence_boundary_v1.json",
    "learning_boundary_v1.json",
    "dynamic_regulation_trace_provenance_contract_v1.json",
    "dynamic_regulation_revision_revocation_model_v1.json",
    "dynamic_regulation_negative_guards_v1.json",
    "dynamic_regulation_minimum_scenario_suite_v1.json",
    "dynamic_regulation_existing_asset_reuse_mapping_v1.json",
    "dynamic_regulation_gap_registry_v1.json",
    "phase_contract.json",
]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _contains_all(items: Iterable[str], required: Iterable[str]) -> bool:
    item_set = set(items)
    return all(r in item_set for r in required)


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (BASE / rel).exists():
            errors.append(f"missing file: {rel}")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return 1

    owner = _load_json(BASE / "dynamic_cognitive_regulation_owner_boundary_v1.json")
    if (
        owner.get("canonical_owner_candidate")
        != "Dynamic Cognitive Regulation Governance"
    ):
        errors.append("canonical owner mismatch")

    phase = _load_json(BASE / "phase_contract.json")
    if phase.get("execution_mode") != "PLANNING_ONLY":
        errors.append("execution_mode must be PLANNING_ONLY")
    if phase.get("agent_stop_state") != "WAITING_FOR_USER_TERMINAL_VERIFICATION":
        errors.append("agent_stop_state mismatch")

    scenarios = _load_json(BASE / "dynamic_regulation_minimum_scenario_suite_v1.json")
    ids = [item.get("id", "") for item in scenarios.get("scenarios", [])]
    expected_ids = [f"R{i:02d}" for i in range(1, 21)]
    if scenarios.get("scenario_count") != 20:
        errors.append("scenario_count must be 20")
    if not _contains_all(ids, expected_ids):
        errors.append("scenario ids incomplete")

    guards = _load_json(BASE / "dynamic_regulation_negative_guards_v1.json")
    forbidden = guards.get("forbidden", [])
    if not _contains_all(
        forbidden,
        [
            "model_weight_mutation",
            "permanent_parameter_persistence",
            "database_write",
            "runtime_side_effect",
            "silent_adaptive_mutation",
        ],
    ):
        errors.append("negative guards incomplete")

    vector_input = _load_json(BASE / "cognitive_state_vector_input_contract_v1.json")
    inv = vector_input.get("state_vector_invariants", {})
    if inv.get("state_vector_not_parameter_store") is not True:
        errors.append("state vector boundary missing")

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return 1

    print(
        "[PASS] dynamic cognitive regulation module planning artifacts are structurally valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
