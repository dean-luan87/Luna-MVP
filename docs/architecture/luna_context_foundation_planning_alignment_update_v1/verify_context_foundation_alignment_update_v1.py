#!/usr/bin/env python3
"""Read-only final verifier for Context Foundation planning alignment update v1."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
STATUS = "PLANNING_CANDIDATE"
READY = "LUNA_CONTEXT_FOUNDATION_PLANNING_ALIGNMENT_UPDATE_READY"
REMEDIATION = "LUNA_CONTEXT_FOUNDATION_PLANNING_ALIGNMENT_UPDATE_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "context_foundation_emotional_carryover_alignment_update.md",
    "mental_field_continuity_schema_candidate.json",
    "field_emotional_signature_reference_candidate.json",
    "context_carryover_projection_contract_candidate.json",
    "context_boundary_alignment_update.json",
    "context_carryover_scenario_extension.json",
    "context_foundation_alignment_impact_review.md",
    "context_foundation_alignment_update_change_manifest.json",
    "phase_contract.json",
    "verify_context_foundation_alignment_update_v1.py",
}

JSON_FILES = REQUIRED_FILES - {
    "context_foundation_emotional_carryover_alignment_update.md",
    "context_foundation_alignment_impact_review.md",
    "verify_context_foundation_alignment_update_v1.py",
}


def load_json(name: str) -> dict[str, Any]:
    value = json.loads((BASE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain a JSON object")
    return value


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    def check(condition: bool, check_id: str) -> None:
        checks.append(check_id)
        if not condition:
            failures.append(check_id)

    actual_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_files == REQUIRED_FILES, "exact_file_set")

    docs: dict[str, dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        try:
            docs[name] = load_json(name)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            docs[name] = {}
            check(False, f"json_parse:{name}")

    for name, document in docs.items():
        check(document.get("status") == STATUS, f"planning_status:{name}")

    alignment = (BASE / "context_foundation_emotional_carryover_alignment_update.md").read_text(encoding="utf-8")
    for token, check_id in [
        (STATUS, "alignment_status"),
        ("Mental Field Continuity", "alignment_mental_field"),
        ("Context Carryover Projection", "alignment_carryover"),
        ("Field Emotional Signature Reference", "alignment_signature"),
        ("Mental Field Continuity is not Memory", "alignment_not_memory"),
        ("Mental Field Continuity is not Emotion State", "alignment_not_emotion_state"),
        ("Mental Field Continuity is not Causal", "alignment_not_causal"),
        ("Context -> Emotion Decision", "alignment_no_emotion_decision"),
        ("Context -> Emotion Mutation", "alignment_no_emotion_mutation"),
        ("creates no Emotion Engine", "alignment_no_emotion_engine"),
    ]:
        check(token in alignment, check_id)

    mental = docs.get("mental_field_continuity_schema_candidate.json", {})
    required_fields = {
        "continuity_id", "source_field", "current_field", "continuity_type",
        "activation_state", "intensity_reference", "duration_scope",
        "release_condition_reference", "uncertainty", "provenance", "status",
    }
    check(required_fields <= set(mental), "mental_required_fields")
    check(set(mental.get("continuity_type", [])) == {"unfinished_task", "emotional_pressure", "role_activation", "relationship_residual"}, "mental_continuity_types")
    check(mental.get("intensity_reference", {}).get("numeric_value_allowed") is False, "mental_no_numeric_intensity")
    check(mental.get("intensity_reference", {}).get("calculation_allowed") is False, "mental_no_calculation")
    uncertainty = mental.get("uncertainty", {})
    check(uncertainty.get("unknown_allowed") is True, "mental_unknown")
    check(uncertainty.get("uncertain_allowed") is True, "mental_uncertain")
    check(uncertainty.get("multiple_candidate_allowed") is True, "mental_multiple")
    boundaries = mental.get("semantic_boundaries", {})
    check(boundaries.get("is_memory") is False, "mental_not_memory")
    check(boundaries.get("is_emotion_state") is False, "mental_not_emotion")
    check(boundaries.get("is_causal_explanation") is False, "mental_not_causal")
    check(boundaries.get("is_decision") is False, "mental_not_decision")
    check(boundaries.get("is_action") is False, "mental_not_action")
    check(boundaries.get("context_reference_only") is True, "mental_reference_only")
    check(mental.get("source_owner_precedence") is True, "mental_source_precedence")
    check(mental.get("active_schema") is False, "mental_schema_inactive")

    signature = docs.get("field_emotional_signature_reference_candidate.json", {})
    signature_fields = {"field_id", "field_type", "emotional_signature_reference", "activation_context", "source_owner", "status"}
    check(signature_fields <= set(signature), "signature_required_fields")
    check(signature.get("source_owner") == "Emotion_or_Field_Owner", "signature_source_owner")
    check(signature.get("reference_only") is True, "signature_reference_only")
    check(signature.get("calculation_allowed") is False, "signature_no_calculation")
    check(signature.get("inference_allowed") is False, "signature_no_inference")
    check(signature.get("mutation_allowed") is False, "signature_no_mutation")
    check(signature.get("numeric_emotion_value_allowed") is False, "signature_no_numeric_value")
    check(signature.get("direct_value_definitions") == [], "signature_no_direct_values")
    check(set(signature.get("forbidden_direct_definitions", [])) == {"happiness", "pain", "stress_value"}, "signature_forbidden_values")
    check(signature.get("active_schema") is False, "signature_schema_inactive")
    check(signature.get("active_contract") is False, "signature_contract_inactive")

    carryover = docs.get("context_carryover_projection_contract_candidate.json", {})
    carryover_fields = {"producer", "consumer", "input_reference", "output_reference", "write_authority", "unknown_allowed", "trace_required", "status"}
    check(carryover_fields <= set(carryover), "carryover_required_fields")
    check(set(carryover.get("input_reference", [])) == {"Previous Field Projection", "Current Field Projection", "Mental State Reference"}, "carryover_inputs")
    check("Context Carryover Candidate" in carryover.get("output_reference", []), "carryover_output")
    check(carryover.get("write_authority") == "Context Carryover Candidate only", "carryover_write_authority")
    check(carryover.get("unknown_allowed") is True, "carryover_unknown")
    check(carryover.get("trace_required") is True, "carryover_trace")
    check(carryover.get("provenance_required") is True, "carryover_provenance")
    check(carryover.get("source_owner_precedence") is True, "carryover_source_precedence")
    check(carryover.get("read_only_projection") is True, "carryover_read_only")
    check({"Emotion Decision", "Emotion Mutation", "Causal Explanation", "Intent", "Decision", "Action", "Memory Mutation", "Field Mutation"} <= set(carryover.get("forbidden_outputs", [])), "carryover_forbidden_outputs")
    check(carryover.get("direct_source_mutation") is False, "carryover_no_source_mutation")
    check(carryover.get("active_contract") is False, "carryover_contract_inactive")

    boundary = docs.get("context_boundary_alignment_update.json", {})
    allowed = {(item.get("source"), item.get("intermediate"), item.get("target")) for item in boundary.get("allowed_flows", [])}
    check(("Emotion System / Emotion Context Boundary", "Mental Field Reference Candidate", "Context Foundation") in allowed, "boundary_emotion_to_context")
    check(("Field State System", "Field Projection", "Context Foundation") in allowed, "boundary_field_to_context")
    forbidden_targets = {item.get("target") for item in boundary.get("forbidden_flows", [])}
    check({"Emotion Decision", "Emotion Mutation", "Causal Explanation", "Personal Cognitive Network Activation", "Memory or Field Mutation"} <= forbidden_targets, "boundary_forbidden_flows")
    check(boundary.get("context_describes_state_only") is True, "boundary_state_only")
    check(boundary.get("context_explains_cause") is False, "boundary_no_cause")
    check(boundary.get("context_judges_reasonableness") is False, "boundary_no_judgment")
    check(boundary.get("context_initiates_change") is False, "boundary_no_change")
    check(boundary.get("owner_metadata_changed") is False, "boundary_no_owner_change")
    check(boundary.get("existing_schema_changed") is False, "boundary_no_schema_change")
    check(boundary.get("existing_contract_changed") is False, "boundary_no_contract_change")
    check(boundary.get("runtime_changed") is False, "boundary_no_runtime")

    scenarios = docs.get("context_carryover_scenario_extension.json", {})
    records = scenarios.get("scenarios", [])
    required_ids = {"CARRYOVER-01-WORK-TO-HOME", "CARRYOVER-02-LONG-WORK-PRESSURE", "CARRYOVER-03-RELATIONSHIP-CONFLICT"}
    check({item.get("scenario_id") for item in records} == required_ids, "scenario_ids")
    check(all(item.get("expected_projection") for item in records), "scenario_expected_projection")
    check(all(item.get("forbidden_results") for item in records), "scenario_forbidden_results")
    check(all(item.get("passes_boundary") is True for item in records), "scenario_boundaries")
    check(scenarios.get("scenario_count") == 3, "scenario_count")
    check(scenarios.get("all_reference_only") is True, "scenario_reference_only")
    check(scenarios.get("emotion_calculation_executed") is False, "scenario_no_emotion_calculation")
    check(scenarios.get("causal_reasoning_executed") is False, "scenario_no_causal")
    check(scenarios.get("implementation_test_executed") is False, "scenario_no_implementation")

    impact = (BASE / "context_foundation_alignment_impact_review.md").read_text(encoding="utf-8")
    for token, check_id in [
        (STATUS, "impact_status"),
        ("additive", "impact_additive"),
        ("existing `context_projection_schema_candidate.json` is unchanged", "impact_schema_unchanged"),
        ("creates no PCN", "impact_no_pcn"),
        ("creates no Causal Engine or Causal Runtime", "impact_no_causal"),
        ("does not affect", "impact_non_effect"),
        ("Memory admission, persistence, retrieval, or mutation", "impact_memory_boundary"),
    ]:
        check(token in impact, check_id)

    manifest = docs.get("context_foundation_alignment_update_change_manifest.json", {})
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_created_files")
    for key in ["modified_existing_files", "deleted_files", "moved_files", "renamed_files", "code_files_changed", "runtime_files_changed", "active_schema_files_changed", "active_contract_files_changed", "owner_metadata_files_changed"]:
        check(manifest.get(key) == [], f"manifest_empty:{key}")
    check(manifest.get("created_update_assets") is True, "manifest_update_assets")
    for key in [
        "existing_context_contract_changed", "existing_context_schema_changed",
        "emotion_engine_created", "emotion_calculation_created", "pressure_algorithm_created",
        "pcn_created", "causal_created", "runtime_changed", "implementation_started",
        "migration_executed", "candidate_activated",
    ]:
        check(manifest.get(key) is False, f"manifest_false:{key}")
    check(manifest.get("planning_assets_only") is True, "manifest_planning_only")

    contract = docs.get("phase_contract.json", {})
    required_contract_fields = {
        "phase", "stage", "execution_mode", "current_work_description", "previous_phase",
        "previous_phase_decision", "input_assets", "required_pre_read", "target_directory",
        "scope", "out_of_scope", "required_final_files", "implementation_principles",
        "required_checks", "negative_guards", "verification_authority", "allowed_agent_checks",
        "allowed_agent_execution", "prohibited_agent_execution", "agent_stop_point",
        "user_terminal_commands", "expected_success_decision", "expected_next",
        "expected_failure_decision", "expected_failure_next", "stop_condition",
        "blocker_conditions", "completion_report_format", "current_status_contract",
    }
    check(required_contract_fields <= set(contract), "phase_contract_required_fields")
    check(contract.get("execution_mode") == "Planning Only", "phase_contract_mode")
    check(contract.get("previous_phase_decision") == "LUNA_CONTEXT_FOUNDATION_PLANNING_READY", "phase_contract_previous")
    check(contract.get("implementation_started") is False, "phase_contract_no_implementation")
    check(contract.get("runtime_change") is False, "phase_contract_no_runtime")
    check(contract.get("architecture_change") is False, "phase_contract_no_architecture_change")
    check(contract.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_contract_stop")
    check(contract.get("expected_success_decision") == READY, "phase_contract_success")
    check(contract.get("expected_failure_decision") == REMEDIATION, "phase_contract_failure")
    check(contract.get("next_phase_auto_entry") is False, "phase_contract_no_auto_entry")
    check(len(contract.get("required_final_files", [])) == len(REQUIRED_FILES), "phase_contract_file_count")
    authority = contract.get("verification_authority", {})
    check(authority.get("V0") == "Agent", "authority_v0")
    check(authority.get("V1") == "NOT_AUTHORIZED", "authority_v1")
    check(authority.get("V2") == "USER_TERMINAL_ONLY", "authority_v2")
    check(authority.get("V3") == "CHATGPT_ONLY", "authority_v3")

    try:
        tree = ast.parse((BASE / "verify_context_foundation_alignment_update_v1.py").read_text(encoding="utf-8"))
        check(True, "verifier_ast_parse")
    except (OSError, SyntaxError):
        tree = ast.Module(body=[], type_ignores=[])
        check(False, "verifier_ast_parse")
    imports = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    check(imports <= {"__future__", "ast", "json", "pathlib", "typing"}, "verifier_standard_library_only")
    forbidden_calls = {"write_text", "write_bytes", "unlink", "rename", "replace", "mkdir", "rmdir", "system", "run", "Popen"}
    calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
    check(not (calls & forbidden_calls), "verifier_read_only")

    print(f"CHECKS: {len(checks)}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {len(checks) - len(failures)}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print(f"READINESS: {REMEDIATION}")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print(f"READINESS: {READY}")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
