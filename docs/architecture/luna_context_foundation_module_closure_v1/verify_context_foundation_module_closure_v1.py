#!/usr/bin/env python3
"""Read-only final phase verifier for Context Foundation module closure v1."""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable


BASE = Path(__file__).resolve().parent
READY = "LUNA_CONTEXT_FOUNDATION_MODULE_CLOSURE_READY"
REMEDIATION = "LUNA_CONTEXT_FOUNDATION_MODULE_CLOSURE_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "context_foundation_module_baseline_v1.json",
    "context_foundation_owner_closure_review.md",
    "context_foundation_io_closure_contract.json",
    "context_projection_governance_baseline.json",
    "mental_field_continuity_closure_review.md",
    "context_resource_constraint_closure.json",
    "context_unknown_resolution_closure.json",
    "context_to_pcn_handoff_contract_candidate.json",
    "context_foundation_closure_summary.md",
    "context_foundation_closure_change_manifest.json",
    "phase_contract.json",
    "verify_context_foundation_module_closure_v1.py",
}

JSON_FILES = REQUIRED_FILES - {
    "context_foundation_owner_closure_review.md",
    "mental_field_continuity_closure_review.md",
    "context_foundation_closure_summary.md",
    "verify_context_foundation_module_closure_v1.py",
}


