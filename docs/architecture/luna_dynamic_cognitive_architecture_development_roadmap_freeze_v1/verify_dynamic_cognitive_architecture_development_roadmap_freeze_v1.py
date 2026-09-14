#!/usr/bin/env python3
"""Read-only V2 final verifier for the Dynamic Cognitive Architecture roadmap freeze."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
STATUS = "DEVELOPMENT_ROADMAP_FREEZE_CANDIDATE"
READY = "LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_DEVELOPMENT_ROADMAP_FREEZE_READY"
REMEDIATION = "LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_DEVELOPMENT_ROADMAP_FREEZE_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "luna_dynamic_cognitive_architecture_development_roadmap_v1.md",
    "development_phase_registry_v1.json",
    "development_dependency_graph_v1.json",
    "phase_gate_contract_v1.json",
    "cross_cutting_capability_boundary_v1.json",
    "context_foundation_entry_contract_v1.json",
    "roadmap_change_control_v1.json",
    "roadmap_freeze_summary.md",
    "roadmap_change_manifest.json",
    "phase_contract.json",
    "verify_dynamic_cognitive_architecture_development_roadmap_freeze_v1.py",
}

JSON_FILES = REQUIRED_FILES - {
    "luna_dynamic_cognitive_architecture_development_roadmap_v1.md",
    "roadmap_freeze_summary.md",
    "verify_dynamic_cognitive_architecture_development_roadmap_freeze_v1.py",
}


def load_json(name: str) -> dict[str, Any]:
    value = json.loads((BASE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain an object")
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
        check(document.get("roadmap_status") == STATUS, f"roadmap_status:{name}")

    registry = docs.get("development_phase_registry_v1.json", {})
    phases = registry.get("phases", [])
    required_names = [
        "Context Foundation",
        "Personal Cognitive Network",
        "Intent Architecture",
        "Causal Reasoning Engine",
        "A/B Simulation & Decision Support",
        "Experience Compression & Cognitive Evolution",
    ]
    check([item.get("sequence") for item in phases] == list(range(6)), "phase_sequence")
    check([item.get("name") for item in phases] == required_names, "phase_names")
    check(len({item.get("phase_id") for item in phases}) == 6, "phase_ids_unique")
    check(all(item.get("entry_gate") and item.get("exit_gate") for item in phases), "phase_gates_present")
    check(all(item.get("implementation_status") == "FUTURE_PHASE_NOT_AUTHORIZED" for item in phases), "phases_not_authorized")
    check(all(item.get("next_phase_auto_entry") is False for item in phases), "no_auto_entry")
    check(registry.get("phase_count") == 6, "phase_count")
    check(registry.get("order_frozen") is True, "order_frozen")
    check(registry.get("parallel_mainline_allowed") is False, "no_parallel_mainline")
    check(registry.get("implementation_authorized") is False, "no_implementation_authority")
    check(registry.get("phase_zero_auto_started") is False, "phase_zero_not_started")

    graph = docs.get("development_dependency_graph_v1.json", {})
    check(graph.get("nodes") == required_names, "graph_nodes_order")
    edges = graph.get("edges", [])
    expected_edges = set(zip(required_names, required_names[1:]))
    check({(item.get("from"), item.get("to")) for item in edges} == expected_edges, "graph_edges_exact")
    check(all(item.get("required") is True for item in edges), "graph_edges_required")
    check(graph.get("acyclic") is True, "graph_acyclic")
    check(graph.get("order_conflicts") == [], "graph_no_order_conflicts")
    check(len(graph.get("forbidden_shortcuts", [])) >= 8, "graph_forbidden_shortcuts")
    check(graph.get("implementation_authorized") is False, "graph_no_implementation")

    gates = docs.get("phase_gate_contract_v1.json", {})
    gate_records = gates.get("gates", [])
    check(len(gate_records) == 7, "gate_count")
    check(len({item.get("gate_id") for item in gate_records}) == 7, "gate_ids_unique")
    check(all(item.get("requirements") for item in gate_records), "gate_requirements_complete")
    check(all(item.get("failure_action") for item in gate_records), "gate_failure_actions")
    check(gates.get("gate_bypass_allowed") is False, "gate_no_bypass")
    check(gates.get("phase_self_authorization_allowed") is False, "gate_no_self_authorization")
    check(gates.get("active_contract") is False, "gate_contract_inactive")

    cross = docs.get("cross_cutting_capability_boundary_v1.json", {})
    capabilities = cross.get("capabilities", [])
    required_capabilities = {"Emotion Engine", "Memory System", "Observation Axis"}
    check({item.get("capability") for item in capabilities} == required_capabilities, "cross_cutting_capabilities")
    check(set(cross.get("required_capabilities", [])) == required_capabilities, "cross_cutting_registry")
    check(all(item.get("owner_retained") for item in capabilities), "cross_cutting_owner_retained")
    check(all(item.get("forbidden_responsibilities") for item in capabilities), "cross_cutting_forbidden_responsibilities")
    check(all(item.get("independent_mainline") is False for item in capabilities), "cross_cutting_no_mainline")
    check(cross.get("owner_transfer_allowed") is False, "cross_cutting_no_owner_transfer")
    check(cross.get("runtime_activation_authorized") is False, "cross_cutting_no_runtime")

    context = docs.get("context_foundation_entry_contract_v1.json", {})
    required_contexts = {"Field Context", "Self Context", "Role Context", "Relationship Context", "Temporal Context"}
    context_objects = context.get("context_objects", [])
    check({item.get("object") for item in context_objects} == required_contexts, "context_objects_complete")
    check(all(item.get("source_owner") for item in context_objects), "context_source_owners")
    check(all(item.get("required_content") for item in context_objects), "context_required_content")
    check(context.get("source_owner_precedence") is True, "context_source_owner_precedence")
    check(context.get("context_is_not_reality_owner") is True, "context_not_reality_owner")
    check(context.get("context_is_not_personal_cognitive_network") is True, "context_not_pcn")
    check(context.get("intent_generation_allowed") is False, "context_no_intent")
    check(context.get("causal_reasoning_allowed") is False, "context_no_causal")
    check(context.get("memory_write_allowed") is False, "context_no_memory_write")
    check(context.get("runtime_required_by_default") is False, "context_no_default_runtime")
    downstream = context.get("acceptance_scenario", {}).get("downstream_not_phase_zero_output", {})
    check(downstream.get("owner") == "Intent Governance", "scenario_intent_owner")
    check(downstream.get("earliest_phase") == "Phase 2", "scenario_intent_phase")
    check(context.get("active_contract") is False, "context_contract_inactive")
    check(context.get("implementation_authorized") is False, "context_implementation_not_authorized")

    control = docs.get("roadmap_change_control_v1.json", {})
    check(len(control.get("change_process", [])) >= 9, "change_process_complete")
    check(len(control.get("changes_requiring_exception", [])) >= 8, "change_exception_scope")
    check(control.get("implementation_phase_may_self_approve_change") is False, "change_no_self_approval")
    check(control.get("automatic_roadmap_update_allowed") is False, "change_no_automatic_update")
    check(control.get("exception_registry") == [], "change_no_current_exceptions")
    check(control.get("roadmap_activated") is False, "roadmap_not_activated")

    manifest = docs.get("roadmap_change_manifest.json", {})
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_created_files")
    for key in [
        "modified_existing_files", "deleted_files", "moved_files", "renamed_files",
        "code_files_changed", "runtime_files_changed", "schema_files_changed",
        "contract_files_changed", "owner_metadata_files_changed", "architecture_files_changed",
    ]:
        check(manifest.get(key) == [], f"manifest_empty:{key}")
    for key in [
        "architecture_changed", "runtime_changed", "schema_changed", "contract_changed",
        "owner_metadata_changed", "migration_executed", "implementation_executed",
        "context_foundation_started",
    ]:
        check(manifest.get(key) is False, f"manifest_false:{key}")
    check(manifest.get("planning_assets_only") is True, "manifest_planning_only")

    contract = docs.get("phase_contract.json", {})
    check(contract.get("execution_mode") == "Planning Only", "contract_mode")
    check(contract.get("previous_phase_decision") == "LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_INTEGRATION_AUDIT_READY", "contract_previous_decision")
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
    check(required_contract_fields <= set(contract), "contract_required_fields")
    check(len(contract.get("required_final_files", [])) == len(REQUIRED_FILES), "contract_required_file_count")
    check(contract.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "contract_stop_point")
    check(contract.get("expected_success_decision") == READY, "contract_success")
    check(contract.get("expected_failure_decision") == REMEDIATION, "contract_failure")
    check(contract.get("next_phase_auto_entry") is False, "contract_no_auto_entry")
    authority = contract.get("verification_authority", {})
    check(authority.get("V0") == "Agent", "authority_v0")
    check(authority.get("V1") == "NOT_AUTHORIZED", "authority_v1")
    check(authority.get("V2") == "USER_TERMINAL_ONLY", "authority_v2")
    check(authority.get("V3") == "CHATGPT_ONLY", "authority_v3")

    roadmap = (BASE / "luna_dynamic_cognitive_architecture_development_roadmap_v1.md").read_text(encoding="utf-8")
    summary = (BASE / "roadmap_freeze_summary.md").read_text(encoding="utf-8")
    for token, check_id in [
        (STATUS, "roadmap_status_token"),
        ("Phase 0 — Context Foundation", "roadmap_phase_zero"),
        ("Phase 5 — Experience Compression & Cognitive Evolution", "roadmap_phase_five"),
        ("does not generate or write Intent", "roadmap_no_context_intent"),
        ("does not activate Phase 0 automatically", "roadmap_no_auto_activation"),
    ]:
        check(token in roadmap, check_id)
    check(STATUS in summary, "summary_status")
    check("does not authorize implementation" in summary, "summary_no_implementation")
    check("requires a separate phase instruction" in summary, "summary_separate_phase")

    try:
        tree = ast.parse((BASE / "verify_dynamic_cognitive_architecture_development_roadmap_freeze_v1.py").read_text(encoding="utf-8"))
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
