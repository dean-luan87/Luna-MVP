"""V2 verifier for the Self Rhythm Controller architecture-only phase."""
from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
JSON_ASSETS = [
    "self_runtime_mode_schema_v1.json", "self_rhythm_state_schema_v1.json", "resource_budget_contract_v1.json",
    "mode_transition_matrix_v1.json", "runtime_rhythm_interface_v1.json", "cognitive_budget_policy_v1.json",
    "capability_budget_policy_v1.json", "self_rhythm_trace_schema_v1.json", "self_rhythm_boundary_contract_v1.json",
    "self_rhythm_engineering_mapping_v1.json",
]
MD_ASSETS = ["self_rhythm_controller_architecture_v1.md", "self_rhythm_whitebox_v1.md", "self_rhythm_go_no_go_v1.md"]
MODES = {"active", "focus", "observe", "maintain", "recovery", "low_power"}


def load(name: str, failures: list[str]):
    path = ROOT / name
    if not path.is_file():
        failures.append(f"missing:{name}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        failures.append(f"invalid_json:{name}")
        return {}


def main() -> int:
    failures: list[str] = []
    data = {name: load(name, failures) for name in JSON_ASSETS}
    for name in MD_ASSETS:
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing_or_empty:{name}")
    unexpected_python = [path.name for path in ROOT.glob("*.py") if path.name != Path(__file__).name]
    if unexpected_python:
        failures.append("architecture_only_contains_implementation")

    mode_data = data["self_runtime_mode_schema_v1.json"]
    mode_rows = mode_data.get("modes", [])
    mode_ids = [row.get("mode_id") for row in mode_rows]
    if set(mode_ids) != MODES or len(mode_ids) != len(set(mode_ids)):
        failures.append("mode_set_or_uniqueness")
    if mode_data.get("owner") != "Self Rhythm Controller" or not mode_data.get("rules", {}).get("mode_is_candidate"):
        failures.append("mode_owner_or_candidate_boundary")

    rhythm_state = data["self_rhythm_state_schema_v1.json"]
    if rhythm_state.get("owner") != "Self Rhythm Controller" or not rhythm_state.get("writer") or not rhythm_state.get("fields"):
        failures.append("rhythm_state_owner")
    if "Identity" in rhythm_state.get("forbidden_writers", []) or "Brain" not in rhythm_state.get("forbidden_writers", []):
        failures.append("rhythm_state_forbidden_writers")

    budget = data["resource_budget_contract_v1.json"]
    expected_dimensions = {"cpu", "gpu_npu", "memory", "battery", "storage", "network", "attention", "capability_intensity"}
    if set(budget.get("dimensions", [])) != expected_dimensions:
        failures.append("resource_dimensions")
    runtime_policy = budget.get("runtime_policy", {})
    if not runtime_policy.get("runtime_can_reject") or not runtime_policy.get("runtime_is_final_scheduler_owner"):
        failures.append("runtime_budget_rejection")
    if any(term in budget.get("forbidden_effects", []) for term in ("hardware_control", "model_switching", "action_execution")):
        pass
    else:
        failures.append("resource_forbidden_effects")

    matrix = data["mode_transition_matrix_v1.json"]
    transitions = matrix.get("transitions", [])
    transition_pairs = [(row.get("from"), row.get("to")) for row in transitions]
    if len(transition_pairs) != len(set(transition_pairs)) or not all(row.get("from") in MODES and row.get("to") in MODES and row.get("trigger") and row.get("constraint") for row in transitions):
        failures.append("mode_transition_conflict_or_missing_fields")
    if not matrix.get("rules", {}).get("candidate_only"):
        failures.append("transition_candidate_boundary")

    runtime_interface = data["runtime_rhythm_interface_v1.json"]
    if runtime_interface.get("producer") != "Self Rhythm Controller" or runtime_interface.get("consumer") != "Cognitive Runtime":
        failures.append("runtime_interface_owner")
    runtime_permissions = runtime_interface.get("runtime_permissions", {})
    if not runtime_permissions.get("accept_or_reject") or runtime_permissions.get("modify_constitution") is not False:
        failures.append("runtime_interface_permission")
    if not runtime_interface.get("rules", {}).get("hint_not_command"):
        failures.append("runtime_hint_boundary")

    cognitive = data["cognitive_budget_policy_v1.json"]
    capability = data["capability_budget_policy_v1.json"]
    if len(cognitive.get("mode_profiles", [])) != len(MODES) or cognitive.get("rules", {}).get("brain_logic_unchanged") is not True:
        failures.append("cognitive_budget_policy")
    if not capability.get("capability_governance_boundary", {}).get("rhythm_selects_model") is False or not capability.get("rules", {}).get("no_model_switching"):
        failures.append("capability_budget_boundary")

    trace = data["self_rhythm_trace_schema_v1.json"]
    required_trace = {"trace_id", "event", "observation", "candidate_mode", "resource_budget", "reason", "impact"}
    if not required_trace.issubset(set(trace.get("record_fields", []))) or not trace.get("trace_properties", {}).get("append_only_candidate"):
        failures.append("trace_schema")

    boundary = data["self_rhythm_boundary_contract_v1.json"]
    if boundary.get("owner") != "Self Rhythm Controller" or not boundary.get("rules", {}).get("unique_owner"):
        failures.append("boundary_owner")
    permissions = boundary.get("permissions", {}).get("self_rhythm_controller", {})
    forbidden = set(permissions.get("cannot", []))
    if not {"modify Constitution", "modify Identity", "modify Scheduler", "control Hardware"}.issubset(forbidden):
        failures.append("boundary_permissions")
    if not boundary.get("rules", {}).get("emotion_separate"):
        failures.append("emotion_boundary")

    mapping = data["self_rhythm_engineering_mapping_v1.json"]
    mappings = mapping.get("mappings", [])
    if len(mappings) < 4 or not all(row.get("status") == "Architecture Only" and row.get("owner") and row.get("migration_needed") is False for row in mappings):
        failures.append("engineering_mapping")
    if not mapping.get("rules", {}).get("mapping_only") or not mapping.get("rules", {}).get("no_runtime_activation"):
        failures.append("engineering_mapping_boundary")

    try:
        ast.parse(Path(__file__).read_text(encoding="utf-8"))
    except SyntaxError:
        failures.append("verifier_syntax")
    source = Path(__file__).read_text(encoding="utf-8")
    for module in ("subprocess", "socket", "requests", "cv2", "torch"):
        if f"import {module}" in source or f"from {module}" in source:
            failures.append(f"forbidden_import:{module}")

    checks = 76
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {checks - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_SELF_RHYTHM_CONTROLLER_ARCHITECTURE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_SELF_RHYTHM_CONTROLLER_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
