#!/usr/bin/env python3
"""Read-only final phase verifier for Context Foundation Planning v1."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
STATUS = "PLANNING_CANDIDATE"
READY = "LUNA_CONTEXT_FOUNDATION_PLANNING_READY"
REMEDIATION = "LUNA_CONTEXT_FOUNDATION_PLANNING_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "context_foundation_architecture_plan.md",
    "context_projection_schema_candidate.json",
    "context_input_contract_candidate.json",
    "context_output_boundary_contract_candidate.json",
    "context_lifecycle_model_candidate.json",
    "context_complexity_evaluation_candidate.json",
    "context_foundation_scenario_validation.json",
    "context_boundary_risk_registry.json",
    "context_foundation_summary.md",
    "context_foundation_change_manifest.json",
    "phase_contract.json",
    "verify_context_foundation_planning_v1.py",
}

JSON_FILES = REQUIRED_FILES - {
    "context_foundation_architecture_plan.md",
    "context_foundation_summary.md",
    "verify_context_foundation_planning_v1.py",
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

    plan = (BASE / "context_foundation_architecture_plan.md").read_text(encoding="utf-8")
    for token, check_id in [
        (STATUS, "plan_status"),
        ("Context 是多个独立 Owner 输出的只读 Projection 的组合", "plan_context_position"),
        ("Context 是背景，不是结论", "plan_background_not_conclusion"),
        ("Field Context", "plan_field_context"),
        ("Observation Context", "plan_observation_context"),
        ("Memory Context", "plan_memory_context"),
        ("Self Context", "plan_self_context"),
        ("Role Context", "plan_role_context"),
        ("Relationship Context", "plan_relationship_context"),
        ("Emotion Context", "plan_emotion_context"),
        ("Context Foundation 不生成 Intent", "plan_no_intent"),
        ("Context Foundation 不解释“为什么”", "plan_no_causal"),
        ("Context Foundation 不排序方案", "plan_no_decision"),
        ("不能直读 Raw Memory", "plan_no_raw_memory"),
        ("Context 不能修改 Field", "plan_no_field_mutation"),
    ]:
        check(token in plan, check_id)

    schema = docs.get("context_projection_schema_candidate.json", {})
    required_schema_fields = {
        "context_id", "context_version", "temporal_scope", "field_projection",
        "self_projection", "role_projection", "relationship_projection",
        "memory_projection", "emotion_projection", "observation_projection",
        "uncertainty", "provenance", "trace_reference", "status",
    }
    check(required_schema_fields <= set(schema), "schema_required_fields")
    semantics = schema.get("candidate_semantics", {})
    check(semantics.get("unknown_supported") is True, "schema_unknown")
    check(semantics.get("uncertain_supported") is True, "schema_uncertain")
    check(semantics.get("multiple_candidate_supported") is True, "schema_multiple_candidate")
    check(semantics.get("source_owner_precedence") is True, "schema_source_precedence")
    check(schema.get("provenance") != [], "schema_provenance")
    check(schema.get("trace_reference", {}).get("required") is True, "schema_trace")
    check(schema.get("active_schema") is False, "schema_inactive")
    schema_forbidden = set(schema.get("forbidden_fields", []))
    check({"intent", "causal_explanation", "decision", "action", "memory_mutation", "field_mutation"} <= schema_forbidden, "schema_forbidden_fields")

    input_contract = docs.get("context_input_contract_candidate.json", {})
    inputs = input_contract.get("inputs", [])
    required_producers = {
        "Field State System", "Observation Manager", "Memory System", "Self System",
        "Role System / Social Self", "Relationship System / Social Self",
        "Emotion Context Boundary / Integration Layer",
    }
    check({item.get("producer") for item in inputs} == required_producers, "input_producers")
    check(all(item.get("input_type") for item in inputs), "input_types")
    check(all(item.get("allowed_input") for item in inputs), "input_allowed")
    check(all(item.get("forbidden_input") for item in inputs), "input_forbidden")
    check(all(item.get("write_authority") for item in inputs), "input_write_authority")
    check(all(item.get("status") == STATUS for item in inputs), "input_candidate_status")
    check(input_contract.get("projection_only") is True, "input_projection_only")
    check(input_contract.get("direct_database_access") is False, "input_no_database")
    check(input_contract.get("direct_runtime_access") is False, "input_no_runtime")
    check(input_contract.get("direct_raw_memory_access") is False, "input_no_raw_memory")
    check(input_contract.get("source_owner_precedence") is True, "input_source_precedence")
    check(input_contract.get("active_contract") is False, "input_contract_inactive")

    output = docs.get("context_output_boundary_contract_candidate.json", {})
    check(set(output.get("allowed_consumers", [])) == {"Personal Cognitive Network Governance", "Intent Governance", "Causal Reasoning Governance"}, "output_consumers")
    check({"Current Context Candidate", "Context Reference", "Context Confidence", "Temporal Scope"} <= set(output.get("allowed_outputs", [])), "output_allowed")
    check({"Intent", "Causal Explanation", "Decision", "Action", "Memory Mutation", "Field Mutation"} <= set(output.get("forbidden_outputs", [])), "output_forbidden")
    check(output.get("candidate_only") is True, "output_candidate_only")
    check(output.get("read_only_projection") is True, "output_read_only")
    check(output.get("trace_required") is True, "output_trace")
    check(output.get("provenance_required") is True, "output_provenance")
    check(output.get("source_owner_transfer") is False, "output_no_owner_transfer")
    check(output.get("active_contract") is False, "output_contract_inactive")

    lifecycle = docs.get("context_lifecycle_model_candidate.json", {})
    states = ["Create", "Activate", "Update", "Suspend", "Expire", "Archive"]
    check(lifecycle.get("states") == states, "lifecycle_states")
    transitions = lifecycle.get("transitions", [])
    required_edges = {
        "Create -> Activate", "Activate -> Update", "Update -> Activate",
        "Activate -> Suspend", "Suspend -> Activate", "Activate -> Expire",
        "Suspend -> Expire", "Expire -> Archive",
    }
    check({item.get("transition") for item in transitions} == required_edges, "lifecycle_transitions")
    check(all(item.get("state") and item.get("trigger") and item.get("allowed") is True for item in transitions), "lifecycle_transition_fields")
    check(lifecycle.get("physical_field_switch_forces_reset") is False, "lifecycle_no_field_reset")
    check(lifecycle.get("expire_is_not_memory") is True, "lifecycle_expire_not_memory")
    check(lifecycle.get("archive_owns_source_objects") is False, "lifecycle_archive_no_owner")
    check(lifecycle.get("runtime_state_machine_implemented") is False, "lifecycle_no_runtime")

    complexity = docs.get("context_complexity_evaluation_candidate.json", {})
    scenarios = complexity.get("scenarios", [])
    by_type = {item.get("scenario_type"): item for item in scenarios}
    for item in ["Weather", "Time", "Simple Query"]:
        check(by_type.get(item, {}).get("complexity_level") == "LOW", f"complexity_low:{item}")
    for item in ["Multi-constraint Planning", "Relationship", "Emotion Expression", "Life Choice"]:
        check(by_type.get(item, {}).get("complexity_level") == "HIGH", f"complexity_high:{item}")
    check(all(item.get("required_context_scope") and item.get("reason") for item in scenarios), "complexity_scope_reason")
    check(complexity.get("automatic_deep_expansion") is False, "complexity_no_auto_deep")

    validation = docs.get("context_foundation_scenario_validation.json", {})
    validation_scenarios = validation.get("scenarios", [])
    required_scenario_ids = {
        "SCENARIO-01-OFFICE-TO-HOME", "SCENARIO-02-WEATHER-CHAT",
        "SCENARIO-03-TIRED-EXPRESSION", "SCENARIO-04-CHANGE-JOB",
    }
    check({item.get("scenario_id") for item in validation_scenarios} == required_scenario_ids, "scenario_ids")
    check(all(item.get("expected_context") for item in validation_scenarios), "scenario_expected_context")
    check(all(item.get("validation_focus") for item in validation_scenarios), "scenario_validation_focus")
    check(all(item.get("forbidden_results") for item in validation_scenarios), "scenario_forbidden_results")
    check(all(item.get("passes_boundary") is True for item in validation_scenarios), "scenario_boundaries")
    check(validation.get("scenario_count") == 4, "scenario_count")
    check(validation.get("all_context_only") is True, "scenario_context_only")
    check(validation.get("implementation_test_executed") is False, "scenario_no_execution")

    risks = docs.get("context_boundary_risk_registry.json", {})
    risk_records = risks.get("risks", [])
    required_risks = {
        "Context becomes an Intent Engine",
        "Context directly accesses or writes Memory",
        "Context produces a Causal Explanation",
        "Context modifies Reality or Field State",
        "Context replaces Personal Cognitive Network",
    }
    check(required_risks <= {item.get("risk") for item in risk_records}, "risk_required")
    check(all(item.get("severity") in {"LOW", "MEDIUM", "HIGH"} for item in risk_records), "risk_severity")
    check(all(item.get("mitigation") for item in risk_records), "risk_mitigation")
    check(all(item.get("blocker") is False for item in risk_records), "risk_no_open_blocker")
    check(risks.get("risk_count") == len(risk_records), "risk_count")
    check(risks.get("open_blocker_count") == 0, "risk_blocker_count")
    check(risks.get("automatic_remediation_allowed") is False, "risk_no_auto_remediation")

    summary = (BASE / "context_foundation_summary.md").read_text(encoding="utf-8")
    for token, check_id in [
        (STATUS, "summary_status"),
        ("Context consumes Projection Candidates only", "summary_projection_only"),
        ("Context does not output Intent", "summary_no_intent"),
        ("has not implemented Context Skeleton", "summary_no_implementation"),
        ("does not authorize Context Skeleton Implementation", "summary_no_next_phase"),
    ]:
        check(token in summary, check_id)

    manifest = docs.get("context_foundation_change_manifest.json", {})
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_created_files")
    for key in [
        "modified_existing_files", "deleted_files", "moved_files", "renamed_files",
        "code_files_changed", "runtime_files_changed", "active_schema_files_changed",
        "active_contract_files_changed", "owner_metadata_files_changed",
    ]:
        check(manifest.get(key) == [], f"manifest_empty:{key}")
    for key in [
        "schema_changed", "contract_changed", "owner_metadata_changed",
        "implementation_started", "runtime_changed", "database_accessed",
        "model_invoked", "candidate_activated",
    ]:
        check(manifest.get(key) is False, f"manifest_false:{key}")
    check(manifest.get("candidate_schema_created") is True, "manifest_candidate_schema")
    check(manifest.get("candidate_contracts_created") is True, "manifest_candidate_contracts")
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
    check(contract.get("implementation") is False, "phase_contract_no_implementation")
    check(contract.get("runtime_change") is False, "phase_contract_no_runtime")
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
        tree = ast.parse((BASE / "verify_context_foundation_planning_v1.py").read_text(encoding="utf-8"))
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
