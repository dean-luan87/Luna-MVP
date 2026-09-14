"""V0 static verifier for Luna Action Runtime Foundation.

Planning Only: validates execution lifecycle, context, monitoring, outcome,
verification, recovery, and authority contracts without importing or executing
Action, Hardware, Robot, API, Device, Provider, or Runtime code.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "action_runtime_layer_definition_v1.json",
    "action_executor_contract_v1.json",
    "action_execution_context_v1.json",
    "action_lifecycle_manager_v1.json",
    "action_resource_governance_v1.json",
    "action_scheduler_boundary_v1.json",
    "action_execution_adapter_boundary_v1.json",
    "action_monitor_contract_v1.json",
    "action_outcome_collector_v1.json",
    "action_verification_contract_v1.json",
    "action_recovery_contract_v1.json",
    "action_runtime_trace_contract_v1.json",
    "action_runtime_os_interface_v1.json",
    "action_runtime_cognitive_interface_v1.json",
    "action_runtime_dependency_boundary_v1.json",
)
MD_ASSETS = (
    "luna_action_runtime_foundation_architecture_v1.md",
    "action_runtime_whitebox_v1.md",
    "action_runtime_go_no_go_v1.md",
)


def main() -> int:
    failures: list[str] = []
    checks = 0

    def check(condition: bool, name: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(name)

    data: dict[str, dict] = {}
    for name in JSON_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_json:{name}")
        if path.is_file():
            try:
                data[name] = json.loads(path.read_text(encoding="utf-8"))
                check(True, f"json_parse:{name}")
            except (OSError, json.JSONDecodeError):
                check(False, f"json_parse:{name}")
    for name in MD_ASSETS:
        path = BASE / name
        check(path.is_file(), f"missing_md:{name}")
        if path.is_file():
            check(bool(path.read_text(encoding="utf-8", errors="replace").strip()), f"nonempty_md:{name}")

    layer = data.get("action_runtime_layer_definition_v1.json", {})
    executor = data.get("action_executor_contract_v1.json", {})
    context = data.get("action_execution_context_v1.json", {})
    lifecycle = data.get("action_lifecycle_manager_v1.json", {})
    resource = data.get("action_resource_governance_v1.json", {})
    scheduler = data.get("action_scheduler_boundary_v1.json", {})
    adapter = data.get("action_execution_adapter_boundary_v1.json", {})
    monitor = data.get("action_monitor_contract_v1.json", {})
    outcome = data.get("action_outcome_collector_v1.json", {})
    verification = data.get("action_verification_contract_v1.json", {})
    recovery = data.get("action_recovery_contract_v1.json", {})
    trace = data.get("action_runtime_trace_contract_v1.json", {})
    os_interface = data.get("action_runtime_os_interface_v1.json", {})
    core_interface = data.get("action_runtime_cognitive_interface_v1.json", {})
    boundary = data.get("action_runtime_dependency_boundary_v1.json", {})

    required_subsystems = {"Action Executor", "Execution Context Manager", "Action Lifecycle Manager", "Action Resource Governance", "Action Scheduler Boundary", "Execution Adapter Boundary", "Action Monitor", "Outcome Collector", "Action Verification", "Action Recovery", "Action Trace Integration"}
    check(layer.get("layer") == "Action Boundary → External Execution Foundation", "runtime_layer")
    check(required_subsystems.issubset(set(layer.get("subsystems", []))), "runtime_subsystems")
    check(layer.get("rules", {}).get("contract_only") is True, "runtime_contract_only")
    check(layer.get("rules", {}).get("execution_disabled") is True, "runtime_execution_disabled")
    check(layer.get("rules", {}).get("external_side_effect_disabled") is True, "runtime_no_side_effect")

    check(executor.get("input") == "Approved Action Candidate", "executor_approved_input")
    check(executor.get("pipeline", [])[0:3] == ["Approved Action", "Execution Context", "Executor"], "executor_pipeline")
    check({"execution_id", "action_id", "executor_id", "status", "trace_id"}.issubset(set(executor.get("schema", []))), "executor_schema")
    check({"Modify Memory", "Modify Value", "Modify Goal", "Replan", "Re-Decide"}.issubset(set(executor.get("not_allowed", []))), "executor_not_allowed")
    check(executor.get("rules", {}).get("approval_required") is True, "executor_approval")
    check(executor.get("rules", {}).get("executor_not_implemented") is True, "executor_not_implemented")

    check({"execution_id", "action_type", "target", "environment", "permission", "risk_level", "timeout", "trace_id"}.issubset(set(context.get("schema", []))), "context_schema")
    check({"unrestricted Brain state", "unbounded Goal", "implicit permission"}.issubset(set(context.get("forbidden_context", []))), "context_isolation")
    check(context.get("rules", {}).get("boundary_required") is True, "context_boundary")
    check(context.get("rules", {}).get("permission_required") is True, "context_permission")

    check({"Requested", "Validated", "Approved", "Ready", "Executing", "Completed", "Verified", "Archived", "Rejected", "Failed", "Interrupted", "Cancelled", "Recovered"}.issubset(set(lifecycle.get("states", []))), "lifecycle_states")
    check(lifecycle.get("normal_path", [])[0:5] == ["Requested", "Validated", "Approved", "Ready", "Executing"], "lifecycle_normal_path")
    check(lifecycle.get("rules", {}).get("approval_before_ready") is True, "lifecycle_approval")
    check(lifecycle.get("rules", {}).get("verification_before_archive") is True, "lifecycle_verification")

    check({"Time", "Energy", "Network", "Device", "Permission", "Environment Condition"}.issubset(set(resource.get("resources", []))), "resource_types")
    check({"action", "resource", "budget", "limit", "status"}.issubset(set(resource.get("schema", []))), "resource_schema")
    check(resource.get("rules", {}).get("action_cannot_request_unlimited") is True, "resource_no_unlimited")
    check(resource.get("rules", {}).get("budget_required") is True, "resource_budget")

    check({"Approved Action", "Priority", "Resource State", "Environment"}.issubset(set(scheduler.get("inputs", []))), "scheduler_inputs")
    check(scheduler.get("output") == "Execution Candidate", "scheduler_output")
    check({"Goal", "Decision", "Value", "Action Permission", "Constitution"}.issubset(set(scheduler.get("not_authority", []))), "scheduler_boundary")
    check(scheduler.get("rules", {}).get("scheduler_not_implemented") is True, "scheduler_not_implemented")

    check(adapter.get("pipeline") == ["Action Runtime", "Adapter", "External Executor"], "adapter_pipeline")
    check({"Execution Candidate", "Execution Context", "Approved Permission"}.issubset(set(adapter.get("adapter_input", []))), "adapter_input")
    check({"specific device internals", "unbounded API authority"}.issubset(set(adapter.get("runtime_not_know", []))), "adapter_isolation")
    check(adapter.get("rules", {}).get("external_executor_future_only") is True, "adapter_future_only")

    check({"status", "time", "deviation", "exception", "environment_change"}.issubset(set(monitor.get("observes", []))), "monitor_observes")
    check({"monitor_id", "execution_id", "observation", "deviation", "threshold", "trace_id"}.issubset(set(monitor.get("schema", []))), "monitor_schema")
    check(monitor.get("rules", {}).get("monitor_not_executor") is True, "monitor_not_executor")
    check(monitor.get("rules", {}).get("environment_change_revalidates") is True, "monitor_revalidate")

    check(outcome.get("pipeline") == ["Execution", "Raw Outcome", "Outcome Collector", "Verification"], "outcome_pipeline")
    check({"outcome_id", "execution_id", "expected", "actual", "difference", "confidence", "timestamp"}.issubset(set(outcome.get("schema", []))), "outcome_schema")
    check(outcome.get("rules", {}).get("raw_outcome_not_evidence_until_verified") is True, "outcome_verification_gate")
    check(outcome.get("rules", {}).get("difference_required") is True, "outcome_difference")

    check(verification.get("pipeline") == ["Expected Outcome", "Actual Outcome", "Difference", "Feedback Signal"], "verification_pipeline")
    check({"Confirmed", "Partial Success", "Failed", "Unexpected", "Unknown"}.issubset(set(verification.get("verification_states", []))), "verification_states")
    check(verification.get("rules", {}).get("expectation_feedback_bound") is True, "verification_feedback")
    check(verification.get("rules", {}).get("partial_success_supported") is True, "verification_partial")

    check({"Execution Failure", "Environment Change", "Permission Change", "Unexpected Outcome"}.issubset(set(recovery.get("failure_types", []))), "recovery_types")
    check(recovery.get("pipeline") == ["Failure", "Diagnosis", "Retry Candidate", "Alternative Action", "Abort"], "recovery_pipeline")
    check(recovery.get("rules", {}).get("goal_immutable") is True, "recovery_goal_guard")
    check(recovery.get("rules", {}).get("value_immutable") is True, "recovery_value_guard")
    check(recovery.get("rules", {}).get("no_auto_retry") is True, "recovery_no_auto_retry")

    check({"Observation", "Context", "Decision", "Action Request", "Validation", "Execution", "Outcome", "Learning"}.issubset(set(trace.get("chain", []))), "trace_chain")
    check({"trace_id", "observation_reference", "context_reference", "decision_reference", "action_request_reference", "validation_reference", "execution_reference", "outcome_reference"}.issubset(set(trace.get("fields", []))), "trace_fields")
    check(trace.get("rules", {}).get("provenance_required") is True, "trace_provenance")
    check(trace.get("rules", {}).get("trace_not_authority") is True, "trace_not_authority")

    check({"Lifecycle", "Event", "State", "Recovery", "Trace", "Resource Governance"}.issubset(set(os_interface.get("inputs", []))), "os_interface_inputs")
    check({"Governance", "Constitution", "Runtime Rules", "Decision Authority"}.issubset(set(os_interface.get("runtime_not_modify", []))), "os_interface_boundary")
    check(os_interface.get("rules", {}).get("l1_owns_lifecycle") is True, "os_interface_lifecycle")
    check({"Approved Action", "Intent", "Goal Reference", "Context", "Constraints", "Expectation"}.issubset(set(core_interface.get("inputs", []))), "core_interface_inputs")
    check({"Goal", "Decision", "Value", "Brain", "Reality", "Learning Policy"}.issubset(set(core_interface.get("runtime_not_own", []))), "core_interface_boundary")
    check(core_interface.get("rules", {}).get("approved_input_required") is True, "core_approved_input")
    check(core_interface.get("rules", {}).get("runtime_not_decision_owner") is True, "core_not_decision_owner")

    forbidden = set(boundary.get("forbidden", []))
    for item in ("Action Runtime → Goal Ownership", "Action Runtime → Decision Ownership", "Action Runtime → Value Modification", "Action Runtime → Constitution Modification", "Executor → Direct Cognitive Control"):
        check(item in forbidden, f"dependency_guard:{item}")
    check(len(boundary.get("allowed", [])) >= 5, "dependency_allowed_edges")
    check(boundary.get("rules", {}).get("approved_candidate_required") is True, "dependency_approval")
    check(boundary.get("rules", {}).get("execution_disabled") is True, "dependency_execution_disabled")
    check(boundary.get("rules", {}).get("no_external_side_effect") is True, "dependency_no_side_effect")

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_ast = ast.parse(verifier_text, filename=str(Path(__file__)))
    imports = set()
    for node in ast.walk(verifier_ast):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".")[0])
    check(not imports.intersection({"subprocess", "socket", "requests", "cv2", "torch"}), "planning_no_runtime_import")
    compile(verifier_text, str(Path(__file__)), "exec")
    check(True, "planning_verifier_compile")

    passed = checks - len(failures)
    print(f"CHECKS: {checks}")
    print(f"FAILED_CHECKS: {failures}")
    print(f"PASSED_CHECK_COUNT: {passed}")
    print(f"FAILED_CHECK_COUNT: {len(failures)}")
    print(f"BLOCKER_COUNT: {len(failures)}")
    if failures:
        print("FINAL_DECISION: BLOCKED_BY_VERIFIER_FAILURE")
        print("NEXT: REMEDIATE_REPORTED_FAILURES_ONLY")
        return 1
    print("FINAL_DECISION: V2_FINAL_VERIFICATION_PASSED")
    print("READINESS: LUNA_ACTION_RUNTIME_FOUNDATION_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
