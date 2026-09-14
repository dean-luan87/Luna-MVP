#!/usr/bin/env python3
"""Read-only verifier for the Dynamic Cognitive Architecture integration audit."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
AUDIT_STATUS = "ARCHITECTURE_AUDIT_CANDIDATE"
READY = "LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_INTEGRATION_AUDIT_READY"
REMEDIATION = "LUNA_DYNAMIC_COGNITIVE_ARCHITECTURE_INTEGRATION_AUDIT_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "architecture_flow_integrity_matrix.json",
    "owner_consistency_audit.json",
    "cognitive_boundary_audit.json",
    "causal_chain_alignment_review.json",
    "field_context_time_alignment_review.json",
    "experience_memory_loop_validation.json",
    "architecture_audit_finding_registry.json",
    "integration_audit_summary.md",
    "audit_change_manifest.json",
    "phase_contract.json",
    "verify_dynamic_cognitive_architecture_integration_audit_v1.py",
}

JSON_FILES = REQUIRED_FILES - {
    "integration_audit_summary.md",
    "verify_dynamic_cognitive_architecture_integration_audit_v1.py",
}


def load_json(name: str) -> dict[str, Any]:
    with (BASE / name).open("r", encoding="utf-8") as handle:
        value = json.load(handle)
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
    check(REQUIRED_FILES == actual_files, "exact_file_set")

    documents: dict[str, dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        try:
            documents[name] = load_json(name)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            documents[name] = {}
            check(False, f"json_parse:{name}")

    for name, document in documents.items():
        check(document.get("audit_status") == AUDIT_STATUS, f"audit_status:{name}")

    flow = documents.get("architecture_flow_integrity_matrix.json", {})
    required_chain = [
        "Reality",
        "Field State",
        "Observation / Evidence",
        "Context Projection",
        "Personal Cognitive Network",
        "Intent",
        "Causal Reasoning",
        "A/B Route",
        "Decision",
        "Task",
        "Runtime",
        "Outcome",
        "Experience Compression",
        "Memory",
    ]
    check(flow.get("required_logical_chain") == required_chain, "flow_required_chain")
    flow_records = flow.get("records", [])
    expected_edges = set(zip(required_chain, required_chain[1:]))
    actual_edges = {(item.get("source"), item.get("target")) for item in flow_records}
    check(expected_edges <= actual_edges, "flow_edges_complete")
    check(len({item.get("flow_id") for item in flow_records}) == len(flow_records), "flow_ids_unique")
    check(all(item.get("owner") for item in flow_records), "flow_owner_complete")
    check(all(item.get("direction_valid") is True for item in flow_records), "flow_direction_valid")
    check(all(item.get("boundary_valid") is True for item in flow_records), "flow_boundary_valid")
    check(all(item.get("evidence_refs") for item in flow_records), "flow_evidence_complete")
    check(flow.get("breakpoints") == [], "flow_no_breakpoints")
    check(flow.get("reverse_dependency_conflicts") == [], "flow_no_reverse_conflicts")
    check(flow.get("owner_conflicts") == [], "flow_no_owner_conflicts")
    check(flow.get("blocker_count") == 0, "flow_no_blockers")

    owners = documents.get("owner_consistency_audit.json", {})
    owner_records = owners.get("records", [])
    required_objects = {
        "Field State",
        "Observation",
        "Memory",
        "Personal Cognitive Network",
        "Intent",
        "Causal",
        "Experience",
        "A/B Route",
        "Decision",
        "Task",
        "Runtime",
        "Model",
    }
    check({item.get("object") for item in owner_records} == required_objects, "owner_objects_complete")
    check(len(owner_records) == len(required_objects), "owner_objects_unique")
    check(all(item.get("owner") for item in owner_records), "owner_names_complete")
    check(all(item.get("write_authority") for item in owner_records), "write_authority_complete")
    check(all(item.get("conflict") is False for item in owner_records), "owner_conflicts_false")
    check(all(item.get("evidence_refs") for item in owner_records), "owner_evidence_complete")
    check(owners.get("duplicate_object_owners") == [], "no_duplicate_object_owners")
    check(owners.get("duplicate_write_authorities") == [], "no_duplicate_writers")
    check(owners.get("owner_drift") == [], "no_owner_drift")
    check(owners.get("blocker_count") == 0, "owner_no_blockers")

    boundaries = documents.get("cognitive_boundary_audit.json", {})
    boundary_records = boundaries.get("records", [])
    required_boundaries = {
        "Field -> Context",
        "Memory -> Projection",
        "Personal Cognitive Network -> Activation",
        "Causal Reasoning -> Candidate Reasoning",
        "Decision -> Task",
        "Observation -> Fact",
        "Memory -> Reality Override",
        "Runtime -> Cognition",
        "Model -> Decision",
        "Task -> Intent",
        "Causal Reasoning -> Action",
    }
    check(required_boundaries <= {item.get("boundary") for item in boundary_records}, "boundaries_complete")
    check(all(item.get("expectation") in {"ALLOWED", "FORBIDDEN"} for item in boundary_records), "boundary_expectations_valid")
    check(all(item.get("status") == "PASS" for item in boundary_records), "boundaries_pass")
    check(all(item.get("reason") for item in boundary_records), "boundary_reasons_complete")
    check(all(item.get("evidence_refs") for item in boundary_records), "boundary_evidence_complete")
    check(boundaries.get("failed_boundaries") == [], "no_failed_boundaries")
    check(boundaries.get("blocker_count") == 0, "boundary_no_blockers")

    causal = documents.get("causal_chain_alignment_review.json", {})
    causal_records = causal.get("records", [])
    check(len(causal_records) == 1, "causal_single_review")
    causal_record = causal_records[0] if causal_records else {}
    check(
        set(causal_record.get("input_sources", []))
        == {"Field Context", "Role Context", "Relationship Context", "Emotion Context", "Memory Context"},
        "causal_inputs_complete",
    )
    check(
        set(causal_record.get("output_scope", []))
        == {"Causal Candidate", "Alternative Explanation", "Confidence", "Decision Support Reference"},
        "causal_outputs_complete",
    )
    check(set(causal_record.get("forbidden_outputs", [])) == {"Fact", "Action", "Reality Mutation"}, "causal_forbidden_outputs")
    check(causal_record.get("candidate_only") is True, "causal_candidate_only")
    check(causal_record.get("unknown_preserved") is True, "causal_unknown_preserved")
    check(causal_record.get("valid") is True, "causal_valid")
    check(causal.get("causal_fact_promotion_allowed") is False, "causal_no_fact_promotion")
    check(causal.get("causal_action_execution_allowed") is False, "causal_no_action")
    check(causal.get("reality_mutation_allowed") is False, "causal_no_reality_mutation")
    check(causal.get("blocker_count") == 0, "causal_no_blockers")

    temporal = documents.get("field_context_time_alignment_review.json", {})
    temporal_checks = temporal.get("checks", [])
    required_temporal = {
        "Current Field",
        "Historical Field",
        "Active Context",
        "Temporal Validity",
        "Emotional Carryover",
        "Short Term Memory Scope",
    }
    check({item.get("item") for item in temporal_checks} == required_temporal, "temporal_checks_complete")
    check(all(item.get("status") == "PASS" for item in temporal_checks), "temporal_checks_pass")
    check(all(item.get("finding") for item in temporal_checks), "temporal_findings_complete")
    check(all(item.get("evidence_refs") for item in temporal_checks), "temporal_evidence_complete")
    check(temporal.get("physical_field_switch_resets_mental_state") is False, "no_field_switch_mental_reset")
    check(temporal.get("continuity_requires_governed_transition") is True, "continuity_governed")
    check(temporal.get("memory_is_not_current_reality") is True, "memory_not_reality")
    check(temporal.get("carryover_is_not_identity") is True, "carryover_not_identity")
    check(temporal.get("blocker_count") == 0, "temporal_no_blockers")

    experience = documents.get("experience_memory_loop_validation.json", {})
    loop_records = experience.get("records", [])
    required_loop_edges = {
        ("Event", "Outcome"),
        ("Outcome", "Observation"),
        ("Observation", "Evaluation"),
        ("Evaluation", "Experience Compression"),
        ("Experience Compression", "Memory Admission"),
    }
    check(required_loop_edges <= {(item.get("source"), item.get("target")) for item in loop_records}, "experience_loop_complete")
    check(all(item.get("valid") is True for item in loop_records), "experience_loop_valid")
    check(all(item.get("evidence_refs") for item in loop_records), "experience_loop_evidence_complete")
    forbidden_paths = experience.get("forbidden_paths", [])
    check({item.get("path") for item in forbidden_paths} >= {"Event -> Memory", "Single Event -> Long Term Experience"}, "experience_forbidden_paths_complete")
    check(all(item.get("prohibited") is True and item.get("status") == "PASS" for item in forbidden_paths), "experience_forbidden_paths_pass")
    check(experience.get("memory_admission_required") is True, "memory_admission_required")
    check(experience.get("single_event_long_term_promotion_allowed") is False, "no_single_event_promotion")
    check(experience.get("automatic_memory_write_allowed") is False, "no_automatic_memory_write")
    check(experience.get("blocker_count") == 0, "experience_no_blockers")

    findings = documents.get("architecture_audit_finding_registry.json", {})
    finding_records = findings.get("findings", [])
    check(len({item.get("finding_id") for item in finding_records}) == len(finding_records), "finding_ids_unique")
    check(all(item.get("severity") in {"INFO", "WARNING", "BLOCKER"} for item in finding_records), "finding_severity_valid")
    check(all(item.get("description") for item in finding_records), "finding_descriptions_complete")
    check(all(item.get("requires_change") is False for item in finding_records), "findings_no_required_change")
    computed_blockers = sum(item.get("severity") == "BLOCKER" for item in finding_records)
    computed_warnings = sum(item.get("severity") == "WARNING" for item in finding_records)
    computed_info = sum(item.get("severity") == "INFO" for item in finding_records)
    check(findings.get("blocker_count") == computed_blockers == 0, "finding_no_blockers")
    check(findings.get("warning_count") == computed_warnings, "finding_warning_count")
    check(findings.get("info_count") == computed_info, "finding_info_count")
    check(findings.get("requires_architecture_change") is False, "no_architecture_change_required")
    check(findings.get("automatic_remediation_allowed") is False, "no_automatic_remediation")

    summary_path = BASE / "integration_audit_summary.md"
    try:
        summary = summary_path.read_text(encoding="utf-8")
        check(True, "summary_readable")
    except OSError:
        summary = ""
        check(False, "summary_readable")
    for token, check_id in [
        (AUDIT_STATUS, "summary_candidate_status"),
        ("Architecture: `READY_FOR_DEVELOPMENT_BASELINE`", "summary_architecture_state"),
        ("No architecture `BLOCKER`", "summary_no_blocker"),
        ("no Runtime, PCN, Causal Engine, Intent Engine", "summary_no_implementation"),
        ("Memory admission", "summary_memory_admission"),
    ]:
        check(token in summary, check_id)

    manifest = documents.get("audit_change_manifest.json", {})
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_exact_created_files")
    for key in [
        "modified_existing_files",
        "deleted_files",
        "moved_files",
        "renamed_files",
        "code_files_changed",
        "runtime_files_changed",
        "schema_files_changed",
        "contract_files_changed",
        "owner_metadata_files_changed",
    ]:
        check(manifest.get(key) == [], f"manifest_empty:{key}")
    for key in [
        "schema_changed",
        "contract_changed",
        "owner_metadata_changed",
        "migration_executed",
        "architecture_modified",
        "runtime_activated",
        "model_invoked",
        "automatic_remediation_executed",
    ]:
        check(manifest.get(key) is False, f"manifest_false:{key}")
    check(manifest.get("audit_assets_only") is True, "manifest_audit_only")

    contract = documents.get("phase_contract.json", {})
    check(contract.get("execution_mode") == "Audit", "contract_execution_mode")
    check(contract.get("execution_profile") == "Validation Planning Only", "contract_execution_profile")
    for key in [
        "architecture_change",
        "migration",
        "implementation",
        "runtime_change",
        "schema_change",
        "contract_change",
        "owner_metadata_change",
        "automatic_remediation",
        "next_phase_auto_entry",
    ]:
        check(contract.get(key) is False, f"contract_false:{key}")
    authority = contract.get("verification_authority", {})
    check(authority.get("V0") == "Agent", "contract_v0_authority")
    check(authority.get("V1") == "NOT_AUTHORIZED", "contract_v1_authority")
    check(authority.get("V2") == "USER_TERMINAL_ONLY", "contract_v2_authority")
    check(authority.get("V3") == "CHATGPT_ONLY", "contract_v3_authority")

    try:
        source = (BASE / "verify_dynamic_cognitive_architecture_integration_audit_v1.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        check(True, "verifier_ast_parse")
    except (OSError, SyntaxError):
        tree = ast.Module(body=[], type_ignores=[])
        check(False, "verifier_ast_parse")
    imported_modules = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_modules.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    check(imported_modules <= {"__future__", "ast", "json", "pathlib", "typing"}, "verifier_standard_library_only")
    forbidden_calls = {"write_text", "write_bytes", "unlink", "rename", "replace", "mkdir", "rmdir", "system", "run", "Popen"}
    call_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                call_names.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                call_names.add(node.func.attr)
    check(not (call_names & forbidden_calls), "verifier_no_mutating_calls")

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
