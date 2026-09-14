"""V0 static verifier for Luna Capability Runtime Integration architecture.

Planning Only: no Provider, Model, Hardware, Scheduler, Runtime execution, or
Action implementation is imported or executed.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "capability_runtime_layer_definition_v1.json",
    "capability_executor_contract_v1.json",
    "execution_context_manager_contract_v1.json",
    "provider_adapter_contract_v1.json",
    "capability_runtime_lifecycle_v1.json",
    "resource_governance_contract_v1.json",
    "capability_scheduler_boundary_v1.json",
    "result_collector_contract_v1.json",
    "capability_health_manager_v1.json",
    "capability_cache_boundary_v1.json",
    "capability_runtime_trace_contract_v1.json",
    "capability_runtime_failure_contract_v1.json",
    "capability_runtime_os_interface_v1.json",
    "capability_runtime_boundary_dependency_v1.json",
)
MD_ASSETS = (
    "luna_capability_runtime_architecture_v1.md",
    "capability_runtime_whitebox_v1.md",
    "capability_runtime_go_no_go_v1.md",
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

    layer = data.get("capability_runtime_layer_definition_v1.json", {})
    executor = data.get("capability_executor_contract_v1.json", {})
    context = data.get("execution_context_manager_contract_v1.json", {})
    adapter = data.get("provider_adapter_contract_v1.json", {})
    lifecycle = data.get("capability_runtime_lifecycle_v1.json", {})
    resource = data.get("resource_governance_contract_v1.json", {})
    scheduler = data.get("capability_scheduler_boundary_v1.json", {})
    collector = data.get("result_collector_contract_v1.json", {})
    health = data.get("capability_health_manager_v1.json", {})
    cache = data.get("capability_cache_boundary_v1.json", {})
    trace = data.get("capability_runtime_trace_contract_v1.json", {})
    failure = data.get("capability_runtime_failure_contract_v1.json", {})
    os_interface = data.get("capability_runtime_os_interface_v1.json", {})
    boundary = data.get("capability_runtime_boundary_dependency_v1.json", {})

    required_subsystems = {"Capability Executor", "Execution Context Manager", "Provider Adapter Layer", "Capability Runtime Lifecycle", "Resource Governance", "Capability Runtime Scheduler Boundary", "Result Collector", "Capability Health Manager", "Capability Cache Boundary", "Runtime Trace Integration", "Runtime Failure Handler"}
    check(layer.get("layer") == "L4 Capability Runtime", "runtime_layer")
    check(required_subsystems.issubset(set(layer.get("subsystems", []))), "runtime_subsystems")
    check(layer.get("rules", {}).get("contract_only") is True, "runtime_contract_only")
    check(layer.get("rules", {}).get("provider_not_instantiated") is True, "runtime_no_provider")
    check(layer.get("rules", {}).get("runtime_execution_disabled") is True, "runtime_execution_disabled")
    check(set(layer.get("not_authority", [])) == {"Goal", "Decision", "Reality", "Constitution", "Action"}, "runtime_not_authority")

    check(executor.get("input") == "Admitted Capability Request", "executor_admitted_input")
    check(executor.get("pipeline", [])[0:3] == ["Capability Request", "Execution Context", "Capability Validation"], "executor_pipeline")
    check({"execution_id", "request_id", "capability_id", "provider_id", "status", "trace_id"}.issubset(set(executor.get("schema", []))), "executor_schema")
    check({"Goal creation", "Decision modification", "Reality modification", "Evidence Gateway bypass"}.issubset(set(executor.get("not_allowed", []))), "executor_boundary")
    check(executor.get("rules", {}).get("admission_required") is True, "executor_admission")
    check(executor.get("rules", {}).get("evidence_gateway_required") is True, "executor_evidence_gateway")

    check({"execution_id", "priority", "timeout", "resource_budget", "constraint", "caller", "trace_id"}.issubset(set(context.get("schema", []))), "context_schema")
    check({"full Brain state", "unrestricted Goal", "Identity secrets"}.issubset(set(context.get("forbidden_context", []))), "context_isolation")
    check(context.get("rules", {}).get("context_isolation") is True, "context_isolated")
    check(context.get("rules", {}).get("timeout_required") is True, "context_timeout")

    check(adapter.get("pipeline") == ["Capability", "Adapter", "Provider"], "adapter_pipeline")
    check({"Capability Request", "Execution Context", "Approved Input"}.issubset(set(adapter.get("adapter_input", []))), "adapter_input")
    check({"full cognitive state", "Goal authority", "Brain internals"}.issubset(set(adapter.get("provider_not_visible", []))), "provider_visibility")
    check(adapter.get("rules", {}).get("provider_isolated") is True, "provider_isolated")
    check(adapter.get("rules", {}).get("adapter_required") is True, "adapter_required")

    check({"Requested", "Validated", "Queued", "Executing", "Collected", "Result Validated", "Completed", "Archived", "Failed", "Degraded", "Recovered"}.issubset(set(lifecycle.get("states", []))), "lifecycle_states")
    check(lifecycle.get("normal_path", [])[0:4] == ["Requested", "Validated", "Queued", "Executing"], "lifecycle_normal_path")
    check(lifecycle.get("failure_path", []) == ["Failed", "Degraded", "Recovered", "Queued"], "lifecycle_failure_path")
    check(lifecycle.get("rules", {}).get("result_validation_required") is True, "lifecycle_result_validation")

    check(set(resource.get("resource_types", [])) == {"CPU", "GPU", "Memory", "Battery", "Network", "Latency"}, "resource_types")
    check({"capability", "max_latency", "resource_limit", "priority"}.issubset(set(resource.get("budget_schema", []))), "resource_schema")
    check(resource.get("rules", {}).get("capability_does_not_control_resource") is True, "resource_no_control")
    check(resource.get("rules", {}).get("budget_required") is True, "resource_budget")

    check({"Capability Request", "Priority", "Resource State", "Admission Result"}.issubset(set(scheduler.get("inputs", []))), "scheduler_inputs")
    check(scheduler.get("output") == "Execution Candidate", "scheduler_output")
    check({"Goal", "Decision", "Action", "Brain", "Reality"}.issubset(set(scheduler.get("not_authority", []))), "scheduler_boundary")
    check(scheduler.get("rules", {}).get("scheduler_not_implemented") is True, "scheduler_not_implemented")

    check(collector.get("pipeline") == ["Provider Output", "Raw Result", "Result Collector", "Evidence Gateway"], "collector_pipeline")
    check({"execution_id", "provider_reference", "content", "status", "timestamp", "trace_id"}.issubset(set(collector.get("raw_result_schema", []))), "collector_schema")
    check("Raw Result → Memory" in collector.get("direct_paths_forbidden", []), "collector_no_memory")
    check(collector.get("rules", {}).get("gateway_required") is True, "collector_gateway")

    check({"capability", "availability", "confidence", "performance", "limitation", "last_check"}.issubset(set(health.get("schema", []))), "health_schema")
    check({"Available", "Degraded", "Limited", "Unavailable", "Unknown"}.issubset(set(health.get("health_values", []))), "health_values")
    check(health.get("rules", {}).get("no_model_parameter_update") is True, "health_no_model_update")
    check(health.get("rules", {}).get("unknown_preserved") is True, "health_unknown")

    check({"Static Evidence", "Dynamic Evidence", "Sensitive Evidence"}.issubset(set(cache.get("cache_classes", []))), "cache_classes")
    check(cache.get("rules", {}).get("sensitive_not_cached") is True, "cache_sensitive")
    check(cache.get("rules", {}).get("unverified_not_cached") is True, "cache_unverified")
    check(cache.get("rules", {}).get("cache_not_reality") is True, "cache_not_reality")
    check(cache.get("rules", {}).get("cache_not_memory_owner") is True, "cache_not_memory_owner")

    check({"Capability Request", "Execution Context", "Provider Reference", "Result", "Evidence", "Cognitive Update"}.issubset(set(trace.get("chain", []))), "trace_chain")
    check({"trace_id", "request_id", "execution_id", "capability_id", "provider_reference", "result_reference", "evidence_reference"}.issubset(set(trace.get("fields", []))), "trace_fields")
    check(trace.get("rules", {}).get("provenance_required") is True, "trace_provenance")
    check(trace.get("rules", {}).get("trace_not_authority") is True, "trace_not_authority")

    check({"Provider Failure", "Timeout", "Resource Failure", "Result Invalid"}.issubset(set(failure.get("failure_types", []))), "failure_types")
    check(failure.get("pipeline") == ["Failure", "Diagnostics", "Degrade", "Alternative Capability", "Unknown"], "failure_pipeline")
    check(failure.get("rules", {}).get("unknown_preserved") is True, "failure_unknown")
    check(failure.get("rules", {}).get("no_auto_provider_switch") is True, "failure_no_auto_switch")

    check({"Lifecycle Contract", "Event Contract", "State Contract", "Trace Contract", "Resource Governance"}.issubset(set(os_interface.get("inputs", []))), "os_interface_inputs")
    check({"Constitution", "Governance Authority", "Brain", "Goal", "Decision", "Reality"}.issubset(set(os_interface.get("runtime_not_modify", []))), "os_interface_boundary")
    check(os_interface.get("rules", {}).get("l1_owns_lifecycle") is True, "os_interface_lifecycle")
    check(os_interface.get("rules", {}).get("runtime_does_not_control_os") is True, "runtime_no_os_control")

    forbidden = set(boundary.get("forbidden", []))
    for item in ("Provider → Brain", "Capability Runtime → Goal", "Capability Runtime → Decision", "Capability Runtime → Reality", "Capability Runtime → Constitution"):
        check(item in forbidden, f"dependency_guard:{item}")
    check(len(boundary.get("allowed", [])) >= 5, "dependency_allowed_edges")
    check(boundary.get("rules", {}).get("evidence_gateway_required") is True, "dependency_evidence_gateway")
    check(boundary.get("rules", {}).get("runtime_execution_disabled") is True, "dependency_runtime_disabled")
    check(boundary.get("rules", {}).get("no_model_calls") is True, "dependency_no_model")

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
    print("READINESS: LUNA_CAPABILITY_RUNTIME_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
