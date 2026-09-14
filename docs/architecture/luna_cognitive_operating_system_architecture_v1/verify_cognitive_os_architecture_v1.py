"""V0 static verifier for Luna Cognitive Operating System architecture.

Planning Only: parses contracts and performs structural checks without
importing or activating any Runtime, Scheduler, Model, Hardware, Provider, or
Action implementation.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent
JSON_ASSETS = (
    "cognitive_os_layer_definition_v1.json",
    "module_lifecycle_system_v1.json",
    "cognitive_flow_controller_contract_v1.json",
    "cognitive_interrupt_contract_v1.json",
    "state_management_system_v1.json",
    "event_system_contract_v1.json",
    "trace_system_schema_v1.json",
    "recovery_system_contract_v1.json",
    "contract_enforcement_system_v1.json",
    "admission_system_contract_v1.json",
    "health_monitoring_system_v1.json",
    "cognitive_os_module_interface_v1.json",
    "cognitive_os_dependency_map_v1.json",
)
MD_ASSETS = (
    "luna_cognitive_os_architecture_v1.md",
    "luna_cognitive_os_whitebox_v1.md",
    "luna_cognitive_os_go_no_go_v1.md",
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

    layer = data.get("cognitive_os_layer_definition_v1.json", {})
    lifecycle = data.get("module_lifecycle_system_v1.json", {})
    flow = data.get("cognitive_flow_controller_contract_v1.json", {})
    interrupt = data.get("cognitive_interrupt_contract_v1.json", {})
    state = data.get("state_management_system_v1.json", {})
    event = data.get("event_system_contract_v1.json", {})
    trace = data.get("trace_system_schema_v1.json", {})
    recovery = data.get("recovery_system_contract_v1.json", {})
    enforcement = data.get("contract_enforcement_system_v1.json", {})
    admission = data.get("admission_system_contract_v1.json", {})
    health = data.get("health_monitoring_system_v1.json", {})
    interface = data.get("cognitive_os_module_interface_v1.json", {})
    dependency = data.get("cognitive_os_dependency_map_v1.json", {})

    required_subsystems = {"Module Lifecycle System", "Cognitive Flow Controller", "State Management System", "Event System", "Trace System", "Recovery System", "Contract Enforcement System", "Admission System", "Health Monitoring System"}
    check(layer.get("layer") == "L1", "l1_layer_id")
    check(required_subsystems.issubset(set(layer.get("children", []))), "l1_subsystems_complete")
    check(layer.get("rules", {}).get("runtime_not_activated") is True, "l1_runtime_not_activated")
    check("Decision ownership" in layer.get("not_authority", []), "l1_not_decision_owner")

    lifecycle_states = set(lifecycle.get("states", []))
    check({"Proposed", "Registered", "Validated", "Admitted", "Active", "Suspended", "Recovered", "Deprecated", "Archived"}.issubset(lifecycle_states), "lifecycle_states")
    check(set(lifecycle.get("required_record", [])) == {"module_id", "owner", "layer", "version", "contract", "dependency", "state"}, "lifecycle_record")
    check(len(lifecycle.get("transitions", [])) >= 8, "lifecycle_transitions")
    check(lifecycle.get("rules", {}).get("bypass_forbidden") is True, "lifecycle_no_bypass")

    flow_nodes = {node.get("node_id") for node in flow.get("nodes", [])}
    check({"observe", "context", "attention", "hypothesis", "evaluate", "brain", "feedback", "learning"}.issubset(flow_nodes), "flow_nodes")
    check(flow.get("ordering", [])[0:3] == ["observe", "context", "attention"], "flow_order_prefix")
    check(flow.get("rules", {}).get("controller_not_brain") is True, "flow_controller_boundary")
    check(flow.get("rules", {}).get("event_cannot_direct_action") is True, "flow_event_action_guard")

    check({"priority", "source", "current_node", "resume_point"}.issubset(set(interrupt.get("required_fields", []))), "interrupt_fields")
    check({"Reflex Signal", "Safety Event", "Capability Failure", "State Conflict"}.issubset(set(interrupt.get("interrupt_sources", []))), "interrupt_sources")
    check(interrupt.get("rules", {}).get("resume_point_required") is True, "interrupt_resume_rule")

    state_records = state.get("states", [])
    state_ids = [row.get("state_id") for row in state_records]
    check(len(state_ids) == len(set(state_ids)), "state_ids_unique")
    required_state_fields = {"state_id", "owner", "writer", "reader", "lifecycle"}
    check(all(required_state_fields.issubset(row) for row in state_records), "state_ownership_fields")
    check(all(row.get("owner") and row.get("writer") and row.get("reader") for row in state_records), "state_owner_writer_reader")
    check(state.get("rules", {}).get("single_writer") is True, "state_single_writer")
    check(state.get("rules", {}).get("snapshot_before_recovery") is True, "state_snapshot_rule")

    check(set(event.get("event_types", [])) == {"External Event", "Internal Event", "System Event"}, "event_types")
    check({"event_id", "source", "timestamp", "target", "payload", "trace_id"}.issubset(set(event.get("schema", []))), "event_schema")
    check({"Created", "Validated", "Routed", "Consumed", "Acknowledged", "Expired", "Archived"}.issubset(set(event.get("lifecycle", []))), "event_lifecycle")
    check("Event → direct Action" in event.get("forbidden", []), "event_no_direct_action")

    check({"trace_id", "timestamp", "input", "evidence", "context", "state_snapshot", "attention", "decision_candidate", "outcome", "learning_candidate"}.issubset(set(trace.get("trace_fields", []))), "trace_fields")
    check(trace.get("rules", {}).get("provenance_required") is True, "trace_provenance")
    check(trace.get("rules", {}).get("trace_not_authority") is True, "trace_not_authority")

    check(recovery.get("recovery_order") == ["Diagnose", "Degrade", "Recover", "Resume", "Escalate"], "recovery_order")
    check({"Module Failure", "Capability Failure", "State Conflict", "Flow Interruption"}.issubset(set(recovery.get("failure_types", []))), "recovery_failure_types")
    check(recovery.get("rules", {}).get("degrade_before_stop") is True, "recovery_degrade_first")
    check(recovery.get("rules", {}).get("recovery_not_goal_owner") is True, "recovery_not_goal_owner")

    check({"Input Contract", "Output Contract", "Permission Contract", "Boundary Contract"}.issubset(set(enforcement.get("contract_types", []))), "enforcement_contract_types")
    check("permission" in " ".join(enforcement.get("checks", [])), "enforcement_permission_check")
    check(enforcement.get("rules", {}).get("enforcement_before_active") is True, "enforcement_before_active")

    check(admission.get("stages", [])[0:2] == ["Proposal", "Registry"], "admission_prefix")
    check({"Contract Check", "Dependency Check", "Permission Check", "Health Check", "Admission"}.issubset(set(admission.get("stages", []))), "admission_checks")
    check(admission.get("rules", {}).get("no_bypass") is True, "admission_no_bypass")
    check(admission.get("rules", {}).get("no_auto_activation") is True, "admission_no_auto_activation")

    check({"Module Health", "State Health", "Contract Health", "Dependency Health"}.issubset(set(health.get("health_domains", []))), "health_domains")
    check({"module", "health", "issue", "recommendation"}.issubset(set(health.get("output_schema", []))), "health_output_schema")
    check(health.get("rules", {}).get("diagnostic_only") is True, "health_diagnostic_only")

    check({"module_id", "owner", "layer", "version", "contract", "dependency", "state"}.issubset(set(interface.get("required_fields", []))), "module_interface_fields")
    check(interface.get("rules", {}).get("contract_before_active") is True, "module_contract_before_active")
    check(interface.get("rules", {}).get("no_direct_action") is True, "module_no_direct_action")

    forbidden = set(dependency.get("forbidden_edges", []))
    check("Cognitive OS → Decision Ownership" in forbidden, "dependency_no_decision_ownership")
    check("Cognitive OS → Reality Modification" in forbidden, "dependency_no_reality_modification")
    check("Capability → Cognitive OS Control" in forbidden, "dependency_no_capability_control")
    check("Emotion → Runtime Control" in forbidden, "dependency_no_emotion_control")
    check(len(dependency.get("allowed_edges", [])) >= 5, "dependency_allowed_edges")
    check(dependency.get("rules", {}).get("l1_is_substrate_not_brain") is True, "dependency_l1_not_brain")

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
    print("READINESS: LUNA_COGNITIVE_OPERATING_SYSTEM_ARCHITECTURE_READY")
    print("NEXT: RETURN_COMPLETE_OUTPUT_TO_CHATGPT_FOR_V3_AUDIT")
    return 0


if __name__ == "__main__":
    sys.exit(main())
