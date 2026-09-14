#!/usr/bin/env python3
"""Static verifier for cognitive flow and state machine organization planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

BASE = Path(__file__).resolve().parent

REQUIRED_FILES = [
    "cognitive_flow_architecture_plan_v1.md",
    "cognitive_flow_existing_asset_inventory_v1.json",
    "cognitive_flow_historical_asset_classification_v1.json",
    "cognitive_flow_owner_boundary_v1.json",
    "cognitive_cycle_definition_v1.json",
    "cognitive_cycle_state_model_v1.json",
    "cognitive_cycle_transition_contract_v1.json",
    "cognitive_flow_module_interaction_matrix_v1.json",
    "cognitive_flow_serial_parallel_feedback_model_v1.json",
    "cognitive_flow_interrupt_suspend_resume_contract_v1.json",
    "cognitive_cycle_inheritance_contract_v1.json",
    "cognitive_flow_memory_insertion_boundary_v1.json",
    "cognitive_flow_learning_insertion_boundary_v1.json",
    "cognitive_flow_trace_provenance_contract_v1.json",
    "cognitive_flow_idempotency_contract_v1.json",
    "cognitive_flow_negative_guards_v1.json",
    "cognitive_flow_minimum_scenario_suite_v1.json",
    "cognitive_flow_gap_registry_v1.json",
    "cognitive_flow_planning_summary_v1.md",
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

    owner = _load_json(BASE / "cognitive_flow_owner_boundary_v1.json")
    if owner.get("canonical_owner_candidate") != "Cognitive Flow Governance":
        errors.append("canonical owner mismatch")

    guards = _load_json(BASE / "cognitive_flow_negative_guards_v1.json")
    ownership = guards.get("ownership", {})
    if ownership.get("flow_owns_context") is not False:
        errors.append("flow must not own context")
    if guards.get("phase", {}).get("planning_only") is not True:
        errors.append("planning_only guard missing")

    scenarios = _load_json(BASE / "cognitive_flow_minimum_scenario_suite_v1.json")
    ids = [item.get("id", "") for item in scenarios.get("scenarios", [])]
    expected = [f"C{i:02d}" for i in range(1, 25)]
    if scenarios.get("scenario_count") != 24:
        errors.append("scenario_count must be 24")
    if not _contains_all(ids, expected):
        errors.append("scenario ids incomplete")

    cycle = _load_json(BASE / "cognitive_cycle_definition_v1.json")
    if cycle.get("definition", "") == "":
        errors.append("cycle definition missing")

    phase = _load_json(BASE / "phase_contract.json")
    if phase.get("execution_mode") != "PLANNING_ONLY":
        errors.append("execution mode mismatch")
    if phase.get("agent_stop_state") != "WAITING_FOR_USER_TERMINAL_VERIFICATION":
        errors.append("agent stop state mismatch")

    gaps = _load_json(BASE / "cognitive_flow_gap_registry_v1.json")
    if not gaps.get("gaps"):
        errors.append("gap registry missing")

    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        return 1

    print(
        "[PASS] cognitive flow and state machine organization planning artifacts are structurally valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
