#!/usr/bin/env python3
"""Static verifier for cognitive learning governance planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

BASE = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "cognitive_learning_architecture_plan_v1.md",
    "cognitive_learning_existing_asset_inventory_v1.json",
    "cognitive_learning_owner_boundary_v1.json",
    "cognitive_learning_concept_boundary_matrix_v1.json",
    "learning_evidence_candidate_schema_v1.json",
    "learning_candidate_schema_v1.json",
    "parameter_update_candidate_schema_v1.json",
    "cognitive_learning_taxonomy_v1.json",
    "learning_admission_state_model_v1.json",
    "learning_generalization_governance_v1.json",
    "learning_confidence_evidence_model_v1.json",
    "learning_contradiction_counterexample_model_v1.json",
    "learning_revision_revocation_model_v1.json",
    "learning_memory_experience_boundary_v1.json",
    "learning_dynamic_regulation_boundary_v1.json",
    "learning_intent_boundary_v1.json",
    "learning_state_formation_boundary_v1.json",
    "learning_causal_boundary_v1.json",
    "learning_self_personality_emotion_boundary_v1.json",
    "learning_privacy_transfer_boundary_v1.json",
    "learning_semantic_compression_deferred_boundary_v1.json",
    "cognitive_learning_trace_provenance_contract_v1.json",
    "cognitive_learning_idempotency_contract_v1.json",
    "cognitive_learning_negative_guards_v1.json",
    "cognitive_learning_minimum_scenario_suite_v1.json",
    "cognitive_learning_gap_registry_v1.json",
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
        for err in errors:
            print(f"[FAIL] {err}")
        return 1

    owner = _load_json(BASE / "cognitive_learning_owner_boundary_v1.json")
    if owner.get("canonical_owner_candidate") != "Cognitive Learning Governance":
        errors.append("canonical owner mismatch")

    concept = _load_json(BASE / "cognitive_learning_concept_boundary_matrix_v1.json")
    inequalities = concept.get("inequalities", [])
    if not _contains_all(
        inequalities,
        [
            "Experience != Learning",
            "Memory != Learning",
            "Learning Candidate != Truth",
            "Parameter Update Candidate != Parameter Activation",
        ],
    ):
        errors.append("concept boundary incomplete")

    taxonomy = _load_json(BASE / "cognitive_learning_taxonomy_v1.json")
    if len(taxonomy.get("learning_kinds", [])) < 17:
        errors.append("taxonomy incomplete")

    scenarios = _load_json(BASE / "cognitive_learning_minimum_scenario_suite_v1.json")
    ids = [item.get("id", "") for item in scenarios.get("scenarios", [])]
    if scenarios.get("scenario_count", 0) < 28:
        errors.append("scenario_count must be >= 28")
    if not _contains_all(ids, [f"L{i:02d}" for i in range(1, 29)]):
        errors.append("L01-L28 coverage missing")

    guards = _load_json(BASE / "cognitive_learning_negative_guards_v1.json").get(
        "guards", {}
    )
    required_false = [
        "learning_can_create_fact",
        "learning_can_mutate_memory",
        "learning_can_activate_parameter",
        "learning_can_activate_genome",
        "cross_user_transfer",
        "semantic_compression_execution",
    ]
    for key in required_false:
        if guards.get(key) is not False:
            errors.append(f"negative guard mismatch: {key}")
    if guards.get("planning_only") is not True:
        errors.append("planning_only guard missing")

    compression = _load_json(
        BASE / "learning_semantic_compression_deferred_boundary_v1.json"
    )
    if compression.get("semantic_compression_status") != "DEFERRED":
        errors.append("semantic compression must be deferred")

    phase = _load_json(BASE / "phase_contract.json")
    if phase.get("execution_mode") != "PLANNING_ONLY":
        errors.append("execution mode mismatch")
    if phase.get("agent_stop_status") != "WAITING_FOR_USER_TERMINAL_VERIFICATION":
        errors.append("agent stop status mismatch")

    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        return 1

    print(
        "[PASS] cognitive learning governance planning artifacts are structurally valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
