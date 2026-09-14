#!/usr/bin/env python3
"""Static final verifier for M3 Runtime Boundary Alignment.

This verifier reads planning assets only. It does not import Luna Runtime or
business modules, execute Runtime, call a model/provider, modify files, create
an Adapter, or execute migration.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]

REQUIRED_JSON = [
    "runtime_boundary_inventory_candidate.json",
    "runtime_cognitive_boundary_matrix_candidate.json",
    "future_cognitive_runtime_gap_registry.json",
    "runtime_adapter_candidate_registry.json",
    "runtime_boundary_risk_register.json",
    "m3_change_manifest.json",
    "phase_contract.json",
]
REQUIRED_MARKDOWN = [
    "runtime_owner_boundary_review.md",
    "runtime_boundary_alignment_summary.md",
]
VERIFIER_NAME = "verify_controlled_architecture_alignment_m3_runtime_boundary_alignment_v1.py"
REQUIRED_FILES = [
    "runtime_boundary_inventory_candidate.json",
    "runtime_cognitive_boundary_matrix_candidate.json",
    "runtime_owner_boundary_review.md",
    "future_cognitive_runtime_gap_registry.json",
    "runtime_adapter_candidate_registry.json",
    "runtime_boundary_risk_register.json",
    "runtime_boundary_alignment_summary.md",
    "m3_change_manifest.json",
    "phase_contract.json",
    VERIFIER_NAME,
]

REQUIRED_RUNTIME_COMPONENTS = {
    "Runtime Foundation",
    "Task Runtime",
    "Capability Runtime",
    "Model Runtime",
    "Protocol Runtime",
    "Cognitive Layer Reference",
    "PCN Reference",
    "Causal Reference",
    "Intent Reference",
}
ACTIVE_RUNTIME_COMPONENTS = {"Runtime Foundation"}
PLANNING_RUNTIME_COMPONENTS = REQUIRED_RUNTIME_COMPONENTS - ACTIVE_RUNTIME_COMPONENTS
ALLOWED_RUNTIME_STATUSES = {"ACTIVE_EXISTING", "PLANNING_REFERENCE"}

REQUIRED_ALLOWED_FLOWS = {
    "Field State → Runtime Context",
    "Observation → Runtime Evidence Transport",
    "Model Manager → Runtime Capability Invocation",
    "Task Manager → Runtime Task Lifecycle",
}
REQUIRED_FORBIDDEN_FLOWS = {
    "Runtime → Intent Generation",
    "Runtime → Causal Reasoning",
    "Runtime → Memory Mutation",
    "Runtime → Reality Interpretation",
}

REQUIRED_FUTURE_GAPS = {
    "Personal Cognitive Network Runtime",
    "Intent Runtime",
    "Causal Runtime",
    "A/B Simulation Runtime",
    "Experience Learning Runtime",
}

REQUIRED_ADAPTERS = {
    "Field Context Read Adapter Candidate",
    "Observation Evidence Transport Adapter Candidate",
    "Governed Capability Invocation Adapter Candidate",
    "Approved Task Lifecycle Adapter Candidate",
    "Approved Cognitive Execution Request Adapter Candidate",
    "Runtime Outcome Trace Projection Adapter Candidate",
}

REQUIRED_RISKS = {
    "RUNTIME_ABSORBS_COGNITIVE_LAYER",
    "TASK_MANAGER_BECOMES_DECISION_OWNER",
    "MODEL_MANAGER_BECOMES_COGNITION_OWNER",
    "RUNTIME_MUTATES_FACT_STATE",
    "COGNITIVE_LAYER_BYPASSES_FIELD_STATE",
    "PREMATURE_FUTURE_RUNTIME_IMPLEMENTATION",
}


class Checks:
    def __init__(self) -> None:
        self.total = 0
        self.failed: list[str] = []

    def check(self, condition: bool, name: str) -> None:
        self.total += 1
        if not condition:
            self.failed.append(name)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def lower_join(values: Any) -> str:
    if not isinstance(values, list):
        return ""
    return " ".join(str(value) for value in values).lower()


def records_from(document: Any) -> list[dict[str, Any]]:
    if not isinstance(document, dict):
        return []
    records = document.get("records", [])
    if not isinstance(records, list):
        return []
    return [record for record in records if isinstance(record, dict)]


def main() -> int:
    checks = Checks()
    loaded: dict[str, Any] = {}

    for name in REQUIRED_FILES:
        checks.check((HERE / name).is_file(), f"required_file:{name}")
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    checks.check(actual_files == set(REQUIRED_FILES), "target_directory_exact_file_set")
    checks.check({path.name for path in HERE.glob("*.py")} == {VERIFIER_NAME}, "final_verifier_only_python_file")

    for name in REQUIRED_JSON:
        try:
            loaded[name] = load_json(HERE / name)
            checks.check(bool(loaded[name]), f"json_nonempty:{name}")
        except (OSError, json.JSONDecodeError):
            loaded[name] = {}
            checks.check(False, f"json_parse:{name}")

    markdown: dict[str, str] = {}
    for name in REQUIRED_MARKDOWN:
        try:
            markdown[name] = (HERE / name).read_text(encoding="utf-8")
            checks.check(len(markdown[name].strip()) > 500, f"markdown_substantial:{name}")
            checks.check("planning_candidate" in markdown[name].lower(), f"markdown_planning_status:{name}")
        except OSError:
            markdown[name] = ""
            checks.check(False, f"markdown_read:{name}")
            checks.check(False, f"markdown_planning_status:{name}")

    try:
        verifier_text = (HERE / VERIFIER_NAME).read_text(encoding="utf-8")
        verifier_tree = ast.parse(verifier_text)
        checks.check(True, "verifier_ast_parse")
    except (OSError, SyntaxError):
        verifier_text = ""
        verifier_tree = ast.Module(body=[], type_ignores=[])
        checks.check(False, "verifier_ast_parse")

    for name in REQUIRED_JSON:
        document = loaded.get(name, {})
        checks.check(isinstance(document, dict), f"json_object:{name}")
        checks.check(document.get("planning_status") == "PLANNING_CANDIDATE", f"planning_status:{name}")

    inventory = loaded.get("runtime_boundary_inventory_candidate.json", {})
    inventory_records = records_from(inventory)
    inventory_by_component = {
        record.get("runtime_component"): record
        for record in inventory_records
        if isinstance(record.get("runtime_component"), str)
    }
    checks.check(set(inventory_by_component) == REQUIRED_RUNTIME_COMPONENTS, "runtime_inventory_exact_components")
    checks.check(len(inventory_records) == len(REQUIRED_RUNTIME_COMPONENTS), "runtime_inventory_unique_components")
    checks.check(inventory.get("candidate_only") is True, "runtime_inventory_candidate_only")
    checks.check(inventory.get("required_active_existing_count") == 1, "runtime_inventory_active_count")
    checks.check(inventory.get("required_planning_reference_count") == 8, "runtime_inventory_planning_count")
    checks.check(inventory.get("runtime_modified") is False, "runtime_inventory_no_runtime_change")
    checks.check(inventory.get("migration_executed") is False, "runtime_inventory_no_migration")

    for component in sorted(REQUIRED_RUNTIME_COMPONENTS):
        record = inventory_by_component.get(component, {})
        checks.check(bool(record.get("current_owner")), f"runtime_owner:{component}")
        checks.check(bool(record.get("current_role")), f"runtime_role:{component}")
        checks.check(bool(record.get("architecture_position")), f"runtime_position:{component}")
        checks.check(record.get("runtime_status") in ALLOWED_RUNTIME_STATUSES, f"runtime_status:{component}")
        checks.check(bool(record.get("allowed_responsibility")), f"runtime_allowed_responsibility:{component}")
        checks.check(bool(record.get("forbidden_responsibility")), f"runtime_forbidden_responsibility:{component}")
        source_refs = record.get("source_refs", [])
        checks.check(isinstance(source_refs, list) and bool(source_refs), f"runtime_source_refs:{component}")
        if isinstance(source_refs, list):
            for ref in source_refs:
                checks.check(isinstance(ref, str) and (ROOT / ref).exists(), f"runtime_source_exists:{component}:{ref}")

    for component in ACTIVE_RUNTIME_COMPONENTS:
        checks.check(inventory_by_component.get(component, {}).get("runtime_status") == "ACTIVE_EXISTING", f"active_runtime_status:{component}")
    for component in sorted(PLANNING_RUNTIME_COMPONENTS):
        checks.check(inventory_by_component.get(component, {}).get("runtime_status") == "PLANNING_REFERENCE", f"planning_runtime_status:{component}")

    runtime_foundation = inventory_by_component.get("Runtime Foundation", {})
    runtime_owner = str(runtime_foundation.get("current_owner", "")).lower()
    runtime_forbidden = lower_join(runtime_foundation.get("forbidden_responsibility"))
    checks.check("cognitive" not in runtime_owner, "runtime_no_cognitive_owner")
    for phrase in ["intent", "causal", "memory", "reality", "value", "personal cognitive network", "a/b simulation"]:
        checks.check(phrase in runtime_forbidden, f"runtime_forbidden:{phrase}")

    task_forbidden = lower_join(inventory_by_component.get("Task Runtime", {}).get("forbidden_responsibility"))
    for phrase in ["intent", "causal", "decision", "runtime dispatch", "action execution", "production scheduler"]:
        checks.check(phrase in task_forbidden, f"task_runtime_forbidden:{phrase}")

    capability_forbidden = lower_join(inventory_by_component.get("Capability Runtime", {}).get("forbidden_responsibility"))
    for phrase in ["cognitive conclusion", "reality", "intent", "decision", "provider", "state mutation"]:
        checks.check(phrase in capability_forbidden, f"capability_runtime_forbidden:{phrase}")

    model_forbidden = lower_join(inventory_by_component.get("Model Runtime", {}).get("forbidden_responsibility"))
    for phrase in ["real model inference", "real model load", "provider runtime call", "cognitive conclusion", "intent", "decision", "production runtime dispatch"]:
        checks.check(phrase in model_forbidden, f"model_runtime_forbidden:{phrase}")

    protocol_forbidden = lower_join(inventory_by_component.get("Protocol Runtime", {}).get("forbidden_responsibility"))
    for phrase in ["runtime protocol loading", "dynamic binding", "protocol registry mutation", "cognitive", "state mutation", "decision", "action execution"]:
        checks.check(phrase in protocol_forbidden, f"protocol_runtime_forbidden:{phrase}")

    for component, activation_phrase in [
        ("PCN Reference", "pcn runtime activation"),
        ("Causal Reference", "causal runtime activation"),
        ("Intent Reference", "intent runtime activation"),
    ]:
        checks.check(activation_phrase in lower_join(inventory_by_component.get(component, {}).get("forbidden_responsibility")), f"future_runtime_activation_forbidden:{component}")

    matrix = loaded.get("runtime_cognitive_boundary_matrix_candidate.json", {})
    matrix_records = records_from(matrix)
    matrix_by_flow = {
        record.get("flow"): record
        for record in matrix_records
        if isinstance(record.get("flow"), str)
    }
    checks.check(len(matrix_by_flow) == len(matrix_records), "boundary_matrix_unique_flows")
    checks.check(REQUIRED_ALLOWED_FLOWS.issubset(matrix_by_flow), "boundary_matrix_required_allowed_flows")
    checks.check(REQUIRED_FORBIDDEN_FLOWS.issubset(matrix_by_flow), "boundary_matrix_required_forbidden_flows")
    checks.check(matrix.get("required_allowed_flow_count") == 4, "boundary_matrix_required_allowed_count")
    checks.check(matrix.get("required_forbidden_flow_count") == 4, "boundary_matrix_required_forbidden_count")
    checks.check(matrix.get("all_new_mutation_authority_forbidden") is True, "boundary_matrix_no_new_mutation")
    checks.check(matrix.get("field_state_bypass_forbidden") is True, "boundary_matrix_field_precedence")
    checks.check(matrix.get("runtime_cognitive_owner") is False, "boundary_matrix_runtime_not_cognitive_owner")
    checks.check(matrix.get("runtime_modified") is False, "boundary_matrix_no_runtime_change")

    for flow, record in sorted(matrix_by_flow.items()):
        checks.check(bool(record.get("source")), f"flow_source:{flow}")
        checks.check(bool(record.get("target")), f"flow_target:{flow}")
        checks.check(isinstance(record.get("allowed"), bool), f"flow_allowed_boolean:{flow}")
        checks.check(bool(record.get("reason")), f"flow_reason:{flow}")
        checks.check(bool(record.get("owner")), f"flow_owner:{flow}")
        checks.check(record.get("mutation_allowed") is False, f"flow_no_mutation:{flow}")
        checks.check(bool(record.get("implementation_status")), f"flow_implementation_status:{flow}")

    for flow in REQUIRED_ALLOWED_FLOWS:
        checks.check(matrix_by_flow.get(flow, {}).get("allowed") is True, f"required_flow_allowed:{flow}")
    for flow in REQUIRED_FORBIDDEN_FLOWS:
        checks.check(matrix_by_flow.get(flow, {}).get("allowed") is False, f"required_flow_forbidden:{flow}")
    for flow in [
        "Runtime → Decision Arbitration",
        "Runtime → Value Judgment",
        "PCN → Runtime Direct Invocation",
        "Cognitive Layer → Field State Bypass",
    ]:
        checks.check(matrix_by_flow.get(flow, {}).get("allowed") is False, f"negative_flow_forbidden:{flow}")

    gaps = loaded.get("future_cognitive_runtime_gap_registry.json", {})
    gap_records = records_from(gaps)
    gap_by_component = {
        record.get("future_component"): record
        for record in gap_records
        if isinstance(record.get("future_component"), str)
    }
    checks.check(set(gap_by_component) == REQUIRED_FUTURE_GAPS, "future_gap_exact_components")
    checks.check(len(gap_records) == len(REQUIRED_FUTURE_GAPS), "future_gap_unique_components")
    checks.check(gaps.get("default_runtime_required") is False, "future_gap_default_false")
    checks.check(gaps.get("runtime_requirement_proven") is False, "future_gap_not_proven")
    checks.check(gaps.get("implementation_created") is False, "future_gap_no_implementation")
    checks.check(gaps.get("runtime_modified") is False, "future_gap_no_runtime_change")
    checks.check(gaps.get("migration_executed") is False, "future_gap_no_migration")
    for component in sorted(REQUIRED_FUTURE_GAPS):
        record = gap_by_component.get(component, {})
        checks.check(bool(record.get("current_status")), f"future_gap_status:{component}")
        checks.check(record.get("runtime_required") is False, f"future_gap_runtime_not_required:{component}")
        checks.check("separate_authorization" in str(record.get("implementation_phase", "")).lower(), f"future_gap_separate_authorization:{component}")
        checks.check(bool(record.get("dependency")), f"future_gap_dependency:{component}")
        checks.check(bool(record.get("risk")), f"future_gap_risk:{component}")

    adapters = loaded.get("runtime_adapter_candidate_registry.json", {})
    adapter_records = records_from(adapters)
    adapter_by_name = {
        record.get("adapter"): record
        for record in adapter_records
        if isinstance(record.get("adapter"), str)
    }
    checks.check(set(adapter_by_name) == REQUIRED_ADAPTERS, "adapter_exact_candidates")
    checks.check(len(adapter_records) == len(REQUIRED_ADAPTERS), "adapter_unique_candidates")
    for adapter in sorted(REQUIRED_ADAPTERS):
        record = adapter_by_name.get(adapter, {})
        checks.check(bool(record.get("purpose")), f"adapter_purpose:{adapter}")
        checks.check(bool(record.get("source")), f"adapter_source:{adapter}")
        checks.check(bool(record.get("target")), f"adapter_target:{adapter}")
        checks.check(record.get("status") == "FUTURE_CANDIDATE", f"adapter_future_status:{adapter}")
        checks.check(record.get("implementation_created") is False, f"adapter_not_created:{adapter}")
    checks.check(adapters.get("adapter_implementation_created") is False, "adapter_registry_no_implementation")
    checks.check(adapters.get("runtime_files_created") is False, "adapter_registry_no_runtime_files")
    checks.check(adapters.get("runtime_modified") is False, "adapter_registry_no_runtime_change")
    checks.check(adapters.get("migration_executed") is False, "adapter_registry_no_migration")

    risks = loaded.get("runtime_boundary_risk_register.json", {})
    risk_records = records_from(risks)
    risk_by_id = {
        record.get("risk_id"): record
        for record in risk_records
        if isinstance(record.get("risk_id"), str)
    }
    checks.check(set(risk_by_id) == REQUIRED_RISKS, "risk_registry_exact_coverage")
    checks.check(len(risk_records) == len(REQUIRED_RISKS), "risk_registry_unique_records")
    for risk_id in sorted(REQUIRED_RISKS):
        record = risk_by_id.get(risk_id, {})
        for field in ["risk", "trigger", "impact", "mitigation", "owner", "status"]:
            checks.check(bool(record.get(field)), f"risk_field:{risk_id}:{field}")
        checks.check(record.get("blocker_if_detected") is True, f"risk_blocker:{risk_id}")
    checks.check(risks.get("active_conflicts") == [], "risk_no_active_conflicts")
    checks.check(risks.get("blocker_count") == 0, "risk_no_current_blocker")
    checks.check(risks.get("runtime_change_required") is False, "risk_no_runtime_change_required")
    checks.check(risks.get("migration_executed") is False, "risk_no_migration")

    owner_review = markdown.get("runtime_owner_boundary_review.md", "").lower()
    for phrase, name in [
        ("scheduling and tick progression", "owner_review_scheduling"),
        ("lifecycle and stop control", "owner_review_lifecycle"),
        ("execution after an authorized boundary", "owner_review_execution"),
        ("resource-state observation and bounded resource management", "owner_review_resource"),
        ("cognition or current reality interpretation", "owner_review_no_cognition"),
        ("causal reasoning", "owner_review_no_causal"),
        ("value judgment", "owner_review_no_value"),
        ("user-personality ownership", "owner_review_no_user_personality"),
        ("legacy_runtime_unaligned", "owner_review_legacy_unaligned"),
        ("no adapter implementation", "owner_review_no_adapter"),
        ("does not start m4", "owner_review_no_m4"),
    ]:
        checks.check(phrase in owner_review, name)

    summary_text = markdown.get("runtime_boundary_alignment_summary.md", "").lower()
    for phrase, name in [
        ("runtime components retained unchanged", "summary_retained_runtime"),
        ("components requiring no current adjustment", "summary_no_adjustment"),
        ("future observation items", "summary_future_observation"),
        ("explicit prohibitions", "summary_prohibitions"),
        ("runtime_required=false", "summary_runtime_required_false"),
        ("implementation_created=false", "summary_adapter_not_created"),
        ("m4 migration integrity validation is not started", "summary_no_m4"),
        ("waiting_for_user_terminal_verification", "summary_stop_status"),
    ]:
        checks.check(phrase in summary_text, name)

    manifest = loaded.get("m3_change_manifest.json", {})
    checks.check(set(manifest.get("created_files", [])) == set(REQUIRED_FILES), "manifest_exact_created_files")
    for field in [
        "modified_existing_files",
        "deleted_files",
        "moved_files",
        "renamed_files",
        "runtime_files_changed",
        "runtime_files_created",
        "code_files_changed",
        "baseline_files_changed",
        "active_contract_changed",
        "active_contract_files_changed",
        "active_schema_files_changed",
        "active_registry_files_changed",
        "active_owner_metadata_changed",
    ]:
        checks.check(manifest.get(field) == [], f"manifest_empty:{field}")
    for field in [
        "runtime_api_changed",
        "adapter_implementation_created",
        "cognitive_runtime_created",
        "migration_executed",
        "m4_started",
    ]:
        checks.check(manifest.get(field) is False, f"manifest_false:{field}")
    checks.check(manifest.get("planning_candidate_only") is True, "manifest_planning_only")

    phase = loaded.get("phase_contract.json", {})
    governance_required_path = ROOT / "docs/architecture/governance/luna_engineering_execution_and_verification_governance_v1/luna_phase_instruction_required_fields_standard_v1.json"
    try:
        governance_required = load_json(governance_required_path)
        required_phase_fields = set(governance_required.get("required_fields", {}))
        checks.check(bool(required_phase_fields), "phase_required_field_standard_loaded")
    except (OSError, json.JSONDecodeError):
        required_phase_fields = set()
        checks.check(False, "phase_required_field_standard_loaded")
    checks.check(required_phase_fields.issubset(phase), "phase_required_fields_complete")
    checks.check(phase.get("Phase") == "Phase-Luna-Controlled-Architecture-Alignment-Migration-M3-Runtime-Boundary-Alignment-v1-001", "phase_id")
    checks.check(phase.get("Stage") == "M3 Runtime Boundary Alignment", "phase_stage")
    checks.check(phase.get("Execution Mode") == "Planning Only", "phase_execution_mode")
    checks.check(phase.get("Previous Phase Decision") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M2_OWNER_METADATA_ALIGNMENT_READY", "phase_previous_decision")
    checks.check(phase.get("Target Directory") == "docs/architecture/luna_controlled_architecture_alignment_migration_m3_runtime_boundary_alignment_v1/", "phase_target_directory")
    checks.check(set(phase.get("Required Final Files", [])) == set(REQUIRED_FILES), "phase_required_final_files")
    authority = phase.get("Verification Authority", {})
    checks.check(authority.get("V0") == "Agent", "phase_v0_authority")
    checks.check(authority.get("V1") == "Not Authorized", "phase_v1_authority")
    checks.check(authority.get("V2") == "User Terminal Only", "phase_v2_authority")
    checks.check(authority.get("V3") == "ChatGPT Only", "phase_v3_authority")
    checks.check(phase.get("Required Checks", {}).get("V1") == [], "phase_no_v1")
    checks.check(phase.get("Agent Stop Point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_agent_stop")
    checks.check(phase.get("Current Status Contract") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_current_status")
    expected_command = "python3 docs/architecture/luna_controlled_architecture_alignment_migration_m3_runtime_boundary_alignment_v1/verify_controlled_architecture_alignment_m3_runtime_boundary_alignment_v1.py"
    checks.check(phase.get("User Terminal Commands") == [expected_command], "phase_exact_user_command")
    checks.check(phase.get("Expected Success Decision") == "V2_FINAL_VERIFICATION_PASSED", "phase_success_decision")
    checks.check(phase.get("Expected Success Readiness") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M3_RUNTIME_BOUNDARY_ALIGNMENT_READY", "phase_success_readiness")
    checks.check(phase.get("Expected Next") == "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT", "phase_success_next")
    checks.check(phase.get("Expected Failure Decision") == "BLOCKED_BY_VERIFIER_FAILURE", "phase_failure_decision")
    checks.check(phase.get("Expected Failure Readiness") == "LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M3_RUNTIME_BOUNDARY_ALIGNMENT_REMEDIATION_REQUIRED", "phase_failure_readiness")
    checks.check(phase.get("Expected Failure Next") == "REMEDIATE_REPORTED_FAILURES_ONLY", "phase_failure_next")
    checks.check(phase.get("Runtime Modification") is False, "phase_no_runtime_modification")
    checks.check(phase.get("Migration") is False, "phase_no_migration")
    checks.check(phase.get("M4 Started") is False, "phase_no_m4")
    negative_guards = lower_join(phase.get("Negative Guards"))
    for phrase in [
        "no-check-weaken",
        "no-hardcoded-pass",
        "no final phase verifier by agent",
        "no runtime import or execution",
        "no runtime or adapter creation",
        "no active asset mutation",
        "no migration execution",
        "no m4 entry",
        "no runtime cognitive ownership",
        "no field state bypass",
    ]:
        checks.check(phrase in negative_guards, f"phase_negative_guard:{phrase}")

    imported_roots: set[str] = set()
    for node in ast.walk(verifier_tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])
    checks.check(imported_roots.issubset({"__future__", "ast", "json", "pathlib", "typing"}), "verifier_standard_library_import_boundary")
    called_names = {
        node.func.id
        for node in ast.walk(verifier_tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    called_attributes = {
        node.func.attr
        for node in ast.walk(verifier_tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    checks.check("open" not in called_names, "verifier_no_builtin_file_open")
    checks.check(
        called_attributes.isdisjoint({"write_text", "write_bytes", "unlink", "rename", "replace", "mkdir", "rmdir"}),
        "verifier_no_file_mutation_calls",
    )

    failed = checks.failed
    passed_count = checks.total - len(failed)
    print(f"CHECKS: {checks.total}")
    print(f"FAILED_CHECKS: {failed}")
    print(f"PASSED_CHECK_COUNT: {passed_count}")
    print(f"FAILED_CHECK_COUNT: {len(failed)}")
    print(f"BLOCKER_COUNT: {len(failed)}")
    if failed:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M3_RUNTIME_BOUNDARY_ALIGNMENT_REMEDIATION_REQUIRED")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_CONTROLLED_ARCHITECTURE_ALIGNMENT_M3_RUNTIME_BOUNDARY_ALIGNMENT_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
