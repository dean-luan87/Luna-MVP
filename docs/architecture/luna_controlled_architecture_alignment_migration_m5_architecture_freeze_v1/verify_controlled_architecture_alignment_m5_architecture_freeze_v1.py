#!/usr/bin/env python3
"""Read-only final verifier for the M5 architecture-freeze candidate phase."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
REPO_ROOT = BASE.parents[2]

REQUIRED_FILES = {
    "architecture_freeze_record.json",
    "canonical_architecture_freeze.md",
    "future_development_boundary_rules.json",
    "future_implementation_entry_rules.md",
    "architecture_dependency_freeze_map.json",
    "architecture_freeze_exception_registry.json",
    "architecture_freeze_validation_report.md",
    "m5_change_manifest.json",
    "phase_contract.json",
    "verify_controlled_architecture_alignment_m5_architecture_freeze_v1.py",
}

JSON_FILES = {
    "architecture_freeze_record.json",
    "future_development_boundary_rules.json",
    "architecture_dependency_freeze_map.json",
    "architecture_freeze_exception_registry.json",
    "m5_change_manifest.json",
    "phase_contract.json",
}

MARKDOWN_FILES = {
    "canonical_architecture_freeze.md",
    "future_implementation_entry_rules.md",
    "architecture_freeze_validation_report.md",
}

REQUIRED_FREEZE_SCOPE = {
    "Dynamic Cognitive Architecture v2",
    "Owner Boundary",
    "Schema Boundary",
    "Contract Boundary",
    "Runtime Boundary",
    "Development Governance",
}

REQUIRED_EXCLUDED_SCOPE_TERMS = {
    "code modification",
    "Runtime modification or activation",
    "Baseline modification or replacement",
    "Active Schema modification",
    "Active Contract modification",
    "Candidate Contract activation",
    "Personal Cognitive Network implementation",
    "Causal Runtime implementation",
    "Intent Runtime implementation",
    "B Route Runtime implementation",
    "Adapter implementation",
    "migration execution",
}

REQUIRED_RULE_IDS = {
    "NO_SECOND_COGNITIVE_ARCHITECTURE",
    "RUNTIME_NO_COGNITIVE_OWNERSHIP",
    "MODEL_MANAGER_NO_REASONING_OWNERSHIP",
    "MEMORY_NO_DIRECT_DECISION",
    "OBSERVATION_NO_DIRECT_FACT",
    "TASK_MANAGER_NO_INTENT",
    "CANDIDATE_REQUIRES_VALIDATION_BEFORE_REALITY",
}

REQUIRED_ALLOWED_DEPENDENCIES = {
    ("Field", "Context"),
    ("Context", "Cognitive"),
    ("Cognitive", "Decision"),
    ("Decision", "Task"),
    ("Task", "Runtime"),
}

REQUIRED_FORBIDDEN_DEPENDENCIES = {
    ("Runtime", "Cognitive Ownership"),
    ("Model", "Decision Ownership"),
    ("Memory", "Reality Override"),
}

REQUIRED_PHASE_CONTRACT_FIELDS = {
    "Phase",
    "Stage",
    "Execution Mode",
    "Current Work Description",
    "Previous Phase",
    "Previous Phase Decision",
    "Input Assets",
    "Required Pre-Read",
    "Target Directory",
    "Scope",
    "Out Of Scope",
    "Required Final Files",
    "Implementation Principles",
    "Required Checks",
    "Negative Guards",
    "Verification Authority",
    "Allowed Agent Checks",
    "Allowed Agent Execution",
    "Prohibited Agent Execution",
    "Agent Stop Point",
    "User Terminal Commands",
    "Expected Success Decision",
    "Expected Next",
    "Expected Failure Decision",
    "Expected Failure Next",
    "Stop Condition",
    "Blocker Conditions",
    "Completion Report Format",
    "Current Status Contract",
}

ALLOWED_IMPORT_ROOTS = {"__future__", "ast", "json", "pathlib", "typing"}
FORBIDDEN_MUTATION_CALLS = {
    "write_text",
    "write_bytes",
    "unlink",
    "rename",
    "replace",
    "mkdir",
    "rmdir",
    "touch",
    "chmod",
}


def load_json(name: str) -> Any:
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def main() -> int:
    checks: list[str] = []
    failed: list[str] = []

    def check(condition: bool, name: str) -> None:
        checks.append(name)
        if not condition:
            failed.append(name)

    actual_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_files == REQUIRED_FILES, "exact_required_file_set")

    data: dict[str, Any] = {}
    for name in sorted(JSON_FILES):
        try:
            data[name] = load_json(name)
            check(True, f"json_parse:{name}")
        except (OSError, json.JSONDecodeError):
            data[name] = {}
            check(False, f"json_parse:{name}")

    markdown: dict[str, str] = {}
    for name in sorted(MARKDOWN_FILES):
        try:
            markdown[name] = (BASE / name).read_text(encoding="utf-8")
            check(bool(markdown[name].strip()), f"markdown_nonempty:{name}")
        except OSError:
            markdown[name] = ""
            check(False, f"markdown_nonempty:{name}")

    for name in sorted(JSON_FILES):
        check(data.get(name, {}).get("freeze_status") == "ARCHITECTURE_FREEZE_CANDIDATE", f"freeze_candidate:{name}")
    for name in sorted(MARKDOWN_FILES):
        check("ARCHITECTURE_FREEZE_CANDIDATE" in markdown.get(name, ""), f"freeze_candidate:{name}")

    record = data.get("architecture_freeze_record.json", {})
    check(record.get("architecture_version") == "Luna Dynamic Cognitive Architecture v2.0", "freeze_architecture_version")
    check(set(record.get("freeze_scope", [])) == REQUIRED_FREEZE_SCOPE, "freeze_scope_complete")
    check(REQUIRED_EXCLUDED_SCOPE_TERMS.issubset(set(record.get("excluded_scope", []))), "excluded_scope_complete")
    source_refs = record.get("source_phase_refs", [])
    check(isinstance(source_refs, list) and bool(source_refs), "freeze_source_refs_present")
    check(all(isinstance(ref, str) and (REPO_ROOT / ref).exists() for ref in source_refs), "freeze_source_refs_exist")
    for phase_token in (
        "migration_m0_documentation_alignment",
        "migration_m1_schema_contract_alignment",
        "migration_m2_owner_metadata_alignment",
        "migration_m3_runtime_boundary_alignment",
        "migration_m4_migration_integrity_validation",
    ):
        check(any(phase_token in ref for ref in source_refs), f"freeze_source_phase:{phase_token}")
    check(record.get("effective_for_future_development") is True, "freeze_effective_for_future_development")
    check(record.get("activation_condition") == "USER_TERMINAL_V2_PASS_AND_CHATGPT_V3_APPROVAL", "freeze_activation_condition")
    check(record.get("currently_active") is False, "freeze_not_agent_activated")
    check(record.get("replaces_architecture_baseline_v2") is False, "freeze_does_not_replace_baseline")
    check(record.get("creates_second_cognitive_architecture") is False, "freeze_no_second_architecture")
    check(record.get("migration_executed") is False, "freeze_no_migration")

    canonical = markdown.get("canonical_architecture_freeze.md", "")
    ordered_flow = [
        "Reality / Evidence",
        "Field State System",
        "Observation / Context",
        "Personal Cognitive Network",
        "Intent / Causal Reasoning",
        "A/B Route",
        "Decision Boundary",
        "Task Lifecycle",
        "Runtime Execution",
        "Capability / Model",
        "Outcome",
        "Experience Compression",
        "Memory",
    ]
    flow_section = canonical.find("## 2. Canonical layered structure")
    flow_block_start = canonical.find("```text", flow_section)
    flow_block_end = canonical.find("```", flow_block_start + len("```text"))
    flow_block = canonical[flow_block_start:flow_block_end] if flow_block_start >= 0 and flow_block_end >= 0 else ""
    flow_positions = [flow_block.find(token) for token in ordered_flow]
    check(all(position >= 0 for position in flow_positions), "canonical_flow_nodes_present")
    check(flow_positions == sorted(flow_positions), "canonical_flow_order")
    for token, name in (
        ("Field State is responsible for `Reality State`", "canonical_field_reality_state"),
        ("Field State is not responsible for Decision", "canonical_field_no_decision"),
        ("`Connection`", "canonical_pcn_connection"),
        ("`Activation`", "canonical_pcn_activation"),
        ("`Projection`", "canonical_pcn_projection"),
        ("PCN is not responsible for `Object Ownership`", "canonical_pcn_no_object_ownership"),
        ("Causal Reasoning is responsible for `Candidate Reasoning`", "canonical_causal_candidate"),
        ("Causal Reasoning is not responsible for `Reality Mutation`", "canonical_causal_no_reality_mutation"),
        ("Runtime is responsible for `Execution`", "canonical_runtime_execution"),
        ("Runtime is not responsible for `Cognition`", "canonical_runtime_no_cognition"),
        ("does not replace the Constitution, Cognitive OS governance, or Luna Architecture Baseline v2.0", "canonical_authority_preserved"),
        ("does not implement or activate PCN", "canonical_no_implementation_activation"),
        ("Migration Executed: `false`", "canonical_migration_false"),
    ):
        check(token in canonical, name)

    rules = data.get("future_development_boundary_rules.json", {})
    rule_records = rules.get("rules", [])
    rule_ids = {record.get("rule_id") for record in rule_records if isinstance(record, dict)}
    check(REQUIRED_RULE_IDS.issubset(rule_ids), "future_required_rules")
    check(rules.get("rule_count") == len(rule_records), "future_rule_count")
    check(
        all(
            isinstance(record, dict)
            and all(bool(record.get(key)) for key in ("rule_id", "rule", "applies_to", "forbidden_pattern", "reason"))
            for record in rule_records
        ),
        "future_rule_fields",
    )
    check(rules.get("candidate_contracts_activated") is False, "future_rules_no_contract_activation")
    check(rules.get("migration_executed") is False, "future_rules_no_migration")

    entry = markdown.get("future_implementation_entry_rules.md", "")
    for token, name in (
        ("**Owner**", "entry_owner"),
        ("**Input**", "entry_input"),
        ("**Output**", "entry_output"),
        ("**Write Authority**", "entry_write_authority"),
        ("**Forbidden Responsibility**", "entry_forbidden_responsibility"),
        ("**Runtime Position**", "entry_runtime_position"),
        ("Architecture classification", "entry_architecture_classification"),
        ("Candidate versus Fact", "entry_candidate_fact"),
        ("Owner and Writer review", "entry_owner_writer_review"),
        ("Runtime necessity review", "entry_runtime_necessity"),
        ("Freeze exception entry", "entry_freeze_exception"),
        ("M5 creates no implementation admission", "entry_no_m5_activation"),
    ):
        check(token in entry, name)

    dependency = data.get("architecture_dependency_freeze_map.json", {})
    allowed_records = dependency.get("allowed_dependencies", [])
    forbidden_records = dependency.get("forbidden_dependencies", [])
    allowed_pairs = {(record.get("from"), record.get("to")) for record in allowed_records if isinstance(record, dict)}
    forbidden_pairs = {(record.get("from"), record.get("to")) for record in forbidden_records if isinstance(record, dict)}
    check(REQUIRED_ALLOWED_DEPENDENCIES.issubset(allowed_pairs), "dependency_required_allowed")
    check(REQUIRED_FORBIDDEN_DEPENDENCIES.issubset(forbidden_pairs), "dependency_required_forbidden")
    check(all(record.get("status") == "ALLOWED" and bool(record.get("condition")) for record in allowed_records), "dependency_allowed_fields")
    check(all(record.get("status") == "FORBIDDEN" and bool(record.get("reason")) for record in forbidden_records), "dependency_forbidden_fields")
    check(dependency.get("creates_runtime_call_graph") is False, "dependency_not_runtime_call_graph")
    check(dependency.get("adapter_created") is False, "dependency_no_adapter")
    check(dependency.get("migration_executed") is False, "dependency_no_migration")

    exception = data.get("architecture_freeze_exception_registry.json", {})
    check(exception.get("default_status") == "FUTURE_ONLY", "exception_future_only")
    check(exception.get("exceptions") == [], "exception_registry_empty")
    check(exception.get("exception_count") == 0, "exception_count_zero")
    process = exception.get("exception_process", {})
    check(process.get("approval_required") is True, "exception_approval_required")
    check(process.get("allowed_status") == "FUTURE_ONLY", "exception_allowed_status")
    check(process.get("implicit_exception_allowed") is False, "exception_no_implicit")
    check(process.get("implementation_change_may_self_approve") is False, "exception_no_self_approval")
    required_steps = set(process.get("required_steps", []))
    for step in (
        "separate phase instruction",
        "architecture impact analysis",
        "Owner and Writer review",
        "Schema and Contract compatibility review",
        "Runtime boundary review",
        "migration and rollback plan",
        "user-terminal V2 final verification",
        "ChatGPT V3 audit",
    ):
        check(step in required_steps, f"exception_step:{step}")
    check(exception.get("migration_executed") is False, "exception_no_migration")

    report = markdown.get("architecture_freeze_validation_report.md", "")
    for token, name in (
        ("M0 Documentation Alignment: completed", "report_m0_complete"),
        ("M1 Schema / Contract Alignment: completed", "report_m1_complete"),
        ("M2 Owner Metadata Alignment: completed", "report_m2_complete"),
        ("M3 Runtime Boundary Alignment: completed", "report_m3_complete"),
        ("M4 Migration Integrity Validation: completed", "report_m4_complete"),
        ("Architecture consistency", "report_architecture_consistency"),
        ("Owner consistency", "report_owner_consistency"),
        ("Contract consistency", "report_contract_consistency"),
        ("Runtime consistency", "report_runtime_consistency"),
        ("Status: `CONSISTENT`", "report_consistent_status"),
        ("Migration Executed: `false`", "report_migration_false"),
        ("does not activate the freeze by itself", "report_no_self_activation"),
    ):
        check(token in report, name)

    manifest = data.get("m5_change_manifest.json", {})
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_created_file_set")
    for field in (
        "modified_existing_files",
        "deleted_files",
        "moved_files",
        "renamed_files",
        "code_files_changed",
        "runtime_files_changed",
        "baseline_files_changed",
        "active_schema_files_changed",
        "active_contract_files_changed",
        "active_registry_files_changed",
        "active_owner_metadata_changed",
    ):
        check(manifest.get(field) == [], f"manifest_empty:{field}")
    for field in (
        "schema_changed",
        "contract_changed",
        "owner_metadata_changed",
        "candidate_contract_activated",
        "pcn_implementation_created",
        "causal_runtime_created",
        "intent_runtime_created",
        "b_route_runtime_created",
        "adapter_created",
        "cognitive_runtime_created",
        "migration_executed",
        "runtime_activated",
        "architecture_activated_by_agent",
    ):
        check(manifest.get(field) is False, f"manifest_false:{field}")
    check(manifest.get("planning_candidate_only") is True, "manifest_planning_candidate_only")

    phase = data.get("phase_contract.json", {})
    check(REQUIRED_PHASE_CONTRACT_FIELDS.issubset(set(phase)), "phase_required_fields")
    check(phase.get("Execution Mode") == "Planning Only", "phase_execution_mode")
    check(phase.get("Execution Profile") == "Architecture Freeze Planning", "phase_execution_profile")
    check(phase.get("Previous Phase Decision") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M4_MIGRATION_INTEGRITY_VALIDATION_READY", "phase_previous_decision")
    check(set(phase.get("Required Final Files", [])) == REQUIRED_FILES, "phase_required_file_set")
    authority = phase.get("Verification Authority", {})
    check(authority.get("V0") == "Agent", "authority_v0")
    check(authority.get("V1") == "Not Authorized", "authority_v1")
    check(authority.get("V2") == "User Terminal Only", "authority_v2")
    check(authority.get("V3") == "ChatGPT Only", "authority_v3")
    check(phase.get("Architecture Freeze Planning") is True, "phase_freeze_planning")
    check(phase.get("Architecture Activated By Agent") is False, "phase_not_agent_activated")
    check(phase.get("Migration") is False, "phase_migration_false")
    check(phase.get("Runtime Change") is False, "phase_runtime_false")
    check(phase.get("Baseline Change") is False, "phase_baseline_false")
    check(phase.get("Schema Change") is False, "phase_schema_false")
    check(phase.get("Contract Change") is False, "phase_contract_false")
    check(phase.get("Owner Metadata Change") is False, "phase_owner_metadata_false")
    check(phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_stop_point")
    expected_command = "python3 docs/architecture/luna_controlled_architecture_alignment_migration_m5_architecture_freeze_v1/verify_controlled_architecture_alignment_m5_architecture_freeze_v1.py"
    check(phase.get("User Terminal Commands") == [expected_command], "phase_terminal_command")
    check(phase.get("Expected Success Decision") == "V2_FINAL_VERIFICATION_PASSED", "phase_success_decision")
    check(phase.get("Expected Success Readiness") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M5_ARCHITECTURE_FREEZE_READY", "phase_success_readiness")
    check(phase.get("Expected Failure Decision") == "BLOCKED_BY_VERIFIER_FAILURE", "phase_failure_decision")
    check(phase.get("Expected Failure Readiness") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M5_ARCHITECTURE_FREEZE_REMEDIATION_REQUIRED", "phase_failure_readiness")

    verifier_path = BASE / "verify_controlled_architecture_alignment_m5_architecture_freeze_v1.py"
    try:
        tree = ast.parse(verifier_path.read_text(encoding="utf-8"))
        check(True, "verifier_ast_parse")
    except (OSError, SyntaxError):
        tree = ast.Module(body=[], type_ignores=[])
        check(False, "verifier_ast_parse")

    import_roots: set[str] = set()
    mutation_calls: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            import_roots.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in FORBIDDEN_MUTATION_CALLS:
                mutation_calls.add(node.func.attr)
    check(import_roots.issubset(ALLOWED_IMPORT_ROOTS), "verifier_standard_imports_only")
    check(not mutation_calls, "verifier_read_only_calls")

    print(f"CHECKS: {len(checks)}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {len(checks) - len(failed)}")
    print(f"FAILED_CHECK_COUNT: {len(failed)}")
    print(f"BLOCKER_COUNT: {len(failed)}")
    if failed:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M5_ARCHITECTURE_FREEZE_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1

    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M5_ARCHITECTURE_FREEZE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
