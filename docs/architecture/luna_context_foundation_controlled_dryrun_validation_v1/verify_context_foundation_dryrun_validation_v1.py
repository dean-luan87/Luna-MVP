#!/usr/bin/env python3
"""Read-only final verifier for Context Foundation DryRun validation v1."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable


BASE = Path(__file__).resolve().parent
STATUS = "VALIDATION_CANDIDATE"
READY = "LUNA_CONTEXT_FOUNDATION_CONTROLLED_DRYRUN_VALIDATION_READY"
REMEDIATION = "LUNA_CONTEXT_FOUNDATION_CONTROLLED_DRYRUN_VALIDATION_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "context_foundation_dryrun_contract_v1.json",
    "context_expansion_governance_candidate.json",
    "resource_bounded_context_expansion_candidate.json",
    "unknown_resolution_policy_candidate.json",
    "context_foundation_dryrun_scenarios.json",
    "context_foundation_dryrun_trace_validation.json",
    "nested_constraint_relationship_candidate.json",
    "context_foundation_dryrun_validation_summary.md",
    "context_foundation_dryrun_change_manifest.json",
    "phase_contract.json",
    "verify_context_foundation_dryrun_validation_v1.py",
}

JSON_FILES = REQUIRED_FILES - {
    "context_foundation_dryrun_validation_summary.md",
    "verify_context_foundation_dryrun_validation_v1.py",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        if (
            candidate / "capabilities/midplatform/core/context_foundation"
        ).is_dir():
            return candidate
    raise RuntimeError("repository_root_with_context_foundation_not_found")


def load_json(name: str) -> Dict[str, Any]:
    value = json.loads((BASE / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def flatten_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, nested in value.items():
            yield str(key)
            yield from flatten_strings(nested)
    elif isinstance(value, (list, tuple)):
        for nested in value:
            yield from flatten_strings(nested)


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    def check(condition: bool, check_id: str) -> None:
        checks.append(check_id)
        if not condition:
            failures.append(check_id)

    try:
        repo_root = find_repo_root()
        check(True, "repo_root_resolved")
    except RuntimeError:
        repo_root = Path.cwd().resolve()
        check(False, "repo_root_resolved")

    actual_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_files == REQUIRED_FILES, "exact_file_set")

    documents: Dict[str, Dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        try:
            documents[name] = load_json(name)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            documents[name] = {}
            check(False, f"json_parse:{name}")

    for name, document in documents.items():
        check(document.get("status") == STATUS, f"validation_status:{name}")

    contract = documents.get("context_foundation_dryrun_contract_v1.json", {})
    check(contract.get("owner") == "Context Foundation Governance Candidate", "contract_owner")
    check(
        contract.get("allowed_flow")
        == [
            "Synthetic Projection",
            "Context Assembly",
            "Context Envelope Candidate",
            "Context Trace Candidate",
        ],
        "contract_allowed_flow",
    )
    required_forbidden_flows = {
        "Context -> Fact",
        "Context -> Intent",
        "Context -> Causal Explanation",
        "Context -> Decision",
        "Context -> Action",
        "Context -> Source Mutation",
        "Context -> Runtime Command",
    }
    check(
        required_forbidden_flows <= set(contract.get("forbidden_flows", [])),
        "contract_forbidden_flows",
    )
    owner_boundary = contract.get("owner_boundary", {})
    check(owner_boundary.get("source_owner_precedence") is True, "contract_owner_precedence")
    check(owner_boundary.get("source_owner_transfer") is False, "contract_no_owner_transfer")
    check(owner_boundary.get("source_mutation_allowed") is False, "contract_no_source_mutation")
    for key in [
        "candidate_only",
        "unknown_preservation_required",
        "evidence_required_for_expansion",
        "resource_budget_reference_required",
        "trace_required",
    ]:
        check(contract.get(key) is True, f"contract_true:{key}")
    for key in [
        "runtime_execution",
        "database_access",
        "model_call",
        "provider_call",
        "state_mutation",
        "active_contract",
    ]:
        check(contract.get(key) is False, f"contract_false:{key}")

    expansion = documents.get("context_expansion_governance_candidate.json", {})
    required_expansion_sources = {
        "Existing Evidence",
        "Historical Experience Reference",
        "Memory Projection",
        "System Rules Reference",
    }
    check(
        set(expansion.get("expansion_source", [])) == required_expansion_sources,
        "expansion_sources",
    )
    check(expansion.get("evidence_required") is True, "expansion_evidence_required")
    check(bool(expansion.get("resource_budget_reference")), "expansion_budget_reference")
    check(expansion.get("inference_allowed") is True, "expansion_candidate_completion_allowed")
    check(expansion.get("inference_scope") == "Candidate Completion only", "expansion_inference_scope")
    check(expansion.get("context_owned_reasoning") is False, "expansion_no_context_reasoning")
    for key in [
        "causal_inference_allowed",
        "intent_generation_allowed",
        "decision_generation_allowed",
        "fact_generation_allowed",
        "unsupported_information_creation_allowed",
        "active_governance",
    ]:
        check(expansion.get(key) is False, f"expansion_false:{key}")
    for key in [
        "candidate_status_required",
        "confidence_required",
        "source_reference_required",
        "source_owner_precedence",
    ]:
        check(expansion.get(key) is True, f"expansion_true:{key}")

    resource = documents.get("resource_bounded_context_expansion_candidate.json", {})
    check(
        set(resource.get("resource_type", []))
        == {"Hardware Resource", "Runtime Resource", "Cognitive Resource"},
        "resource_types",
    )
    check(bool(resource.get("available_budget_reference")), "resource_budget_reference")
    check(bool(resource.get("expansion_scope")), "resource_expansion_scope")
    check(bool(resource.get("degradation_behavior")), "resource_degradation_behavior")
    check(
        resource.get("resource_insufficient_result")
        == "Degraded Context Scope Candidate",
        "resource_degraded_candidate",
    )
    check(resource.get("resource_insufficiency_is_failure") is False, "resource_not_failure")
    check(resource.get("static_layer_limit_allowed") is False, "resource_no_static_limit")
    check(resource.get("numeric_expansion_limit_owned_by_context") is False, "resource_no_numeric_limit")
    check(resource.get("minimum_context_preserved") is True, "resource_minimum_preserved")
    resource_text = " ".join(flatten_strings(resource)).lower()
    for token, check_id in [
        ("depth=3", "resource_no_depth_3"),
        ("depth=5", "resource_no_depth_5"),
        ("max_context_layer", "resource_no_max_context_layer"),
    ]:
        check(token not in resource_text, check_id)

    unknown = documents.get("unknown_resolution_policy_candidate.json", {})
    check(unknown.get("unknown_type") == "Context Unknown Reference", "unknown_type")
    check(
        set(unknown.get("completion_source", []))
        == {"Historical Experience", "Personal Memory Pattern", "System Rule"},
        "unknown_completion_sources",
    )
    check(
        unknown.get("completion_output") == "Unknown Completion Candidate",
        "unknown_candidate_output",
    )
    for key in [
        "confidence_required",
        "source_reference_required",
        "provenance_required",
        "candidate_status_required",
        "multiple_candidates_allowed",
        "contradiction_preservation_required",
        "current_reality_precedence",
        "fact_promotion_forbidden",
    ]:
        check(unknown.get(key) is True, f"unknown_true:{key}")
    for key in [
        "automatic_memory_write_allowed",
        "intent_generation_allowed",
        "causal_conclusion_allowed",
        "decision_generation_allowed",
        "active_policy",
    ]:
        check(unknown.get(key) is False, f"unknown_false:{key}")

    scenarios = documents.get("context_foundation_dryrun_scenarios.json", {})
    records = scenarios.get("scenarios", [])
    required_case_ids = {
        "DRYRUN-CF-01-WORK-TO-HOME",
        "DRYRUN-CF-02-COMPLEX-PLANNING",
        "DRYRUN-CF-03-UNKNOWN-COMPLETION",
        "DRYRUN-CF-04-WEATHER-MINIMAL",
    }
    check({item.get("case_id") for item in records} == required_case_ids, "scenario_ids")
    check(scenarios.get("scenario_count") == 4, "scenario_count")
    check(all(item.get("passes_boundary") is True for item in records), "scenario_boundaries")
    check(scenarios.get("synthetic_only") is True, "scenario_synthetic_only")
    check(scenarios.get("runtime_executed") is False, "scenario_no_runtime")
    check(scenarios.get("model_called") is False, "scenario_no_model")
    check(scenarios.get("state_mutation") is False, "scenario_no_mutation")
    by_id = {item.get("case_id"): item for item in records}
    case_1 = by_id.get("DRYRUN-CF-01-WORK-TO-HOME", {})
    check("Mental Field Continuity Reference" in case_1.get("expected_candidates", []), "scenario_carryover")
    check("用户讨厌工作" in case_1.get("forbidden_conclusions", []), "scenario_no_work_dislike")
    case_2 = by_id.get("DRYRUN-CF-02-COMPLEX-PLANNING", {})
    outcomes = case_2.get("resource_outcomes", {})
    check(bool(outcomes.get("sufficient_budget")), "scenario_resource_sufficient")
    check(bool(outcomes.get("limited_budget")), "scenario_resource_limited")
    check(case_2.get("insufficient_resource_is_failure") is False, "scenario_resource_not_failure")
    case_3 = by_id.get("DRYRUN-CF-03-UNKNOWN-COMPLETION", {})
    check(case_3.get("allowed_candidate_completion") == "朋友可能在忙", "scenario_unknown_candidate")
    check("朋友生气" in case_3.get("forbidden_facts", []), "scenario_unknown_not_fact")
    check(case_3.get("fact_promotion_forbidden") is True, "scenario_fact_promotion_forbidden")
    case_4 = by_id.get("DRYRUN-CF-04-WEATHER-MINIMAL", {})
    check(case_4.get("expected_candidate") == "Minimal Context Envelope Candidate", "scenario_minimal_context")

    trace = documents.get("context_foundation_dryrun_trace_validation.json", {})
    required_trace_fields = {
        "source_reference",
        "expansion_reason",
        "resource_constraint",
        "confidence",
        "candidate_status",
    }
    check(set(trace.get("required_trace_fields", [])) == required_trace_fields, "trace_fields")
    trace_rules = trace.get("trace_rules", {})
    check(all(trace_rules.get(key) is True for key in [
        "source_reference_required",
        "expansion_reason_required",
        "resource_constraint_required",
        "confidence_required",
        "candidate_status_required",
        "unknown_preserved",
        "multiple_candidates_traceable",
        "source_owner_precedence",
    ]), "trace_rules")
    check(trace.get("runtime_trace_created") is False, "trace_no_runtime")
    check(trace.get("database_trace_written") is False, "trace_no_database")

    nested = documents.get("nested_constraint_relationship_candidate.json", {})
    required_relationships = {
        "CONTEXT_RESOURCE",
        "CONTEXT_EMOTION",
        "CONTEXT_MEMORY",
        "CONTEXT_FIELD",
        "CONTEXT_CAUSAL_FUTURE_DEPENDENCY",
    }
    relations = nested.get("relationships", [])
    check(
        {item.get("relationship_id") for item in relations} == required_relationships,
        "nested_relationships",
    )
    check(set(nested.get("required_relationship_ids", [])) == required_relationships, "nested_registry")
    check(nested.get("relationship_count") == 5, "nested_count")
    check(all(item.get("context_constraint") for item in relations), "nested_context_constraints")
    check(all(item.get("feedback_constraint") for item in relations), "nested_feedback_constraints")
    check(nested.get("feedback_is_candidate_only") is True, "nested_candidate_only")
    check(nested.get("loop_runtime_implemented") is False, "nested_no_runtime")
    check(nested.get("source_mutation_allowed") is False, "nested_no_mutation")

    summary = (
        BASE / "context_foundation_dryrun_validation_summary.md"
    ).read_text(encoding="utf-8")
    for token, check_id in [
        (STATUS, "summary_status"),
        ("Constraint-driven dynamic cognitive system", "summary_dynamic_system"),
        ("Context itself owns no reasoning", "summary_no_context_reasoning"),
        ("Degraded Context Scope Candidate", "summary_resource_degradation"),
        ("Unknown Completion Candidate", "summary_unknown_candidate"),
        ("Mental Field Continuity Reference", "summary_carryover"),
        ("No existing Context Skeleton code is changed or executed by the Agent", "summary_skeleton_unchanged"),
        ("Do not enter PCN, Intent, or Causal development", "summary_stop_boundary"),
    ]:
        check(token in summary, check_id)

    manifest = documents.get("context_foundation_dryrun_change_manifest.json", {})
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_files")
    for key in ["modified_existing_files", "deleted_files", "moved_files", "renamed_files"]:
        check(manifest.get(key) == [], f"manifest_empty:{key}")
    for key in [
        "runtime_changed",
        "schema_changed",
        "contract_changed",
        "implementation_changed",
        "owner_metadata_changed",
        "dryrun_executed_by_agent",
        "model_called",
        "provider_called",
        "database_accessed",
        "state_mutation_executed",
    ]:
        check(manifest.get(key) is False, f"manifest_false:{key}")
    check(manifest.get("dryrun_only") is True, "manifest_dryrun_only")
    protected_hashes = manifest.get("protected_skeleton_baseline_hashes", {})
    code_dir = repo_root / "capabilities/midplatform/core/context_foundation"
    check(len(protected_hashes) == 9, "protected_hash_count")
    for name, expected_hash in sorted(protected_hashes.items()):
        path = code_dir / name
        check(path.is_file(), f"protected_file_exists:{name}")
        check(path.is_file() and sha256(path) == expected_hash, f"protected_hash:{name}")

    phase = documents.get("phase_contract.json", {})
    required_phase_fields = {
        "phase", "stage", "execution_mode", "current_work_description",
        "previous_phase", "previous_phase_decision", "input_assets",
        "required_pre_read", "target_directory", "scope", "out_of_scope",
        "required_final_files", "implementation_principles", "required_checks",
        "negative_guards", "verification_authority", "allowed_agent_checks",
        "allowed_agent_execution", "prohibited_agent_execution", "agent_stop_point",
        "user_terminal_commands", "expected_success_decision", "expected_next",
        "expected_failure_decision", "expected_failure_next", "stop_condition",
        "blocker_conditions", "completion_report_format", "current_status_contract",
    }
    check(required_phase_fields <= set(phase), "phase_required_fields")
    check(phase.get("execution_mode") == "Planning Only", "phase_mode")
    check(phase.get("execution_profile") == "Controlled Validation Only", "phase_profile")
    check(bool(phase.get("execution_mode_normalization_reason")), "phase_normalization")
    check(
        phase.get("previous_phase_decision")
        == "LUNA_CONTEXT_FOUNDATION_CONTROLLED_SKELETON_IMPLEMENTATION_READY",
        "phase_previous_decision",
    )
    authority = phase.get("verification_authority", {})
    check(authority.get("V0") == "Agent", "authority_v0")
    check(authority.get("V1") == "NOT_AUTHORIZED", "authority_v1")
    check(authority.get("V2") == "USER_TERMINAL_ONLY", "authority_v2")
    check(authority.get("V3") == "CHATGPT_ONLY", "authority_v3")
    check(phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_stop")
    check(phase.get("expected_success_decision") == READY, "phase_ready")
    check(phase.get("dryrun_executed_by_agent") is False, "phase_no_agent_dryrun")
    check(phase.get("implementation_changed") is False, "phase_no_implementation_change")
    check(phase.get("next_phase_auto_entry") is False, "phase_no_auto_next")
    check(len(phase.get("required_final_files", [])) == len(REQUIRED_FILES), "phase_file_count")
    check(
        all((repo_root / path).exists() for path in phase.get("required_final_files", [])),
        "phase_references_exist",
    )

    try:
        source = (
            BASE / "verify_context_foundation_dryrun_validation_v1.py"
        ).read_text(encoding="utf-8")
        tree = ast.parse(source)
        compile(source, str(BASE / "verify_context_foundation_dryrun_validation_v1.py"), "exec")
        check(True, "verifier_compile")
    except (OSError, SyntaxError, ValueError):
        tree = ast.Module(body=[], type_ignores=[])
        check(False, "verifier_compile")
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
    check(
        imports <= {"__future__", "ast", "hashlib", "json", "pathlib", "typing"},
        "verifier_standard_library_only",
    )
    forbidden_calls = {
        "write_text", "write_bytes", "unlink", "rename", "replace",
        "mkdir", "rmdir", "system", "run", "Popen", "connect",
    }
    calls = set()
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
