#!/usr/bin/env python3
"""Read-only final phase verifier for Runtime Executor Architecture Planning v1."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path
from typing import Any, Dict


BASE = Path(__file__).resolve().parent
READY = "LUNA_RUNTIME_EXECUTOR_ARCHITECTURE_PLANNING_READY"
REMEDIATION = "LUNA_RUNTIME_EXECUTOR_ARCHITECTURE_PLANNING_REMEDIATION_REQUIRED"

REQUIRED_FILES = {
    "runtime_executor_architecture_plan_v1.md",
    "runtime_executor_owner_boundary_candidate_v1.json",
    "runtime_executor_concept_boundary_matrix_v1.json",
    "execution_request_schema_candidate_v1.json",
    "execution_state_model_candidate_v1.json",
    "execution_admission_contract_candidate_v1.json",
    "execution_permission_safety_final_gate_candidate_v1.json",
    "execution_idempotency_model_candidate_v1.json",
    "execution_attempt_retry_boundary_candidate_v1.json",
    "execution_timeout_cancellation_model_candidate_v1.json",
    "execution_partial_result_model_candidate_v1.json",
    "execution_failure_boundary_candidate_v1.json",
    "execution_rollback_responsibility_boundary_candidate_v1.json",
    "execution_scheduler_boundary_candidate_v1.json",
    "execution_task_manager_boundary_candidate_v1.json",
    "execution_adapter_device_boundary_candidate_v1.json",
    "execution_result_schema_candidate_v1.json",
    "execution_result_handoff_contract_candidate_v1.json",
    "execution_diagnostics_maintenance_boundary_candidate_v1.json",
    "execution_provenance_trace_schema_candidate_v1.json",
    "runtime_executor_negative_guards_v1.json",
    "runtime_executor_existing_asset_reuse_mapping_v1.json",
    "runtime_executor_minimum_scenario_suite_v1.json",
    "runtime_executor_open_questions_registry_v1.json",
    "runtime_executor_planning_change_manifest_v1.json",
    "runtime_executor_architecture_planning_summary_v1.md",
    "phase_contract.json",
    "verify_runtime_executor_architecture_planning_v1.py",
}

JSON_FILES = {name for name in REQUIRED_FILES if name.endswith(".json")}


def load_json(path: Path) -> Dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain a JSON object")
    return value


def emit(checks: list[str], failures: list[str]) -> None:
    print("CHECKS")
    for item in checks:
        print(item)

    print("FAILED_CHECKS")
    for item in failures:
        print(item)

    print("PASSED_CHECK_COUNT")
    print(max(0, len(checks) - len(failures)))

    print("FAILED_CHECK_COUNT")
    print(len(failures))

    print("BLOCKER_COUNT")
    print(len(failures))

    print("FINAL_DECISION")
    print(READY if not failures else "BLOCKED_BY_VERIFIER_FAILURE")

    print("READINESS")
    print(READY if not failures else REMEDIATION)

    print("NEXT")
    print(
        "RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT"
        if not failures
        else "REMEDIATE_REPORTED_FAILURES_ONLY"
    )


def main() -> int:
    checks: list[str] = []
    failures: list[str] = []

    def check(condition: bool, check_id: str) -> None:
        checks.append(check_id)
        if not condition:
            failures.append(check_id)

    actual_files = {path.name for path in BASE.iterdir() if path.is_file()}
    check(actual_files == REQUIRED_FILES, "exact_required_file_set")

    docs: Dict[str, Dict[str, Any]] = {}
    for name in sorted(JSON_FILES):
        try:
            docs[name] = load_json(BASE / name)
            check(True, f"json_parse:{name}")
        except (OSError, TypeError, json.JSONDecodeError):
            docs[name] = {}
            check(False, f"json_parse:{name}")

    try:
        ast.parse(
            (BASE / "verify_runtime_executor_architecture_planning_v1.py").read_text(
                encoding="utf-8"
            )
        )
        check(True, "verifier_ast_parse")
    except SyntaxError:
        check(False, "verifier_ast_parse")

    owner = docs.get("runtime_executor_owner_boundary_candidate_v1.json", {})
    check(owner.get("canonical_owner") == "Runtime Executor", "canonical_owner")
    check(owner.get("unique_owner") is True, "canonical_owner_unique")
    aliases = owner.get("legacy_aliases", [])
    check(
        all(item.get("mutation_authority") is False for item in aliases),
        "legacy_alias_no_authority",
    )
    check(
        all(item.get("creates_new_owner") is False for item in aliases),
        "no_parallel_runtime_executor_owner",
    )

    concept = docs.get("runtime_executor_concept_boundary_matrix_v1.json", {})
    neq = concept.get("non_equivalence_guards", {})
    check(
        neq.get("action_candidate_not_execution_request") is True, "action_not_request"
    )
    check(
        neq.get("execution_readiness_not_execution") is True, "readiness_not_execution"
    )
    check(neq.get("executor_not_decision_governance") is True, "executor_not_decision")
    check(neq.get("executor_not_action_governance") is True, "executor_not_action")
    check(neq.get("executor_not_task_manager") is True, "executor_not_task_manager")
    check(neq.get("executor_not_scheduler") is True, "executor_not_scheduler")

    request_schema = docs.get("execution_request_schema_candidate_v1.json", {})
    req_required = set(request_schema.get("required", []))
    check("action_candidate_ref" in req_required, "request_has_action_ref")
    check("execution_readiness_ref" in req_required, "request_has_readiness_ref")
    check("candidate_only" in req_required, "request_candidate_only_required")
    check("planning_only" in req_required, "request_planning_only_required")

    state_model = docs.get("execution_state_model_candidate_v1.json", {})
    states = set(state_model.get("states", []))
    check("ADMITTED_CANDIDATE" in states, "state_admitted_present")
    check("PARTIAL_RESULT_CANDIDATE" in states, "state_partial_present")
    check("ROLLBACK_REQUIRED_CANDIDATE" in states, "state_rollback_required_present")

    admission = docs.get("execution_admission_contract_candidate_v1.json", {})
    a_rules = admission.get("admission_rules", {})
    check(
        a_rules.get("permission_recheck_required") is True,
        "admission_permission_recheck",
    )
    check(a_rules.get("safety_recheck_required") is True, "admission_safety_recheck")
    check(
        a_rules.get("unknown_not_auto_pass") is True, "admission_unknown_not_auto_pass"
    )

    final_gate = docs.get(
        "execution_permission_safety_final_gate_candidate_v1.json", {}
    )
    fg = final_gate.get("final_gate", {})
    check(fg.get("required") is True, "final_gate_required")
    check(fg.get("permission_still_valid") is True, "final_gate_permission")
    check(fg.get("safety_still_valid") is True, "final_gate_safety")
    check(fg.get("confirmation_not_revoked") is True, "final_gate_confirmation")

    idempotency = docs.get("execution_idempotency_model_candidate_v1.json", {})
    i_rules = idempotency.get("rules", {})
    check(
        i_rules.get("same_key_same_scope_reuse_previous_result_candidate") is True,
        "idempotency_reuse",
    )
    check(
        i_rules.get("same_key_different_scope_reject") is True,
        "idempotency_scope_reject",
    )

    retry = docs.get("execution_attempt_retry_boundary_candidate_v1.json", {})
    r_rules = retry.get("retry_rules", {})
    check(
        r_rules.get("retry_requires_explicit_authority") is True,
        "retry_explicit_authority",
    )
    check(r_rules.get("automatic_retry_forbidden") is True, "retry_no_automatic")
    check(
        r_rules.get("failure_only_not_retry_authority") is True,
        "retry_failure_not_authority",
    )

    timeout_cancel = docs.get(
        "execution_timeout_cancellation_model_candidate_v1.json", {}
    )
    tc_rules = timeout_cancel.get("rules", {})
    check(tc_rules.get("timeout_not_success") is True, "timeout_not_success")
    check(tc_rules.get("cancelled_not_suspended") is True, "cancelled_not_suspended")
    check(tc_rules.get("timeout_requires_trace") is True, "timeout_trace_required")

    partial = docs.get("execution_partial_result_model_candidate_v1.json", {})
    p_rules = partial.get("rules", {})
    check(p_rules.get("partial_result_not_success") is True, "partial_not_success")
    check(
        p_rules.get("partial_result_requires_explicit_terminal_followup") is True,
        "partial_followup_required",
    )

    failure = docs.get("execution_failure_boundary_candidate_v1.json", {})
    f_rules = failure.get("rules", {})
    check(f_rules.get("failure_requires_trace") is True, "failure_trace_required")
    check(f_rules.get("failure_not_auto_retry") is True, "failure_not_auto_retry")

    rollback = docs.get(
        "execution_rollback_responsibility_boundary_candidate_v1.json", {}
    )
    rb_rules = rollback.get("rules", {})
    check(
        rb_rules.get("rollback_not_action_governance_responsibility") is True,
        "rollback_not_action_owner",
    )
    check(
        rb_rules.get("rollback_not_decision_responsibility") is True,
        "rollback_not_decision_owner",
    )

    scheduler = docs.get("execution_scheduler_boundary_candidate_v1.json", {})
    s_rel = scheduler.get("relation", {})
    check(
        s_rel.get("executor_not_scheduler") is True,
        "scheduler_boundary_executor_not_scheduler",
    )
    check(
        s_rel.get("scheduler_not_executor") is True,
        "scheduler_boundary_scheduler_not_executor",
    )

    task = docs.get("execution_task_manager_boundary_candidate_v1.json", {})
    t_rel = task.get("relation", {})
    check(
        t_rel.get("executor_not_task_manager") is True,
        "task_boundary_executor_not_task",
    )
    check(
        t_rel.get("task_manager_reference_only") is True, "task_boundary_reference_only"
    )

    adapter = docs.get("execution_adapter_device_boundary_candidate_v1.json", {})
    ad = adapter.get("adapter_contract", {})
    check(ad.get("adapter_required") is True, "adapter_required")
    check(ad.get("device_isolated") is True, "adapter_device_isolated")
    check(
        ad.get("direct_device_control_by_executor") is False,
        "adapter_no_direct_device_control",
    )

    result_schema = docs.get("execution_result_schema_candidate_v1.json", {})
    rr = set(result_schema.get("required", []))
    check("status" in rr and "attempt_count" in rr, "result_required_fields")

    handoff = docs.get("execution_result_handoff_contract_candidate_v1.json", {})
    hguards = handoff.get("guards", {})
    check(
        handoff.get("handoff_kind") == "RUNTIME_EXECUTOR_RESULT_CANDIDATE_HANDOFF",
        "result_handoff_kind",
    )
    check(
        hguards.get("result_handoff_not_owner_mutation") is True,
        "result_handoff_no_owner_transfer",
    )

    diagnostics = docs.get(
        "execution_diagnostics_maintenance_boundary_candidate_v1.json", {}
    )
    db = diagnostics.get("maintenance_boundary", {})
    check(
        db.get("diagnostics_produce_evidence_only") is True, "diagnostics_evidence_only"
    )
    check(
        db.get("diagnostics_not_decision_owner") is True,
        "diagnostics_not_decision_owner",
    )

    trace = docs.get("execution_provenance_trace_schema_candidate_v1.json", {})
    tr = set(trace.get("required", []))
    check("attempt_refs" in tr and "result_ref" in tr, "trace_attempt_result_required")
    check(
        "failure_refs" in tr and "rollback_refs" in tr,
        "trace_failure_rollback_required",
    )
    check("scheduler_refs" in tr and "task_refs" in tr, "trace_scheduler_task_required")

    negative = docs.get("runtime_executor_negative_guards_v1.json", {})
    ng = set(negative.get("forbidden_events", []))
    check("action_candidate_equals_execution_request" in ng, "guard_action_not_request")
    check("execution_readiness_equals_execution" in ng, "guard_readiness_not_execution")
    check("automatic_retry" in ng, "guard_no_automatic_retry")

    scenarios = docs.get("runtime_executor_minimum_scenario_suite_v1.json", {})
    check(scenarios.get("scenario_count", 0) >= 18, "minimum_scenario_count")
    scenario_ids = {item.get("scenario_id") for item in scenarios.get("scenarios", [])}
    check(
        {"R01", "R06", "R08", "R10", "R12", "R15", "R18"} <= scenario_ids,
        "minimum_scenario_semantic_coverage",
    )

    reuse = docs.get("runtime_executor_existing_asset_reuse_mapping_v1.json", {})
    mapping = reuse.get("mapping", [])
    check(len(mapping) >= 6, "reuse_mapping_density")
    check(
        all(item.get("modification") is False for item in mapping),
        "reuse_mapping_no_modification",
    )

    open_questions = docs.get("runtime_executor_open_questions_registry_v1.json", {})
    check(len(open_questions.get("open_questions", [])) >= 3, "open_questions_present")

    manifest = docs.get("runtime_executor_planning_change_manifest_v1.json", {})
    check(manifest.get("new_files_only") is True, "manifest_new_files_only")
    check(
        manifest.get("modified_existing_assets") == [],
        "manifest_no_existing_modification",
    )

    phase = docs.get("phase_contract.json", {})
    check(phase.get("execution_mode") == "Planning Only", "phase_mode_planning_only")
    check(phase.get("planning_only") is True, "phase_planning_only_true")
    check(phase.get("runtime_executed") is False, "phase_runtime_executed_false")
    check(phase.get("scheduler_execution") is False, "phase_scheduler_execution_false")
    check(phase.get("task_lifecycle_mutation") is False, "phase_task_mutation_false")
    check(phase.get("device_control") is False, "phase_device_control_false")
    check(phase.get("database_write") is False, "phase_database_write_false")
    check(
        phase.get("agent_stop_point") == "WAITING_FOR_USER_TERMINAL_VERIFICATION",
        "phase_agent_stop_point",
    )

    emit(checks, failures)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
