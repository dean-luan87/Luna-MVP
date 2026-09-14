#!/usr/bin/env python3
"""Static verifier for cognitive memory and experience governance planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

BASE = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "cognitive_memory_experience_architecture_plan_v1.md",
    "cognitive_memory_experience_existing_asset_inventory_v1.json",
    "cognitive_memory_experience_owner_boundary_v1.json",
    "cognitive_memory_experience_concept_boundary_matrix_v1.json",
    "experience_candidate_schema_v1.json",
    "memory_candidate_schema_v1.json",
    "memory_type_taxonomy_v1.json",
    "memory_admission_state_model_v1.json",
    "experience_to_memory_formation_contract_v1.json",
    "memory_salience_retention_decay_model_v1.json",
    "memory_contradiction_revision_revocation_model_v1.json",
    "memory_context_boundary_v1.json",
    "memory_pcn_boundary_v1.json",
    "memory_intent_boundary_v1.json",
    "memory_state_formation_boundary_v1.json",
    "memory_dynamic_regulation_boundary_v1.json",
    "memory_learning_boundary_v1.json",
    "memory_personality_self_boundary_v1.json",
    "memory_privacy_sensitivity_boundary_v1.json",
    "memory_trace_provenance_contract_v1.json",
    "memory_idempotency_contract_v1.json",
    "cognitive_memory_experience_negative_guards_v1.json",
    "cognitive_memory_experience_minimum_scenario_suite_v1.json",
    "cognitive_memory_experience_gap_registry_v1.json",
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

    inventory = _load_json(
        BASE / "cognitive_memory_experience_existing_asset_inventory_v1.json"
    )
    if inventory.get("equivalent_current_canonical_memory_owner_found") is not False:
        errors.append("equivalent canonical memory owner unexpectedly found")

    owner = _load_json(BASE / "cognitive_memory_experience_owner_boundary_v1.json")
    if (
        owner.get("canonical_owner_candidate")
        != "Cognitive Memory & Experience Governance"
    ):
        errors.append("canonical owner mismatch")

    taxonomy = _load_json(BASE / "memory_type_taxonomy_v1.json")
    types = [item.get("type", "") for item in taxonomy.get("types", [])]
    if not _contains_all(
        types,
        [
            "EPISODIC",
            "SEMANTIC",
            "RELATIONAL",
            "SELF_RELATED",
            "PREFERENCE",
            "PROCEDURAL_REFERENCE",
            "ENVIRONMENTAL_CONTEXT",
            "TASK_EXPERIENCE",
            "SOCIAL_EXPERIENCE",
            "EMOTIONAL_EXPERIENCE",
            "UNRESOLVED_EXPERIENCE",
        ],
    ):
        errors.append("memory taxonomy incomplete")

    admission = _load_json(BASE / "memory_admission_state_model_v1.json")
    states = admission.get("states", [])
    if not _contains_all(
        states,
        [
            "PROPOSED",
            "ELIGIBLE",
            "INSUFFICIENT_EVIDENCE",
            "CONTESTED",
            "NEEDS_CONFIRMATION",
            "TEMPORARY",
            "ADMITTED_CANDIDATE",
            "REJECTED",
            "SUPERSEDED",
            "REVISED",
            "REVOKED",
            "EXPIRED",
        ],
    ):
        errors.append("admission states incomplete")

    scenarios = _load_json(
        BASE / "cognitive_memory_experience_minimum_scenario_suite_v1.json"
    )
    if scenarios.get("scenario_count", 0) < 24:
        errors.append("scenario_count must be >= 24")
    ids = [item.get("id", "") for item in scenarios.get("scenarios", [])]
    if not _contains_all(ids, [f"M{i:02d}" for i in range(1, 25)]):
        errors.append("required memory scenarios incomplete")

    guards = _load_json(
        BASE / "cognitive_memory_experience_negative_guards_v1.json"
    ).get("guards", {})
    if guards.get("database_write") is not False:
        errors.append("database_write guard mismatch")
    if guards.get("runtime_execution") is not False:
        errors.append("runtime_execution guard mismatch")
    if guards.get("planning_only") is not True:
        errors.append("planning_only guard missing")

    phase = _load_json(BASE / "phase_contract.json")
    if phase.get("execution_mode") != "PLANNING_ONLY":
        errors.append("execution_mode mismatch")
    if phase.get("agent_stop_state") != "WAITING_FOR_USER_TERMINAL_VERIFICATION":
        errors.append("agent_stop_state mismatch")

    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        return 1

    print(
        "[PASS] cognitive memory and experience governance planning artifacts are structurally valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