def find_repo_root() -> Path:
    current = Path.cwd().resolve()
    for candidate in (current,) + tuple(current.parents):
        if (candidate / "capabilities/midplatform/core/context_foundation").is_dir():
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

    baseline = documents.get("context_foundation_module_baseline_v1.json", {})
    check(baseline.get("module_id") == "context_foundation", "baseline_module_id")
    check(baseline.get("module_status") == "BASELINE_READY", "baseline_module_status")
    check(baseline.get("owner") == "Context_Foundation", "baseline_owner")
    check(baseline.get("owner_count") == 1, "baseline_unique_owner")
    check(baseline.get("status") == "FROZEN", "baseline_frozen")
    check(baseline.get("runtime_activated") is False, "baseline_no_runtime")
    check(baseline.get("active_schema") is False, "baseline_no_active_schema")
    check(baseline.get("active_contract") is False, "baseline_no_active_contract")
    required_responsibilities = {
        "Context Envelope Candidate assembly",
        "Projection Reference Management",
        "Context Trace Candidate management",
    }
    check(required_responsibilities <= set(baseline.get("responsibilities", [])), "baseline_responsibilities")
    forbidden_text = " ".join(baseline.get("forbidden_responsibilities", [])).lower()
    for token, check_id in [
        ("reality", "baseline_forbidden_reality"),
        ("memory", "baseline_forbidden_memory"),
        ("emotion", "baseline_forbidden_emotion"),
        ("intent", "baseline_forbidden_intent"),
        ("causal", "baseline_forbidden_causal"),
        ("decision", "baseline_forbidden_decision"),
        ("action", "baseline_forbidden_action"),
        ("runtime", "baseline_forbidden_runtime"),
    ]:
        check(token in forbidden_text, check_id)
    check("Context Envelope Candidate" in baseline.get("output_types", []), "baseline_envelope_output")
    check("Context Trace Candidate" in baseline.get("output_types", []), "baseline_trace_output")

    owner_review = (BASE / "context_foundation_owner_closure_review.md").read_text(encoding="utf-8")
    for token, check_id in [
        ("Context_Foundation", "owner_review_owner"),
        ("Context Envelope Assembly", "owner_review_envelope"),
        ("Projection Reference Management", "owner_review_projection"),
        ("Context Trace Candidate management", "owner_review_trace"),
        ("does not own", "owner_review_negative_boundary"),
        ("Reality or Field State", "owner_review_no_reality"),
        ("Memory or Experience", "owner_review_no_memory"),
        ("Intent", "owner_review_no_intent"),
        ("Causal Reasoning", "owner_review_no_causal"),
        ("Decision", "owner_review_no_decision"),
        ("Action", "owner_review_no_action"),
    ]:
        check(token in owner_review, check_id)

    io_contract = documents.get("context_foundation_io_closure_contract.json", {})
    check(io_contract.get("owner") == "Context_Foundation", "io_owner")
    check(io_contract.get("input_semantics") == "Owner Projection only", "io_projection_only")
    expected_input_owners = {
        "Field State System",
        "Observation Manager",
        "Memory System",
        "Self System",
        "Role System / Social Self",
        "Relationship System / Social Self",
        "Emotion Context Boundary / Integration Layer",
        "Mental Field Continuity source owners",
    }
    inputs = io_contract.get("inputs", [])
    check({item.get("source_owner") for item in inputs} == expected_input_owners, "io_input_owners")
    check(all(item.get("read_only") is True for item in inputs), "io_inputs_read_only")
    check(io_contract.get("primary_output") == "Context Envelope Candidate", "io_primary_output")
    check({"Action", "Decision", "Fact", "Intent"} <= set(io_contract.get("forbidden_outputs", [])), "io_forbidden_outputs")
    check(io_contract.get("candidate_only") is True, "io_candidate_only")
    check(io_contract.get("source_owner_transfer") is False, "io_no_owner_transfer")
    check(io_contract.get("source_mutation_allowed") is False, "io_no_mutation")
    check(io_contract.get("active_contract") is False, "io_not_active")
    check(io_contract.get("runtime_integration") is False, "io_no_runtime")

    projection = documents.get("context_projection_governance_baseline.json", {})
    required_metadata = {"Source Owner", "Version", "Provenance", "Validity", "Confidence", "Unknown"}
    check(required_metadata <= set(projection.get("required_metadata", [])), "projection_required_metadata")
    rules = projection.get("governance_rules", {})
    for key in [
        "source_owner_required",
        "version_required",
        "provenance_required",
        "validity_required",
        "confidence_required_or_explicit_unknown",
        "unknown_preservation_required",
        "multiple_candidates_allowed",
        "contradiction_preservation_required",
        "current_reality_precedence",
        "read_only",
        "reference_only",
    ]:
        check(rules.get(key) is True, f"projection_true:{key}")
    for key in ["source_owner_transfer", "source_mutation_allowed", "fact_promotion_allowed"]:
        check(rules.get(key) is False, f"projection_false:{key}")
    check(projection.get("active_contract") is False, "projection_not_active")

    mental = (BASE / "mental_field_continuity_closure_review.md").read_text(encoding="utf-8")
    for token, check_id in [
        ("Context Input Reference", "mental_context_input_reference"),
        ("is not", "mental_negative_boundary"),
        ("Emotion Engine or Emotion State", "mental_not_emotion"),
        ("Memory or a Memory record", "mental_not_memory"),
        ("Causal Explanation", "mental_not_causal"),
        ("cannot override current Reality", "mental_reality_precedence"),
        ("reference-only Context input", "mental_reference_only"),
    ]:
        check(token in mental, check_id)

    resource = documents.get("context_resource_constraint_closure.json", {})
    check(set(resource.get("context_expansion_constraints", [])) == {"Hardware", "Runtime", "Cognitive Resource"}, "resource_constraints")
    check(resource.get("insufficient_resource_result") == "Degraded Context Scope Candidate", "resource_degraded_candidate")
    check(resource.get("resource_insufficiency_is_context_failure") is False, "resource_not_failure")
    for key in [
        "fixed_depth_allowed",
        "static_layer_limit_allowed",
        "numeric_limit_owned_by_context",
        "budget_mutation_allowed",
        "hardware_control_allowed",
        "runtime_control_allowed",
        "model_switching_allowed",
        "active_contract",
    ]:
        check(resource.get(key) is False, f"resource_false:{key}")
    resource_text = " ".join(flatten_strings(resource)).lower()
    for token, check_id in [("depth=3", "resource_no_depth_3"), ("depth=5", "resource_no_depth_5"), ("max_context_layer", "resource_no_max_layer")]:
        check(token not in resource_text, check_id)

    unknown = documents.get("context_unknown_resolution_closure.json", {})
    check(unknown.get("candidate_completion_allowed") is True, "unknown_candidate_allowed")
    check(set(unknown.get("completion_sources", [])) == {"Historical Experience", "Memory Pattern", "System Rule"}, "unknown_sources")
    check(unknown.get("completion_output") == "Unknown Completion Candidate", "unknown_output")
    check(unknown.get("multiple_candidates_allowed") is True, "unknown_multiple")
    check(unknown.get("current_reality_precedence") is True, "unknown_reality_precedence")
    for key in [
        "fact_promotion_allowed",
        "automatic_memory_write_allowed",
        "intent_generation_allowed",
        "causal_conclusion_allowed",
        "decision_generation_allowed",
        "action_generation_allowed",
        "active_contract",
    ]:
        check(unknown.get(key) is False, f"unknown_false:{key}")

    pcn = documents.get("context_to_pcn_handoff_contract_candidate.json", {})
    check(pcn.get("producer") == "Context_Foundation", "pcn_producer")
    check(pcn.get("consumer") == "Personal Cognitive Network Governance", "pcn_consumer")
    check(pcn.get("handoff_direction") == "Context Envelope Candidate -> PCN", "pcn_direction")
    check(pcn.get("accepted_input") == "Context Envelope Candidate", "pcn_input")
    check({"Current Context", "Related Projection", "Activation Reference", "Provenance"} <= set(pcn.get("provided_references", [])), "pcn_references")
    check(pcn.get("pcn_entry_consumes_context_handoff_only") is True, "pcn_context_only")
    check({"Decision", "Causal Result"} <= set(pcn.get("forbidden_handoff_outputs", [])), "pcn_forbidden")
    check(pcn.get("source_owner_precedence") is True, "pcn_owner_precedence")
    check(pcn.get("source_owner_transfer") is False, "pcn_no_owner_transfer")
    check(pcn.get("pcn_source_object_ownership") is False, "pcn_no_source_ownership")
    check(pcn.get("implementation_started") is False, "pcn_not_started")
    check(pcn.get("active_contract") is False, "pcn_not_active")

    summary = (BASE / "context_foundation_closure_summary.md").read_text(encoding="utf-8")
    for token, check_id in [
        ("MODULE_CLOSURE_CANDIDATE", "summary_status"),
        ("Context remains cognitive infrastructure, not a cognitive subject", "summary_context_position"),
        ("Planning, Alignment Update, Controlled Skeleton, and Controlled DryRun Validation", "summary_phase_coverage"),
        ("Context Envelope Candidate", "summary_envelope"),
        ("Mental Field Continuity is frozen as a Context Input Reference", "summary_mental"),
        ("no fixed depth", "summary_no_fixed_depth"),
        ("Unknown Completion Candidate", "summary_unknown"),
        ("Future PCN planning", "summary_pcn_planning"),
        ("Do not enter PCN implementation", "summary_stop"),
    ]:
        check(token in summary, check_id)

    manifest = documents.get("context_foundation_closure_change_manifest.json", {})
    check(set(manifest.get("created_files", [])) == REQUIRED_FILES, "manifest_files")
    for key in ["modified_existing_files", "deleted_files", "moved_files", "renamed_files"]:
        check(manifest.get(key) == [], f"manifest_empty:{key}")
    check(manifest.get("baseline_created") is True, "manifest_baseline_created")
    for key in [
        "runtime_changed",
        "schema_changed",
        "contract_changed",
        "pcn_started",
        "implementation_expanded",
        "context_skeleton_changed",
        "planning_assets_changed",
        "alignment_assets_changed",
        "dryrun_assets_changed",
        "active_schema_or_contract_created",
    ]:
        check(manifest.get(key) is False, f"manifest_false:{key}")
    hashes = manifest.get("protected_skeleton_baseline_hashes", {})
    check(len(hashes) == 9, "protected_hash_count")
    code_dir = repo_root / "capabilities/midplatform/core/context_foundation"
    for name, expected in sorted(hashes.items()):
        path = code_dir / name
        check(path.is_file(), f"protected_file_exists:{name}")
        check(path.is_file() and sha256(path) == expected, f"protected_hash:{name}")

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
    check(phase.get("execution_profile") == "Closure Validation", "phase_profile")
    check(bool(phase.get("execution_mode_normalization_reason")), "phase_normalization")
    check(phase.get("previous_phase_decision") == "LUNA_CONTEXT_FOUNDATION_CONTROLLED_DRYRUN_VALIDATION_READY", "phase_previous_decision")
    authority = phase.get("verification_authority", {})
    check(authority.get("V0") == "Agent", "authority_v0")
    check(authority.get("V1") == "NOT_AUTHORIZED", "authority_v1")
    check(authority.get("V2") == "USER_TERMINAL_ONLY", "authority_v2")
    check(authority.get("V3") == "CHATGPT_ONLY", "authority_v3")
    check(phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_stop")
    check(phase.get("expected_success_decision") == READY, "phase_ready")
    check(phase.get("current_status_contract") == "WAITING_FOR_USER_TERMINAL_VERIFICATION", "phase_current_status")
    check(phase.get("implementation_expansion") is False, "phase_no_implementation")
    check(phase.get("runtime_integration") is False, "phase_no_runtime")
    check(phase.get("schema_changed") is False, "phase_no_schema_change")
    check(phase.get("contract_changed") is False, "phase_no_contract_change")
    check(phase.get("pcn_started") is False, "phase_no_pcn")
    check(phase.get("next_phase_auto_entry") is False, "phase_no_auto_next")
    check(len(phase.get("required_final_files", [])) == len(REQUIRED_FILES), "phase_file_count")
    check(all((repo_root / path).exists() for path in phase.get("required_final_files", [])), "phase_references_exist")

    try:
        source = (BASE / "verify_context_foundation_module_closure_v1.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        compile(source, str(BASE / "verify_context_foundation_module_closure_v1.py"), "exec")
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
    check(imports <= {"__future__", "ast", "hashlib", "json", "pathlib", "typing"}, "verifier_standard_library_only")
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
